"""thermal_run.py: baseline electrode thermal solution, validation, mesh study, sensitivity, figures and Octave exports."""
import csv, json, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import thermal_fvm as F
from params import P

OUT = F.OUT
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})


def wcsv(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def metrics(c):
    zc, ax, surf = F.axis_profile(c)
    j, qi, qr = F.heat_balance(c["T"], c["re"], c["ze"], c["active"], c["kc"], c["qv"], c["dmask"], c["rob"])
    zs = F.K("z_shoe_top")
    return dict(Tmax=float(np.nanmax(c["T"])), T_axis_tip=float(ax[np.isfinite(ax)][0]),
                T_axis_roof=float(np.interp(P["z_roof_t"], zc, ax)), T_surf_stock=float(np.interp(P["z_stock"] - 0.2, zc, surf)),
                z500=F.z_cross(zc, ax, 500.0, zs - 1.0), z800=F.z_cross(zc, ax, 800.0, zs - 1.0),
                joule_MW=j / 1e6, from_bath_burden_MW=qi / 1e6, losses_MW=sum(qr.values()) / 1e6,
                balance_residual_W=float(qi + j - sum(qr.values())), loss_split_MW={k: v / 1e6 for k, v in qr.items()})


# ------------------------------------------------------------------------------------------------ validation
def analytic_test(nr=200):
    """Long cylinder, uniform source q, fixed surface temperature: T(0) = Ts + q R^2 / (4 k)."""
    R, k, q, Ts = 0.775, 15.0, 1.0e5, 100.0
    re = np.linspace(0, R, nr + 1); ze = np.linspace(0, 1.0, 5)
    nz = len(ze) - 1
    active = np.ones((nz, nr), bool)
    rob = {f: np.zeros((nz, nr)) for f in ("w", "e", "s", "n")}; rob.update({f + "T": np.zeros((nz, nr)) for f in ("w", "e", "s", "n")})
    rob["e"][:, -1] = 1e9; rob["eT"][:, -1] = Ts
    T, _ = F.solve_generic(re, ze, active, np.full((nz, nr), k), np.full((nz, nr), q), np.zeros((nz, nr), bool), np.zeros((nz, nr)), rob)
    exact_c = Ts + q * R ** 2 / (4 * k)
    return float(T[0, 0]), exact_c


def mesh_study():
    rows = []
    for s in (0.5, 1.0, 2.0):
        c = F.run_case(nr_scale=s); m = metrics(c)
        rows.append([s, int(c["active"].sum()), round(m["Tmax"], 1), round(m["T_axis_roof"], 1), round(m["z500"], 3), round(m["joule_MW"], 4), round(m["from_bath_burden_MW"], 4)])
    wcsv("validation_mesh_convergence.csv", ["mesh_scale", "active_cells", "Tmax_C", "T_axis_at_roof_C", "z500_m", "joule_MW", "heat_from_bath_burden_MW"], rows)
    return rows


# ------------------------------------------------------------------------------------------------ octave export
def export_octave(c):
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "octave_io"); os.makedirs(d, exist_ok=True)
    np.savetxt(os.path.join(d, "re.csv"), c["re"], delimiter=","); np.savetxt(os.path.join(d, "ze.csv"), c["ze"], delimiter=",")
    for nm, arr in (("active", c["active"].astype(float)), ("k", c["kc"]), ("q", c["qv"]), ("dmask", c["dmask"].astype(float)), ("dval", c["dval"])):
        np.savetxt(os.path.join(d, nm + ".csv"), arr, delimiter=",", fmt="%.17g")
    for f in ("w", "e", "s", "n"):
        np.savetxt(os.path.join(d, f"h_{f}.csv"), c["rob"][f], delimiter=",", fmt="%.17g")
        np.savetxt(os.path.join(d, f"T_{f}.csv"), c["rob"][f + "T"], delimiter=",", fmt="%.17g")
    T = np.where(np.isfinite(c["T"]), c["T"], -1.0)
    np.savetxt(os.path.join(d, "T_python.csv"), T, delimiter=",", fmt="%.17g")


# ------------------------------------------------------------------------------------------------ figures
def fig_field(c, m):
    re, ze, rc, zc, T = c["re"], c["ze"], c["rc"], c["zc"], c["T"]
    rm = np.concatenate([-re[::-1], re[1:]])
    Tm = np.concatenate([T[:, ::-1], T], axis=1)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 9.5), gridspec_kw={"width_ratios": [1.0, 1.0]})
    for ax, (z0, z1, ttl) in zip(axs, ((ze[0], 9.0, "(a) Furnace region"), (7.0, ze[-1], "(b) Electrode above the roof"))):
        pm = ax.pcolormesh(rm, ze, np.ma.masked_invalid(Tm), cmap="inferno", vmin=0, vmax=2600, shading="flat")
        rcm = np.concatenate([-rc[::-1], rc])
        cs = ax.contour(rcm, zc, np.ma.masked_invalid(Tm), levels=[500, 800, 1200, 1600, 1800, 2000, 2400], colors="white", linewidths=0.6)
        ax.clabel(cs, fmt="%d", fontsize=6.5)
        for zz in (0.0, P["z_metal"], P["z_bath"], P["z_stock"], P["z_roof_u"], P["z_roof_t"], F.K("z_shoe_top") - 1.0, F.K("z_shoe_top")):
            ax.axhline(zz, color="#cccccc", lw=0.3)
        ax.set_ylim(z0, z1); ax.set_xlim(-c["R_c"], c["R_c"]); ax.set_xlabel("r (m), mirrored"); ax.set_ylabel("z (m), hearth floor = 0")
        ax.set_title(ttl, fontsize=10); ax.set_aspect("equal")
    for z, lab in ((0.25, "metal 1732 C"), (1.2, "slag 1800 C"), (4.0, "burden (prescribed)"), (-0.7, "floor lining"), (6.8, "freeboard")):
        axs[0].text(-c["R_c"] + 0.1, z, lab, color="white" if z > 0 else "black", fontsize=7, va="center")
    axs[0].text(0, c["z_tip"] - 0.2, "tip", color="white", fontsize=7, ha="center", va="top")
    cb = fig.colorbar(pm, ax=axs, shrink=0.8, pad=0.02); cb.set_label("Temperature (C)")
    fig.suptitle("Temperature in the single-electrode unit cell (steady state, axisymmetric)\nInputs flagged ASSUMED in thermal_fvm.py: results are illustrative until material data and measured temperatures replace them", fontsize=10)
    fig.savefig(os.path.join(IMG, "thermal_temperature_field.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


def fig_axial(c, m):
    zc, ax, surf = F.axis_profile(c)
    fig, a = plt.subplots(figsize=(7.5, 8.5))
    a.plot(ax, zc, "r-", lw=1.6, label="electrode axis"); a.plot(surf, zc, "b-", lw=1.6, label="electrode surface")
    for z, lab in ((0.0, "hearth floor"), (P["z_metal"], "metal top"), (P["z_bath"], "slag top"), (P["z_stock"], "stock line"), (P["z_roof_t"], "roof top"),
                   (F.K("z_shoe_top"), "contact shoes top"), (c["z_tip"], "electrode tip")):
        a.axhline(z, color="#999", lw=0.5, ls=":"); a.text(2680, z, lab, fontsize=7, va="bottom", ha="right")
    for lv, z in ((500, m["z500"]), (800, m["z800"])):
        if z:
            a.plot([lv], [z], "ko"); a.annotate(f"{lv} C at z = {z:.2f} m", (lv, z), (lv + 250, z + 0.7), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.5))
    a.set_xlim(0, 2700); a.set_ylim(-1.41, F.K("z_col_top")); a.set_xlabel("Temperature (C)"); a.set_ylabel("z (m)")
    a.set_title("Axial temperature of the electrode"); a.legend(loc="center right"); a.grid(alpha=0.25)
    fig.savefig(os.path.join(IMG, "thermal_axial_profile.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    wcsv("axial_profile.csv", ["z_m", "T_axis_C", "T_surface_C"], [[round(z, 4), round(a_, 2) if np.isfinite(a_) else "", round(s_, 2) if np.isfinite(s_) else ""] for z, a_, s_ in zip(zc, ax, surf)])


def fig_radial(c):
    rc, zc, T = c["rc"], c["zc"], c["T"]
    fig, a = plt.subplots(figsize=(7.5, 5))
    ir = np.searchsorted(rc, c["r_e"])
    for z in (1.8, 4.0, 6.0, 7.5, 9.1):
        iz = int(np.argmin(abs(zc - z)))
        a.plot(rc[:ir], T[iz, :ir], label=f"z = {zc[iz]:.1f} m")
    a.set_xlabel("r (m), electrode radius 0.775"); a.set_ylabel("Temperature (C)"); a.grid(alpha=0.3); a.legend()
    a.set_title("Radial temperature across the electrode")
    fig.savefig(os.path.join(IMG, "thermal_radial_profiles.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


def sensitivity(base):
    rows = []
    def add(label, **kw):
        old = dict(F.THERMAL_INPUTS)
        rho = kw.pop("rho", None); over = kw.pop("over", {}); jsc = kw.pop("jscale", 1.0)
        if rho is not None:
            F.THERMAL_INPUTS["rho_electrode_uOhm_m"] = (rho, "ASSUMED", "")
        for kk, vv in over.items():
            F.THERMAL_INPUTS[kk] = (vv, "ASSUMED", "")
        c = F.run_case(jscale=jsc, **kw); m = metrics(c)
        F.THERMAL_INPUTS.clear(); F.THERMAL_INPUTS.update(old)
        rows.append([label, round(m["Tmax"]), round(m["T_axis_roof"]), round(m["z500"], 2), round(m["z800"], 2), round(m["joule_MW"], 2), round(m["from_bath_burden_MW"], 2)])
    add("baseline")
    add("k electrode 10", k_el=10.0); add("k electrode 30", k_el=30.0)
    add("resistivity 20", rho=20.0); add("resistivity 45", rho=45.0)
    add("current -10 %", jscale=0.9); add("current +10 %", jscale=1.1)
    add("tip height 1.0 m", z_tip=1.0); add("tip height 2.0 m", z_tip=2.0)
    add("burden profile exponent 1", over={"burden_profile_exponent": 1.0}); add("burden profile exponent 3", over={"burden_profile_exponent": 3.0})
    add("freeboard h 75", over={"h_freeboard": 75.0}); add("freeboard h 300", over={"h_freeboard": 300.0})
    add("shoe h 150", over={"h_shoe": 150.0}); add("shoe h 600", over={"h_shoe": 600.0})
    wcsv("sensitivity.csv", ["case", "Tmax_C", "T_axis_at_roof_C", "z500_m", "z800_m", "joule_MW", "heat_from_bath_burden_MW"], rows)
    return rows


def fig_sens(rows):
    labs = [r[0] for r in rows]; tm = [r[1] for r in rows]; z5 = [r[3] for r in rows]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
    y = np.arange(len(rows))[::-1]
    axs[0].barh(y, tm, color="#b8532b"); axs[0].axvline(tm[0], color="k", lw=0.8); axs[0].set_xlabel("Maximum temperature (C)")
    axs[1].barh(y, z5, color="#3b6e9e"); axs[1].axvline(z5[0], color="k", lw=0.8); axs[1].set_xlabel("Height of the 500 C isotherm on the axis (m)")
    axs[1].set_xlim(min(z5) - 0.3, max(z5) + 0.3)
    axs[0].set_yticks(y); axs[0].set_yticklabels(labs)
    for a in axs:
        a.grid(alpha=0.25, axis="x")
    fig.suptitle("Sensitivity of the electrode thermal solution to the assumed inputs", fontsize=10)
    fig.savefig(os.path.join(IMG, "thermal_sensitivity.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


def fig_balance(m):
    fig, a = plt.subplots(figsize=(6.5, 4))
    lab = ["Joule heat in\nthe electrode", "Net exchange with slag,\nmetal and burden", "Loss through\nthe floor", "Loss from the\nelectrode surface"]
    val = [m["joule_MW"], m["from_bath_burden_MW"], -m["loss_split_MW"].get("s", 0), -(m["loss_split_MW"].get("e", 0) + m["loss_split_MW"].get("n", 0))]
    a.bar(lab, val, color=["#c0392b", "#e67e22", "#2c6e9e", "#2c6e9e"]); a.axhline(0, color="k", lw=0.8)
    for i, v in enumerate(val):
        a.text(i, v + (0.05 if v >= 0 else -0.05), f"{v:.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8)
    a.set_ylabel("Heat flow into (+) or out of (-) the electrode cell (MW)"); a.set_title(f"Energy balance, residual {m['balance_residual_W']:.1e} W", fontsize=9)
    fig.savefig(os.path.join(IMG, "thermal_energy_balance.png"), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    c = F.run_case(); m = metrics(c)
    print(json.dumps(m, indent=1, default=float))
    tc, te = analytic_test()
    print("analytic test: numerical", tc, "exact", te, "rel err", abs(tc - te) / te)
    ms = mesh_study(); print(ms)
    rows = sensitivity(m); [print(r) for r in rows]
    export_octave(c)
    fig_field(c, m); fig_axial(c, m); fig_radial(c); fig_sens(rows); fig_balance(m)
    # field export
    wcsv("temperature_field.csv", ["r_m", "z_m", "T_C", "region"],
         [[round(c["rc"][i], 4), round(c["zc"][j], 4), round(c["T"][j, i], 2), int(c["region"][j, i])] for j in range(len(c["zc"])) for i in range(len(c["rc"])) if np.isfinite(c["T"][j, i])])
    res = dict(metrics=m, analytic=dict(numerical=tc, exact=te), mesh=ms, inputs={k: list(v) for k, v in F.THERMAL_INPUTS.items()})
    json.dump(res, open(os.path.join(OUT, "thermal_summary.json"), "w"), indent=1, default=float)
