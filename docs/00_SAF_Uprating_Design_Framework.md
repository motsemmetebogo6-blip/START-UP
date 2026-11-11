# FERROCHROME SUBMERGED ARC FURNACE (SAF): ENGINEERING SCALE-UP DESIGN FRAMEWORK

**Document:** 00 – Controlling engineering document (Rev 0, issued for team approval at Gate G0)
**Project:** Design and Scale-Up of a Closed Ferrochrome Submerged Arc Furnace from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Owner:** Project Leader (engineering methodology and integration)
**Date:** 2026-11-11
**Precedence:** This document controls all other project documents. Where `docs/01` (design basis) or `docs/02` (electrical design) conflict with it, this document governs, and the conflict is logged in the change log (Section 12).

---

## 0. The governing question

> **How can an existing closed three-phase ferrochrome submerged arc furnace operating at approximately 55 MW be uprated to 60 MW using a 65 MVA transformer, while retaining the existing furnace infrastructure and maintaining safe, stable and efficient metallurgical operation?**

Every calculation, drawing, Power BI visual and report chapter must trace to this question through a work package (Section 3), a parameter or register ID (Section 7), and a decision criterion (Section 6).

### 0.1 What we already know (evidence from docs/01 and docs/02)

| Finding | Value | Status |
|---|---|---|
| Power increase | 60/55 = 1.0909, i.e. **+9.09 %** | [S] |
| Balanced phase power | 55/3 = **18.33 MW** → 60/3 = **20.00 MW** per electrode | [C] |
| Minimum power factor for 60 MW within 65 MVA | PF ≥ 60/65 = **0.9231** | [C] |
| Typical power factor of a large ferrochrome SAF | ≈ 0.85 or lower | [L] R-02, R-14 (abstract level) |
| Transformer loading if 60 MW is run at the baseline PF (0.846) | *S* = 60/0.846 = **70.9 MVA → 109 % of rating** | [C] calc 02 |
| Required increase in R/X (operating resistance ÷ circuit reactance) | 1.59 → 2.40 = **+51 %**, independent of the current calibration | [C] calc 02 |
| Preliminary feasible operating point (case 3c-20) | X −20 %, R +21 % → 114.4 kA, 328 V, J = 6.06 A/cm² | [C] (provisional, awaiting Gate G3) |

**Consequence for the methodology:** the 65 MVA transformer is **not** sufficient by itself. 60 MW is feasible only if the electrical operating regime changes: higher voltage, lower current, higher operating resistance, lower circuit reactance. That change must then be shown to be acceptable thermally, mechanically and metallurgically. The framework is built around proving or disproving this.

---

## 1. Project purpose

Develop and apply an integrated engineering method to decide whether, and how, an existing closed three-phase ferrochrome SAF can be uprated from ≈55 MW to 60 MW on a 65 MVA (total) transformer installation. The uprate must make maximum use of the existing infrastructure while maintaining electrical integrity, electrode performance, refractory life, operational stability, chromium recovery and product quality.

**The outcome is a feasibility decision, not a predetermined "yes".** A justified "60 MW is not feasible without upgrade X", or "the maximum safe uprate is Y MW", is an acceptable engineering result.

---

## 2. Design philosophy: brownfield uprating

| Principle | Meaning in this project |
|---|---|
| **Retain** | The existing furnace is the reference configuration. The shell, hearth and roof are fixed (S-08). |
| **Optimise** | Electrical operating point, electrode geometry (PCD and tip position), control setpoints and burden are the primary levers. |
| **Verify** | Every retained component is shown to have enough capacity at 60 MW. **Nothing is "retained" by default.** |
| **Target** | Technically feasible, safe and stable 60 MW operation, with stated margins. |

### 2.1 Equipment classification (four categories)

Your draft proposed three categories. I have added a fourth, **Verify**, because in a scenario without plant data many items **cannot yet be classified**. Without it, unclassified equipment would silently default to "Retain".

| Class | Definition | Evidence required to assign |
|---|---|---|
| **R – Retain** | Adequate verified capacity at 60 MW, with no change | Calculated utilisation ≤ acceptance limit (Section 6) |
| **O – Optimise** | Can handle 60 MW through operating or geometric adjustment, without replacing hardware | Calculation showing the adjusted state meets the limits |
| **U – Upgrade** | Cannot safely handle 60 MW and must be modified or replaced | Calculation showing a limit is exceeded, plus the proposed upgrade |
| **V – Verify** | Insufficient information to classify yet | Owner, data needed and due gate stated |

The live classification is kept in `registers/equipment_classification.csv` (Section 8). Its initial provisional entries are in Section 8.2.

---

## 3. Harmonised stage and work-package structure

Your draft used three numbering systems: Stages 1–10, work packages A–H and WP1–WP10. **One structure is adopted here:** each Stage *is* a work package, so Stage *n* = WP*n*. The letters A–H are kept only as aliases so existing notes can be traced.

| Stage / WP | Title | Alias (draft A–H) | Lead | Main deliverable | Gate closed |
|---|---|---|---|---|---|
| WP1 | Existing furnace assessment: **Reference Furnace Specification (RFS)** | A | M1 | `docs/03_Reference_Furnace_Specification` | G1 |
| WP2 | Design requirements, constraints and acceptance criteria | – | M6 (with all) | Section 6 of this document, frozen | G1 |
| WP3 | Electrical system assessment | B | M2 | Electrical design (docs/02 → Rev B) | G3 |
| WP4 | Electrode system optimisation | C | M3 | Electrode optimisation report | G3 |
| WP5 | Thermal, cooling and refractory assessment | D | M4 | Thermal assessment | G3 |
| WP6 | Mechanical and structural assessment | E | M1 (with M4) | Structural assessment | G3 |
| WP7 | Metallurgical performance (mass and energy balances) | F | M5 | Mass and energy balance report | G3 |
| WP8 | Integrated 60 MW design | G | M6 + Project Leader | 60 MW design proposal | G4 |
| WP9 | Technical and economic validation | H | M6 (economics), all (verification) | Feasibility decision and economic evaluation | G5 |
| WP10 | Implementation and monitoring | – | M6 with M2/M4 | Upgrade sequence, commissioning plan, KPIs | G6 |

**Mapping to earlier work:** `docs/01` covers parts of WP1/WP2. `docs/02` is a *preliminary* WP3 (electrical) result. The old "Phase 1–6" plan in docs/01 Section 9 is **superseded** by this table.

### 3.1 Stage gates

| Gate | Name | Pass condition | Approver |
|---|---|---|---|
| **G0** | Framework approval | This document agreed by all six members | Project Leader |
| **G1** | Baseline freeze | RFS (WP1) and acceptance criteria (WP2) frozen; common assumptions register at Rev 1 | Project Leader + M1 |
| **G2** | Method review | Each WP owner presents its method, inputs and outputs (no results needed) and interfaces are agreed (Section 5) | Project Leader |
| **G3** | Subsystem results | WP3–WP7 results calculated, independently checked (Section 9), and equipment classified R/O/U | Project Leader + checker |
| **G4** | Integrated design | One consistent 60 MW configuration; every interface value matches across WPs | Project Leader |
| **G5** | Feasibility decision | All Section 6 criteria evaluated; sensitivity and risk complete; decision recorded | Whole team |
| **G6** | Final report | Report, dashboard and drawings trace to registers; no untagged numbers | Project Leader |

**Rule:** a WP may start work before its gate. It may **not** pass results downstream as final until the gate is closed. Values used before a gate are marked *provisional* in the register.

---

## 4. Responsibilities: six-member allocation

| Member | Technical responsibility | Owns WPs | Independent checker of |
|---|---|---|---|
| **M1** | Existing furnace assessment and configuration; mechanical/structural | WP1, WP6 | WP5 |
| **M2** | Electrical engineering and transformer calculations | WP3 | WP4 |
| **M3** | Electrode geometry and optimisation | WP4 | WP3 |
| **M4** | Thermal, cooling and refractory | WP5 | WP6 |
| **M5** | Metallurgy: mass and energy balances | WP7 | WP9 (technical) |
| **M6** | Power BI, economics, design integration | WP2, WP8, WP9, WP10 | WP7 |
| **Project Leader** | Engineering methodology (this document), interface coordination, gate approval, final technical sign-off | Framework, registers | All (spot checks) |

The cross-checking pairs are deliberate: electrical ↔ electrode, and thermal ↔ mechanical, are the most tightly coupled interfaces. Each member checks the work that feeds their own.

---

## 5. Interface control

### 5.1 The central coupling loop

The uprate is **not** a sequence of independent calculations. The central loop is:

| Loop step | From → To | What is passed |
|---|---|---|
| ① | WP3 Electrical → WP4 Electrodes | Required *R*, *X*, *I* and *V* for 60 MW within 65 MVA |
| ② | WP4 Electrodes → WP5 Thermal | Geometry that achieves *R*: PCD, tip position, burden resistivity |
| ③ | WP5 Thermal → WP7 Metallurgy | Resulting heat distribution (hearth, burden top, roof, off-gas) |
| ④ | WP7 Metallurgy → WP3 Electrical | Accept, or a feedback constraint (SEC, Cr recovery, slag temperature) → loop again |
| ⑤ | WP7 → WP5 / WP6 / WP9 | Production rate, off-gas and heat loads once the loop closes |

1. WP3 states the R and X needed for 60 MW within 65 MVA (currently R +21 % with X −20 %).
2. WP4 must show which geometry (PCD, electrode tip position, burden resistivity) **achieves** that R within the existing roof and shell.
3. WP5 checks the heat distribution this causes. Higher R normally means shallower electrode tips, so more heat goes to the top of the furnace and less to the hearth.
4. WP7 checks the effect on chromium recovery, slag temperature and specific energy (SEC).
5. If any check fails, the loop repeats with a different R/X split.

**Iteration rule:** at most three loops before Gate G4. If no split satisfies everything, the Project Leader escalates to a **capacity decision** (the maximum feasible MW, or a required upgrade) instead of forcing 60 MW.

### 5.2 Interface register (summary; full list in `registers/interfaces.csv`)

| ID | From → To | Data item | Unit | Needed by |
|---|---|---|---|---|
| IF-01 | WP1 → all | Reference Furnace Specification (dimensions, D, PCD, transformer data) | various | G1 |
| IF-02 | WP3 → WP4 | Electrode current *I*, required operating resistance *R* | kA, mΩ | G2 |
| IF-03 | WP4 → WP3 | Resistance achievable from geometry; electrode column reactance | mΩ | G3 |
| IF-04 | WP3 → WP5 | Power split: bath, electrode, and conductor losses | MW | G3 |
| IF-05 | WP4 → WP5 | Electrode tip position and penetration; PCD | m | G3 |
| IF-06 | WP7 → WP5 | Process heat balance: heat to slag, alloy, off-gas and losses | MW | G3 |
| IF-07 | WP5 → WP7 | Hearth and slag temperature feasibility | °C | G3 |
| IF-08 | WP7 → WP6/WP9 | Production rate, alloy and slag masses, off-gas volume | t/d, Nm³/h | G3 |
| IF-09 | WP3 → WP6 | Electrode current and short-circuit forces on holders and busbars | kA, kN | G3 |
| IF-10 | WP3–WP7 → WP9 | Equipment utilisation against limits (for the dashboard) | % | G4 |
| IF-11 | WP8/WP9 → WP10 | Upgrade list and operating limits | – | G5 |

---

## 6. Engineering decision criteria (acceptance limits)

The 60 MW configuration may be recommended **only** if every criterion below is met, or a deviation is formally accepted with a mitigation. Limits marked ◇ are **provisional engineering-judgement values**. They must be justified or replaced by the WP owner before G1.

| ID | Criterion | Acceptance limit | Basis | WP |
|---|---|---|---|---|
| DC-01 | Transformer apparent power | *S* ≤ 65 MVA continuous at the operating tap (loading ≤ 100 %) | S-07; IEC 60076-1 rating concept | WP3 |
| DC-02 | Furnace power factor at the operating point | PF ≥ 0.923 (= 60/65, η_el = 1); higher once circuit losses are counted | Derived (docs/02) | WP3 |
| DC-03 | Secondary voltage | Operating voltage within the transformer tap range, with ≥ ±5 % control margin ◇ | Furnace transformer practice; IEEE C57.17 to be referenced | WP3 |
| DC-04 | Electrode current density | J(60 MW) ≤ J(baseline) = 6.38 A/cm² | A-07 (revised); docs/02 §2 | WP4 |
| DC-05 | Electrode current | I(60 MW) ≤ baseline current (120.5 kA), i.e. no increase in holder/clamp loading | RFS; A-14 | WP4/WP6 |
| DC-06 | Cooling-water heat removal | Heat load ≤ 90 % of design capacity (≥ 10 % margin) ◇ | Engineering judgement, to be referenced | WP5 |
| DC-07 | Refractory and shell | Hot-face/shell temperatures and heat flux within the design values of the RFS; no increase in hearth hot-spot risk | WP5 analysis | WP5 |
| DC-08 | Structural | Roof, shell and electrode support loads within rated capacity | WP6 analysis | WP6 |
| DC-09 | Chromium recovery | No reduction greater than 1 percentage point versus baseline ◇ | Engineering judgement | WP7 |
| DC-10 | Specific energy consumption | SEC(60 MW) ≤ SEC(baseline) × 1.02 ◇ | Engineering judgement | WP7 |
| DC-11 | Off-gas and auxiliaries | Off-gas flow, feed and tapping capacity ≥ 60 MW requirement (≈ +9 %) | WP7 → plant capacities in the RFS | WP7/WP6 |
| DC-12 | Operational stability | Operating point inside the stable control region (resistance control preferred, R-02); no persistent operation on electrode top or bottom stops | WP3/WP4 | WP3/WP4 |
| DC-13 | Economics | Positive NPV over the evaluation period at the agreed discount rate ◇ | WP9 method | WP9 |

**Note on capacitors (a common error to avoid):** shunt capacitors on the HV side improve the PF that the **grid** sees. They do **not** reduce the furnace transformer's MVA loading. They can only help DC-02/DC-01 if placed on the secondary side, which is a separate design option needing its own evaluation.

---

## 7. Mathematical design basis

### 7.1 Scenario definitions

| Scenario | Definition |
|---|---|
| **A – Existing** | 55 MW furnace (Reference Furnace Specification), 65 MVA total, existing electrode geometry |
| **B – Proposed** | 60 MW, the same 65 MVA, optimised electrode geometry and electrical operating point |
| B-variants | B0: change R only (3c-0); **B20: X −20 % plus R +21 % (preferred, provisional)**; B30: mainly reduce X (3c-30) |

**Comparison rule:** the same feed, reductant, product grade, slag chemistry and calculation methods are used in A and B. Only the uprate variables change (docs/01, A-12).

### 7.2 Initial project parameters

| Parameter | Scenario A | Scenario B | Tag |
|---|---|---|---|
| Active power *P* | 55 MW | 60 MW | [S] |
| Transformer rating *S*_rated | 65 MVA (total) | 65 MVA (total) | [S] |
| Power increase | – | +9.09 % | [C] |
| Balanced phase power *P*/3 | 18.33 MW | 20.00 MW | [C] |
| Minimum PF at 65 MVA | 55/65 = 0.846 | 60/65 = **0.923** | [C] |
| Transformer loading at baseline PF 0.846 | 100 % | **109 %** (70.9 MVA) | [C] |

### 7.3 Calculation register (what each WP must calculate)

Status: ✔ done (provisional) · ◐ partly done · ○ not started · ⊘ blocked by missing data (a stated assumption is needed).

| WP | Calculation | Governing equation(s) | Status |
|---|---|---|---|
| WP3 | Active, reactive and apparent power | *P* = 3*I*²*R*; *Q* = 3*I*²*X*; *S* = √(*P*² + *Q*²) | ✔ docs/02 |
| WP3 | Secondary voltage | *V*_LL = *S* / (√3 *I*) | ✔ docs/02 |
| WP3 | Primary current | *I*_1 = *S* / (√3 *V*_HV) | ⊘ HV voltage not given → assumption needed (typical SA furnace supply 33–132 kV) |
| WP3 | Secondary winding current (delta closed at the electrodes) | *I*_winding = *I*_electrode / √3 | ◐ docs/02 §6 (≈ 66–70 kA) |
| WP3 | Transformer loading and margin | Loading = *S*/*S*_rated | ✔ |
| WP3 | Transformer impedance and short-circuit reactance | *X*_T = *u*_k · *V*² / *S*_rated | ⊘ *u*_k not given → literature range |
| WP3 | Furnace R and X; split of X into transformer, short network and columns | *X* = *X*_T + *X*_SN + *X*_col | ◐ total only |
| WP3 | Losses and electrical efficiency | η_el = *P*_bath / *P*_tx = 1 − *I*²*R*_cond / *P*_tx | ○ |
| WP4 | Electrode current, cross-section, current density | *A* = π*D*²/4; *J* = *I*/*A* | ✔ docs/02 |
| WP4 | Electrode (column) resistance and resistive heating | *R*_e = ρ_e*L*/*A*; *P*_e = *I*²*R*_e | ○ (needs paste resistivity, literature) |
| WP4 | Pitch circle diameter and spacing | PCD/D ratio; spacing = PCD·sin 60° (= PCD·√3/2) | ○ (literature ratio needed, A-10) |
| WP4 | Immersion/tip position vs operating resistance | Andreae/Kelly *k*-factor relations; R vs penetration | ○ (needs R-01 full text) |
| WP4 | Electrode (paste) consumption | kg paste per t alloy × production rate | ○ |
| WP5 | Heat balance and losses; cooling-water heat removal | *Q* = ṁ*c*_pΔ*T* | ○ |
| WP5 | Refractory thermal loading | 1-D conduction *q* = ΔT/ΣR_th through the lining layers | ○ |
| WP5 | Hearth and shaft power density | *P*/*A*_hearth (+9.1 % at fixed area) | ◐ |
| WP6 | Shell integrity, roof loading, electrode support/clamp capacity | Load vs rating; electromagnetic forces on conductors | ○ |
| WP7 | SEC, production rate | Ṁ = *P*·*t*·*u* / SEC | ◐ indicative (docs/01 §6) |
| WP7 | Cr recovery; charge, slag and carbon balances | Element balances (Cr, Fe, Si, C, O) | ○ |
| WP7 | Heat balance; slag–metal separation (slag liquidus/viscosity, tapping) | Enthalpy balance; slag chemistry | ○ |
| WP9 | Economic evaluation | NPV, payback; capital cost of the U-class items | ○ |

**Data warning (agreeing with your note):** electrode current and current density depend on the circuit configuration, secondary voltage and electrode dimensions. Because the scenario has **no** plant data (S-10), those inputs come from the frozen RFS (Section 8.1), not from measurements. The current calibration (Westly *C*₃ = 8.33) is therefore a **reference-furnace assumption** (A-18). Every WP must quote results as *for the reference furnace*.

---

## 8. Common design basis: one source of truth

### 8.1 Reference Furnace Specification (replaces "obtain existing plant data")

The draft's first action, "obtain the existing furnace specifications and operating data", **cannot be carried out**: the lecturer has confirmed that the scenario is hypothetical and that no plant data exists (S-10). Requesting it again would stall the team. Instead:

> **WP1 produces a Reference Furnace Specification (RFS):** a complete, self-consistent description of the "existing" 55 MW furnace, built only from the brief [S], referenced literature [L], documented assumptions [A] and calculation [C]. At Gate G1 it is **frozen** and becomes the "existing furnace" for every WP. It is never described as real plant data.

**Update (Rev 0.1):** the full draft RFS is now `docs/03_Reference_Furnace_Specification.md` (Rev A, for freezing at G1). The summary below is kept for reference; docs/03 governs.

Provisional RFS contents. Entries marked ◐ are already established; the rest are WP1 tasks:

| RFS item | Provisional value | Tag / source |
|---|---|---|
| Furnace power / rating | 55 MW / 65 MVA total | [S] |
| Transformer arrangement | 3 × 21.7 MVA single-phase, delta closed at the electrodes ◐ | [A] docs/02 §6 |
| Secondary voltage / current at baseline | 312 V / 120.5 kA ◐ | [C] calibrated (A-18) |
| Operating resistance / reactance per phase | 1.264 / 0.796 mΩ ◐ | [C] |
| Electrode type / diameter | Söderberg, 1.55 m ◐ | [A] A-02, A-16 (R-11, R-13) |
| Shell inner diameter | ≈ 13.7 m (published 63 MVA SA ferrochrome analogue) | [L] R-11 (abstract level), to be confirmed |
| PCD, hearth diameter and depth, roof penetrations | **WP1 task** | [L]/[C] |
| Feed, reductant, product and slag chemistry | **WP1/WP7 task** (published SA chromite) | [L] |
| HV supply voltage, transformer *u*_k, tap range | **WP1/WP3 task** | [A]/[L] |
| Cooling-water design capacity; off-gas plant capacity | **WP1/WP5 task** | [A] |

### 8.2 Common registers (controlled, in `registers/`)

| Register | File | Controlled by | Content |
|---|---|---|---|
| Assumptions | `registers/assumptions_register.csv` | Project Leader | Every [A] value: ID, value, unit, justification, reference, confidence, owner, status |
| Equipment classification | `registers/equipment_classification.csv` | Project Leader with WP owners | R/O/U/V per component: limit, value A, value B, utilisation, evidence |
| Interfaces | `registers/interfaces.csv` | Project Leader | IF-xx items (Section 5.2) |
| References | `references/REFERENCES.md` | Each author adds; Project Leader audits | Status FT/AB/TBF |
| Parameters (for calculations) | `calcs/parameters.py` | WP owners, via change control | The only place input numbers live |

**Initial provisional equipment classification** (to be confirmed at G3):

| Component | Provisional class | Reason (current evidence) | Owner |
|---|---|---|---|
| Furnace shell, hearth refractory | R → **V** | Fixed by S-08; power density at fixed area +9.1 % | M4/M1 |
| Roof and seals | **V** | Roof heat and off-gas load ≈ +9 %; higher if electrodes ride higher | M1/M4 |
| Furnace transformers (65 MVA) | **V → likely U (tap range)** | MVA unchanged, but 60 MW needs ≈ 328–367 V versus 312 V at baseline | M2 |
| Short network (busbars, flexibles) | **U** | X −20 % needed (case B20) | M2 |
| Electrode columns (D = 1.55 m) | **R** (provisional) | Current density falls: 6.38 → 6.06 A/cm² | M3 |
| Electrode holders and contact clamps | **R** (provisional) | Current falls: 120.5 → 114.4 kA | M3/M1 |
| Electrode PCD and positions | **O** if within the existing roof openings; otherwise **U** | Needed to raise R | M3/M1 |
| Electrode regulation (control) | **O** | New resistance setpoints; resistance control preferred | M2/M3 |
| Electrode slipping and paste system | **V** | Paste consumption ≈ +9 % | M3 |
| Cooling-water system | **V** | Heat load increase not yet quantified | M4 |
| Off-gas cleaning | **V** | ≈ +9 % gas | M5/M1 |
| Feed preparation, charging, tapping | **V** | ≈ +9 % throughput | M5/M1 |
| HV supply and reactive compensation | **V** | Grid PF and harmonics: flagged only (scope) | M2 |

### 8.3 Data tagging and change control

* Every number carries one tag: **[S]** brief/leader · **[L]** literature (with R-ID and FT/AB status) · **[A]** assumption (A-ID) · **[C]** calculated (calc file) · **[M]** missing. There is **no "actual/measured" tag in this project**, because no measurements exist (S-10). Your Power BI requirement to "distinguish actual measurements, design assumptions and calculated values" is met with these tags, and the dashboard must show that the "measured" category is empty.
* A change to any frozen value after G1 needs a **change note** in Section 12: what changed, why, which WPs are affected, and re-run calcs. Only the Project Leader approves.
* No assumed value may be presented as plant operating data.

---

## 9. Verification and validation

| Level | Method | Who |
|---|---|---|
| V1 – Arithmetic | Every hand calculation reproduced in Python (`calcs/`) from `parameters.py` | WP owner |
| V2 – Independent check | Checker re-derives the key results without seeing the author's script (pairs in Section 4) | Checker |
| V3 – Benchmark | Results compared against published furnace data (for example C₃, J, PF, SEC ranges) | WP owner |
| V4 – Sensitivity | One-at-a-time variation of the top uncertain inputs (C₃, η_el, PF, SEC, X reduction) | WP owner; M6 collates |
| V5 – Consistency | At G4, every interface value is identical in the sending and receiving WP | Project Leader |

---

## 10. Power BI: engineering decision-support dashboard (M6)

### 10.1 Pages

| Page | Content | Key visuals |
|---|---|---|
| 01 Overview | Scenario A vs B KPIs and feasibility verdict | KPI cards (MW, MVA, PF, kA, V, t/d, MWh/t); a red/green criteria strip for DC-01…DC-13 |
| 02 Electrical | MVA, MW, Mvar, PF, I, V, R, X, loading | Operating chart (P vs I with the 65 MVA limit); B-variant comparison |
| 03 Electrodes | J, I, D, PCD, tip position, paste consumption | J vs limit gauge; geometry table |
| 04 Metallurgy | Production, Cr recovery, SEC, slag, off-gas | A vs B bars; mass-balance Sankey (optional) |
| 05 Feasibility and constraints | Equipment utilisation vs limits; R/O/U/V classification; risks | Utilisation bar chart (limit = 100 %); classification matrix; risk heat map |
| 06 Data provenance (added) | Share of values by tag [S]/[L]/[A]/[C]; open assumptions; references not yet full-text | Provenance donut; table of low-confidence items driving decisions |

Page 06 is added because the dashboard's value depends on showing **how much of each verdict rests on assumptions**.

### 10.2 Data model (star schema, fed only from the repository)

| Table | Grain | Key columns |
|---|---|---|
| `fact_values` | One value per parameter per scenario | ScenarioID, ParamID, Value, Unit, Tag, SourceRef, WP, Gate, Rev |
| `dim_scenario` | Scenario | ScenarioID, Name, Description |
| `dim_parameter` | Parameter | ParamID, Name, Unit, WP, Owner, Category |
| `fact_limits` | Equipment × scenario | EquipmentID, Limit, Value, Utilisation, Class |
| `dim_assumption` | Assumption | A-ID, Value, Confidence, Status, Owner |

Example measures:
`Utilisation % = DIVIDE(SUM(fact_limits[Value]), SUM(fact_limits[Limit]))` and `Margin % = 1 − [Utilisation %]`. Conditional formatting: green ≤ 90 %, amber 90–100 %, red > 100 %.

**Rule:** Power BI never holds hand-typed engineering numbers. All data comes from CSVs generated by `calcs/export_powerbi.py`, so the dashboard always matches the calculations. A starter dataset is in `powerbi/`.

---

## 11. Deliverables and traceability

| # | Deliverable | WP | Gate |
|---|---|---|---|
| 1 | Reference Furnace Specification (existing furnace assessment) | WP1 | G1 |
| 2 | Engineering design basis (docs/01) | WP2 | G1 |
| 3 | Common assumptions register | WP2 | G1 |
| 4 | Electrical calculations and transformer assessment | WP3 | G3 |
| 5 | Electrode optimisation assessment | WP4 | G3 |
| 6 | Thermal assessment | WP5 | G3 |
| 7 | Mechanical/structural assessment | WP6 | G3 |
| 8 | Metallurgical mass and energy balances | WP7 | G3 |
| 9 | Proposed 60 MW engineering configuration | WP8 | G4 |
| 10 | Technical risk assessment and sensitivity | WP9 | G5 |
| 11 | Economic evaluation | WP9 | G5 |
| 12 | Power BI performance dashboard | WP9 (M6) | G5 |
| 13 | Drawings and schematics (single-line diagram, electrode layout plan, short-network arrangement) | WP3/WP4/WP6 | G4 |
| 14 | Implementation, commissioning and monitoring plan | WP10 | G6 |
| 15 | Final engineering design report | All | G6 |

**Traceability chain (mandatory):** report statement → table/figure → calc file and result CSV → `parameters.py` entry → tag → register ID or reference ID.

---

## 12. Change log and decisions affecting earlier documents

| No. | Date | Change | Affects |
|---|---|---|---|
| CN-01 | 2026-11-11 | Framework adopted as the controlling document; the Phase 1–6 plan in docs/01 §9 is superseded by WP1–WP10 and Gates G0–G6 | docs/01 |
| CN-02 | 2026-11-11 | **Scope change:** economic evaluation (WP9) and mechanical/structural assessment (WP6) are now **in scope**. This reverses the Q3 default in docs/01 §1.3. | docs/01 §1.3 |
| CN-03 | 2026-11-11 | "Obtain existing plant data" replaced by the Reference Furnace Specification, because no plant data exists (S-10) | WP1 |
| CN-04 | 2026-11-11 | Fourth equipment class **V – Verify** added to Retain/Optimise/Upgrade | Section 2.1 |
| CN-05 | 2026-11-11 | Results in docs/02 reclassified as *preliminary WP3 results*, provisional until G3; questions Q9–Q11 are carried into G2/G3 | docs/02 |

---

## 13. Immediate actions (before detailed calculations)

| # | Action | Owner | Gate |
|---|---|---|---|
| 1 | Circulate this framework; all members confirm or comment | Project Leader | G0 |
| 2 | Produce the **Reference Furnace Specification** (replaces obtaining plant data) | M1 (+ M2 transformer data, M3 electrode layout) | G1 |
| 3 | Justify or replace every ◇ provisional acceptance limit in Section 6 | Each WP owner | G1 |
| 4 | Review the common assumptions register; each member adds their WP's assumptions **there only**, not in private files | All | G1 |
| 5 | Present the WP method statement (inputs, equations, outputs, interfaces) | Each WP owner | G2 |
| 6 | Build Power BI pages 01, 02 and 06 from the starter dataset in `powerbi/` | M6 | G2 |

**Technical warning (adopted from the Project Leader's brief):** a 65 MVA transformer is not automatically sufficient because it is close to the 60 MW requirement. Its suitability must be shown against the actual operating power factor, tap range, impedance and complete secondary circuit (DC-01 to DC-03). The preliminary evidence (Section 0.1) shows it is sufficient **only** if R/X rises by about 51 %.

---

**Overall objective:** establish a technically defensible route for increasing the existing ferrochrome SAF operating power from 55 MW to 60 MW, or a justified alternative maximum, without compromising the integrity, safety, stability and metallurgical performance of the existing furnace.
