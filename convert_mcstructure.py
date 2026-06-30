#!/usr/bin/env python3
"""
Convert Minecraft Bedrock .mcstructure files to Java Edition .nbt structure files.
Output: SNBT format (text-based NBT) for use with Minecraft Java data packs / mods.
"""
import struct, json, os, sys, math

STRUCTURES_DIR = "/tmp/opencode/m_addon/[v1.0.0] More Simple Structures - BP/structures/wypnt_mss"
OUTPUT_DIR = "/tmp/opencode/mss_mod/src/main/resources/data/mss/structure"

# Block ID mapping from Bedrock to Java
BLOCK_MAP = {
    "minecraft:air": "minecraft:air",
    "minecraft:stone": "minecraft:stone",
    "minecraft:dirt": "minecraft:dirt",
    "minecraft:grass_block": "minecraft:grass_block",
    "minecraft:coarse_dirt": "minecraft:coarse_dirt",
    "minecraft:podzol": "minecraft:podzol",
    "minecraft:sand": "minecraft:sand",
    "minecraft:sandstone": "minecraft:sandstone",
    "minecraft:sandstone_stairs": "minecraft:sandstone_stairs",
    "minecraft:cut_sandstone": "minecraft:cut_sandstone",
    "minecraft:chiseled_sandstone": "minecraft:chiseled_sandstone",
    "minecraft:smooth_sandstone": "minecraft:smooth_sandstone",
    "minecraft:smooth_sandstone_stairs": "minecraft:smooth_sandstone_stairs",
    "minecraft:red_sandstone": "minecraft:red_sandstone",
    "minecraft:red_sandstone_stairs": "minecraft:red_sandstone_stairs",
    "minecraft:cut_red_sandstone": "minecraft:cut_red_sandstone",
    "minecraft:chiseled_red_sandstone": "minecraft:chiseled_red_sandstone",
    "minecraft:smooth_red_sandstone": "minecraft:smooth_red_sandstone",
    "minecraft:oak_log": "minecraft:oak_log",
    "minecraft:oak_planks": "minecraft:oak_planks",
    "minecraft:oak_stairs": "minecraft:oak_stairs",
    "minecraft:oak_slab": "minecraft:oak_slab[type=bottom]",
    "minecraft:oak_fence": "minecraft:oak_fence",
    "minecraft:oak_fence_gate": "minecraft:oak_fence_gate",
    "minecraft:oak_door": "minecraft:oak_door",
    "minecraft:oak_trapdoor": "minecraft:oak_trapdoor",
    "minecraft:oak_leaves": "minecraft:oak_leaves",
    "minecraft:spruce_log": "minecraft:spruce_log",
    "minecraft:spruce_planks": "minecraft:spruce_planks",
    "minecraft:spruce_stairs": "minecraft:spruce_stairs",
    "minecraft:spruce_slab": "minecraft:spruce_slab[type=bottom]",
    "minecraft:spruce_fence": "minecraft:spruce_fence",
    "minecraft:spruce_fence_gate": "minecraft:spruce_fence_gate",
    "minecraft:spruce_door": "minecraft:spruce_door",
    "minecraft:spruce_trapdoor": "minecraft:spruce_trapdoor",
    "minecraft:spruce_leaves": "minecraft:spruce_leaves",
    "minecraft:birch_log": "minecraft:birch_log",
    "minecraft:birch_planks": "minecraft:birch_planks",
    "minecraft:birch_stairs": "minecraft:birch_stairs",
    "minecraft:birch_fence": "minecraft:birch_fence",
    "minecraft:birch_door": "minecraft:birch_door",
    "minecraft:jungle_log": "minecraft:jungle_log",
    "minecraft:jungle_planks": "minecraft:jungle_planks",
    "minecraft:jungle_stairs": "minecraft:jungle_stairs",
    "minecraft:jungle_fence": "minecraft:jungle_fence",
    "minecraft:jungle_door": "minecraft:jungle_door",
    "minecraft:acacia_log": "minecraft:acacia_log",
    "minecraft:acacia_planks": "minecraft:acacia_planks",
    "minecraft:acacia_stairs": "minecraft:acacia_stairs",
    "minecraft:acacia_fence": "minecraft:acacia_fence",
    "minecraft:acacia_door": "minecraft:acacia_door",
    "minecraft:dark_oak_log": "minecraft:dark_oak_log",
    "minecraft:dark_oak_planks": "minecraft:dark_oak_planks",
    "minecraft:dark_oak_stairs": "minecraft:dark_oak_stairs",
    "minecraft:dark_oak_fence": "minecraft:dark_oak_fence",
    "minecraft:dark_oak_door": "minecraft:dark_oak_door",
    "minecraft:mangrove_log": "minecraft:mangrove_log",
    "minecraft:mangrove_planks": "minecraft:mangrove_planks",
    "minecraft:mangrove_stairs": "minecraft:mangrove_stairs",
    "minecraft:mangrove_fence": "minecraft:mangrove_fence",
    "minecraft:mangrove_door": "minecraft:mangrove_door",
    "minecraft:mangrove_roots": "minecraft:mangrove_roots",
    "minecraft:mud": "minecraft:mud",
    "minecraft:mud_bricks": "minecraft:mud_bricks",
    "minecraft:mud_brick_stairs": "minecraft:mud_brick_stairs",
    "minecraft:mud_brick_slab": "minecraft:mud_brick_slab[type=bottom]",
    "minecraft:packed_mud": "minecraft:packed_mud",
    "minecraft:cobblestone": "minecraft:cobblestone",
    "minecraft:stone_bricks": "minecraft:stone_bricks",
    "minecraft:stone_brick_stairs": "minecraft:stone_brick_stairs",
    "minecraft:stone_brick_slab": "minecraft:stone_brick_slab[type=bottom]",
    "minecraft:chiseled_stone_bricks": "minecraft:chiseled_stone_bricks",
    "minecraft:cracked_stone_bricks": "minecraft:cracked_stone_bricks",
    "minecraft:mossy_stone_bricks": "minecraft:mossy_stone_bricks",
    "minecraft:mossy_cobblestone": "minecraft:mossy_cobblestone",
    "minecraft:mossy_cobblestone_stairs": "minecraft:mossy_cobblestone_stairs",
    "minecraft:mossy_cobblestone_wall": "minecraft:mossy_cobblestone_wall",
    "minecraft:stone_brick_wall": "minecraft:stone_brick_wall",
    "minecraft:cobblestone_wall": "minecraft:cobblestone_wall",
    "minecraft:cobblestone_stairs": "minecraft:cobblestone_stairs",
    "minecraft:andesite": "minecraft:andesite",
    "minecraft:diorite": "minecraft:diorite",
    "minecraft:granite": "minecraft:granite",
    "minecraft:polished_andesite": "minecraft:polished_andesite",
    "minecraft:polished_diorite": "minecraft:polished_diorite",
    "minecraft:polished_granite": "minecraft:polished_granite",
    "minecraft:bricks": "minecraft:bricks",
    "minecraft:brick_stairs": "minecraft:brick_stairs",
    "minecraft:brick_slab": "minecraft:brick_slab[type=bottom]",
    "minecraft:nether_bricks": "minecraft:nether_bricks",
    "minecraft:nether_brick_stairs": "minecraft:nether_brick_stairs",
    "minecraft:nether_brick_fence": "minecraft:nether_brick_fence",
    "minecraft:red_nether_bricks": "minecraft:red_nether_bricks",
    "minecraft:red_nether_brick_stairs": "minecraft:red_nether_brick_stairs",
    "minecraft:blackstone": "minecraft:blackstone",
    "minecraft:blackstone_stairs": "minecraft:blackstone_stairs",
    "minecraft:blackstone_slab": "minecraft:blackstone_slab[type=bottom]",
    "minecraft:blackstone_wall": "minecraft:blackstone_wall",
    "minecraft:polished_blackstone": "minecraft:polished_blackstone",
    "minecraft:polished_blackstone_stairs": "minecraft:polished_blackstone_stairs",
    "minecraft:polished_blackstone_bricks": "minecraft:polished_blackstone_bricks",
    "minecraft:polished_blackstone_brick_stairs": "minecraft:polished_blackstone_brick_stairs",
    "minecraft:chiseled_polished_blackstone": "minecraft:chiseled_polished_blackstone",
    "minecraft:gilded_blackstone": "minecraft:gilded_blackstone",
    "minecraft:gold_block": "minecraft:gold_block",
    "minecraft:iron_block": "minecraft:iron_block",
    "minecraft:diamond_block": "minecraft:diamond_block",
    "minecraft:emerald_block": "minecraft:emerald_block",
    "minecraft:lapis_block": "minecraft:lapis_block",
    "minecraft:redstone_block": "minecraft:redstone_block",
    "minecraft:coal_block": "minecraft:coal_block",
    "minecraft:copper_block": "minecraft:copper_block",
    "minecraft:exposed_copper": "minecraft:exposed_copper",
    "minecraft:weathered_copper": "minecraft:weathered_copper",
    "minecraft:oxidized_copper": "minecraft:oxidized_copper",
    "minecraft:waxed_copper_block": "minecraft:waxed_copper_block",
    "minecraft:bookshelf": "minecraft:bookshelf",
    "minecraft:glass": "minecraft:glass",
    "minecraft:glass_pane": "minecraft:glass_pane",
    "minecraft:white_stained_glass": "minecraft:white_stained_glass",
    "minecraft:black_stained_glass": "minecraft:black_stained_glass",
    "minecraft:white_stained_glass_pane": "minecraft:white_stained_glass_pane",
    "minecraft:sea_lantern": "minecraft:sea_lantern",
    "minecraft:glowstone": "minecraft:glowstone",
    "minecraft:jack_o_lantern": "minecraft:jack_o_lantern",
    "minecraft:lantern": "minecraft:lantern",
    "minecraft:campfire": "minecraft:campfire",
    "minecraft:soul_campfire": "minecraft:soul_campfire",
    "minecraft:torch": "minecraft:torch",
    "minecraft:chest": "minecraft:chest",
    "minecraft:trapped_chest": "minecraft:trapped_chest",
    "minecraft:barrel": "minecraft:barrel",
    "minecraft:crafting_table": "minecraft:crafting_table",
    "minecraft:furnace": "minecraft:furnace",
    "minecraft:blast_furnace": "minecraft:blast_furnace",
    "minecraft:smoker": "minecraft:smoker",
    "minecraft:anvil": "minecraft:anvil",
    "minecraft:chipped_anvil": "minecraft:chipped_anvil",
    "minecraft:damaged_anvil": "minecraft:damaged_anvil",
    "minecraft:enchanting_table": "minecraft:enchanting_table",
    "minecraft:brewing_stand": "minecraft:brewing_stand",
    "minecraft:cauldron": "minecraft:cauldron",
    "minecraft:water": "minecraft:water",
    "minecraft:lava": "minecraft:lava",
    "minecraft:gravel": "minecraft:gravel",
    "minecraft:soul_sand": "minecraft:soul_sand",
    "minecraft:soul_soil": "minecraft:soul_soil",
    "minecraft:basalt": "minecraft:basalt",
    "minecraft:polished_basalt": "minecraft:polished_basalt",
    "minecraft:smooth_basalt": "minecraft:smooth_basalt",
    "minecraft:crimson_nylium": "minecraft:crimson_nylium",
    "minecraft:warped_nylium": "minecraft:warped_nylium",
    "minecraft:netherrack": "minecraft:netherrack",
    "minecraft:magma_block": "minecraft:magma_block",
    "minecraft:shroomlight": "minecraft:shroomlight",
    "minecraft:crimson_stem": "minecraft:crimson_stem",
    "minecraft:warped_stem": "minecraft:warped_stem",
    "minecraft:crimson_hyphae": "minecraft:crimson_hyphae",
    "minecraft:warped_hyphae": "minecraft:warped_hyphae",
    "minecraft:crimson_planks": "minecraft:crimson_planks",
    "minecraft:warped_planks": "minecraft:warped_planks",
    "minecraft:crimson_fence": "minecraft:crimson_fence",
    "minecraft:warped_fence": "minecraft:warped_fence",
    "minecraft:crimson_stairs": "minecraft:crimson_stairs",
    "minecraft:warped_stairs": "minecraft:warped_stairs",
    "minecraft:crimson_slab": "minecraft:crimson_slab[type=bottom]",
    "minecraft:warped_slab": "minecraft:warped_slab[type=bottom]",
    "minecraft:crimson_door": "minecraft:crimson_door",
    "minecraft:warped_door": "minecraft:warped_door",
    "minecraft:end_stone": "minecraft:end_stone",
    "minecraft:end_stone_bricks": "minecraft:end_stone_bricks",
    "minecraft:end_stone_brick_stairs": "minecraft:end_stone_brick_stairs",
    "minecraft:end_stone_brick_slab": "minecraft:end_stone_brick_slab[type=bottom]",
    "minecraft:end_stone_brick_wall": "minecraft:end_stone_brick_wall",
    "minecraft:purpur_block": "minecraft:purpur_block",
    "minecraft:purpur_pillar": "minecraft:purpur_pillar",
    "minecraft:purpur_stairs": "minecraft:purpur_stairs",
    "minecraft:purpur_slab": "minecraft:purpur_slab[type=bottom]",
    "minecraft:obsidian": "minecraft:obsidian",
    "minecraft:crying_obsidian": "minecraft:crying_obsidian",
    "minecraft:bone_block": "minecraft:bone_block",
    "minecraft:coal_ore": "minecraft:coal_ore",
    "minecraft:iron_ore": "minecraft:iron_ore",
    "minecraft:gold_ore": "minecraft:gold_ore",
    "minecraft:diamond_ore": "minecraft:diamond_ore",
    "minecraft:emerald_ore": "minecraft:emerald_ore",
    "minecraft:lapis_ore": "minecraft:lapis_ore",
    "minecraft:redstone_ore": "minecraft:redstone_ore",
    "minecraft:copper_ore": "minecraft:copper_ore",
    "minecraft:deepslate": "minecraft:deepslate",
    "minecraft:cobbled_deepslate": "minecraft:cobbled_deepslate",
    "minecraft:cobbled_deepslate_stairs": "minecraft:cobbled_deepslate_stairs",
    "minecraft:cobbled_deepslate_slab": "minecraft:cobbled_deepslate_slab[type=bottom]",
    "minecraft:cobbled_deepslate_wall": "minecraft:cobbled_deepslate_wall",
    "minecraft:polished_deepslate": "minecraft:polished_deepslate",
    "minecraft:deepslate_bricks": "minecraft:deepslate_bricks",
    "minecraft:deepslate_brick_stairs": "minecraft:deepslate_brick_stairs",
    "minecraft:deepslate_brick_slab": "minecraft:deepslate_brick_slab[type=bottom]",
    "minecraft:deepslate_brick_wall": "minecraft:deepslate_brick_wall",
    "minecraft:deepslate_tiles": "minecraft:deepslate_tiles",
    "minecraft:deepslate_tile_stairs": "minecraft:deepslate_tile_stairs",
    "minecraft:cracked_deepslate_bricks": "minecraft:cracked_deepslate_bricks",
    "minecraft:cracked_deepslate_tiles": "minecraft:cracked_deepslate_tiles",
    "minecraft:mycelium": "minecraft:mycelium",
    "minecraft:brown_mushroom_block": "minecraft:brown_mushroom_block",
    "minecraft:red_mushroom_block": "minecraft:red_mushroom_block",
    "minecraft:mushroom_stem": "minecraft:mushroom_stem",
    "minecraft:vine": "minecraft:vine",
    "minecraft:cobweb": "minecraft:cobweb",
    "minecraft:spider_egg": "minecraft:cobweb",
    "minecraft:lectern": "minecraft:lectern",
    "minecraft:red_carpet": "minecraft:red_carpet",
    "minecraft:white_carpet": "minecraft:white_carpet",
    "minecraft:gray_carpet": "minecraft:gray_carpet",
    "minecraft:black_carpet": "minecraft:black_carpet",
    "minecraft:cyan_carpet": "minecraft:cyan_carpet",
    "minecraft:lime_carpet": "minecraft:lime_carpet",
    "minecraft:magenta_carpet": "minecraft:magenta_carpet",
    "minecraft:purple_carpet": "minecraft:purple_carpet",
    "minecraft:blue_carpet": "minecraft:blue_carpet",
    "minecraft:brown_carpet": "minecraft:brown_carpet",
    "minecraft:green_carpet": "minecraft:green_carpet",
    "minecraft:orange_carpet": "minecraft:orange_carpet",
    "minecraft:pink_carpet": "minecraft:pink_carpet",
    "minecraft:yellow_carpet": "minecraft:yellow_carpet",
    "minecraft:red_wool": "minecraft:red_wool",
    "minecraft:white_wool": "minecraft:white_wool",
    "minecraft:gray_wool": "minecraft:gray_wool",
    "minecraft:black_wool": "minecraft:black_wool",
    "minecraft:brown_wool": "minecraft:brown_wool",
    "minecraft:blue_wool": "minecraft:blue_wool",
    "minecraft:cyan_wool": "minecraft:cyan_wool",
    "minecraft:lime_wool": "minecraft:lime_wool",
    "minecraft:green_wool": "minecraft:green_wool",
    "minecraft:magenta_wool": "minecraft:magenta_wool",
    "minecraft:orange_wool": "minecraft:orange_wool",
    "minecraft:pink_wool": "minecraft:pink_wool",
    "minecraft:purple_wool": "minecraft:purple_wool",
    "minecraft:yellow_wool": "minecraft:yellow_wool",
    "minecraft:light_blue_wool": "minecraft:light_blue_wool",
    "minecraft:light_gray_wool": "minecraft:light_gray_wool",
    "minecraft:terracotta": "minecraft:terracotta",
    "minecraft:white_terracotta": "minecraft:white_terracotta",
    "minecraft:red_terracotta": "minecraft:red_terracotta",
    "minecraft:blue_terracotta": "minecraft:blue_terracotta",
    "minecraft:cyan_terracotta": "minecraft:cyan_terracotta",
    "minecraft:lime_terracotta": "minecraft:lime_terracotta",
    "minecraft:brown_terracotta": "minecraft:brown_terracotta",
    "minecraft:black_terracotta": "minecraft:black_terracotta",
    "minecraft:gray_terracotta": "minecraft:gray_terracotta",
    "minecraft:green_terracotta": "minecraft:green_terracotta",
    "minecraft:light_blue_terracotta": "minecraft:light_blue_terracotta",
    "minecraft:light_gray_terracotta": "minecraft:light_gray_terracotta",
    "minecraft:magenta_terracotta": "minecraft:magenta_terracotta",
    "minecraft:orange_terracotta": "minecraft:orange_terracotta",
    "minecraft:pink_terracotta": "minecraft:pink_terracotta",
    "minecraft:purple_terracotta": "minecraft:purple_terracotta",
    "minecraft:yellow_terracotta": "minecraft:yellow_terracotta",
    "minecraft:prismarine": "minecraft:prismarine",
    "minecraft:prismarine_bricks": "minecraft:prismarine_bricks",
    "minecraft:dark_prismarine": "minecraft:dark_prismarine",
    "minecraft:prismarine_stairs": "minecraft:prismarine_stairs",
    "minecraft:tuff": "minecraft:tuff",
    "minecraft:calcite": "minecraft:calcite",
    "minecraft:dripstone_block": "minecraft:dripstone_block",
    "minecraft:pointed_dripstone": "minecraft:pointed_dripstone",
    "minecraft:ochre_froglight": "minecraft:ochre_froglight",
    "minecraft:verdant_froglight": "minecraft:verdant_froglight",
    "minecraft:pearlescent_froglight": "minecraft:pearlescent_froglight",
    "minecraft:reinforced_deepslate": "minecraft:reinforced_deepslate",
    "minecraft:trial_spawner": "minecraft:trial_spawner",
    "minecraft:vault": "minecraft:vault",
    "minecraft:crafter": "minecraft:crafter",
    "minecraft:flowering_azalea": "minecraft:flowering_azalea",
    "minecraft:azalea": "minecraft:azalea",
    "minecraft:moss_block": "minecraft:moss_block",
    "minecraft:sculk": "minecraft:sculk",
    "minecraft:sculk_sensor": "minecraft:sculk_sensor",
    "minecraft:sculk_shrieker": "minecraft:sculk_shrieker",
    "minecraft:sculk_catalyst": "minecraft:sculk_catalyst",
    "minecraft:sculk_vein": "minecraft:sculk_vein",
    "minecraft:cherry_log": "minecraft:cherry_log",
    "minecraft:cherry_planks": "minecraft:cherry_planks",
    "minecraft:cherry_stairs": "minecraft:cherry_stairs",
    "minecraft:cherry_slab": "minecraft:cherry_slab[type=bottom]",
    "minecraft:cherry_fence": "minecraft:cherry_fence",
    "minecraft:cherry_door": "minecraft:cherry_door",
    "minecraft:cherry_leaves": "minecraft:cherry_leaves",
    "minecraft:pale_oak_log": "minecraft:pale_oak_log",
    "minecraft:pale_oak_planks": "minecraft:pale_oak_planks",
    "minecraft:pale_oak_stairs": "minecraft:pale_oak_stairs",
    "minecraft:pale_oak_slab": "minecraft:pale_oak_slab[type=bottom]",
    "minecraft:pale_oak_fence": "minecraft:pale_oak_fence",
    "minecraft:pale_oak_door": "minecraft:pale_oak_door",
    "minecraft:pale_oak_leaves": "minecraft:pale_oak_leaves",
    "minecraft:pale_moss_block": "minecraft:pale_moss_block",
    "minecraft:pale_moss_carpet": "minecraft:pale_moss_carpet",
    "minecraft:spore_blossom": "minecraft:spore_blossom",
    "minecraft:hanging_roots": "minecraft:hanging_roots",
    "minecraft:rooted_dirt": "minecraft:rooted_dirt",
    "minecraft:tinted_glass": "minecraft:tinted_glass",
    "minecraft:ochre_froglight": "minecraft:ochre_froglight",
    "minecraft:bone_block": "minecraft:bone_block",
    "minecraft:white_concrete": "minecraft:white_concrete",
    "minecraft:orange_concrete": "minecraft:orange_concrete",
    "minecraft:magenta_concrete": "minecraft:magenta_concrete",
    "minecraft:light_blue_concrete": "minecraft:light_blue_concrete",
    "minecraft:yellow_concrete": "minecraft:yellow_concrete",
    "minecraft:lime_concrete": "minecraft:lime_concrete",
    "minecraft:pink_concrete": "minecraft:pink_concrete",
    "minecraft:gray_concrete": "minecraft:gray_concrete",
    "minecraft:light_gray_concrete": "minecraft:light_gray_concrete",
    "minecraft:cyan_concrete": "minecraft:cyan_concrete",
    "minecraft:purple_concrete": "minecraft:purple_concrete",
    "minecraft:blue_concrete": "minecraft:blue_concrete",
    "minecraft:brown_concrete": "minecraft:brown_concrete",
    "minecraft:green_concrete": "minecraft:green_concrete",
    "minecraft:red_concrete": "minecraft:red_concrete",
    "minecraft:black_concrete": "minecraft:black_concrete",
    "minecraft:suspicious_sand": "minecraft:suspicious_sand",
    "minecraft:suspicious_gravel": "minecraft:suspicious_gravel",
}

def parse_mcstructure(data):
    offset = [0]
    max_offset = len(data)
    def rn():
        name_len = struct.unpack('<H', data[offset[0]:offset[0]+2])[0]
        offset[0] += 2
        name = data[offset[0]:offset[0]+name_len].decode('utf-8', errors='replace')
        offset[0] += name_len
        return name
    def pv(tag_type):
        if offset[0] >= max_offset: return ('END',)
        if tag_type == 0: return ('END',)
        elif tag_type == 1:
            v = data[offset[0]]; offset[0] += 1; return ('BYTE', v)
        elif tag_type == 2:
            v = struct.unpack('<h', data[offset[0]:offset[0]+2])[0]; offset[0] += 2; return ('SHORT', v)
        elif tag_type == 3:
            v = struct.unpack('<i', data[offset[0]:offset[0]+4])[0]; offset[0] += 4; return ('INT', v)
        elif tag_type == 4:
            v = struct.unpack('<q', data[offset[0]:offset[0]+8])[0]; offset[0] += 8; return ('LONG', v)
        elif tag_type == 5:
            v = struct.unpack('<f', data[offset[0]:offset[0]+4])[0]; offset[0] += 4; return ('FLOAT', v)
        elif tag_type == 6:
            v = struct.unpack('<d', data[offset[0]:offset[0]+8])[0]; offset[0] += 8; return ('DOUBLE', v)
        elif tag_type == 7:
            length = struct.unpack('<i', data[offset[0]:offset[0]+4])[0]; offset[0] += 4
            v = list(data[offset[0]:offset[0]+length]); offset[0] += length; return ('BYTE[]', v)
        elif tag_type == 8:
            length = struct.unpack('<H', data[offset[0]:offset[0]+2])[0]; offset[0] += 2
            v = data[offset[0]:offset[0]+length].decode('utf-8', errors='replace'); offset[0] += length; return ('STR', v)
        elif tag_type == 9:
            elem_type = data[offset[0]]; offset[0] += 1
            list_len = struct.unpack('<i', data[offset[0]:offset[0]+4])[0]; offset[0] += 4
            items = []
            for i in range(list_len):
                items.append(pv(elem_type))
            return ('LIST', items)
        elif tag_type == 10:
            items = {}
            while offset[0] < max_offset and data[offset[0]] != 0:
                item = pt(1)
                if item[0] != 'END':
                    items[item[1]] = item
            if offset[0] < max_offset and data[offset[0]] == 0:
                offset[0] += 1
            return ('COMPOUND', items)
        elif tag_type == 11:
            length = struct.unpack('<i', data[offset[0]:offset[0]+4])[0]; offset[0] += 4
            vals = [struct.unpack('<i', data[offset[0]+i*4:offset[0]+i*4+4])[0] for i in range(length)]
            offset[0] += length * 4
            return ('INT[]', vals)
        else:
            return (f'UKN_{tag_type}', None)
    def pt(depth=0):
        if offset[0] >= max_offset: return ('END',)
        tag_type = data[offset[0]]; offset[0] += 1
        if tag_type == 0: return ('END',)
        name = rn()
        result = pv(tag_type)
        return (result[0], name, *result[1:])
    return pt(0)

def get_value(tag):
    """Extract the value from a parsed tag tuple."""
    if isinstance(tag, tuple):
        if tag[0] in ('INT', 'SHORT', 'BYTE', 'FLOAT', 'LONG'):
            return tag[-1]  # Last element is the value (position varies: list items vs named)
        elif tag[0] in ('STR', 'LIST', 'COMPOUND', 'BYTE[]', 'INT[]'):
            return tag[-1]
    return tag

def convert_blocks(palette_compound, block_indices):
    """Convert block data to Java structure palette + blocks."""
    palette_dict = get_value(palette_compound) if isinstance(palette_compound, tuple) else palette_compound
    default_entry = palette_dict.get('default', None) if isinstance(palette_dict, dict) else None
    block_palette_list = get_value(default_entry) if default_entry else None
    if block_palette_list:
        bp_dict = get_value(block_palette_list) if isinstance(block_palette_list, tuple) else block_palette_list
        block_palette_list = get_value(bp_dict.get('block_palette', None)) if isinstance(bp_dict, dict) else None
    else:
        return [], []
    
    palette = []
    for entry in block_palette_list:
        entry = get_value(entry)
        name = get_value(entry['name'])
        # Map to Java
        mapped = BLOCK_MAP.get(name, name)
        # Handle block states
        states = entry.get('states', None)
        state_str = ""
        if states and get_value(states):
            state_entries = []
            for k, v in get_value(states).items():
                val = get_value(v)
                if isinstance(val, bool):
                    state_entries.append(f"{k}={str(val).lower()}")
                elif isinstance(val, int):
                    state_entries.append(f"{k}={val}")
                elif isinstance(val, str):
                    state_entries.append(f"{k}={val}")
            if state_entries:
                state_str = "[" + ",".join(state_entries) + "]"
        if state_str:
            palette.append(mapped + state_str)
        else:
            palette.append(mapped)
    
    # Get block indices (palette references)
    indices_list = get_value(block_indices)
    # First list is palette index per block
    block_palette_indices = None
    if indices_list and len(indices_list) > 0:
        idx_list = get_value(indices_list[0])
        if idx_list:
            block_palette_indices = [get_value(x) for x in idx_list]
    
    return palette, block_palette_indices

def to_snbt_palette(palette):
    """Convert palette to SNBT."""
    entries = []
    for i, block in enumerate(palette):
        if '[' in block:
            name, props = block.split('[', 1)
            props = '[' + props
        else:
            name = block
            props = "{}"
        entries.append(f'  {{\n    "Name": "{name}",\n    "Properties": {props if props != "{}" else "{ }"}\n  }}')
    return ",\n".join(entries)

def to_snbt_blocks(block_palette_indices, size):
    """Convert block indices to SNBT blocks list."""
    if not block_palette_indices or not size:
        return ""
    wx, wy, wz = size
    total = wx * wy * wz
    indices = block_palette_indices[:total]
    
    # Java structure stores blocks as a list of palette indices
    # If all blocks are the default (0), we can skip
    if all(i == 0 for i in indices):
        return ""
    
    # Write as int array
    return ", ".join(str(i) if i >= 0 else "-1" for i in indices)

def convert_structure(input_path, output_name):
    with open(input_path, 'rb') as f:
        data = f.read()
    
    parsed = parse_mcstructure(data)
    root = get_value(parsed)
    
    format_ver = get_value(root.get('format_version'))
    size = [get_value(x) for x in get_value(root.get('size'))]
    structure = get_value(root.get('structure'))
    
    if not structure:
        print(f"  WARNING: No structure data in {output_name}")
        return None
    
    block_indices = structure.get('block_indices')
    palette = structure.get('palette')
    
    # Check for entity data
    entities_list = get_value(structure.get('entities', ('LIST', 'entities', [])))
    
    java_palette, block_palette_indices = convert_blocks(palette if palette else ('COMPOUND', 'palette', {}), block_indices)
    
    if not java_palette:
        print(f"  WARNING: Empty palette for {output_name}")
        return None
    
    if not block_palette_indices:
        print(f"  WARNING: No block indices for {output_name}")
        return None
    
    wx, wy, wz = size
    
    # Build SNBT
    snbt = '{\n'
    snbt += f'  "DataVersion": 3955,\n'
    
    # Palette
    snbt += f'  "palette": [\n'
    for i, block in enumerate(java_palette):
        if '[' in block:
            name, props = block.split('[', 1)
            if props.endswith(']'):
                props = props[:-1]
            # Parse properties
            prop_dict = {}
            if props:
                for p in props.split(','):
                    if '=' in p:
                        k, v = p.split('=', 1)
                        prop_dict[k] = v
            if prop_dict:
                props_str = ", ".join(f'"{k}": "{v}"' for k, v in prop_dict.items())
                props_part = f'{{ {props_str} }}'
            else:
                props_part = '{ }'
            snbt += f'    {{ "Name": "{name}", "Properties": {props_part} }}'
        else:
            snbt += f'    {{ "Name": "{block}", "Properties": {{ }} }}'
        if i < len(java_palette) - 1:
            snbt += ','
        snbt += '\n'
    snbt += '  ],\n'
    
    # Size
    snbt += f'  "size": [{wx}, {wy}, {wz}],\n'
    
    # Block data
    snbt += f'  "blocks": [\n'
    for i, idx in enumerate(block_palette_indices):
        if idx < 0:
            continue  # Skip air
        z = i // (wx * wy)
        y = (i % (wx * wy)) // wx
        x = (i % (wx * wy)) % wx
        
        pos = f'[{x}, {y}, {z}]'
        snbt += f'    {{ "pos": {pos}, "state": {idx} }}'
        if i < len(block_palette_indices) - 1:
            # Check if there are more non-air blocks
            has_more = False
            for j in range(i + 1, len(block_palette_indices)):
                if block_palette_indices[j] >= 0:
                    has_more = True
                    break
            if has_more:
                snbt += ','
        snbt += '\n'
    snbt += '  ],\n'
    
    # Entities
    snbt += '  "entities": [\n'
    snbt += '  ]\n'
    snbt += '}'
    
    return snbt, size

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = sorted(os.listdir(STRUCTURES_DIR))
    count = 0
    for fname in files:
        if not fname.endswith('.mcstructure'):
            continue
        input_path = os.path.join(STRUCTURES_DIR, fname)
        name = fname.replace('.mcstructure', '')
        
        # Map Bedrock name to Java name
        java_name = f"mss_{name}"
        
        result = convert_structure(input_path, java_name)
        if result:
            snbt, size = result
            output_path = os.path.join(OUTPUT_DIR, f"{java_name}.snbt")
            with open(output_path, 'w') as f:
                f.write(snbt)
            print(f"  ✓ {java_name}.snbt (size: {size})")
            count += 1
        else:
            print(f"  ✗ {fname} - conversion failed")
    
    print(f"\nConverted {count} structures")

if __name__ == "__main__":
    main()
