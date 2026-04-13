import json
import base64
import os

def extract_images(notebook_path, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    img_idx = 0
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') != 'code':
            continue
        for output in cell.get('outputs', []):
            if 'data' in output and 'image/png' in output['data']:
                img_data = output['data']['image/png']
                if isinstance(img_data, list):
                    img_data = ''.join(img_data)
                
                img_bytes = base64.b64decode(img_data)
                
                out_path = os.path.join(output_dir, f"{prefix}_{img_idx}.png")
                with open(out_path, 'wb') as img_file:
                    img_file.write(img_bytes)
                print(f"Saved {out_path}")
                img_idx += 1

extract_images('Borehole_Multiplots/Analysis_03_Electron_Equivalent_Modeling_v3.ipynb', 'web-app/public/plots/eem', 'eem_plot')
