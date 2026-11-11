# 03 – Reference Furnace Specification (RFS): the existing 55 MW furnace

**Work package:** WP1 – Existing furnace assessment (lead: M1; prepared by the Project Leader as a starting draft)
**Revision:** Rev A – DRAFT for freezing at **Gate G1**
**Controlling document:** `docs/00_SAF_Uprating_Design_Framework.md` §8.1
**Verification:** every derived value is reproduced by `calcs/01_reference_furnace.py`. Inputs are in `calcs/parameters.py` and the output is `results/01_rfs.csv` (47 items).

> **What this document is:** the scenario is hypothetical and no plant data exists (S-10). This RFS is a **complete, self-consistent, referenced description of a representative existing 55 MW closed ferrochrome SAF**, assembled from the brief [S], published furnace data [L], documented assumptions [A] and calculation [C]. Once frozen at G1 it **is** "the existing furnace" for all work packages. It must never be described as real plant data. Literature marked AB was taken from abstracts or search excerpts. The full texts could not be retrieved from this session and must be checked before the final report.

---

## 1. How the RFS was built

1. **Fix what the brief specifies:** 55 MW, 65 MVA total, closed SAF, three phases, an existing furnace (S-01 to S-10).
2. **Anchor on published South African ferrochrome furnaces of the same size:** a 63 MVA furnace with 1.55 m Söderberg electrodes and a 13.7 m shell [R-11], and a 48 MW / 110 kA furnace with 1.55 m electrodes [R-13].
3. **Derive the electrical operating point** from the Westly similarity calibrated on the analogue (C₃ = 8.33, A-18), taking the full 65 MVA at 55 MW (A-14).
4. **Derive the geometry** from published ratios of two independent ferrochrome furnaces [R-16, R-17].
5. **Cross-check** the results against each other and against independent data (Section 6). A value is accepted only if the checks agree.

---

## 2. General description

| Item | Specification | Tag |
|---|---|---|
| Furnace type | Closed (sealed roof), circular, three-phase AC submerged arc furnace | [S] |
| Product | High-carbon ferrochrome (charge chrome) | [A] A-01 |
| Feed | Pelletised (and lumpy) South African chromite with preheating; coke/anthracite reductant; quartzite flux | [A] A-04 (default Q4) |
| Electrodes | 3 Söderberg (self-baking) electrodes in an equilateral triangle | [A] A-02 |
| Off-gas | CO-rich gas, collected, cleaned (wet scrubbing) and re-used or flared | [A] |
| Operating basis | Continuous smelting, tapped intermittently | [A] |
| Grid | 50 Hz | [A] A-15 |

---

## 3. Electrical specification

### 3.1 Transformer installation

| Item | Value | Tag / basis |
|---|---|---|
| Total rating | 65 MVA | [S] S-07 |
| Arrangement | 3 × 21.67 MVA single-phase units, delta closed at the electrodes | [A] docs/02 §6 |
| HV supply voltage | 132 kV (sensitivity case 88 kV) | [A] A-21 – no data; typical SA furnace supply levels |
| Primary line current at 65 MVA | *I*₁ = 65×10⁶ / (√3 × 132×10³) = **284 A** (426 A at 88 kV) | [C] |
| Existing secondary tap range | **260–340 V** | [A] A-23 – **low confidence**; it governs the transformer's classification (Section 7) |
| Secondary winding current | *I*_w = *I* / √3 = 120.45 / 1.732 = **69.5 kA** | [C] |

### 3.2 Operating point at 55 MW (Scenario A)

| Quantity | Equation and substitution | Value | Tag |
|---|---|---|---|
| Active power | brief | **55.0 MW** | [S] |
| Phase power | 55 / 3 | **18.33 MW** | [C] |
| Apparent power | at full rating (A-14) | **65.0 MVA** | [A] |
| Power factor | 55 / 65 | **0.846** | [C] |
| Reactive power | √(65² − 55²) | **34.6 Mvar** | [C] |
| Electrode current | 8.33 × 55^(2/3) | **120.5 kA** | [C] A-18 |
| Secondary voltage (line) | √3 × 65×10⁶ / (3 × 120.45×10³) | **312 V** | [C] |
| Operating resistance per phase | 55×10⁶ / (3 × (120.45×10³)²) | **1.264 mΩ** | [C] |
| Total reactance per phase | √(1.494² − 1.264²) | **0.796 mΩ** | [C] |
| of which short network + electrode columns | 0.70 × 0.796 | **0.557 mΩ** | [C] R-14 share (AB) |
| of which transformer + remainder | 0.30 × 0.796 | **0.239 mΩ** | [C] |
| Reactance per unit (base 65 MVA, 312 V; *Z*_base = 312²/65×10⁶ = 1.498 mΩ) | 0.796 / 1.498 | **0.53 pu** | [C] |
| Implied transformer short-circuit reactance | 0.239 / 1.498 | **≈ 0.16 pu** | [C] **flag for WP3** |
| R/X | 1.264 / 0.796 | **1.59** | [C] |

**Significance:** a reactance of about 0.5 pu on the furnace base is why large SAFs are reactance-limited. Only 85 % of the transformer's MVA becomes active power. The implied transformer share (≈ 16 %) depends on the 70/30 split from R-14 (AB). WP3 must compare it with published furnace-transformer impedances before G1. If the real transformer share is lower, more of the reactance sits in the short network, and the 20 % reduction target (A-17) becomes easier to reach.

---

## 4. Geometry

| Item | Equation | Value | Tag |
|---|---|---|---|
| Electrode diameter *D* | – | **1.55 m** | [A] A-16 (R-11, R-13) |
| Electrode cross-section | π*D*²/4 | **1.887 m²** | [C] |
| Electrode current density | 120 450 A / 18 869 cm² | **6.38 A/cm²** | [C] |
| Pitch circle diameter (PCD) | 2.70 × 1.55 | **4.19 m** | [A] A-19: PCD/D = 2.70, mid-point of 2.44 [R-16] and 3.0 [R-17] |
| Electrode centre-to-centre spacing | PCD × √3/2 = 4.185 × 0.866 | **3.62 m** | [C] |
| Clear gap between electrodes | 3.624 − 1.55 | **2.07 m** | [C] |
| Hearth diameter (inside the lining) | 2.60 × 4.185 | **10.88 m** | [A] A-20: hearth/PCD = 2.60, mid-point of 2.55 [R-16] and 2.67 [R-17] |
| Electrode surface to sidewall | 10.881/2 − 4.185/2 − 1.55/2 | **2.57 m** | [C] |
| Shell inner diameter | – | **13.7 m** | [L] R-11 (63 MVA SA ferrochrome furnace) |
| Implied sidewall lining thickness | (13.7 − 10.88)/2 | **1.41 m** | [C] plausibility check (Section 6) |
| Hearth area | π × 10.88²/4 | **93.0 m²** | [C] |
| Hearth power density | 55 / 93.0 → 60 / 93.0 | **0.59 → 0.65 MW/m²** (+9.1 %) | [C] |
| Hearth depth, roof height, tap-hole positions | – | **Open (WP1/WP5)** | [M] |

**Significance for "optimised electrode geometry":** the baseline PCD/D (2.70) sits in the middle of the published range of 2.44–3.0. That leaves room to **increase the PCD** (to raise the operating resistance R) while staying inside proven practice. At PCD/D = 3.0 the PCD would be 4.65 m and the electrode-to-wall distance would fall to about 2.3 m. WP4 must check this against the existing roof penetrations (EQ-05) and the sidewall heat load (WP5).

---

## 5. Process specification

### 5.1 Feed: LG6 chromite concentrate [R-18, AB]

| Cr₂O₃ | FeO | Al₂O₃ | MgO | SiO₂ | Sum | Cr/Fe (calc) | Cr/Fe (reported) |
|---|---|---|---|---|---|---|---|
| 44.2 % | 24.1 % | 13.8 % | 11.5 % | 2.5 % | 96.1 % | **1.61** | 1.62 |

Cr = 44.2 × (2 × 52.00/151.99) = 30.24 %; Fe = 24.1 × (55.85/71.84) = 18.73 %; Cr/Fe = 1.61. This agrees with the reported value, confirming the analysis was transcribed correctly. The 3.9 % remainder (CaO, TiO₂, V₂O₅, loss on ignition, etc.) is to be defined in WP7.

### 5.2 Product, slag and production

| Item | Value | Tag |
|---|---|---|
| Alloy (charge chrome) | Cr ≈ 50–55 %, C ≈ 6–8 %, Si ≈ 2–6 % (typical) | [A] A-01 – reference **still to be found** (R-10, WP7) |
| Slag (typical SA ferrochrome) | SiO₂ 30 %, Al₂O₃ 26 %, MgO 23 %, CaO 2 %; Cr₂O₃ 4.5–13 % | [L] R-19, R-20 (AB) |
| Slag basicity (CaO + MgO)/SiO₂ | (2 + 23)/30 = **0.83** | [C] |
| Slag MgO/Al₂O₃ | 23/26 = **0.88** | [C] |
| Specific electrical energy (SEC) | **3.25 MWh/t** alloy | [A] A-04 (mid of 3.0–3.5) |
| Utilisation | **0.92** | [A] A-09 (mid of 0.90–0.95) |
| Alloy production at 55 MW | 55 × 24 × 0.92 / 3.25 = **374 t/d** (≈ 136 kt/a) | [C] |
| Indicative production at 60 MW (same SEC) | **408 t/d** (+9.1 %) | [C] – WP7 to confirm |

### 5.3 Auxiliary plant (cooling water, off-gas cleaning, feed, tapping)

| Item | Value | Tag |
|---|---|---|
| Design capacity relative to the 55 MW duty | **1.10 ×** (10 % design margin) | [A] A-22 – **low confidence; critical** |
| Utilisation at 60 MW, if load scales with power | 1.0909 / 1.10 = **0.99 (99 %)** | [C] |

**Significance (an important early finding):** if the auxiliaries were designed with the usual 10 % margin over the 55 MW duty, the +9.1 % uprate **uses almost all of it**. Utilisation reaches 99 %, which fails acceptance criterion DC-06 (≤ 90 % of design). The cooling-water, off-gas and feed systems are therefore **likely Upgrade items**, not Retain items, unless WP5/WP7 show their loads grow less than in proportion to power. This is exactly the trap the framework's "do not assume everything can stay" principle is meant to catch.

---

## 6. Internal consistency checks

| Check | Result | Verdict |
|---|---|---|
| Winding current from the electrode current (*I*/√3) vs from the unit rating (21.67 MVA / 312 V) | 69.54 kA = 69.54 kA | ✔ The electrical model is self-consistent |
| Feed Cr/Fe calculated vs reported | 1.614 vs 1.62 | ✔ The analysis was transcribed correctly |
| Geometry ratios from two sources [R-16, R-17] combined with an independent shell diameter [R-11] | Implied lining 1.41 m | ✔ Plausible order of magnitude for a ferrochrome sidewall plus freeze lining (WP5 to confirm) |
| Current density vs a published furnace with the same electrode diameter | 6.38 vs 5.83 A/cm² [R-13] | ✔ Same order; the baseline is 9 % higher because its power is higher |
| Westly C₃ inside the reported ferrochrome range | 8.33 within 6–11 [R-12] | ✔ |
| Power factor vs typical | 0.846 vs ≈ 0.85 [R-02, R-14] | ✔ |

---

## 7. Consequences for the equipment classification (feeds `registers/equipment_classification.csv`)

| Equipment | Finding from the RFS | Class change |
|---|---|---|
| EQ-01 Transformers | Case B20 needs 328 V, inside the assumed 260–340 V range. With the ±5 % control margin (DC-03), however, the top of the band is 328 × 1.05 = **344 V > 340 V**, so it is marginal. Case B0 needs 367 V, which is outside the range. | V → **Optimise (marginal) for B20; Upgrade (tap changer/windings) for B0**. Depends on A-23. |
| EQ-10/11/12 Auxiliaries | 99 % utilisation at 60 MW with a 10 % design margin | V → **likely Upgrade** (depends on A-22) |
| EQ-05 Electrode PCD | Baseline PCD/D 2.70; proven range up to 3.0 | Confirms **Optimise** is geometrically possible; the roof penetrations still need checking |
| EQ-08 Hearth | Power density 0.59 → 0.65 MW/m² | Stays V until WP5 |

---

## 8. New assumptions (added to `registers/assumptions_register.csv`)

| ID | Assumption | Value | Basis | Conf. |
|---|---|---|---|---|
| A-19 | Baseline PCD/D | 2.70 | Mid-point of 2.44 [R-16] and 3.0 [R-17] | M |
| A-20 | Hearth/PCD | 2.60 | Mid-point of 2.55 [R-16] and 2.67 [R-17] | M |
| A-21 | HV supply voltage | 132 kV (88 kV sensitivity) | Typical SA furnace supply levels; no data | L |
| A-22 | Auxiliary design margin over the 55 MW duty | 10 % | Engineering judgement; no data | **L – critical** |
| A-23 | Existing secondary tap range | 260–340 V | Engineering judgement around 312 V; no data | **L – critical** |

A-22 and A-23 are **critical**: they decide whether the transformer and the auxiliaries are Retain, Optimise or Upgrade. They should be (i) reviewed by the team at G1 and (ii) varied in the WP9 sensitivity analysis.

## 9. Open items to close before freezing at G1

1. Hearth depth, bath and slag heights, roof height, and tap-hole arrangement (WP1/WP5).
2. Alloy specification reference (R-10) and the full feed recipe: pellet/lump split, reductant analysis, flux (WP7).
3. Published furnace-transformer impedance to test the implied ≈ 16 % (WP3).
4. Team agreement on A-22 and A-23.
5. Full-text verification of R-11, R-13, R-16 to R-20.
