
import pandas as pd
import numpy as np
import json
import re
import os

# --- ID Normalization (as in notebook) ---
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

# --- Color Interface Logic (simplified but compatible) ---
def get_color_fri_all(df_litho, df_cmap, df_lmap):
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
        try:
            return float(raw_pox)
        except:
            return 0.0

    def compute_interval_pox(row, apply_litho):
        z = (row['Depth_From'] + row['Depth_To']) / 2.0
        cmap_match = df_cmap[df_cmap['Danish Color'].str.lower() == str(row['Color_Description']).lower()]
        lmap_match = df_lmap[df_lmap['Lithology'].str.lower() == str(row['Lithology']).lower()]
        if cmap_match.empty or lmap_match.empty: return np.nan
        base_pox = calculate_base_pox(z, cmap_match.iloc[0]['English Equivalent'], cmap_match.iloc[0]['Raw Oxic Fraction'], cmap_match.iloc[0]['Pox Definition / Logic'])
        if not apply_litho: return base_pox
        factor_str = str(lmap_match.iloc[0]['Factor'])
        if 'Ignore' in factor_str: return np.nan
        factor = 1.0
        if 'unless P_ox=1' in factor_str:
            factor = 1.0 if base_pox == 1.0 else 0.0
        else:
            try:
                factor = float(factor_str)
            except:
                factor = 1.0
        return base_pox * factor

    results = {}
    for (loop, norm_id), sub in df_litho.groupby(['LOOPNr', 'Norm_ID']):
        sub = sub.copy()
        sub["P_ox"] = sub.apply(lambda r: compute_interval_pox(r, apply_litho=True), axis=1)
        sub = sub.dropna(subset=["P_ox"])
        if sub.empty:
            results[(loop, norm_id)] = np.nan
            continue
        max_depth = int(np.ceil(sub["Depth_To"].max()))
        bin_size = 0.2
        bins = np.round(np.arange(0, max_depth + 1, bin_size), 3)
        binned_pox = []
        for i in range(len(bins)-1):
            b_start, b_end = bins[i], bins[i+1]
            w_sum, t_len = 0, 0
            for _, row in sub.iterrows():
                overlap = min(b_end, row["Depth_To"]) - max(b_start, row["Depth_From"])
                if overlap > 0:
                    w_sum += overlap * row["P_ox"]; t_len += overlap
            binned_pox.append(w_sum / t_len if t_len > 0 else np.nan)
        
        found = False
        for i in range(len(binned_pox) - 5 + 1):
            window = binned_pox[i:i+5]
            if not np.isnan(window).any() and np.all(np.array(window) <= 0.1):
                results[(loop, norm_id)] = bins[i]
                found = True
                break
        if not found:
            results[(loop, norm_id)] = np.nan
    return results

def main():
    # Load data
    base_dir = '/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC'
    df_algo = pd.read_csv(os.path.join(base_dir, 'Interface_Detection/Extracted_Advanced_Interfaces.csv'))
    df_geochem = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Geochemistry/Master_Geochemistry.csv'))
    df_metadata = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Borehole_Metadata.csv'))
    df_litho = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Master_Lithology.csv'), encoding='iso-8859-1')
    df_cmap = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Color_mapping.csv'), encoding='iso-8859-1')
    df_lmap = pd.read_csv(os.path.join(base_dir, 'Python_Redox_Geochemistry/Lithology/Lithology_mapping.csv'), encoding='iso-8859-1')

    # Normalize IDs
    df_algo['Norm_ID'] = df_algo.apply(lambda row: normalize_id(row, 'Redox'), axis=1)
    df_geochem['Norm_ID'] = df_geochem.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)
    df_metadata['Norm_ID'] = df_metadata.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)
    df_litho['Norm_ID'] = df_litho.apply(lambda row: normalize_id(row, 'Geochem'), axis=1)

    # Clean Nitrate
    for col in ['NO₃⁻ [mg/L]', 'GW_NO₃⁻ [mg/L]']:
        if col in df_geochem.columns: df_geochem[col] = pd.to_numeric(df_geochem[col], errors='coerce')
    df_geochem['Nitrate'] = df_geochem['NO₃⁻ [mg/L]'].fillna(df_geochem.get('GW_NO₃⁻ [mg/L]', np.nan))
    df_geochem = df_geochem.dropna(subset=['Depth (m)', 'Nitrate'])

    # Consensus Boundaries
    df_consensus = df_algo.groupby(['LOOPNr', 'Norm_ID'])[['Main_Drop_Z', 'Sec_Drop_Z']].mean().reset_index()

    # Color Boundaries
    color_fri_map = get_color_fri_all(df_litho, df_cmap, df_lmap)

    # Pre-calculate Boundaries for all boreholes
    boreholes_list = df_geochem[['LOOPNr', 'Norm_ID']].drop_duplicates()
    bh_data = {}
    for _, bh in boreholes_list.iterrows():
        loop, norm_id = bh['LOOPNr'], bh['Norm_ID']
        
        # Exclusions as in notebook
        if loop == 'LOOP3' and str(norm_id) == '6': continue
        if loop == 'LOOP6' and str(norm_id) in ['2', '2a', '2A']: continue
        
        redox_row = df_consensus[(df_consensus['LOOPNr'] == loop) & (df_consensus['Norm_ID'] == norm_id)]
        p_redox = redox_row['Main_Drop_Z'].iloc[0] if not redox_row.empty else np.nan
        s_redox = redox_row['Sec_Drop_Z'].iloc[0] if not redox_row.empty else np.nan
        
        meta_row = df_metadata[(df_metadata['LOOPNr'] == loop) & (df_metadata['Norm_ID'] == norm_id)]
        g_fri = pd.to_numeric(meta_row['GEUS_FRI'].iloc[0], errors='coerce') if not meta_row.empty else np.nan
        
        c_fri = color_fri_map.get((loop, norm_id), np.nan)
        
        geochem = df_geochem[(df_geochem['LOOPNr'] == loop) & (df_geochem['Norm_ID'] == norm_id)].sort_values('Depth (m)')
        if geochem.empty: continue
        
        bh_data[(loop, norm_id)] = {
            'boundaries': {
                'redox_primary': p_redox,
                'redox_secondary': s_redox,
                'geus_fri': g_fri,
                'fri_color': c_fri
            },
            'depths': geochem['Depth (m)'].values,
            'nitrates': geochem['Nitrate'].values
        }

    # Parameters
    BOUNDARIES = ['redox_primary', 'redox_secondary', 'fri_color', 'geus_fri']
    DISTANCES = [0.2, 0.5, 1.0, 2.0]
    REDUCTIONS = [50, 80, 90, 100]
    THRESHOLDS = [1, 2, 5]

    results = {}

    for boundary in BOUNDARIES:
        results[boundary] = {}
        for dist in DISTANCES:
            dist_key = str(dist)
            results[boundary][dist_key] = {}
            for red_pct in REDUCTIONS:
                red_key = str(red_pct)
                results[boundary][dist_key][red_key] = {}
                for thresh in THRESHOLDS:
                    thresh_key = str(thresh)
                    
                    tp, fp, fn, tn = 0, 0, 0, 0
                    ratio = red_pct / 100.0
                    
                    for (loop, norm_id), data in bh_data.items():
                        # Exclusions (LOOP2 1, LOOP2 2A are Fail in reality)
                        is_excluded = (loop == 'LOOP2' and str(norm_id) == '1') or (loop == 'LOOP2' and str(norm_id).upper() == '2A')
                        
                        depths = data['depths']
                        nitrates = data['nitrates']
                        bz = data['boundaries'][boundary]
                        
                        # Ground Truth: does borehole have reduction?
                        # Using notebook-like baseline: max above some depth OR global max
                        # For ground truth, we want to know if there's a drop from > 10 to < thresh
                        # Find Z_nitrate: shallowest depth where nitrate < thresh AND max above is > 10
                        z_nitrate = np.nan
                        if not is_excluded:
                            for i in range(len(nitrates)):
                                if nitrates[i] < thresh:
                                    if np.any(nitrates[:i+1] > 10.0):
                                        z_nitrate = depths[i]
                                        break
                        
                        has_reduction = not np.isnan(z_nitrate)
                        
                        # Prediction: does boundary pass the test?
                        # Use check_reduction 'relaxed' logic as it combines Ratio and Threshold
                        passed = False
                        if pd.notna(bz):
                            above_idx = depths < bz
                            baseline_n = np.max(nitrates[above_idx]) if np.any(above_idx) else 0.0
                            
                            mask = (depths >= bz - dist) & (depths <= bz + dist)
                            if np.any(mask):
                                w_min = np.min(nitrates[mask])
                                # Logic: drop below thresh OR drop by ratio
                                if w_min < thresh or (baseline_n > 0 and w_min <= (1.0 - ratio) * baseline_n):
                                    passed = True
                            else:
                                # Interpolated fallback if no points in window
                                if np.any(depths > bz + dist) and np.any(depths < bz - dist):
                                    w_min = min(np.interp(bz - dist, depths, nitrates), np.interp(bz + dist, depths, nitrates))
                                    if w_min < thresh or (baseline_n > 0 and w_min <= (1.0 - ratio) * baseline_n):
                                        passed = True

                        if has_reduction and passed:
                            # Verify if it's the SAME interface
                            # TP if the predicted boundary is within dist of the actual nitrate interface
                            if abs(bz - z_nitrate) <= dist * 2: # Being slightly generous with window alignment
                                tp += 1
                            else:
                                fp += 1 # Boundary found but at wrong depth
                                fn += 1 # Missed the actual depth
                        elif has_reduction and not passed:
                            fn += 1
                        elif not has_reduction and passed:
                            fp += 1
                        else:
                            tn += 1
                    
                    total = tp + fp + fn + tn
                    results[boundary][dist_key][red_key][thresh_key] = {
                        'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
                        'rate': round((tp + tn) / total * 100, 1) if total > 0 else 0
                    }

    # Save to JSON
    output_path = os.path.join(base_dir, 'web-app/src/data/nitrateStats.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved stats to {output_path}")

if __name__ == "__main__":
    main()
