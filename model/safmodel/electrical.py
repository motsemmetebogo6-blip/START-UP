"""
electrical.py – per-phase steady-state electrical model of the three-phase SAF supply.

Conventions (balanced three-phase, star-equivalent per electrode):
  S_rated   transformer bank rating (MVA) – 3 single-phase units, delta closed at the electrodes
  PF        power factor (cos phi); LF load factor = fraction of time on full load
  P_mean    time-average active power (MW)          P_mean = P_on * LF
  P_on      active power while on load (MW)         P_on   = S_on * PF
  S_on      apparent power while on load (MVA)      loading = S_on / S_rated
  I_e       electrode (= secondary line) current     I_e = C3 * P_on^(2/3)   [Westly, ESTIMATE]
  V_LL      secondary line voltage                   V_LL = S_on / (sqrt3 * I_e)
  I_w       winding current of each 1-phase unit    I_w = I_e / sqrt3        (delta)
  R, X      per-phase operating resistance / reactance:  P_on = 3 I_e^2 R,  X = R tan(phi)
  J         electrode current density                J = I_e / (pi D^2 / 4)
All functions are pure; units: MW, MVA, Mvar, kA, V, mOhm, A/cm2.
"""
import math

SQRT3 = math.sqrt(3.0)


def onload_from_mean(P_mean, LF):
    return P_mean / LF


def apparent_power(P_on, PF):
    return P_on / PF


def reactive_power(S, PF):
    return S * math.sqrt(1.0 - PF ** 2)


def rx_ratio(PF):
    return PF / math.sqrt(1.0 - PF ** 2)


def primary_line_current_A(S_MVA, V_kV):
    return S_MVA * 1e6 / (SQRT3 * V_kV * 1e3)


def electrode_current_kA(P_on, C3):
    """Westly (1974): I = C3 * P^(2/3); P total furnace MW on load, I in kA. ESTIMATE."""
    return C3 * P_on ** (2.0 / 3.0)


def secondary_voltage_V(S_MVA, I_kA):
    return S_MVA * 1e6 / (SQRT3 * I_kA * 1e3)


def winding_current_kA(I_kA):
    return I_kA / SQRT3


def resistance_reactance_mohm(P_on, I_kA, PF):
    I = I_kA * 1e3
    R = P_on * 1e6 / (3.0 * I ** 2)
    X = R * math.tan(math.acos(PF))
    return R * 1e3, X * 1e3


def current_density(I_kA, D_m):
    return I_kA * 1e3 / (math.pi / 4.0 * (D_m * 100.0) ** 2)


def pf_lf_required(P_mean_target, S_rated, PF=None, LF=None):
    """Return the PF (given LF) or LF (given PF) needed for a mean-power target at full rating."""
    if PF is not None:
        return P_mean_target / (S_rated * PF)
    if LF is not None:
        return P_mean_target / (S_rated * LF)
    return P_mean_target / S_rated          # required product PF*LF


def pf_route_current_ratio(PF0, PF1, route):
    """
    Ratio I1/I0 of electrode current when the power factor is raised from PF0 to PF1
    at constant on-load apparent power S (transformer at rating).
      route 'R': raise operating resistance R, reactance X unchanged  -> Z = X / sin(phi)
      route 'X': lower reactance X, resistance R unchanged             -> Z = R / cos(phi)
    With S = 3 I^2 Z fixed, I ∝ Z^-1/2. Independent of the C3 calibration.
    """
    s0, s1 = math.sqrt(1 - PF0 ** 2), math.sqrt(1 - PF1 ** 2)
    if route == "R":
        return math.sqrt(s1 / s0)
    if route == "X":
        return math.sqrt(PF1 / PF0)
    raise ValueError(route)


def operating_point(P_mean, PF, LF, S_rated, C3, D_m, V_HV_kV):
    """Full electrical operating point for one scenario. Returns dict metric -> (value, unit, equation)."""
    P_on = onload_from_mean(P_mean, LF)
    S_on = apparent_power(P_on, PF)
    Q_on = reactive_power(S_on, PF)
    I_e = electrode_current_kA(P_on, C3)
    V = secondary_voltage_V(S_on, I_e)
    R, X = resistance_reactance_mohm(P_on, I_e, PF)
    return {
        "P_mean_MW": (P_mean, "MW", "input or S*PF*LF"),
        "P_on_MW": (P_on, "MW", "P_on = P_mean / LF"),
        "S_on_MVA": (S_on, "MVA", "S_on = P_on / PF"),
        "Q_on_Mvar": (Q_on, "Mvar", "Q = S sin(phi)"),
        "loading_on_pct": (100 * S_on / S_rated, "%", "S_on / S_rated"),
        "headroom_on_MVA": (S_rated - S_on, "MVA", "S_rated - S_on"),
        "P_phase_mean_MW": (P_mean / 3, "MW", "P_mean / 3"),
        "RX_ratio": (rx_ratio(PF), "-", "PF / sqrt(1-PF^2)"),
        "I_primary_A_at_HV": (primary_line_current_A(S_on, V_HV_kV), "A", "S / (sqrt3 V_HV)"),
        "I_electrode_kA_est": (I_e, "kA", "C3 P_on^(2/3)  [ESTIMATE]"),
        "I_winding_kA_est": (winding_current_kA(I_e), "kA", "I_e / sqrt3 (delta)"),
        "V_secondary_LL_V_est": (V, "V", "S_on / (sqrt3 I_e)"),
        "R_phase_mohm_est": (R, "mOhm", "P_on / (3 I_e^2)"),
        "X_phase_mohm_est": (X, "mOhm", "R tan(phi)"),
        "J_A_cm2_est": (current_density(I_e, D_m), "A/cm2", "I_e / (pi D^2 / 4)"),
        "PFxLF": (PF * LF, "-", "PF*LF"),
    }
