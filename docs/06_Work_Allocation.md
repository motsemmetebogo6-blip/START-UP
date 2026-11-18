# WORK ALLOCATION: WHO DOES WHAT (Rev 6)

**Project:** Design and Scale-Up of a Closed Ferrochrome SAF from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Tebogo Motsemme (Project Leader)
**Document:** 06 (Rev 6), 2026-11-18. **Replaces all previous allocations.** *Proposed after Mkhonto's request; to be confirmed by Tebogo before circulation.*
**Governs:** where documents 00 to 05 name a lead for a chapter, **this document takes precedence**.

---

## 1. Final allocation

| Member | Lead chapters | Effort points* |
|---|---|---|
| **Tebogo Motsemme** | 4 Design basis · 7 Existing condition calculations · 12 Development of alternatives | **7** |
| **Jeff** | 2 Problem definition · 10 Electrical analysis · 13 Detailed calculations | **8** |
| **Mkhonto** | 5 Assumptions · 6 Literature review (editor) · 8 Mass balance | **6** |
| **Ngesi** | 9 Energy balance · 11 Process/metallurgical analysis · 19 Implementation plan · 20 Conclusion | **7** |
| **Sibandze** | 14 Equipment/design requirements · 15 Economic evaluation · 18 Recommended design | **7** |
| **Simphiwe** | 1 Executive summary · 3 Existing process description · 16 Sensitivity analysis · 17 Risk assessment | **7** |

\*Effort points per chapter: Low = 1, Medium = 2, High = 3, Very high = 4. **All 20 chapters are allocated once (42 points).** There is no separate "compiler" any more: Chapters 1, 18 and 20 are normal chapters with their own leads.

**Final assembly of the report** (merging chapters into one Word file, formatting, contents page, figure and table numbering) is part of **Tebogo's** leader duties, together with the registers, Python calculations, gate reviews, Power BI, Appendices and final edit (not counted).

**Everyone also:**
* writes **one literature sub-section** for Chapter 6 (Section 4);
* gives Simphiwe **three risks** for Chapter 17 and the **input ranges** from their own chapter for Chapter 16;
* submits their chapters in the **common template** (Tebogo issues it), so assembly is quick;
* checks one other member's work (Section 5).

---

## 2. All chapters at a glance

| Ch. | Section | Lead | Supported by | Effort | Gate |
|---|---|---|---|---|---|
| 1 | Executive summary | **Simphiwe** | All | Low (1) | G6 |
| 2 | Problem definition | **Jeff** | Tebogo | Low (1) | G1 |
| 3 | Existing process description | **Simphiwe** | Mkhonto (chemistry) | Medium (2) | G1 |
| 4 | Design basis | **Tebogo** | Sibandze | Medium (2) | G1 |
| 5 | Assumptions | **Mkhonto** | Everyone sends new assumptions to Tebogo for the register | Low (1) | G1 |
| 6 | Literature review | **Mkhonto** (editor) | Everyone writes one sub-section | Medium (2) | G2 |
| 7 | Existing condition calculations | **Tebogo** | Jeff | Medium (2) | G1 |
| 8 | Mass balance | **Mkhonto** | Ngesi | High (3) | G3 |
| 9 | Energy balance | **Ngesi** | Mkhonto (mass balance), Jeff (heat losses) | High (3) | G3 |
| 10 | Electrical analysis (incl. electrodes) | **Jeff** | – | Very high (4) | G3 |
| 11 | Process/metallurgical analysis | **Ngesi** | Mkhonto | Medium (2) | G3 |
| 12 | Development of alternatives | **Tebogo** | Jeff, Ngesi | High (3) | G3 |
| 13 | Detailed calculations | **Jeff** | Ngesi (13.4 metallurgical) | High (3) | G3 |
| 14 | Equipment/design requirements | **Sibandze** | Jeff, all | Medium (2) | G4 |
| 15 | Economic evaluation | **Sibandze** | Mkhonto, Ngesi (production), Tebogo (chosen alternative) | High (3) | G5 |
| 16 | Sensitivity analysis | **Simphiwe** | All (input ranges); Tebogo (Python model) | Medium (2) | G5 |
| 17 | Risk assessment | **Simphiwe** | All (three risks each) | Medium (2) | G5 |
| 18 | Recommended design | **Sibandze** | Tebogo, Jeff, Ngesi | Medium (2) | G5 |
| 19 | Implementation plan | **Ngesi** | Sibandze | Low (1) | G6 |
| 20 | Conclusion | **Ngesi** | Tebogo | Low (1) | G6 |
| – | References | **Mkhonto** (as literature editor) | All | – | G6 |
| – | Appendices and final assembly | **Tebogo** | All | – | G6 |

---

## 3. Task cards

### Tebogo Motsemme – Ch. 4, 7, 12 (+ leader duties and final assembly)
* **Ch. 4 Design basis:** Scenario A and Scenario B; units; standards (IEC 60076-1, IEEE C57.17, IEC 60909, NRS 048-2); acceptance criteria DC-01 to DC-13 with justified limits.
* **Ch. 7 Existing condition calculations:** the 55 MW baseline in report form (from doc 03): electrical operating point, transformer currents, electrode current density, geometry, production, consistency checks; close the open items (hearth depth, tap-holes).
* **Ch. 12 Development of alternatives:** compare **B0** (raise resistance only; needs 367 V, so a transformer upgrade), **B20** (reactance −20 % plus resistance +21 %), **B30** (mainly reduce reactance), PCD options (PCD/D 2.7 to 3.0), and "do nothing / maximum MW". Comparison matrix against DC-01 to DC-13, cost and risk; justified choice.
* **Leader:** registers, Python calculations, gate reviews, Power BI, Appendices, **chapter template and final assembly of the report**.
* **Read first:** docs 00, 01, 02, 03; R-02, R-11, R-13, R-14, R-15; standards.
* **First step:** issue the chapter template, set the gate dates (Section 7) and draft Ch. 4 and 7 for G1.

### Jeff – Ch. 2, 10, 13
* **Ch. 2 Problem definition:** the governing question; brownfield philosophy (retain, optimise, verify); constraints; why 65 MVA forces PF ≥ 0.923.
* **Ch. 10 Electrical analysis:** equivalent circuit; transformer loading; operating chart; reactance breakdown (check the implied 16 % transformer reactance); losses; electrode current density; how PCD and electrode tip position give the required +21 % resistance; paste consumption.
* **Ch. 13 Detailed calculations for the chosen alternative:** electrical (13.1), thermal (cooling-water heat removal, refractory heat flux, hearth power density 0.59 → 0.65 MW/m²) and mechanical (shell, roof, electrode holders, conductor forces). Collect Ngesi's 13.4 metallurgical section. End each section with a pass/fail verdict.
* **Hands over:** required R, X, current and voltage to Tebogo, Ngesi and Sibandze (by G2); heat losses to Ngesi (Ch. 9); detailed results to Sibandze for Ch. 14 and 18 (by G3).
* **Read first:** **R-13** (most important), R-01, R-02, R-14, R-15, R-08, R-09, R-11, R-17; refractory and cooling data (gaps G-04 to G-06).
* **First step:** draft Ch. 2 for G1 (from docs 00 and 01); confirm the 48 MW / 1.55 m / 110 kA values in R-13.

### Mkhonto – Ch. 5, 6, 8 (+ References)
* **Ch. 5 Assumptions:** the full assumptions table from the common register, with an explanation of the four critical assumptions (A-17, A-18, A-22, A-23). Tebogo keeps the master register.
* **Ch. 6 Literature review:** edit the six sub-sections into one critical review, and write sub-section 6.1 yourself.
* **Ch. 8 Mass balance:** per tonne of alloy, then per day at 55 and 60 MW; Cr, Fe, Si, C and O balances; alloy, slag and off-gas; Cr recovery; reductant requirement.
* **References:** one Harvard-style list of every source used (from doc 05).
* **No compiling:** final assembly of the report is done by Tebogo.
* **Hands over:** mass balance to Ngesi (early G3); production, slag and off-gas volumes to Sibandze and Tebogo.
* **Read first:** doc 05 (whole), **R-18** (confirm the feed analysis), R-19, R-20; find R-10 (alloy specification).
* **First step:** send each member their literature sub-section and a deadline; confirm the LG6 analysis.

### Ngesi – Ch. 9, 11, 19, 20
* **Ch. 9 Energy balance:** calculate the specific energy (MWh/t) instead of assuming it; reaction heats; sensible heat of alloy, slag and gas; heat losses (from Jeff); preheating effect; 55 vs 60 MW.
* **Ch. 11 Process/metallurgical analysis:** slag chemistry (basicity 0.83, MgO/Al₂O₃ 0.88); slag–metal separation; Cr recovery; the effect of shallower electrode tips; product quality.
* **Ch. 19 Implementation plan:** equipment ordering; shutdown and installation; commissioning; power raised in steps 55 → 57.5 → 60 MW with hold points; KPIs to monitor.
* **Ch. 20 Conclusion:** answers the governing question directly: feasible or not, under which conditions, the critical upgrades and assumptions, and what should be verified next.
* **Hands over:** specific energy to Sibandze and Tebogo; section 13.4 to Jeff (by G3).
* **Read first:** R-04, R-05, R-07, R-19, R-20; thermodynamic data (gap G-07).
* **First step:** set up the energy-balance method and thermodynamic data while Mkhonto starts the mass balance.

### Sibandze – Ch. 14, 15, 18
* **Ch. 14 Equipment/design requirements:** the final Retain/Optimise/Upgrade table (EQ-01 to EQ-13) and a specification for each upgrade (transformer tap range and current rating, short-network reactance target, cooling-water and off-gas capacity), based on Jeff's Ch. 13.
* **Ch. 15 Economic evaluation:** capital cost of the Upgrade items; value of the extra production (about +34 t/d); extra electricity, reductant and paste costs; NPV, payback and IRR.
* **Ch. 18 Recommended design:** the chosen design in one place: operating point (MW, MVA, PF, kA, V), electrode geometry, upgrades, performance (production, SEC, recovery), cost, and how each acceptance criterion is met (from Ch. 12–17).
* **Hands over:** upgrade list to Ngesi (Ch. 19) and Simphiwe (Ch. 17); economic results to Simphiwe (Ch. 16); recommended design to Simphiwe (Ch. 1) and Ngesi (Ch. 20).
* **Read first:** R-05; standards; cost and price data (gaps G-08, G-09).
* **First step:** collect cost data (transformers, busbars, cooling upgrades, electricity tariff, ferrochrome price) and set up the economic model.

### Simphiwe – Ch. 1, 3, 16, 17
* **Ch. 3 Existing process description:** the reference 55 MW furnace and its process; main reduction reactions; furnace construction (shell, lining, roof, three Söderberg electrodes, transformers, short network); feed, product and slag; auxiliaries; block flow diagram and electrode layout on the pitch circle. Chemistry agreed with Mkhonto.
* **Ch. 16 Sensitivity analysis:** vary the critical assumptions (A-22 auxiliary margin, A-23 tap range, A-17 reactance reduction, A-18 C₃, A-04 SEC, electricity price); tornado chart; the conditions under which the decision changes. Tebogo supplies the Python model.
* **Ch. 17 Risk assessment:** risk register (likelihood × consequence → score, mitigation, owner, residual risk), including the **water-leak explosion hazard**, roof/gas blow-outs, electrode breakage, tap-hole failure, transformer overloading, control instability, Cr recovery loss, cost and schedule risks. Collect three risks from each member.
* **Ch. 1 Executive summary:** 1–2 pages covering the problem, approach, key numbers, recommendation, cost, risks and decision, finalised once Ch. 18 and 20 are complete.
* **Read first:** docs 00 and 03; R-02, R-06, R-11.
* **First step:** draft Chapter 3 from doc 03 and send the team the risk-register template.

---

## 4. Literature review (Chapter 6): one sub-section each

| Sub-section | Topic | Writer | Main sources |
|---|---|---|---|
| 6.1 | Ferrochrome production and closed-furnace technology | Mkhonto | R-05, R-06, R-07, R-18 |
| 6.2 | SAF electrical theory: resistance, reactance, PF, Westly scale-up | Tebogo | R-01, R-02, R-03, R-12, R-13, R-14 |
| 6.3 | Söderberg electrodes, current density and furnace geometry | Ngesi | R-08, R-09, R-16, R-17 |
| 6.4 | Refractory, cooling and heat losses | Jeff | R-11 + gaps G-04 to G-06 |
| 6.5 | Furnace safety and risk in closed SAFs | Simphiwe | R-06, R-11 + safety literature |
| 6.6 | Economic evaluation of furnace upgrades | Sibandze | R-15 + gaps G-08, G-09 |
| – | Editing and critical comparison | Mkhonto | All |

---

## 5. Checking pairs

| Author | Checked by | Why this pair |
|---|---|---|
| Jeff (2, 10, 13) | Sibandze | Sibandze builds Ch. 14 and 18 on Jeff's calculations |
| Sibandze (14, 15, 18) | Jeff | Jeff supplies the design results the equipment, costs and recommendation are based on |
| Mkhonto (5, 6, 8) | Ngesi | Ngesi's energy balance is built on the mass balance |
| Ngesi (9, 11, 19, 20) | Mkhonto | Mkhonto supplies the mass balance |
| Tebogo (4, 7, 12) | Simphiwe | Simphiwe's sensitivity analysis tests Tebogo's basis and choice |
| Simphiwe (1, 3, 16, 17) | Tebogo | Tebogo supplies the Python model for Ch. 16 |

---

## 6. Who hands what to whom

| From | To | What | By gate |
|---|---|---|---|
| Tebogo | All | Frozen baseline (doc 03), design basis, registers, chapter template, this allocation | G1 |
| Jeff | Tebogo, Ngesi, Sibandze | Required R, X, current, voltage; electrode tip position and PCD | G2 / G3 |
| Mkhonto | Ngesi | Mass balance (alloy, slag, gas per tonne) | early G3 |
| Mkhonto, Ngesi | Sibandze, Tebogo | Production rate, slag and off-gas volumes, specific energy | G3 |
| Jeff | Ngesi | Heat losses (cooling water, shell, roof) | G3 |
| Tebogo | Jeff, Sibandze, Simphiwe, Ngesi | Chosen alternative (Ch. 12) | G3 |
| Jeff | Sibandze | Detailed calculation results (Ch. 13) | G3 |
| Sibandze | Ngesi, Simphiwe, Tebogo | Upgrade list, economic results, recommended design (Ch. 18) | G4 / G5 |
| Everyone | Simphiwe | Three risks each; sensitivity input ranges | G5 |
| All members | Tebogo | Checked chapters in the common template, for final assembly | G6 |

---

## 7. Gate dates (to be set by Tebogo)

| Gate | What is due | Date |
|---|---|---|
| G0 | Everyone accepts this allocation | ____ |
| G1 | Ch. 2, 3, 4, 5, 7 drafts; baseline frozen | ____ |
| G2 | Ch. 6 sub-sections; each person presents their method | ____ |
| G3 | Ch. 8 to 13 calculated and checked | ____ |
| G4 | Ch. 14; one integrated design | ____ |
| G5 | Ch. 15 to 18; feasibility decision | ____ |
| G6 | Ch. 1, 19, 20, References, Appendices; Tebogo assembles the final report | ____ |

**Rules reminder:** use the common numbers (doc 04 §2); tag every number [S]/[L]/[A]/[C]; send new assumptions to Tebogo; never present assumed values as plant data; if 60 MW doesn't work for your part, say so. That is a valid result.
