"""
00_screening_transformer_pf.py
Screening check ONLY (pre-design-basis approval). Uses ratios, no plant data.

Question: can a 65 MVA furnace transformer installation deliver 60 MW to the
furnace, and what does that imply for power factor (PF) and the bath
resistance-to-reactance ratio R/X?

Relations (per-phase equivalent star circuit, balanced 3-phase):
    S = P_tx / PF                      [MVA]
    PF = R / sqrt(R^2 + X^2)  ->  R/X = PF / sqrt(1 - PF^2)
    P_tx = P_furnace / eta_el          (eta_el = electrical efficiency of
                                         secondary circuit, ASSUMED range)
All PF / efficiency values below are ASSUMPTIONS for sensitivity, not plant data.
"""
import math

S_RATED = 65.0          # MVA, from project brief (interpretation: total installed)
P_BASE, P_NEW = 55.0, 60.0   # MW furnace power, from brief

def rx(pf):
    return pf / math.sqrt(1 - pf**2)

print("1) Minimum PF needed at 65 MVA (P_tx = P_furnace / eta_el)")
print(f"{'eta_el':>7} {'P_tx 55MW':>10} {'PFmin 55':>9} {'P_tx 60MW':>10} {'PFmin 60':>9} {'R/X 60':>7}")
for eta in (1.00, 0.98, 0.96, 0.94):
    p55, p60 = P_BASE/eta, P_NEW/eta
    pf55, pf60 = p55/S_RATED, p60/S_RATED
    print(f"{eta:7.2f} {p55:10.2f} {pf55:9.3f} {p60:10.2f} {pf60:9.3f} {rx(pf60):7.2f}")

print("\n2) MVA needed for 60 MW furnace power at assumed PF (eta_el = 0.96)")
for pf in (0.75, 0.80, 0.85, 0.90, 0.92, 0.94):
    print(f"   PF {pf:.2f}: S = {P_NEW/0.96/pf:6.1f} MVA   (R/X = {rx(pf):.2f})")

print("\n3) Active power available from 65 MVA at assumed PF")
for pf in (0.75, 0.80, 0.85, 0.90):
    print(f"   PF {pf:.2f}: P_tx = {S_RATED*pf:5.1f} MW -> furnace ~{S_RATED*pf*0.96:5.1f} MW (eta 0.96)")

pf_a, pf_b = 0.85, P_NEW/0.96/S_RATED
print(f"\n4) Required R/X increase from PF {pf_a} to PF {pf_b:.3f}: "
      f"{(rx(pf_b)/rx(pf_a)-1)*100:.0f} %")
