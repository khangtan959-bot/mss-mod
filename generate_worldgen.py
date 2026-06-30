#!/usr/bin/env python3
"""Generate NeoForge 1.21.1 worldgen JSON files for structures."""
import json, os

OUT = "/tmp/opencode/mss_mod/src/main/resources/data/mss/worldgen"

# Map structures to their biome categories and weights based on the addon feature_rules
STRUCTURES = [
    # (name, biomes, weight, height_anchor, placement_type)
    # Overworld surface structures
    ("abandoned_castle_1", ["forest", "plains", "taiga", "swamp"], 330, "surface", "surface_pass"),
    ("abandoned_fort_1", ["forest", "swamp", "dark_forest", "birch_forest", "taiga"], 400, "surface", "surface_pass"),
    ("abandoned_house_1", ["forest", "plains", "taiga"], 500, "surface", "surface_pass"),
    ("altar_ruins_1", ["forest", "plains", "taiga", "birch_forest", "dark_forest", "savanna", "meadow"], 450, "surface", "surface_pass"),
    ("camp_1", ["forest", "plains", "taiga", "birch_forest", "dark_forest", "meadow", "swamp", "cherry_grove"], 350, "surface", "surface_pass"),
    ("cemetery_1", ["forest", "plains", "taiga", "dark_forest", "savanna"], 500, "surface", "surface_pass"),
    ("desert_pyramid_1", ["desert"], 330, "surface", "surface_pass"),
    ("desert_ruin_1", ["desert"], 500, "surface", "surface_pass"),
    ("desert_ruin_2", ["desert"], 500, "surface", "surface_pass"),
    ("desert_ruin_3", ["desert"], 500, "surface", "surface_pass"),
    ("evoker_tower", ["swamp", "dark_forest", "taiga"], 600, "surface", "surface_pass"),
    ("fishing_hut", ["beach"], 500, "surface", "surface_pass"),
    ("fishing_hut_ruin_1", ["beach"], 600, "surface", "surface_pass"),
    ("grave", ["forest", "plains", "taiga", "dark_forest", "savanna"], 600, "surface", "surface_pass"),
    ("haunted_house_1", ["dark_forest", "swamp"], 700, "surface", "surface_pass"),
    ("illager_fort_1", ["forest", "plains", "swamp", "meadow", "grove", "savanna"], 500, "surface", "surface_pass"),
    ("jungle_brazier", ["jungle"], 500, "surface", "surface_pass"),
    ("jungle_fort_ruin", ["jungle"], 500, "surface", "surface_pass"),
    ("jungle_pedastal", ["jungle"], 500, "surface", "surface_pass"),
    ("jungle_pyramid_1", ["jungle"], 400, "surface", "surface_pass"),
    ("jungle_statue_1", ["jungle"], 500, "surface", "surface_pass"),
    ("mangrove_hut", ["mangrove_swamp"], 500, "surface", "surface_pass"),
    ("mushroom_house", ["mushroom_fields"], 400, "surface", "surface_pass"),
    ("ocean_statue_1", ["ocean"], 600, "surface", "surface_pass"),
    ("pillager_cabin_1", ["forest", "taiga"], 500, "surface", "surface_pass"),
    ("pillager_camp", ["plains", "savanna", "forest", "meadow", "grove", "taiga"], 500, "surface", "surface_pass"),
    ("ruins_1", ["forest", "dark_forest", "plains", "taiga", "savanna"], 500, "surface", "surface_pass"),
    ("small_desert_totem_pillar_1", ["desert"], 500, "surface", "surface_pass"),
    ("desert_sphinx_1", ["desert"], 600, "surface", "surface_pass"),
    ("ss2", ["forest", "dark_forest", "plains", "taiga", "savanna"], 500, "surface", "surface_pass"),
    ("surface_dungeon_1", ["birch_forest", "forest", "dark_forest", "taiga"], 500, "surface", "surface_pass"),
    ("swamp_cabin_1", ["swamp"], 500, "surface", "surface_pass"),
    ("tall_rock_1", ["forest", "plains", "taiga", "savanna"], 400, "surface", "surface_pass"),
    ("trader_cart", ["forest", "plains", "taiga", "savanna", "desert", "meadow", "cherry_grove"], 500, "surface", "surface_pass"),
    ("trial_tower", ["forest", "plains", "taiga", "desert", "savanna", "jungle", "dark_forest", "swamp", "snowy_plains"], 800, "surface", "surface_pass"),
    ("watch_tower", ["forest", "taiga"], 500, "surface", "surface_pass"),
    ("well_ruin_1", ["forest", "plains", "taiga", "dark_forest", "savanna"], 500, "surface", "surface_pass"),
    ("wolf_den_1", ["forest", "dark_forest", "taiga", "savanna", "grove"], 500, "surface", "surface_pass"),
    ("pirate_ship_1", ["ocean", "deep_ocean"], 600, "surface", "surface_pass"),
    ("pirate_shipwreck_1", ["ocean", "deep_ocean"], 500, "surface", "surface_pass"),
    ("broken_conduit", ["ocean", "deep_ocean"], 500, "surface", "surface_pass"),
    # Underground
    ("spider_nest", ["overworld"], 150, "underground", "underground_pass"),
    ("underground_dungeon_1", ["overworld"], 500, "underground", "underground_pass"),
    ("cave_camp", ["overworld"], 500, "underground", "underground_pass"),
    # Nether
    ("piglin_boat", ["nether"], 500, "surface", "surface_pass"),
    ("piglin_fortress", ["nether"], 400, "surface", "surface_pass"),
    ("piglin_outpost", ["nether"], 500, "surface", "surface_pass"),
    # End
    ("end_ruin_banner", ["end"], 500, "surface", "surface_pass"),
    ("end_ruin_pillar_1", ["end"], 500, "surface", "surface_pass"),
    ("crashed_endship_1", ["end"], 400, "surface", "surface_pass"),
]

BIOME_MAP = {
    "forest": "minecraft:forest",
    "plains": "minecraft:plains",
    "taiga": "minecraft:taiga",
    "swamp": "minecraft:swamp",
    "dark_forest": "minecraft:dark_forest",
    "birch_forest": "minecraft:birch_forest",
    "savanna": "minecraft:savanna",
    "meadow": "minecraft:meadow",
    "desert": "minecraft:desert",
    "beach": "minecraft:beach",
    "jungle": "minecraft:jungle",
    "mangrove_swamp": "minecraft:mangrove_swamp",
    "mushroom_fields": "minecraft:mushroom_fields",
    "cherry_grove": "minecraft:cherry_grove",
    "grove": "minecraft:grove",
    "ocean": "minecraft:ocean",
    "deep_ocean": "minecraft:deep_ocean",
    "snowy_plains": "minecraft:snowy_plains",
    "nether": "minecraft:nether_wastes",
    "end": "minecraft:the_end",
    "overworld": "minecraft:overworld",
}

BIOME_TAGS = {
    "overworld": "#minecraft:is_overworld",
    "nether": "#minecraft:is_nether",
    "end": "#minecraft:is_end",
}

def generate_structure_json(name, biomes, weight, height_type, env):
    structure = {
        "type": "minecraft:jigsaw",
        "biomes": [],
        "step": "surface_structures",
        "spawn_overrides": {},
        "terrain_adaptation": "beard_thin",
        "start_pool": f"mss:{name}_pool",
        "size": 1,
        "start_height": {
            "absolute": 0
        } if height_type == "surface" else {
            "type": "minecraft:uniform",
            "max_inclusive": {"absolute": 32},
            "min_inclusive": {"absolute": -32}
        },
        "project_start_to_heightmap": "WORLD_SURFACE_WG" if height_type == "surface" else None,
        "max_distance_from_center": 80,
        "use_expansion_hack": False,
    }

    if biomes and biomes[0] in BIOME_TAGS:
        structure["biomes"] = BIOME_TAGS[biomes[0]]
    else:
        structure["biomes"] = [BIOME_MAP.get(b, f"minecraft:{b}") for b in biomes]

    return structure

def generate_pool_json(structure_name):
    return {
        "name": f"mss:{structure_name}_pool",
        "fallback": "minecraft:empty",
        "elements": [
            {
                "weight": 1,
                "element": {
                    "element_type": "minecraft:single_pool_element",
                    "location": f"mss:mss_{structure_name}",
                    "projection": "rigid",
                    "processors": "minecraft:empty"
                }
            }
        ]
    }

def generate_structure_set_json(structure_name, weight, biomes):
    # Calculate spacing based on weight
    spacing = max(12, int(weight / 10))
    separation = max(4, int(weight / 20))

    struct_set = {
        "structures": [
            {
                "structure": f"mss:{structure_name}",
                "weight": 1
            }
        ],
        "placement": {
            "type": "minecraft:random_spread",
            "salt": hash(structure_name) % 10000000,
            "spacing": spacing,
            "separation": separation,
            "super_exclusion_zone": {
                "chunk_count": 2,
                "other_set": "#minecraft:villages"
            } if weight < 600 else None
        }
    }
    # Remove None values
    if struct_set["placement"]["super_exclusion_zone"] is None:
        del struct_set["placement"]["super_exclusion_zone"]
    return struct_set

def main():
    struct_dir = os.path.join(OUT, "structure")
    pool_dir = os.path.join(OUT, "template_pool")
    set_dir = os.path.join(OUT, "structure_set")

    os.makedirs(struct_dir, exist_ok=True)
    os.makedirs(pool_dir, exist_ok=True)
    os.makedirs(set_dir, exist_ok=True)

    # Track unique structure names (excluding variant suffixes)
    # Group by base structure name
    base_structs = {}
    for name, biomes, weight, height, env in STRUCTURES:
        base = name.rsplit('_', 1)[0] if name[-1].isdigit() and '_' in name else name
        if base not in base_structs:
            base_structs[base] = (name, biomes, weight, height, env)

    for base, (example_name, biomes, weight, height, env) in base_structs.items():
        # Use the example structure for the pool
        pool_name = example_name

        json.dump(generate_structure_json(example_name, biomes, weight, height, env),
                  open(os.path.join(struct_dir, f"{example_name}.json"), "w"), indent=2)
        json.dump(generate_pool_json(example_name),
                  open(os.path.join(pool_dir, f"{example_name}_pool.json"), "w"), indent=2)
        json.dump(generate_structure_set_json(example_name, weight, biomes),
                  open(os.path.join(set_dir, f"{example_name}.json"), "w"), indent=2)
        print(f"  ✓ {example_name}")

    print(f"\nGenerated {len(base_structs)} structure sets")

if __name__ == "__main__":
    main()
