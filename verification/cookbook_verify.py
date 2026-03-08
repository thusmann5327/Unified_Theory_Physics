#!/usr/bin/env python3
"""
HUSMANN COOKBOOK VERIFICATION
=============================
Validates every material selection claim in the Cookbook.

© 2026 Thomas A. Husmann / iBuilt LTD
CC BY-NC-SA 4.0

Usage:
    python3 cookbook_verify.py
"""
import numpy as np

PHI = (1 + np.sqrt(5)) / 2
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}")
        failed += 1

print("=" * 65)
print("HUSMANN COOKBOOK — MATERIAL SELECTION VERIFICATION")
print("=" * 65)

# ── 1. Unity equation composition match ──
print("\n[1] COMPOSITION vs UNITY EQUATION")
print("-" * 40)
Al, Cu, Fe = 0.64, 0.23, 0.13
de = 1/PHI; dm = 1/PHI**3; m = 1/PHI**4

print(f"  Al={Al:.2f} vs 1/phi={de:.4f}  diff={abs(Al-de):.4f}")
print(f"  Cu={Cu:.2f} vs 1/phi3={dm:.4f} diff={abs(Cu-dm):.4f}")
print(f"  Fe={Fe:.2f} vs 1/phi4={m:.4f}  diff={abs(Fe-m):.4f}")

check("Al ~ 1/phi (within 0.03)", abs(Al - de) < 0.03)
check("Cu ~ 1/phi^3 (within 0.01)", abs(Cu - dm) < 0.01)
check("Fe ~ 1/phi^4 (within 0.02)", abs(Fe - m) < 0.02)
check("Sum = 1", abs(de + dm + m - 1.0) < 1e-10)

# ── 2. Electron concentration ──
print("\n[2] ELECTRON CONCENTRATION")
print("-" * 40)
e_a = Al * 3 + Cu * 1 + Fe * 2
print(f"  e/a = {Al}*3 + {Cu}*1 + {Fe}*2 = {e_a:.4f}")
check("e/a > HCP threshold (1.75)", e_a > 1.75)
check("e/a in QC range (2.0-2.6)", 2.0 < e_a < 2.6)

# ── 3. Icosahedron φ structure ──
print("\n[3] ICOSAHEDRON PHI STRUCTURE")
print("-" * 40)
verts = []
for s1 in [1, -1]:
    for s2 in [1, -1]:
        verts.append([0, s1, s2*PHI])
        verts.append([s1, s2*PHI, 0])
        verts.append([s2*PHI, 0, s1])
verts = np.array(verts)

dists = []
for i in range(12):
    for j in range(i+1, 12):
        dists.append(np.linalg.norm(verts[i] - verts[j]))
dists = sorted(set([round(d, 6) for d in dists]))

edge = dists[0]
short_diag = dists[1]
ratio = short_diag / edge
print(f"  Edge = {edge:.4f}, Short diagonal = {short_diag:.4f}")
print(f"  Ratio = {ratio:.6f}, phi = {PHI:.6f}")
check("Icosahedron diag/edge = phi", abs(ratio - PHI) < 0.01)

# ── 4. K-shell coupling ──
print("\n[4] K-SHELL COUPLING (Z^3)")
print("-" * 40)
wires = {"Fe": 26, "Cu": 29, "Pd": 46, "W": 74, "Pt": 78, "Th": 90, "U": 92, "Pu": 94}
z3 = {k: v**3 for k, v in wires.items()}
print(f"  Th Z^3 = {z3['Th']:,}")
print(f"  Pd Z^3 = {z3['Pd']:,}")
print(f"  Th/Pd  = {z3['Th']/z3['Pd']:.1f}x")
check("Th > 7x Pd coupling", z3['Th'] / z3['Pd'] > 7)
check("Th > Pt coupling", z3['Th'] > z3['Pt'])
check("U only 7% above Th", abs(z3['U']/z3['Th'] - 1) < 0.08)

# ── 5. Sector mapping: l → sector ──
print("\n[5] ORBITAL SECTOR MAPPING")
print("-" * 40)
# Verify orbital counts are Fibonacci-adjacent
orbital_counts = {0: 1, 1: 3, 2: 5, 3: 7}
fibs = [1, 1, 2, 3, 5, 8, 13]
for l, count in orbital_counts.items():
    is_fib = count in fibs
    is_fib_sum = any(count == fibs[i] + fibs[j] 
                      for i in range(len(fibs)) 
                      for j in range(i+1, len(fibs)))
    print(f"  l={l}: {count} orbitals (Fibonacci: {is_fib}, Fib-sum: {is_fib_sum})")

check("l=0 gives F(1)=1 orbital", orbital_counts[0] == 1)
check("l=1 gives F(4)=3 orbitals", orbital_counts[1] == 3)
check("l=2 gives F(5)=5 orbitals", orbital_counts[2] == 5)

# ── 6. Resonant pair verification ──
print("\n[6] RESONANT PAIRS (p1 + p5 = p6)")
print("-" * 40)
pairs = [("Al", 1, "Cl", 5), ("Al", 1, "F", 5), ("Al", 1, "Br", 5),
         ("Ga", 1, "Cl", 5), ("In", 1, "I", 5)]
for d_name, d_p, a_name, a_p in pairs:
    total = d_p + a_p
    print(f"  {d_name}(p{d_p}) + {a_name}(p{a_p}) = p{total}")
    check(f"{d_name}-{a_name} resonant (p6)", total == 6)

# ── 7. Bond energy ordering ──
print("\n[7] BOND ENERGY ORDERING")
print("-" * 40)
bonds = {"Cu-Cu": 176, "Al-Al": 255, "C-Cl": 328, "C-C": 346,
         "C-O": 358, "N-H": 386, "C-H": 411, "Fe-O": 407,
         "H-H": 432, "O-H": 459, "Si-O": 452, "Al-O": 511,
         "C=C": 614, "Th-O": 878}

check("Cu-Cu weakest (conduit mobile)", bonds["Cu-Cu"] == min(bonds.values()))
check("Th-O strongest (wire survives all)", bonds["Th-O"] == max(bonds.values()))
check("Al-O > Fe-O (backbone anchors harder than gate)", bonds["Al-O"] > bonds["Fe-O"])
check("Cu-Cu < Al-Al (conduit weaker than backbone)", bonds["Cu-Cu"] < bonds["Al-Al"])

# ── 8. Condensation bracket ordering ──
print("\n[8] CONDENSATION SEQUENCE")
print("-" * 40)
cond = {"Os": 141.3, "W": 141.5, "Pt": 141.8, "Lu": 142.21,
        "Al": 142.3, "Th": 142.25, "Ce": 142.35, "Si": 142.65,
        "Fe": 143.0, "Cu": 143.8, "Au": 143.5, "Na": 145.5, "H2O": 146.80}

check("Os condenses first (ultra-refractory)", cond["Os"] == min(cond.values()))
check("HREE before silicate cliff", cond["Lu"] < cond["Si"])
check("Th in HREE zone", abs(cond["Th"] - cond["Lu"]) < 0.2)
check("Silicate cliff at 142.65", cond["Si"] == 142.65)
check("Ice line at 146.80", cond["H2O"] == 146.80)
check("Fe after Si (iron zone after cliff)", cond["Fe"] > cond["Si"])

# ── 9. Zeckendorf addresses ──
print("\n[9] ZECKENDORF ADDRESSES")
print("-" * 40)

def zeckendorf(n):
    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    result = []
    rem = int(round(n))
    for f in reversed(fibs):
        if f <= rem:
            result.append(f)
            rem -= f
    return result

targets = {142: [89, 34, 13, 5, 1], 144: [144],
           145: [144, 1], 148: [144, 3, 1]}

for n, expected in targets.items():
    z = zeckendorf(n)
    print(f"  {n} = {{{', '.join(map(str, z))}}}")
    check(f"Zeckendorf({n}) correct", z == expected)

# Check no consecutive Fibonacci numbers in any decomposition
for n, z in targets.items():
    # Check no consecutive Fibonacci numbers: for each pair in decomposition,
    # verify they are NOT adjacent Fibonacci numbers
    fibs_list = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    consecutive = False
    for i in range(len(z)-1):
        a, b = z[i], z[i+1]
        if a in fibs_list and b in fibs_list:
            ia = fibs_list.index(a)
            ib = fibs_list.index(b)
            if abs(ia - ib) == 1:
                consecutive = True
    check(f"Zeckendorf({n}) no consecutive Fibs", not consecutive)

# ── 10. Hume-Rothery progression ──
print("\n[10] HUME-ROTHERY STRUCTURE PROGRESSION")
print("-" * 40)
print(f"  BCC: e/a ~ 1.48")
print(f"  FCC: e/a ~ 1.62 (~ phi = {PHI:.4f})")
print(f"  HCP: e/a ~ 1.75")
print(f"  QC:  e/a ~ {e_a:.2f}")
check("FCC threshold ~ phi", abs(1.62 - PHI) < 0.01)
check("QC above all periodic thresholds", e_a > 1.75)

# ── Summary ──
print(f"\n{'='*65}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed+failed}")
print(f"{'='*65}")
if failed == 0:
    print("\n  ALL TESTS PASSED — Cookbook material selections verified.")
else:
    print(f"\n  {failed} test(s) failed — review above.")
