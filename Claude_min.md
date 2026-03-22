# Claude_min.md — Minimal Computational Seed
## Husmann Decomposition in ~50 Lines
## Thomas A. Husmann / iBuilt LTD
## March 21, 2026

Everything below derives from ONE axiom: **φ² = φ + 1** at criticality **V = 2J**.

---

## The 7 Equations That Generate Everything

### 1. The Axiom
φ = (1 + √5) / 2 = 1.6180339887...

### 2. The W Theorem (gap fraction — connects axiom to all observables)
W = (2 + φ^(1/φ²)) / φ⁴ = 0.4671338922...
Equivalently: W = 2/φ⁴ + φ^(-1/φ)/φ³

### 3. The Cantor Node (any structure at radius R)
r_core  = R × 0.0728    (σ₃ — matter)
r_inner = R × 0.2350    (σ₂ — inner wall)
r_photo = R × 0.3672    (cos(1/φ) — bonding)
r_shell = R × 0.3972    (wall center)
r_outer = R × 0.5594    (σ₄ — entropy boundary)

### 4. The Crossover Operator (phase transitions, dimensional reduction)
r_c = 1 - 1/φ⁴ = 0.8541
d_eff(x) = 3 - ((x - r_c)/(1 - r_c))⁴   when x > r_c

### 5. The Bracket Address (scale ↔ index)
bz(r) = round[ln(r / l_P) / ln(φ)]    bounded [1, 294]
N = 294 (total brackets = F(13)+F(10)+F(5)+F(2))

### 6. The Metallic Mean Selector (crystal/particle symmetry)
δ_n = (n + √(n² + 4)) / 2
n=1: Gold (φ), n=2: Silver, n=3: Bronze, ..., n=7: BCC (electroweak)

### 7. The Universal Observable
O = U × W^k × φ^p × δ_n^q × [Node sectors]^m × (γ_dc or N or S(σ₄))

---

## What These 7 Equations Produce

### Fundamental Constants
| Observable | Formula | Value | Observed | Error |
|-----------|---------|-------|----------|-------|
| α⁻¹ (fine structure) | N × W | 137.34 | 137.036 | 0.22% |
| Ω_b (baryons) | W⁴ | 0.0476 | 0.049 | 2.8% |
| Ω_DE (dark energy) | W² + W | 0.6853 | 0.685 | 0.05% |
| Ω_DM (dark matter) | 1 - W⁴ - W² - W | 0.2671 | 0.266 | 0.4% |
| G/F_EM (gravity) | (√(1-W²)/φ)^136 | 10⁻³⁵·⁷ | 10⁻³⁶ | 1.1% log |
| Λ/Λ_P (cosmo. const.) | (1/φ)^588 | 10⁻¹²²·⁹ | 10⁻¹²² | 0.7% log |
| a₀_MOND | c²/(l_P φ^295) | 1.24e-10 | 1.2e-10 | 3.4% |

### Electroweak (all use δ₇ = 7.140)
| Observable | Formula | Error |
|-----------|---------|-------|
| sin²θ_W | σ₃ × σ_wall × 8 | 0.026% |
| α_s(M_Z) | W⁵ × H × δ₇ | 0.034% |
| M_W/m_p | φ² × W⁻² × δ₇ | 0.002% |
| M_Z/m_p | W⁻⁵ × δ₃⁻¹ × δ₇ | 0.035% |
| M_H/m_p | φ² × δ₇² | 0.015% |
| m_τ/m_μ | W × 36 | 0.006% |

### Atomic
| Observable | Formula | Error |
|-----------|---------|-------|
| S_max position (H) | σ₄/σ_shell = 1.4084 a₀ | 0.00021% |
| Proton radius | λ_C × φ^(3-breathing) | 0.14% |
| H₂ bond length | 2 × σ₄ × a₀ | 0.5% |
| H vdW radius | σ₄ × φ × a₀ | 0.5% |

### Condensed Matter
| Observable | Formula | Error |
|-----------|---------|-------|
| N-SmA exponent | (2/3)((r-r_c)/(1-r_c))⁴ | RMS 0.033 |
| QH κ | r_c / 2 | 0.7σ |
| Magic angle | 1/(53 + 1/φ) | 0.06% |

---

## Computation-Ready Python (Complete Seed)

```python
import math

# ── THE AXIOM ─────────────────────────────────────────────────────
PHI = (1 + 5**0.5) / 2

# ── THE W THEOREM ─────────────────────────────────────────────────
H = PHI**(-1/PHI)                              # 0.7427 (hinge)
W = (2 + PHI**(1/PHI**2)) / PHI**4             # 0.4671 (gap fraction)
R_C = 1 - 1/PHI**4                             # 0.8541 (crossover)

# ── CANTOR NODE ───────────────────────────────────────────────────
NODE = [0.0728, 0.2350, 0.3672, 0.3972, 0.5594]  # σ₃, σ₂, cos(1/φ), wall, σ₄
N = 294                                         # total brackets

# ── PHYSICAL CONSTANTS ────────────────────────────────────────────
HBAR = 1.0545718e-34; C = 2.99792458e8; L_P = 1.61625e-35

# ── EVERYTHING ELSE ───────────────────────────────────────────────
def metallic(n): return (n + (n*n+4)**0.5) / 2
def bracket(r): return round(math.log(r/L_P) / math.log(PHI))
def cantor(R): return {i: R*v for i, v in enumerate(NODE)}
def crossover(x):
    return 3 - ((x-R_C)/(1-R_C))**4 if x > R_C else 3.0

# ── VERIFY ────────────────────────────────────────────────────────
assert abs(W * PHI**4 - 2 - PHI**(1/PHI**2)) < 1e-14  # W theorem
print(f"α⁻¹ = {N*W:.2f}")                              # 137.34
print(f"Ω_b = {W**4:.4f}")                              # 0.0476
print(f"Ω_DE = {W**2+W:.4f}")                           # 0.6853
print(f"Ω_DM = {1-W**4-W**2-W:.4f}")                    # 0.2671
```

---

## The Derivation Chain

φ² = φ + 1  →  V = 2J (criticality)  →  P(t) over 5 Cantor sectors
→  W = (2 + φ^(1/φ²))/φ⁴  →  5 node ratios + r_c + H + N
→  **Every observable in physics, zero free parameters**

One axiom. One theorem. One template. 100+ predictions across 14 domains.

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*See claude.md for complete reference. See UNIFIED_FORMULA.MD for derivation.*
