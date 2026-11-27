"""
production.py – energy-limited production at the furnace electrical boundary.
  E_d = 24 * P_mean  (MWh/d)       M = E_d / SEC  (t/d)
"""


def daily_energy_MWh(P_mean):
    return 24.0 * P_mean


def production_tpd(P_mean, SEC):
    return daily_energy_MWh(P_mean) / SEC


def sec_required(P_mean, target_tpd):
    return daily_energy_MWh(P_mean) / target_tpd


def power_required(target_tpd, SEC):
    return target_tpd * SEC / 24.0


def hot_charge_sec(SEC_cold, saving_per_100C, T_C, T_ref_C=0.0):
    """Linear vendor rule of thumb (R-04): SEC falls by `saving` MWh/t per 100 C of feed preheat.
    T_ref = 0 C reproduces the project's screening assumption (3.5 - 0.07*5 = 3.15).
    NOTE: an ambient reference (~25 C) would give 3.1675; recorded as a limitation."""
    return SEC_cold - saving_per_100C * (T_C - T_ref_C) / 100.0
