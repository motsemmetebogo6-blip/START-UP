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
