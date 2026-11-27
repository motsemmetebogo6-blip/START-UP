# Purpose and scope

This report documents the design and scale-up of an existing closed, three-phase ferrochrome submerged arc furnace (SAF) from its present mean power of 57.43 MW to a mean power of 60 MW, using the existing 65 MVA transformers and keeping the existing furnace shell, hearth, roof and Søderberg electrodes. The performance requirement is a production of at least 450 t/d of alloy.

# Existing condition

The plant data show a furnace that is already at the limit of its electrical supply. It draws 57.43 MW mean (60.45 MW while on load) at a power factor of 0.93 and a load factor of 0.95, produces 393.65 t/d at 3.5 MWh/t, and loads the 65 MVA transformers to 100 % whenever it is on load. The target of 450 t/d would need 65.6 MW mean at the present specific energy, which is more than the transformers can deliver. No electrical measure alone can meet both requirements, so the specific energy per tonne must also fall.

# Approach and main findings

The work followed the stages of the design framework: design basis, existing condition, mass and energy balances, electrical and metallurgical analysis, alternatives, detailed calculations, economics, sensitivity and risk. All calculations were repeated in a verified Python model and cross-checked in MATLAB (GNU Octave), with 104 of 104 electrical comparisons and 18 of 18 mass-balance and optimisation comparisons agreeing.

1. **Mass balance.** The plant analyses are mutually consistent (closure -0.41 %, every element balance within 3 %). Per tonne of alloy the furnace consumes 2.14 t of ore, 0.433 t of dry reductant and 0.366 t of flux, and produces 1.19 t of slag and about 597 Nm³ of off-gas. The chromium recovery is 86.9 %, not the 78 % assumed in the data.
2. **Energy balance.** The 3.50 MWh/t divides into 2.90 MWh/t of process requirement, 0.15 MWh/t of electrical loss and 0.46 MWh/t of thermal loss. Hot charging of pellets at 500 °C returns 712 MJ/t.
3. **Electrical analysis.** A 60 MW mean power is reachable only when the power factor is at its 0.95 limit and the load factor is at least 0.972. The transformers have no on-load headroom (64.98 MVA of 65 MVA).
4. **Selected design (C1).** The 60 MW electrical uprate (power factor 0.95, load factor 0.972) is combined with hot charging of the pellets at about 500 °C. It was the first-ranked alternative under every weighting tested. It gives between 444 and 463 t/d depending on how much of the burden is heated, and about 455 t/d in the verified model.
5. **Optimisation.** The least preheat that meets 450 t/d is 452 °C. A Monte Carlo study shows that the design reaches 450 t/d in only about 10 % of cases while the hot-charging saving is unverified, and a robust optimisation shows that a preheater designed for about 610 °C gives a 90 % probability once the saving has been confirmed by a plant trial.
6. **Economics.** The total investment is about R402 million. The incremental pre-tax profit is about R383 million per year, the net present value over 15 years at 12 % is about R1 540 million, the internal rate of return is about 70 % and the after-tax payback is about 1.4 years.
7. **Sensitivity.** The net present value stays positive in every case tested, and falls to zero only at an alloy price of about US$734/t. The binding requirement is technical: a halved hot-charging saving, a load factor that stays at 0.95, or a power factor that stays at 0.93 each cause the 450 t/d requirement to fail. At the design margin assumed for the auxiliary systems, their utilisation reaches about 105 %, so upgrades are required.
8. **Digital tools.** The calculations are available as a Python model cross-checked in MATLAB, an Excel workbook, a five-page Power BI dashboard and a MATLAB dashboard (Appendices B to D). A CAD model of the furnace with dimensioned open-cut, top, side and bottom views, and a COMSOL-type temperature study of one electrode, are given in Appendix A. The temperature inside the electrode rests on assumed material data and must be calibrated.

# Recommendation

The uprate is recommended, subject to the gates in the implementation plan. Before capital is released, the plant should (a) measure the actual feed heat and energy saving delivered by hot charging in a plant trial, (b) meter the power factor and load factor to confirm that 0.95 and 0.972 can be reached, (c) survey the actual capacity of the cooling, off-gas, tapping and slag systems, and (d) replace the estimated electrode current and voltage with measured values. The slag superheat of only about 44 °C must be protected, so the electrodes are retained as they are.
