import streamlit as st
import aero_data
import time

st.set_page_config(
    page_title="APS · B737-800",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:     #070c12;
    --surf:   #0d1520;
    --card:   #111c2a;
    --brd:    #1c2d40;
    --gold:   #c8a84b;
    --goldA:  rgba(200,168,75,0.12);
    --green:  #3ecf8e;
    --red:    #e05252;
    --blue:   #4a90d9;
    --txt:    #ccd8e8;
    --muted:  #4a6480;
    --dim:    #0f1e2e;
}

/* ── Hide default chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden !important; height: 0 !important; }

/* ── Main area background ── */
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
section[data-testid="stMain"] {
    background: var(--bg) !important;
}
.block-container {
    padding: 0 2.5rem 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surf) !important;
    border-right: 1px solid var(--brd) !important;
    width: 340px !important;
    min-width: 340px !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
[data-testid="stSidebarContent"] {
    padding: 24px 18px !important;
    background: var(--surf) !important;
}

/* ── Sidebar collapse button ── */
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ── LABELS ── */
label,
[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* ── INPUTS ── */
[data-testid="stNumberInput"] input {
    background: var(--card) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 5px !important;
    color: var(--txt) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    padding: 7px 11px !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(200,168,75,0.15) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] button {
    background: var(--dim) !important;
    border-color: var(--brd) !important;
    color: var(--muted) !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--card) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 5px !important;
    color: var(--txt) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
[data-testid="stSelectbox"] svg { color: var(--gold) !important; }

/* ── RADIO ── */
[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: 6px !important;
    flex-wrap: nowrap !important;
}
[data-testid="stRadio"] label {
    background: var(--card) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 5px !important;
    padding: 6px 14px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: var(--muted) !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    white-space: nowrap !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: var(--goldA) !important;
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

/* ── BUTTONS ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    border-radius: 5px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 3px !important;
    transition: all 0.15s !important;
}
[data-testid="stButton"] > button[kind="primary"] {
    background: var(--gold) !important;
    border: none !important;
    color: #060e05 !important;
    font-size: 17px !important;
    padding: 13px 0 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #d4b55a !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--brd) !important;
    color: var(--muted) !important;
    font-size: 13px !important;
    padding: 10px 0 !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    background: var(--goldA) !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    background: rgba(224,82,82,0.08) !important;
    border: 1px solid rgba(224,82,82,0.3) !important;
    border-radius: 5px !important;
    color: var(--red) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}
[data-testid="stWarning"] {
    background: rgba(200,168,75,0.08) !important;
    border: 1px solid rgba(200,168,75,0.3) !important;
    border-radius: 5px !important;
    color: var(--gold) !important;
}

/* ════════════ CUSTOM HTML COMPONENTS ════════════ */

/* ── Topbar ── */
.nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 2.5rem;
    height: 56px;
    background: var(--surf);
    border-bottom: 1px solid var(--brd);
    margin-bottom: 2rem;
    margin-left: -2.5rem; margin-right: -2.5rem;
}
.nav-logo { font-family: 'Bebas Neue', sans-serif; font-size: 20px; letter-spacing: 5px; color: var(--gold); }
.nav-sub  { font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }
.nav-r    { display: flex; align-items: center; gap: 14px; }
.nav-live { display: flex; align-items: center; gap: 6px; font-family: 'DM Mono', monospace; font-size: 9px; color: var(--green); letter-spacing: 1.5px; text-transform: uppercase; }
.nav-dot  { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); }
.nav-pill { font-family: 'DM Mono', monospace; font-size: 9px; color: #060e05; background: var(--gold); padding: 4px 13px; border-radius: 20px; letter-spacing: 1.5px; text-transform: uppercase; }

/* ── Sidebar section heading ── */
.sec {
    display: flex; align-items: center; gap: 8px;
    margin: 18px 0 10px; padding-bottom: 7px;
    border-bottom: 1px solid var(--brd);
    font-family: 'DM Mono', monospace; font-size: 8px;
    letter-spacing: 3px; color: var(--gold); text-transform: uppercase;
}
.sec:first-child { margin-top: 0; }
.sec::before { content: ''; width: 5px; height: 5px; border-radius: 50%; background: var(--gold); flex-shrink: 0; }

/* ── Airport card ── */
.ap {
    background: var(--card); border: 1px solid var(--brd); border-radius: 6px;
    padding: 11px 14px; display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
}
.ap-icao { font-family: 'Bebas Neue', sans-serif; font-size: 28px; letter-spacing: 3px; color: var(--txt); line-height: 1; }
.ap-name { font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; }
.ap-elev { margin-left: auto; text-align: right; font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; line-height: 1.6; }
.ap-elev b { font-family: 'Bebas Neue', sans-serif; font-size: 18px; color: var(--gold); letter-spacing: 1px; display: block; }

/* ── Runway strip ── */
.rwy { display: grid; grid-template-columns: repeat(4,1fr); gap: 5px; margin-bottom: 6px; }
.rwy-c { background: var(--card); border: 1px solid var(--brd); border-radius: 5px; padding: 7px 9px; }
.rwy-l { font-family: 'DM Mono', monospace; font-size: 7px; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 3px; }
.rwy-v { font-family: 'Bebas Neue', sans-serif; font-size: 16px; color: var(--txt); letter-spacing: 1px; line-height: 1; }
.rwy-u { font-family: 'DM Mono', monospace; font-size: 7px; color: var(--muted); margin-left: 2px; }

/* ── Obstacle pill ── */
.obs { display: inline-flex; align-items: center; gap: 5px; font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 1px; text-transform: uppercase; padding: 3px 9px; border-radius: 3px; margin-top: 5px; }
.obs-y { background: rgba(224,82,82,0.1); color: var(--red); border: 1px solid rgba(224,82,82,0.3); }
.obs-n { background: rgba(62,207,142,0.08); color: var(--green); border: 1px solid rgba(62,207,142,0.2); }

/* ── MTOW Banner ── */
.banner {
    background: linear-gradient(135deg, #081a10, #050e08);
    border: 1px solid #163024;
    border-left: 4px solid var(--green);
    border-radius: 8px;
    padding: 24px 28px;
    display: flex; align-items: center; justify-content: space-between; gap: 20px;
    margin-bottom: 20px;
}
.b-lbl  { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 3px; color: var(--green); text-transform: uppercase; margin-bottom: 6px; }
.b-val  { font-family: 'Bebas Neue', sans-serif; font-size: 64px; line-height: 1; color: #fff; }
.b-unit { font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: var(--green); margin-left: 8px; }
.b-sub  { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted); margin-top: 5px; }
.b-plbl { font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }
.b-pill {
    font-family: 'DM Mono', monospace; font-size: 10px; color: var(--gold);
    letter-spacing: 2px; text-transform: uppercase;
    background: var(--goldA); border: 1px solid var(--gold);
    border-radius: 20px; padding: 7px 20px; white-space: nowrap;
}

/* ── Breakdown grid ── */
.bk { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 24px; }
.bkc {
    background: var(--card); border: 1px solid var(--brd);
    border-radius: 7px; padding: 16px 14px;
    transition: border-color 0.2s;
}
.bkc:hover { border-color: var(--muted); }
.bkc.lim  { border-color: var(--red) !important; }
.bk-l { font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
.bk-v { font-family: 'Bebas Neue', sans-serif; font-size: 28px; color: #fff; line-height: 1; }
.bk-v.na { font-family: 'DM Mono', monospace; font-size: 12px; color: var(--muted); }
.bk-u { font-family: 'DM Mono', monospace; font-size: 9px; color: var(--gold); margin-left: 3px; }
.bk-t { font-family: 'DM Mono', monospace; font-size: 7px; color: var(--red); letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px; }

/* ── V-speed section header ── */
.vsec {
    display: flex; align-items: center; gap: 8px;
    margin: 0 0 16px; padding-bottom: 8px;
    border-bottom: 1px solid var(--brd);
    font-family: 'DM Mono', monospace; font-size: 9px;
    letter-spacing: 3px; color: var(--gold); text-transform: uppercase;
}
.vsec::before { content: ''; width: 5px; height: 5px; border-radius: 50%; background: var(--gold); }

/* ── V-speed grid ── */
.vg { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; }
.vc {
    background: var(--card); border: 1px solid var(--brd);
    border-radius: 8px; padding: 24px 18px; text-align: center;
    position: relative; overflow: hidden;
}
.vc::after {
    content: ''; position: absolute; bottom: 0; left: 15%; right: 15%;
    height: 2px; border-radius: 2px;
}
.vc1::after { background: var(--blue); }
.vcr::after { background: var(--green); }
.vc2::after { background: var(--gold); }
.vc-k { font-family: 'Bebas Neue', sans-serif; font-size: 22px; letter-spacing: 5px; }
.vc1 .vc-k { color: var(--blue); }
.vcr .vc-k { color: var(--green); }
.vc2 .vc-k { color: var(--gold); }
.vc-d { font-family: 'DM Mono', monospace; font-size: 8px; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; margin: 2px 0 16px; }
.vc-v { font-family: 'Bebas Neue', sans-serif; font-size: 64px; color: #fff; line-height: 1; }
.vc-u { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--muted); margin-top: 6px; }

/* ── Condition strip ── */
.cs {
    display: flex; flex-wrap: wrap; gap: 16px;
    background: var(--card); border: 1px solid var(--brd);
    border-radius: 5px; padding: 12px 16px; margin-top: 14px;
}
.ci { font-family: 'DM Mono', monospace; font-size: 9px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }
.ci span { color: var(--gold); margin-left: 5px; }

/* ── Placeholder ── */
.ph {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 60vh; gap: 10px;
}
.ph-t { font-family: 'Bebas Neue', sans-serif; font-size: 80px; color: var(--brd); letter-spacing: 8px; line-height: 1; }
.ph-s { font-family: 'DM Mono', monospace; font-size: 9px; color: var(--dim); letter-spacing: 2px; text-transform: uppercase; margin-top: 4px; }
.ph-g { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: 28px; width: 100%; }
.ph-c { background: var(--card); border: 1px solid var(--brd); border-radius: 8px; padding: 22px 16px; text-align: center; }
.ph-k { font-family: 'Bebas Neue', sans-serif; font-size: 20px; letter-spacing: 4px; color: var(--brd); }
.ph-v { font-family: 'Bebas Neue', sans-serif; font-size: 52px; color: var(--dim); line-height: 1; margin-top: 8px; }
.ph-u { font-family: 'DM Mono', monospace; font-size: 9px; color: var(--dim); margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════════════════════
@st.cache_resource
def load_perf_data():
    return aero_data.PerfCalculator("Data.xlsx")

calc = load_perf_data()

airports = {
    "DAAS": {
        "name": "Setif", "elevation": 1016,
        "runways": {
            "09": {"TORA":2900,"TODA":2900,"ASDA":2900,"SLOPE":-0.3, "OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
            "27": {"TORA":2900,"TODA":2900,"ASDA":2900,"SLOPE": 0.32,"OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
        }
    },
    "DAAE": {
        "name": "Bejaia", "elevation": 6,
        "runways": {
            "08": {"TORA":2400,"TODA":2400,"ASDA":2400,"SLOPE":-0.13,"OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
            "26": {"TORA":2400,"TODA":2400,"ASDA":2460,"SLOPE": 0.13,"OBSTACLE":1,   "DISTANCE":2630,"HEIGHT":20},
        }
    },
    "DAUB": {
        "name": "Biskra", "elevation": 86,
        "runways": {
            "13": {"TORA":3300,"TODA":3300,"ASDA":3300,"SLOPE":-0.44,"OBSTACLE":1,   "DISTANCE":4300,"HEIGHT":96},
            "31": {"TORA":3300,"TODA":3300,"ASDA":3400,"SLOPE": 0.49,"OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
        }
    },
    "DAAV": {
        "name": "Jijel", "elevation": 11,
        "runways": {
            "17": {"TORA":2400,"TODA":2400,"ASDA":2500,"SLOPE": 0.22,"OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
            "35": {"TORA":2400,"TODA":2400,"ASDA":2460,"SLOPE":-0.22,"OBSTACLE":None,"DISTANCE":None,"HEIGHT":None},
        }
    },
}

# ══════════════════════════════════════════════════════════════════
#  V-SPEED HELPERS  (unchanged)
# ══════════════════════════════════════════════════════════════════
def interp(x, x1, x2, y1, y2):
    if x1 == x2: return y1
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

def bounds(value, keys):
    keys = sorted(keys)
    for i in range(len(keys) - 1):
        if keys[i] <= value <= keys[i + 1]:
            return keys[i], keys[i + 1]
    return keys[0], keys[-1]

def get_base(weight, flaps5_speeds):
    w1, w2 = bounds(weight, flaps5_speeds.keys())
    return {k: interp(weight, w1, w2, flaps5_speeds[w1][k], flaps5_speeds[w2][k])
            for k in ["V1","VR","V2"]}

def temp_alt_adj(temp, alt, temp_alt_table):
    t1, t2 = bounds(temp, temp_alt_table.keys())
    result = {}
    for k in ["V1","VR","V2"]:
        def interp_alt(t):
            a1, a2 = bounds(alt, temp_alt_table[t].keys())
            return interp(alt, a1, a2, temp_alt_table[t][a1][k], temp_alt_table[t][a2][k])
        result[k] = interp(temp, t1, t2, interp_alt(t1), interp_alt(t2))
    return result

def slope_wind_adj(weight, slope, wind, slope_wind_table):
    w = min(slope_wind_table.keys(), key=lambda x: abs(x - weight))
    s1, s2 = bounds(slope, slope_wind_table[w].keys())
    def interp_wind(s):
        w1, w2 = bounds(wind, slope_wind_table[w][s].keys())
        return interp(wind, w1, w2, slope_wind_table[w][s][w1], slope_wind_table[w][s][w2])
    return interp(slope, s1, s2, interp_wind(s1), interp_wind(s2))

DRY_FLAPS5 = {
    90:{"V1":159,"VR":162,"V2":167}, 80:{"V1":149,"VR":152,"V2":159},
    70:{"V1":139,"VR":141,"V2":151}, 60:{"V1":128,"VR":129,"V2":142},
    50:{"V1":114,"VR":115,"V2":131}, 40:{"V1":100,"VR":101,"V2":120},
}
DRY_TEMP_ALT = {
    70:{-2:{"V1":7,"VR":5,"V2":-3},  0:{"V1":8,"VR":5,"V2":-3}},
    60:{-2:{"V1":5,"VR":3,"V2":-2},  0:{"V1":5,"VR":4,"V2":-3},  2:{"V1":7,"VR":6,"V2":-4},  4:{"V1":10,"VR":7,"V2":-5}},
    50:{-2:{"V1":2,"VR":2,"V2":-2},  0:{"V1":3,"VR":3,"V2":-2},  2:{"V1":4,"VR":4,"V2":-3},  4:{"V1":6,"VR":5,"V2":-4},
         6:{"V1":8,"VR":6,"V2":-4},  8:{"V1":10,"VR":8,"V2":-5}, 10:{"V1":12,"VR":8,"V2":-6}},
    40:{-2:{"V1":1,"VR":1,"V2":-1},  0:{"V1":1,"VR":1,"V2":-1},  2:{"V1":2,"VR":2,"V2":-2},  4:{"V1":4,"VR":4,"V2":-2},
         6:{"V1":5,"VR":5,"V2":-3},  8:{"V1":7,"VR":6,"V2":-4}, 10:{"V1":8,"VR":7,"V2":-5}},
    30:{-2:{"V1":0,"VR":0,"V2":0},   0:{"V1":0,"VR":0,"V2":0},   2:{"V1":1,"VR":1,"V2":-1},  4:{"V1":2,"VR":2,"V2":-2},
         6:{"V1":3,"VR":4,"V2":-2},  8:{"V1":5,"VR":5,"V2":-3}, 10:{"V1":6,"VR":6,"V2":-4}},
    20:{-2:{"V1":0,"VR":0,"V2":0},   0:{"V1":0,"VR":0,"V2":0},   2:{"V1":1,"VR":1,"V2":-1},  4:{"V1":2,"VR":2,"V2":-1},
         6:{"V1":3,"VR":3,"V2":-2},  8:{"V1":4,"VR":4,"V2":-3}, 10:{"V1":6,"VR":6,"V2":-4}},
   -60:{-2:{"V1":0,"VR":0,"V2":0},   0:{"V1":0,"VR":0,"V2":0},   2:{"V1":1,"VR":1,"V2":-1},  4:{"V1":2,"VR":2,"V2":-1},
         6:{"V1":3,"VR":3,"V2":-2},  8:{"V1":4,"VR":4,"V2":-3}, 10:{"V1":5,"VR":5,"V2":-3}},
}
DRY_SLOPE_WIND = {
    90:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1}},
    80:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1}},
    70:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1}},
    60:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:1,30:1,40:1}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:1,30:1,40:1},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1}},
    50:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0}},
    40:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0}},
}
WET_FLAPS5 = {
    90:{"V1":153,"VR":162,"V2":167}, 80:{"V1":142,"VR":152,"V2":159},
    70:{"V1":131,"VR":141,"V2":151}, 60:{"V1":118,"VR":129,"V2":142},
    50:{"V1":104,"VR":115,"V2":131}, 40:{"V1":89, "VR":101,"V2":120},
}
WET_TEMP_ALT = {
    70:{-2:{"V1":10,"VR":7,"V2":-3},  0:{"V1":13,"VR":7,"V2":-3},  2:{"V1":5,"VR":5,"V2":-3},
         4:{"V1":5,"VR":10,"V2":-4},  6:{"V1":5,"VR":3,"V2":-3},   8:{"V1":5,"VR":4,"V2":-3},  10:{"V1":5,"VR":6,"V2":-4}},
    60:{-2:{"V1":7,"VR":6,"V2":-2},   0:{"V1":8,"VR":6,"V2":-3},   2:{"V1":11,"VR":7,"V2":-3},
         4:{"V1":14,"VR":10,"V2":-4}, 6:{"V1":3,"VR":3,"V2":-3},   8:{"V1":4,"VR":4,"V2":-4},  10:{"V1":6,"VR":6,"V2":-5}},
    50:{-2:{"V1":3,"VR":2,"V2":-2},   0:{"V1":4,"VR":3,"V2":-2},   2:{"V1":6,"VR":4,"V2":-3},
         4:{"V1":8,"VR":5,"V2":-4},   6:{"V1":11,"VR":6,"V2":-5},  8:{"V1":15,"VR":8,"V2":-5}, 10:{"V1":15,"VR":9,"V2":-6}},
    40:{-2:{"V1":1,"VR":1,"V2":-1},   0:{"V1":2,"VR":1,"V2":-1},   2:{"V1":3,"VR":2,"V2":-3},
         4:{"V1":5,"VR":4,"V2":-4},   6:{"V1":6,"VR":5,"V2":-5},   8:{"V1":9,"VR":6,"V2":-6},  10:{"V1":11,"VR":7,"V2":-7}},
    30:{-2:{"V1":0,"VR":0,"V2":0},    0:{"V1":0,"VR":0,"V2":0},    2:{"V1":1,"VR":1,"V2":-1},
         4:{"V1":2,"VR":2,"V2":-2},   6:{"V1":3,"VR":4,"V2":-2},   8:{"V1":5,"VR":5,"V2":-3},  10:{"V1":6,"VR":6,"V2":-4}},
   -60:{-2:{"V1":0,"VR":0,"V2":0},    0:{"V1":0,"VR":0,"V2":0},    2:{"V1":1,"VR":1,"V2":-1},
         4:{"V1":2,"VR":2,"V2":-1},   6:{"V1":3,"VR":3,"V2":-2},   8:{"V1":4,"VR":4,"V2":-3},  10:{"V1":5,"VR":5,"V2":-3}},
}
WET_SLOPE_WIND = {
    90:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1}},
    80:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:0,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:1,40:1}},
    70:{-2:{-15:-2,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1},-1:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1},
         0:{-15:-1,-10:-1,-5:-1,0:0,10:0,20:1,30:1,40:1}, 1:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1}},
    60:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:1,30:1,40:1}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:1,30:1,40:1},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:1,30:1,40:1}},
    50:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0}},
    40:{-2:{-15:-2,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0}, -1:{-15:-1,-10:-1,-5:0,0:0,10:0,20:0,30:0,40:0},
         0:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},    1:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0},
         2:{-15:0,-10:0,-5:0,0:0,10:0,20:0,30:0,40:0}},
}

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR — INPUTS
# ══════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Airport & Runway ──────────────────────────────────────────
    st.markdown('<div class="sec">Airport & Runway</div>', unsafe_allow_html=True)

    airport_choice = st.selectbox(
        "Airport ICAO",
        list(airports.keys()),
        format_func=lambda k: f"{k} — {airports[k]['name']}"
    )
    airport_data = airports[airport_choice]

    runway_choice = st.selectbox(
        "Active Runway",
        list(airport_data["runways"].keys()),
        format_func=lambda r: f"RWY {r}"
    )
    runway_data = airport_data["runways"][runway_choice]

    slope_str = ("+" if runway_data["SLOPE"] > 0 else "") + str(runway_data["SLOPE"]) + "%"
    obs_cls   = "obs obs-y" if runway_data["OBSTACLE"] else "obs obs-n"
    obs_txt   = "⚠ Obstacle Active" if runway_data["OBSTACLE"] else "✓ Clear"

    st.markdown(f"""
    <div class="ap">
      <div>
        <div class="ap-icao">{airport_choice}</div>
        <div class="ap-name">{airport_data['name']}</div>
      </div>
      <div class="ap-elev">Elevation<b>{airport_data['elevation']:,} ft</b></div>
    </div>
    <div class="rwy">
      <div class="rwy-c"><div class="rwy-l">TORA</div><div class="rwy-v">{runway_data['TORA']}<span class="rwy-u">m</span></div></div>
      <div class="rwy-c"><div class="rwy-l">TODA</div><div class="rwy-v">{runway_data['TODA']}<span class="rwy-u">m</span></div></div>
      <div class="rwy-c"><div class="rwy-l">ASDA</div><div class="rwy-v">{runway_data['ASDA']}<span class="rwy-u">m</span></div></div>
      <div class="rwy-c"><div class="rwy-l">Slope</div><div class="rwy-v" style="font-size:14px">{slope_str}</div></div>
    </div>
    <span class="{obs_cls}">{obs_txt}</span>
    """, unsafe_allow_html=True)

    # ── Environmental Conditions ──────────────────────────────────
    st.markdown('<div class="sec">Environmental Conditions</div>', unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        pa_input    = st.number_input("Pressure Alt (ft)", value=0)
        temperature = st.number_input("OAT (°C)", value=15)
    with cb:
        wind_speed    = st.number_input("Wind Speed (kt)", min_value=0, value=0)
        structural_wt = st.number_input("Struct. MTOW (kg)", value=79000)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    cc, cd = st.columns(2)
    with cc:
        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:8px;color:#4a6480;text-transform:uppercase;letter-spacing:2px;margin-bottom:5px">RWY Condition</p>', unsafe_allow_html=True)
        runway_condition = st.radio("rwyc", ["Dry", "Wet"], horizontal=True, label_visibility="collapsed")
    with cd:
        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:8px;color:#4a6480;text-transform:uppercase;letter-spacing:2px;margin-bottom:5px">Wind Direction</p>', unsafe_allow_html=True)
        wind_type = st.radio("windd", ["Headwind", "Tailwind"], horizontal=True, label_visibility="collapsed")

    ce, cf = st.columns(2)
    with ce:
        anti_ice = st.selectbox("Anti-Ice", ["OFF", "ON"])
    with cf:
        air_conditioning = st.selectbox("A/C Pack", ["ON", "OFF"])

    # ── Obstacle Override ─────────────────────────────────────────
    st.markdown('<div class="sec">Obstacle Override</div>', unsafe_allow_html=True)

    cg, ch = st.columns(2)
    with cg:
        obs_dist_input   = st.number_input("Distance (m)", value=float(runway_data.get("DISTANCE") or 0))
    with ch:
        obs_height_input = st.number_input("Height (m)",   value=float(runway_data.get("HEIGHT") or 0))

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    calc_clicked  = st.button("Calculate Final MTOW", type="primary",  use_container_width=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    speed_clicked = st.button("Show Takeoff V-Speeds", type="secondary", use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  MAIN AREA — TOPBAR + RESULTS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nav">
  <div>
    <div class="nav-logo">✈ Aero Performance System</div>
    <div class="nav-sub">B737-800 · CFM56-7B27 · Flaps 5 · Takeoff Performance</div>
  </div>
  <div class="nav-r">
    <div class="nav-live"><div class="nav-dot"></div>Systems Normal</div>
    <div class="nav-pill">Takeoff Perf</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MTOW Calculation ──────────────────────────────────────────────
if calc_clicked:
    with st.spinner("Computing performance data…"):
        tora        = float(runway_data.get("TORA", 0))
        slope       = float(runway_data.get("SLOPE", 0))
        actual_wind = wind_speed if wind_type == "Headwind" else -wind_speed
        obs_d       = obs_dist_input   if obs_dist_input > 0 else None
        obs_h       = obs_height_input if obs_dist_input > 0 else None
        try:
            results = calc.calculate_all(
                tora=tora, slope=slope, wind_kts=actual_wind,
                temp_c=temperature, cond=runway_condition,
                pa=pa_input, structural=structural_wt,
                anti_ice=anti_ice, air_cond=air_conditioning,
                obs_height=obs_h, obs_dist=obs_d
            )
            time.sleep(0.4)
            st.session_state["results"] = results
            st.session_state["inputs"]  = dict(
                runway_condition=runway_condition, temperature=temperature,
                pa_input=pa_input, wind_speed=wind_speed, wind_type=wind_type,
                structural_wt=structural_wt, airport_choice=airport_choice,
                runway_choice=runway_choice
            )
        except Exception as e:
            st.error(f"Calculation error: {e}")
            st.stop()

# ── MTOW Results ─────────────────────────────────────────────────
if "results" in st.session_state and not speed_clicked:
    results = st.session_state["results"]
    inp     = st.session_state.get("inputs", {})

    candidates = {
        "Runway":      results["MTOW_Runway"],
        "2nd Segment": results["MTOW_2ndSegment"],
        "Structural":  inp.get("structural_wt", structural_wt),
    }
    if results["MTOW_Obstacle"]:
        candidates["Obstacle"] = results["MTOW_Obstacle"]
    limiting_name = min(candidates, key=candidates.get)
    fin = results["Final_MTOW"]

    st.markdown(f"""
    <div class="banner">
      <div>
        <div class="b-lbl">▸ Final Applied MTOW</div>
        <div class="b-val">{fin:,.0f}<span class="b-unit">kg</span></div>
        <div class="b-sub">{fin/1000:.1f} tonnes</div>
      </div>
      <div style="text-align:right">
        <div class="b-plbl">Limiting Factor</div>
        <div class="b-pill">{limiting_name}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    def lc(n): return "bkc lim" if n == limiting_name else "bkc"
    def lt(n): return '<div class="bk-t">◄ Limiting</div>' if n == limiting_name else ""
    obs_v = results["MTOW_Obstacle"]

    st.markdown(f"""
    <div class="bk">
      <div class="{lc('Runway')}">
        <div class="bk-l">Runway Limit</div>
        <div class="bk-v">{results['MTOW_Runway']:,.0f}<span class="bk-u">kg</span></div>
        {lt('Runway')}
      </div>
      <div class="{lc('2nd Segment')}">
        <div class="bk-l">2nd Segment</div>
        <div class="bk-v">{results['MTOW_2ndSegment']:,.0f}<span class="bk-u">kg</span></div>
        {lt('2nd Segment')}
      </div>
      <div class="{lc('Obstacle')}">
        <div class="bk-l">Obstacle</div>
        {'<div class="bk-v">' + f"{obs_v:,.0f}" + '<span class="bk-u">kg</span></div>' if obs_v else '<div class="bk-v na">No limit</div>'}
        {lt('Obstacle')}
      </div>
      <div class="{lc('Structural')}">
        <div class="bk-l">Structural</div>
        <div class="bk-v">{inp.get('structural_wt', structural_wt):,.0f}<span class="bk-u">kg</span></div>
        {lt('Structural')}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── V-Speeds ──────────────────────────────────────────────────────
if speed_clicked:
    if "results" not in st.session_state:
        st.warning("Calculate MTOW first before viewing V-speeds.")
        st.stop()

    results = st.session_state["results"]
    inp     = st.session_state.get("inputs", {})
    fin     = results["Final_MTOW"]

    candidates = {
        "Runway": results["MTOW_Runway"], "2nd Segment": results["MTOW_2ndSegment"],
        "Structural": inp.get("structural_wt", structural_wt),
    }
    if results["MTOW_Obstacle"]: candidates["Obstacle"] = results["MTOW_Obstacle"]
    limiting_name = min(candidates, key=candidates.get)

    # Compact MTOW banner
    st.markdown(f"""
    <div class="banner" style="padding:18px 24px;margin-bottom:18px">
      <div>
        <div class="b-lbl">▸ Final Applied MTOW</div>
        <div class="b-val" style="font-size:42px">{fin:,.0f}<span class="b-unit" style="font-size:18px">kg</span></div>
      </div>
      <div style="text-align:right">
        <div class="b-plbl">Limiting</div>
        <div class="b-pill">{limiting_name}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cond = inp.get("runway_condition", runway_condition)
    f5, tat, swt = (DRY_FLAPS5, DRY_TEMP_ALT, DRY_SLOPE_WIND) if cond == "Dry" else (WET_FLAPS5, WET_TEMP_ALT, WET_SLOPE_WIND)

    weight = fin / 1000
    temp   = inp.get("temperature", temperature)
    alt    = inp.get("pa_input", pa_input) / 1000
    slp    = runway_data.get("SLOPE", 0)
    wnd    = inp.get("wind_speed", wind_speed)
    wtyp   = inp.get("wind_type", wind_type)
    wind_v = wnd if wtyp == "Headwind" else -wnd

    base = get_base(weight, f5)
    ta   = temp_alt_adj(temp, alt, tat)
    sw   = slope_wind_adj(weight, slp, wind_v, swt)

    V1 = round(base["V1"] + ta["V1"] + sw)
    VR = round(base["VR"] + ta["VR"])
    V2 = round(base["V2"] + ta["V2"])

    st.session_state["results"]["V1"] = V1
    st.session_state["results"]["VR"] = VR
    st.session_state["results"]["V2"] = V2

    st.markdown('<div class="vsec">Takeoff V-Speeds · Flaps 5</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="vg">
      <div class="vc vc1">
        <div class="vc-k">V1</div>
        <div class="vc-d">Decision Speed</div>
        <div class="vc-v">{V1}</div>
        <div class="vc-u">kt</div>
      </div>
      <div class="vc vcr">
        <div class="vc-k">VR</div>
        <div class="vc-d">Rotation Speed</div>
        <div class="vc-v">{VR}</div>
        <div class="vc-u">kt</div>
      </div>
      <div class="vc vc2">
        <div class="vc-k">V2</div>
        <div class="vc-d">Takeoff Safety Speed</div>
        <div class="vc-v">{V2}</div>
        <div class="vc-u">kt</div>
      </div>
    </div>
    <div class="cs">
      <span class="ci">Cond<span>{cond}</span></span>
      <span class="ci">MTOW<span>{fin:,.0f} kg</span></span>
      <span class="ci">PA<span>{inp.get('pa_input', pa_input):,} ft</span></span>
      <span class="ci">OAT<span>{temp} °C</span></span>
      <span class="ci">Wind<span>{wtyp} {wnd} kt</span></span>
      <span class="ci">Airport<span>{inp.get('airport_choice', airport_choice)} RWY {inp.get('runway_choice', runway_choice)}</span></span>
    </div>
    """, unsafe_allow_html=True)

# ── Placeholder ───────────────────────────────────────────────────
if "results" not in st.session_state and not calc_clicked:
    st.markdown("""
    <div class="ph">
      <div class="ph-t">Standby</div>
      <div class="ph-s">Configure inputs on the left · Press Calculate Final MTOW</div>
      <div class="ph-g">
        <div class="ph-c"><div class="ph-k">V1</div><div class="ph-v">—</div><div class="ph-u">kt</div></div>
        <div class="ph-c"><div class="ph-k">VR</div><div class="ph-v">—</div><div class="ph-u">kt</div></div>
        <div class="ph-c"><div class="ph-k">V2</div><div class="ph-v">—</div><div class="ph-u">kt</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)