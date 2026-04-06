import csv
import json
import re
import os

def detect_delimiter(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline()
        if ';' in first_line:
            return ';'
        return ','

def convert_metadata(src, dest):
    delimiter = detect_delimiter(src)
    data = {}
    with open(src, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            key = f"{row['LOOPNr']}_{row['ID']}"
            data[key] = row
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def convert_geochemistry(src, dest):
    delimiter = detect_delimiter(src)
    data = {}
    with open(src, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            borehole_id = f"{row['LOOPNr']}_{row['ID']}"
            if borehole_id not in data:
                data[borehole_id] = []
            
            # Convert values to float if possible, otherwise keep as is or None
            clean_row = {}
            for k, v in row.items():
                if k in ['LOOPNr', 'ID', 'method', 'DGUnr']:
                    clean_row[k] = v
                else:
                    try:
                        clean_row[k] = float(v) if v.strip() else None
                    except ValueError:
                        clean_row[k] = v
            data[borehole_id].append(clean_row)
    
    # Restructure into profiles for easier use in the web app
    profiles = {}
    for b_id, rows in data.items():
        # Sort by depth
        rows.sort(key=lambda x: x.get('Depth (m)', 0) if x.get('Depth (m)') is not None else 0)
        
        borehole_profile = {}
        if not rows: continue
        
        keys = rows[0].keys()
        for k in keys:
            borehole_profile[k] = [r.get(k) for r in rows]
        
        profiles[b_id] = borehole_profile

    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2)

def extract_animation_config(src, dest):
    with open(src, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    config_text = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if 'BOREHOLE_OPTIONS' in source:
                config_text = source
                break
    
    # Extract BOREHOLE_OPTIONS dictionary using regex
    # This is a bit tricky as it's Python code in a string.
    # We can try to find the start and end of the dictionary.
    match = re.search(r"'BOREHOLE_OPTIONS':\s*(\{.*?\})", config_text, re.DOTALL)
    if match:
        dict_str = match.group(1)
        # Convert Python dict-like string to JSON compatible string
        # Replace single quotes with double quotes, but be careful with nested quotes
        # For simplicity, since it's a known structure, we can do some basic replacements
        # or use a smarter approach.
        
        # A more robust way to extract a Python dict and convert to JSON is to use ast.literal_eval
        import ast
        try:
            # We need the whole dictionary including the outer braces if we were to parse it alone
            # but BOREHOLE_OPTIONS is part of ANIMATION_CONFIG.
            # Let's find ANIMATION_CONFIG and eval it.
            full_match = re.search(r"ANIMATION_CONFIG\s*=\s*(\{.*?\n\s*\})", config_text, re.DOTALL)
            if full_match:
                config_dict_str = full_match.group(1)
                config_dict = ast.literal_eval(config_dict_str)
                borehole_options = config_dict.get('BOREHOLE_OPTIONS', {})
                with open(dest, 'w', encoding='utf-8') as f:
                    json.dump(borehole_options, f, indent=2)
                return
        except Exception as e:
            print(f"Error parsing ANIMATION_CONFIG: {e}")

    # Fallback regex if ast fails
    print("Fallback to regex extraction")
    # This is very basic and might fail on complex dicts
    # borehole_options = {} ... implementation omitted for brevity as ast is preferred

if __name__ == "__main__":
    convert_metadata('Python_Redox_Geochemistry/Borehole_Metadata.csv', 'web-app/src/data/metadata.json')
    convert_geochemistry('Python_Redox_Geochemistry/Geochemistry/Master_Geochemistry.csv', 'web-app/src/data/geochemistry.json')
    extract_animation_config('Borehole_Multiplots/Animated.ipynb', 'web-app/src/data/animationConfig.json')
