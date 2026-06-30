#!/usr/bin/env python3
"""Convert JSON structure files to gzip-compressed NBT for Minecraft Java."""
import json, os, gzip, struct

SNBT_DIR = "/tmp/opencode/mss_mod/src/main/resources/data/mss/structure"
OUTPUT_DIR = SNBT_DIR  # Replace .snbt with .nbt

TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12

def write_nbt_string(f, s):
    encoded = s.encode('utf-8')
    f.write(struct.pack('>H', len(encoded)))
    f.write(encoded)

def write_value(f, val, tag_type=None):
    if tag_type is None:
        if isinstance(val, dict): tag_type = TAG_COMPOUND
        elif isinstance(val, list): tag_type = TAG_LIST
        elif isinstance(val, str): tag_type = TAG_STRING
        elif isinstance(val, bool): tag_type = TAG_BYTE
        elif isinstance(val, int): tag_type = TAG_INT
        elif isinstance(val, float): tag_type = TAG_DOUBLE
        else: tag_type = TAG_STRING
    
    if tag_type == TAG_BYTE:
        f.write(struct.pack('>b', 1 if val else 0))
    elif tag_type == TAG_SHORT:
        f.write(struct.pack('>h', int(val)))
    elif tag_type == TAG_INT:
        f.write(struct.pack('>i', int(val)))
    elif tag_type == TAG_LONG:
        f.write(struct.pack('>q', int(val)))
    elif tag_type == TAG_FLOAT:
        f.write(struct.pack('>f', float(val)))
    elif tag_type == TAG_DOUBLE:
        f.write(struct.pack('>d', float(val)))
    elif tag_type == TAG_STRING:
        write_nbt_string(f, str(val))
    elif tag_type == TAG_LIST:
        if not val:
            f.write(struct.pack('>b', TAG_BYTE) + struct.pack('>i', 0))
            return
        elem_type = TAG_COMPOUND if isinstance(val[0], dict) else TAG_STRING
        f.write(struct.pack('>b', elem_type) + struct.pack('>i', len(val)))
        for item in val:
            write_value(f, item, elem_type)
    elif tag_type == TAG_COMPOUND:
        for k, v in val.items():
            if k == 'Properties':
                # Write properties as compound with string values
                if isinstance(v, dict) and v:
                    prop_dict = v
                elif isinstance(v, str):
                    # Parse "key=value,key2=value2" or JSON-like
                    continue
                else:
                    continue
                f.write(struct.pack('>b', TAG_COMPOUND))
                write_nbt_string(f, k)
                for pk, pv in prop_dict.items():
                    f.write(struct.pack('>b', TAG_STRING))
                    write_nbt_string(f, pk)
                    write_nbt_string(f, str(pv))
                f.write(struct.pack('>b', TAG_END))
            elif k in ('state',):
                f.write(struct.pack('>b', TAG_INT))
                write_nbt_string(f, k)
                f.write(struct.pack('>i', int(v)))
            elif isinstance(v, list):
                f.write(struct.pack('>b', TAG_LIST))
                write_nbt_string(f, k)
                write_value(f, v, TAG_LIST)
            elif isinstance(v, dict):
                f.write(struct.pack('>b', TAG_COMPOUND))
                write_nbt_string(f, k)
                write_value(f, v, TAG_COMPOUND)
            elif isinstance(v, str):
                f.write(struct.pack('>b', TAG_STRING))
                write_nbt_string(f, k)
                write_nbt_string(f, v)
            elif isinstance(v, bool):
                f.write(struct.pack('>b', TAG_BYTE))
                write_nbt_string(f, k)
                f.write(struct.pack('>b', 1 if v else 0))
            elif isinstance(v, int):
                f.write(struct.pack('>b', TAG_INT))
                write_nbt_string(f, k)
                f.write(struct.pack('>i', v))
            elif isinstance(v, float):
                f.write(struct.pack('>b', TAG_DOUBLE))
                write_nbt_string(f, k)
                f.write(struct.pack('>d', v))
        f.write(struct.pack('>b', TAG_END))
    elif tag_type == TAG_BYTE_ARRAY:
        f.write(struct.pack('>i', len(val)))
        f.write(bytes(val))
    elif tag_type == TAG_INT_ARRAY:
        f.write(struct.pack('>i', len(val)))
        for v in val:
            f.write(struct.pack('>i', int(v)))
    elif tag_type == TAG_LONG_ARRAY:
        f.write(struct.pack('>i', len(val)))
        for v in val:
            f.write(struct.pack('>q', int(v)))

def convert_json_blocks_to_structure(data):
    """Convert our JSON structure format to Minecraft NBT structure format."""
    # Minecraft structure NBT format:
    # {
    #   DataVersion: int
    #   size: [int, int, int]
    #   palette: [ { Name: "block", Properties: {...} }, ... ]
    #   blocks: [ { pos: [int,int,int], state: int }, ... ]
    #   entities: [ ... ]
    # }
    
    palette = data.get('palette', [])
    blocks = data.get('blocks', [])
    size = data.get('size', [0, 0, 0])
    data_version = data.get('DataVersion', 3955)
    
    # Normalize palette entries
    new_palette = []
    for entry in palette:
        if isinstance(entry, str):
            # "minecraft:block_name[props]" format
            if '[' in entry:
                name, props_str = entry.split('[', 1)
                props_str = props_str.rstrip(']')
                props = {}
                if props_str:
                    for p in props_str.split(','):
                        if '=' in p:
                            k, v = p.split('=', 1)
                            props[k] = v
                new_palette.append({"Name": name, "Properties": props if props else {}})
            else:
                new_palette.append({"Name": entry, "Properties": {}})
        elif isinstance(entry, dict):
            new_palette.append(entry)
    
    # Normalize blocks
    new_blocks = []
    for block in blocks:
        if isinstance(block, dict):
            new_blocks.append({
                "pos": block.get("pos", [0, 0, 0]),
                "state": int(block.get("state", 0))
            })
    
    output = {
        "DataVersion": data_version,
        "size": size if len(size) == 3 else [1, 1, 1],
        "palette": new_palette,
        "blocks": new_blocks,
        "entities": data.get('entities', [])
    }
    
    return output

def main():
    count = 0
    for fname in sorted(os.listdir(SNBT_DIR)):
        if not fname.endswith('.snbt') and not fname.endswith('.json_structure'):
            continue
        path = os.path.join(SNBT_DIR, fname)
        with open(path, 'r') as f:
            raw = f.read()
        
        try:
            data = json.loads(raw)
        except:
            print(f"  ✗ {fname} - not valid JSON")
            continue
        
        struct_data = convert_json_blocks_to_structure(data)
        nbt_name = fname.rsplit('.', 1)[0] + '.nbt'
        nbt_path = os.path.join(OUTPUT_DIR, nbt_name)
        
        with gzip.open(nbt_path, 'wb') as f:
            f.write(struct.pack('>b', TAG_COMPOUND))
            write_nbt_string(f, "")  # Root empty name
            # Write DataVersion
            f.write(struct.pack('>b', TAG_INT))
            write_nbt_string(f, "DataVersion")
            f.write(struct.pack('>i', struct_data["DataVersion"]))
            # Write size
            f.write(struct.pack('>b', TAG_LIST))
            write_nbt_string(f, "size")
            f.write(struct.pack('>b', TAG_INT) + struct.pack('>i', 3))
            for s in struct_data["size"]:
                f.write(struct.pack('>i', int(s)))
            # Write palette
            f.write(struct.pack('>b', TAG_LIST))
            write_nbt_string(f, "palette")
            palette = struct_data["palette"]
            f.write(struct.pack('>b', TAG_COMPOUND) + struct.pack('>i', len(palette)))
            for entry in palette:
                write_value(f, entry, TAG_COMPOUND)
            # Write blocks
            blocks = struct_data["blocks"]
            f.write(struct.pack('>b', TAG_LIST))
            write_nbt_string(f, "blocks")
            f.write(struct.pack('>b', TAG_COMPOUND) + struct.pack('>i', len(blocks)))
            for block in blocks:
                f.write(struct.pack('>b', TAG_LIST))
                write_nbt_string(f, "pos")
                f.write(struct.pack('>b', TAG_INT) + struct.pack('>i', 3))
                for p in block["pos"]:
                    f.write(struct.pack('>i', int(p)))
                f.write(struct.pack('>b', TAG_INT))
                write_nbt_string(f, "state")
                f.write(struct.pack('>i', block["state"]))
                # nbt (optional, but structure expects it)
                f.write(struct.pack('>b', TAG_COMPOUND))
                write_nbt_string(f, "nbt")
                f.write(struct.pack('>b', TAG_END))
            # Write entities
            f.write(struct.pack('>b', TAG_LIST))
            write_nbt_string(f, "entities")
            f.write(struct.pack('>b', TAG_COMPOUND) + struct.pack('>i', 0))
            f.write(struct.pack('>b', TAG_END))  # End root compound
        
        os.remove(path)
        print(f"  ✓ {fname} -> {nbt_name}")
        count += 1
    
    print(f"\nConverted {count} structures to NBT")

if __name__ == "__main__":
    main()
