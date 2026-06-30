#!/usr/bin/env python3
"""Convert SNBT structure files to gzip-compressed NBT for Minecraft Java."""
import os, gzip, struct, re

SNBT_DIR = "/tmp/opencode/mss_mod/src/main/resources/data/mss/structure"
OUTPUT_DIR = "/tmp/opencode/mss_mod/src/main/resources/data/mss/structure"

def parse_snbt_value(s, i):
    """Parse an SNBT value starting at index i."""
    s = s[i:].strip()
    if not s:
        return None, 0
    
    if s[0] == '{':
        return parse_snbt_compound(s, 0)
    elif s[0] == '[':
        return parse_snbt_list(s, 0)
    elif s[0] == '"':
        end = s.index('"', 1)
        while s[end-1] == '\\':
            end = s.index('"', end + 1)
        return s[1:end], end + 1
    elif s[0].isdigit() or s[0] == '-':
        m = re.match(r'-?\d+', s)
        if m:
            return int(m.group()), m.end()
        m = re.match(r'-?\d+\.\d+', s)
        if m:
            return float(m.group()), m.end()
    elif s.startswith('true'):
        return True, 4
    elif s.startswith('false'):
        return False, 5
    return None, 0

def parse_snbt_compound(s, i):
    """Parse {key:value, ...}"""
    result = {}
    i += 1  # skip {
    while i < len(s):
        s_stripped = s[i:].strip()
        if not s_stripped:
            break
        if s_stripped[0] == '}':
            return result, i + s.index('}', i) - i + 1
        # Parse key
        if s_stripped[0] == '"':
            end = s_stripped.index('"', 1)
            while s_stripped[end-1] == '\\':
                end = s_stripped.index('"', end + 1)
            key = s_stripped[1:end]
            i += end + 1
        else:
            m = re.match(r'\w+', s_stripped)
            if not m:
                break
            key = m.group()
            i += m.end()
        
        # Skip : and whitespace
        while i < len(s) and (s[i] in ' :\n\r\t'):
            i += 1
        
        # Parse value
        val, consumed = parse_snbt_value(s, i)
        if val is not None:
            result[key] = val
            i += consumed
        
        # Skip , and whitespace
        while i < len(s) and (s[i] in ',\n\r\t '):
            i += 1
    return result, i

def parse_snbt_list(s, i):
    """Parse [item, ...]"""
    result = []
    i += 1
    while i < len(s):
        s_stripped = s[i:].strip()
        if not s_stripped:
            break
        if s_stripped[0] == ']':
            return result, i + s.index(']', i) - i + 1
        val, consumed = parse_snbt_value(s, i)
        if val is not None:
            result.append(val)
            i += consumed
        while i < len(s) and s[i] in ',\n\r\t ':
            i += 1
    return result, i

def value_to_nbt(tag_type, value):
    """Convert a Python value to NBT binary."""
    if tag_type == 1:  # Byte
        return struct.pack('>b', value if isinstance(value, int) else (1 if value else 0))
    elif tag_type == 2:  # Short
        return struct.pack('>h', value)
    elif tag_type == 3:  # Int
        return struct.pack('>i', value)
    elif tag_type == 4:  # Long
        return struct.pack('>q', value)
    elif tag_type == 5:  # Float
        return struct.pack('>f', value)
    elif tag_type == 6:  # Double
        return struct.pack('>d', value)
    elif tag_type == 8:  # String
        encoded = value.encode('utf-8')
        return struct.pack('>H', len(encoded)) + encoded
    elif tag_type == 9:  # List
        if not value:
            return struct.pack('>b', 1) + struct.pack('>i', 0)  # empty byte list
        elem_type = 3  # Default to int
        data = b''
        for item in value:
            if isinstance(item, dict):
                elem_type = 10  # Compound
                break
            elif isinstance(item, list):
                elem_type = 9  # List
                break
            elif isinstance(item, str):
                elem_type = 8  # String
                break
            elif isinstance(item, bool):
                elem_type = 1  # Byte
                break
            elif isinstance(item, float):
                elem_type = 5  # Float
                break
            elif isinstance(item, int):
                elem_type = 3  # Int
                break
        data = struct.pack('>b', elem_type) + struct.pack('>i', len(value))
        for item in value:
            data += value_to_nbt(elem_type, item)
        return data
    elif tag_type == 10:  # Compound
        data = b''
        for k, v in value.items():
            if isinstance(v, dict):
                data += struct.pack('>b', 10) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(10, v)
            elif isinstance(v, list):
                data += struct.pack('>b', 9) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(9, v)
            elif isinstance(v, str):
                data += struct.pack('>b', 8) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(8, v)
            elif isinstance(v, bool):
                data += struct.pack('>b', 1) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(1, v)
            elif isinstance(v, float):
                data += struct.pack('>b', 5) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(5, v)
            elif isinstance(v, int):
                data += struct.pack('>b', 3) + struct.pack('>H', len(k)) + k.encode('utf-8') + value_to_nbt(3, v)
        data += struct.pack('>b', 0)  # TAG_End
        return data
    elif tag_type == 7:  # Byte array
        if isinstance(value, list):
            byte_data = bytes(value)
        else:
            byte_data = bytes(value)
        return struct.pack('>i', len(byte_data)) + byte_data
    elif tag_type == 11:  # Int array
        int_list = value if isinstance(value, list) else []
        return struct.pack('>i', len(int_list)) + b''.join(struct.pack('>i', x) for x in int_list)
    elif tag_type == 12:  # Long array
        long_list = value if isinstance(value, list) else []
        return struct.pack('>i', len(long_list)) + b''.join(struct.pack('>q', x) for x in long_list)
    return b''

def guess_snbt_type(val):
    if isinstance(val, dict): return 10
    if isinstance(val, list): return 9
    if isinstance(val, str): return 8
    if isinstance(val, bool): return 1
    if isinstance(val, float): return 5
    if isinstance(val, int): return 3
    return 3

def dict_to_nbt(data, name=""):
    """Convert a Python dict to NBT binary format (big-endian)."""
    compound = b''
    for k, v in data.items():
        t = guess_snbt_type(v)
        compound += struct.pack('>b', t)
        encoded_key = k.encode('utf-8')
        compound += struct.pack('>H', len(encoded_key)) + encoded_key
        compound += value_to_nbt(t, v)
    compound += b'\x00'  # TAG_End
    root = struct.pack('>b', 10) + struct.pack('>H', len(name)) + name.encode('utf-8') + compound
    return root

def main():
    for fname in os.listdir(SNBT_DIR):
        if not fname.endswith('.snbt'):
            continue
        snbt_path = os.path.join(SNBT_DIR, fname)
        with open(snbt_path, 'r') as f:
            snbt = f.read()
        try:
            data, _ = parse_snbt_value(snbt, 0)
            if data and isinstance(data, dict):
                nbt_data = dict_to_nbt(data, "")
                nbt_path = os.path.join(OUTPUT_DIR, fname.replace('.snbt', '.nbt'))
                with gzip.open(nbt_path, 'wb') as f:
                    f.write(nbt_data)
                os.remove(snbt_path)
                print(f"  ✓ {fname} -> {os.path.basename(nbt_path)}")
            else:
                print(f"  ✗ {fname} - parse failed: {type(data)}")
        except Exception as e:
            print(f"  ✗ {fname} - {e}")

if __name__ == "__main__":
    main()
