#!/usr/bin/env python3
"""Convert Bedrock loot tables to Java Edition format."""
import json, os

SRC = "/tmp/opencode/m_addon/[v1.0.0] More Simple Structures - BP/loot_tables/coreblockstudios/moresimplestructures"
DST = "/tmp/opencode/mss_mod/src/main/resources/data/mss/loot_table"

ID_MAP = {
    "minecraft:web": "minecraft:cobweb",
    "minecraft:horsearmoriron": "minecraft:iron_horse_armor",
    "minecraft:horsearmorgold": "minecraft:golden_horse_armor",
    "minecraft:horsearmordiamond": "minecraft:diamond_horse_armor",
    "minecraft:record_13": "minecraft:music_disc_13",
    "minecraft:record_cat": "minecraft:music_disc_cat",
}

def convert_table(data):
    """Convert a Bedrock loot table to Java format."""
    pools = []
    for pool in data.get("pools", []):
        rolls = pool.get("rolls", 1)
        if isinstance(rolls, dict):
            rolls = {"min": rolls["min"], "max": rolls["max"]}
            rolls_type = "uniform"
        else:
            rolls = rolls
            rolls_type = "fixed"
        
        entries = []
        for entry in pool.get("entries", []):
            if entry.get("type") == "empty":
                entries.append({
                    "type": "minecraft:empty",
                    "weight": entry.get("weight", 1)
                })
                continue
            
            name = entry.get("name", "minecraft:air")
            name = ID_MAP.get(name, name)
            
            java_entry = {
                "type": "minecraft:item",
                "name": name,
                "weight": entry.get("weight", 1)
            }
            
            functions = []
            for func in entry.get("functions", []):
                fname = func.get("function", "")
                if fname == "set_count":
                    count = func.get("count", 1)
                    if isinstance(count, dict):
                        functions.append({
                            "function": "minecraft:set_count",
                            "count": {"type": "minecraft:uniform", "min": count["min"], "max": count["max"]}
                        })
                    else:
                        functions.append({
                            "function": "minecraft:set_count",
                            "count": count
                        })
                elif fname == "enchant_with_levels":
                    functions.append({
                        "function": "minecraft:enchant_with_levels",
                        "levels": {"type": "minecraft:uniform", "min": func.get("levels", 30), "max": func.get("levels", 30)},
                        "treasure": func.get("treasure", False)
                    })
                elif fname == "enchant_randomly":
                    functions.append({
                        "function": "minecraft:enchant_randomly"
                    })
                elif fname == "set_data":
                    # For Java Edition, data values are usually item-specific
                    pass
            
            if functions:
                java_entry["functions"] = functions
            
            entries.append(java_entry)
        
        java_pool = {
            "rolls": rolls,
            "entries": entries
        }
        pools.append(java_pool)
    
    return {"pools": pools}

def main():
    for root, dirs, files in os.walk(SRC):
        for fname in files:
            if not fname.endswith('.json'):
                continue
            src_path = os.path.join(root, fname)
            with open(src_path) as f:
                try:
                    data = json.load(f)
                except:
                    print(f"  ✗ {fname}: invalid JSON")
                    continue
            
            java_data = convert_table(data)
            
            # Determine output path
            rel = os.path.relpath(src_path, SRC)
            dst_path = os.path.join(DST, rel)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            
            with open(dst_path, 'w') as f:
                json.dump(java_data, f, indent=2)
            print(f"  ✓ {rel}")

if __name__ == "__main__":
    main()
