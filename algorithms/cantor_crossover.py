#!/usr/bin/env python3
"""
CANTOR CROSSOVER OPERATOR v2
================================

Extended March 14-15, 2026 — Hofstadter's Golden Butterfly

v1 (March 14): Generalized from gaba_engine.py TubulinDimer.gaba_collapse()
v2 (March 15): Added metallic mean hierarchy, Chern number computation,
               topological pair annihilation, graphene/microtubule identifiers,
               continued fraction nesting detection.

The GABA engine models a single quantum measurement as a continuous
collapse parameterized by gate_strength. The crossover operator
generalizes this to ANY system at the AAH critical point (V = 2J),
parameterized by metallic mean index n.

The metallic mean hierarchy (x² = nx + 1) maps onto physical systems:

  n = 1  (golden):  hydrogen, cosmological scales, LCD polarizers
  n = 2  (silver):  helium shell
  n = 3  (bronze):  bronze-mean quasicrystal (Majorana modes, Zeng 2024)
  n = 13:           microtubule (13 protofilaments = F(7))
  n = 53:           graphene magic angle (0.06% match)
  n = 60:           graphene/hBN lattice mismatch (0.66% match)

Five instances of the same operator:

  GABA gate:     gate_strength → entropy → collapse completeness
  N-SmA:         McMillan ratio r → d_eff → heat capacity α
  Quantum Hall:  effective V/J → D_s^(obs) → temperature scaling κ
  Magic angle:   twist θ → moiré period → flat band condition
  LCD polarizer: polarization angle → intensity → 5→3 projection

One axiom: φ² = φ + 1
One parameter: r_c = 1 - 1/φ⁴

References:
  Hofstadter (1976) Phys Rev B 14, 2239
  Aubry & André (1980) Ann Israel Phys Soc 3, 133
  Sütő (1989) J Stat Phys 56, 525
  Bellissard et al (1992) Rev Math Phys 4, 1
  Liu, Fulga & Asbóth (2020) Phys Rev Research 2, 022048(R)
  Subramanyan et al (2021) arXiv:2112.12203
  Zhang et al (2022) arXiv:2108.01708
  Zheng, Timms & Kolodrubetz (2022) arXiv:2206.13926v2
  Zeng et al (2024) Phys Rev B 109, L121403
  Kobiałka et al (2024) Phys Rev B 110, 134508
  Ji & Xu (2025) Commun Phys 8, 336
  Varjas et al (2025) arXiv:2602.09769
  Nuckolls et al (2025) Nature 639, 60
  Satija (2025) arXiv:2507.13418
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ============================================================
# CONSTANTS
# ============================================================

PHI = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)

R_C = 1 - 1 / PHI**4                        # = 0.8541
GAMMA_DC = 4                                  # band boundaries
D_S = 0.5                                     # Hausdorff dimension
NU = 1.0 / (2.0 - D_S)                       # = 2/3

assert abs(PHI**2 * R_C - SQRT5) < 1e-14

K_B = 1.380649e-23; EV = 1.602176634e-19
HBAR = 1.054571817e-34; H_PLANCK = 6.62607015e-34
C_LIGHT = 299792458; E_CHARGE = 1.602176634e-19

J_HOPPING = 10.578
L0 = C_LIGHT * HBAR / (2 * J_HOPPING * EV)
A_GRAPHENE = 0.2462e-9; A_HBN = 0.2504e-9
DELTA_GH = 1 - A_GRAPHENE / A_HBN

# ============================================================
# METALLIC MEAN HIERARCHY
# ============================================================

def metallic_mean(n):
    return (n + math.sqrt(n * n + 4)) / 2

def metallic_alpha(n):
    return 1.0 / metallic_mean(n)

def continued_fraction(x, n_terms=15):
    cf = []
    for _ in range(n_terms):
        a = int(x)
        cf.append(a)
        frac = x - a
        if abs(frac) < 1e-10: break
        x = 1.0 / frac
    return cf

def cf_nesting_depth(x, n_terms=12):
    cf = continued_fraction(x, n_terms)
    if len(cf) < 2: return (cf[0] if cf else 0, 0)
    first = cf[1] if cf[0] == 0 else cf[0]
    ones = sum(1 for i in range(2 if cf[0]==0 else 1, min(8, len(cf))) if cf[i]==1)
    return (first, ones)

# ============================================================
# AAH SPECTRUM
# ============================================================

def aah_spectrum(alpha, N=610, V=2.0):
    import numpy as np; from scipy.linalg import eigvalsh
    H = np.zeros((N, N))
    for i in range(N):
        H[i, i] = V * math.cos(2 * math.pi * alpha * i)
        if i+1 < N: H[i, i+1] = 1.0; H[i+1, i] = 1.0
    return np.sort(eigvalsh(H))

def find_gaps(evals, min_width=0.01):
    import numpy as np
    N = len(evals); spacings = np.diff(evals)
    order = np.argsort(spacings)[::-1]
    return [(spacings[idx], (idx+1)/N) for idx in order if spacings[idx] >= min_width]

def box_counting_Ds(evals):
    import numpy as np
    E_min, E_max = evals[0], evals[-1]; E_range = E_max - E_min
    xs = [math.log(2**k / E_range) for k in range(3, 10)]
    ys = [math.log(len(set(int((E-E_min)/(E_range/2**k)) for E in evals))) for k in range(3, 10)]
    x, y = np.array(xs), np.array(ys); n = len(x)
    return (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / (n*np.sum(x**2) - np.sum(x)**2)

# ============================================================
# CHERN NUMBERS
# ============================================================

def gap_label_chern(ids, alpha):
    best_s, best_t, best_err = 0, 0, 999.0
    for s in range(-10, 11):
        for t in range(-10, 11):
            err = abs(s + t * alpha - ids)
            if err < best_err: best_err = err; best_s, best_t = s, t
    return (best_s, best_t)

def chern_numbers_at_alpha(alpha, N=987, n_gaps=6):
    evals = aah_spectrum(alpha, N); gaps = find_gaps(evals)
    results = []
    for i, (w, ids) in enumerate(gaps[:n_gaps]):
        s, t = gap_label_chern(ids, alpha)
        results.append({'rank': i+1, 'width': w, 'ids': ids, 's': s, 't_chern': t})
    return results

# ============================================================
# TOPOLOGICAL PAIR ANNIHILATION
# ============================================================

@dataclass
class CollapseResult:
    inner_gaps: List[Dict] = field(default_factory=list)
    outer_gaps: List[Dict] = field(default_factory=list)
    inner_chern_sum: int = 0
    outer_chern_sum: int = 0
    alternates: bool = False
    inner_larger: bool = False
    topologically_valid: bool = False

def analyze_collapse(alpha=None, N=987):
    if alpha is None: alpha = 1.0 / PHI
    cherns = chern_numbers_at_alpha(alpha, N, 6)
    if len(cherns) < 4: return CollapseResult()
    four = sorted(cherns[:4], key=lambda x: x['ids'])
    r = CollapseResult()
    r.outer_gaps = [four[0], four[3]]; r.inner_gaps = [four[1], four[2]]
    r.outer_chern_sum = sum(g['t_chern'] for g in r.outer_gaps)
    r.inner_chern_sum = sum(g['t_chern'] for g in r.inner_gaps)
    ts = [g['t_chern'] for g in four]
    r.alternates = all(ts[i]*ts[i+1] < 0 for i in range(len(ts)-1))
    r.inner_larger = all(ig['width'] > og['width'] for ig in r.inner_gaps for og in r.outer_gaps)
    r.topologically_valid = (r.outer_chern_sum == 0 and r.inner_chern_sum == 0
                             and r.alternates and r.inner_larger)
    return r

# ============================================================
# PHYSICAL SYSTEM IDENTIFIERS
# ============================================================

def identify_graphene_hbn():
    a60 = metallic_alpha(60); err = abs(a60 - DELTA_GH) / DELTA_GH * 100
    return {'name': 'G/hBN mismatch', 'n': 60, 'alpha': a60, 'match_pct': err,
            'lambda_max_nm': 60 * A_GRAPHENE * 1e9}

def identify_magic_angle():
    theta = math.radians(1.08); a53 = metallic_alpha(53)
    err = abs(a53 - theta) / theta * 100
    return {'name': 'Magic angle', 'n': 53, 'alpha': a53, 'match_pct': err,
            'lambda_nm': 53 * A_GRAPHENE * 1e9}

def identify_microtubule():
    return {'name': 'Microtubule', 'n': 13, 'alpha': metallic_alpha(13),
            'protofilaments': 13, 'helix_starts': 3, 'seams': 1,
            'note': 'SSH topological insulator (Subramanyan 2021)'}

def identify_l0():
    B = H_PLANCK / (E_CHARGE * L0**2); lB = math.sqrt(HBAR / (E_CHARGE * B))
    t = 1.0 / math.sqrt(2 * math.pi)
    return {'l0_nm': L0*1e9, '38ag': 38*A_GRAPHENE*1e9, '37ahBN': 37*A_HBN*1e9,
            'err38': abs(38*A_GRAPHENE - L0)/L0*100, 'err37': abs(37*A_HBN - L0)/L0*100,
            'lB_over_l0': lB/L0, 'target': t, 'mag_err': abs(lB/L0 - t)/t*100}

def band_structure(n, N=987):
    alpha = metallic_alpha(n); evals = aah_spectrum(alpha, N); gaps = find_gaps(evals)
    if len(gaps) < 2: return {'n': n, 'error': 'insufficient gaps'}
    ids1 = min(gaps[0][1], gaps[1][1]); ids2 = max(gaps[0][1], gaps[1][1])
    return {'n': n, 'alpha': alpha, 'ids1': ids1, 'ids2': ids2,
            'band1': ids1, 'band2': ids2-ids1, 'band3': 1-ids2, 'D_s': box_counting_Ds(evals)}

# ============================================================
# CROSSOVER OPERATOR (preserved from v1)
# ============================================================

def cantor_crossover(x, x_c=R_C, gamma=GAMMA_DC, d_full=3):
    if x <= x_c:
        return {'f_decouple': 0.0, 'd_eff': float(d_full),
                'alpha': 2.0 - NU * d_full, 'nu_eff': NU, 'below_xc': True}
    f_dec = ((x - x_c) / (1 - x_c)) ** gamma
    return {'f_decouple': f_dec, 'd_eff': d_full - f_dec,
            'alpha': 2.0 - NU * (d_full - f_dec), 'nu_eff': NU, 'below_xc': False}

def alpha_nsma(r): return cantor_crossover(r)['alpha']
def kappa_qh(W=0.0): return R_C/2 if W <= 0 else min(1.0, D_S + W*(1-D_S))*R_C
def kappa_qah(): return 1/PHI**2
def nu_noninteracting(): return PHI**2
def nu_interacting(): return 2/R_C

# ============================================================
# GABA ENGINE BRIDGE (preserved)
# ============================================================

class TubulinDimer:
    MATTER_FRAC = 1 / PHI ** (PHI ** 3)
    def __init__(self, p_inside=0.535):
        self.p_inside = p_inside; self.collapsed = False
    @property
    def entropy(self):
        p = self.p_inside
        if p <= 0 or p >= 1: return 0.0
        return -(p*math.log(p) + (1-p)*math.log(1-p))
    def gaba_collapse(self, gate_strength=1.0):
        if self.collapsed: return 0.0
        S_before = self.entropy
        self.p_inside += (1.0 - self.p_inside) * gate_strength
        S_after = self.entropy
        self.collapsed = gate_strength >= self.MATTER_FRAC
        return (S_before - S_after) * K_B * 310 / EV
    def to_crossover(self, gs):
        return cantor_crossover(0.60 + 0.40 * gs)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 68)
    print("  CANTOR CROSSOVER OPERATOR v2")
    print("  Metallic Mean Hierarchy + Topological Pair Annihilation")
    print("  One axiom: φ² = φ + 1")
    print("=" * 68)

    print(f"\n  φ = {PHI:.10f},  r_c = {R_C:.10f},  l₀ = {L0*1e9:.3f} nm")
    print(f"  φ²×r_c = {PHI**2*R_C:.10f} = √5 ✓")

    print(f"\n  METALLIC MEAN HIERARCHY:")
    print(f"  {'n':>4}  {'δ_n':>8}  {'α_n':>10}  {'system':>30}")
    for n, lab in [(1,"golden/hydrogen"),(2,"silver/helium"),(3,"bronze/Majorana QC"),
                   (13,"MICROTUBULE (F(7))"),(53,"MAGIC ANGLE"),(60,"G/hBN MISMATCH")]:
        print(f"  {n:>4}  {metallic_mean(n):>8.4f}  {metallic_alpha(n):>10.6f}  {lab:>30}")

    print(f"\n  PHYSICAL SYSTEMS:")
    for fn in [identify_graphene_hbn, identify_magic_angle, identify_microtubule]:
        d = fn(); print(f"    {d['name']}: n={d['n']}, {d}")

    print(f"\n  CF NESTING: δ_G/hBN = [{', '.join(str(x) for x in continued_fraction(DELTA_GH, 8))}]")
    first, ones = cf_nesting_depth(DELTA_GH)
    print(f"    Golden [1,1,1,...] nested after quotient {first} ({ones} consecutive 1's)")

    l = identify_l0()
    print(f"\n  l₀ = {l['l0_nm']:.3f} nm: 38×a_g={l['38ag']:.3f}nm ({l['err38']:.2f}%), "
          f"37×a_hBN={l['37ahBN']:.3f}nm ({l['err37']:.2f}%)")
    print(f"    l_B/l₀ = {l['lB_over_l0']:.6f} ≈ 1/√(2π) = {l['target']:.6f} ({l['mag_err']:.3f}%)")

    print(f"\n  N-SmA: ", end="")
    for r in [0.80, R_C, 0.90, 0.95, 1.00]:
        print(f"r={r:.2f}→α={alpha_nsma(r):.4f}  ", end="")
    print()

    print(f"\n  QH: κ={kappa_qh():.4f}(0.42), κ_QAH={kappa_qah():.4f}(0.38), "
          f"ν_CC={nu_noninteracting():.4f}(2.593), ν_exp={nu_interacting():.4f}(2.38)")

    print(f"\n  BAND STRUCTURE vs n:")
    print(f"  {'n':>4}  {'band1':>7}  {'band2':>7}  {'band3':>7}  {'D_s':>5}")
    for n in [1, 2, 3, 5, 8, 13, 53, 60]:
        b = band_structure(n)
        if 'error' not in b:
            print(f"  {n:>4}  {b['band1']:>7.4f}  {b['band2']:>7.4f}  {b['band3']:>7.4f}  {b['D_s']:>5.3f}")

    print(f"\n  CHERN NUMBERS (α=1/φ):")
    for c in chern_numbers_at_alpha(1/PHI, 987, 6):
        print(f"    IDS={c['ids']:.4f}  width={c['width']:.4f}  t={c['t_chern']:+d}")

    print(f"\n  5→3 COLLAPSE:")
    col = analyze_collapse()
    print(f"    Outer sum={col.outer_chern_sum:+d}, Inner sum={col.inner_chern_sum:+d}, "
          f"Alternates={col.alternates}, Valid={col.topologically_valid}")
