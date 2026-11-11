"""
parameters.py – single source of input values for all calculations.

Tags:  S = specified in brief / by Project Leader
       A = assumption (see assumptions register, docs/01)
       L = literature value (see references/REFERENCES.md; status AB = abstract-level only)
No plant operating data exists for this scenario (S-10): nothing here is plant data.
"""

# ---- Specified [S] ----------------------------------------------------------
P_BASE_MW = 55.0          # S-01 furnace active power, baseline
P_NEW_MW = 60.0           # S-02 furnace active power, uprate
S_RATED_MVA = 65.0        # S-03/S-07 total installed transformer rating
F_HZ = 50.0               # South African grid frequency (S-10 context; A-15)

# ---- Assumptions [A] --------------------------------------------------------
# A-11: P is active power into the furnace (secondary side); HV-metered = sensitivity
# A-14: the existing 55 MW furnace already runs on the 65 MVA bank at full MVA
S_BASE_MVA = 65.0
# A-06: secondary-circuit electrical efficiency (sensitivity only)
ETA_EL_RANGE = (0.94, 0.96, 0.98, 1.00)
# A-16: baseline electrode diameter taken equal to published 63 MVA FeCr analogue
D_ELECTRODE_M = 1.55      # L: R-11 (two 63 MVA SA FeCr SAFs, 1.55 m Söderberg) [AB]

# ---- Literature [L] ---------------------------------------------------------
# Westly similarity  I[kA] = C3 * P[MW]^(2/3)  (P = total furnace power)
C3_FECR_RANGE = (6.0, 11.0)      # R-12 reported range for HC FeCr [AB]
# Calibration analogue: FeCr furnace, 48 MW, 1.55 m electrodes, 110 kA (R-13) [AB]
ANALOGUE_P_MW, ANALOGUE_I_KA = 48.0, 110.0
# Söderberg current-density guideline for D > 1.3 m (R-08, patent, low confidence)
J_GUIDE_A_CM2 = (4.5, 5.0)
# Typical upper PF for SAFs; ~70 % of reactance from short network (R-14) [AB]
PF_TYPICAL_LIMIT = 0.85
SHORT_NETWORK_X_SHARE = 0.70

# ============================================================================
# Reference Furnace Specification inputs (docs/03, WP1) – added Rev 1
# ============================================================================
# Geometry ratios from two published FeCr SAFs (R-16: PCD/D 2.44, hearth/PCD 2.55;
# R-17: PCD/D 3.0, hearth/PCD 2.67). Mid-range adopted.
PCD_D_RATIO = 2.70            # A-19
HEARTH_PCD_RATIO = 2.60       # A-20
SHELL_ID_M = 13.7             # L: R-11 (63 MVA SA FeCr analogue, inner shell diameter) [AB]
# HV supply (no data). Typical SA furnace supply levels 88 / 132 kV.
HV_KV = 132.0                 # A-21 (sensitivity: 88 kV)
HV_KV_ALT = 88.0
# Existing transformer secondary tap range (no data) – L confidence, drives EQ-01 class
TAP_RANGE_V = (260.0, 340.0)  # A-23
# Auxiliary plant (cooling water, off-gas, feed, tapping) design margin above 55 MW duty
AUX_DESIGN_MARGIN = 0.10      # A-22
# Process (mid-points of A-04 and A-09)
SEC_MWH_T = 3.25              # A-04 mid of 3.0-3.5 MWh/t (pelletised, preheated)
UTILISATION = 0.92            # A-09 mid of 0.90-0.95
# Feed: LG6 chromite concentrate, SAIMM (R-18) [AB]  (mass %)
FEED_CONC = dict(Cr2O3=44.2, FeO=24.1, Al2O3=13.8, MgO=11.5, SiO2=2.5)
FEED_CR_FE_REPORTED = 1.62
# Slag: SA FeCr case study (R-19) typical; Cr2O3 range from R-20 [AB]
SLAG_TYPICAL = dict(SiO2=30.0, Al2O3=26.0, MgO=23.0, CaO=2.0)
SLAG_CR2O3_RANGE = (4.5, 13.0)
