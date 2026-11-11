# 01 – Engineering Design Basis (Rev C, for Project Leader review)

**Project:** Design and Scale-Up of a Closed Ferrochrome Submerged Arc Furnace (SAF) from 55 MW to 60 MW using 65 MVA Transformers and Optimised Electrode Geometry
**Discipline:** BEngTech Metallurgical Engineering – design assignment
**Status:** DRAFT Rev C – HOLD POINT 1 (partially cleared: Q1, Q1b, Q2, Q5, Q6 answered). No detailed calculations proceed until the Project Leader has reviewed this document and answered the decision questions in Section 10.
**Date:** 2026-11-11

**Revision log:** Rev A – first issue. Rev B – Project Leader confirmed Q1 (65 MVA is the **total** installed transformer rating) and Q2 (**uprate of an existing furnace**). A-03 and A-13 are now specified items S-07 and S-08. Q3–Q8 remain open. Rev C – Project Leader confirmed the 55 MW furnace **exists** (Q1b) and that the scenario is a **lecturer-defined hypothetical with no real plant data** (Q5/Q6). All baseline values are therefore reference-furnace values derived from literature and first principles. Q3, Q4, Q7 and Q8 remain open.

> **Data integrity rule used throughout:** Every number is tagged as
> **[S]** = specified in the project brief, **[A]** = assumption (justified, in the register in Section 5),
> **[L]** = typical literature value (referenced), **[C]** = calculated in this project, **[M]** = missing, required from the Project Leader or plant.
> No plant operating data has been invented. Where no source exists, the item is shown as missing, not filled in.

---

## 0. Review of existing project files

| Item | Finding |
|---|---|
| Repository | `motsemmetebogo6-blip/START-UP`, branch `claude/ferrochrome-furnace-scaleup-i1i0si` |
| Existing files | `START` (1 byte, empty, the only file from the initial commit) |
| Existing brief / instructions / data | **None in the repository.** The brief is taken from the Project Leader's message of 2026-11-11. |
| Action | `START` left untouched. New work is added under `docs/`, `calcs/` and `references/` only. |

**Request:** if a written brief, rubric, lecturer's handout or plant datasheet exists, please add it to `brief/`. Several items in Section 4 may already be answered there.

---

## 1. Interpretation of the project brief

### 1.1 Breaking down the title

| Element of title | Engineering interpretation | Consequence for design |
|---|---|---|
| *Closed* furnace | Sealed roof; CO-rich off-gas (typically ~75–90 % CO by volume, to be confirmed by mass balance) is collected, cleaned and usually re-used (for example to preheat or sinter the feed). Usually paired with pelletised and/or preheated feed, because fines cause roof eruptions and blowouts in closed furnaces. | Off-gas volume, gas-cleaning capacity and the roof/seal design all scale with power. Feed must be permeable. |
| *Ferrochrome* | Assumed: **high-carbon ferrochrome / charge chrome** made from chromite ore. Product type is not specified. | Drives the slag system (SiO₂–MgO–Al₂O₃), the specific energy and the target Cr recovery. |
| *Submerged arc furnace* | AC, three-phase, three electrodes in a triangle. Most of the heat is released resistively in the slag/coke bed, with a small arc component. | Bath (load) resistance is the key electrical design variable. |
| *Scale-up 55 MW → 60 MW* | +9.09 % active power (60/55 = 1.0909). **Confirmed (Q2): uprate of an existing furnace.** | Fixes which dimensions are frozen (shell, hearth) and which can change (transformers, electrodes, PCD, voltage taps). |
| *65 MVA transformers* | **Confirmed (Q1): 65 MVA total installed** (e.g. 3 × ~21.7 MVA single-phase, or one three-phase unit; configuration still open under M-01). | Fixes the maximum apparent power and therefore the **minimum power factor**. See Section 7.3. |
| *Optimised electrode geometry* | Electrode diameter *D*, pitch circle diameter (PCD), electrode tip position/penetration and electrode–wall spacing. | These set current density, bath resistance (and therefore the power factor) and hearth power distribution. |

### 1.2 What the assignment must deliver (interpreted)

1. A defensible **55 MW baseline** furnace description.
2. A **60 MW operating case** that respects the 65 MVA transformer limit.
3. **Electrical design**: secondary voltage/current operating point, tap range, power factor, resistance and reactance, electrode current density, electrode diameter and PCD.
4. **Metallurgical design**: mass and energy balance, specific energy, production rate, slag chemistry, reductant requirement, off-gas, electrode paste consumption.
5. **Scale-up justification**: similarity criteria (Andreae/Kelly *k*, Westly *C₃*) checked against first-principles calculations.
6. Risks, constraints and recommendations.

### 1.3 Scope boundaries (proposed; confirm under Q3)

- **In scope:** furnace transformers (secondary side), high-current line, electrodes, bath and hearth, feed and products, off-gas quantity.
- **Out of scope unless instructed:** HV substation and grid compliance detail (harmonics and flicker only flagged), pelletising/sintering plant design, gas-cleaning plant detailed design, detailed refractory thermal FEA, costing (include it only if the rubric requires an economic evaluation).

---

## 2. Design philosophy and governing basis

| Basis item | Proposed basis |
|---|---|
| Units | SI. Electrical: MW, MVA, Mvar, kA, V, mΩ. Energy: MWh/t alloy. |
| Comparison rule | Between the 55 MW and 60 MW cases, **feed blend, reductant type, product grade and slag chemistry are held constant** unless a change is explicitly justified. The scale-up effect is then isolated. |
| Electrical model | Balanced three-phase equivalent star circuit per electrode: furnace load resistance *R* in series with the secondary-circuit reactance *X* (busbars, flexibles, electrode columns). Power, PF and current are found from *R* and *X*. Interaction between electrodes is acknowledged as a limitation (Mulholland, 2009). |
| Scale-up rules | (i) First-principles electrical circuit; (ii) Westly *C₃* similarity (I ∝ P^(2/3), V ∝ P^(1/3)); (iii) Andreae/Kelly *k* (bath resistance × electrode diameter); (iv) electrode current density limits; (v) hearth/shaft power density. Westly is used as a **cross-check only**, because its validity is disputed (ABM, 2007). |
| Thermochemistry | Mass and energy balance in Python, using standard thermochemical data (to be sourced, e.g. NIST-JANAF / published ΔH values) and a clearly stated reaction scheme. |
| Standards (applicability to be confirmed) | IEC 60076-1 (power transformers – general); IEEE C57.17 (arc furnace transformers); IEC 60909 (short-circuit currents); NRS 048-2 (South African voltage quality – flicker/unbalance, if SA grid); IEC 61000-3-6/-3-7 (harmonic and flicker emission limits). |
| Verification | Every hand calculation is reproduced in a Python script in `calcs/`, with inputs read from one parameter file so that a change propagates everywhere. |

---

## 3. Process description (assumed basis, confirm under Q4)

Chromite (lumpy ore plus pellets, possibly preheated) + carbonaceous reductant (coke/anthracite/char) + flux (quartzite, possibly lime/dolomite) → closed AC SAF with three Söderberg electrodes → tapped HC FeCr alloy + slag. CO-rich off-gas → wet scrubber/venturi → flare or re-use.

Simplified overall reactions (to be expanded in the balance):

- FeO·Cr₂O₃ + 4C → Fe + 2Cr + 4CO (and carbide formation: Cr₇C₃, (Cr,Fe)₇C₃)
- SiO₂ + 2C → Si(alloy) + 2CO (partial, sets alloy Si)
- MgO, Al₂O₃, most of the SiO₂ and CaO report to the slag. MgO/Al₂O₃ ratio and SiO₂ set liquidus and resistivity.

---

## 4. Parameter register: known vs missing

### 4.1 Specified in the brief [S]

| ID | Parameter | Value | Note |
|---|---|---|---|
| S-01 | Baseline furnace active power | 55 MW | Measurement point not defined (see Q5) |
| S-02 | Proposed furnace active power | 60 MW | Same |
| S-03 | Transformer rating | 65 MVA | Total (see S-07) |
| S-04 | Furnace type | Closed SAF | |
| S-05 | Product | Ferrochrome | Grade not defined (Q4) |
| S-06 | Design levers | Transformers + electrode geometry | |
| S-07 | Transformer rating basis | 65 MVA **total** installed | Confirmed by Project Leader (Q1), Rev B |
| S-08 | Project type | **Uprate of existing furnace**: shell, hearth and roof are fixed | Confirmed by Project Leader (Q2), Rev B |
| S-09 | Baseline status | 55 MW furnace **exists** (operating baseline) | Confirmed (Q1b), Rev C |
| S-10 | Data status | **Lecturer-defined hypothetical scenario; no real plant data supplied** | Confirmed (Q5/Q6), Rev C. Every non-[S] value must come from literature or calculation and be tagged. |

### 4.2 Missing parameters (needed for a rigorous design)

Priority: **H** = blocks the electrical/metallurgical design, **M** = needed for detailed calculations, **L** = refinement.

| ID | Missing parameter | Priority | If not supplied, proposed treatment |
|---|---|---|---|
| M-01 | Transformer configuration (1×3φ or 3×1φ), HV voltage, secondary voltage tap range, short-circuit impedance, overload capability | H | Assume 3 × 1φ units, on-load tap changer. Secondary tap range derived from the calculations and checked against published similar furnaces. |
| M-02 | Measurement point of the 55/60 MW (HV metering, transformer secondary, or electrode/bath) | H | Treat as an assumption with sensitivity analysis (A-11) |
| M-03 | Baseline electrical operating point: secondary voltage, electrode current, PF, operating resistance, secondary reactance | H | **Not invented.** Back-calculated from literature-typical PF and similarity rules, labelled [A]/[C] |
| M-04 | Existing electrode diameter, PCD, shell and hearth diameter, hearth depth | H | Derived from current-density and similarity rules, labelled [C] |
| M-05 | Feed chemistry (ore Cr₂O₃, FeO, SiO₂, MgO, Al₂O₃, CaO; Cr/Fe ratio), size/pellet fraction, preheat temperature | H | Use a **published** representative South African chromite (UG2/LG6 type) analysis with its reference |
| M-06 | Reductant proximate analysis (fixed C, VM, ash, moisture) | M | Published typical coke/anthracite analysis, referenced |
| M-07 | Product specification (Cr, C, Si, S, P) | M | Typical charge-chrome specification, referenced |
| M-08 | Slag target (basicity, MgO/Al₂O₃, Cr₂O₃ loss) | M | Literature range, referenced |
| M-09 | Specific energy consumption of the baseline (MWh/t) | H | Literature range 3.0–4.0 MWh/t depending on preheat, validated by own energy balance |
| M-10 | Furnace availability/utilisation, tapping frequency | M | Assumption (A-09) |
| M-11 | Cooling, refractory and off-gas plant limits (gas-cleaning capacity) | M | Flag as constraint checks; +9 % gas load to be verified |
| M-12 | Grid data: fault level at the point of common coupling, existing compensation (SVC/capacitors) | L | Out of scope unless required (Q3) |
| M-13 | Assessment rubric / required report format | H (for planning) | Request |

---

## 5. Assumptions register (Rev A)

Confidence: **H** = well supported by multiple sources; **M** = one credible source or engineering convention; **L** = weak, must be verified or tested by sensitivity analysis.

| ID | Assumption | Value / range | Justification and reference | Conf. | How it will be tested |
|---|---|---|---|---|---|
| A-01 | Product is HC FeCr / charge chrome from South African chromite | Cr ≈ 50–55 %, C ≈ 6–8 %, Si ≈ 2–6 % (typical, to be referenced) | Typical SA closed-furnace product. Ref. to be confirmed [R-10] | M | Q4 to Project Leader |
| A-02 | Electrodes are Söderberg (self-baking) | — | Standard for large SA closed FeCr furnaces [R-06] | H | Q4 |
| A-03 | ~~65 MVA = total installed rating~~ | — | **Closed: confirmed, now S-07** | — | — |
| A-04 | Specific electrical energy (furnace) | 3.0–3.5 MWh/t with pelletised/preheated feed; up to ~4 MWh/t with cold mixed feed | 3–3.5 MWh/t for the Outotec route [R-05]; lowest 3.31 MWh/t at 6 % SiO₂ in ore [R-07]; −70 kWh/t per +100 °C preheat [R-04] | M | Own energy balance (Phase 3) |
| A-05 | Baseline power factor at furnace | 0.80–0.85 | 0.85 cited as typical for an "average-sized" FeCr furnace; larger modern FeCr furnaces run lower [R-02] | M | Sensitivity analysis (see 7.3) |
| A-06 | Electrical efficiency of the secondary circuit (power in bath / transformer active power) | 0.94–0.98 | Engineering judgement. **No reference yet: flagged for research** | L | Literature search; sensitivity |
| A-07 | Maximum allowable Söderberg current density for D > 1.3 m | 4.5–5 A/cm² (5.5–6 A/cm² for 1.1–1.3 m) | Single patent source [R-08]. Vendor guideline, not peer reviewed | L | Seek a second source (e.g. Elkem/Infacon); cross-check against published furnace data |
| A-08 | Westly constant *C₃* is the same for the 55 and 60 MW cases (same process) | I ∝ P^(2/3) | Classical similarity [R-01]; disputed [R-03] | L–M | Cross-check only, never the sole basis |
| A-09 | Furnace utilisation | 90–95 % of calendar time at nominal power | Engineering judgement, to be referenced | L | Sensitivity on production rate |
| A-10 | PCD/D ratio | To be determined from literature (expected order 2.5–3.0) | **Not yet referenced: research item** | L | Phase 4 literature review |
| A-11 | 55/60 MW = active power **into the furnace** (transformer secondary / electrodes), not HV-metered power | — | Brief does not define it (S-10). The conservative choice (highest required MVA) is adopted as the **design basis**, and HV-metered power is reported as a sensitivity case | M | Sensitivity on η_el |
| A-12 | Feed blend, reductant, slag chemistry and product grade unchanged between the cases | — | Isolates the scale-up effect (Section 2) | H (as a method) | — |
| A-13 | ~~Furnace shell and hearth re-used~~ | — | **Closed: confirmed, now S-08** | — | — |
| A-14 | The existing 55 MW furnace already operates on the 65 MVA (total) transformer bank, i.e. the uprate gains 5 MW **without** more MVA | Baseline PF = 55/65 = 0.846 at η_el = 1 | Consistent with the brief (55 MW exists; 65 MVA stated) and with typical FeCr PF ≈ 0.85 [R-02]. Alternative: the existing transformer is smaller and replaced by 65 MVA. **Both give the same 60 MW constraint (PF ≥ 0.923)**, so the design conclusion does not depend on this | M | Report both interpretations; Q1b wording |

---

## 6. 55 MW baseline: how it will be established

Because **no plant operating data has been supplied**, the baseline is built as a **reference furnace**: a self-consistent design from published typical values and first-principles calculation. It is labelled as such and never presented as a real plant's data. If the Project Leader has real data (M-03, M-04), it replaces the reference values directly.

| Baseline quantity | Method | Tag |
|---|---|---|
| Active power *P* = 55 MW | Brief | [S] |
| Apparent power *S*, PF | *S* = *P*/PF with PF from A-05; checked against 65 MVA | [A]→[C] |
| Secondary voltage and current | From *S* = √3·*V*·*I* and Westly/Andreae similarity, cross-checked | [C] |
| Operating resistance *R* and reactance *X* | *P* = 3*I*²*R*; *X* = *R*·tan φ | [C] |
| Electrode diameter *D* | *D* = √(4*I* / (π·*J*)), *J* from A-07 | [C] |
| PCD, shell and hearth size | Literature ratios (A-10) and hearth power density | [C] |
| Production rate | Ṁ = *P*·*t*·*u* / SEC | [C] |

**Indicative order of magnitude only (to show significance, not a result):**
Daily energy = 55 MW × 24 h = 1 320 MWh/d. With SEC = 3.0–3.5 MWh/t [A-04] and utilisation 0.90–0.95 [A-09]:
Ṁ = 1 320 × (0.90 … 0.95) / (3.5 … 3.0) ≈ **340–418 t alloy/d** (≈ 124–153 kt/a).
Every additional 0.1 MWh/t of SEC costs roughly 11–14 t/d. The energy balance therefore matters as much as the electrical uprate.

---

## 7. 60 MW proposed case: definition and first findings

### 7.1 Definition
Same furnace (A-13) and same feed and product (A-12), with furnace active power raised to 60 MW [S] within a 65 MVA transformer limit [S]. Electrode geometry (D, PCD, penetration) and transformer secondary voltage taps are the design variables.

### 7.1a Consequences of the confirmed uprate basis (Rev B)

Because the shell, hearth and roof are fixed (S-08) and the apparent power is capped at 65 MVA total (S-07):

| Consequence | Quantity | Significance |
|---|---|---|
| Hearth / shaft power density rises at fixed hearth area | × 1.091 (+9.1 %) | Higher hearth and sidewall heat flux. Refractory and cooling-water capacity must be checked (M-11). |
| Off-gas generation and roof heat load rise roughly in proportion to production | ≈ +9 % (confirmed later by the mass balance) | The closed-furnace gas-cleaning plant, seals and pressure control must have this margin. |
| Electrode diameter can only grow if the existing electrode holder, contact clamps, casing and slipping system are replaced; PCD is limited by the existing roof penetrations and the electrode-to-wall clearance | Geometric limit | "Optimised electrode geometry" works **within fixed roof/shell boundaries**. PCD changes need new roof penetrations (a major outage). |
| PF at 65 MVA total becomes a binding constraint | PF ≥ 0.923 (η_el = 1) | See 7.3. The core design problem. |

**New question arising (Q1b):** Is the 65 MVA bank **new** (replacing the existing transformers), or does the existing 55 MW furnace **already run on 65 MVA**? If it already runs on 65 MVA, the uprate is purely an *R*/*X* (power factor) improvement. If the transformers are new, the existing rating and impedance are needed for the baseline.

### 7.2 Simple scale ratios (power ratio 60/55 = 1.0909)

| Scaling basis | Current ratio | Voltage ratio | Comment |
|---|---|---|---|
| Constant bath resistance *R* (*P* = 3*I*²*R*) | √1.0909 = **1.044** (+4.4 %) | 1.044 | Same geometry, more current |
| Westly similarity (*I* ∝ *P*^(2/3), *V* ∝ *P*^(1/3)) | 1.0909^(2/3) = **1.060** (+6.0 %) | 1.0909^(1/3) = **1.029** (+2.9 %) | Implies *R* ∝ *P*^(−1/3), i.e. R falls by 2.9 % |
| Constant current, higher voltage | 1.000 | **1.091** (+9.1 %) | Needs higher resistance: geometry or slag change |

**Significance:** at constant electrode diameter, the electrode current density rises by 4–6 %. If the baseline electrode already runs near its current-density limit (A-07), the uprate must be achieved mainly by **raising voltage and bath resistance** (larger PCD, higher-resistance burden/slag, electrode tip position) rather than by more current. This is why the brief couples the transformers with *electrode geometry*.

### 7.3 Critical finding: the 65 MVA limit forces a high power factor (screening, `calcs/00_screening_transformer_pf.py`)

Equations:
*S* = *P*_tx / PF  and  *P*_tx = *P*_furnace / η_el  ⇒  PF_min = *P*_furnace / (η_el · *S*_rated)
PF = *R* / √(*R*² + *X*²)  ⇒  *R*/*X* = PF / √(1 − PF²)

Substitution for 60 MW, 65 MVA, η_el = 1.00: PF_min = 60 / 65 = **0.923**, so *R*/*X* = 0.923/√(1 − 0.923²) = **2.40**.

| η_el (A-06) | PF_min at 55 MW | PF_min at 60 MW | Required *R*/*X* at 60 MW |
|---|---|---|---|
| 1.00 (power metered at the furnace terminals) | 0.846 | **0.923** | 2.40 |
| 0.98 | 0.863 | 0.942 | 2.80 |
| 0.96 | 0.881 | 0.962 | 3.50 |
| 0.94 | 0.900 | 0.982 | 5.20 |

Conversely, at the typical PF = 0.85 [A-05], 65 MVA delivers 55.2 MW of transformer active power, which is **almost exactly the 55 MW baseline**. 60 MW at PF 0.85 would need ≈ 70.6 MVA (η_el = 1) to 73.5 MVA (η_el = 0.96).

**Engineering interpretation, and a challenge to the brief:**
1. The 55 MW baseline appears to already be **MVA-limited on 65 MVA at PF ≈ 0.85**. The 60 MW case is therefore **not achievable by transformer rating alone**. It requires PF ≥ 0.92 at the very least, and more once circuit losses are counted.
2. PF ≥ 0.92 on a large FeCr SAF is **above the typical range** (0.85 for average-sized furnaces, lower for large ones [R-02]). It is only plausible if the circuit **reactance *X* is reduced** (shorter/interleaved high-current line, closer conductor spacing, low-reactance busbar design) **and/or the bath resistance *R* is increased** (larger PCD, burden/slag resistivity, electrode tip position), by roughly 50–120 % in *R*/*X* relative to PF 0.85.
3. **Shunt capacitor banks on the HV side do NOT reduce the furnace transformer MVA loading.** They improve the PF seen by the grid only. This is a common misconception and must not be used to justify the uprate.
4. Alternative routes to be evaluated: (a) transformer **overload rating** (furnace transformers are often specified with a continuous overload margin, M-01); (b) defining 60 MW at HV metering (Q5); (c) a larger transformer (outside the brief). *Rev B: the "65 MVA per transformer" escape route is closed by the Q1 answer, so the 65 MVA limit is **binding**.*

This finding becomes the central design argument of the assignment: **"optimised electrode geometry" is the lever that raises R/X so that 60 MW fits within 65 MVA.** It is tested quantitatively in Phase 2, with the risks that higher operating resistance carries (shallower electrode penetration, hotter roof and burden top, higher off-gas temperature, risk of a lower Cr recovery).

---

## 8. Methodology for the next phases (outline only, to be detailed after review)

### 8.1 Electrical calculation methodology (Phase 2)
1. Equivalent circuit per phase: *V*_ph = *I*(*R* + j*X*). *P* = 3*I*²*R*, *Q* = 3*I*²*X*, *S* = 3*V*_ph*I*.
2. Operating ("circle") diagram: *P*, *Q*, PF, *I* versus *R* for fixed secondary voltage taps. Locate the 55 and 60 MW points inside the 65 MVA and current-density limits.
3. Transformer secondary voltage and tap range: *V*_LL = *S*/(√3·*I*), with a tap range covering ±10–15 % of the operating point.
4. Electrode sizing: *D* = √(4*I*/(π*J*)). Check against *J*_max (A-07).
5. PCD and bath resistance: Andreae/Kelly *k* = *R*·*D* (or *R*·PCD) relationships. Westly *C₃* cross-check.
6. Secondary-circuit losses (η_el) and reactance budget (busbar, flexibles, clamps, columns).
7. Sensitivity and uncertainty: Monte-Carlo or one-at-a-time on PF, η_el, *J*, SEC.
8. Flagged only: harmonics, flicker, phase unbalance, interaction between electrodes (Mulholland, 2009).

### 8.2 Transformer and electrode investigation (Phase 2/4)
Transformer type (3×1φ vs 3φ), cooling (OFWF), on-load tap changer range and step size, impedance, overload capability, delta-closed-at-electrodes connection. Electrode: Söderberg casing, paste quality and baking zone, slipping rate versus current (paste consumption kg/t), breakage risk at higher current density, holder/contact-clamp current limits.

### 8.3 Additional metallurgical calculations (Phase 3)
1. Mass balance: feed → alloy + slag + gas. Cr, Fe and Si recoveries; Cr₂O₃ loss to slag.
2. Reductant (fixed-carbon) requirement and C in the alloy.
3. Slag chemistry: basicity (CaO+MgO)/SiO₂, MgO/Al₂O₃, liquidus temperature, slag volume per tonne.
4. Energy balance: reaction enthalpies + sensible heat of alloy, slag and gas + heat losses → SEC. Effect of preheating (A-04).
5. Production rate and tapping schedule at 55 and 60 MW.
6. Off-gas volume and composition (CO, H₂, CO₂). Gas-cleaning capacity check (+~9 %).
7. Electrode paste consumption.
8. Hearth/shaft power density (MW/m²) and residence time. Refractory and cooling heat flux implications.

### 8.4 Literature still to be researched
Original Westly (1974/75) and Andreae/Kelly papers; PCD/D design ratios; η_el and secondary reactance for large closed FeCr furnaces; peer-reviewed Söderberg current-density limits; published SA furnace design cases (Infacon / SAIMM / Pyrometallurgy.co.za).

---

## 9. Technical execution plan

| Phase | Content | Deliverable | Hold point |
|---|---|---|---|
| 1 | Brief interpretation, design basis, parameters, assumptions (**this document**) | `docs/01_Engineering_Design_Basis.md` | **HP-1: Project Leader review** |
| 2 | Electrical design: baseline and 60 MW operating points, PF/MVA envelope, tap range, electrode D/PCD | `docs/02_Electrical_Design.md`, `calcs/02_*.py` | HP-2 |
| 3 | Metallurgical mass and energy balance, SEC, production, slag, off-gas | `docs/03_Metallurgical_Balance.md`, `calcs/03_*.py` | HP-3 |
| 4 | Transformer and electrode specification, scale-up cross-checks (Westly/Andreae), sensitivity | `docs/04_Equipment_and_ScaleUp.md` | HP-4 |
| 5 | Risk register, constraints, recommendations | `docs/05_Risks_Recommendations.md` | HP-5 |
| 6 | Final assignment compilation (only when instructed) | Report | Final |

All parameters will be held in one file (`calcs/parameters.py`) carrying the [S]/[A]/[L]/[C] tags, so that any answer to Section 10 propagates through every calculation.

---

## 10. Decisions required from the Project Leader (HP-1)

| Q | Question | Why it matters |
|---|---|---|
| Q1 | ~~65 MVA total or per transformer?~~ **ANSWERED (Rev B): total.** | 65 MVA limit is binding |
| Q1b | ~~New or existing 65 MVA?~~ **ANSWERED (Rev C): the 55 MW furnace exists.** The existing transformer rating is not given, so it is handled by A-14 | Baseline electrical point via A-14 |
| Q2 | ~~Uprate or new design?~~ **ANSWERED (Rev B): uprate of existing furnace.** | Shell, hearth and roof fixed |
| Q3 | Confirm scope: include HV/grid, gas-cleaning, refractory, economics? | Workload and report structure |
| Q4 | Product grade (charge chrome / HC FeCr), electrode type (Söderberg?), feed type (pellets, preheated?) | Mass and energy balance and SEC |
| Q5 | ~~Measurement point?~~ **ANSWERED (Rev C): hypothetical lecturer scenario, not defined.** A-11 (power into furnace) adopted, with sensitivity | PF_min 0.923 (basis) → 0.96 (with losses) |
| Q6 | ~~Real data?~~ **ANSWERED (Rev C): none.** Reference-furnace approach (Section 6) confirmed | — |
| Q7 | Is there an assessment rubric / required referencing style (Harvard / IEEE)? | Report planning |
| Q8 | Do you accept the challenge in Section 7.3, i.e. that the central design problem is raising R/X (PF ≥ 0.92) by electrode geometry and reactance reduction? | Defines the thesis of the design |

---

## 11. References

See `references/REFERENCES.md` (R-01 … R-10). Status flags there show which sources were checked in full text and which only by abstract or synopsis.
