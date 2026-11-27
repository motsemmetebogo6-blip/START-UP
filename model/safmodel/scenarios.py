"""
scenarios.py – named operating scenarios. Each scenario states exactly what "the power" means,
which resolves the three different meanings of "60 MW" found in the audit (doc 08, A.4).
"""
from dataclasses import dataclass

from . import electrical as el
from . import production as pr
from .provenance import Record


@dataclass
class Scenario:
    sid: str
    name: str
    PF: float
    LF: float
    SEC: float
    P_mean: float = None          # None -> furnace at full rating: P_mean = S*PF*LF
    definition: str = ""
    used_by: str = ""
    tag: str = "CALCULATED"


def build_scenarios(inp):
    S = inp["wb.transformer_capacity"].value
    PF0, LF0 = inp["wb.power_factor"].value, inp["wb.load_factor"].value
    SEC0 = inp["wb.specific_energy_baseline"].value
    pf1, lf1 = inp["prop.pf_c1"].value, inp["prop.lf_c1"].value
    sec_hot = pr.hot_charge_sec(SEC0, inp["asm.hot_charge_sec_saving_per_100C"].value,
                                inp["asm.hot_charge_temperature_C"].value, 25.0)   # ambient reference (AF-14, conservative)
    return [
        Scenario("A", "Existing operation (workbook)", PF0, LF0, SEC0, None,
                 "full rating on load; mean = 65 x 0.93 x 0.95", "Ch. 4, 7; Jeff Ch. 2"),
        Scenario("S-N55", "Brief '55 MW' read as continuous power", PF0, 1.0, SEC0, 55.0,
                 "55 MW continuous at PF 0.93", "Ngesi Ch. 9 (AF-02)"),
        Scenario("E1", "PF raised to 0.95, LF unchanged", pf1, LF0, SEC0, None,
                 "full rating; mean = 65 x 0.95 x 0.95", "Ch. 12"),
        Scenario("S-B", "60 MW MEAN (recommended definition) = E2", pf1, lf1, SEC0, 60.0,
                 "mean 60 MW at PF 0.95, LF 0.972", "Ch. 12, 14, 18"),
        Scenario("S-N60", "60 MW CONTINUOUS (LF = 1)", PF0, 1.0, SEC0, 60.0,
                 "60 MW continuous at PF 0.93", "Ngesi Ch. 9 (AF-01)"),
        Scenario("S-O60", "60 MW ON LOAD, LF unchanged", PF0, LF0, SEC0, 60.0 * LF0,
                 "on-load 60 MW at PF 0.93; mean = 60 x 0.95", "Simphiwe Ch. 16"),
        Scenario("P1", "Hot charging only (~500 C)", PF0, LF0, sec_hot, None,
                 "existing electrical + SEC from hot charging", "Ch. 12"),
        Scenario("C1", "60 MW mean + hot charging (selected)", pf1, lf1, sec_hot, 60.0,
                 "S-B electrical + SEC from hot charging", "Ch. 12, 14, 15, 18"),
    ]


def evaluate(sc, inp, hv_key="asm.hv_supply_kV"):
    S = inp["wb.transformer_capacity"].value
    P_mean = sc.P_mean if sc.P_mean is not None else S * sc.PF * sc.LF
    op = el.operating_point(P_mean, sc.PF, sc.LF, S, inp["lit.westly_C3"].value,
                            inp["lit.electrode_diameter_m"].value, inp[hv_key].value)
    target = inp["wb.ferrochrome_production_target"].value
    recs = []
    for k, (v, u, eq) in op.items():
        tag = "CALCULATED"
        note = "estimate: Westly C3 single-analogue calibration (AF-08)" if k.endswith("_est") else ""
        recs.append(Record(sc.sid, k, v, u, tag, eq, note))
    E = pr.daily_energy_MWh(P_mean)
    M = pr.production_tpd(P_mean, sc.SEC)
    recs += [
        Record(sc.sid, "SEC_MWh_t", sc.SEC, "MWh/t", "SUPPLIED" if sc.SEC == inp["wb.specific_energy_baseline"].value
               else "CALCULATED", "input / hot-charge rule"),
        Record(sc.sid, "E_daily_MWh", E, "MWh/d", "CALCULATED", "24 P_mean"),
        Record(sc.sid, "production_tpd", M, "t/d", "CALCULATED", "E / SEC"),
        Record(sc.sid, "production_change_pct_vs_actual", 100 * (M / inp["wb.ferrochrome_production_baseline"].value - 1),
               "%", "CALCULATED", "M / 393.65 - 1"),
        Record(sc.sid, "meets_450_tpd", 1.0 if M >= target - 1e-9 else 0.0, "bool", "CALCULATED", "M >= 450"),
        Record(sc.sid, "SEC_required_for_450", pr.sec_required(P_mean, target), "MWh/t", "CALCULATED", "E / 450"),
        Record(sc.sid, "PF_within_limit", 1.0 if sc.PF <= inp["asm.pf_upper_limit"].value + 1e-12 else 0.0,
               "bool", "CALCULATED", "PF <= 0.95"),
        Record(sc.sid, "S_on_within_rating", 1.0 if op["S_on_MVA"][0] <= S + 1e-6 else 0.0,
               "bool", "CALCULATED", "S_on <= 65"),
    ]
    return P_mean, recs
