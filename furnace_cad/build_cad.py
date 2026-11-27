"""build_cad.py: parametric 3D model of the furnace (CadQuery), STEP/STL export, revolve-cut profile DXF."""
import json, math, os
import cadquery as cq
import ezdxf
from params import P, TAG

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cad_files")
os.makedirs(OUT, exist_ok=True)
V = cq.Vector


def cyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(r).extrude(z1 - z0)


def tube(ro, ri, z0, z1, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(ro).circle(ri).extrude(z1 - z0)


def oblique(ro, ri, p0, p1):
    """Hollow cylinder between two points."""
    v = V(*p1) - V(*p0)
    h = v.Length
    outer = cq.Solid.makeCylinder(ro, h, V(*p0), v.normalized())
    inner = cq.Solid.makeCylinder(ri, h, V(*p0), v.normalized())
    return cq.Workplane("XY").add(outer.cut(inner))


def build():
    R_so, R_si, R_h = P["R_shell_o"], P["R_shell_i"], P["R_hearth"]
    zb, z0, zr, zrt = P["z_bottom"], 0.0, P["z_roof_u"], P["z_roof_t"]
    parts = {}

    # steel shell: wall + bottom plate
    shell = cyl(R_so, zb, zrt).cut(cyl(R_si, zb + P["t_steel"], zrt + 1))
    parts["steel_shell"] = shell

    # lining block, then the REVOLVE CUT of the hearth cavity profile
    lining_block = cyl(R_si, zb + P["t_steel"], zr)
    cavity_profile = (cq.Workplane("XZ").moveTo(0, z0).lineTo(R_h, z0).lineTo(R_h, zr).lineTo(0, zr).close())
    cavity = cavity_profile.revolve(360, (0, 0, 0), (0, 1, 0))
    lining = lining_block.cut(cavity)
    parts["lining"] = lining

    # roof slab with three electrode holes
    roof = cyl(R_so, zr, zrt)
    holes = None
    for a in P["e_angles"]:
        x, y = P["R_e_axis"] * math.cos(math.radians(a)), P["R_e_axis"] * math.sin(math.radians(a))
        h = cyl(P["D_e"] / 2, zr - 0.1, zrt + 0.1, x, y)
        holes = h if holes is None else holes.union(h)
    parts["roof"] = roof.cut(holes)

    # process zones inside the cavity (for the open cut and for COMSOL-type domain definitions)
    def zone(z0_, z1_):
        z = cyl(R_h, z0_, z1_)
        for a in P["e_angles"]:
            x, y = P["R_e_axis"] * math.cos(math.radians(a)), P["R_e_axis"] * math.sin(math.radians(a))
            z = z.cut(cyl(P["D_e"] / 2, z0_ - 0.1, z1_ + 0.1, x, y))
        return z
    parts["metal_pad"] = zone(0.0, P["z_metal"])
    parts["slag_layer"] = zone(P["z_metal"], P["z_bath"])
    parts["burden"] = zone(P["z_bath"], P["z_stock"])

    # electrode support plate
    parts["support_plate"] = cyl(P["D_plate"] / 2, P["z_plate_b"], P["z_plate_t"])

    ro, ri = P["D_e"] / 2, P["D_e"] / 2 - P["wall_e"]
    stubs = tubes = conns = None
    for k, a in enumerate(P["e_angles"]):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        xs, ys = P["R_e_axis"] * c, P["R_e_axis"] * s
        xt, yt = P["R_tube_axis"] * c, P["R_tube_axis"] * s
        parts[f"electrode_column_{k + 1}"] = cyl(ro, P["z_tip"], zrt, xs, ys)
        # stub from the roof top to the plate underside (solid electrode column continues inside the furnace)
        parts[f"electrode_stub_{k + 1}"] = tube(ro, ri, zrt, P["z_plate_b"], xs, ys)
        # oblique 45 degree connector from the stub top to the base of the vertical tube
        p0 = (xs, ys, P["z_plate_t"] - 0.0)
        p1 = (xt, yt, P["z_plate_t"] + P["offset"])
        parts[f"electrode_connector_{k + 1}"] = oblique(ro, ri, p0, p1)
        parts[f"electrode_tube_{k + 1}"] = tube(ro, ri, P["z_plate_t"] + P["offset"], P["z_tube_top"], xt, yt)
    # tap pipes
    for k, a in enumerate(P["tap_angles"]):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        p0 = (R_si * c * 0.98, R_si * s * 0.98, P["z_tap"])
        p1 = ((R_so + P["L_tap"]) * c, (R_so + P["L_tap"]) * s, P["z_tap"])
        parts[f"tap_pipe_{k + 1}"] = oblique(P["D_tap_o"] / 2, P["D_tap_i"] / 2, p0, p1)
    return parts


def volume(wp):
    return sum(s.Volume() for s in wp.vals())


def export(parts):
    # assembly STEP with named parts
    asm = cq.Assembly(name="ferrochrome_SAF")
    colours = {"steel_shell": (0.45, 0.47, 0.55), "lining": (0.80, 0.62, 0.45), "roof": (0.55, 0.55, 0.6),
               "support_plate": (0.55, 0.57, 0.65), "electrode": (0.35, 0.37, 0.45), "tap": (0.4, 0.42, 0.5),
               "metal_pad": (0.85, 0.75, 0.3), "slag_layer": (0.85, 0.35, 0.2), "burden": (0.45, 0.33, 0.25)}
    for n, w in parts.items():
        key = "electrode" if n.startswith("electrode") else ("tap" if n.startswith("tap") else n)
        if key not in colours:
            key = "steel_shell"
        asm.add(w, name=n, color=cq.Color(*colours[key]))
    asm.save(os.path.join(OUT, "furnace_assembly.step"))
    # single fused solid (as drawn in the picture) and a quarter cut-away for viewing
    fused = None
    for n, w in parts.items():
        fused = w if fused is None else fused.union(w)
    cq.exporters.export(fused, os.path.join(OUT, "furnace_solid.step"))
    cq.exporters.export(fused, os.path.join(OUT, "furnace_solid.stl"), tolerance=0.02, angularTolerance=0.1)
    # open cut: remove the quarter x>0, y<0 (a 90 degree wedge) so that the lining, cavity and electrodes are visible
    cutter = cq.Workplane("XY").box(30, 30, 40, centered=(False, False, True)).translate((0, -30, 0))
    cut = fused.cut(cutter)
    cq.exporters.export(cut, os.path.join(OUT, "furnace_open_cut_quarter.step"))
    cq.exporters.export(cut, os.path.join(OUT, "furnace_open_cut_quarter.stl"), tolerance=0.02, angularTolerance=0.1)
    return fused, cut


def revolve_profile_dxf():
    """Half-section profile (r, z) of the furnace body: the sketch for the SolidWorks revolve and revolve cut."""
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.M
    msp = doc.modelspace()
    for name, color in (("OUTLINE_BODY", 7), ("REVOLVE_CUT_CAVITY", 1), ("AXIS", 5)):
        doc.layers.add(name, color=color)
    R_so, R_si, R_h = P["R_shell_o"], P["R_shell_i"], P["R_hearth"]
    zb, zr, zrt = P["z_bottom"], P["z_roof_u"], P["z_roof_t"]
    msp.add_lwpolyline([(0, zb), (R_so, zb), (R_so, zrt), (0, zrt)], close=True, dxfattribs={"layer": "OUTLINE_BODY"})
    msp.add_lwpolyline([(0, 0), (R_h, 0), (R_h, zr), (0, zr)], close=True, dxfattribs={"layer": "REVOLVE_CUT_CAVITY"})
    msp.add_line((0, zb - 1), (0, P["z_plate_t"] + 1), dxfattribs={"layer": "AXIS", "linetype": "CENTER"})
    doc.saveas(os.path.join(OUT, "revolve_cut_profile_half_section.dxf"))


if __name__ == "__main__":
    parts = build()
    fused, cut = export(parts)
    revolve_profile_dxf()
    # validation: volume of the lining against the analytic revolve volume
    R_si, R_h, zb, zr = P["R_shell_i"], P["R_hearth"], P["z_bottom"] + P["t_steel"], P["z_roof_u"]
    v_lin = math.pi * R_si ** 2 * (zr - zb) - math.pi * R_h ** 2 * zr
    info = {"lining_volume_cad_m3": volume(parts["lining"]), "lining_volume_analytic_m3": v_lin,
            "n_parts": len(parts), "fused_volume_m3": volume(fused), "bbox": [fused.val().BoundingBox().xmin, fused.val().BoundingBox().xmax,
                                                                              fused.val().BoundingBox().ymin, fused.val().BoundingBox().ymax,
                                                                              fused.val().BoundingBox().zmin, fused.val().BoundingBox().zmax]}
    print(json.dumps(info, indent=1))
    json.dump({"parameters": {k: v for k, v in P.items()}, "tags": {k: list(v) for k, v in TAG.items()}, "checks": info},
              open(os.path.join(OUT, "furnace_parameters.json"), "w"), indent=1)
