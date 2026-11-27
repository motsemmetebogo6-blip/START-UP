"""
optimise.py – Increment 2b: how the selected design was optimised, and how robust it is.

Problem O-1 (least intervention): choose PF, LF and hot-charge temperature T to MINIMISE T
(the hot-charging system is the largest capital item, R200 M, Ch. 15) subject to
    production M = 24 * S * PF * LF / SEC(T) >= 450 t/d        (DC-14, mandatory)
    S_on = P_on / PF <= 65 MVA  (always at rating on load)     (DC-01)
    0.93 <= PF <= 0.95                                          (DC-02, supervisor limit)
    0.95 <= LF <= LF_max                                        (LF_max = achievable uptime, varied)
    SEC(T) = SEC0 - s * (T - T_ref)/100                          (vendor rule, R-04)
Solved numerically (SLSQP) and checked against the closed-form solution
    T* = T_ref + 100 * (SEC0 - 24 S PF* LF* / 450) / s,  with PF* = 0.95, LF* = LF_max.
Problem O-2: maximum production for given limits.
Uncertainty: Monte-Carlo propagation and one-at-a-time tornado for the selected design C1.
"""
import numpy as np
from scipy.optimize import minimize


def sec_of_T(T, SEC0, s, T_ref):
    return SEC0 - s * (T - T_ref) / 100.0


def production(PF, LF, T, S, SEC0, s, T_ref):
    return 24.0 * S * PF * LF / sec_of_T(T, SEC0, s, T_ref)


def T_closed_form(PF, LF, S, SEC0, s, T_ref, target=450.0):
    sec_req = 24.0 * S * PF * LF / target
    return T_ref + 100.0 * (SEC0 - sec_req) / s


def solve_min_T(S, SEC0, s, T_ref, LF_max, pf_lim=(0.93, 0.95), target=450.0, T_max=900.0):
    cons = [{"type": "ineq", "fun": lambda x: production(x[0], x[1], x[2], S, SEC0, s, T_ref) - target}]
    bounds = [pf_lim, (0.95, LF_max), (T_ref, T_max)]
    best = None
    for x0 in ([0.94, 0.95, 600.0], [0.95, LF_max, 400.0], [0.93, 0.96, 800.0]):
        r = minimize(lambda x: x[2], x0, bounds=bounds, constraints=cons, method="SLSQP",
                     options={"ftol": 1e-10, "maxiter": 500})
        if r.success and (best is None or r.fun < best.fun):
            best = r
    return best


def monte_carlo(n, S, SEC0, rng, dist):
    """dist: dict of samplers -> arrays. Returns production samples for C1."""
    s = dist["s"](rng, n); T = dist["T"](rng, n); LF = dist["LF"](rng, n); PF = dist["PF"](rng, n)
    sec0 = dist["SEC0"](rng, n); Tref = dist["T_ref"](rng, n)
    M = 24.0 * S * PF * LF / (sec0 - s * (T - Tref) / 100.0)
    return M, dict(s=s, T=T, LF=LF, PF=PF, SEC0=sec0, T_ref=Tref)


def tornado(base, ranges, S):
    """One-at-a-time: production of C1 at low/high of each input, others at base."""
    out = []
    f = lambda p: 24.0 * S * p["PF"] * p["LF"] / (p["SEC0"] - p["s"] * (p["T"] - p["T_ref"]) / 100.0)
    M0 = f(base)
    for k, (lo, hi, label) in ranges.items():
        pl, ph = dict(base), dict(base); pl[k] = lo; ph[k] = hi
        out.append((label, k, lo, hi, f(pl), f(ph)))
    out.sort(key=lambda r: -abs(r[5] - r[4]))
    return M0, out


def robust_T(S, SEC0, target, p_req, rng, n=60000, s_lo=0.035, s_hi=0.070, T_grid=None,
             lf=(0.95, 0.972, 0.98), pf=(0.93, 0.95, 0.95), sec_sd=0.035, T_spread=50.0, T_ref=25.0):
    """Chance-constrained design: smallest design preheat temperature T_d with P(M >= target) >= p_req.
    Achieved T ~ Tri(T_d - spread, T_d, T_d + spread); other inputs as in the Monte-Carlo (A-27)."""
    if T_grid is None:
        T_grid = np.arange(400, 1001, 5)
    s = rng.uniform(s_lo, s_hi, n); LF = rng.triangular(*lf, n); PF = rng.triangular(*pf, n)
    sec0 = rng.normal(SEC0, sec_sd, n); u = rng.triangular(-1, 0, 1, n)
    curve = []
    for Td in T_grid:
        T = Td + T_spread * u
        M = 24.0 * S * PF * LF / (sec0 - s * (T - T_ref) / 100.0)
        curve.append((Td, float((M >= target).mean())))
    feas = [t for t, p in curve if p >= p_req]
    return (feas[0] if feas else None), curve
