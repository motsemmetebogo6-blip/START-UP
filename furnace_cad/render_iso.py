"""render_iso.py: shaded isometric views of the CAD solid (full and open-cut) with matplotlib."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cadquery as cq
from build_cad import build, OUT as CADOUT
from params import P

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images"); os.makedirs(IMG, exist_ok=True)


def mesh(wp, tol=0.03):
    v, t = wp.val().tessellate(tol, 0.15)
    V = np.array([[p.x, p.y, p.z] for p in v]); T = np.array(t)
    return V[T]


def shade(tri, light=np.array([-0.4, -0.7, 0.6]), base=np.array([0.52, 0.55, 0.68])):
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
    l = light / np.linalg.norm(light)
    k = 0.45 + 0.55 * np.abs(n @ l)
    return np.clip(base[None, :] * k[:, None], 0, 1)


def draw(tri, name, elev=22, azim=-62, title=None, section=False):
    fig = plt.figure(figsize=(8, 9))
    ax = fig.add_subplot(111, projection="3d")
    pc = Poly3DCollection(tri, facecolors=shade(tri), edgecolors="none", linewidths=0)
    ax.add_collection3d(pc)
    lim = 8.0
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-1.5, 2 * lim + 1.5 - 1.5)
    ax.set_box_aspect((2 * lim, 2 * lim, 2 * lim + 1.5))
    ax.view_init(elev, azim); ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=11)
    fig.savefig(os.path.join(IMG, name), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


import numba
from PIL import Image, ImageDraw, ImageFont

COL = {"steel_shell": (0.45, 0.48, 0.58), "lining": (0.82, 0.64, 0.46), "roof": (0.66, 0.67, 0.72), "support_plate": (0.55, 0.58, 0.70),
       "metal_pad": (0.90, 0.78, 0.30), "slag_layer": (0.88, 0.38, 0.22), "burden": (0.50, 0.38, 0.30), "electrode_column": (0.22, 0.23, 0.27),
       "electrode": (0.52, 0.55, 0.70), "tap": (0.45, 0.48, 0.60)}


def colour_of(name):
    if name.startswith("electrode_column"):
        return COL["electrode_column"]
    if name.startswith("electrode"):
        return COL["electrode"]
    if name.startswith("tap"):
        return COL["tap"]
    return COL[name]


@numba.njit(cache=True)
def raster(px, py, pz, cols, W, H):
    img = np.ones((H, W, 3))
    zb = np.full((H, W), -1e18)
    for i in range(px.shape[0]):
        x0, x1, x2 = px[i, 0], px[i, 1], px[i, 2]
        y0, y1, y2 = py[i, 0], py[i, 1], py[i, 2]
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        xmin = max(int(np.floor(min(x0, x1, x2))), 0); xmax = min(int(np.ceil(max(x0, x1, x2))), W - 1)
        ymin = max(int(np.floor(min(y0, y1, y2))), 0); ymax = min(int(np.ceil(max(y0, y1, y2))), H - 1)
        for yy in range(ymin, ymax + 1):
            for xx in range(xmin, xmax + 1):
                a = ((y1 - y2) * (xx + 0.5 - x2) + (x2 - x1) * (yy + 0.5 - y2)) / den
                b = ((y2 - y0) * (xx + 0.5 - x2) + (x0 - x2) * (yy + 0.5 - y2)) / den
                c = 1 - a - b
                if a >= 0 and b >= 0 and c >= 0:
                    z = a * pz[i, 0] + b * pz[i, 1] + c * pz[i, 2]
                    if z > zb[yy, xx]:
                        zb[yy, xx] = z
                        img[yy, xx, 0] = cols[i, 0]; img[yy, xx, 1] = cols[i, 1]; img[yy, xx, 2] = cols[i, 2]
    return img


def draw_parts(parts, name, cutter=None, elev=24, azim=-40, title=None, W=1500, H=1700):
    tris, cols = [], []
    for n, w in parts.items():
        wp = w if cutter is None else w.cut(cutter)
        if not wp.vals():
            continue
        try:
            tri = mesh(wp, 0.02)
        except Exception:
            continue
        tris.append(tri); cols.append(shade(tri, light=np.array([-0.5, -0.6, 0.65]), base=np.array(colour_of(n))))
    tri = np.concatenate(tris); col = np.concatenate(cols)
    az, el = np.radians(azim), np.radians(elev)
    # view rotation: rotate about z by -azim, then tilt by elev; screen x right, screen y up, depth toward viewer
    Rz = np.array([[np.cos(az), -np.sin(az), 0], [np.sin(az), np.cos(az), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(el), -np.sin(el)], [0, np.sin(el), np.cos(el)]])
    pts = tri.reshape(-1, 3) @ Rz.T @ Rx.T
    # after rotations: x right, y = depth (away), z up on screen
    sx, sd, sz = pts[:, 0], pts[:, 1], pts[:, 2]
    scale = min(W / (sx.max() - sx.min()), H / (sz.max() - sz.min())) * 0.92
    X = (sx - (sx.max() + sx.min()) / 2) * scale + W / 2
    Y = H / 2 - (sz - (sz.max() + sz.min()) / 2) * scale
    D = -sd
    px, py, pz = X.reshape(-1, 3), Y.reshape(-1, 3), D.reshape(-1, 3)
    img = raster(px, py, pz, col, W, H)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    if title:
        d = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
        except Exception:
            f = None
        d.text((40, 30), title, fill=(0, 0, 0), font=f)
    im.save(os.path.join(IMG, name), dpi=(200, 200))


if __name__ == "__main__":
    parts = build()
    draw_parts(parts, "iso_full.png", azim=-55, elev=22, title="Furnace model (isometric)")
    cutter = cq.Workplane("XY").box(30, 30, 40, centered=(False, False, True)).translate((0, -30, 0))
    draw_parts(parts, "iso_open_cut_quarter.png", cutter=cutter, azim=-55, elev=28, title="Open cut: quarter removed (x > 0, y < 0)")
