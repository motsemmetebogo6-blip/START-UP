"""drawings.py: 2D engineering views (open cut section, top, side, bottom) with dimensions, from params.py. Units: m."""
import math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Arc
from params import P, TAG

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images"); os.makedirs(IMG, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "hatch.linewidth": 0.5})
LW = 1.1

R_so, R_si, R_h = P["R_shell_o"], P["R_shell_i"], P["R_hearth"]
zb, zr, zrt = P["z_bottom"], P["z_roof_u"], P["z_roof_t"]
re_, rt_ = P["D_e"] / 2, P["D_e"] / 2 - P["wall_e"]
xe, xt = P["R_e_axis"], P["R_tube_axis"]
zp0, zp1, zt = P["z_plate_b"], P["z_plate_t"], P["z_tube_top"]
star = lambda k: "*" if TAG[k][0] in ("PICTURE", "ASSUMED") else ""


def poly(ax, pts, fc="none", ec="k", hatch=None, lw=LW, z=2, ls="-"):
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, hatch=hatch, lw=lw, zorder=z, ls=ls))


def rect(ax, x0, z0, x1, z1, **kw):
    poly(ax, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], **kw)


def dim(ax, p1, p2, off, text, horizontal=True, fs=7.5, ext=True, text_off=0.0, tx=None):
    """Linear dimension between p1 and p2, dimension line displaced by off (m) perpendicular to the measured direction."""
    (x1, y1), (x2, y2) = p1, p2
    if horizontal:
        yd = max(y1, y2) + off if off >= 0 else min(y1, y2) + off
        a, b = (x1, yd), (x2, yd)
        if ext:
            for (x, y) in (p1, p2):
                ax.plot([x, x], [y + (0.15 if yd > y else -0.15), yd + (0.2 if yd > y else -0.2)], "k", lw=0.5)
        tx_, ty, rot = ((x1 + x2) / 2 if tx is None else tx), yd, 0
        va = "bottom" if off >= 0 else "top"
        ax.text(tx_, ty + (0.12 if off >= 0 else -0.12) + text_off, text, ha="center", va=va, fontsize=fs, rotation=rot, zorder=9)
    else:
        xd = max(x1, x2) + off if off >= 0 else min(x1, x2) + off
        a, b = (xd, y1), (xd, y2)
        if ext:
            for (x, y) in (p1, p2):
                ax.plot([x + (0.15 if xd > x else -0.15), xd + (0.2 if xd > x else -0.2)], [y, y], "k", lw=0.5)
        ax.text(xd + (-0.12 if off < 0 else 0.12), (y1 + y2) / 2 + text_off, text, ha="right" if off < 0 else "left", va="center", fontsize=fs, rotation=90, zorder=9)
    ax.annotate("", xy=a, xytext=b, arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color="k", shrinkA=0, shrinkB=0, mutation_scale=7), zorder=9)


def label(ax, xy, text, xytext, fs=7.5, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs, ha=ha, va="center", zorder=9,
                arrowprops=dict(arrowstyle="-", lw=0.5, color="k"))


def centreline(ax, x0, y0, x1, y1):
    ax.plot([x0, x1], [y0, y1], color="#1f4e9e", lw=0.6, ls=(0, (8, 2, 1, 2)), zorder=1)


# ------------------------------------------------------------------------------------------------
def section(ax):
    """Open cut: section on the plane y = 0 through the axis and electrode 1 (azimuth 0 deg), viewed from -y."""
    # steel shell
    rect(ax, -R_so, zb, R_so, zb + P["t_steel"], fc="#555b6e", hatch=None)
    for s in (-1, 1):
        rect(ax, s * R_si, zb + P["t_steel"], s * R_so, zrt, fc="#555b6e")
    # lining wall and floor
    for s in (-1, 1):
        x0, x1 = sorted((s * R_h, s * R_si))
        rect(ax, x0, 0, x1, zr, fc="#e8c9a0", hatch="////")
    rect(ax, -R_si, zb + P["t_steel"], R_si, 0, fc="#e8c9a0", hatch="////")
    # roof slab with the electrode opening
    rect(ax, -R_si, zr, xe - re_, zrt, fc="#d6d8e0", hatch="\\\\\\\\")
    rect(ax, xe + re_, zr, R_si, zrt, fc="#d6d8e0", hatch="\\\\\\\\")
    # process zones inside the cavity
    for (a, b, c, name) in ((0, P["z_metal"], "#f1d36b", "metal pad"), (P["z_metal"], P["z_bath"], "#f08a5d", "slag layer"),
                            (P["z_bath"], P["z_stock"], "#b49a85", "burden"), (P["z_stock"], zr, "#f4f6fb", "freeboard (gas)")):
        rect(ax, -R_h, a, R_h, b, fc=c, lw=0.6, z=1.5)
    ax.text(-R_h + 0.3, 0.25, "metal pad", fontsize=6.5, va="center"); ax.text(-R_h + 0.3, 1.35, "slag layer", fontsize=6.5, va="center")
    ax.text(-R_h + 0.3, 4.1, "burden", fontsize=6.5, va="center"); ax.text(-R_h + 0.3, 6.75, "freeboard", fontsize=6.5, va="center")
    # electrode 1: solid column inside the furnace (carbon), then hollow stub, oblique connector, vertical tube
    rect(ax, xe - re_, P["z_tip"], xe + re_, zrt, fc="#2e3038", hatch="xx", ec="k", z=3)
    for s in (-1, 1):
        x0, x1 = sorted((xe + s * re_, xe + s * rt_))
        rect(ax, x0, zrt, x1, zp0, fc="#9aa0b8")
    rect(ax, -P["D_plate"] / 2, zp0, P["D_plate"] / 2, zp1, fc="#c9cbe0", hatch="\\\\")
    # connector walls (oblique at 45 degrees), drawn as two parallel strips
    v = np.array([xt - xe, P["offset"]]); L = np.linalg.norm(v); u = v / L; n = np.array([-u[1], u[0]])
    p0 = np.array([xe, zp1])
    for r0, r1 in ((rt_, re_), (-re_, -rt_)):
        poly(ax, [p0 + r0 * n, p0 + r1 * n, p0 + r1 * n + v, p0 + r0 * n + v], fc="#9aa0b8")
    base_t = zp1 + P["offset"]
    for s in (-1, 1):
        x0, x1 = sorted((xt + s * re_, xt + s * rt_))
        rect(ax, x0, base_t, x1, zt, fc="#9aa0b8")
    # electrodes 2 and 3 (behind the section plane): outlines only
    for a in P["e_angles"][1:]:
        c = math.cos(math.radians(a))
        for xx, z0_, z1_, w in ((P["R_e_axis"] * c, P["z_tip"], zrt, re_), (P["R_tube_axis"] * c, base_t, zt, re_)):
            ax.add_patch(Rectangle((xx - w, z0_), 2 * w, z1_ - z0_, fc="none", ec="#777", lw=0.6, ls="--", zorder=1))
    # centrelines
    centreline(ax, 0, zb - 1.0, 0, zt + 1.0); centreline(ax, xe, P["z_tip"] - 0.6, xe, zp1 + 0.5); centreline(ax, xt, base_t - 0.5, xt, zt + 0.6)
    # ---- dimensions
    X = R_so + 0.9
    dim(ax, (R_so, zb), (R_so, zt), 1.2, f"{P['H_total']:.2f}", horizontal=False, text_off=0)
    dim(ax, (R_so, zb), (R_so, zrt), 0.55, f"{P['H_body']:.2f}", horizontal=False)
    dim(ax, (xt + re_, zp1 + P["offset"]), (xt + re_, zt), 1.0, f"{P['L_tube']:.2f}{star('L_tube')}", horizontal=False)
    dim(ax, (-R_so, zb), (R_so, zb), -1.1, f"shell outer {2 * R_so:.2f}", horizontal=True)
    dim(ax, (-R_h, 4.9), (R_h, 4.9), 0.0, f"hearth {P['D_hearth']:.2f}", horizontal=True, ext=False, tx=-2.5)
    dim(ax, (-P["D_plate"] / 2, zp1), (P["D_plate"] / 2, zp1), 0.9, f"support plate {P['D_plate']:.2f}{star('D_plate')}", horizontal=True, tx=-2.6)
    dim(ax, (xe - re_, zrt + 0.4), (xe + re_, zrt + 0.4), 0.0, f"{P['D_e']:.2f}", horizontal=True, ext=False)
    dim(ax, (0, zr - 0.7), (xe, zr - 0.7), 0.0, f"PCD/2 = {xe:.3f}", horizontal=True, ext=False, tx=-1.4)
    dim(ax, (-R_si, zb + P["t_steel"]), (-R_si, 0), -0.7, f"{P['t_floor']:.2f}{star('t_floor')}", horizontal=False)
    dim(ax, (-R_h, 3.0), (-R_si, 3.0), 0.0, f"{P['t_lining']:.2f}", horizontal=True, ext=False)
    dim(ax, (-R_si, 0), (-R_si, zr), -1.7, f"cavity {P['H_cavity']:.2f}{star('H_cavity')}", horizontal=False)
    dim(ax, (-R_si, zr), (-R_si, zrt), -0.5, f"{P['t_roof']:.2f}{star('t_roof')}", horizontal=False)
    dim(ax, (xe + 2.2, P["z_tip"]), (xe + 2.2, zrt), 0.0, f"column {zrt - P['z_tip']:.2f}", horizontal=False, ext=False)
    dim(ax, (xe + 3.0, zrt), (xe + 3.0, zp0), 0.0, f"{P['h_stub']:.2f}{star('h_stub')}", horizontal=False, ext=False)
    dim(ax, (xe, zp1 + 3.0), (xt, zp1 + 3.0), 0.0, f"offset {P['offset']:.2f}{star('offset')}", horizontal=True, ext=False, tx=xe - 1.6)
    ax.plot([xe, xe], [zp1 + 2.9, zp1 + 3.1], "k", lw=0.5); ax.plot([xt, xt], [zp1 + 2.9, zp1 + 3.1], "k", lw=0.5)
    ax.text(xe - 1.0, P["z_tip"] - 0.55, "electrode tip z = %.2f*" % P["z_tip"], fontsize=6.5, va="center", ha="right", zorder=9)
    ax.set_xlim(-R_so - 3.3, R_so + 3.8); ax.set_ylim(zb - 2.2, zt + 2.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("SECTION A-A (open cut through the axis and electrode 1)", fontsize=9, fontweight="bold")


# ------------------------------------------------------------------------------------------------
def top(ax):
    ax.add_patch(Circle((0, 0), R_so, fc="none", ec="k", lw=LW))
    ax.add_patch(Circle((0, 0), R_h, fc="none", ec="#555", lw=0.7, ls="--"))
    ax.add_patch(Circle((0, 0), P["D_plate"] / 2, fc="none", ec="k", lw=LW))
    ax.add_patch(Circle((0, 0), xe, fc="none", ec="#1f4e9e", lw=0.5, ls=(0, (8, 2, 1, 2))))
    for k, a in enumerate(P["e_angles"]):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        for r_, rad in ((xe, re_), (xt, re_)):
            ax.add_patch(Circle((r_ * c, r_ * s), rad, fc="#e6e8f2" if r_ == xt else "none", ec="k", lw=LW, zorder=3))
            ax.add_patch(Circle((r_ * c, r_ * s), rt_, fc="white", ec="k", lw=0.6, zorder=4))
        # connector (oblique tube) in plan
        ax.plot([xe * c, xt * c], [xe * s, xt * s], "k", lw=0.6, zorder=2)
        ax.text(xt * c * 1.0, xt * s * 1.0 - 0.0, f"E{k + 1}", fontsize=7, ha="center", va="center", zorder=10)
    for a in P["tap_angles"]:
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        w = P["D_tap_o"] / 2
        p0, p1 = np.array([R_so * c, R_so * s]), np.array([(R_so + P["L_tap"]) * c, (R_so + P["L_tap"]) * s])
        n = np.array([-s, c]) * w
        poly(ax, [p0 + n, p1 + n, p1 - n, p0 - n], fc="white", z=1)
        centreline(ax, 0.0, 0.0, p1[0] * 1.05, p1[1] * 1.05)
    centreline(ax, -R_so - 1.5, 0, R_so + 3.2, 0); centreline(ax, 0, -R_so - 3.2, 0, R_so + 1.5)
    # dimensions
    dim(ax, (-R_so, R_so), (R_so, R_so), 0.9, f"{2 * R_so:.2f}", horizontal=True)
    dim(ax, (-P["D_plate"] / 2, -R_so), (P["D_plate"] / 2, -R_so), -0.9, f"support plate {P['D_plate']:.2f}{star('D_plate')}", horizontal=True, ext=False)
    c1, s1 = math.cos(math.radians(120)), math.sin(math.radians(120))
    ax.annotate("", xy=(xe * math.cos(math.radians(60)) * 0 + xe, 0), xytext=(-xe, 0), arrowprops=dict(arrowstyle="<|-|>", lw=0.7, shrinkA=0, shrinkB=0, mutation_scale=7), zorder=9)
    ax.text(0, 0.18, f"PCD {P['PCD']:.2f}", fontsize=7.5, ha="center", va="bottom", zorder=9)
    # electrode diameter leader and tap labels
    label(ax, (xt + re_ * 0.7, 0.0 + re_ * 0.7), f"tube OD {P['D_e']:.2f}", (xt + 2.3, 2.4))
    a0 = P["tap_angles"][0]; c, s = math.cos(math.radians(a0)), math.sin(math.radians(a0))
    label(ax, ((R_so + P["L_tap"] * 0.6) * c, (R_so + P["L_tap"] * 0.6) * s), f"tap pipe OD {P['D_tap_o']:.2f}{star('D_tap_o')}, bore {P['D_tap_i']:.2f}\nprojection {P['L_tap']:.2f}{star('L_tap')}",
          (-R_so - 3.2, -R_so - 1.0), ha="center")
    ax.text(R_so + 0.3, R_so * 0.55, f"hearth {P['D_hearth']:.2f}\n(hidden, dashed)", fontsize=7, ha="left", color="#444")
    for a, nm in zip(P["tap_angles"], ("T1", "T2")):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        ax.text((R_so + P["L_tap"] + 0.6) * c, (R_so + P["L_tap"] + 0.6) * s, f"{nm} {a:.0f}°", fontsize=7, ha="center", va="center")
    ax.set_xlim(-R_so - 4.2, R_so + 4.4); ax.set_ylim(-R_so - 4.2, R_so + 2.6)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title("TOP VIEW", fontsize=9, fontweight="bold")


# ------------------------------------------------------------------------------------------------
def side(ax):
    """Front elevation seen from -y."""
    rect(ax, -R_so, zb, R_so, zrt, fc="#e1e3ec")
    rect(ax, -P["D_plate"] / 2, zp0, P["D_plate"] / 2, zp1, fc="#c9cbe0")
    base_t = zp1 + P["offset"]
    for k, a in enumerate(P["e_angles"]):
        c = math.cos(math.radians(a)); xs, xt_ = xe * c, xt * c
        rect(ax, xs - re_, zrt, xs + re_, zp0, fc="#e6e8f2", lw=0.8)
        poly(ax, [(xs - re_, zp1), (xs + re_, zp1), (xt_ + re_, base_t), (xt_ - re_, base_t)], fc="#e6e8f2", lw=0.8)
        rect(ax, xt_ - re_, base_t, xt_ + re_, zt, fc="#e6e8f2", lw=0.8)
    for a in P["tap_angles"]:
        c = math.cos(math.radians(a)); x0, x1 = R_so * c, (R_so + P["L_tap"]) * c
        rect(ax, min(x0, x1), P["z_tap"] - P["D_tap_o"] / 2, max(x0, x1), P["z_tap"] + P["D_tap_o"] / 2, fc="#e6e8f2", lw=0.9, z=4)
    ax.plot([-R_so, R_so], [0, 0], color="#555", lw=0.5, ls="--"); ax.text(0.2, 0.15, "hearth floor z = 0 (hidden)", fontsize=6.5, va="bottom", color="#444")
    centreline(ax, 0, zb - 1, 0, zt + 1)
    dim(ax, (R_so, zb), (R_so, zt), 1.2, f"{P['H_total']:.2f}", horizontal=False)
    dim(ax, (R_so, zb), (R_so, zrt), 0.55, f"{P['H_body']:.2f}", horizontal=False)
    dim(ax, (-R_so, zb), (R_so, zb), -1.1, f"{2 * R_so:.2f}", horizontal=True)
    dim(ax, (-R_so, zt), (R_so, zt), 0.0, "", horizontal=True, ext=False) if False else None
    xs3 = [xt * math.cos(math.radians(a)) for a in P["e_angles"]]
    dim(ax, (min(xs3), zt), (max(xs3), zt), 0.9, f"tube centres {max(xs3) - min(xs3):.2f}", horizontal=True)
    dim(ax, (-P["D_plate"] / 2, zp1), (P["D_plate"] / 2, zp1), 1.4, f"plate {P['D_plate']:.2f}{star('D_plate')}", horizontal=True)
    dim(ax, (-R_so, zrt), (-R_so, zp0), -0.5, f"{P['h_stub']:.2f}{star('h_stub')}", horizontal=False, ext=False)
    ax.text(-R_so - 0.4, zb + (P["z_tap"] - zb), "", fontsize=6)
    xl = min(R_so * math.cos(math.radians(a)) for a in P["tap_angles"]) - P["L_tap"] * 0.6
    dim(ax, (-R_so - P["L_tap"] * math.cos(math.radians(35)) - 0.3, P["z_tap"] - P["D_tap_o"] / 2), (-R_so - P["L_tap"] * math.cos(math.radians(35)) - 0.3, P["z_tap"] + P["D_tap_o"] / 2), -0.5,
        f"{P['D_tap_o']:.2f}{star('D_tap_o')}", horizontal=False, ext=False)
    ax.text(-R_so - 4.0, P["z_tap"] + 1.6, f"tap pipes at {P['tap_angles'][0]:.0f}°, {P['tap_angles'][1]:.0f}°\nheight {P['z_tap']:.2f}{star('z_tap')} above hearth", fontsize=7)
    ax.set_xlim(-R_so - 4.5, R_so + 4.0); ax.set_ylim(zb - 2.2, zt + 2.0)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title("SIDE VIEW (front elevation)", fontsize=9, fontweight="bold")


# ------------------------------------------------------------------------------------------------
def bottom(ax):
    """View from below: x as in the top view, y mirrored."""
    f = lambda a: -a
    ax.add_patch(Circle((0, 0), R_so, fc="#e1e3ec", ec="k", lw=LW))
    ax.add_patch(Circle((0, 0), R_h, fc="none", ec="#555", lw=0.7, ls="--"))
    for k, a in enumerate(P["e_angles"]):
        c, s = math.cos(math.radians(a)), -math.sin(math.radians(a))
        ax.add_patch(Circle((xe * c, xe * s), re_, fc="none", ec="#555", lw=0.7, ls="--"))
        ax.text(xe * c, xe * s, f"E{k + 1}", fontsize=7, ha="center", va="center")
    for a, nm in zip(P["tap_angles"], ("T1", "T2")):
        c, s = math.cos(math.radians(a)), -math.sin(math.radians(a))
        w = P["D_tap_o"] / 2
        p0, p1 = np.array([R_so * c, R_so * s]), np.array([(R_so + P["L_tap"]) * c, (R_so + P["L_tap"]) * s])
        n = np.array([-s, c]) * w
        poly(ax, [p0 + n, p1 + n, p1 - n, p0 - n], fc="white", z=1)
        ax.text((R_so + P["L_tap"] + 0.6) * c, (R_so + P["L_tap"] + 0.6) * s, f"{nm}", fontsize=7, ha="center", va="center")
        centreline(ax, 0, 0, p1[0] * 1.05, p1[1] * 1.05)
    centreline(ax, -R_so - 1.5, 0, R_so + 3.2, 0); centreline(ax, 0, -R_so - 3.2, 0, R_so + 1.5)
    dim(ax, (-R_so, R_so), (R_so, R_so), 0.9, f"{2 * R_so:.2f}", horizontal=True)
    dim(ax, (-R_h, -R_so), (R_h, -R_so), -0.9, f"hearth (hidden) {P['D_hearth']:.2f}", horizontal=True, ext=False)
    a0 = P["tap_angles"][0]; c, s = math.cos(math.radians(a0)), -math.sin(math.radians(a0))
    label(ax, ((R_so + P["L_tap"] * 0.6) * c, (R_so + P["L_tap"] * 0.6) * s), f"tap projection {P['L_tap']:.2f}{star('L_tap')}", (-R_so - 3.2, R_so * 0.6), ha="center")
    ax.text(R_h * 0.2, -R_h * 0.92, f"shell bottom plate t = {P['t_steel']:.2f}{star('t_steel')}", fontsize=7, ha="center")
    ax.set_xlim(-R_so - 4.2, R_so + 4.4); ax.set_ylim(-R_so - 4.2, R_so + 2.6)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title("BOTTOM VIEW (seen from below)", fontsize=9, fontweight="bold")


def single(fn, name, size):
    fig, ax = plt.subplots(figsize=size)
    fn(ax)
    fig.text(0.01, 0.01, "All dimensions in metres.  * = estimated from the picture or assumed (not plant data); replace with the SolidWorks value.",
             fontsize=6.5, color="#444")
    for ext in ("png", "pdf", "svg"):
        fig.savefig(os.path.join(IMG, f"{name}.{ext}"), dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def sheet():
    fig = plt.figure(figsize=(16.5, 11.7))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.05, 1.0, 1.0], hspace=0.08, wspace=0.03)
    section_ax = fig.add_subplot(gs[:, 0]); top_ax = fig.add_subplot(gs[0, 1]); side_ax = fig.add_subplot(gs[0, 2])
    bot_ax = fig.add_subplot(gs[1, 1]); tb = fig.add_subplot(gs[1, 2])
    section(section_ax); top(top_ax); side(side_ax); bottom(bot_ax)
    tb.axis("off")
    rows = [("Project", "Design and scale-up of a closed ferrochrome SAF, 55 to 60 MW"),
            ("Drawing", "Furnace model: open cut, top, side and bottom views"),
            ("Units", "metres (m)"),
            ("Scale", "not to scale; views drawn proportionally"),
            ("DATA values", "shell inner dia 13.70, hearth 10.88, electrode 1.55, PCD 4.19"),
            ("DERIVED", "lining thickness 1.41 = (13.70 - 10.88)/2"),
            ("* PICTURE / ASSUMED", "all other dimensions: estimated from the SolidWorks\nscreenshot or assumed; replace and re-run run_all.py"),
            ("Section A-A", "plane y = 0, through the axis and electrode 1 (0 deg)"),
            ("Electrodes", "E1, E2, E3 at 0, 120, 240 deg; taps T1, T2 at -145, -35 deg")]
    y = 0.95
    tb.text(0.0, 1.0, "TITLE BLOCK", fontsize=10, fontweight="bold", va="top")
    for k, v in rows:
        tb.text(0.0, y - 0.04, k, fontsize=7, fontweight="bold", va="top"); tb.text(0.36, y - 0.04, v, fontsize=7, va="top"); y -= 0.085 if "\n" not in v else 0.12
    tb.add_patch(Rectangle((-0.02, -0.02), 1.04, 1.06, fc="none", ec="k", lw=1.0, transform=tb.transAxes, clip_on=False))
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(IMG, f"furnace_drawing_sheet.{ext}"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    single(section, "view_section_open_cut", (9.0, 11.5))
    single(top, "view_top", (9.0, 8.0))
    single(side, "view_side", (9.5, 10.5))
    single(bottom, "view_bottom", (9.0, 8.0))
    sheet()
    print("drawings done")
