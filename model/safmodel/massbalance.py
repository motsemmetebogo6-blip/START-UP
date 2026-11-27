"""
massbalance.py – Increment 2: steady-state mass balance per tonne of alloy, solved as a
data-reconciliation problem.

Unknowns (kg per tonne alloy, all >= 0):
    m_o  ore blend (80 % pellets / 20 % lumpy, workbook recipe)
    m_r  reductant blend, dry (10 % coke / 54 % anthracite 1 / 36 % anthracite 2)
    m_q  quartz            m_l  limestone            m_s  slag
Balances (7 equations, 5 unknowns -> over-determined; weighted least squares, non-negative):
    Al2O3, MgO, CaO      feed = slag                                   (inert oxides)
    SiO2                 feed = slag + SiO2 reduced to Si in alloy
    Cr                   feed = alloy + slag (Cr2O3)                   (dust not measured)
    Fe                   feed = alloy + slag (FeO)
    C                    fixed carbon = C in alloy + C in slag + C to CO for oxide reduction
Each equation is divided by its own magnitude so the residuals are relative (%), and every
equation has equal weight. Residuals measure the internal consistency of the plant data.
Recovery of Cr is an OUTPUT. Off-gas is calculated from the reconciled flows.
Assumptions (stated in the report): reductant analyses on a dry basis; all reduction gas leaves
as CO (closed furnace, reducing conditions); dust/fume not measured -> not in the balance;
Ti, Mn, P, S, V minor elements reported in alloy are not balanced.
"""
import numpy as np
from scipy.optimize import lsq_linear

M = {"Cr": 51.996, "Fe": 55.845, "Si": 28.086, "C": 12.011, "O": 15.999, "Ca": 40.078,
     "Mg": 24.305, "Al": 26.982, "Ti": 47.867, "Mn": 54.938, "H": 1.008}
F_Cr_Cr2O3 = 2 * M["Cr"] / (2 * M["Cr"] + 3 * M["O"])
F_Fe_FeO = M["Fe"] / (M["Fe"] + M["O"])
F_Fe_Fe2O3 = 2 * M["Fe"] / (2 * M["Fe"] + 3 * M["O"])
F_Si_SiO2 = M["Si"] / (M["Si"] + 2 * M["O"])
MW_CO, MW_CO2, MW_H2O = M["C"] + M["O"], M["C"] + 2 * M["O"], 2 * M["H"] + M["O"]
VM3 = 22.414            # Nm3 per kmol (0 C, 1 atm)


def feeds_from_inputs(inp):
    """Composition vectors (mass fractions) of the five streams + alloy, from the workbook."""
    g = lambda k: inp[k].value / 100.0
    rp, rl = inp["recipe.ore.pellets"].value, inp["recipe.ore.small_lumpy_ore"].value
    ore = {k: rp * g(f"ore.pellets.{k} (%)") + rl * g(f"ore.small_lumpy_ore.{k} (%)")
           for k in ("Cr2O3", "FeO", "Al2O3", "MgO", "SiO2", "CaO", "TiO2", "MnO")}
    red_w = {m: inp[f"recipe.reductant.{m}"].value for m in ("coke", "anthracite_1", "anthracite_2")}
    def red(k):
        return sum(w * inp[f"reductants.{m}.{k}"].value / 100.0 for m, w in red_w.items())
    reductant = {"FC": red("Fixed carbon, DFC (%)"), "ash": red("Ash (%)"), "VM": red("Volatile matter (%)"),
                 "moist_total": red("Total moisture (%)"), "Al2O3": red("Al2O3 (%)"), "CaO": red("CaO (%)"),
                 "Fe2O3": red("Fe2O3 (%)"), "MgO": red("MgO (%)"), "SiO2": red("SiO2 (%)"), "TiO2": red("TiO2 (%)"),
                 "S": red("S XRF (%)")}
    q = {k: g(f"fluxes.quartz.{k} (%)") for k in ("Al2O3", "CaO", "Fe2O3", "MgO", "SiO2")}
    lime = {k: g(f"fluxes.limestone.{k} (%)") for k in ("Al2O3", "CaO", "Fe2O3", "MgO", "SiO2")}
    lime["CO2"] = 1.0 - inp["fluxes.limestone.Total oxide (%)"].value / 100.0      # loss on calcination
    alloy = {k: g(f"metal.metal.{k} (%)") for k in ("Cr", "Fe", "Si", "C", "Ti", "Mn")}
    slag = {k: g(f"slag.slag.{k} (%)") for k in ("Al2O3", "CaO", "Cr2O3", "FeO", "MgO", "SiO2", "C")}
    return ore, reductant, q, lime, alloy, slag


def oxygen_removed_per_t(alloy):
    """kg O removed per tonne alloy to produce the reduced metal (Cr, Fe from FeO basis, Si)."""
    a = {k: 1000.0 * v for k, v in alloy.items()}
    return (a["Cr"] * 3 * M["O"] / (2 * M["Cr"]) + a["Fe"] * M["O"] / M["Fe"] + a["Si"] * 2 * M["O"] / M["Si"])


def build_system(ore, red, q, lime, alloy, slag):
    """Return A (7x5), b (7), equation names. Columns: m_o, m_r, m_q, m_l, m_s (kg/t alloy)."""
    a = {k: 1000.0 * v for k, v in alloy.items()}
    SiO2_red = a["Si"] / F_Si_SiO2
    O_rem = oxygen_removed_per_t(alloy)
    C_need = a["C"] + O_rem * M["C"] / M["O"]                 # alloy C + C to CO (slag C added below)
    rows, rhs, names = [], [], []
    for ox in ("Al2O3", "MgO", "CaO"):
        rows.append([ore[ox], red[ox], q[ox], lime[ox], -slag[ox]]); rhs.append(0.0); names.append(ox)
    rows.append([ore["SiO2"], red["SiO2"], q["SiO2"], lime["SiO2"], -slag["SiO2"]]); rhs.append(SiO2_red); names.append("SiO2")
    rows.append([ore["Cr2O3"] * F_Cr_Cr2O3, 0, 0, 0, -slag["Cr2O3"] * F_Cr_Cr2O3]); rhs.append(a["Cr"]); names.append("Cr")
    rows.append([ore["FeO"] * F_Fe_FeO, red["Fe2O3"] * F_Fe_Fe2O3, q["Fe2O3"] * F_Fe_Fe2O3, lime["Fe2O3"] * F_Fe_Fe2O3,
                 -slag["FeO"] * F_Fe_FeO]); rhs.append(a["Fe"]); names.append("Fe")
    rows.append([0, red["FC"], 0, 0, -slag["C"]]); rhs.append(C_need); names.append("C")
    return np.array(rows, float), np.array(rhs, float), names


def solve(A, b, names):
    """Relative weighting: each equation scaled by the magnitude of its largest term."""
    scale = np.maximum(np.abs(A).max(axis=1) * 1000.0, np.abs(b))
    scale[scale == 0] = 1.0
    Aw, bw = A / scale[:, None], b / scale
    res = lsq_linear(Aw, bw, bounds=(0, np.inf), lsmr_tol="auto", method="bvls")
    x = res.x
    resid = A @ x - b
    rel = resid / scale
    return x, resid, rel, scale


def full_balance(inp, production_tpd=None):
    ore, red, q, lime, alloy, slag = feeds_from_inputs(inp)
    A, b, names = build_system(ore, red, q, lime, alloy, slag)
    x, resid, rel, scale = solve(A, b, names)
    m_o, m_r, m_q, m_l, m_s = x
    a = {k: 1000.0 * v for k, v in alloy.items()}
    # Cr distribution and recovery (output)
    Cr_in = m_o * ore["Cr2O3"] * F_Cr_Cr2O3
    Cr_slag = m_s * slag["Cr2O3"] * F_Cr_Cr2O3
    recovery = a["Cr"] / Cr_in
    # gases
    O_rem = oxygen_removed_per_t(alloy)
    n_CO = O_rem / M["O"]                                       # kmol CO /t (1 O -> 1 CO)
    CO2_lime = m_l * lime["CO2"]
    moist = m_r * red["moist_total"] / (1 - red["moist_total"])  # water with as-received reductant (dry basis A-26)
    vm = m_r * red["VM"]
    gas_mass = n_CO * MW_CO + CO2_lime + moist + vm
    gas_Nm3 = (n_CO + CO2_lime / MW_CO2 + moist / MW_H2O) * VM3   # VM volume not counted (composition unknown)
    total_in = m_o + m_r + moist + m_q + m_l
    total_out = 1000.0 + m_s + gas_mass
    out = {
        "m_ore": m_o, "m_reductant_dry": m_r, "m_quartz": m_q, "m_limestone": m_l, "m_slag": m_s,
        "m_reductant_moisture": moist, "Cr_in": Cr_in, "Cr_alloy": a["Cr"], "Cr_slag": Cr_slag,
        "Cr_unaccounted": Cr_in - a["Cr"] - Cr_slag, "Cr_recovery": recovery,
        "O_removed": O_rem, "CO_kmol": n_CO, "CO_kg": n_CO * MW_CO, "CO2_lime_kg": CO2_lime, "H2O_kg": moist,
        "VM_kg": vm, "gas_Nm3": gas_Nm3, "mass_in": total_in, "mass_out": total_out,
        "closure_pct": 100 * (total_out - total_in) / total_in,
        "slag_basicity_check": (slag["CaO"] + slag["MgO"]) / slag["SiO2"],
    }
    feed = (A * x).clip(min=0).sum(axis=1) + np.where(b < 0, -b, 0)      # positive (input) side of each balance
    eqs = [dict(equation=n, feed_kg=f, residual_kg=r, residual_rel_pct=100 * r / f, residual_scaled_pct=100 * rr)
           for n, f, r, rr in zip(names, feed, resid, rel)]
    if production_tpd:
        out["per_day"] = {k: out[k] * production_tpd / 1000.0 for k in
                          ("m_ore", "m_reductant_dry", "m_quartz", "m_limestone", "m_slag", "m_reductant_moisture")}
        out["per_day"]["gas_Nm3_h"] = out["gas_Nm3"] * production_tpd / 24.0
    return out, eqs, (A, b, names, x)
