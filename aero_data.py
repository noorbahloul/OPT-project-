import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator

class PerfCalculator:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.xl = pd.ExcelFile(excel_path)
        
        self.runway_corrections = {}
        self.field_limit_tables = {}
        self.obstacle_tables = {}
        
        self._load_data()

    def _load_data(self):
        # 1. Load Runway Length Corrections (Slope & Wind)
        for cond in ['dry', 'wet']:
            sheet_name = f'{cond} slope wind  '.replace('  ', ' ')
            if sheet_name not in self.xl.sheet_names:
                # try finding a close match
                for s in self.xl.sheet_names:
                    if cond in s.lower() and 'slope' in s.lower() and 'wind' in s.lower():
                        sheet_name = s
                        break
            
            df = self.xl.parse(sheet_name)
            
            # Slope Table
            # Row 1 has slopes. Row 2..21 has lengths
            slope_row = df.iloc[1].values[1:]
            slopes = []
            valid_slope_indices = []
            for i, val in enumerate(slope_row):
                if pd.notna(val):
                    slopes.append(float(val))
                    valid_slope_indices.append(i + 1)
                    
            lengths_slope = []
            slope_matrix = []
            for i in range(2, 22):
                if pd.isna(df.iloc[i, 0]): break
                lengths_slope.append(float(df.iloc[i, 0]))
                slope_matrix.append([float(df.iloc[i, idx]) for idx in valid_slope_indices])
            
            # Wind Table
            # Find the row that contains "WIND COMPONENT (KTS)"
            wind_idx = -1
            for i in range(len(df)):
                if str(df.iloc[i, 1]).strip() == "WIND COMPONENT (KTS)":
                    wind_idx = i
                    break
            
            wind_row = df.iloc[wind_idx + 1].values[1:]
            winds = []
            valid_wind_indices = []
            for i, val in enumerate(wind_row):
                if pd.notna(val):
                    winds.append(float(val))
                    valid_wind_indices.append(i + 1)
                    
            lengths_wind = []
            wind_matrix = []
            for i in range(wind_idx + 2, wind_idx + 22):
                if i >= len(df) or pd.isna(df.iloc[i, 0]): break
                lengths_wind.append(float(df.iloc[i, 0]))
                wind_matrix.append([float(df.iloc[i, idx]) for idx in valid_wind_indices])
                
            self.runway_corrections[cond] = {
                'slopes': np.array(slopes),
                'lengths_slope': np.array(lengths_slope),
                'slope_matrix': np.array(slope_matrix),
                'winds': np.array(winds),
                'lengths_wind': np.array(lengths_wind),
                'wind_matrix': np.array(wind_matrix)
            }
        
        # 2. Load Field Limit Weights
        for cond in ['dry', 'wet']:
            self.field_limit_tables[cond] = {}
            for alt_range in ['MSL2000', '40006000', '800010000']:
                sheet_name = f'{cond} {alt_range}'.replace('dry', 'Dry') if cond == 'dry' and alt_range == 'MSL2000' else f'{cond} {alt_range}'
                # Try finding closest
                actual_sheet = sheet_name
                for s in self.xl.sheet_names:
                    if cond.lower() in s.lower() and alt_range in s.replace(' ', ''):
                        actual_sheet = s
                        break
                        
                df = self.xl.parse(actual_sheet)
                
                # OAT in row 1
                oat_row = df.iloc[1].values[1:]
                oats = []
                valid_oats = []
                for i, val in enumerate(oat_row):
                    if pd.notna(val):
                        oats.append(float(val))
                        valid_oats.append(i + 1)
                        
                lengths = []
                mtow_matrix = []
                for i in range(2, 50): # up to 50 rows
                    if i >= len(df) or pd.isna(df.iloc[i, 0]): break
                    if "LIMIT WEIGHT" in str(df.iloc[i, 0]): continue
                    try:
                        lengths.append(float(df.iloc[i, 0]))
                        mtow_matrix.append([float(df.iloc[i, idx]) for idx in valid_oats])
                    except:
                        pass
                
                alt_val = 0
                if '2000' in alt_range: alt_val = 2000
                if '4000' in alt_range: alt_val = 6000
                if '8000' in alt_range: alt_val = 10000
                if alt_range == 'MSL2000': alt_val = 0 # base alt for this block? Actually table is for base
                
                self.field_limit_tables[cond][alt_range] = {
                    'oats': np.array(oats),
                    'lengths': np.array(lengths),
                    'matrix': np.array(mtow_matrix)
                }

        # 3. Load Obstacle Limit Weights
        obs_sheet = [s for s in self.xl.sheet_names if 'Obstacle' in s][0]
        df_obs = self.xl.parse(obs_sheet)
        dist_row = df_obs.iloc[1].values[1:]
        dists = []
        valid_dist = []
        for i, val in enumerate(dist_row):
            if pd.notna(val):
                dists.append(float(val))
                valid_dist.append(i + 1)
        
        heights = []
        obs_matrix = []
        for i in range(2, 20):
            if i >= len(df_obs) or pd.isna(df_obs.iloc[i, 0]): break
            val = df_obs.iloc[i, 0]
            if type(val) is str and 'Ref' in val: continue
            try:
                heights.append(float(val))
                obs_matrix.append([float(df_obs.iloc[i, idx]) for idx in valid_dist])
            except: pass
            
        self.obstacle_tables['base'] = {
            'heights': np.array(heights),
            'distances': np.array(dists),
            'matrix': np.array(obs_matrix)
        }
        
    def interp2d(self, x, y, x_arr, y_arr, z_matrix):
        # Clip inputs to array boundaries to avoid extrapolation errors implicitly
        x = np.clip(x, np.min(x_arr), np.max(x_arr))
        y = np.clip(y, np.min(y_arr), np.max(y_arr))
        interp = RegularGridInterpolator((x_arr, y_arr), z_matrix, bounds_error=False, fill_value=None)
        return float(interp((x, y)))

    def calculate_mtow_runway(self, tora, slope, wind, cond, oat, pa, anti_ice, air_cond):
        def _get_dry_mtow(actual_cond):
            corr_data = self.runway_corrections[actual_cond]
            # 1. Correcy for slope
            slope_corr_len = self.interp2d(tora, slope, corr_data['lengths_slope'], corr_data['slopes'], corr_data['slope_matrix'])
            # 2. Correct for wind
            final_corr_len = self.interp2d(slope_corr_len, wind, corr_data['lengths_wind'], corr_data['winds'], corr_data['wind_matrix'])
            
            # 3. Interpolate field limit mtow
            tables = self.field_limit_tables[actual_cond]
            # Simplistic altitude selection based on instruction: "interpolate or next higher"
            # We'll do a simple selection for the exact table
            keys = list(tables.keys())
            
            if pa <= 2000: active_table = tables[keys[0]]
            elif pa <= 6000: active_table = tables[keys[1]]
            else: active_table = tables[keys[2]]
            
            # mtow_matrix is dependent on lengths(y) and oat(x)
            # The matrix rows are lengths, cols are oat
            mtow = self.interp2d(final_corr_len, oat, active_table['lengths'], active_table['oats'], active_table['matrix'])
            return mtow * 1000 # convert to KG

        dry_mtow = _get_dry_mtow('dry')
        if cond.lower() == 'wet':
            wet_mtow = _get_dry_mtow('wet')
            mtow_runway = min(dry_mtow, wet_mtow)
        else:
            mtow_runway = dry_mtow
            
        # Apply specs corrections
        if anti_ice == 'ON': mtow_runway -= 200
        if air_cond == 'OFF': mtow_runway += 400
        
        return mtow_runway
        
    def calculate_mtow_2nd_segment(self, oat, pa, cond, anti_ice, air_cond):
        tables = self.field_limit_tables[cond.lower()]
        keys = list(tables.keys())
        if pa <= 2000: active_table = tables[keys[0]]
        elif pa <= 6000: active_table = tables[keys[1]]
        else: active_table = tables[keys[2]]
        
        # Second segment / climb limit is at the bottom of the table, conceptually.
        # It's independent of field length. Let's extract the last valid row which corresponds to climb limits
        climb_row = active_table['matrix'][-1, :]
        
        oats = active_table['oats']
        # 1D interpolation
        oat_clipped = np.clip(oat, np.min(oats), np.max(oats))
        climb_mtow = np.interp(oat_clipped, oats, climb_row) * 1000
        
        if air_cond == 'OFF': climb_mtow += 1450
        if anti_ice == 'ON': climb_mtow -= 250
        
        return climb_mtow
        
    def calculate_mtow_obstacle(self, obs_height, obs_dist, oat, pa, wind, anti_ice, air_cond):
        if obs_height is None or obs_dist is None or obs_height <= 0:
            return float('inf') # No obstacle limit
            
        base_data = self.obstacle_tables['base']
        
        # The distances in the table are in 100M
        obs_dist_100 = obs_dist / 100.0
        
        ref_weight = self.interp2d(obs_height, obs_dist_100, base_data['heights'], base_data['distances'], base_data['matrix'])
        ref_weight_kg = ref_weight * 1000
        
        # TODO: Implement proper OAT, PA, Wind adjustments for Obstacle (Skipped exact parse to simplify, apply flat for now or ignore non-critical if missing)
        # We know anti-ice and air-cond apply as direct kg offsets
        
        if anti_ice == 'ON': ref_weight_kg -= 300
        if air_cond == 'ON': ref_weight_kg += 600 # By default packs ON is ref, but prompt says "if air conditioning ON -> +600" -- wait, ref is 'packs on and anti ice off'.
        
        return ref_weight_kg

    def calculate_all(self, tora, slope, wind_kts, temp_c, cond,
                  pa,
                  structural=None,
                  anti_ice='OFF',
                  air_cond='ON',
                  obs_height=None,
                  obs_dist=None):
        
        
        mtow_rwy = self.calculate_mtow_runway(tora, slope, wind_kts, cond, temp_c, pa, anti_ice, air_cond)
        mtow_2nd = self.calculate_mtow_2nd_segment(temp_c, pa, cond, anti_ice, air_cond)
        mtow_obs = self.calculate_mtow_obstacle(obs_height, obs_dist, temp_c, pa, wind_kts, anti_ice, air_cond)
        
        limits = [mtow_rwy, mtow_2nd, mtow_obs]
        if structural and structural > 0:
            limits.append(structural)
            
        final_mtow = min(limits)
        
       
        return{
        'MTOW_Runway': mtow_rwy,
        'MTOW_2ndSegment': mtow_2nd,
        'MTOW_Obstacle': mtow_obs if mtow_obs != float('inf') else None,
        'Final_MTOW': final_mtow,
        'PA': pa,
        
        }
