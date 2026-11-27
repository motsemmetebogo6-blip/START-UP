import csv
R='/home/user/START-UP/results/model/'
rows={r['scenario']:r for r in csv.DictReader(open(R+'I1_scenario_summary.csv'))}
f=lambda x,n=2:f"{float(x):.{n}f}"
names={'A':'Existing operation (workbook)','S-N55':'"55 MW" read as continuous power','E1':'Power factor raised to 0.95, load factor unchanged',
'S-B':'60 MW mean (adopted definition)','S-N60':'60 MW continuous (load factor 1)','S-O60':'60 MW on load, load factor unchanged',
'P1':'Hot charging only','C1':'60 MW mean with hot charging (selected)'}
order=['A','S-N55','E1','S-B','S-N60','S-O60','P1','C1']
t1=['| ID | Meaning | PF | LF | P mean (MW) | P on load (MW) | S on load (MVA) | Loading (%) |','|---|---|---|---|---|---|---|---|']
t2=['| ID | Electrode current (kA) | Secondary voltage (V) | Current density (A/cm²) | SEC (MWh/t) | Production (t/d) | 450 t/d met |','|---|---|---|---|---|---|---|']
for k in order:
    r=rows[k]
    t1.append(f"| {k} | {names[k]} | {f(r['PF'])} | {f(r['LF'],3) if k in('S-B','C1') else f(r['LF'])} | {f(r['P_mean_MW'])} | {f(r['P_on_MW'])} | {f(r['S_on_MVA'])} | {f(r['loading_on_pct'],1)} |")
    t2.append(f"| {k} | {f(r['I_electrode_kA_est'],1)} | {f(r['V_secondary_LL_V_est'],0)} | {f(r['J_A_cm2_est'])} | {f(r['SEC_MWh_t'])} | {f(r['production_tpd'],1)} | {'Yes' if float(r['meets_450_tpd'])==1 else 'No'} |")
pf=[r for r in csv.DictReader(open(R+'I1_pf_route_comparison.csv')) if r['PF'] in('0.93','0.94','0.95')]
t3=['| Route | PF | Current ratio | Current density (A/cm²) | Change (%) | DC-04 |','|---|---|---|---|---|---|']
for r in pf:
    rt={'R':'Raise operating resistance','X':'Lower reactance'}[r['route']]
    t3.append(f"| {rt} | {r['PF']} | {float(r['I_ratio_vs_existing']):.4f} | {f(r['J_A_cm2_est'])} | {float(r['J_change_pct']):+.1f} | {'Met' if r['DC-04']=='PASS' else 'Exceeded'} |")
md=f'''# Purpose and basis

The electrical analysis establishes what the existing 65 MVA transformers and the electrode system can deliver, and tests whether a mean power of 60 MW can be reached on them. The inputs are the transformer rating S = 65 MVA, the power factor PF = 0.93 and the load factor LF = 0.95 from the plant data (Ferrochrome Data Workbook, 2026), the Søderberg electrode diameter of 1.55 m (A-16), the Westly constant C₃ = 8.33 (A-18) and a high-voltage supply of 132 kV (A-21). The power factor of 0.93 is an assumption in the plant data and the load factor of 0.95 was back-solved from production, so both must be confirmed by metering. Electrode current, secondary voltage and current density are estimates because the plant data contain no secondary-circuit measurements.

# Electrical relationships

The load factor LF is the fraction of time that the furnace is on load. It is not a cap on transformer loading. The mean power, the power while on load and the apparent power are therefore related by:

::: {{custom-style="Equation"}}
P_mean = S × PF × LF  (10.1)
:::

::: {{custom-style="Equation"}}
P_on = P_mean / LF  (10.2)
:::

::: {{custom-style="Equation"}}
S_on = P_on / PF,   Q_on = S_on × sin φ,   cos φ = PF  (10.3)
:::

where P_mean is the mean active power (MW), P_on the active power while on load (MW), S_on the apparent power while on load (MVA) and Q_on the reactive power (Mvar). The electrode current is estimated from the Westly similarity relation, the winding current and secondary voltage follow from a delta-connected single-phase transformer arrangement, and the current density from the electrode area:

::: {{custom-style="Equation"}}
I_e = C₃ × P_on^(2/3)  (10.4)
:::

::: {{custom-style="Equation"}}
I_winding = I_e / √3,   V_LL = S_on / (√3 × I_e)  (10.5)
:::

::: {{custom-style="Equation"}}
J = I_e / (π D² / 4),   R = P_on / (3 I_e²),   X = R × tan φ  (10.6)
:::

At 60 MW mean power, PF 0.95 and LF 0.972, Equation (10.2) gives P_on = 60 / 0.972 = 61.73 MW and Equation (10.3) gives S_on = 61.73 / 0.95 = 64.98 MVA, which is 99.97 % of the transformer rating.

# Scenarios and the meaning of 60 MW

The statement "60 MW" can be read in three ways, and each gives a different transformer loading. Eight scenarios were therefore defined and calculated with the same equations. The adopted definition is S-B, a mean power of 60 MW at the power factor limit of 0.95 and a load factor of 0.972. Scenario C1 combines S-B with hot charging and is the design selected in Chapter 12.

::: {{custom-style="Table Caption"}}
Table 10.1: Electrical operating points of the scenarios
:::

{chr(10).join(t1)}

::: {{custom-style="Table Caption"}}
Table 10.2: Electrode estimates and production of the scenarios
:::

{chr(10).join(t2)}

Values for the electrode current, secondary voltage and current density are estimates from the Westly relation with C₃ = 8.33. Over the reported range C₃ = 6 to 11, the electrode current of the existing furnace spans 92 to 169 kA, so these values must be replaced by measurements (gate G1 of Chapter 19). Production is the daily energy divided by the specific energy, with the hot-charging specific energy of 3.1675 MWh/t calculated from the ambient reference of 25 °C.

# Transformer loading and headroom

![](../../report/figures/F2_transformer_loading.png){{width=6.2in}}

::: {{custom-style="Figure Caption"}}
Figure 10.1: On-load transformer loading of each scenario.
:::

The existing furnace already draws 65.00 MVA while on load, and every scenario that raises production electrically stays at 99 to 100 % of the rating. The uprate is therefore a question of time on load and power factor, not of spare capacity. The transformer manufacturer's thermal confirmation, in accordance with IEC 60076-7, is a hard gate before power is raised.

# Operating envelope for 60 MW mean power

![](../../report/figures/F1_operating_envelope.png){{width=5.2in}}

::: {{custom-style="Figure Caption"}}
Figure 10.2: Mean active power on a 65 MVA rating as a function of power factor and load factor.
:::

Equation (10.1) shows that 60 MW mean power is reached only in a narrow corner of the plane: the power factor must be at its 0.95 limit and the load factor at least 0.972. Every 0.001 shortfall in load factor costs about 0.06 MW of mean power.

# Reconciliation with the values in earlier chapters

Some chapters quote different transformer loadings and electrode values for "60 MW". The differences arise from the definition of the power and from the reference used for the preheat, and are not calculation errors.

::: {{custom-style="Table Caption"}}
Table 10.3: Reconciliation of electrical values quoted in this report
:::

| Quantity | Value quoted | Basis of the quoted value | Value in this chapter |
|---|---|---|---|
| Apparent power, 60 MW at PF 0.95 | 63.2 MVA (97 %) | 60 MW taken as the power while on load | 64.98 MVA (100.0 %) for 60 MW mean |
| Apparent power, 60 MW at PF 0.93 | 64.5 MVA (99.3 %) | 60 MW continuous, load factor 1 | 64.52 MVA (S-N60) |
| Electrode current at 55 MW | 120.5 kA, 6.38 A/cm² | 55 MW continuous | 120.5 kA, 6.38 A/cm² (S-N55) |
| Electrode current of the existing furnace | 128 kA, 6.8 A/cm² | 57.43 MW mean, 60.45 MW on load | 128.3 kA, 6.80 A/cm² (A) |
| Production of C1 | 457 t/d | Preheat referenced to 0 °C | 454.6 t/d with the 25 °C ambient reference |

# Raising the power factor: two routes

At constant apparent power the power factor can be raised by increasing the operating resistance of the furnace or by reducing the reactance of the circuit. The two routes load the electrodes differently.

![](../../report/figures/F3_pf_route_current_density.png){{width=5.2in}}

::: {{custom-style="Figure Caption"}}
Figure 10.3: Electrode current density against power factor for the two routes.
:::

::: {{custom-style="Table Caption"}}
Table 10.4: Effect of the power-factor route on the electrode current
:::

{chr(10).join(t3)}

Raising the operating resistance lowers the electrode current by 7.8 % at PF 0.95, whereas lowering the reactance raises it by 1.1 %, which exceeds the acceptance criterion DC-04 (current density not above the existing value). These ratios do not depend on the uncertain C₃ calibration, so the result is robust. Chapter 14 selects the rearrangement of the conductors of the short network, which reduces the reactance. The estimated current density at 60 MW is therefore 6.90 A/cm², which is 1.5 % above the existing 6.80 A/cm². This is a small increase within normal Søderberg practice, but it should either be accepted formally by revising DC-04 or be offset by a small increase in operating resistance.

# Electrode system and secondary voltage

The self-baking Søderberg electrodes of 1.55 m diameter are retained unchanged. The estimated electrode current at C1 is 130.1 kA, the winding current of each single-phase transformer is 75.1 kA and the primary current at 132 kV is 284 A. The estimated secondary line voltage is 288 V against 292 V for the existing furnace, which lies inside the assumed tap range of 260 to 340 V (A-23). Allowing the ±5 % control margin raises the highest voltage required to about 303 V, so the existing tap range is probably adequate, but the nameplate range of the transformers must be confirmed. The per-phase resistance and reactance at C1 are estimated at 1.22 mΩ and 0.40 mΩ, giving a resistance to reactance ratio of 3.04, against 2.53 for the existing furnace.

# Verification of the electrical calculations

All electrical equations were programmed in Python and repeated independently in MATLAB (GNU Octave), reading only the numeric scenario table. All 104 comparisons agree, with a worst relative difference of 3.5 × 10⁻¹⁵. In addition, 52 numbers quoted in the team's chapters were recalculated and 47 were reproduced within 0.5 to 3 %. The five that differ are explained by the definition of the 60 MW power (63.2 against 64.98 MVA), the preheat reference (457.1 against 454.6 t/d) and the use of the earlier 55 MW basis for the electrode current, voltage and current density.

# Summary

The transformers have no on-load headroom in any scenario that raises production electrically, so the uprate depends on the power factor and the load factor. A mean power of 60 MW needs PF 0.95 and LF of at least 0.972, and loads the transformers to 99.97 % while on load. Reducing the reactance, which is the route selected in Chapter 14, raises the electrode current density by about 1.5 % to an estimated 6.90 A/cm², so criterion DC-04 must be revisited. The electrode current, voltage and current density are estimates that must be replaced by plant measurements before capital is released.
'''
open('/home/user/START-UP/final_report/md/ch10_electrical_analysis.md','w',encoding='utf8').write(md)
print(md[:300]); print(len(md))
