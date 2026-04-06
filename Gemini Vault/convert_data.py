import pandas as pd
import json
import os
import re

def main():
    os.makedirs('web-app/src/data', exist_ok=True)
    
    # 1. Metadata
    try:
        df_meta = pd.read_csv('Python_Redox_Geochemistry/Borehole_Metadata.csv', encoding='utf-8-sig')
        metadata = {}
        for _, row in df_meta.iterrows():
            key = f"{row['LOOPNr']}_{row['ID']}"
            metadata[key] = row.to_dict()
        with open('web-app/src/data/metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        print("Metadata written.")
    except Exception as e:
        print(f"Error metadata: {e}")

    # 2. Geochemistry
    try:
        df_geochem = pd.read_csv('Python_Redox_Geochemistry/Geochemistry/Master_Geochemistry.csv', encoding='utf-8-sig')
        geochem = {}
        # Group by LOOPNr and ID
        for (loop, bh_id), group in df_geochem.groupby(['LOOPNr', 'ID']):
            key = f"{loop}_{bh_id}"
            # Sort by depth
            group = group.sort_values('Depth (m)')
            geochem[key] = group.to_dict(orient='records')
        with open('web-app/src/data/geochemistry.json', 'w') as f:
            json.dump(geochem, f, indent=2)
        print("Geochemistry written.")
    except Exception as e:
        print(f"Error geochemistry: {e}")

    # 3. Animation Config from Notebook
    try:
        with open('Borehole_Multiplots/Animated.ipynb', 'r') as f:
            nb = json.load(f)
            # Find the cell containing BOREHOLE_OPTIONS
            options_text = ""
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    content = "".join(cell['source'])
                    if 'BOREHOLE_OPTIONS' in content:
                        # Extract the dictionary part using regex or simple split
                        match = re.search(r"'BOREHOLE_OPTIONS':\s*({.*?})", content, re.DOTALL)
                        if match:
                            options_text = match.group(1)
                            # Convert single quotes to double quotes for JSON (naive approach)
                            options_text = options_text.replace("'", '"').replace('True', 'true').replace('False', 'false')
                            # Handle trailing commas if they break json.loads
                            options_text = re.sub(r",\s*}", "}", options_text)
                            options_text = re.sub(r",\s*]", "]", options_text)
                            try:
                                options = json.loads(options_text)
                                with open('web-app/src/data/animationConfig.json', 'w') as f_out:
                                    json.dump(options, f_out, indent=2)
                                print("Animation config written.")
                            except Exception as je:
                                print(f"JSON Parse error in config: {je}")
                                # Fallback: just save the raw text for manual fix
                                with open('web-app/src/data/animationConfig_raw.txt', 'w') as f_raw:
                                    f_raw.write(options_text)
    except Exception as e:
        print(f"Error animation config: {e}")

if __name__ == "__main__":
    main()
