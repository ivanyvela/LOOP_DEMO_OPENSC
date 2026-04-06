
import math
import re
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import numpy as np
import itertools
import random
import base64
from io import BytesIO

# ==========================================
# CONFIGURATION
# ==========================================
WORKSPACE_ROOT = "/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC"
OUTPUT_PLOTS_DIR = os.path.join(WORKSPACE_ROOT, "web-app/public/plots")
OUTPUT_JSON_PATH = os.path.join(WORKSPACE_ROOT, "web-app/src/data/plot_animations.json")

os.makedirs(OUTPUT_PLOTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)

PLOT_BOUNDARIES = {
    'redox_primary': True,
    'redox_secondary': True,
    'fri_color_with_litho': True,
    'fri_color_without_litho': True,
    'geus_fri': True
}

CONFIG = {
    'BIN_SIZE_M': 0.2,
    'REDOX_THRESHOLD': 0.1,
    'PERSISTENCE_BINS': 5,
    'DIRECTION': 'top-down',
    'DEPTH_DEPENDENT_MODEL': 'linear',
    'APPLY_LITHOLOGY_FACTOR': True
}

ANIMATION_CONFIG = {
    'TOTAL_FRAMES': 200,
    'MASTER_SPEED_TRACK': 'Nitrate',
    'BOREHOLE_OPTIONS': {
        'DEMO_D6': {'animate': True, 'interval': [4.7, 10], 'exclude_logs': []},
        'DEMO_D7': {'animate': True, 'interval': [4.5, 12], 'exclude_logs': []},
        'LOOP2_P1': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP2_P2': {'animate': True, 'interval': [1.7,5], 'exclude_logs': ['Apr-20 a Pt']},
        'LOOP2_P2A': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP2_P3': {'animate': True, 'interval': [1,4], 'exclude_logs': []},
        'LOOP2_P4': {'animate': True, 'interval': 'all', 'exclude_logs': []},
        'LOOP3_P1': {'animate': True, 'interval': [3, 8.5], 'exclude_logs': []},
        'LOOP3_P2': {'animate': True, 'interval': [2.5, 7.5], 'exclude_logs': []},
        'LOOP3_P3': {'animate': True, 'interval': [2.5, 6], 'exclude_logs': []},
        'LOOP3_P5': {'animate': True, 'interval': [3.5, 9], 'exclude_logs': []},
        'LOOP3_P6': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP4_GeoW-2': {'animate': True, 'interval': [3.3, 6], 'exclude_logs': []},
        'LOOP4_IS-1': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP4_IS-2': {'animate': True, 'interval': [3, 8], 'exclude_logs': []},
        'LOOP4_MS-1': {'animate': True, 'interval': [2.2, 8], 'exclude_logs': []},
        'LOOP4_MS-2': {'animate': True, 'interval': [2, 7], 'exclude_logs': []},
        'LOOP4_TL-1': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP4_TL-2': {'animate': True, 'interval': [2, 4.5], 'exclude_logs': []},
        'LOOP6_P1': {'animate': True, 'interval': [1.5, 4], 'exclude_logs': []},
        'LOOP6_P2': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP6_P2A': {'animate': False, 'interval': 'all', 'exclude_logs': []},
        'LOOP6_P3': {'animate': True, 'interval': [2, 9], 'exclude_logs': []},
        'LOOP6_P4': {'animate': True, 'interval': [3, 7.5], 'exclude_logs': []},
        'LOOP6_P5': {'animate': True, 'interval': [6, 9], 'exclude_logs': []},
        'LOOP6_P6': {'animate': True, 'interval': [2, 8.5], 'exclude_logs': []},
        'LOOP6_P7': {'animate': True, 'interval': [2, 7], 'exclude_logs': []},
    }
}

table4_params = {
    'Grayish brown': (50.8, 76.6),
    'Light brownish gray': (41.8, 59.9),
    'Pale brown': (39.2, 46.2),
    'Light yellowish brown': (46.3, 51.6),
    'Dark grayish brown': (34.1, 55.9)
}

def calculate_base_pox(z, color_en, raw_pox, logic):
    logic = str(logic).strip()
    if logic == 'P_ox=1': return 1.0
    if logic == 'P_ox=0': return 0.0
    if logic == 'P_ox=0.35': return 0.35
    match = re.search(r'([0-9.]+) down to ([0-9]+)m', logic)
    if match:
        x_val = float(match.group(1))
        y_depth = float(match.group(2))
        return x_val if z <= y_depth else 0.0
    if 'Table 4' in logic or 'Depth dependent' in logic:
        key = str(color_en).strip()
        if key == 'Dark grayish brown' and raw_pox < 0.1: key = 'Dark grayish brown'
        elif key == 'Dark grayish brown': key = 'Grayish brown'
        if key not in table4_params:
            if 'Gray' in key: key = 'Gray'
            elif 'brownish gray' in key: key = 'Light brownish gray'
            elif 'grayish brown' in key: key = 'Grayish brown'
            else: return float(raw_pox) if pd.notna(raw_pox) else 0.0
        z_01, z_0 = table4_params.get(key, (0, 0))
        if z_01 == 0: return 0.0
        if z >= z_0: return 0.0
        if CONFIG.get('DEPTH_DEPENDENT_MODEL', 'linear') == 'linear':
            slope = -0.1 / (z_0 - z_01)
            p = 0.1 + slope * (z - z_01)
            return max(0.0, min(1.0, p))
        else:
            A = float(raw_pox) if pd.notna(raw_pox) else 0.0
            if A > 0.1:
                k = -math.log(0.1 / A) / z_01
                p = A * math.exp(-k * z)
                if z > z_01:
                    slope = -0.1 / (z_0 - z_01)
                    p = 0.1 + slope * (z - z_01)
            else:
                if z > z_01:
                    slope = -A / (z_0 - z_01)
                    p = A + slope * (z - z_01)
                else: p = A
            return max(0.0, min(1.0, p))
    return float(raw_pox) if pd.notna(raw_pox) and str(raw_pox).replace('.','').isdigit() else 0.0

def get_litho_factor(litho_en, factor_str, pox):
    if pd.isna(factor_str) or 'Ignore' in str(factor_str): return None
    if not CONFIG.get('APPLY_LITHOLOGY_FACTOR', True): return 1.0
    if 'unless P_ox=1' in str(factor_str): return 1.0 if pox == 1.0 else 0.0
    try: return float(factor_str)
    except: return 1.0

def compute_interval_pox(row, df_cmap, df_lmap):
    z = (row['Depth_From'] + row['Depth_To']) / 2.0
    color_da = str(row['Color_Description']).strip()
    litho_da = str(row['Lithology']).strip()
    cmap_row = df_cmap[df_cmap['Danish Color'].str.lower() == color_da.lower()]
    lmap_row = df_lmap[df_lmap['Lithology'].str.lower() == litho_da.lower()]
    if cmap_row.empty or lmap_row.empty: return np.nan
    color_en = cmap_row.iloc[0]['English Equivalent']
    raw_pox = cmap_row.iloc[0]['Raw Oxic Fraction']
    try: raw_pox = float(raw_pox)
    except: raw_pox = 0.0
    logic = cmap_row.iloc[0]['Pox Definition / Logic']
    litho_factor_str = lmap_row.iloc[0]['Factor']
    litho_en = lmap_row.iloc[0]['Lithology_EN']
    base_pox = calculate_base_pox(z, color_en, raw_pox, logic)
    if 'Depth dependent for coarse' in str(logic) and 'coarse' not in str(lmap_row.iloc[0]['Feature_factor']):
        if CONFIG.get('APPLY_LITHOLOGY_FACTOR', True): base_pox = 0.0
    factor = get_litho_factor(litho_en, litho_factor_str, base_pox)
    if factor is None: return np.nan
    return base_pox * factor

def calculate_fri_for_borehole(loop, id_val, df_litho, df_cmap, df_lmap):
    sub = df_litho[(df_litho["LOOPNr"] == loop) & (df_litho["ID"] == id_val)].copy()
    if sub.empty: return None
    sub["P_ox"] = sub.apply(lambda r: compute_interval_pox(r, df_cmap, df_lmap), axis=1)
    sub = sub.dropna(subset=["P_ox"])
    if sub.empty: return None
    max_depth = int(np.ceil(sub["Depth_To"].max()))
    if max_depth <= 0: return None
    bins = np.round(np.arange(0, max_depth + 1, CONFIG["BIN_SIZE_M"]), 3)
    if len(bins) < 2: return None
    bin_centers = bins[:-1] + CONFIG["BIN_SIZE_M"] / 2.0
    binned_pox = np.zeros(len(bins) - 1)
    for i in range(len(bins)-1):
        b_start, b_end = bins[i], bins[i+1]
        weighted_sum, total_length = 0, 0
        for _, row in sub.iterrows():
            overlap_start = max(b_start, row["Depth_From"])
            overlap_end = min(b_end, row["Depth_To"])
            if overlap_start < overlap_end:
                length = overlap_end - overlap_start
                weighted_sum += length * row["P_ox"]
                total_length += length
        if total_length > 0: binned_pox[i] = weighted_sum / total_length
        else: binned_pox[i] = np.nan
    fri_depth = None
    if CONFIG["DIRECTION"] == "top-down":
        for i in range(len(binned_pox) - CONFIG["PERSISTENCE_BINS"] + 1):
            valid_slice = binned_pox[i:i+CONFIG["PERSISTENCE_BINS"]]
            if not np.isnan(valid_slice).any() and np.all(valid_slice <= CONFIG["REDOX_THRESHOLD"]):
                fri_depth = bins[i]
                break
    elif CONFIG["DIRECTION"] == "bottom-up":
        deepest_oxic_idx = -1
        req_bins = CONFIG["PERSISTENCE_BINS"]
        for i in range(len(binned_pox) - req_bins, -1, -1):
            valid_slice = binned_pox[i:i+req_bins]
            if not np.isnan(valid_slice).any() and np.all(valid_slice > CONFIG["REDOX_THRESHOLD"]):
                deepest_oxic_idx = i + req_bins - 1
                break
        if deepest_oxic_idx != -1:
            has_reduced_below = False
            for j in range(deepest_oxic_idx + 1, len(binned_pox)):
                if not np.isnan(binned_pox[j]):
                    if binned_pox[j] <= CONFIG["REDOX_THRESHOLD"]: has_reduced_below = True
                    break
            if has_reduced_below: fri_depth = bins[deepest_oxic_idx + 1]
            else: fri_depth = None
        else:
            for i in range(len(binned_pox)):
                if not np.isnan(binned_pox[i]):
                    fri_depth = bins[i]
                    break
    return {"LOOPNr": loop, "ID": id_val, "Color_FRI_Depth": fri_depth, "Binned_Pox": binned_pox, "Bin_Centers": bin_centers}

# ==========================================
# TRACKS TO INCLUDE
# ==========================================
GEOCHEM_TRACKS = [
    dict(gs=3,  top=['Fe(II)_FA [mg/kg]','Fe(total)_FA [mg/kg]'], bot=['Fe(II)/Fe(total) [-]'],
         title_top="Sediment Fe\n[mg/kg]", title_bot="Ratio [-]", is_last=False),
    dict(gs=4,  top=['δ¹⁸O [‰]'], bot=['δD [‰]'],
         title_top="δ¹⁸O [‰]", title_bot="δD [‰]", is_last=False),
    dict(gs=5,  top=['DOC [mg/L]','TIC [mg/L]'], bot=['NH₄⁺ [μg/L]'],
         title_top="DOC, TIC\n[mg/L]", title_bot="NH₄⁺ [μg/L]", is_last=False),
    dict(gs=6,  top=['NO₃⁻ [mg/L]','SO₄²⁻ [mg/L]','Cl⁻ [mg/L]'], bot=[],
         title_top="Anions 1\n[mg/L]", title_bot=None, is_last=False),
    dict(gs=7,  top=['F⁻ [mg/L]','Br⁻ [mg/L]','PO₄⁻ [mg/L]'], bot=[],
         title_top="Anions 2\n[mg/L]", title_bot=None, is_last=False),
    dict(gs=8,  top=['K⁺ [mg/L]','Mg²⁺ [mg/L]','Na⁺ [mg/L]'], bot=[],
         title_top="Cations 1\n[mg/L]", title_bot=None, is_last=False),
    dict(gs=9,  top=['Ni²⁺ [mg/L]','Al³⁺ [mg/L]','Fe²⁺ [mg/L]'], bot=['Ca²⁺ [mg/L]'],
         title_top="Cations 2\n[mg/L]", title_bot="Ca²⁺ [mg/L]", is_last=False),
    dict(gs=10, top=['Sr²⁺ [mg/L]','Mn²⁺ [mg/L]','Ba²⁺ [mg/L]'], bot=[],
         title_top="Cations 3\n[mg/L]", title_bot=None, is_last=True),
]

# ==========================================
# 1. SETUP & DATA LOADING
# ==========================================
path_litho_master = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Lithology', 'Master_Lithology.csv')
path_litho_map = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Lithology', 'Lithology_mapping.csv')
path_color_map = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Lithology', 'Color_mapping.csv')
path_redox = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Redox', 'Master_Redox.csv')
path_geochem = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Geochemistry', 'Master_Geochemistry.csv')
path_metadata = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Borehole_Metadata.csv')
path_gwt = os.path.join(WORKSPACE_ROOT, 'Python_Redox_Geochemistry', 'Lithology', 'GWT.csv')
algo_path = os.path.join(WORKSPACE_ROOT, 'Interface_Detection/Extracted_Advanced_Interfaces.csv')

def load_and_clean(path):
    encodings = ['utf-8-sig', 'utf-8', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            df.columns = df.columns.str.strip().str.replace('^ï»¿', '', regex=True)
            return df
        except: continue
    raise ValueError(f"Failed to read {path}")

df_litho = load_and_clean(path_litho_master)
df_litho_map = load_and_clean(path_litho_map)
df_color_map = load_and_clean(path_color_map)
df_redox = load_and_clean(path_redox)
df_geochem = load_and_clean(path_geochem)
try: df_metadata = pd.read_csv(path_metadata)
except: df_metadata = pd.DataFrame()

for df in [df_litho, df_litho_map, df_color_map, df_redox, df_geochem]:
    for col in df.columns:
        if df[col].dtype == object: df[col] = df[col].str.strip()

df_litho = pd.merge(df_litho, df_litho_map[['Lithology', 'Lithology_simple_EN']], on='Lithology', how='left')
df_litho = pd.merge(df_litho, df_color_map[['Danish Color', 'English Equivalent']], left_on='Color_Description', right_on='Danish Color', how='left')
df_litho['English Equivalent'] = df_litho['English Equivalent'].fillna(df_litho['Color_Description'])
df_redox['DateTime'] = pd.to_datetime(df_redox['DateTime'], errors='coerce')
df_redox['Redox_mV_Plot'] = df_redox['Redox_mV'] + 225 if 'Redox_mV' in df_redox.columns else np.nan

def normalize_id(row, source):
    loop = str(row['LOOPNr']).strip().upper()
    raw_id = str(row['ID']).strip()
    if source == 'Redox':
        norm = re.sub(r'[a-z]$', '', raw_id, flags=re.IGNORECASE)
        if loop == 'DEMO' and norm.isdigit(): norm = f"D{norm}"
        if loop == 'LOOP4':
            norm = norm.replace('Geological Window-', 'GeoW-').replace('interglacial sand-', 'IS-').replace('meltwater sand-', 'MS-').replace('Til layer-', 'TL-')
        return norm
    elif source == 'Geochem':
        if loop in ['LOOP2', 'LOOP3', 'LOOP6']: return re.sub(r'^P', '', raw_id)
        return raw_id

df_redox['Normalized_ID'] = df_redox.apply(lambda row: normalize_id(row, 'Redox'), axis=1)
df_geochem['Normalized_ID'] = df_geochem.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)

try:
    df_gwt_raw = pd.read_csv(path_gwt, sep=',', encoding='utf-8')
    def parse_gwt_sounding(s):
        s = str(s).strip().upper()
        if 'DEMO' in s:
            match = re.search(r'\d+', s)
            return 'DEMO', f"D{match.group()}" if match else None
        elif 'LOOP' in s:
            s = s.replace('LOOP ', 'LOOP')
            match = re.search(r'(LOOP\d+)\s+BOREHOLE\s+(.*)', s)
            if match:
                loop, norm = match.group(1), match.group(2).strip()
                if loop == 'LOOP4': norm = norm.replace('GW2', 'GeoW-2').replace('MWS1', 'MS-1').replace('MWS2', 'MS-2').replace('TIL2', 'TL-2').replace('TIL', 'TL-1')
                elif loop in ['LOOP2', 'LOOP3', 'LOOP6']: norm = re.sub(r'^P', '', norm)
                return loop, norm
        return None, None
    gwt_list = []
    for _, row in df_gwt_raw.iterrows():
        loop, norm_id = parse_gwt_sounding(row['Sounding'])
        if loop and norm_id:
            try: gwt_list.append({'LOOPNr': loop, 'Normalized_ID': norm_id, 'GWT': float(row['GWT'])})
            except: pass
    df_gwt = pd.DataFrame(gwt_list)
except: df_gwt = pd.DataFrame(columns=['LOOPNr', 'Normalized_ID', 'GWT'])

try:
    df_algo = pd.read_csv(algo_path)
    df_algo['Norm_ID'] = df_algo.apply(lambda row: normalize_id(row, 'Redox'), axis=1)
    df_interfaces = df_algo.groupby(['LOOPNr', 'Norm_ID'])[['Main_Drop_Z', 'Sec_Drop_Z']].mean().reset_index()
except: df_interfaces = pd.DataFrame(columns=['LOOPNr', 'Norm_ID', 'Auto_1', 'Auto_2'])

valid_plots = []
for _, row in df_geochem[['LOOPNr', 'ID', 'Normalized_ID']].drop_duplicates().iterrows():
    loop, norm_id, disp_id = row['LOOPNr'], row['Normalized_ID'], row['ID']
    if not df_redox[(df_redox['LOOPNr'] == loop) & (df_redox['Normalized_ID'] == norm_id)].empty:
        valid_plots.append((loop, disp_id, norm_id))

# ==========================================
# HELPER FUNCTIONS & STYLING
# ==========================================
TITLE_SIZE, LABEL_SIZE, TICK_SIZE, LEGEND_SIZE = 10, 9, 9, 12

def get_color_hex(color_name):
    if pd.isna(color_name) or str(color_name).lower() in ['nan', 'none', 'no sample']: return 'none'
    c = str(color_name).lower().strip().replace('grey', 'gray')
    color_dict = {
        'pale yellow': '#F5EDB0', 'light yellowish brown': '#D9C589', 'yellowish brown': '#C4A484', 'dark yellowish brown': '#9B7A27', 'pale brown': '#C7A995', 'light olive brown': '#A89F5B',
        'brown': '#8B5A2B', 'dark grayish brown': '#6A5D57', 'grayish brown': '#8A7B71', 'reddish brown': '#A0522D', 'dark brown': '#5C4033', 'mørk brun': '#5C4033', 'blackish brown': '#3D2314', 'olive brown': '#6B6032',
        'light gray': '#D3D3D3', 'light yellowish gray': '#DCD0BA', 'light brownish gray': '#A8A096', 'gray': '#808080', 'olive gray': '#A09F8D', 'olivengrå': '#A09F8D', 'dark greenish gray': '#4A5D4E', 'dark gray': '#5A5A5A', 'blackish gray': '#363839', 'sortgrå': '#363839',
        'light brownish black': '#2B2522', 'black': '#1C1C1C'
    }
    return color_dict.get(c, '#E0E0E0')

def get_litho_text_color(bg_hex):
    return 'white' if bg_hex in ['#556B2F', '#808000'] else 'black'

def get_sediment_text_color(color_name):
    if pd.isna(color_name) or str(color_name).lower() in ['nan', 'none', 'no sample']: return 'none'
    c = str(color_name).lower().strip().replace('grey', 'gray')
    return 'white' if c in ['reddish brown', 'dark gray', 'light brownish black', 'dark brown', 'mørk brun', 'blackish brown', 'black', 'dark grayish brown', 'dark greenish gray', 'olive brown', 'gray', 'blackish gray', 'sortgrå'] else 'black'

def get_litho_color(litho_simple):
    if pd.isna(litho_simple) or str(litho_simple).lower() in ['nan', 'none', 'no sample']: return 'none'
    l = str(litho_simple).upper()
    if 'CLAY' in l: return '#8FBC8F'
    if 'SAND' in l: return '#F4A460'
    if 'SILT' in l: return '#D2B48C'
    if 'GRAVEL' in l: return '#A9A9A9'
    if 'PEAT' in l or 'HUMUS' in l: return '#556B2F'
    if 'GYTTJA' in l: return '#808000'
    return '#E0E0E0'

def merge_intervals(df, col_to_check):
    if df.empty: return df
    df = df.sort_values('Depth_From').reset_index(drop=True)
    merged = []
    current = df.iloc[0].copy()
    for i in range(1, len(df)):
        row = df.iloc[i]
        if (row['Depth_From'] == current['Depth_To']) and (row[col_to_check] == current[col_to_check]): current['Depth_To'] = row['Depth_To']
        else:
            merged.append(current)
            current = row.copy()
    merged.append(current)
    return pd.DataFrame(merged)

def get_high_contrast_cycle():
    base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#000080', '#FF00FF', '#008080', '#800000', '#00FF00', '#0000FF']
    random.seed(42); random.shuffle(base_colors)
    return itertools.cycle(base_colors)

color_gen = get_high_contrast_cycle()
assigned_colors = {}
MANUAL_COLORS = {'NO₃⁻ [mg/L]': "#F20B0B", 'PO₄⁻ [mg/L]': '#6a3d9a', 'SO₄²⁻ [mg/L]': '#1b9e77'}

def get_param_color(param_name):
    if param_name in MANUAL_COLORS: return MANUAL_COLORS[param_name]
    if param_name not in assigned_colors: assigned_colors[param_name] = next(color_gen)
    return assigned_colors[param_name]

def style_legend_white_no_outline(leg):
    if leg:
        frame = leg.get_frame()
        frame.set_facecolor("white"); frame.set_edgecolor("none"); frame.set_linewidth(0.0); frame.set_alpha(1.0)

def _is_borehole_6(x):
    m = re.search(r'\d+', str(x).strip().upper())
    return (m is not None) and (int(m.group()) == 6)

PLOTTED_GEOCHEM_COLS = set()
for t in GEOCHEM_TRACKS:
    PLOTTED_GEOCHEM_COLS.update(t['top']); PLOTTED_GEOCHEM_COLS.update(t['bot'])
PLOTTED_GEOCHEM_COLS.discard(None)

def max_depth_geochem_plotted(sub_geo, plotted_cols):
    if sub_geo.empty or 'Depth (m)' not in sub_geo.columns: return np.nan
    depth = pd.to_numeric(sub_geo['Depth (m)'], errors='coerce')
    cols = [c for c in plotted_cols if c in sub_geo.columns]
    if not cols: return np.nan
    any_plotted = pd.Series(False, index=sub_geo.index)
    for c in cols: any_plotted |= pd.to_numeric(sub_geo[c], errors='coerce').notna()
    m = any_plotted & depth.notna()
    return float(depth[m].max()) if m.any() else np.nan

# ==========================================
# MAIN EXECUTION
# ==========================================
all_animations = {}

for loop_nr, display_id, normalized_id in valid_plots:
    print(f"Processing {loop_nr} - {display_id}...")
    redox_lines, nitrate_lines_info = [], []
    sub_litho = df_litho[(df_litho['LOOPNr'] == loop_nr) & (df_litho['ID'] == display_id)].copy()
    sub_redox = df_redox[(df_redox['LOOPNr'] == loop_nr) & (df_redox['Normalized_ID'] == normalized_id)].copy()
    if str(loop_nr).strip().upper() == "DEMO" and _is_borehole_6(display_id):
        sub_redox["Depth"] = pd.to_numeric(sub_redox["Depth"], errors="coerce") + 2.0
    sub_geo = df_geochem[(df_geochem['LOOPNr'] == loop_nr) & (df_geochem['ID'] == display_id)].copy()
    dgu_nr = sub_geo['DGUnr'].iloc[0] if 'DGUnr' in sub_geo.columns else "?"
    meta_row = df_metadata[(df_metadata['LOOPNr'] == loop_nr) & (df_metadata['ID'] == normalized_id)] if not df_metadata.empty else pd.DataFrame()
    d1 = pd.to_numeric(sub_litho['Depth_To'], errors='coerce').max() if not sub_litho.empty else np.nan
    d2 = pd.to_numeric(sub_redox['Depth'], errors='coerce').max() if not sub_redox.empty else np.nan
    d3 = max_depth_geochem_plotted(sub_geo, PLOTTED_GEOCHEM_COLS)
    local_max_depth = float(np.nanmax([d1, d2, d3, 0.0]))
    plot_depth_limit = max(2.0, local_max_depth + 3.0)
    fig_height = max(8.0, (plot_depth_limit * 0.55) + 3.5)
    fig = plt.figure(figsize=(26, fig_height))
    LEFT, RIGHT, TOP_IN, BOTTOM_IN = 0.03, 0.97, 1.5, 0.9
    H = fig.get_figheight()
    suptitle_y, top, bottom = 1 - (0.1/H), 1 - (TOP_IN/H), BOTTOM_IN/H
    fig.suptitle(f"{loop_nr} - Borehole {display_id} - DGUnr {dgu_nr}", fontsize=20, weight="bold", y=suptitle_y)
    gs = gridspec.GridSpec(1, 11, figure=fig, left=LEFT, right=RIGHT, bottom=bottom, top=top, width_ratios=[1, 1, 2.5, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2], wspace=0.15)

    def setup_ticks(ax, is_left=False, is_right=False):
        ax.set_ylim(plot_depth_limit, 0)
        y_max = int(np.ceil(plot_depth_limit))
        ax.yaxis.set_major_locator(ticker.FixedLocator(np.arange(0, y_max + 1, 2)))
        ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(1, y_max + 1, 2)))
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
        ax.grid(True, axis='y', which='major', ls='-', lw=0.7, alpha=0.5, color='gray')
        ax.grid(True, axis='y', which='minor', ls='-', lw=0.5, alpha=0.18, color='gray')
        ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False, length=0)
        if is_left:
            ax.set_ylabel("Depth (m)", fontsize=LABEL_SIZE, fontweight='bold')
            ax.tick_params(axis='y', which='major', left=True, labelleft=True, labelsize=TICK_SIZE, length=3)
        if is_right:
            ax.set_ylabel("Depth (m)", fontsize=LABEL_SIZE, fontweight='bold', labelpad=12)
            ax.yaxis.set_label_position("right")
            ax.tick_params(axis='y', which='minor', right=True, labelright=True, labelsize=TICK_SIZE, length=3)

    # Track 1: Lithology
    ax_lith = plt.subplot(gs[0]); setup_ticks(ax_lith, is_left=True)
    ax_lith.set_title("Lithology", fontsize=TITLE_SIZE, pad=30, fontweight='bold'); ax_lith.set_xticks([])
    for _, row in merge_intervals(sub_litho, 'Lithology_simple_EN').iterrows():
        t, b, name = row['Depth_From'], row['Depth_To'], row['Lithology_simple_EN']
        fill = get_litho_color(name)
        ax_lith.add_patch(patches.Rectangle((0, t), 1, b-t, lw=0.5, ec='black', fc=fill))
        if b-t > 0.1 and fill != 'none': ax_lith.text(0.5, t+(b-t)/2, name, ha='center', va='center', fontsize=7, color=get_litho_text_color(fill))
    if PLOT_BOUNDARIES['geus_fri'] and not meta_row.empty:
        gfd = pd.to_numeric(meta_row['GEUS_FRI'].iloc[0], errors='coerce')
        if pd.notna(gfd):
            if gfd <= plot_depth_limit: ax_lith.axhline(gfd, color='cyan', lw=2.0, zorder=10)
            style_legend_white_no_outline(ax_lith.legend(handles=[plt.Line2D([0],[0], color='cyan', lw=2.0, label='GEUS FRI')], loc='upper center', bbox_to_anchor=(0.5, -0.02), fontsize=10))

    # Track 2: Color
    ax_col = plt.subplot(gs[1]); setup_ticks(ax_col)
    ax_col.set_title("Color", fontsize=TITLE_SIZE, pad=30, fontweight='bold'); ax_col.set_xticks([])
    for _, row in merge_intervals(sub_litho, 'English Equivalent').iterrows():
        t, b, name = row['Depth_From'], row['Depth_To'], row['English Equivalent']
        fill = get_color_hex(name) if str(row['Lithology']).lower() != 'x' else 'none'
        ax_col.add_patch(patches.Rectangle((0, t), 1, b-t, lw=0.5, ec='black', fc=fill))
        if b-t > 0.1 and fill != 'none': ax_col.text(0.5, t+(b-t)/2, name, ha='center', va='center', fontsize=7, color=get_sediment_text_color(name))
    ch = []
    if PLOT_BOUNDARIES["fri_color_with_litho"]:
        CONFIG['APPLY_LITHOLOGY_FACTOR'] = True
        res = calculate_fri_for_borehole(loop_nr, display_id, df_litho, df_color_map, df_litho_map)
        if res and res["Color_FRI_Depth"] is not None:
            ax_col.axhline(res["Color_FRI_Depth"], color='magenta', lw=2.0, zorder=10)
            ch.append(plt.Line2D([0],[0], color='magenta', lw=2.0, label='Color Interface'))
    if PLOT_BOUNDARIES["fri_color_without_litho"]:
        CONFIG['APPLY_LITHOLOGY_FACTOR'] = False
        res = calculate_fri_for_borehole(loop_nr, display_id, df_litho, df_color_map, df_litho_map)
        if res and res["Color_FRI_Depth"] is not None:
            ax_col.axhline(res["Color_FRI_Depth"], color='lime', ls='--', lw=2.0, zorder=10)
            ch.append(plt.Line2D([0],[0], color='lime', ls='--', lw=2.0, label='Color Int.(NO factor)'))
    if ch: style_legend_white_no_outline(ax_col.legend(handles=ch, loc='upper center', bbox_to_anchor=(0.53, -0.0005), fontsize=10))

    # Track 3: Redox
    ax_redox = plt.subplot(gs[2]); setup_ticks(ax_redox)
    ax_redox.set_title("Redox\n(mV-corrected)", fontsize=TITLE_SIZE, pad=15, fontweight='bold')
    ax_redox.xaxis.tick_top(); ax_redox.xaxis.set_label_position('top'); ax_redox.axvline(0, color='gray', lw=0.5, alpha=0.5)
    if not sub_redox.empty:
        sub_redox = sub_redox[sub_redox['UpDn'].str.upper() == 'DN'].dropna(subset=['Depth', 'Redox_mV_Plot', 'DateTime'])
        sub_redox['DateLabel'] = sub_redox['DateTime'].dt.strftime('%b-%y')
        g = sub_redox.groupby(['DateLabel', 'ID', 'Electrode_Label', 'Depth'], as_index=False)['Redox_mV_Plot'].mean()
        ax_redox.set_xlim(g['Redox_mV_Plot'].min()-50, g['Redox_mV_Plot'].max()+50)
        uk = g[['DateLabel', 'ID']].drop_duplicates().sort_values(['DateLabel', 'ID']).reset_index(drop=True)
        pal = (plt.cm.tab20 if len(uk) > 10 else plt.cm.tab10)(np.linspace(0, 1, max(len(uk), 1)))
        color_for = {(r['DateLabel'], r['ID']): pal[i % len(pal)] for i, r in uk.iterrows()}
        for (dl, rid, elec), grp in g.sort_values(['DateLabel', 'ID', 'Electrode_Label', 'Depth']).groupby(['DateLabel', 'ID', 'Electrode_Label']):
            grp = grp.sort_values('Depth')
            ls = '--' if (re.search(r'2$', str(elec)) or 'PT2' in str(elec).upper()) else '-'
            lbl = f"{dl} {rid} {elec}".strip()
            ax_redox.plot(grp['Redox_mV_Plot'], grp['Depth'], ls=ls, lw=1.5, color=color_for[(dl, rid)], label=lbl)
            
            loop_p_id = f"{loop_nr}_{display_id}"
            bh_c = ANIMATION_CONFIG['BOREHOLE_OPTIONS'].get(loop_p_id, {'animate': True, 'exclude_logs': []})
            if not any(ex.lower() in lbl.lower() for ex in bh_c.get('exclude_logs', [])):
                dv, vv = grp['Depth'].values, grp['Redox_mV_Plot'].values
                vs = pd.Series(vv).rolling(window=max(3, int(0.5/np.mean(np.diff(dv)))) if len(dv)>=3 and np.mean(np.diff(dv))>0 else 3, center=True, min_periods=1).mean().values if len(dv)>=3 else vv
                redox_lines.append((lbl, dv, vs, color_for[(dl, rid)]))
        style_legend_white_no_outline(ax_redox.legend(fontsize=LEGEND_SIZE, loc='lower center', bbox_to_anchor=(0.5, 0.01), frameon=True))
        if not (intf := df_interfaces[(df_interfaces['LOOPNr'] == loop_nr) & (df_interfaces['Norm_ID'] == normalized_id)]).empty:
            ih = []
            if pd.notna(a1 := intf['Main_Drop_Z'].iloc[0]) and PLOT_BOUNDARIES['redox_primary']:
                ax_redox.axhline(a1, color='red', ls='--', lw=2.0, zorder=10); ih.append(plt.Line2D([0],[0], color='red', ls='--', lw=2.0, label='Primary Interface'))
            if pd.notna(a2 := intf['Sec_Drop_Z'].iloc[0]) and PLOT_BOUNDARIES['redox_secondary']:
                ax_redox.axhline(a2, color='gold', ls='--', lw=1.5, zorder=10); ih.append(plt.Line2D([0],[0], color='gold', ls='--', lw=1.5, label='Secondary Interface'))
            if ih: style_legend_white_no_outline(ax_redox.legend(handles=ih, loc='upper center', bbox_to_anchor=(0.55, -.0005), fontsize=10))

    def plot_geochem_track(ax, data, ct, cb, tt, tb=None, last=False, rv=None, ho=False):
        setup_ticks(ax, is_right=last)
        ax.set_xlabel(tt, fontsize=TITLE_SIZE, fontweight='bold', labelpad=10); ax.xaxis.set_label_position('top'); ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', which='both', top=True, labeltop=True, bottom=False, labelbottom=False, labelsize=TICK_SIZE, pad=2)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=4, prune='both'))
        res = []
        for i, c in enumerate([c for c in ct if c in data.columns]):
            if not (s := data[[c, 'Depth (m)']].dropna()).empty:
                v, d = pd.to_numeric(s[c], errors='coerce'), pd.to_numeric(s['Depth (m)'], errors='coerce')
                m = v.notna() & d.notna(); v, d = v[m], d[m]
                if not v.empty:
                    col = get_param_color(c)
                    if 'NO₃⁻ [mg/L]' in c: nitrate_lines_info.append((c, display_id, d.values, v.values, ax, col))
                    l, = ax.plot(v, d, marker=['o','x','o','^'][i%4], ms=4.8, ls=['-','-','--','--'][i%4], lw=1.1, color=col, mfc='none' if i==2 else col, mec=col, label=c.split('[')[0].strip())
                    res.append((l, v.min(), v.max()))
        if res:
            xmin, xmax = min(r[1] for r in res), max(r[2] for r in res)
            if rv: xmin, xmax = min(xmin, min(x for x, _ in rv)), max(xmax, max(x for x, _ in rv))
            pad = 0.05*(xmax-xmin) if xmax>xmin else 1.0
            ax.set_xlim(xmin-pad, xmax+pad)
            style_legend_white_no_outline(ax.legend([r[0] for r in res], [r[0].get_label() for r in res], fontsize=LEGEND_SIZE, loc='lower center', bbox_to_anchor=(0.5, 0.01), frameon=True))
        if rv: 
            for x, kw in rv: ax.axvline(x, **{**dict(color='gray', ls='--', lw=0.9, alpha=0.22, zorder=0.5), **(kw or {})})
        if cb:
            ab = ax.twiny(); ab.set_ylim(ax.get_ylim()); ab.patch.set_visible(False); ab.grid(False)
            for s in ab.spines.values(): s.set_visible(False)
            ab.spines['bottom'].set_visible(True); ab.spines['bottom'].set_position(('outward', 0))
            ab.xaxis.set_ticks_position('bottom'); ab.xaxis.set_label_position('bottom')
            ab.tick_params(axis='x', which='both', bottom=True, labelbottom=True, top=False, labeltop=False, labelsize=TICK_SIZE, pad=2)
            if tb: ab.set_xlabel(tb, fontsize=TITLE_SIZE, fontweight='bold', labelpad=10)
            ab.xaxis.set_major_locator(ticker.MaxNLocator(nbins=4, prune='both'))
            br = []
            for i, c in enumerate([c for c in cb if c in data.columns]):
                if not (s := data[[c, 'Depth (m)']].dropna()).empty:
                    v, d = pd.to_numeric(s[c], errors='coerce'), pd.to_numeric(s['Depth (m)'], errors='coerce')
                    m = v.notna() & d.notna(); v, d = v[m], d[m]
                    if not v.empty:
                        col = get_param_color(c)
                        l, = ab.plot(v, d, marker=['o','x','o','^'][i%4], ms=4.8, ls=['-','-','--','--'][i%4], lw=1.1, color=col, mfc='none' if i==2 else col, mec=col, label=c.split('[')[0].strip())
                        br.append((l, v.min(), v.max()))
            if br:
                xmin, xmax = min(r[1] for r in br), max(r[2] for r in br)
                pad = 0.05*(xmax-xmin) if xmax>xmin else 1.0
                ab.set_xlim(xmin-pad, xmax+pad)
                style_legend_white_no_outline(ab.legend([r[0] for r in br], [r[0].get_label() for r in br], fontsize=LEGEND_SIZE, loc='lower center', bbox_to_anchor=(0.5, 0.01), frameon=True))

    no3_c = 'NO₃⁻ [mg/L]'
    has_no3 = (no3_c in sub_geo.columns) and pd.to_numeric(sub_geo[no3_c], errors='coerce').notna().any()
    ac = 200 if str(loop_nr)=="LOOP4" and str(display_id)=="TL-2" else True
    plot_geochem_track(plt.subplot(gs[3]), sub_geo, ['Fe(II)_FA [mg/kg]','Fe(total)_FA [mg/kg]'], ['Fe(II)/Fe(total) [-]'], "Sediment Fe\n[mg/kg]", "Ratio [-]")
    plot_geochem_track(plt.subplot(gs[4]), sub_geo, ['δ¹⁸O [‰]'], ['δD [‰]'], "δ¹⁸O [‰]", "δD [‰]")
    plot_geochem_track(plt.subplot(gs[5]), sub_geo, ['DOC [mg/L]','TIC [mg/L]'], ['NH₄⁺ [μg/L]'], "DOC, TIC\n[mg/L]", "NH₄⁺ [μg/L]")
    plot_geochem_track(plt.subplot(gs[6]), sub_geo, [no3_c,'SO₄²⁻ [mg/L]','Cl⁻ [mg/L]'], [], "Anions 1\n[mg/L]", rv=[(50, dict(alpha=0.18, lw=2, ls='--', color='red'))] if has_no3 else None, ho=ac)
    plot_geochem_track(plt.subplot(gs[7]), sub_geo, ['F⁻ [mg/L]','Br⁻ [mg/L]','PO₄⁻ [mg/L]'], [], "Anions 2\n[mg/L]")
    plot_geochem_track(plt.subplot(gs[8]), sub_geo, ['K⁺ [mg/L]','Mg²⁺ [mg/L]','Na⁺ [mg/L]'], [], "Cations 1\n[mg/L]")
    plot_geochem_track(plt.subplot(gs[9]), sub_geo, ['Ni²⁺ [mg/L]','Al³⁺ [mg/L]','Fe²⁺ [mg/L]'], ['Ca²⁺ [mg/L]'], "Cations 2\n[mg/L]", "Ca²⁺ [mg/L]")
    plot_geochem_track(plt.subplot(gs[10]), sub_geo, ['Sr²⁺ [mg/L]','Mn²⁺ [mg/L]','Ba²⁺ [mg/L]'], [], "Cations 3\n[mg/L]", last=True)

    if not (gwt_s := df_gwt[(df_gwt['LOOPNr'] == loop_nr) & (df_gwt['Normalized_ID'] == normalized_id)]).empty:
        gwtd = gwt_s['GWT'].iloc[0]
        if pd.notna(gwtd):
            import matplotlib.transforms as mtrans
            fig.add_artist(plt.Line2D([LEFT, RIGHT], [gwtd, gwtd], transform=mtrans.blended_transform_factory(fig.transFigure, ax_lith.transData), color='blue', ls='--', lw=4, alpha=0.4, zorder=20))
            ax_lith.set_xlim(0, 1); ax_lith.plot(1.10, gwtd-0.2, marker='v', color='blue', ms=10, transform=ax_lith.transData, clip_on=False, zorder=20, mec='white', mew=0.5, alpha=0.6)

    # Animation Data
    bh_id = f"{loop_nr}_{display_id}"
    bh_c = ANIMATION_CONFIG['BOREHOLE_OPTIONS'].get(bh_id, {'animate': True, 'interval': 'all'})
    anim_borehole = []
    if bh_c.get('animate', True):
        zf = np.linspace(0, plot_depth_limit, ANIMATION_CONFIG['TOTAL_FRAMES'])
        if ANIMATION_CONFIG['MASTER_SPEED_TRACK'].lower() == 'nitrate' and nitrate_lines_info:
            for info in nitrate_lines_info:
                if info[0] == no3_c:
                    _, _, nd, nv, axn, _ = info
                    if len(nd) > 1:
                        idx = np.argsort(nd); ds, vs = nd[idx], nv[idx]
                        dfine = np.linspace(0, plot_depth_limit, 1000)
                        vfine = np.interp(dfine, ds, vs)
                        frac = fig.transFigure.inverted().transform(axn.transData.transform(np.column_stack([vfine, dfine])))
                        dxv, dyv = np.diff(frac[:, 0])*26, np.diff(frac[:, 1])*fig_height
                        S = np.concatenate(([0], np.cumsum(np.sqrt(dxv**2 + dyv**2))))
                        if S[-1] > 0: zf = np.interp(np.linspace(0, S[-1], ANIMATION_CONFIG['TOTAL_FRAMES']), S, dfine)
                    break
        if (iv := bh_c.get('interval', 'all')) != 'all': zf = zf[(zf >= iv[0]) & (zf <= iv[1])]
        if len(zf) > 0:
            def get_path(ax, dv, vv, zf):
                vi = np.interp(zf, dv, vv); vi[(zf < dv.min()) | (zf > dv.max())] = np.nan
                frac = fig.transFigure.inverted().transform(ax.transData.transform(np.column_stack([vi, zf])))
                return [None if np.isnan(r[0]) else [float(round(r[0], 5)), float(round(r[1], 5))] for r in frac]
            for _, dv, vv, col in redox_lines:
                if len(dv) > 0: anim_borehole.append({'color': '#{:02x}{:02x}{:02x}'.format(*(int(c*255) for c in (col[:3] if isinstance(col, (tuple, np.ndarray)) else [0,0,0]))), 'path': get_path(ax_redox, dv, vv, zf)})
            for info in nitrate_lines_info:
                if info[0] == no3_c:
                    _, _, nd, nv, axn, col = info
                    if len(nd) > 0: anim_borehole.append({'color': col if isinstance(col, str) else '#{:02x}{:02x}{:02x}'.format(*(int(c*255) for c in col[:3])), 'path': get_path(axn, nd, nv, zf)})
                    break
    all_animations[bh_id] = anim_borehole
    
    save_path = os.path.join(OUTPUT_PLOTS_DIR, f"{loop_nr}_{display_id}.png")
    fig.savefig(save_path, dpi=300)
    plt.close(fig)

with open(OUTPUT_JSON_PATH, 'w') as f:
    json.dump(all_animations, f)

print("Done! High-res PNGs saved to web-app/public/plots/ and animation data to web-app/src/data/plot_animations.json")
