---
title: "Presentation Script"
subtitle: "MPG 118S final project: closed ferrochrome submerged arc furnace, 55 to 60 MW"
---

# 1. How to use this script

The presentation has 22 slides and is delivered by six members in about 25 minutes. The script follows the slide order. Each part is marked with the name of the speaker, and the last sentence of a part is the hand-over to the next speaker. The text is written to be read aloud at about 130 words a minute, which is 3003 words, or about 23 minutes of speaking plus about one minute of hand-overs and slide changes.

* Read your own part three times aloud with a timer before the day, and shorten a sentence rather than speed up.
* Look at the audience, not at the slide; the slide has the figures and this script has the words.
* Say the numbers exactly as written. They are the verified results of the report.
* If you are running late, drop the figure description and keep the numbers and the hand-over.
* Only the speaker named in a heading speaks. Slides 17 and 18 have two speakers.

# 2. Who presents what

::: {custom-style="Table Caption"}
Table 1: Allocation of sections, slides and time
:::

| Member | Sections | Slides | Words | Time |
|---|---|---|---|---|
| Mkhonto | Compiler of the report; literature review; opening and conclusions | 1, 2, 5, 21, 22 | 515 | 3:57 |
| Jeff | Problem definition, existing process, electrical analysis, detailed calculations | 3, 4, 10, 12 | 573 | 4:24 |
| Tebogo | Mass balance and optimisation, alternatives and selected design, design basis | 6, 7, 8, 11 | 506 | 3:53 |
| Ngesi | Energy balance, metallurgical analysis, thermal model, implementation plan | 9, 15, 16, 18 | 520 | 4:00 |
| Simphiwe | CAD model, sensitivity analysis, risk | 13, 14, 17, 18 | 445 | 3:25 |
| Sibandze | Economic evaluation, Power BI, MATLAB, Excel and digital files | 17, 19, 20 | 444 | 3:24 |
| Total | | 1 to 22 | 3003 | 23:06 |

The names are those used in the project group. If two members swap sections, move their slide numbers between the parts below; the hand-over sentences name the next speaker and must be changed with them.

# 3. Running order and timing

::: {custom-style="Table Caption"}
Table 2: Running order with cumulative time (hand-overs of 3 to 4 seconds each are not included)
:::

| Slide | Title | Speaker | Time | Cumulative |
|---|---|---|---|---|
| 1 | Title | Mkhonto | 0:29 | 0:29 |
| 2 | Presentation outline | Mkhonto | 0:43 | 1:12 |
| 3 | Executive summary, background and problem | Jeff | 1:13 | 2:26 |
| 4 | Existing process, design basis and assumptions | Jeff | 1:06 | 3:32 |
| 5 | Literature review and existing condition | Mkhonto | 1:15 | 4:48 |
| 6 | Mass balance | Tebogo | 1:12 | 6:00 |
| 7 | How the optimisation was achieved | Tebogo | 1:03 | 7:04 |
| 8 | Robust design | Tebogo | 0:35 | 7:39 |
| 9 | Energy balance and metallurgical analysis | Ngesi | 1:16 | 8:56 |
| 10 | Electrical analysis | Jeff | 1:09 | 10:06 |
| 11 | Alternatives, selected design C1 and investment | Tebogo | 1:02 | 11:08 |
| 12 | Detailed calculations of C1 and equipment | Jeff | 0:54 | 12:03 |
| 13 | CAD model of the furnace: open cut and revolve cut | Simphiwe | 1:12 | 13:16 |
| 14 | Top, side and bottom views | Simphiwe | 0:44 | 14:00 |
| 15 | Thermal model of the electrode (COMSOL-type) | Ngesi | 1:06 | 15:06 |
| 16 | Thermal results | Ngesi | 0:54 | 16:01 |
| 17 | Economic evaluation and sensitivity | Sibandze and Simphiwe | 1:59 | 18:00 |
| 18 | Risk assessment and implementation plan | Simphiwe and Ngesi | 1:12 | 19:13 |
| 19 | Power BI dashboard | Sibandze | 1:10 | 20:24 |
| 20 | MATLAB dashboard, Excel model and digital files | Sibandze | 1:12 | 21:36 |
| 21 | Conclusions and recommendations | Mkhonto | 1:10 | 22:47 |
| 22 | References and questions | Mkhonto | 0:18 | 23:06 |

# 4. The script, slide by slide

## Slide 1: Title

*On the screen:* Title slide with the TUT banner.

**MKHONTO** (0:29)

Good day, panel and fellow students. We are the MPG 118S project group: Sithole, Motsemme, Ngesi, Mabapa, Sibandze and Mkhonto. Our project is the design and scale-up of a closed ferrochrome submerged arc furnace from 55 to 60 megawatts, using the existing 65 MVA transformers. Six of us will present in the next twenty-five minutes, and we follow the order of our final report.

## Slide 2: Presentation outline

*On the screen:* Table with 13 rows: slide, content, report chapter.

**MKHONTO** (0:43)

This slide is the table of contents of the presentation. The left column gives the slide numbers, the middle column the content, and the right column the chapter or appendix of the report that each part summarises. Jeff will start with the problem and the existing condition. Tebogo will take the mass balance and the optimisation. Ngesi will cover the energy balance and the thermal model of the electrode, Simphiwe the CAD model and the sensitivity analysis, and Sibandze the economics and the digital tools. I will close with the conclusions. Jeff, please begin.

*Hand-over:* Hand over to Jeff.

## Slide 3: Executive summary, background and problem

*On the screen:* Three cards (455 t/d, R1 540 M, R402 M) and two text columns.

**JEFF** (1:13)

Thank you, Mkhonto. Ferrochrome smelting uses electricity as its heat source, and it is one of the largest operating costs. Eskom tariffs rose by 12.74 percent in April 2025 and by 8.76 percent in April 2026, while the alloy price is set in US dollars. The brief is to raise the mean power of the existing furnace from 57.43 to 60 megawatts on its 65 MVA transformers. Today the furnace makes 393.65 tonnes a day at 3.5 megawatt-hours per tonne. The central difficulty is that 450 tonnes a day at the present specific energy needs 65.6 megawatts mean, which is more than the transformers can deliver. So the specific energy must also fall. The three cards show the answer of the whole project: about 455 tonnes a day, a net present value of about 1 540 million rand, and a total investment of 402 million rand. The findings on the right are explained by my colleagues in the next slides.

## Slide 4: Existing process, design basis and assumptions

*On the screen:* Left: acceptance criteria table. Right: existing process and critical assumptions.

**JEFF** (1:06)

The furnace is a closed, three-phase furnace. The ore is eighty percent pellets and twenty percent lumpy ore, the flux is fifty-five percent quartz and forty-five percent limestone, and the reductant is coke and two anthracites. Three single-phase transformers of 21.67 MVA give the 65 MVA, and three Søderberg electrodes carry the current. The table on the left gives our acceptance criteria: apparent power not above 65 MVA, power factor between 0.93 and 0.95, production of at least 450 tonnes a day, and a positive net present value. Plant data rank first in our hierarchy, and every value carries a provenance tag. Four assumptions are critical and have low confidence: the hot-charging saving, the auxiliary design margin, the transformer tap range and the reactance reduction. The power factor of 0.93 is also not yet metered, so it is checked at the first gate.

*Hand-over:* Hand over to Mkhonto.

## Slide 5: Literature review and existing condition

*On the screen:* Left: operating envelope figure. Right: literature table and three findings.

**MKHONTO** (1:15)

Thank you, Jeff. The literature shows that power cannot be raised independently of the transformer, the electrodes and the electrical circuit. Barker in 2011 shows that scale-up is limited by reactance and electrode current. De Waal and co-authors represent the furnace as a resistance and a reactance. Magnussen explains how electrode spacing and diameter decide performance, and Sweeten and co-authors show that the ore mineralogy sets the mass and energy balance. The figure applies this to our furnace. Mean power is the rating times the power factor times the load factor, so 60 megawatts mean is reached only when the power factor is at its limit of 0.95 and the load factor is at least 0.972. The plant data reproduce the measured 393.65 tonnes a day to within 0.04 percent. They also show a chromium recovery of about 87 percent, not the 78 percent assumed. No electrical measure alone reaches 450 tonnes a day. Tebogo will now show what the mass balance tells us.

*Hand-over:* Hand over to Tebogo.

## Slide 6: Mass balance

*On the screen:* Mass balance figure, chromium figure, rate table, three cards.

**TEBOGO** (1:12)

Thank you, Mkhonto. The plant data give the analyses of every stream but no flows, so we treated the mass balance as a data-reconciliation problem. We wrote seven balances, on aluminium, magnesium and calcium oxides, silica, chromium, iron and carbon, for five unknowns: the ore, the dry reductant, the quartz, the limestone and the slag. We solved it by weighted non-negative least squares in Python and repeated it independently in MATLAB. The mass closes to minus 0.41 percent and every residual is within 3 percent, so the plant analyses are consistent. Per tonne of alloy the furnace uses 2.144 tonnes of ore, 0.433 tonnes of dry reductant and 0.366 tonnes of flux, and makes 1.188 tonnes of slag. The chromium recovery is 86.9 percent, not 78. At C1 every daily duty rises by 15.5 percent, so with a ten percent design margin the auxiliary systems would run at 105 percent of design and must be upgraded.

## Slide 7: How the optimisation was achieved

*On the screen:* Three step boxes, optimisation map and Monte Carlo histogram.

**TEBOGO** (1:03)

The optimisation asks for the least intervention that still meets 450 tonnes a day. The hot-charging system is our largest cost, so we minimise the preheat temperature subject to the production, power factor and transformer limits. It was done in three steps. First, the deterministic step, solved with a sequential quadratic programme and checked against a closed-form equation and against MATLAB, gives 452 degrees Celsius. Second, a Monte Carlo study with 100 000 samples shows that the design reaches 450 tonnes a day in only about ten percent of cases, because the hot-charging saving rests on a vendor rule of thumb. The left figure shows how the required temperature falls as the load factor rises, and the right figure shows the spread of production. Third, a robust optimisation finds the temperature that gives a stated probability of success.

## Slide 8: Robust design

*On the screen:* Robust figure and table of temperatures.

**TEBOGO** (0:35)

The table shows the result. If the saving is unverified, no practical temperature gives a ninety percent chance of success. If a plant trial confirms the vendor saving, a preheater designed for about 610 degrees gives ninety percent. The cheapest risk reduction is therefore a plant trial before capital is released. Also, every 0.01 of load factor saves about 48 degrees of preheat, so uptime and preheating are interchangeable levers. Ngesi will now take the energy balance.

*Hand-over:* Hand over to Ngesi.

## Slide 9: Energy balance and metallurgical analysis

*On the screen:* Three energy cards, energy and metallurgy bullets.

**NGESI** (1:16)

Thank you, Tebogo. The energy balance divides the 3.50 megawatt-hours per tonne into 2.90 of process requirement, 0.15 of electrical circuit loss and 0.46 of thermal loss. Pellets at 500 degrees return 712 megajoules per tonne, which gives 444 tonnes a day, just below the gate. If the lumpy ore and the fluxes are also hot, the result is 463 tonnes a day. The 450 gate needs at least 832 megajoules per tonne of feed heat, so the hot-charging scope must be defined by feed heat. On the metallurgy side, the chromium recovery is about 87 percent, with 90 percent as the planning value and 93 percent as the target. The slag has only 44 degrees of superheat, which is why we do not raise the electrodes, and we set a stop level of 25 degrees. The flux of 0.449 tonnes per tonne is more than the slag needs, and the specific-energy target of 2.41 needs 58 percent metallisation, above the 40 to 50 percent range.

*Hand-over:* Hand over to Jeff.

## Slide 10: Electrical analysis

*On the screen:* Transformer loading figure and power-factor route figure.

**JEFF** (1:09)

Thank you, Ngesi. The electrical analysis puts eight scenarios on one 65 MVA basis. The case we adopt, 60 megawatts mean power at power factor 0.95 and load factor 0.972, loads the transformers to 64.98 MVA while on load, which is 100 percent. There is no headroom. The other readings of 60 megawatts fail: 60 megawatts on load gives only 57 megawatts mean and 391 tonnes a day, below today. The right figure compares two ways of raising the power factor. Raising the operating resistance cuts the electrode current by 7.8 percent, while the selected route, lowering the reactance by rearranging the conductors, raises it by 1.1 percent. The estimated current density at C1 is therefore 6.90 amperes per square centimetre against 6.80 today, so criterion DC-04 must be revisited. Our model reproduces 47 of 52 numbers in the earlier chapters, and Python and MATLAB agree on 104 of 104 values.

*Hand-over:* Hand over to Tebogo.

## Slide 11: Alternatives, selected design C1 and investment

*On the screen:* Alternatives table and investment table.

**TEBOGO** (1:02)

Thank you, Jeff. We generated seven alternatives from the three levers: power factor, load factor and specific energy. The table shows that only two combinations reach 450 tonnes a day, and one of them, pre-reduction, would overload the gas, tapping and slag systems. The selected design, C1, raises the power factor to 0.95, the load factor to 0.972, and hot-charges the pellets at about 500 degrees. It ranked first under every weighting we tested. It keeps the transformers, the shell and the electrodes. The investment is 402 million rand: 45 for the conductor works, 25 for transformer monitoring, 10 for controls, 30 for auxiliary upgrades, 200 for hot charging, 62 for contingency and 30 for production lost in the shutdown. Capital figures are early-stage estimates with an accuracy of minus 40 to plus 40 percent.

*Hand-over:* Hand over to Jeff.

## Slide 12: Detailed calculations of C1 and equipment

*On the screen:* Calculation table and equipment list.

**JEFF** (0:54)

Thank you, Tebogo. The detailed calculations of C1 are on the left. The mean power is 65 times 0.95 times 0.972, which is 60.02 megawatts. The apparent power while on load is 64.98 MVA. The electrode current, estimated from the Westly relation, is 130.1 kiloamperes. The specific energy with hot charging is 3.1675 megawatt-hours per tonne, giving 454.6 tonnes a day, and the least preheat for 450 is 452 degrees. The margin in specific energy is only one percent, so the hot-charging saving must be verified before capital is committed. The equipment packages on the right are the conductor rearrangement, transformer thermal monitoring, electrode monitors, the auxiliary upgrades and the hot-charging system. Simphiwe will now show the furnace model.

*Hand-over:* Hand over to Simphiwe.

## Slide 13: CAD model of the furnace: open cut and revolve cut

*On the screen:* Section A-A drawing and quarter-cut render.

**SIMPHIWE** (1:12)

Thank you, Jeff. We rebuilt the furnace from the SolidWorks screenshot as a parametric CAD model. The model has the shell, the lining, the roof, three electrodes with angled feet, and two tap pipes. The hearth cavity is a true revolve cut: a cylinder of lining is cut by the revolved half-profile, with a radius of 5.44 metres and a height of 7.5 metres. The left view is the open cut through the axis and electrode 1, and the right view has a quarter removed to show the lining, metal, slag, burden and electrode. The screenshot has no dimensions, so only four values are plant data: the shell at 13.70 metres, the hearth at 10.88, the electrode at 1.55 and the pitch circle at 4.19. All other values are estimates marked with an asterisk, and they are replaced in one parameter file. The model is exported as a STEP assembly, STL files and a DXF of the half-section.

## Slide 14: Top, side and bottom views

*On the screen:* Three dimensioned views.

**SIMPHIWE** (0:44)

These are the top, side and bottom views with dimensions in metres. The three electrodes sit at 0, 120 and 240 degrees on a pitch circle of 4.19 metres, and the two tap pipes at minus 145 and minus 35 degrees. Each electrode has a stub through the roof, an angled foot and a vertical tube above the support plate. The drawings are generated from the same parameters as the 3D model, so if the SolidWorks dimensions are entered, every view and every file is rebuilt. Ngesi will now explain the temperature study that uses this geometry.

*Hand-over:* Hand over to Ngesi.

## Slide 15: Thermal model of the electrode (COMSOL-type)

*On the screen:* Input and COMSOL feature table, validation table, sensitivity chart.

**NGESI** (1:06)

Thank you, Simphiwe. To check the temperature distribution in the electrode we solved steady heat conduction with Joule heating, including the skin effect, on an axisymmetric cell around one electrode. This is the same physics as a COMSOL heat-transfer study, and the table gives the COMSOL feature for each input. The slag temperature of 1 800 degrees and the metal temperature of 1 732 degrees come from the plant data. The current of 130.1 kiloamperes is an estimate, and the resistivity, the conductivity and the film coefficients are assumptions. We did not produce a COMSOL project file, because COMSOL was not available, but the STEP geometry imports directly. The solver was validated: against an analytic cylinder to 3.5 times ten to the minus eight, by mesh refinement, by energy balance, and against an independent MATLAB solution to ten to the minus eleven degrees.

## Slide 16: Thermal results

*On the screen:* Temperature field and three result cards.

**NGESI** (0:54)

The result is the temperature field in the electrode cell. One electrode develops 2.74 megawatts of Joule heat. The 500-degree isotherm, which marks the baking zone of the paste, lies at 9.94 metres, about 0.34 metres above the contact shoes. The highest temperature inside the electrode is 2 550 degrees, but it ranges from 2 220 to 3 580 degrees over the cases we tested, because it depends on assumed material data. We therefore present these electrode temperatures as illustrative. The temperatures of the slag, the metal and the floor follow from plant data. To make it a prediction we need the SolidWorks dimensions, the paste and refractory data and one measured temperature. Sibandze will now take the economics.

*Hand-over:* Hand over to Sibandze.

## Slide 17: Economic evaluation and sensitivity

*On the screen:* Four cards, NPV tornado chart and four bullets.

**SIBANDZE** (1:01)

Thank you, Ngesi. The extra production of 63.3 tonnes a day earns about 604 million rand a year, against incremental operating costs of 220.7 million. The profit before tax is about 383 million rand a year. On an investment of 402 million rand, the net present value over fifteen years at twelve percent is about 1 540 million rand, the internal rate of return is about 70 percent, and the payback after tax is about 1.4 years. When we rerun the economics with the reconciled mass balance and a conservative production of 454.8 tonnes a day, we obtain 1 479 million rand and 68.7 percent. The operating break-even is about 550 US dollars a tonne, and the net present value reaches zero only at about 734. Simphiwe will now show what moves these numbers.

**SIMPHIWE** (0:57)

Thank you, Sibandze. The tornado chart ranks the effect of each assumption on the net present value. The alloy price has the largest swing, 1 159 million rand, but the net present value stays positive in every case we tested. The real risk is technical. If only half the hot-charging saving is achieved, production falls to 432 tonnes a day and the target fails. If the power factor stays at 0.93 or the load factor at 0.95, production is 445 or 444 tonnes a day, and it fails again. The auxiliary systems run at 105 percent with a ten percent design margin, and they need about 28 percent spare capacity to stay below 90 percent. The production target, not the economics, binds the design.

*Hand-over:* Hand over from Sibandze to Simphiwe in the middle of the slide.

## Slide 18: Risk assessment and implementation plan

*On the screen:* Risk table, two cards and implementation bullets.

**SIMPHIWE** (0:30)

Our risk register scores each risk by likelihood times consequence. Transformer overload scores 16 and falls to a low residual rating with monitoring. Auxiliary-system limits score 16 and fall to moderate. Water ingress, roof or gas blowout and hearth or tap-hole failure score 15, and the last two keep a high residual rating, so they need continued surveillance. Ngesi will explain how we implement the project.

**NGESI** (0:42)

Thank you, Simphiwe. The implementation plan runs for 26 months with four decision gates. Power is raised in three stages, 57.4, 58.7 and 60 megawatts, and each stage has numeric entry criteria, including a slag superheat of at least 25 degrees. The tie-in is in the annual shutdown in month 18. The acceptance gate requires 450 tonnes a day, a specific energy not above 3.5, and a transformer loading within 65 MVA. We exclude a new transformer, a power factor above 0.95, raised electrode tips and a pre-reduction plant in this project.

*Hand-over:* Hand over to Sibandze.

## Slide 19: Power BI dashboard

*On the screen:* Five dashboard page images.

**SIBANDZE** (1:10)

Thank you, Ngesi. Our Power BI dashboard has five pages, and each page answers one engineering question. Page one compares the baseline with the selected design. Page two shows the transformer and electrical loading. Page three shows the mass balance. Page four shows the optimisation and its robustness, and page five shows the model verification and the provenance of every input. The dashboard is built on a dataset of fifteen tables in a star schema, with DAX measures and a theme, and a build guide. No number is typed into Power BI: if an input changes, we run the model and refresh the dashboard. We use red only for a failed criterion or a risk, and green only for a pass. Every page states that the electrode values are estimates. The images are the page layouts; the report file is built in Power BI Desktop in about ten minutes from the dataset.

## Slide 20: MATLAB dashboard, Excel model and digital files

*On the screen:* MATLAB dashboard image, verification bullets and file table. Presenter: run saf_dashboard.m once in MATLAB before the presentation.

**SIBANDZE** (1:12)

The MATLAB dashboard draws six panels from files written by the model: the production and the loading of each scenario, the mass balance, the least preheat against load factor, the tornado of the net present value, and the temperature of the electrode. Our rule is that Python is the reference model and MATLAB repeats each calculation independently. The agreement is 104 of 104 electrical values, 18 of 18 for the mass balance and the optimum, 2 times ten to the minus fifteen for the net present value, and ten to the minus eleven degrees for the thermal model. The Excel workbook has 264 live formulas and no errors, so the team can change an input and see the result. The table at the bottom groups the digital files: the CAD files, the thermal solver, the model, the workbook and the dashboards. All of them are in the project repository, and every number in the report can be regenerated.

*Hand-over:* Hand over to Mkhonto.

## Slide 21: Conclusions and recommendations

*On the screen:* Two columns: conclusions and before capital release.

**MKHONTO** (1:10)

Thank you, Sibandze. To conclude. The selected design C1, which is 60 megawatts mean power with hot charging, gives about 455 tonnes a day. The chromium recovery is 86.9 percent, the flux is 0.366 tonnes per tonne, and all duties rise by 15.5 percent. The net present value is about 1 540 million rand and it is positive in every case we tested. The 450 tonnes a day target binds: the hot-charging saving, the load factor of 0.972 and the power factor of 0.95 must all be delivered. The optimum is 452 degrees, but it is robust only at about 610. Before capital is released we recommend a plant trial to measure the hot-charging saving, metering of the power factor and load factor, a survey of the auxiliary capacities, and measured electrode values. For the thermal model we also need the SolidWorks dimensions, the paste and refractory data, and one measured temperature.

## Slide 22: References and questions

*On the screen:* Fourteen references and the thank-you line.

**MKHONTO** (0:18)

The references are in the TUT Harvard style, with the author names in capitals. The slide shows the main ones, and the full list of 38 is in the report. Thank you for your attention. We are ready for your questions.

*Hand-over:* Open for questions.

# 5. Individual reading sheets

Each member can print the sheet below with only their own parts.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Mkhonto

Sections: Compiler of the report; literature review; opening and conclusions. Slides 1, 2, 5, 21, 22. Time about 3:57.

**Slide 1: Title**

Good day, panel and fellow students. We are the MPG 118S project group: Sithole, Motsemme, Ngesi, Mabapa, Sibandze and Mkhonto. Our project is the design and scale-up of a closed ferrochrome submerged arc furnace from 55 to 60 megawatts, using the existing 65 MVA transformers. Six of us will present in the next twenty-five minutes, and we follow the order of our final report.

**Slide 2: Presentation outline**

This slide is the table of contents of the presentation. The left column gives the slide numbers, the middle column the content, and the right column the chapter or appendix of the report that each part summarises. Jeff will start with the problem and the existing condition. Tebogo will take the mass balance and the optimisation. Ngesi will cover the energy balance and the thermal model of the electrode, Simphiwe the CAD model and the sensitivity analysis, and Sibandze the economics and the digital tools. I will close with the conclusions. Jeff, please begin.

**Slide 5: Literature review and existing condition**

Thank you, Jeff. The literature shows that power cannot be raised independently of the transformer, the electrodes and the electrical circuit. Barker in 2011 shows that scale-up is limited by reactance and electrode current. De Waal and co-authors represent the furnace as a resistance and a reactance. Magnussen explains how electrode spacing and diameter decide performance, and Sweeten and co-authors show that the ore mineralogy sets the mass and energy balance. The figure applies this to our furnace. Mean power is the rating times the power factor times the load factor, so 60 megawatts mean is reached only when the power factor is at its limit of 0.95 and the load factor is at least 0.972. The plant data reproduce the measured 393.65 tonnes a day to within 0.04 percent. They also show a chromium recovery of about 87 percent, not the 78 percent assumed. No electrical measure alone reaches 450 tonnes a day. Tebogo will now show what the mass balance tells us.

**Slide 21: Conclusions and recommendations**

Thank you, Sibandze. To conclude. The selected design C1, which is 60 megawatts mean power with hot charging, gives about 455 tonnes a day. The chromium recovery is 86.9 percent, the flux is 0.366 tonnes per tonne, and all duties rise by 15.5 percent. The net present value is about 1 540 million rand and it is positive in every case we tested. The 450 tonnes a day target binds: the hot-charging saving, the load factor of 0.972 and the power factor of 0.95 must all be delivered. The optimum is 452 degrees, but it is robust only at about 610. Before capital is released we recommend a plant trial to measure the hot-charging saving, metering of the power factor and load factor, a survey of the auxiliary capacities, and measured electrode values. For the thermal model we also need the SolidWorks dimensions, the paste and refractory data, and one measured temperature.

**Slide 22: References and questions**

The references are in the TUT Harvard style, with the author names in capitals. The slide shows the main ones, and the full list of 38 is in the report. Thank you for your attention. We are ready for your questions.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Jeff

Sections: Problem definition, existing process, electrical analysis, detailed calculations. Slides 3, 4, 10, 12. Time about 4:24.

**Slide 3: Executive summary, background and problem**

Thank you, Mkhonto. Ferrochrome smelting uses electricity as its heat source, and it is one of the largest operating costs. Eskom tariffs rose by 12.74 percent in April 2025 and by 8.76 percent in April 2026, while the alloy price is set in US dollars. The brief is to raise the mean power of the existing furnace from 57.43 to 60 megawatts on its 65 MVA transformers. Today the furnace makes 393.65 tonnes a day at 3.5 megawatt-hours per tonne. The central difficulty is that 450 tonnes a day at the present specific energy needs 65.6 megawatts mean, which is more than the transformers can deliver. So the specific energy must also fall. The three cards show the answer of the whole project: about 455 tonnes a day, a net present value of about 1 540 million rand, and a total investment of 402 million rand. The findings on the right are explained by my colleagues in the next slides.

**Slide 4: Existing process, design basis and assumptions**

The furnace is a closed, three-phase furnace. The ore is eighty percent pellets and twenty percent lumpy ore, the flux is fifty-five percent quartz and forty-five percent limestone, and the reductant is coke and two anthracites. Three single-phase transformers of 21.67 MVA give the 65 MVA, and three Søderberg electrodes carry the current. The table on the left gives our acceptance criteria: apparent power not above 65 MVA, power factor between 0.93 and 0.95, production of at least 450 tonnes a day, and a positive net present value. Plant data rank first in our hierarchy, and every value carries a provenance tag. Four assumptions are critical and have low confidence: the hot-charging saving, the auxiliary design margin, the transformer tap range and the reactance reduction. The power factor of 0.93 is also not yet metered, so it is checked at the first gate.

**Slide 10: Electrical analysis**

Thank you, Ngesi. The electrical analysis puts eight scenarios on one 65 MVA basis. The case we adopt, 60 megawatts mean power at power factor 0.95 and load factor 0.972, loads the transformers to 64.98 MVA while on load, which is 100 percent. There is no headroom. The other readings of 60 megawatts fail: 60 megawatts on load gives only 57 megawatts mean and 391 tonnes a day, below today. The right figure compares two ways of raising the power factor. Raising the operating resistance cuts the electrode current by 7.8 percent, while the selected route, lowering the reactance by rearranging the conductors, raises it by 1.1 percent. The estimated current density at C1 is therefore 6.90 amperes per square centimetre against 6.80 today, so criterion DC-04 must be revisited. Our model reproduces 47 of 52 numbers in the earlier chapters, and Python and MATLAB agree on 104 of 104 values.

**Slide 12: Detailed calculations of C1 and equipment**

Thank you, Tebogo. The detailed calculations of C1 are on the left. The mean power is 65 times 0.95 times 0.972, which is 60.02 megawatts. The apparent power while on load is 64.98 MVA. The electrode current, estimated from the Westly relation, is 130.1 kiloamperes. The specific energy with hot charging is 3.1675 megawatt-hours per tonne, giving 454.6 tonnes a day, and the least preheat for 450 is 452 degrees. The margin in specific energy is only one percent, so the hot-charging saving must be verified before capital is committed. The equipment packages on the right are the conductor rearrangement, transformer thermal monitoring, electrode monitors, the auxiliary upgrades and the hot-charging system. Simphiwe will now show the furnace model.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Tebogo

Sections: Mass balance and optimisation, alternatives and selected design, design basis. Slides 6, 7, 8, 11. Time about 3:53.

**Slide 6: Mass balance**

Thank you, Mkhonto. The plant data give the analyses of every stream but no flows, so we treated the mass balance as a data-reconciliation problem. We wrote seven balances, on aluminium, magnesium and calcium oxides, silica, chromium, iron and carbon, for five unknowns: the ore, the dry reductant, the quartz, the limestone and the slag. We solved it by weighted non-negative least squares in Python and repeated it independently in MATLAB. The mass closes to minus 0.41 percent and every residual is within 3 percent, so the plant analyses are consistent. Per tonne of alloy the furnace uses 2.144 tonnes of ore, 0.433 tonnes of dry reductant and 0.366 tonnes of flux, and makes 1.188 tonnes of slag. The chromium recovery is 86.9 percent, not 78. At C1 every daily duty rises by 15.5 percent, so with a ten percent design margin the auxiliary systems would run at 105 percent of design and must be upgraded.

**Slide 7: How the optimisation was achieved**

The optimisation asks for the least intervention that still meets 450 tonnes a day. The hot-charging system is our largest cost, so we minimise the preheat temperature subject to the production, power factor and transformer limits. It was done in three steps. First, the deterministic step, solved with a sequential quadratic programme and checked against a closed-form equation and against MATLAB, gives 452 degrees Celsius. Second, a Monte Carlo study with 100 000 samples shows that the design reaches 450 tonnes a day in only about ten percent of cases, because the hot-charging saving rests on a vendor rule of thumb. The left figure shows how the required temperature falls as the load factor rises, and the right figure shows the spread of production. Third, a robust optimisation finds the temperature that gives a stated probability of success.

**Slide 8: Robust design**

The table shows the result. If the saving is unverified, no practical temperature gives a ninety percent chance of success. If a plant trial confirms the vendor saving, a preheater designed for about 610 degrees gives ninety percent. The cheapest risk reduction is therefore a plant trial before capital is released. Also, every 0.01 of load factor saves about 48 degrees of preheat, so uptime and preheating are interchangeable levers. Ngesi will now take the energy balance.

**Slide 11: Alternatives, selected design C1 and investment**

Thank you, Jeff. We generated seven alternatives from the three levers: power factor, load factor and specific energy. The table shows that only two combinations reach 450 tonnes a day, and one of them, pre-reduction, would overload the gas, tapping and slag systems. The selected design, C1, raises the power factor to 0.95, the load factor to 0.972, and hot-charges the pellets at about 500 degrees. It ranked first under every weighting we tested. It keeps the transformers, the shell and the electrodes. The investment is 402 million rand: 45 for the conductor works, 25 for transformer monitoring, 10 for controls, 30 for auxiliary upgrades, 200 for hot charging, 62 for contingency and 30 for production lost in the shutdown. Capital figures are early-stage estimates with an accuracy of minus 40 to plus 40 percent.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Ngesi

Sections: Energy balance, metallurgical analysis, thermal model, implementation plan. Slides 9, 15, 16, 18. Time about 4:00.

**Slide 9: Energy balance and metallurgical analysis**

Thank you, Tebogo. The energy balance divides the 3.50 megawatt-hours per tonne into 2.90 of process requirement, 0.15 of electrical circuit loss and 0.46 of thermal loss. Pellets at 500 degrees return 712 megajoules per tonne, which gives 444 tonnes a day, just below the gate. If the lumpy ore and the fluxes are also hot, the result is 463 tonnes a day. The 450 gate needs at least 832 megajoules per tonne of feed heat, so the hot-charging scope must be defined by feed heat. On the metallurgy side, the chromium recovery is about 87 percent, with 90 percent as the planning value and 93 percent as the target. The slag has only 44 degrees of superheat, which is why we do not raise the electrodes, and we set a stop level of 25 degrees. The flux of 0.449 tonnes per tonne is more than the slag needs, and the specific-energy target of 2.41 needs 58 percent metallisation, above the 40 to 50 percent range.

**Slide 15: Thermal model of the electrode (COMSOL-type)**

Thank you, Simphiwe. To check the temperature distribution in the electrode we solved steady heat conduction with Joule heating, including the skin effect, on an axisymmetric cell around one electrode. This is the same physics as a COMSOL heat-transfer study, and the table gives the COMSOL feature for each input. The slag temperature of 1 800 degrees and the metal temperature of 1 732 degrees come from the plant data. The current of 130.1 kiloamperes is an estimate, and the resistivity, the conductivity and the film coefficients are assumptions. We did not produce a COMSOL project file, because COMSOL was not available, but the STEP geometry imports directly. The solver was validated: against an analytic cylinder to 3.5 times ten to the minus eight, by mesh refinement, by energy balance, and against an independent MATLAB solution to ten to the minus eleven degrees.

**Slide 16: Thermal results**

The result is the temperature field in the electrode cell. One electrode develops 2.74 megawatts of Joule heat. The 500-degree isotherm, which marks the baking zone of the paste, lies at 9.94 metres, about 0.34 metres above the contact shoes. The highest temperature inside the electrode is 2 550 degrees, but it ranges from 2 220 to 3 580 degrees over the cases we tested, because it depends on assumed material data. We therefore present these electrode temperatures as illustrative. The temperatures of the slag, the metal and the floor follow from plant data. To make it a prediction we need the SolidWorks dimensions, the paste and refractory data and one measured temperature. Sibandze will now take the economics.

**Slide 18: Risk assessment and implementation plan**

Thank you, Simphiwe. The implementation plan runs for 26 months with four decision gates. Power is raised in three stages, 57.4, 58.7 and 60 megawatts, and each stage has numeric entry criteria, including a slag superheat of at least 25 degrees. The tie-in is in the annual shutdown in month 18. The acceptance gate requires 450 tonnes a day, a specific energy not above 3.5, and a transformer loading within 65 MVA. We exclude a new transformer, a power factor above 0.95, raised electrode tips and a pre-reduction plant in this project.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Simphiwe

Sections: CAD model, sensitivity analysis, risk. Slides 13, 14, 17, 18. Time about 3:25.

**Slide 13: CAD model of the furnace: open cut and revolve cut**

Thank you, Jeff. We rebuilt the furnace from the SolidWorks screenshot as a parametric CAD model. The model has the shell, the lining, the roof, three electrodes with angled feet, and two tap pipes. The hearth cavity is a true revolve cut: a cylinder of lining is cut by the revolved half-profile, with a radius of 5.44 metres and a height of 7.5 metres. The left view is the open cut through the axis and electrode 1, and the right view has a quarter removed to show the lining, metal, slag, burden and electrode. The screenshot has no dimensions, so only four values are plant data: the shell at 13.70 metres, the hearth at 10.88, the electrode at 1.55 and the pitch circle at 4.19. All other values are estimates marked with an asterisk, and they are replaced in one parameter file. The model is exported as a STEP assembly, STL files and a DXF of the half-section.

**Slide 14: Top, side and bottom views**

These are the top, side and bottom views with dimensions in metres. The three electrodes sit at 0, 120 and 240 degrees on a pitch circle of 4.19 metres, and the two tap pipes at minus 145 and minus 35 degrees. Each electrode has a stub through the roof, an angled foot and a vertical tube above the support plate. The drawings are generated from the same parameters as the 3D model, so if the SolidWorks dimensions are entered, every view and every file is rebuilt. Ngesi will now explain the temperature study that uses this geometry.

**Slide 17: Economic evaluation and sensitivity**

Thank you, Sibandze. The tornado chart ranks the effect of each assumption on the net present value. The alloy price has the largest swing, 1 159 million rand, but the net present value stays positive in every case we tested. The real risk is technical. If only half the hot-charging saving is achieved, production falls to 432 tonnes a day and the target fails. If the power factor stays at 0.93 or the load factor at 0.95, production is 445 or 444 tonnes a day, and it fails again. The auxiliary systems run at 105 percent with a ten percent design margin, and they need about 28 percent spare capacity to stay below 90 percent. The production target, not the economics, binds the design.

**Slide 18: Risk assessment and implementation plan**

Our risk register scores each risk by likelihood times consequence. Transformer overload scores 16 and falls to a low residual rating with monitoring. Auxiliary-system limits score 16 and fall to moderate. Water ingress, roof or gas blowout and hearth or tap-hole failure score 15, and the last two keep a high residual rating, so they need continued surveillance. Ngesi will explain how we implement the project.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Reading sheet: Sibandze

Sections: Economic evaluation, Power BI, MATLAB, Excel and digital files. Slides 17, 19, 20. Time about 3:24.

**Slide 17: Economic evaluation and sensitivity**

Thank you, Ngesi. The extra production of 63.3 tonnes a day earns about 604 million rand a year, against incremental operating costs of 220.7 million. The profit before tax is about 383 million rand a year. On an investment of 402 million rand, the net present value over fifteen years at twelve percent is about 1 540 million rand, the internal rate of return is about 70 percent, and the payback after tax is about 1.4 years. When we rerun the economics with the reconciled mass balance and a conservative production of 454.8 tonnes a day, we obtain 1 479 million rand and 68.7 percent. The operating break-even is about 550 US dollars a tonne, and the net present value reaches zero only at about 734. Simphiwe will now show what moves these numbers.

**Slide 19: Power BI dashboard**

Thank you, Ngesi. Our Power BI dashboard has five pages, and each page answers one engineering question. Page one compares the baseline with the selected design. Page two shows the transformer and electrical loading. Page three shows the mass balance. Page four shows the optimisation and its robustness, and page five shows the model verification and the provenance of every input. The dashboard is built on a dataset of fifteen tables in a star schema, with DAX measures and a theme, and a build guide. No number is typed into Power BI: if an input changes, we run the model and refresh the dashboard. We use red only for a failed criterion or a risk, and green only for a pass. Every page states that the electrode values are estimates. The images are the page layouts; the report file is built in Power BI Desktop in about ten minutes from the dataset.

**Slide 20: MATLAB dashboard, Excel model and digital files**

The MATLAB dashboard draws six panels from files written by the model: the production and the loading of each scenario, the mass balance, the least preheat against load factor, the tornado of the net present value, and the temperature of the electrode. Our rule is that Python is the reference model and MATLAB repeats each calculation independently. The agreement is 104 of 104 electrical values, 18 of 18 for the mass balance and the optimum, 2 times ten to the minus fifteen for the net present value, and ten to the minus eleven degrees for the thermal model. The Excel workbook has 264 live formulas and no errors, so the team can change an input and see the result. The table at the bottom groups the digital files: the CAD files, the thermal solver, the model, the workbook and the dashboards. All of them are in the project repository, and every number in the report can be regenerated.

# 6. Questions and answers

The panel may ask questions after the presentation. The member named answers first; any other member may add. The answers use only the verified numbers of the report.

::: {custom-style="Table Caption"}
Table 3: Likely questions and answers
:::

| Question | Answers | Answer |
|---|---|---|
| Why not just raise the power factor above 0.95? | Jeff | The supervisor limits the power factor to 0.95, and at 0.95 and a load factor of 0.972 the transformers are already at 100 percent while on load. Even then 60 MW mean at the present 3.5 MWh/t gives only 411 t/d, so the specific energy must fall. |
| Why is the chromium recovery 86.9 percent and not 78 percent? | Tebogo | The 78 percent in the workbook is an assumption. A balance of seven element and oxide equations on the measured analyses closes to minus 0.41 percent and gives 504.2 kg of the 579.9 kg chromium in the alloy per tonne, which is 86.9 percent. The 78 percent would need a slag rate of about 2.2 t/t, which no analysis supports. |
| What does 452 degrees mean when the design uses 500 degrees? | Tebogo | 452 degrees is the least preheat that meets 450 t/d if every input takes its nominal value. The 500 degrees leaves a margin of 48 degrees. The Monte Carlo study shows that the margin is not enough while the saving is unverified. |
| Your report says 457 t/d in one place and 454.6 in another. Which is right? | Jeff | Both follow from the same equation. Chapter 12 measures the preheat from 0 degrees Celsius and gets 457.1 t/d. The verified model measures it from ambient, 25 degrees, which is more conservative, and gets 454.6 t/d. The energy balance chapter gives 444 to 463 t/d depending on how much of the burden is heated. |
| Is the 64.98 MVA a problem? | Jeff | It is 99.97 percent of the 65 MVA rating while the furnace is on load, so there is no headroom. It is acceptable only with the power factor at 0.95 and thermal confirmation from the transformer manufacturer, which is a hard gate in the plan. |
| How reliable are the electrode temperatures? | Ngesi | The slag, metal and floor temperatures come from plant data and are reliable to the accuracy of those data. The electrode interior depends on assumed resistivity, conductivity and cooling, and it varies from 2 220 to 3 580 degrees over our cases. The baking zone moves only about 0.5 metres. We need measured data to calibrate it. |
| Why is there no COMSOL file? | Simphiwe | COMSOL was not available to us. The geometry is a STEP file that imports into COMSOL, and the report gives the domains, materials, loads and study to set up. We solved the same equations with our own finite-volume solver and checked it against an analytic solution and an independent MATLAB solution. |
| Are the CAD dimensions real? | Simphiwe | Four are plant data: shell 13.70 m, hearth 10.88 m, electrode 1.55 m and pitch circle 4.19 m. The rest were scaled from the SolidWorks screenshot, which has no dimensions, and are marked with an asterisk. They are replaced in one file. |
| What happens if the alloy price falls? | Sibandze | The net present value stays positive down to an alloy price of about US$734 per tonne. The operating break-even in the economic chapter is about US$550 per tonne. At US$1 200 per tonne the net present value is about R900 million. |
| Which risk worries you most? | Simphiwe | Technically the hot-charging saving, because if only half is achieved the 450 t/d target fails. Operationally the roof or gas blowout and the hearth or tap-hole failure, which keep a high residual rating. |
| What is the first thing to do after approval? | Ngesi | The measurement campaign: meter the power factor and load factor, measure the cooling-water duty and the mass balance, and run a plant trial of hot charging. Capital is released only at gate G2, after these results. |
| Is the Power BI dashboard finished? | Sibandze | The dataset, the measures, the theme, the page layouts and the build guide are finished. The .pbix file is built in Power BI Desktop from the dataset in about ten minutes. |

# 7. Checklist before the presentation

* Open the PowerPoint and the PDF copy on the presentation computer, and check slide 22 shows the references.
* Run `saf_dashboard.m` once in MATLAB so that the MATLAB dashboard can be shown live if asked (Sibandze). Only its data part was tested in Octave.
* Have the report open at Appendix A (CAD and thermal model), Appendix B (Power BI) and Appendix C (MATLAB) for questions.
* Agree who advances the slides, and who watches the time and signals 5 minutes and 1 minute to the end.
* Agree the order of answers to questions: the member named in Table 3 first.
* Say that the temperatures inside the electrode are illustrative and that the 450 t/d target is the binding requirement. These two points will be asked.
