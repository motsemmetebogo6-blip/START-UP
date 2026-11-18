# LITERATURE AND EVIDENCE MAP: where our basis information comes from

**Project:** Design and Scale-Up of a Closed Ferrochrome SAF from 55 MW to 60 MW Using 65 MVA Transformers and Optimised Electrode Geometry
**Issued by:** Project Leader **To:** All team members (M1 to M6)
**Document:** 05 (Rev 0), 2026-11-18
**Purpose:** answers the team's question *"where does the information in the basis documents come from?"*. For every article it gives the link, **what we took from it**, **where we used it**, **who must read it**, and **what still has to be checked**.

> **Honest status:** the values from these sources were taken from abstracts and search excerpts. The full papers could not be downloaded from the project's working environment because its network blocks these sites. **Each member must download the papers for their chapters (links below) and confirm our values against the full text**, using the checklist in Section 5. Until then, the sources are marked **"abstract only"** and must not be cited in the final report as fully verified.

---

## 1. Quick guide: which papers each member must read

| Member | Must read (reference numbers) | Mainly for chapters |
|---|---|---|
| **M1** – furnace and mechanical | R-06, **R-11**, R-16, R-17 | 3, 7, 13.3 |
| **M2** – electrical | **R-01**, **R-02**, R-03, R-12, **R-13**, **R-14**, **R-15**, standards | 6.2, 10.1–10.5, 12 |
| **M3** – electrodes | R-01, R-03, **R-08**, **R-09**, R-13, **R-16**, **R-17** | 6.3, 10.6–10.9 |
| **M4** – thermal and refractory | R-04, R-11, R-17 (+ gaps G-04 to G-06) | 6.4, 9, 13.2, 17 |
| **M5** – metallurgy | **R-04**, **R-05**, **R-07**, R-10, **R-18**, **R-19**, **R-20** | 6.1, 8, 9, 11 |
| **M6** – economics and Power BI | R-05 (+ gaps G-08, G-09) | 6.6, 15, 16 |
| **PL** – Project Leader | All (audit) | 2, 4, 5 |

**Bold** = the most important source for that member, because a key design number depends on it.

---

## 2. The articles: what we took and where we used it

**How to read each entry:**
* **Link** – where to download it.
* **Access** – Free = free PDF; Login = free account or request from the author; Library = through the university library.
* **What we took** – the exact information or values we used.
* **Where used** – document and section, assumption ID, report chapter.
* **Check** – what the member must confirm in the full text.

### 2.1 Electrical theory and scale-up

#### R-01 – Westly, J. (1974). *Resistance and heat distribution in a submerged-arc furnace.* Proceedings of INFACON I (First International Ferroalloys Congress).
* **Link:** <https://www.pyrometallurgy.co.za/InfaconI/121-Westly.pdf> (Free)
* **What we took:** the scale-up similarity relation **I = C₃ · P^(2/3)** and **V = P^(1/3) / C₃** (I in kA, P in MW), with C₃ constant for a given process.
* **Where used:** docs/02 §1–2 (calibration of the baseline current); docs/03 §3.2 (electrode current 120.5 kA); assumptions A-08 and A-18; report Chapters 6.2 and 10.
* **Who:** M2 (lead), M3.
* **Check:** the exact form of the equation; whether P is total furnace MW or per phase; the units; any table of C₃ values for ferrochrome; Westly's resistance relations for electrode diameter and PCD (needed by M3 to turn the required +21 % resistance into geometry).

#### R-02 – Mulholland, A.C. (2009). *The effectiveness of current control of submerged arc furnace electrode penetration in selected scenarios.* Journal of the SAIMM, 109(10).
* **Link:** <https://scielo.org.za/pdf/jsaimm/v109n10/04.pdf> (Free)
* **What we took:** a power factor of **≈ 0.85 is typical of an average-sized ferrochrome furnace**, and larger modern furnaces run lower. Resistance control is better than current control because the electrodes interact electrically.
* **Where used:** docs/01 A-05 and §7.3 (the critical PF finding); docs/02 §1 (model limitations); docs/03 §6 (consistency check); acceptance criterion DC-12 (stability); Chapters 6.2, 10, 17.
* **Who:** M2.
* **Check:** the exact PF and operating point used in the paper; the description of electrode interaction; recommendations for large furnaces.

#### R-03 – ABM Proceedings (2007). *Correlação entre tensão ideal, potência e diâmetro de eletrodos nos fornos a arco submerso – fator J* (in Portuguese).
* **Link:** <https://abmproceedings.com.br/en/article/download-pdf/correlao-entre-tenso-ideal-potncia-e-dimetro-de-eletrodos-nos-fornos-a-arco-submerso-fator-j> (Free)
* **What we took:** a **critique of Westly**: the authors found Westly's relations do not match their data, and that the ideal voltage and current also depend on **electrode diameter and spacing**.
* **Where used:** docs/01 §2 and A-08 (why Westly is used only as a cross-check); Chapter 6.2 (critical review).
* **Who:** M2, M3.
* **Check:** the authors' alternative "J-factor" relation. It may be the better tool for M3's geometry calculation.

#### R-12 – Reported Westly C₃ range for high-carbon ferrochrome: **6 to 11** (secondary sources)
* **Links:**
  * Archives of Metallurgy and Materials (2017) 62(4): <https://www.imim.pl/files/archiwum/Vol4_2017/54.pdf> (Free)
  * SAIMM (2018) *Basic parameters in the operation and design of submerged arc furnaces, with particular reference to production of high-silicon alloys*: <https://www.scielo.org.za/scielo.php?script=sci_arttext&pid=S2225-62532018000600014> (Free)
* **What we took:** C₃ for HC ferrochrome lies between **6 and 11**, with lower values for "a particular group of furnaces".
* **Where used:** docs/02 §2 and §5 (our C₃ = 8.33 lies inside this range; sensitivity C₃ = 6–11); docs/03 §6; A-18; Chapters 10 and 16.
* **Who:** M2.
* **Check:** **which** of the two papers actually states the 6–11 range for ferrochrome. Cite the original source.

#### R-13 – (Author to confirm; probably McDougall) *Finite element modelling of electric currents in AC submerged arc furnaces.*
* **Link:** <https://www.researchgate.net/publication/30509695_Finite_element_modelling_of_electric_currents_in_AC_submerged_arc_furnaces> (Login)
* **What we took:** a **ferrochrome furnace of 48 MW with 1.55 m electrodes at 110 kA**. This is our calibration furnace: C₃ = 110 / 48^(2/3) = **8.33**, and current density = **5.83 A/cm²**.
* **Where used:** docs/02 §2 (calibration of the whole electrical baseline); docs/03 §3.2 and §6; A-07 (revised current-density criterion), A-16, A-18; Chapters 7 and 10.
* **Who:** M2, M3.
* **Check:** ⚠ **The most important check in the project.** The 48 MW, 1.55 m and 110 kA values underpin every electrical number. Confirm them and record the author, year and page.

#### R-14 – (Authors to confirm) (2023). Paper on the SAF short network. *Energies*, 16(21), 7386.
* **Link:** <https://www.mdpi.com/1996-1073/16/21/7386> (Free, open access)
* **What we took:** the power factor of an SAF can **hardly exceed ≈ 0.85**, and **≈ 70 % of the system reactance comes from the short network** (busbars, flexibles, electrodes).
* **Where used:** docs/02 §4.3 (feasibility of the 20 % reactance reduction); docs/03 §3.2 (split of reactance into 0.557 mΩ short network and 0.239 mΩ transformer); A-17; Chapters 10.4 and 12.
* **Who:** M2.
* **Check:** the 70 % figure and how it was obtained; any reactance values in mΩ; any methods for reducing short-network reactance and their effect on PF.

#### R-15 – Stewart, A.B. (1980). *An analysis of the electrical circuit of submerged-arc furnaces.* PhD thesis, University of Cape Town.
* **Link:** <https://open.uct.ac.za/bitstream/11427/14048/1/thesis_ebe_1980_stewart_alistair_bruce.pdf> (Free)
* **What we took:** **not yet used**. It is identified as the main source for busbar and flexible reactance and for the effect of furnace geometry on reactance.
* **Where it will be used:** Chapter 10.4 (reactance breakdown); Chapter 12 (the reactance −20 % alternative); Chapter 13.1.
* **Who:** M2.
* **Check:** methods to calculate short-network reactance from conductor geometry. This is what proves whether the −20 % (A-17) is achievable.

### 2.2 Electrodes and furnace geometry

#### R-08 – US Patent 9,347,108. *Advanced technology for iron-chrome alloys production and related plant.*
* **Link:** <https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9347108> (Free)
* **What we took:** a Söderberg current-density guideline by electrode diameter: **≤ 7 A/cm² for 0.8–1.0 m; 5.5–6 A/cm² for 1.1–1.3 m; 4.5–5 A/cm² above 1.3 m**.
* **Where used:** docs/01 A-07 (original limit); docs/02 §2 (**challenged**: the published furnace R-13 runs at 5.83 A/cm², above this limit, so we replaced the limit with "no higher than the existing furnace"); operating chart; Chapter 6.3.
* **Who:** M3.
* **Check:** the exact wording and units. A patent is not peer-reviewed, so **find a second source** (an Elkem or INFACON paper on Söderberg electrodes).

#### R-09 – Steenkamp, J.D. et al. (2016). Mintek paper (title to confirm).
* **Link:** <https://www.pyrometallurgy.co.za/Mintek/Files/2016Steenkamp3.pdf> (Free)
* **What we took:** McDougall's finding that in a charge-chrome furnace **very little current passes through the charge**; it enters the slag in a relatively small region.
* **Where used:** background to the electrical model (docs/01 §1.1); Chapter 6.2 and Chapter 10.7–10.8 (how electrode tip position changes the resistance).
* **Who:** M3.
* **Check:** the title and authors; what it says about current paths and how the operating resistance depends on electrode penetration.

#### R-16 – (Authors to confirm). *Simulation of the production of ferrochromium in submerged-arc furnace.*
* **Link:** <https://www.researchgate.net/publication/287585366_Simulation_of_the_production_of_ferrochromium_in_submerged-Arc_furnace> (Login)
* **What we took:** a ferrochrome furnace with **hearth diameter 8385 mm, electrode diameter 1350 mm, PCD 3290 mm**, giving **PCD/D = 2.44** and **hearth/PCD = 2.55**.
* **Where used:** docs/03 §4 (PCD 4.19 m and hearth 10.88 m of the reference furnace); A-19, A-20; Chapters 7 and 10.7.
* **Who:** M3, M1.
* **Check:** the dimensions; the furnace power (to judge how similar it is to ours); any power or current data.

#### R-17 – (Authors to confirm) (2024). DEM study of a ferrochrome SAF. *Journal of the SAIMM*, 124(3).
* **Link:** <https://scielo.org.za/pdf/jsaimm/v124n3/06.pdf> (Free)
* **What we took:** **vessel radius 6.00 m, electrode radius 0.75 m, PCD radius 2.25 m**, giving **PCD/D = 3.0** and **hearth/PCD ≈ 2.67**.
* **Where used:** docs/03 §4 (together with R-16 it sets our geometry; PCD/D = 3.0 is the upper limit for the PCD optimisation); A-19, A-20; Chapters 7, 10.7 and 12.
* **Who:** M3, M1.
* **Check:** whether the 6.00 m is the inside of the lining or the shell; burden behaviour near the electrodes (useful for M4).

#### R-11 – (Authors to confirm) (2019). *Wear analysis of tap-holes at two ferrochromium production furnaces.* Journal of the SAIMM, 119(6).
* **Link:** <https://www.scielo.org.za/scielo.php?script=sci_arttext&pid=S2225-62532019000600005> (Free)
* **What we took:** two South African ferrochrome SAFs of **63 MVA** with **13.7 m inner shell diameter** and **three 1.55 m Söderberg electrodes**. This is the "same size" furnace our reference furnace is modelled on.
* **Where used:** docs/03 §1, §4 (shell 13.7 m, electrode 1.55 m); A-16; Chapters 3 and 7.
* **Who:** M1 (and M4 for the tap-hole and refractory information).
* **Check:** all furnace data in the paper (hearth, refractory, tap-holes, operating data); confirm the 63 MVA, 13.7 m and 1.55 m values.

### 2.3 Process, energy and metallurgy

#### R-04 – Metso (n.d.). *SAF smelting plant* (vendor web page).
* **Link:** <https://www.metso.com/portfolio/saf-smelting-plant/> (Free)
* **What we took:** furnace specific energy falls by **≈ 70 kWh per tonne of alloy for every 100 °C of feed preheating**.
* **Where used:** docs/01 A-04; the energy balance method (Chapter 9).
* **Who:** M5.
* **Check:** vendor information. Find a peer-reviewed source confirming the preheating effect.

#### R-05 – Engineering News (2017). *Low grades, high power costs key snags to SA chromite sector's competitiveness.*
* **Link:** <https://www.engineeringnews.co.za/article/low-grades-high-power-costs-key-snags-to-sa-chromite-sectors-competitiveness-2017-07-14> (Free)
* **What we took:** the Outotec closed-furnace route uses **3.0–3.5 MWh per tonne of alloy**.
* **Where used:** docs/01 A-04; docs/03 §5.2 (SEC 3.25 MWh/t, production 374 t/d); Chapters 9 and 15.
* **Who:** M5, M6.
* **Check:** this is trade press, so **replace it with a peer-reviewed source** for the final report.

#### R-06 – Creamer Media (2014). *Ferrochrome smelter uses significantly less electricity.*
* **Link:** <https://newsletter.mw.creamermedia.com/article/ferrochrome-smelter-uses-significantly-less-electricity-2014-12-12> (Free)
* **What we took:** South African closed ferrochrome furnaces use **Söderberg electrodes** and **pelletising with preheating**.
* **Where used:** docs/01 A-02 (Söderberg electrodes); docs/03 §2; Chapter 3.
* **Who:** M1, M5.
* **Check:** trade press; use it as background only.

#### R-07 – Kleynhans, E.L.J. NWU dissertation (title and year to confirm).
* **Link:** <https://repository.nwu.ac.za/bitstream/handle/10394/38919/Kleynhans_E.L.J..pdf?sequence=5> (Free)
* **What we took:** electricity consumption for HC ferrochrome depends strongly on the SiO₂ content of the ore, with a **lowest value of 3.31 MWh/t at 6 % SiO₂**.
* **Where used:** docs/01 A-04 (supports the 3.0–3.5 MWh/t range); Chapters 9 and 11.
* **Who:** M5.
* **Check:** confirm this dissertation is the source of the 3.31 MWh/t value; record the title, year and page.

#### R-18 – (Authors to confirm) (2004). Paper in the *Journal of the SAIMM*, 104(9), p. 517 (South African chromite ore compositions).
* **Link:** <https://www.saimm.co.za/Journal/v104n09p517.pdf> (Free)
* **What we took:** the **LG6 concentrate analysis: 44.2 % Cr₂O₃, 24.1 % FeO, 13.8 % Al₂O₃, 11.5 % MgO, 2.5 % SiO₂, Cr/Fe = 1.62** (also UG2: 41.6 % Cr₂O₃, Cr/Fe 1.36).
* **Where used:** docs/03 §5.1 (the feed of the reference furnace; Cr/Fe check 1.61 vs 1.62); Chapters 3 and 8 (mass balance basis).
* **Who:** M5.
* **Check:** ⚠ the table was partly garbled in the extraction. **Confirm every number against the PDF.** Note the remaining oxides (CaO, TiO₂ and so on) for the mass balance.

#### R-19 – NWU repository. *Exploring beneficial uses of ferrochrome slag: a case study of a South African ferrochrome industry.*
* **Link:** <https://repository.nwu.ac.za/items/fcacc069-12fb-4d14-9291-3a06e8b7c510> (Free)
* **What we took:** a typical South African ferrochrome slag of **30 % SiO₂, 26 % Al₂O₃, 23 % MgO, ≈ 2 % CaO**.
* **Where used:** docs/03 §5.2 (slag, basicity 0.83, MgO/Al₂O₃ 0.88); Chapters 8 and 11.
* **Who:** M5.
* **Check:** the authors and year; the full slag analysis including Cr₂O₃ and FeO.

#### R-20 – (Authors to confirm) (2024). *Value extraction from ferrochrome slag: a thermochemical equilibrium calculation and experimental approach.* Minerals, 14(11), 1097.
* **Link:** <https://doi.org/10.3390/min14111097> (Free, open access)
* **What we took:** slag ranges of **27–35 % SiO₂, 15–29 % Al₂O₃, 23–33 % MgO, 1–5 % CaO, 7–13 % Cr₂O₃**.
* **Where used:** docs/03 §5.2 (the Cr₂O₃-in-slag range 4.5–13 %); Chapters 8 and 11 (Cr recovery).
* **Who:** M5.
* **Check:** the source of the ranges; any thermodynamic data useful for the energy balance.

### 2.4 Standards (through the university library)

| Standard | Used for | Who |
|---|---|---|
| IEC 60076-1 Power transformers – General | Transformer rating and loading (DC-01) | M2 |
| IEEE C57.17 Requirements for arc furnace transformers | Tap range, current rating, rated region (docs/02 §6, DC-03) | M2 |
| IEC 60909 Short-circuit currents | Short-circuit forces on busbars and holders (Chapter 13.3) | M2, M1 |
| IEC 61000-3-6 / 61000-3-7 | Harmonic and flicker emission limits (flagged only) | M2 |
| NRS 048-2 (South Africa) | Voltage quality on the SA grid (flagged only) | M2 |

---

## 3. Reverse map: which sources support each report chapter

| Ch. | Chapter | Sources | Status |
|---|---|---|---|
| 2 | Problem definition | R-02, R-14 | Abstract only |
| 3 | Existing process description | R-06, R-11, R-18, R-19 | Abstract only |
| 4 | Design basis | Standards; R-01, R-03 | Standards not yet obtained |
| 5 | Assumptions | All (each assumption cites its source) | – |
| 6 | Literature review | All R-01 to R-20 + gaps in Section 4 | Abstract only |
| 7 | Existing condition calculations | R-11, R-13, R-16, R-17, R-12 | Abstract only |
| 8 | Mass balance | R-18, R-19, R-20, **R-10 (missing)** | Gap |
| 9 | Energy balance | R-04, R-05, R-07 + **G-07 (missing)** | Gap |
| 10 | Electrical analysis | R-01, R-02, R-03, R-08, R-09, R-12, R-13, R-14, R-15 | Abstract only |
| 11 | Process/metallurgical analysis | R-07, R-19, R-20 | Abstract only |
| 12 | Development of alternatives | R-14, R-15, R-16, R-17 | Abstract only |
| 13 | Detailed calculations | R-15 + **G-04 to G-06 (missing)** | Gap |
| 14 | Equipment requirements | Standards | Not obtained |
| 15 | Economic evaluation | R-05 + **G-08, G-09 (missing)** | Gap |
| 16–17 | Sensitivity, risk | R-12 (C₃ range), R-02 | Abstract only |

---

## 4. Gaps: sources we still need to find

| Gap | What is missing | Needed for | Who | Where to look |
|---|---|---|---|---|
| R-10 | **Charge-chrome alloy specification** (Cr, C, Si, S, P) | A-01, Chapter 8 | M5 | ISO ferrochromium specification (to be confirmed); ICDA; producer data sheets |
| G-01 | Original Andreae / Kelly k-factor papers (resistance vs electrode geometry) | Converting +21 % resistance into PCD/tip position (Chapter 10.7) | M3 | pyrometallurgy.co.za INFACON archive; Westly R-01 reference list |
| G-02 | Published furnace-transformer short-circuit impedance | Testing the implied 16 % (docs/03 §3.2) | M2 | Transformer manufacturer papers; R-15 |
| G-03 | A peer-reviewed Söderberg current-density / electrode-breakage source | A-07 (replace the patent R-08) | M3 | INFACON proceedings; Elkem papers |
| G-04 | Refractory lining design of ferrochrome SAFs (thickness, freeze lining) | Lining check 1.41 m; Chapter 13.2 | M4 | SAIMM / INFACON (Steenkamp is a key author on refractories) |
| G-05 | Hearth power density / heat flux data for ferrochrome furnaces | DC-07; Chapter 13.2 | M4 | INFACON; SAIMM |
| G-06 | Cooling-water heat loads of closed SAFs | DC-06 and A-22 (auxiliary margin) | M4 | INFACON; plant design papers |
| G-07 | Thermodynamic data (reaction enthalpies, heat capacities) | Energy balance (Chapter 9) | M5 | NIST-JANAF tables; HSC/FactSage data; textbooks |
| G-08 | Capital cost of transformers, busbars and cooling upgrades | Chapter 15 | M6 | Cost indices; vendor budget prices; published project costs |
| G-09 | Electricity tariff and ferrochrome price | Chapter 15 | M6 | Eskom tariff book; market reports |
| G-10 | Electrical efficiency (η_el) of the secondary circuit | A-06 | M2 | R-15; INFACON |

**Rule:** when you find a new source, send it to the Project Leader for the next R-number. Do not use it until it is in the reference register.

---

## 5. Checklist when you download a paper

1. Save the PDF as **R-xx_FirstAuthor_Year.pdf** (for example `R-13_McDougall_2007.pdf`) and send it to the Project Leader for the shared folder (`references/papers/`).
2. Find **every value we took from it** (Section 2, "What we took") and confirm it is exactly right. Note the **page and table number**.
3. Fill in the full citation (authors, year, title, journal, volume, pages) in Harvard style.
4. If a value is **different** from what we used, tell the Project Leader **immediately**. It may change the baseline (especially R-13, R-11, R-16, R-17 and R-18).
5. Note anything else useful for your chapter.
6. The Project Leader then changes the status from **"abstract only" to "full text checked"** in the reference register.

**Priority order for checking**, because the most design numbers depend on these: **R-13** (calibration furnace) → **R-11** (63 MVA analogue) → **R-16 and R-17** (geometry) → **R-18** (feed) → **R-02 and R-14** (power factor and reactance) → **R-01** (Westly) → the rest.

---

## 6. How to get the papers

| Website | Access |
|---|---|
| pyrometallurgy.co.za (INFACON, Mintek papers) | Free PDF – click the link |
| scielo.org.za and saimm.co.za (Journal of the SAIMM) | Free PDF – click the link |
| mdpi.com / doi.org (Energies, Minerals) | Free – open access |
| open.uct.ac.za, repository.nwu.ac.za (theses) | Free PDF |
| USPTO (patents) | Free PDF |
| researchgate.net | Free account, or press "Request full text" to ask the author |
| abmproceedings.com.br | Free PDF (in Portuguese – use a translator) |
| Standards (IEC, IEEE, NRS) | University library database |
