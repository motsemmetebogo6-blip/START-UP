"""
params.py: parametric dimensions of the furnace model (metres).
Source tags:  DATA = supervisor plant data or the design basis (project report);
              DERIVED = calculated from DATA;
              PICTURE = estimated from the proportions of the SolidWorks screenshot, anchored on the shell diameter;
              ASSUMED = engineering assumption, no data.
Replace any PICTURE or ASSUMED value with the SolidWorks dimension and re-run run_all.py.
"""
import math

P = {}
TAG = {}


def d(name, value, tag, note=""):
    P[name] = value
    TAG[name] = (tag, note)


d("D_shell_in", 13.70, "DATA", "Shell inner diameter, Chapter 3 (existing furnace configuration)")
d("D_hearth", 10.88, "DATA", "Hearth diameter inside the lining, Chapter 3")
d("D_e", 1.55, "DATA", "Soderberg electrode diameter, Chapter 4 (A-16)")
d("PCD", 4.19, "DATA", "Electrode pitch circle diameter, 2.70 x 1.55 (A-19)")
d("t_lining", round((P["D_shell_in"] - P["D_hearth"]) / 2, 3), "DERIVED", "(13.70 - 10.88)/2: lining and ramming between shell and hearth")
d("t_steel", 0.03, "ASSUMED", "Steel shell plate thickness")
d("t_floor", P["t_lining"], "ASSUMED", "Floor lining taken equal to the wall lining")
d("H_cavity", 7.50, "PICTURE", "Inside height from hearth floor to roof underside (overall height 9.5 m from the picture)")
d("t_roof", 0.60, "ASSUMED", "Roof slab thickness")
d("z_metal", 0.50, "ASSUMED", "Top of the metal pad above the hearth floor")
d("z_bath", 2.20, "ASSUMED", "Top of the slag layer above the hearth floor")
d("z_stock", 6.00, "ASSUMED", "Burden stock line above the hearth floor")
d("z_tip", 1.50, "ASSUMED", "Electrode tip height above the hearth floor (immersed in the slag layer)")
d("D_plate", 9.60, "PICTURE", "Electrode support plate diameter, 0.70 of the shell diameter")
d("t_plate", 0.50, "PICTURE", "Electrode support plate thickness")
d("h_stub", 1.00, "PICTURE", "Stub height between roof top and support plate")
d("offset", 1.20, "PICTURE", "Horizontal offset of each vertical electrode tube from its stub (outward)")
d("L_tube", 8.00, "PICTURE", "Vertical electrode tube length above the support plate")
d("wall_e", 0.20, "PICTURE", "Electrode tube wall thickness (hollow casing in the picture)")
d("D_tap_o", 1.20, "PICTURE", "Tap pipe outer diameter")
d("D_tap_i", 0.80, "PICTURE", "Tap pipe bore")
d("L_tap", 2.00, "PICTURE", "Tap pipe projection beyond the shell")
d("z_tap", 0.30, "PICTURE", "Tap pipe axis height above the hearth floor")
d("tap_angles", (-145.0, -35.0), "PICTURE", "Tap pipe azimuths in plan (x to the right, y to the back)")
d("e_angles", (0.0, 120.0, 240.0), "PICTURE", "Electrode azimuths in plan")

# derived levels (z = 0 at the hearth floor)
P["R_shell_o"] = P["D_shell_in"] / 2 + P["t_steel"]
P["R_shell_i"] = P["D_shell_in"] / 2
P["R_hearth"] = P["D_hearth"] / 2
P["z_bottom"] = -(P["t_floor"] + P["t_steel"])
P["z_roof_u"] = P["H_cavity"]
P["z_roof_t"] = P["H_cavity"] + P["t_roof"]
P["z_plate_b"] = P["z_roof_t"] + P["h_stub"]
P["z_plate_t"] = P["z_plate_b"] + P["t_plate"]
P["z_tube_top"] = P["z_plate_t"] + P["L_tube"]
P["H_total"] = P["z_tube_top"] - P["z_bottom"]
P["H_body"] = P["z_roof_t"] - P["z_bottom"]
P["R_e_axis"] = P["PCD"] / 2
P["R_tube_axis"] = P["PCD"] / 2 + P["offset"]
