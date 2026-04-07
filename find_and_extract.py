import json
import base64
import os

def extract_specific(nb_path, search_str, out_prefix):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    img_idx = 0
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            if search_str in source:
                for output in cell.get('outputs', []):
                    if 'data' in output and 'image/png' in output['data']:
                        img_data = output['data']['image/png']
                        if isinstance(img_data, list):
                            img_data = ''.join(img_data)
                        img_bytes = base64.b64decode(img_data)
                        out_path = f"web-app/public/plots/method/{out_prefix}_{img_idx}.png"
                        with open(out_path, 'wb') as img_file:
                            img_file.write(img_bytes)
                        print(f"Saved {out_path}")
                        img_idx += 1

extract_specific('Interface_Detection/Automated_vs_Human_Stats.ipynb', "Human vs. Algorithmic Interface Depth", "stats_main")

# For the 2026_Interface_Detection.ipynb, the single and dual interface plots are probably generated in the same cell or consecutive cells. 
# Let's check how many images are in the cell that contains "LOGS WITH SINGLE INTERFACE"
def extract_from_cell_with_string(nb_path, search_str, out_prefix):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    img_idx = 0
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            if search_str in source:
                for output in cell.get('outputs', []):
                    if 'data' in output and 'image/png' in output['data']:
                        img_data = output['data']['image/png']
                        if isinstance(img_data, list):
                            img_data = ''.join(img_data)
                        img_bytes = base64.b64decode(img_data)
                        out_path = f"web-app/public/plots/method/{out_prefix}_{img_idx}.png"
                        with open(out_path, 'wb') as img_file:
                            img_file.write(img_bytes)
                        print(f"Saved {out_path}")
                        img_idx += 1

extract_from_cell_with_string('Interface_Detection/2026_Interface_Detection.ipynb', "LOGS WITH SINGLE INTERFACE", "single_interface")
extract_from_cell_with_string('Interface_Detection/2026_Interface_Detection.ipynb', "LOGS WITH DUAL INTERFACES", "dual_interface")
extract_from_cell_with_string('Interface_Detection/Interfaces_Detection_All_Logs.ipynb', "plot_comparison", "all_logs_final")

