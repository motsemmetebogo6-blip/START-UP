# 09 – Increment 1 Model Report: Electrical and Production Model

**Model:** `model/safmodel` v0.1.0 (Python) and `matlab/saf_electrical_I1.m` (MATLAB/Octave) · **Date:** 2026-11-27

## 1. What Increment 1 does

1. Reads the supervisor's workbook directly and tags every value with its provenance (`model/inputs/model_inputs.csv`, 106 inputs).
2. Evaluates eight named scenarios, including the **three different meanings of "60 MW"** found in the audit.
3. Calculates for each scenario:
   * mean and on-load active power;
   * apparent and reactive power;
   * on-load transformer loading and headroom;
   * primary line current;
   * electrode, winding and secondary-voltage estimates;
   * per-phase *R*, *X* and *R*/*X*;
   * electrode current density;
   * daily energy, production and the 450 t/d check.
4. Compares the two ways of raising the power factor (operating resistance against reactance) for their effect on electrode current.
5. **Recalculates 52 numbers from the team's chapters** and reports whether each is reproduced.
6. **Cross-validates** Python against an independent MATLAB/Octave implementation.

## 2. Verification of the team's calculations

**47 of 52 team numbers are reproduced** (tolerance 0.5–3 %, depending on rounding in the source). The five that differ are all explained by audit findings in document 08:

| Check | Team value | Model value | Reason |
|---|---|---|---|
| T-02 | 457.1 t/d | 454.6 t/d | AF-14: preheat should be measured from ambient, not 0 °C |
| S-02 | 63.2 MVA | 64.98 MVA | AF-03: the team value used mean instead of on-load power |
| M-06/07/08 | 312 V, 120.5 kA, 6.38 A/cm² | 292 V, 128.3 kA, 6.80 A/cm² | AF-04: pre-workbook values. The model reproduces them exactly as scenario S-N55 (55 MW continuous) |

Several *reproduced* numbers still carry a disputed basis: Ngesi's "95 % loading" (AF-01), the 55 MW baseline (AF-02) and the 2.13 t/t ore "measured" label (AF-05). The audit note on each line of `results/model/I1_verification.csv` records this.

## 3. Python–MATLAB/Octave cross-validation

`matlab/saf_electrical_I1.m` re-implements every equation without using any Python code, reading only the numeric scenario table. Of **104 comparisons, 104 pass**, with a worst relative difference of **3.5 × 10⁻¹⁵** (machine precision). The script was run in GNU Octave 8.4; it uses only functions common to MATLAB and Octave (`csvread`, `fprintf`).

## 4. Scenario results

| ID | Meaning | PF | LF | *P*_mean (MW) | *P*_on (MW) | *S*_on (MVA) | On-load loading | *I*_e est. (kA) | *V*_LL est. (V) | *J* est. (A/cm²) | SEC | t/d | ≥ 450? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | Existing (workbook) | 0.93 | 0.95 | 57.43 | 60.45 | 65.00 | 100.0 % | 128.3 | 292 | 6.80 | 3.50 | 393.8 | No |
| S-N55 | "55 MW" continuous | 0.93 | 1.00 | 55.00 | 55.00 | 59.14 | 91.0 % | 120.5 | 283 | 6.38 | 3.50 | 377.1 | No |
| E1 | PF raised to 0.95 | 0.95 | 0.95 | 58.66 | 61.75 | 65.00 | 100.0 % | 130.1 | 288 | 6.90 | 3.50 | 402.3 | No |
| **S-B** | **60 MW mean** (recommended definition) | 0.95 | 0.972 | 60.00 | 61.73 | 64.98 | 100.0 % | 130.1 | 288 | 6.90 | 3.50 | 411.4 | No |
| S-N60 | 60 MW continuous | 0.93 | 1.00 | 60.00 | 60.00 | 64.52 | 99.3 % | 127.7 | 292 | 6.77 | 3.50 | 411.4 | No |
| S-O60 | 60 MW on load | 0.93 | 0.95 | 57.00 | 60.00 | 64.52 | 99.3 % | 127.7 | 292 | 6.77 | 3.50 | 390.9 | No |
| P1 | Hot charging only | 0.93 | 0.95 | 57.43 | 60.45 | 65.00 | 100.0 % | 128.3 | 292 | 6.80 | 3.15 | 437.5 | No |
| **C1** | **60 MW mean + hot charging** | 0.95 | 0.972 | 60.00 | 61.73 | 64.98 | 100.0 % | 130.1 | 288 | 6.90 | 3.15 | 457.1 | Yes |

*Values marked "est." derive from the Westly relation with C₃ = 8.33 (one literature calibration; AF-08). Over the reported range C₃ = 6–11, the current at scenario A spans 92–169 kA.*

## 5. Engineering findings from Increment 1

1. **The transformers have essentially no on-load headroom** in any scenario that raises production electrically (Figure F2). The baseline already draws 65.00 MVA on load. A 60 MW **mean** (S-B and C1) needs 64.98 MVA on load. The uprate is therefore a question of time-on-load (LF) and power factor, **not of spare MVA**. The transformer OEM's thermal confirmation (IEC 60076-7) is a hard gate.
2. **60 MW mean is reachable only in a narrow corner** of the PF–LF plane: PF at its 0.95 limit *and* LF ≥ 0.972 (Figure F1). Every 0.001 shortfall in LF costs about 0.06 MW mean.
3. **Electrode loading depends on the power-factor route** (Figure F3; AF-10). At constant 65 MVA:
   * raising the operating resistance lowers the electrode current by **7.8 %** (to PF 0.95);
   * lowering the reactance raises it by **1.1 %**, which exceeds DC-04 ("not above existing").

   These ratios are independent of the uncertain C₃ calibration, which makes this a robust result. The route chosen in Ch. 14 and 18 (short-network rearrangement) therefore needs either a combined *R*/*X* route or a revised DC-04 limit (decision for Jeff, Ch. 10/13).
4. The Westly relation, applied at the higher on-load power of C1, also predicts **+1.5 %** current density (6.80 → 6.90 A/cm²). This is consistent with point 3: unless the operating resistance is raised, the electrodes carry slightly more current.

## 6. Figures for the report (`report/figures/`, PNG 300 dpi + SVG)

| Figure | Question answered |
|---|---|
| F1_operating_envelope | Which combinations of power factor and load factor give 60 MW mean on 65 MVA? |
| F2_transformer_loading | How much on-load transformer headroom does each scenario leave? |
| F3_pf_route_current_density | How does the way the power factor is raised affect electrode current density (DC-04)? |

## 7. How to reproduce

```
python3 model/run_increment1.py                     # model, verification, exports
octave-cli --eval "addpath('matlab'); saf_electrical_I1();"   # or run in MATLAB
python3 model/crossval_I1.py                        # Python vs MATLAB/Octave
python3 model/figures_increment1.py                 # figures
python3 -m pytest model/tests -q                    # 7 automated tests
```

## 8. Limitations carried forward

* Electrode current, secondary voltage and current density are **estimates** (no plant measurements).
* The single-phase transformer winding current assumes a delta closed at the electrodes, which is the standard arrangement but is not confirmed by plant data.
* The model is steady-state and balanced. Electrode interaction, phase unbalance and harmonics are outside its scope (see document 08 §B.5 for the ETAP study scope).
