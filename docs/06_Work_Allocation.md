# WORK ALLOCATION: WHO DOES WHAT (Rev 1 – balanced)

**Project:** Design and Scale-Up of a Closed Ferrochrome SAF from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Tebogo Motsemme (Project Leader)
**Document:** 06 (Rev 1), 2026-11-18. **Replaces Rev 0 and the earlier group arrangement.**
**Governs:** where documents 00 to 05 name a lead for a chapter, **this document takes precedence**.

---

## 1. Final allocation: every member carries the same load

| Member | Lead chapters | Effort points* | Starts early with |
|---|---|---|---|
| **Tebogo Motsemme** | 15 Economic evaluation · 16 Sensitivity analysis · 17 Risk assessment | **7** | 17 (risk register) |
| **Jeff** | 2 Problem definition · 7 Existing condition calculations · 10 Electrical analysis | **7** | 2 and 7 |
| **Mkhonto** | 5 Assumptions · 8 Mass balance · 9 Energy balance | **7** | 5 and 8 |
| **Ngesi** | 6 Literature review (editor) · 11 Process/metallurgical analysis · 12 Development of alternatives | **7** | 6 |
| **Sibandze** | 4 Design basis · 13 Detailed calculations · 14 Equipment/design requirements | **7** | 4 |
| **Simphiwe** | 1 Executive summary · 3 Existing process description · 18 Recommended design · 19 Implementation plan · 20 Conclusion | **7** | 3 |

\*Effort points per chapter: Low = 1, Medium = 2, High = 3, Very high = 4 (Section 3). **All 20 chapters are allocated once, and the 42 points total are split exactly 7 per person.**

**Everyone also:**
* writes **one literature sub-section** for Chapter 6 (Section 5);
* contributes **at least three risks** to Chapter 17;
* names the input values for the sensitivity analysis (Chapter 16) from their own chapter;
* checks one other member's work (Section 6).

**Tebogo additionally** keeps the common registers and Python calculations, runs the gate reviews, builds the Power BI dashboard and does the final edit. These are leader duties and are not counted in the 7 points.

---

## 2. What was wrong with the previous arrangement, and what changed

| Member | Previous chapters | Previous effort | New chapters | New effort |
|---|---|---|---|---|
| Motsemme | 3, 15, 16, 17 | 9 | 15, 16, 17 | 7 |
| Ngesi | 2, 6, 12, 19 | 7 | 6, 11, 12 | 7 |
| Simphiwe | 1, 18, 20 | **4** | 1, 3, 18, 19, 20 | 7 |
| Sibandze | 4, 5, 14 | **5** | 4, 13, 14 | 7 |
| Jeff | 7, 10, 11, 13 | **11** | 2, 7, 10 | 7 |
| Mkhonto | 7, 8, 9, 13 | **11** | 5, 8, 9 | 7 |

**Problems fixed:**
1. **Duplicates:** Chapters **7** and **13** were given to both Jeff and Mkhonto. Two people writing the same chapter causes conflicting numbers. Now **every chapter has exactly one lead**.
2. **Uneven load:** effort ranged from **4 to 11 points**. Jeff and Mkhonto carried four of the six heavy calculation chapters (8, 9, 10, 13) between them. Now **everyone has 7 points**.
3. **Work spread across the whole project:** Chapters 1, 18 and 20 can only be finalised at the end. The integration role therefore also includes **Chapter 3** (at the start) and **Chapter 19** (implementation), so every member has work in every phase.
4. **Logical grouping:** related chapters now sit with one person, so the hand-overs are simpler:
   * Mkhonto: assumptions + mass balance + energy balance (one consistent set of numbers).
   * Jeff: problem definition + baseline calculations + electrical analysis (the core electrical argument).
   * Ngesi: literature + process analysis + alternatives.
   * Sibandze: design basis + detailed calculations + equipment requirements (the design itself).
   * Tebogo: economics + sensitivity + risk (the decision evaluation).
   * Simphiwe: design integration and reporting: process description, the recommended design that combines everyone's results, the implementation plan, and the executive summary and conclusion.
5. **Continuity:** as many previous chapters as possible are kept, so work already started is not lost. Each member keeps at least one previous chapter.

---

## 3. All 20 chapters at a glance

| Ch. | Section | Lead | Supported by | Effort | Gate |
|---|---|---|---|---|---|
| 1 | Executive summary | **Simphiwe** | Tebogo | Low (1) | G6 |
| 2 | Problem definition | **Jeff** | Tebogo | Low (1) | G1 |
| 3 | Existing process description | **Simphiwe** | Mkhonto (chemistry), Jeff | Medium (2) | G1 |
| 4 | Design basis | **Sibandze** | Tebogo | Medium (2) | G1 |
| 5 | Assumptions | **Mkhonto** | Everyone sends new assumptions to Tebogo for the register | Low (1) | G1 |
| 6 | Literature review | **Ngesi** (editor) | Everyone writes one sub-section | Medium (2) | G2 |
| 7 | Existing condition calculations | **Jeff** | Sibandze | Medium (2) | G1 |
| 8 | Mass balance | **Mkhonto** | – | High (3) | G3 |
| 9 | Energy balance | **Mkhonto** | Sibandze (heat losses) | High (3) | G3 |
| 10 | Electrical analysis (incl. electrodes) | **Jeff** | Ngesi (electrode geometry options) | Very high (4) | G3 |
| 11 | Process/metallurgical analysis | **Ngesi** | Mkhonto | Medium (2) | G3 |
| 12 | Development of alternatives | **Ngesi** | Jeff | High (3) | G3 |
| 13 | Detailed calculations | **Sibandze** | Jeff (13.1 electrical), Mkhonto (13.4 metallurgical) | High (3) | G3 |
| 14 | Equipment/design requirements | **Sibandze** | All | Medium (2) | G4 |
| 15 | Economic evaluation | **Tebogo** | Mkhonto (production), Sibandze (upgrade list) | High (3) | G5 |
| 16 | Sensitivity analysis | **Tebogo** | All (input ranges) | Medium (2) | G5 |
| 17 | Risk assessment | **Tebogo** | All (three risks each) | Medium (2) | G5 |
| 18 | Recommended design | **Simphiwe** | Sibandze, Ngesi, Tebogo | Medium (2) | G5 |
| 19 | Implementation plan | **Simphiwe** | Sibandze | Low (1) | G6 |
| 20 | Conclusion | **Simphiwe** | Tebogo | Low (1) | G6 |
| – | References | **Ngesi** (as literature editor) | All | – | G6 |
| – | Appendices | **Tebogo** (calculation printouts, registers) | All | – | G6 |

---

## 4. Task cards

### Tebogo Motsemme – Ch. 15, 16, 17 (+ leader duties)
* **Ch. 15 Economic evaluation:** capital cost of the Upgrade items; value of the extra production (about +34 t/d); extra electricity, reductant and paste costs; NPV, payback and IRR.
* **Ch. 16 Sensitivity analysis:** vary the critical assumptions (A-22 auxiliary margin, A-23 tap range, A-17 reactance reduction, A-18 C₃, A-04 SEC, electricity price); tornado chart; when does the decision change?
* **Ch. 17 Risk assessment:** risk register (likelihood × consequence), including the **water-leak explosion hazard** in a closed furnace. Collect three risks from each member.
* **Leader:** registers, Python calculations, gate reviews, Power BI, Appendices, final edit.
* **Receives:** production (Mkhonto), upgrade list (Sibandze), risks (all).
* **Read:** R-05; gaps G-08, G-09 (cost and price data).
* **First step:** set the gate dates (Section 8) and start the risk register.

### Jeff – Ch. 2, 7, 10
* **Ch. 2 Problem definition:** the governing question; brownfield philosophy (retain, optimise, verify); constraints; why 65 MVA forces PF ≥ 0.923 (from docs 00 and 01).
* **Ch. 7 Existing condition calculations:** turn the Reference Furnace Specification (doc 03) into report form: electrical operating point, transformer currents, electrode current density, geometry, production, consistency checks. Close the open items (hearth depth, tap-holes).
* **Ch. 10 Electrical analysis:** equivalent circuit; transformer loading; operating chart; reactance breakdown (check the implied 16 % transformer reactance); losses; electrode current density; how PCD and electrode tip position give the required +21 % resistance; paste consumption.
* **Hands over:** required R, X, current and voltage to Ngesi, Sibandze and Mkhonto (by G2).
* **Read first:** **R-13** (most important), R-01, R-02, R-14, R-15, R-08, R-09.
* **First step:** confirm the 48 MW / 1.55 m / 110 kA values in R-13; review docs 02 and 03.

### Mkhonto – Ch. 5, 8, 9
* **Ch. 5 Assumptions:** the full assumptions table from the common register (A-01 to A-23 and any new ones), plus an explanation of the four critical assumptions. Coordinate with Tebogo, who keeps the master register.
* **Ch. 8 Mass balance:** per tonne of alloy, then per day at 55 and 60 MW; Cr, Fe, Si, C and O balances; alloy, slag and off-gas; Cr recovery; reductant requirement.
* **Ch. 9 Energy balance:** calculate the specific energy (MWh/t) instead of assuming it; reaction heats; sensible heat of products; heat losses (from Sibandze); the preheating effect.
* **Hands over:** production, slag and off-gas volumes to Ngesi, Sibandze and Tebogo; heat to cooling water to Sibandze (by G3).
* **Read first:** **R-18** (confirm the feed analysis), R-19, R-20, R-04, R-05, R-07; find R-10 (alloy specification) and thermodynamic data (G-07).
* **First step:** confirm the LG6 analysis and find a charge-chrome alloy specification.

### Ngesi – Ch. 6, 11, 12 (+ References)
* **Ch. 6 Literature review:** edit the six sub-sections into one critical review, and write sub-section 6.3 yourself.
* **Ch. 11 Process/metallurgical analysis:** slag chemistry (basicity 0.83, MgO/Al₂O₃ 0.88); slag–metal separation; Cr recovery; the effect of shallower electrode tips; product quality.
* **Ch. 12 Development of alternatives:** compare B0 (resistance only, 367 V), **B20 (reactance −20 % and resistance +21 %)**, B30, PCD options (PCD/D 2.7 to 3.0), and "do nothing / maximum MW". Use a comparison matrix against the acceptance criteria, then make a justified choice.
* **References:** one Harvard-style list of all sources used (from doc 05).
* **Read first:** doc 05 (whole), R-16, R-17, R-03, R-19, R-20.
* **First step:** send each member their literature sub-section and a deadline.

### Sibandze – Ch. 4, 13, 14
* **Ch. 4 Design basis:** Scenario A and Scenario B definitions; units; standards (IEC 60076-1, IEEE C57.17, IEC 60909, NRS 048-2); the acceptance criteria DC-01 to DC-13 with justified limits (from docs 00 and 01).
* **Ch. 13 Detailed calculations for the chosen alternative:** thermal (cooling-water heat removal, refractory heat flux, hearth power density 0.59 → 0.65 MW/m²) and mechanical (shell, roof, electrode holders, conductor forces). Collect Jeff's 13.1 and Mkhonto's 13.4. End each section with a pass/fail verdict against its criterion.
* **Ch. 14 Equipment/design requirements:** the final Retain/Optimise/Upgrade table (EQ-01 to EQ-13) and a specification for each upgrade.
* **Hands over:** heat losses to Mkhonto (Ch. 9); the upgrade list to Tebogo and Simphiwe (by G4).
* **Read first:** R-11, R-16, R-17; refractory and cooling data (gaps G-04 to G-06); standards.
* **First step:** write Chapter 4 from doc 00 §6–7; propose the cooling (DC-06) and refractory (DC-07) limits.

### Simphiwe – Ch. 1, 3, 18, 19, 20 (design integration and reporting)
* **Ch. 3 Existing process description:** the reference 55 MW furnace and its process (chromite pellets + reductant + flux → closed SAF → alloy + slag + CO gas); the main reduction reactions; furnace construction (shell, lining, roof, three Söderberg electrodes, transformers, short network); feed, product and slag; auxiliaries. Include a block flow diagram and an electrode layout sketch on the pitch circle. Based on doc 03; chemistry agreed with Mkhonto.
* **Ch. 19 Implementation plan:** the steps to carry out the upgrade: (1) order equipment; (2) shutdown and installation; (3) commissioning; (4) raise power in steps 55 → 57.5 → 60 MW with checks; (5) KPIs to monitor (MVA loading, PF, electrode current, cooling temperatures, Cr recovery, energy use). Use Sibandze's upgrade list.
* **Ch. 18 Recommended design:** one chapter that brings the chosen design together: operating point (MW, MVA, PF, kA, V), electrode geometry, upgrades, performance, and how each acceptance criterion is met. Take it from Ngesi's Ch. 12, Sibandze's Ch. 13–14 and Tebogo's Ch. 15–17.
* **Ch. 1 Executive summary and Ch. 20 Conclusion:** finalised last. They state the problem, approach, key numbers, recommendation, cost, risks and the feasibility decision, and answer the governing question directly.
* **Receives:** chosen alternative (Ngesi), upgrade list (Sibandze), economics, sensitivity and risk (Tebogo).
* **Read first:** docs 00, 03 and 05; R-06, R-11, R-02.
* **First step:** draft Chapter 3 from doc 03 and set up the structure of Chapter 18 so each member knows which results it needs from them.

---

## 5. Literature review (Chapter 6): one sub-section each

| Sub-section | Topic | Writer | Main sources |
|---|---|---|---|
| 6.1 | Ferrochrome production and closed-furnace technology | Mkhonto | R-05, R-06, R-07, R-18 |
| 6.2 | SAF electrical theory: resistance, reactance, PF, Westly scale-up | Jeff | R-01, R-02, R-03, R-12, R-13, R-14 |
| 6.3 | Söderberg electrodes, current density and furnace geometry | Ngesi | R-08, R-09, R-16, R-17 |
| 6.4 | Refractory, cooling and heat losses | Sibandze | R-11 + gaps G-04 to G-06 |
| 6.5 | Brownfield furnace uprating and process description | Simphiwe | R-06, R-11 |
| 6.6 | Economic evaluation and risk in furnace upgrades | Tebogo | Gaps G-08, G-09 |
| – | Editing and critical comparison | Ngesi | All |

About 1–2 pages each. **Compare** the sources and point out disagreements; don't just summarise.

---

## 6. Checking pairs (everyone checks someone)

| Author | Work checked by | Why this pair |
|---|---|---|
| Jeff (2, 7, 10) | Sibandze | Sibandze uses Jeff's electrical results in Ch. 13 |
| Sibandze (4, 13, 14) | Jeff | Jeff supplies section 13.1 |
| Mkhonto (5, 8, 9) | Ngesi | Ngesi uses the mass balance in Ch. 11 |
| Ngesi (6, 11, 12) | Mkhonto | Mkhonto supplies the metallurgical inputs |
| Simphiwe (1, 3, 18, 19, 20) | Tebogo | Ch. 18 integrates every member's results; leader sign-off |
| Tebogo (15, 16, 17) | Simphiwe | Simphiwe uses these results in Ch. 18 |

The checker re-calculates the key results independently and signs "checked by / date" at the end of the chapter.

---

## 7. Who hands what to whom

| From | To | What | By gate |
|---|---|---|---|
| Tebogo | All | Frozen baseline (doc 03), registers, this allocation | G1 |
| Jeff | Ngesi, Sibandze, Mkhonto | Required R, X, current, voltage; electrode tip position and PCD | G2 / G3 |
| Mkhonto | Ngesi, Sibandze, Tebogo | Production rate, slag and off-gas volumes, specific energy | G3 |
| Sibandze | Mkhonto | Heat losses (cooling water, shell, roof) | G3 |
| Ngesi | Sibandze, Simphiwe | Chosen alternative (Ch. 12) | G3 |
| Sibandze | Tebogo, Simphiwe | Final upgrade list (Retain/Optimise/Upgrade) | G4 |
| Tebogo | Simphiwe | Economics, sensitivity and risk results | G5 |
| Everyone | Tebogo | New assumptions (as they arise); three risks each | Ongoing / G5 |

---

## 8. Gate dates (to be set by Tebogo)

| Gate | What is due | Date |
|---|---|---|
| G0 | Everyone accepts this allocation | ____ |
| G1 | Ch. 2, 3, 4, 5, 7 drafts; baseline frozen | ____ |
| G2 | Ch. 6 sub-sections; each person presents their method | ____ |
| G3 | Ch. 8 to 13 calculated and checked | ____ |
| G4 | Ch. 14; one integrated design | ____ |
| G5 | Ch. 15 to 18; feasibility decision | ____ |
| G6 | Ch. 1, 19, 20, References, Appendices; final report | ____ |

**Rules reminder:** use the common numbers (doc 04 §2); tag every number [S]/[L]/[A]/[C]; send new assumptions to Tebogo; never present assumed values as plant data; if 60 MW doesn't work for your part, say so. That is a valid result.
