import pandas as pd
import numpy as np
import json
import re
import os

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

base_dir = '/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC'
df_algo = pd.read_csv(os.path.join(base_dir, 'Interface_Detection/Extracted_Advanced_Interfaces.csv'))
df_geochem = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Geochemistry/Master_Geochemistry.csv'))
df_metadata = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Borehole_Metadata.csv'))
df_litho = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Master_Lithology.csv'), encoding='iso-8859-1')
df_cmap = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Color_mapping.csv'), encoding='iso-8859-1')
df_lmap = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Lithology_mapping.csv'), encoding='iso-8859-1')

df_algo['Norm_ID'] = df_algo.apply(lambda row: normalize_id(row, 'Redox'), axis=1)
df_geochem['Norm_ID'] = df_geochem.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)
df_metadata['Norm_ID'] = df_metadata.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)
df_litho['Norm_ID'] = df_litho.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)

df_consensus = df_algo.groupby(['LOOPNr', 'Norm_ID'])[['Main_Drop_Z', 'Sec_Drop_Z']].mean().reset_index()

for col in ['NO₃⁻ [mg/L]', 'GW_NO₃⁻ [mg/L]']:
    if col in df_geochem.columns: df_geochem[col] = pd.to_numeric(df_geochem[col], errors='coerce')
df_geochem['Nitrate'] = df_geochem['NO₃⁻ [mg/L]'].fillna(df_geochem.get('GW_NO₃⁻ [mg/L]', np.nan))
df_geochem = df_geochem.dropna(subset=['Depth (m)', 'Nitrate'])

table4_params = {
    'Grayish brown': (50.8, 76.6), 'Gray': (40.1, 55.6), 'Light brownish gray': (41.8, 59.9),
    'Pale brown': (39.2, 46.2), 'Light yellowish brown': (46.3, 51.6), 'Dark grayish brown': (34.1, 55.9)
}

def calculate_base_pox(z, color_en, raw_pox, logic):
    logic = str(logic).strip()
    if logic == 'P_ox=1': return 1.0
    if logic == 'P_ox=0': return 0.0
    if logic == 'P_ox=0.35': return 0.35
    try:
        raw_pox_val = float(raw_pox) if pd.notna(raw_pox) else 0.0
    except:
        raw_pox_val = 0.0
    match = re.search(r'([0-9.]+) down to ([0-9]+)m', logic)
    if match: return float(match.group(1)) if z <= float(match.group(2)) else 0.0
    if 'Table 4' in logic or 'Depth dependent' in logic:
        key = str(color_en).strip()
        if key == 'Dark grayish brown' and raw_pox_val >= 0.1: key = 'Grayish brown'
        if key not in table4_params:
            if 'Gray' in key: key = 'Gray'
            elif 'brownish gray' in key: key = 'Light brownish gray'
            elif 'grayish brown' in key: key = 'Grayish brown'
            else: return 0.0
        z_01, z_0 = table4_params.get(key, (0, 0))
        if z_01 == 0 or z >= z_0: return 0.0
        slope = -0.1 / (z_0 - z_01)
        p = 0.1 + slope * (z - z_01)
        return max(0.0, min(1.0, p))
    return float(raw_pox) if pd.notna(raw_pox) and str(raw_pox).replace('.','').isdigit() else 0.0

def compute_interval_pox(row, df_cmap, df_lmap, apply_litho):
    z = (row['Depth_From'] + row['Depth_To']) / 2.0
    cmap_row = df_cmap[df_cmap['Danish Color'].str.lower() == str(row['Color_Description']).lower()]
    lmap_row = df_lmap[df_lmap['Lithology'].str.lower() == str(row['Lithology']).lower()]
    if cmap_row.empty or lmap_row.empty: return np.nan
    base_pox = calculate_base_pox(z, cmap_row.iloc[0]['English Equivalent'], cmap_row.iloc[0]['Raw Oxic Fraction'], cmap_row.iloc[0]['Pox Definition / Logic'])
    if not apply_litho: return base_pox
    factor_str = str(lmap_row.iloc[0]['Factor'])
    if 'Ignore' in factor_str: return np.nan
    factor = 1.0 if 'unless P_ox=1' in factor_str and base_pox == 1.0 else (0.0 if 'unless P_ox=1' in factor_str else float(factor_str) if factor_str.replace('.','').isdigit() else 1.0)
    return base_pox * factor

COLOR_ALGO_CONFIG = {
    'BIN_SIZE_M': 0.2,
    'REDOX_THRESHOLD': 0.1,
    'PERSISTENCE_BINS': 5
}

def get_color_fri(loop, norm_id, apply_litho):
    sub = df_litho[(df_litho["LOOPNr"] == loop) & (df_litho["Norm_ID"] == norm_id)].copy()
    if sub.empty: return np.nan
    sub["P_ox"] = sub.apply(lambda r: compute_interval_pox(r, df_cmap, df_lmap, apply_litho), axis=1)
    sub = sub.dropna(subset=["P_ox"])
    if sub.empty: return np.nan
    max_depth = int(np.ceil(sub["Depth_To"].max()))
    bins = np.round(np.arange(0, max_depth + 1, COLOR_ALGO_CONFIG["BIN_SIZE_M"]), 3)
    binned_pox = []
    for i in range(len(bins)-1):
        b_start, b_end = bins[i], bins[i+1]
        w_sum, t_len = 0, 0
        for _, row in sub.iterrows():
            overlap = min(b_end, row["Depth_To"]) - max(b_start, row["Depth_From"])
            if overlap > 0:
                w_sum += overlap * row["P_ox"]; t_len += overlap
        binned_pox.append(w_sum / t_len if t_len > 0 else np.nan)
    for i in range(len(binned_pox) - COLOR_ALGO_CONFIG["PERSISTENCE_BINS"] + 1):
        if not np.isnan(binned_pox[i:i+5]).any() and np.all(np.array(binned_pox[i:i+5]) <= COLOR_ALGO_CONFIG["REDOX_THRESHOLD"]):
            return bins[i]
    return np.nan

boreholes = df_geochem[['LOOPNr', 'Norm_ID']].drop_duplicates()
boundary_data = []

# Precalculate boundaries
for _, bh in boreholes.iterrows():
    loop, norm_id = bh['LOOPNr'], bh['Norm_ID']
    redox_row = df_consensus[(df_consensus['LOOPNr'] == loop) & (df_consensus['Norm_ID'] == norm_id)]
    p_redox = redox_row['Main_Drop_Z'].iloc[0] if not redox_row.empty else np.nan
    s_redox = redox_row['Sec_Drop_Z'].iloc[0] if not redox_row.empty else np.nan
    meta_row = df_metadata[(df_metadata['LOOPNr'] == loop) & (df_metadata['Norm_ID'] == norm_id)]
    g_fri = pd.to_numeric(meta_row['GEUS_FRI'].iloc[0], errors='coerce') if not meta_row.empty else np.nan
    c_litho = get_color_fri(loop, norm_id, apply_litho=True)
    c_no_litho = get_color_fri(loop, norm_id, apply_litho=False)
    
    boundary_data.append({
        'LOOPNr': loop, 'Norm_ID': norm_id,
        'redox_primary': p_redox, 'redox_secondary': s_redox, 'geus_fri': g_fri, 'color_with_litho': c_litho, 'color_without_litho': c_no_litho
    })

df_boundaries = pd.DataFrame(boundary_data)
df_boundaries = df_boundaries.dropna(subset=['redox_primary'])
df_boundaries = df_boundaries[~((df_boundaries['LOOPNr'] == 'LOOP3') & (df_boundaries['Norm_ID'] == '6'))]
df_boundaries = df_boundaries[~((df_boundaries['LOOPNr'] == 'LOOP6') & (df_boundaries['Norm_ID'] == '2'))]
df_boundaries = df_boundaries[~((df_boundaries['LOOPNr'] == 'LOOP6') & (df_boundaries['Norm_ID'].str.lower() == '2a'))]

# Compile Profiles Data
profiles = {}
df_merged = pd.merge(df_boundaries, df_geochem[['LOOPNr', 'Norm_ID', 'Depth (m)', 'Nitrate']], on=['LOOPNr', 'Norm_ID'])

for (loop, norm_id), group in df_merged.groupby(['LOOPNr', 'Norm_ID']):
    bh_name = f"{loop} {norm_id}"
    group = group.sort_values('Depth (m)')
    profiles[bh_name] = {
        'depths': group['Depth (m)'].tolist(),
        'nitrates': group['Nitrate'].tolist(),
        'boundaries': {
            'redox_primary': group['redox_primary'].iloc[0] if pd.notna(group['redox_primary'].iloc[0]) else None,
            'redox_secondary': group['redox_secondary'].iloc[0] if pd.notna(group['redox_secondary'].iloc[0]) else None,
            'geus_fri': group['geus_fri'].iloc[0] if pd.notna(group['geus_fri'].iloc[0]) else None,
            'color_with_litho': group['color_with_litho'].iloc[0] if pd.notna(group['color_with_litho'].iloc[0]) else None,
            'color_without_litho': group['color_without_litho'].iloc[0] if pd.notna(group['color_without_litho'].iloc[0]) else None,
        }
    }

# Parameters to test
BOUNDARIES = ['redox_primary', 'redox_secondary', 'geus_fri', 'color_with_litho', 'color_without_litho']
DISTANCES_1 = [0.5, 1.0, 1.5, 2.0]
DISTANCES_2 = [1.0, 2.0, 2.5, 3.0]
RATIOS = [40, 50, 60, 70, 80, 90]
THRESHOLDS = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
LOGIC = 'relaxed'
MIN_BASELINE = 3.0
STABILITY_MARGIN = 0.8

results = {}

print("Generating combinations...")
for b in BOUNDARIES:
    for d1 in DISTANCES_1:
        for d2 in DISTANCES_2:
            for r in RATIOS:
                ratio_val = r / 100.0
                for t in THRESHOLDS:
                    key = f"{b}|{d1}|{d2}|{r}|{t}"
                    res_map = {}
                    
                    for (loop, norm_id), group in df_merged.groupby(['LOOPNr', 'Norm_ID']):
                        bh_name = f"{loop} {norm_id}"
                        bz = group[b].iloc[0]
                        depths = group['Depth (m)'].values
                        nitrates = group['Nitrate'].values
                        
                        if pd.notna(bz):
                            above_idx = depths < bz
                            baseline_n = np.max(nitrates[above_idx]) if np.any(above_idx) else 0.0
                        else:
                            baseline_n = np.max(nitrates) if len(nitrates) > 0 else 0.0

                        # Exceptions
                        if loop == 'LOOP2' and str(norm_id) == '1':
                            res_map[bh_name] = [-1, -1, -1, -1] if pd.isna(bz) else [0, 0, 0, 0]
                            continue
                        if loop == 'LOOP2' and str(norm_id).upper() == '2A':
                            res_map[bh_name] = [-1, -1, -1, -1] if pd.isna(bz) else [0, 0, 0, 0]
                            continue
                        if pd.isna(bz):
                            res_map[bh_name] = [0, 0, 0, 0]
                            continue

                        def check_reduction(win):
                            mask = (depths >= bz - win) & (depths <= bz + win)
                            if not np.any(mask):
                                if not np.any(depths > bz + win) or not np.any(depths < bz - win):
                                    return 0
                                w_min = min(np.interp(bz - win, depths, nitrates), np.interp(bz + win, depths, nitrates))
                            else:
                                w_min = np.min(nitrates[mask])
                            
                            if w_min < t or w_min <= (1.0 - ratio_val) * baseline_n: return 1
                            return 0

                        def check_no_nitrate(win):
                            mask = (depths > bz) & (depths <= bz + win)
                            if not np.any(mask):
                                if not np.any(depths > bz + win) or not np.any(depths < bz):
                                    return 0
                                n_at_win = np.interp(bz + win, depths, nitrates)
                                if n_at_win >= t: return 0
                                limit = t * (1 + STABILITY_MARGIN)
                                deeper = depths > bz + win
                                return 1 if not (np.any(deeper) and np.any(nitrates[deeper] > limit)) else 0
                            
                            low_ids = np.where(mask & (nitrates < t))[0]
                            if len(low_ids) == 0: return 0
                            limit = t * (1 + STABILITY_MARGIN)
                            deeper = depths > depths[low_ids[0]]
                            return 1 if not (np.any(deeper) and np.any(nitrates[deeper] > limit)) else 0
                        
                        n_red1 = check_reduction(d1)
                        n_red2 = check_reduction(d2)
                        zero1 = check_no_nitrate(d1)
                        zero2 = check_no_nitrate(d2)
                        
                        res_map[bh_name] = [n_red1, n_red2, zero1, zero2]
                    
                    results[key] = res_map

output_data = {
    'profiles': profiles,
    'results': results,
    'bh_list': list(profiles.keys())
}

out_path = os.path.join(base_dir, 'web-app/src/data/nitrate_interactive.json')
with open(out_path, 'w') as f:
    json.dump(output_data, f)

print(f"Successfully generated {len(results)} combinations and profile data to {out_path}.")
