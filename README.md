# ✈ Aero Performance System — B737-800

A professional-grade Boeing 737-800 takeoff performance calculator built with Python and Streamlit. The system automates the computation of Maximum Takeoff Weight (MTOW) across four regulatory limiting factors and derives certified V-speeds for any runway and atmospheric condition.

---

## Overview

Before every flight, pilots and dispatchers must cross-reference multiple Aircraft Flight Manual (AFM) performance tables to determine the maximum allowable takeoff weight. This process is time-consuming and error-prone when done manually.

**APS** automates this by reading certified performance data from an Excel AFM, applying bilinear interpolation across all relevant tables, and returning the most restrictive MTOW along with computed V-speeds — in under a second.

---

## Features

- **Four-factor MTOW computation** — Runway field limit, 2nd segment climb, obstacle clearance, and structural limit evaluated simultaneously
- **Certified V-speed output** — V1 (Decision), VR (Rotation), V2 (Takeoff Safety) with temperature, altitude, slope, and wind corrections
- **Dry & Wet runway support** — Separate performance tables for both surface conditions
- **Obstacle clearance logic** — Weight reduction automatically applied when a departure obstacle is present
- **Anti-ice & A/C pack corrections** — Weight adjustments for engine anti-ice ON and air conditioning pack OFF configurations
- **Airport database** — Six Algerian airports with real runway geometry (TORA, TODA, ASDA, slope, obstacles)
- **Aviation-grade dark UI** — Custom Streamlit interface styled to match real EFB (Electronic Flight Bag) aesthetics

---

## Project Structure

```
├── main.py          # Streamlit frontend — UI layout, inputs, results display
├── aero_data.py     # Backend — PerfCalculator class, data loading, interpolation
├── Data.xlsx        # Excel AFM — certified B737-800 performance tables
└── README.md
```

### `aero_data.py` — Backend Engine

The `PerfCalculator` class handles everything:

- **Data loading** — Parses all sheets from `Data.xlsx` on startup using `pandas`
- **`calculate_mtow_runway()`** — Applies slope and wind corrections to TORA, then interpolates field limit weight from OAT and pressure altitude tables
- **`calculate_mtow_2nd_segment()`** — Extracts climb limit weight based on OAT and PA, independent of runway length
- **`calculate_mtow_obstacle()`** — Interpolates obstacle weight limit from height and distance tables
- **`calculate_all()`** — Orchestrates all three computations, applies corrections, and returns `min()` of all limits

### `main.py` — Streamlit Frontend

- Sidebar for all pilot inputs (airport, runway, OAT, PA, wind, anti-ice, A/C pack, obstacle override)
- Main panel displays MTOW banner, four-factor breakdown grid, and V-speed cards
- Built with fully custom CSS — no third-party UI libraries

---

## Airport Database

| ICAO | Name | Elevation |
|------|------|-----------|
| DAAS | Setif — Ain Arnat | 1,016 ft |
| DAAG | Algiers — Houari Boumediene | 82 ft |
| DABB | Annaba — Rabah Bitat | 16 ft |
| DABP | Skikda | 16 ft |
| DABC | Constantine — Mohamed Boudiaf | 2,265 ft |
| DAFH | Hassi Messaoud | 463 ft |

---

## MTOW Limiting Factors

| Factor | Description |
|--------|-------------|
| **Runway Field Limit** | TORA corrected for slope and wind, then interpolated against OAT and pressure altitude |
| **2nd Segment Climb** | Minimum climb gradient after engine failure with gear up — driven by OAT and PA only |
| **Obstacle Clearance** | 35 ft clearance above departure obstacle; indexed by obstacle height and distance |
| **Structural MTOW** | Physical airframe limit — 79,000 kg for the B737-800 |

**Final MTOW = min(Runway, 2nd Segment, Obstacle, Structural)**

---

## V-Speed Corrections

V-speeds are derived from built-in lookup tables with three correction layers:

1. **Base speeds** — From weight-indexed Flaps 5 table (dry or wet)
2. **Temperature/altitude adjustment** — Corrects V1, VR, V2 for non-standard conditions
3. **Slope/wind adjustment** — Applied to V1 only

---

## Technology Stack

| Library | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `pandas` | Excel parsing and data manipulation |
| `numpy` | Array operations and 1D interpolation |
| `scipy` — `RegularGridInterpolator` | Bilinear 2D interpolation across performance tables |

---

## Installation & Usage

```bash
# 1. Clone the repository
git clone <repo-url>
cd aero-performance-system

# 2. Install dependencies
pip install streamlit pandas numpy scipy openpyxl

# 3. Place Data.xlsx in the project root

# 4. Run the application
streamlit run main.py
```

The app will open at `http://localhost:8501`.

---

## Configuration

**Anti-Ice corrections:**
- Anti-ice ON → −200 kg (runway limit), −250 kg (2nd segment), −300 kg (obstacle)

**Air Conditioning corrections:**
- A/C pack OFF → +400 kg (runway), +1,450 kg (2nd segment)
- A/C pack ON → +600 kg (obstacle, relative to pack-off reference)

---

## Aircraft Reference

| Parameter | Value |
|-----------|-------|
| Aircraft | Boeing 737-800 |
| Engines | CFM56-7B27 |
| Flap setting | Flaps 5 |
| Structural MTOW | 79,000 kg |
| Performance basis | Boeing AFM tables |

---

## Academic Context

This project was developed as a university aeronautical engineering assignment. All performance data is sourced from Boeing 737-800 Aircraft Flight Manual tables and is intended for educational purposes only.

> **Disclaimer:** This tool is for academic use only. It must not be used for actual flight operations. Always consult certified AFM data and qualified flight dispatchers for operational performance calculations.
