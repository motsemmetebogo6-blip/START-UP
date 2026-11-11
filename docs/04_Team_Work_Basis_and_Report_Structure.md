# TEAM WORK BASIS AND PROJECT REPORT STRUCTURE

**Project:** Design and Scale-Up of a Closed Ferrochrome Submerged Arc Furnace from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Project Leader
**To:** All team members (M1 to M6)
**Document:** 04 (Rev 0), issued 2026-11-11
**Purpose:** to tell every member **what we are working from, which numbers to use, what rules apply, and which part of the final report each person writes.**

> **Read this first.** Everything you calculate or write must start from the documents and numbers listed in Sections 1 and 2. Do **not** create your own baseline, invent plant data, or use different input values. If you need a value that is not in the registers, ask the Project Leader so it can be added for everyone.

---

## 1. What we are working from (our basis)

| # | Document / file | What it gives you | Status |
|---|---|---|---|
| 1 | **00 – SAF Uprating Design Framework** | The controlling method: governing question, work packages WP1–WP10, gates G0–G6, acceptance criteria DC-01 to DC-13, Retain/Optimise/Upgrade/Verify classes | Rev 0 – for approval |
| 2 | **01 – Engineering Design Basis** | Interpretation of the brief, scope, missing parameters, original assumptions | Rev D |
| 3 | **02 – Electrical Design (preliminary)** | Baseline and 60 MW electrical operating points, the R/X requirement, transformer requirements | Rev A – provisional |
| 4 | **03 – Reference Furnace Specification (RFS)** | **The "existing 55 MW furnace"**: electrical, geometry, feed, slag, production, auxiliaries | Rev A – to freeze at G1 |
| 5 | **Assumptions register** (`registers/assumptions_register.csv`) | Every assumed value (A-01 to A-23) with justification and confidence | Live – the only place assumptions are kept |
| 6 | **Equipment classification register** (`registers/equipment_classification.csv`) | Retain/Optimise/Upgrade/Verify status of each component (EQ-01 to EQ-13) | Live |
| 7 | **Interface register** (`registers/interfaces.csv`) | What each member must hand to whom, and by which gate (IF-01 to IF-11) | Live |
| 8 | **Reference register** (`references/REFERENCES.md`) | All sources R-01 to R-20, with full-text status | Live |
| 9 | **Calculation files** (`calcs/`) and **results** (`results/`) | Python verification of every number; `parameters.py` holds all inputs | Live |
| 10 | **Power BI dataset** (`powerbi/`) | The dashboard tables generated from the calculations | Starter |

**Important – nature of the data:** the lecturer confirmed that this is a **hypothetical scenario with no real plant data**. Our "existing furnace" is the **Reference Furnace Specification**: a referenced, self-consistent representative furnace. In the report we always say "the reference furnace", never "the plant data shows".

---

## 2. Common numbers – everyone uses these

Use these exact values. If your work shows one of them is wrong, raise it with the Project Leader. Do not quietly use a different number.

| Quantity | Existing (Scenario A) | Proposed 60 MW (Scenario B20, provisional) | Source |
|---|---|---|---|
| Active power | 55 MW | 60 MW | Brief |
| Transformer rating (total) | 65 MVA (3 × 21.67 MVA single-phase) | 65 MVA | Brief / RFS |
| Phase power | 18.33 MW | 20.00 MW | Calc |
| Power factor | 0.846 | 0.923 (minimum required) | RFS / docs/02 |
| Electrode current | 120.5 kA | 114.4 kA | RFS / docs/02 |
| Secondary voltage (line) | 312 V | 328 V | RFS / docs/02 |
| Operating resistance per phase | 1.264 mΩ | 1.528 mΩ (+21 %) | docs/02 |
| Reactance per phase | 0.796 mΩ | 0.637 mΩ (−20 %) | docs/02 |
| R/X | 1.59 | 2.40 | docs/02 |
| Electrode diameter / current density | 1.55 m / 6.38 A/cm² | 1.55 m / 6.06 A/cm² | RFS |
| Pitch circle diameter (PCD) | 4.19 m | **to be optimised (WP4)** | RFS |
| Hearth diameter / power density | 10.88 m / 0.59 MW/m² | 10.88 m / 0.65 MW/m² | RFS |
| Shell inner diameter | 13.7 m | 13.7 m (fixed) | RFS |
| Specific energy (SEC) | 3.25 MWh/t | **to be calculated (WP7)** | Assumption A-04 |
| Alloy production | 374 t/d | ≈ 408 t/d (indicative) | RFS |
| Feed (LG6 concentrate) | Cr₂O₃ 44.2 %, FeO 24.1 %, Al₂O₃ 13.8 %, MgO 11.5 %, SiO₂ 2.5 % (Cr/Fe 1.61) | same | RFS |
| Slag (typical) | SiO₂ 30 %, Al₂O₃ 26 %, MgO 23 %, CaO 2 %, Cr₂O₃ 4.5–13 % | **to be calculated (WP7)** | RFS |

**Three findings everyone must understand before starting:**

1. **The 65 MVA transformer does not automatically give 60 MW.** At today's power factor (0.846), 60 MW needs 70.9 MVA, i.e. **109 % loading**. 60 MW is only possible if R/X rises by about 51 %, through higher operating resistance (electrode geometry) and lower circuit reactance (busbar/short-network changes).
2. **Electrode current goes down, not up.** The 60 MW case runs at higher voltage and lower current. Electrode diameter can stay at 1.55 m. "Optimised electrode geometry" means **PCD and electrode tip position**, not a bigger electrode.
3. **Auxiliary plant is probably at its limit.** With a 10 % design margin (A-22), cooling water, off-gas and feed systems would run at 99 % at 60 MW. They are therefore likely **Upgrade** items.

---

## 3. Rules of work (apply to every chapter)

1. **Tag every number:** [S] brief · [L] literature (with reference) · [A] assumption (with A-number) · [C] calculated. There is **no "measured" data** in this project.
2. **Show every calculation:** equation → substitution with units → result → **what it means for the design**.
3. **Verify in Python:** every hand calculation is repeated in `calcs/`, reading its inputs from `parameters.py`.
4. **One assumptions list:** new assumptions go into the common register (ask the Project Leader for the next A-number). No private assumption lists.
5. **References:** Harvard style. Each source goes into the reference register with its status (full text read / abstract only). Abstract-only sources must be checked before the final report.
6. **Units:** SI. Power in MW and MVA, current in kA, resistance in mΩ, energy in MWh/t, temperature in °C.
7. **Interfaces:** when your result is needed by someone else (see the interface register), send it by the stated gate and record it in the register.
8. **Challenge, don't force:** if your calculation shows 60 MW does not work for your equipment, **report it**. That is a valid engineering result.
9. **Independent check:** each member checks another member's work (Section 6).
10. **Never** present an assumed or literature value as plant operating data.

---

## 4. Project report structure and responsibilities

**Key:** PL = Project Leader. M1 = furnace/mechanical. M2 = electrical. M3 = electrodes. M4 = thermal/refractory. M5 = metallurgy. M6 = Power BI/economics/integration.

### Overview

| Ch. | Title | Lead | Contributors | WP | Gate | Starting material | Status |
|---|---|---|---|---|---|---|---|
| 1 | Executive summary | PL | M6 | – | G6 | Written last | Not started |
| 2 | Problem definition | PL | – | WP2 | G1 | docs/00 §0–1, docs/01 §1 | Draft material exists |
| 3 | Existing process description | M1 | M5 | WP1 | G1 | docs/03 §2, §5 | Draft material exists |
| 4 | Design basis | PL | M6 | WP2 | G1 | docs/01, docs/00 §6–7 | Draft material exists |
| 5 | Assumptions | PL | All | WP2 | G1 | Assumptions register (A-01 to A-23) | Live |
| 6 | Literature review | M5 (editor) | All | All | G2 | Reference register R-01 to R-20 | Partly done |
| 7 | Existing condition calculations | M1 | M2 | WP1 | G1 | docs/03, calc 01 | Draft material exists |
| 8 | Mass balance | M5 | – | WP7 | G3 | Feed and slag data in docs/03 §5 | Not started |
| 9 | Energy balance | M5 | M4 | WP7/WP5 | G3 | SEC range A-04 | Not started |
| 10 | Electrical analysis (includes the electrode system) | M2 | **M3** (electrodes) | WP3/WP4 | G3 | docs/02, calc 02 | Preliminary done |
| 11 | Process/metallurgical analysis | M5 | M3, M4 | WP7 | G3 | Chapters 8–9 | Not started |
| 12 | Development of alternatives | M2 | M3, PL | WP8 | G3 | docs/02 cases B0/B20/B30 | Preliminary done |
| 13 | Detailed calculations (recommended alternative) | All | M4 thermal, M1 mechanical | WP3–WP7 | G3 | All WPs | Not started |
| 14 | Equipment/design requirements | M6 (compiler) | All | WP8 | G4 | Equipment register EQ-01 to EQ-13 | Started |
| 15 | Economic evaluation | M6 | M1 | WP9 | G5 | Upgrade (U) list | Not started |
| 16 | Sensitivity analysis | M6 | All | WP9 | G5 | Critical assumptions A-22, A-23, A-17, A-18, A-04 | Not started |
| 17 | Risk assessment | M4 | All | WP9 | G5 | – | Not started |
| 18 | Recommended design | PL | M6 | WP8 | G5 | Chapters 12–17 | Not started |
| 19 | Implementation plan | M6 | M1, M2 | WP10 | G6 | – | Not started |
| 20 | Conclusion | PL | – | – | G6 | Written last | Not started |
| – | References | PL (audit) | All | – | G6 | Reference register | Live |
| – | Appendices | M6 (compiler) | All | – | G6 | Python printouts, registers, drawings | Live |

**Where the missing topics go:** the given structure has no separate chapters for electrodes, thermal/refractory or mechanical work. They are placed as follows:
* **Electrode system (M3):** Chapter 10 (Sections 10.6 to 10.9), Chapter 12 (geometry alternatives) and Chapter 13.
* **Thermal, cooling and refractory (M4):** Chapter 9 (heat losses), Chapter 13 (Section 13.2) and Chapter 14.
* **Mechanical/structural (M1):** Chapter 13 (Section 13.3) and Chapter 14.

**Workload per member (lead chapters):** M1 – 3, 7, 13.3 · M2 – 10, 12 · M3 – 10.6–10.9, electrode parts of 12/13 · M4 – 13.2, 17, heat losses in 9 · M5 – 6, 8, 9, 11 · M6 – 14, 15, 16, 19, Power BI · PL – 1, 2, 4, 5, 18, 20, and integration.

---

### Chapter 1 – Executive summary (PL)
* **Purpose:** a one-to-two page summary that a manager can read alone.
* **Must contain:** the problem; the approach; the key numbers (55 → 60 MW, PF 0.846 → 0.923, R/X +51 %); the recommended design; the upgrades needed; the cost and payback; the main risks; the decision (feasible / feasible with upgrades / not feasible).
* **Write it last.**

### Chapter 2 – Problem definition (PL)
* **Purpose:** state exactly what problem we are solving.
* **Must contain:** the governing question (docs/00 §0); the brownfield philosophy (retain, optimise, verify); scope in and out (scope change CN-02: economics and mechanical are in scope); constraints (65 MVA fixed, shell/hearth/roof fixed); the success criteria (DC-01 to DC-13).
* **Key point:** the 65 MVA limit forces PF ≥ 0.923, against a typical 0.85.

### Chapter 3 – Existing process description (M1, with M5)
* **Purpose:** describe the reference 55 MW furnace and its process.
* **Must contain:** a process flow description (chromite pellets + reductant + flux → closed SAF → alloy + slag + CO gas); a block flow diagram; the chemistry (main reduction reactions); furnace construction (shell, lining, roof, three Söderberg electrodes, transformers, short network); feed, product and slag; auxiliaries (cooling water, off-gas cleaning, tapping).
* **Starting material:** docs/03 §2 and §5; docs/01 §3.
* **Deliverable:** block flow diagram and furnace cross-section sketch (electrode layout on the PCD).

### Chapter 4 – Design basis (PL, with M6)
* **Purpose:** the fixed basis all calculations rest on.
* **Must contain:** Scenario A and Scenario B definitions; units; standards (IEC 60076-1, IEEE C57.17, IEC 60909, NRS 048-2); the comparison rule (same feed and product in both scenarios); the acceptance criteria table DC-01 to DC-13 with justified limits.
* **Starting material:** docs/00 §6–7; docs/01 §2.

### Chapter 5 – Assumptions (PL, all contribute)
* **Purpose:** the full, justified assumptions register.
* **Must contain:** the table A-01 to A-23 (and any new ones), each with value, justification, reference, confidence, and how it is tested. Highlight the **critical** ones: A-22 (auxiliary margin), A-23 (tap range), A-17 (20 % reactance reduction), A-18 (current calibration).
* **Rule:** this chapter is printed directly from the common register, so it is never retyped.

### Chapter 6 – Literature review (M5 as editor; every member writes their topic)
* **Purpose:** show the technical basis from credible sources.
* **Sections and writers:**
  * 6.1 Ferrochrome production and closed-SAF technology – M5
  * 6.2 SAF electrical theory: resistance, reactance, PF, Westly/Andreae similarity – M2
  * 6.3 Söderberg electrodes, current density, PCD and penetration – M3
  * 6.4 Refractory, cooling and heat losses in ferrochrome furnaces – M4
  * 6.5 Furnace mechanical design and the brownfield uprating approach – M1
  * 6.6 Economic evaluation of furnace upgrades – M6
* **Must contain:** comparison and critique, not just summaries. State where sources disagree (for example, Westly's relation is disputed; the patent current-density limit conflicts with published furnace practice).
* **Rule:** prefer SAIMM, INFACON (pyrometallurgy.co.za), journals and theses. Mark abstract-only sources.

### Chapter 7 – Existing condition calculations (M1, with M2)
* **Purpose:** calculate the 55 MW baseline: the "before" picture.
* **Must contain:** electrical operating point (P, Q, S, PF, I, V, R, X); transformer currents (primary 284 A at 132 kV; winding 69.5 kA); electrode current density; geometry (PCD, spacing, hearth area, power density); production rate; the consistency checks.
* **Starting material:** docs/03 (complete draft) and `calcs/01_reference_furnace.py`.
* **Status:** largely done. Write it up in report form and check it independently.

### Chapter 8 – Mass balance (M5)
* **Purpose:** inputs = outputs for the reference furnace at 55 MW, then at 60 MW.
* **Must contain:** basis (per tonne of alloy, then per day); feed recipe (ore, reductant, flux); element balances for Cr, Fe, Si, C, O, Mg, Al and Ca; alloy, slag and off-gas masses and compositions; Cr recovery; reductant (fixed carbon) requirement; carbon balance; off-gas volume (Nm³/h). The **off-gas volume is needed by M1 and M6** (interface IF-08).
* **Starting material:** feed and slag data in docs/03 §5; the alloy specification (A-01) still needs a reference.
* **Verify in Python.**

### Chapter 9 – Energy balance (M5, with M4 for heat losses)
* **Purpose:** prove the specific energy (MWh/t) instead of assuming it.
* **Must contain:** reaction enthalpies; sensible heat of alloy, slag and off-gas at tapping/exit temperatures; heat losses (cooling water, shell, roof) from M4; the effect of feed preheating (−70 kWh/t per +100 °C [R-04]); the calculated SEC compared with the 3.0–3.5 MWh/t range; the 55 vs 60 MW comparison.
* **Interface:** heat-to-cooling-water results go to M4 for the auxiliary-capacity check (DC-06).

### Chapter 10 – Electrical analysis (M2; M3 writes the electrode sections)
* **Purpose:** show whether, and how, 60 MW fits within 65 MVA.
* **Sections:**
  * 10.1 Equivalent circuit and equations (M2)
  * 10.2 Transformer loading and the PF requirement (PF ≥ 0.923) (M2)
  * 10.3 Operating chart: P versus I with the 65 MVA limit (M2)
  * 10.4 Reactance breakdown: transformer, short network, electrode columns. **Check the implied 16 % transformer reactance against literature** (M2)
  * 10.5 Losses and electrical efficiency (M2)
  * 10.6 Electrode current and current density (M3)
  * 10.7 PCD, electrode spacing and the operating resistance they give (M3)
  * 10.8 Electrode tip position/penetration and its effect on heat distribution (M3)
  * 10.9 Electrode paste consumption and slipping (M3)
* **Starting material:** docs/02 (preliminary results) and `calcs/02_electrical_operating_points.py`.
* **Critical interface:** M2 tells M3 the required resistance (+21 %). M3 must show which geometry **achieves** it (IF-02/IF-03).

### Chapter 11 – Process/metallurgical analysis (M5, with M3 and M4)
* **Purpose:** show the metallurgy stays acceptable at 60 MW.
* **Must contain:** slag chemistry, liquidus and viscosity (basicity 0.83, MgO/Al₂O₃ 0.88); slag–metal separation and tapping; Cr recovery and Cr₂O₃ loss to slag; the effect of shallower electrode tips (a hotter top, a colder hearth) on recovery and SEC; production increase; product quality (Cr, C, Si).
* **Acceptance:** DC-09 (Cr recovery) and DC-10 (SEC).

### Chapter 12 – Development of alternatives (M2 lead, with M3 and PL)
* **Purpose:** compare the different ways of reaching 60 MW.
* **Minimum alternatives:**
  * B0 – raise resistance only (needs 367 V: transformer upgrade)
  * **B20 – reactance −20 % plus resistance +21 % (current preferred)**
  * B30 – mainly reduce reactance
  * Electrode geometry options (PCD/D from 2.7 up to 3.0)
  * Do-nothing / maximum MW without upgrades
  * Optional: secondary-side compensation, or a transformer replacement
* **Must contain:** a comparison matrix of technical criteria (DC-01 to DC-13), cost and risk, and a justified choice.

### Chapter 13 – Detailed calculations for the recommended alternative (all)
* 13.1 Electrical and electrode – M2/M3
* 13.2 Thermal: cooling-water heat removal, refractory heat flux, hearth power density, hot spots – **M4**
* 13.3 Mechanical: shell, roof loading, electrode holders and clamps, electromagnetic forces on conductors – **M1**
* 13.4 Metallurgical (60 MW mass and energy balance) – M5
* **Rule:** each section ends with a **verdict against its DC criterion** (pass, or fail plus mitigation).

### Chapter 14 – Equipment/design requirements (M6 compiles; all contribute)
* **Purpose:** what must be kept, adjusted or bought.
* **Must contain:** the final Retain/Optimise/Upgrade table (EQ-01 to EQ-13); a specification for each Upgrade item (for example transformer tap range ≈ 280–400 V and ≈ 125 kA rating; short-network reactance target; cooling-water capacity); a single-line diagram; the electrode layout.

### Chapter 15 – Economic evaluation (M6, with M1)
* **Purpose:** is the uprate worth doing?
* **Must contain:** capital cost of the Upgrade items (with sources); extra production (≈ +34 t/d) and its value; extra electricity, reductant and electrode paste costs; NPV, payback and IRR; all cost assumptions in the register.

### Chapter 16 – Sensitivity analysis (M6, with all)
* **Purpose:** show how robust the recommendation is.
* **Must vary at least:** A-22 auxiliary margin; A-23 tap range; A-17 achievable reactance reduction; A-18 current calibration (C₃ 6–11); A-04 SEC; electrical efficiency (A-06); electricity price.
* **Output:** tornado chart; the conditions under which the decision changes.

### Chapter 17 – Risk assessment (M4 lead, with all)
* **Purpose:** identify and control the technical and safety risks.
* **Must contain:** a risk register (likelihood × consequence) covering **water leaks into a closed furnace (explosion hazard)**, roof/gas blowouts, electrode breakage, hearth and tap-hole failure, transformer overloading, control instability, Cr recovery loss, and project/cost risks; mitigations; the residual risk.

### Chapter 18 – Recommended design (PL, with M6)
* **Purpose:** the final 60 MW configuration in one place.
* **Must contain:** the operating point (MW, MVA, PF, kA, V); electrode geometry; the upgrades required; performance (production, SEC, recovery); how each DC criterion is met; the feasibility decision.

### Chapter 19 – Implementation plan (M6, with M1 and M2)
* **Purpose:** how the upgrade would be carried out.
* **Must contain:** upgrade sequence and shutdown planning; commissioning steps (stepwise power increase 55 → 57.5 → 60 MW with hold points); operating limits; monitoring KPIs (MVA loading, PF, electrode current, shell/cooling temperatures, Cr recovery, SEC) linked to the Power BI dashboard.

### Chapter 20 – Conclusion (PL)
* **Purpose:** answer the governing question directly.
* **Must contain:** feasible or not; under which conditions; the most important upgrades; the critical assumptions and what should be verified next.

---

## 5. Power BI dashboard (M6) – link to the report

| Dashboard page | Feeds report chapter |
|---|---|
| 01 Overview | 1, 18 |
| 02 Electrical | 10, 12 |
| 03 Electrodes | 10.6–10.9 |
| 04 Metallurgy | 8, 9, 11 |
| 05 Feasibility and constraints | 14, 16, 17 |
| 06 Data provenance | 5 |

All dashboard data comes from `powerbi/`, which is generated from the calculations. No hand-typed engineering values.

---

## 6. Review and checking pairs

| Author | Checks the work of |
|---|---|
| M1 | M4 (thermal) |
| M2 | M3 (electrodes) |
| M3 | M2 (electrical) |
| M4 | M1 (mechanical) |
| M5 | M6 (economics, technical inputs) |
| M6 | M5 (mass and energy balance) |
| PL | Spot checks on all; signs off each gate |

The checker re-derives the key results independently and records "checked by / date" at the end of each chapter.

---

## 7. Gates and order of work

| Gate | What must be ready | Chapters |
|---|---|---|
| **G0** | Everyone has read and accepted this document and the framework | – |
| **G1** | Baseline frozen: RFS, design basis, assumptions, acceptance limits | 2, 3, 4, 5, 7 |
| **G2** | Each member presents their method (inputs, equations, outputs) | 6 (draft), method sections of 8–11 |
| **G3** | Subsystem results calculated and checked | 8, 9, 10, 11, 12, 13 |
| **G4** | One integrated design; all interface values agree | 14 |
| **G5** | Feasibility decision, economics, sensitivity, risk | 15, 16, 17, 18 |
| **G6** | Final report, dashboard, appendices | 1, 19, 20, References, Appendices |

*Dates for each gate are set by the Project Leader and added to this table.*

---

## 8. Immediate actions for each member

| Member | First action |
|---|---|
| **M1** | Review docs/03 (RFS). Close its open items (hearth depth, tap-holes, roof). Start Chapters 3 and 7. |
| **M2** | Review docs/02. Find a published furnace-transformer impedance to test the implied 16 %. Start Chapter 10.1–10.5. |
| **M3** | Find published PCD/penetration–resistance relations (Westly, Andreae/Kelly). Start Chapter 10.6–10.9. |
| **M4** | Propose cooling-water and refractory acceptance limits (DC-06, DC-07). Start the risk register (Chapter 17). |
| **M5** | Find an alloy specification reference (A-01) and a reductant analysis. Set up the mass balance (Chapter 8). Coordinate Chapter 6. |
| **M6** | Build Power BI pages 01, 02 and 06 from `powerbi/`. Set up the economic model structure (Chapter 15). |
| **All** | Read docs/00 and this document. Confirm acceptance at G0. Send new assumptions to the Project Leader for the register. |

---

**Remember:** the aim is a **technically defensible answer** to the governing question. If the honest result is "60 MW is feasible only with upgrades X and Y", or "the safe maximum is Z MW", that is a successful project outcome.
