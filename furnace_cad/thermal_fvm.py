"""
thermal_fvm.py: axisymmetric steady-state heat conduction with Joule heating (finite volume), single-electrode unit cell.

Equation  div(k grad T) + q = 0  in (r, z);  Dirichlet in the slag and metal (plant data temperatures),
Robin (film h to an environment temperature) on free surfaces, symmetry (adiabatic) at the cell edge.
This is the same physics as a COMSOL Heat Transfer in Solids model with Electromagnetic Heating reduced to a
specified volumetric source; the geometry is the single-electrode unit cell of the furnace in furnace_cad/params.py.

Provenance of every input is listed in THERMAL_INPUTS (DATA, DERIVED, ASSUMED).  Units: m, W, K, degrees C.
"""
import csv, json, math, os
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from params import P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thermal_results"); os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------------------------------
# inputs with provenance
# ---------------------------------------------------------------------------------------------------
I_ELECTRODE_KA = 130.107       # DERIVED: Westly estimate at C1 (docs/09, AF-08)
T_SLAG = 1800.05               # DATA: mean in-furnace slag temperature, Slag sheet L10
T_METAL = 1732.2               # DATA: alloy liquidus 1549.95 + mean superheat 182.25 (Metal sheet)
THERMAL_INPUTS = {
    "T_slag_C": (T_SLAG, "DATA", "Ferrochrome Data Workbook, Slag sheet, in-furnace temperature, mean"),
    "T_metal_C": (T_METAL, "DERIVED", "Alloy liquidus 1549.95 + superheat 182.25 (Metal sheet)"),
    "I_electrode_kA": (I_ELECTRODE_KA, "DERIVED", "Westly estimate at C1, C3 = 8.33 (A-18); not measured"),
    "rho_electrode_uOhm_m": (30.0, "ASSUMED", "Baked Soderberg carbon at operating temperature, low end of the typical range; replace with supplier data"),
    "k_electrode": (20.0, "ASSUMED", "W/(m K) baked carbon electrode, typical range 5 to 25"),
    "k_lining": (3.0, "ASSUMED", "W/(m K) magnesia-chrome type refractory, typical range 2 to 5"),
    "k_burden": (1.5, "ASSUMED", "W/(m K) effective, porous charge including radiation, typical range 0.5 to 3"),
    "h_bottom": (15.0, "ASSUMED", "W/(m2 K) shell bottom to ambient"),
    "T_ambient_C": (25.0, "ASSUMED", ""),
    "h_freeboard": (150.0, "ASSUMED", "W/(m2 K) electrode and burden surface to furnace gas (convection plus radiation)"),
    "T_gas_C": (700.0, "ASSUMED", "Furnace gas temperature in the freeboard"),
    "h_above_roof": (30.0, "ASSUMED", "W/(m2 K) electrode surface above the roof to ambient"),
    "burden_profile_exponent": (2.0, "ASSUMED", "Charge temperature T_gas + (T_slag - T_gas) * s^n, s = fraction of the burden depth above the bath"),
    "z_shoe_top": (9.6, "ASSUMED", "m: top of the contact-shoe band (current enters the electrode here); band is 1.0 m deep"),
    "h_shoe": (300.0, "ASSUMED", "W/(m2 K) water-cooled contact shoes on the electrode surface"),
    "T_shoe_water_C": (60.0, "ASSUMED", ""),
    "h_above_shoes": (15.0, "ASSUMED", "W/(m2 K) electrode surface above the shoes to ambient air"),
    "T_air_C": (40.0, "ASSUMED", ""),
    "z_col_top": (float(P["z_plate_t"] + 4.0), "ASSUMED", "m: top of the modelled electrode column (4 m above the support plate)"),
    "T_above_roof_C": (60.0, "ASSUMED", "Air around the electrode above the roof"),
}
K = lambda name: THERMAL_INPUTS[name][0]


# ---------------------------------------------------------------------------------------------------
# generic solver
# ---------------------------------------------------------------------------------------------------
def solve_generic(re, ze, active, kc, qv, dir_mask, dir_val, rob):
    """
    Cell-centred finite volume on a rectilinear (r, z) grid (axisymmetric).
    re, ze     : cell edges, length nr+1 and nz+1
    active     : bool (nz, nr)
    kc, qv     : conductivity W/(m K) and volumetric source W/m3 per cell
    dir_mask   : bool (nz, nr), dir_val: fixed temperature
    rob        : dict face -> (h, Tenv) arrays (nz, nr) for faces 'w','e','s','n' (h = 0: none)
    Returns T (nz, nr) with NaN in inactive cells, and the sparse system pieces.
    """
    nz, nr = active.shape
    rc = 0.5 * (re[1:] + re[:-1]); zc = 0.5 * (ze[1:] + ze[:-1])
    dr = np.diff(re); dz = np.diff(ze)
    idx = -np.ones((nz, nr), dtype=int)
    idx[active] = np.arange(active.sum())
    n = int(active.sum())
    rows, cols, vals = [], [], []
    b = np.zeros(n)
    diag = np.zeros(n)

    def add(i, j, g):
        rows.append(i); cols.append(j); vals.append(-g)
        diag[i] += g

    for iz in range(nz):
        for ir in range(nr):
            if not active[iz, ir]:
                continue
            i = idx[iz, ir]
            vol = math.pi * (re[ir + 1] ** 2 - re[ir] ** 2) * dz[iz]
            b[i] += qv[iz, ir] * vol
            k0 = kc[iz, ir]
            # east / west (radial)
            for (di, face, rf, dd) in ((1, "e", re[ir + 1], dr[ir] / 2), (-1, "w", re[ir], dr[ir] / 2)):
                jr = ir + di
                area = 2 * math.pi * rf * dz[iz]
                if 0 <= jr < nr and active[iz, jr]:
                    if dir_mask[iz, jr] and not dir_mask[iz, ir]:
                        g = area / (dd / k0)              # the fixed temperature of the neighbour acts at the shared face
                    else:
                        g = area / (dd / k0 + (dr[jr] / 2) / kc[iz, jr])
                    add(i, idx[iz, jr], g)
                else:
                    h, Te = rob[face][iz, ir], rob[face + "T"][iz, ir]
                    if h > 0 and area > 0:
                        g = area / (dd / k0 + 1.0 / h)
                        diag[i] += g; b[i] += g * Te
            # south / north (axial)
            for (dj, face, dd) in ((-1, "s", dz[iz] / 2), (1, "n", dz[iz] / 2)):
                jz = iz + dj
                area = math.pi * (re[ir + 1] ** 2 - re[ir] ** 2)
                if 0 <= jz < nz and active[jz, ir]:
                    if dir_mask[jz, ir] and not dir_mask[iz, ir]:
                        g = area / (dd / k0)
                    else:
                        g = area / (dd / k0 + (dz[jz] / 2) / kc[jz, ir])
                    add(i, idx[jz, ir], g)
                else:
                    h, Te = rob[face][iz, ir], rob[face + "T"][iz, ir]
                    if h > 0:
                        g = area / (dd / k0 + 1.0 / h)
                        diag[i] += g; b[i] += g * Te
    A = sp.coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr() + sp.diags(diag)
    A = A.tolil()
    # Dirichlet rows
    dflat = dir_mask[active]
    vflat = dir_val[active]
    for i in np.where(dflat)[0]:
        A.rows[i] = [i]; A.data[i] = [1.0]; b[i] = vflat[i]
    A = A.tocsr()
    x = spla.spsolve(A, b)
    T = np.full((nz, nr), np.nan)
    T[active] = x
    return T, dict(A=A, b=b, idx=idx, rc=rc, zc=zc, dr=dr, dz=dz)


def heat_balance(T, re, ze, active, kc, qv, dir_mask, rob):
    """Heat flows (W) for the free (non-Dirichlet) cells: Joule generation, inflow from fixed-temperature cells, Robin losses."""
    nz, nr = active.shape
    dr = np.diff(re); dz = np.diff(ze)
    vol = np.pi * (re[1:][None, :] ** 2 - re[:-1][None, :] ** 2) * dz[:, None]
    free = active & ~dir_mask
    joule = float(np.sum(qv[free] * vol[free]))
    q_in = 0.0
    q_in_clamp = 0.0
    q_rob = {}
    for iz in range(nz):
        for ir in range(nr):
            if not free[iz, ir]:
                continue
            k0 = kc[iz, ir]
            for (di, dj, face, dd, area) in (
                    (1, 0, "e", dr[ir] / 2, 2 * math.pi * re[ir + 1] * dz[iz]), (-1, 0, "w", dr[ir] / 2, 2 * math.pi * re[ir] * dz[iz]),
                    (0, -1, "s", dz[iz] / 2, math.pi * (re[ir + 1] ** 2 - re[ir] ** 2)), (0, 1, "n", dz[iz] / 2, math.pi * (re[ir + 1] ** 2 - re[ir] ** 2))):
                jr, jz = ir + di, iz + dj
                if 0 <= jr < nr and 0 <= jz < nz and active[jz, jr]:
                    if dir_mask[jz, jr]:
                        g = area / (dd / k0)
                        q_in += g * (T[jz, jr] - T[iz, ir])        # positive: from the fixed-temperature cell into the free cell
                else:
                    h = rob[face][iz, ir]
                    if h > 0 and area > 0:
                        g = area / (dd / k0 + 1.0 / h)
                        q_rob[face] = q_rob.get(face, 0.0) + g * (T[iz, ir] - rob[face + "T"][iz, ir])
    return joule, q_in, q_rob


# ---------------------------------------------------------------------------------------------------
# furnace single-electrode unit cell
# ---------------------------------------------------------------------------------------------------
def segs(points, n_per):
    out = [points[0]]
    for a, b, n in zip(points[:-1], points[1:], n_per):
        out += list(np.linspace(a, b, n + 1)[1:])
    return np.array(out)


def skin_source(rc, R, I, rho, f=50.0, mu0=4e-7 * math.pi):
    """Joule source per unit volume for AC current I (A, rms) in a long cylinder of radius R with skin effect.
    J(r) = A I0(k r), k = (1 + j)/delta, I1 identity gives the amplitude from the total current."""
    from scipy.special import iv
    delta = math.sqrt(2 * rho / (2 * math.pi * f * mu0))
    kk = (1 + 1j) / delta
    amp = I / abs(2 * math.pi * R * iv(1, kk * R) / kk)
    return rho * (amp * np.abs(iv(0, kk * rc))) ** 2


def build_cell(z_tip=None, k_el=None, k_bur=None, jscale=1.0, nr_scale=1.0):
    z_tip = P["z_tip"] if z_tip is None else z_tip
    k_el = K("k_electrode") if k_el is None else k_el
    k_bur = K("k_burden") if k_bur is None else k_bur
    r_e = P["D_e"] / 2
    R_c = P["R_hearth"] / math.sqrt(3.0)           # equal-area unit cell of one electrode (DERIVED)
    z_floor = -P["t_floor"]
    z_top = K("z_col_top")                           # top of the modelled electrode column (plate level)
    z_lv = [z_floor, 0.0, P["z_metal"], z_tip, P["z_bath"], P["z_stock"], P["z_roof_u"], P["z_roof_t"], K("z_shoe_top") - 1.0, K("z_shoe_top"), z_top]
    z_lv = sorted(set(round(z, 6) for z in z_lv))
    nzs = [max(2, int(round(s * (z1 - z0) * nr_scale))) for z0, z1, s in zip(z_lv[:-1], z_lv[1:], [8] * (len(z_lv) - 1))]
    ze = segs(z_lv, nzs)
    re = np.concatenate([np.linspace(0, r_e, int(24 * nr_scale) + 1), r_e + (R_c - r_e) * (np.linspace(0, 1, int(48 * nr_scale) + 1)[1:] ** 1.4)])
    nz, nr = len(ze) - 1, len(re) - 1
    rc = 0.5 * (re[1:] + re[:-1]); zc = 0.5 * (ze[1:] + ze[:-1])
    RR, ZZ = np.meshgrid(rc, zc)
    active = np.ones((nz, nr), bool)
    kc = np.zeros((nz, nr)); qv = np.zeros((nz, nr)); dmask = np.zeros((nz, nr), bool); dval = np.zeros((nz, nr))
    region = np.zeros((nz, nr), int)   # 0 void, 1 lining, 2 metal, 3 slag, 4 burden, 5 electrode
    el = (RR < r_e) & (ZZ > z_tip)
    for iz in range(nz):
        for ir in range(nr):
            z, r = zc[iz], rc[ir]
            if z < 0:
                region[iz, ir] = 1
            elif z < P["z_metal"]:
                region[iz, ir] = 2
            elif z < P["z_bath"]:
                region[iz, ir] = 5 if el[iz, ir] else 3
            elif z < P["z_stock"]:
                region[iz, ir] = 5 if el[iz, ir] else 4
            else:
                region[iz, ir] = 5 if el[iz, ir] else 0
    active = region > 0
    kc[region == 1] = K("k_lining"); kc[region == 4] = k_bur; kc[region == 5] = k_el
    kc[region == 2] = 20.0; kc[region == 3] = 2.0       # not used: Dirichlet
    # the charge is prescribed from the process: its temperature falls from the slag temperature at the bath to the gas temperature
    # at the stock line, because the gas-solid heat exchange and the reactions of the burden are outside a conduction model
    sfrac = np.clip((P["z_stock"] - ZZ) / (P["z_stock"] - P["z_bath"]), 0, 1)
    tb = K("T_gas_C") + (T_SLAG - K("T_gas_C")) * sfrac ** K("burden_profile_exponent")
    dmask[region == 4] = True; dval[region == 4] = tb[region == 4]
    dmask[region == 2] = True; dval[region == 2] = T_METAL
    dmask[region == 3] = True; dval[region == 3] = T_SLAG
    rho = K("rho_electrode_uOhm_m") * 1e-6
    qrad = skin_source(rc, r_e, I_ELECTRODE_KA * 1e3 * jscale, rho)          # W/m3 as a function of radius
    qfull = np.broadcast_to(qrad[None, :], (nz, nr)).copy()
    qfull[ZZ > K("z_shoe_top")] = 0.0                                          # no current above the contact shoes
    qv[region == 5] = qfull[region == 5]
    # Robin faces
    names = ("w", "e", "s", "n")
    rob = {f: np.zeros((nz, nr)) for f in names}; rob.update({f + "T": np.zeros((nz, nr)) for f in names})
    for iz in range(nz):
        for ir in range(nr):
            if not active[iz, ir]:
                continue
            z = zc[iz]
            # bottom face of the floor
            if iz == 0:
                rob["s"][iz, ir] = K("h_bottom"); rob["sT"][iz, ir] = K("T_ambient_C")
            # radial faces towards void: electrode surface in the freeboard, roof, shoe band and above
            if ir + 1 < nr and not active[iz, ir + 1]:
                if z < P["z_roof_u"]:
                    rob["e"][iz, ir] = K("h_freeboard"); rob["eT"][iz, ir] = K("T_gas_C")
                elif z < K("z_shoe_top") - 1.0:
                    rob["e"][iz, ir] = K("h_above_roof"); rob["eT"][iz, ir] = K("T_above_roof_C")
                elif z < K("z_shoe_top"):
                    rob["e"][iz, ir] = K("h_shoe"); rob["eT"][iz, ir] = K("T_shoe_water_C")
                else:
                    rob["e"][iz, ir] = K("h_above_shoes"); rob["eT"][iz, ir] = K("T_air_C")
            # burden top surface (north face of the burden cells at the stock line)
            if iz + 1 < nz and not active[iz + 1, ir]:
                rob["n"][iz, ir] = K("h_freeboard"); rob["nT"][iz, ir] = K("T_gas_C")
            # top of the electrode column
            if iz == nz - 1:
                rob["n"][iz, ir] = K("h_above_shoes"); rob["nT"][iz, ir] = K("T_air_C")
    return dict(re=re, ze=ze, rc=rc, zc=zc, active=active, kc=kc, qv=qv, dmask=dmask, dval=dval, rob=rob, region=region,
                r_e=r_e, R_c=R_c, z_tip=z_tip)


def run_case(**kw):
    c = build_cell(**kw)
    T, aux = solve_generic(c["re"], c["ze"], c["active"], c["kc"], c["qv"], c["dmask"], c["dval"], c["rob"])
    c["T"] = T
    return c


def axis_profile(c):
    T, zc, rc = c["T"], c["zc"], c["rc"]
    ie = np.searchsorted(rc, c["r_e"]) - 1
    el = c["region"][:, 0] == 5                      # electrode cells only
    ax = np.where(el, T[:, 0], np.nan)
    surf = np.where(el, T[np.arange(len(zc)), ie], np.nan)
    return zc, ax, surf


def z_cross(zc, T, level, z_min):
    """Highest z above z_min where the temperature on the profile falls through 'level' going up."""
    out = None
    for i in range(len(zc) - 1):
        if zc[i] >= z_min and np.isfinite(T[i]) and np.isfinite(T[i + 1]) and T[i] >= level > T[i + 1]:
            out = zc[i] + (zc[i + 1] - zc[i]) * (T[i] - level) / (T[i] - T[i + 1])
    return out


# ---------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    c = run_case()
    zc, ax, surf = axis_profile(c)
    joule, q_dir, q_rob = heat_balance(c["T"], c["re"], c["ze"], c["active"], c["kc"], c["qv"], c["dmask"], c["rob"])
    loss = sum(q_rob.values())
    z500 = z_cross(zc, ax, 500.0, c["z_tip"])
    print(f"cells {c['active'].sum()}, joule {joule/1e6:.3f} MW, Dirichlet to solids {q_dir/1e6:.3f} MW, Robin losses {loss/1e6:.3f} MW")
    print("balance residual (Dirichlet + Joule - losses) MW:", (q_dir + joule - loss) / 1e6)
    print("z(500 C) on the axis:", z500, " T at z=roof top:", np.interp(P['z_roof_t'], zc, ax), "T top:", ax[-1])
