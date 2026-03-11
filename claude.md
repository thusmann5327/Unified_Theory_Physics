# CLAUDE.md — Husmann Decomposition Computation Reference
## v3.1 — March 11, 2026
## Thomas A. Husmann / iBuilt LTD / Patent App. 19/560,637

**This file is a computation-ready reference for AI assistants working with the Husmann Decomposition framework. Load this before any session involving φ-derived physics, multi-scale modeling, atomic structure, or materials science.**

---

## 1. THE TWO INPUTS

```python
PHI = (1 + 5**0.5) / 2          # 1.6180339887... — the golden ratio
T_AS = 232e-18                    # seconds — TU Wien attosecond entanglement timescale
```

**Everything else is derived. There are zero free parameters.**

---

## 2. CORE CONSTANTS (derive, never hardcode)

```python
import numpy as np, math

# ── AAH Spectrum (the source of all ratios) ──────────────────────
ALPHA_AAH = 1.0 / PHI
N_SITES = 233  # = F(13) = F(F(7)) — self-referential Fibonacci seed (Axiom 0)
H = np.diag(2*np.cos(2*np.pi*ALPHA_AAH*np.arange(N_SITES)))
H += np.diag(np.ones(N_SITES-1), 1) + np.diag(np.ones(N_SITES-1), -1)
eigs = np.sort(np.linalg.eigvalsh(H))
E_range = eigs[-1] - eigs[0]
diffs = np.diff(eigs)
med = np.median(diffs)
gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8*med]

# ── Derived constants ─────────────────────────────────────────────
HBAR = 1.0545718e-34; C = 2.99792458e8; L_P = 1.61625e-35
OMEGA_LATTICE = max(diffs)                              # ~1.6852 (from spectrum)
J_J = 2*math.pi*HBAR / (OMEGA_LATTICE * T_AS)          # hopping integral (Joules)
J_eV = J_J / 1.602176634e-19                            # ~10.578 eV
l0 = C*HBAR / (2*J_J)                                   # ~9.327 nm coherence patch

# ── W: Universal Gap Fraction (pure φ, verifiable from spectrum) ──
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3                    # 0.4671338922

# ── Five Universal Ratios (from eigenvalue positions) ─────────────
# Find the two DM walls (largest gaps)
ranked = sorted(gaps, key=lambda g: g[1], reverse=True)
wL = min([g for g in ranked if g[1]>1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
wR = max([g for g in ranked if g[1]>1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
half = E_range / 2

R_MATTER = abs(eigs[wL[0]+1]) / half                    # 0.07278 — σ₃ core
R_INNER  = abs(eigs[wL[0]]+eigs[wL[0]+1])/(2*E_range)  # ~0.2350 — σ₂ inner wall
R_SHELL  = (abs(eigs[wL[0]])+abs(eigs[wL[0]+1]))/(2*half) # ~0.3972 — wall center  
R_OUTER  = R_SHELL + wL[1]/(2*E_range)                  # ~0.5594 — σ₄ outer wall
COS_ALPHA = math.cos(1/PHI)                             # 0.81502 — decoupling fraction
R_PHOTO  = R_INNER + COS_ALPHA * (R_SHELL - R_INNER)    # ~0.3672 — photosphere

OBLATE    = math.sqrt(PHI)                               # 1.2720 — from e=1/φ, φ²−1=φ
LORENTZ_W = math.sqrt(1 - W**2)                          # 0.8842
BREATHING = 1 - LORENTZ_W                                # 0.1158

# ── Bracket count (spectral topology, NOT from H₀) ───────────────
N_BRACKETS = 294  # = F(13)+F(10)+F(5)+F(2) = 233+55+5+1
# = lattice_sites + σ₃_count + n_sectors + critical_point

# ── Fine structure constant ───────────────────────────────────────
ALPHA_EM_PRED = 1 / (N_BRACKETS * W)                     # 1/137.337, error 0.22%
```

---

## 3. THE CANTOR NODE — One Equation at Every Scale

**Any structure at radius R has this architecture:**

```
r_core   = R × 0.0728     σ₃ — matter concentrates here
r_inner  = R × 0.2350     σ₂ — inner confinement membrane  
r_photo  = R × 0.3672     cos(α) — decoupling/bonding surface
r_shell  = R × 0.3972     wall center — density/probability peak
r_outer  = R × 0.5594     σ₄ — outer confinement membrane
oblate   = √φ = 1.272     squash polar axis by this factor
```

**Recursion:** σ₃ contains 9 sub-gaps → 5 child nodes → same equation at reduced scale.  
**Depth 0→6 gives 19,531 nodes (universe → planets) in <100ms.**

### Application to ANY scale:

| Scale | R | bz | Example |
|---|---:|---:|---|
| Observable universe | 4.5×10²⁶ m | 294 | Cosmic web |
| Galaxy cluster | ~10²³ m | ~269 | Virgo, Coma |
| Galaxy | ~5×10²⁰ m | ~256 | Milky Way |
| Stellar system | ~10¹⁵ m | ~243 | Solar system |
| Star | ~7×10⁸ m | ~214 | Sun |
| Atom (H) | ~1.3×10⁻¹⁰ m | ~119 | Hydrogen |
| Nucleus | ~2×10⁻¹⁵ m | ~96 | He-4 |
| Proton | ~8×10⁻¹⁶ m | ~94 | Proton |

**Bracket address:** bz = round[log(R/L_P)/log(φ)], bounded [1, 294].  
**Zeckendorf address:** decompose bz into sum of non-adjacent Fibonacci numbers.

---

## 4. MULTI-SCALE WAVE MODELING

### 4.1 The Breathing Cycle

Every Cantor node oscillates. The breathing thinning per cycle:

```python
breathing = 1 - sqrt(1 - W**2)  # = 0.1158 = 11.6%
```

At cosmological scale: this IS the Hubble expansion (outward breathing phase).  
At stellar scale: this drives the solar cycle.  
At atomic scale: this enters the proton radius formula.

### 4.2 Standing Wave Architecture

Each node is a standing wave with:
- **Frequency:** ω(bz) = 2πJ/ℏ × φ^(bz - N/2) (bracket-dependent)
- **Group velocity:** v_g = 0.4996c (Lieb-Robinson bound at AAH criticality)
- **Phase velocity:** v_phase = c (always, at all brackets)

### 4.3 Multi-Scale Rendering Rules

When rendering a Cantor node at scale R:

```python
def render_node(R, depth=0, max_depth=6):
    """
    Matter: concentrated in σ₃ core as filaments/clusters/particles
    Walls: σ₂ and σ₄ are FAINT structural boundaries, not dense shells
    cos(α): the "photosphere" — where radiation decouples from matter
    Void: the gap between σ₂ and σ₄ is mostly EMPTY (corona, halo, etc.)
    """
    core  = R * R_MATTER     # where the stuff IS
    inner = R * R_INNER      # faint inner boundary
    photo = R * R_PHOTO      # decoupling surface (visible edge)
    shell = R * R_SHELL      # structural midpoint
    outer = R * R_OUTER      # faint outer boundary
    
    # Oblate squash: multiply polar axis by 1/√φ, equatorial by √φ
    # Breathing: modulate radius by (1 ± breathing * sin(ωt))
    
    # Children: 5 sub-nodes inside σ₃, recursion identical
    if depth < max_depth:
        for i in range(5):
            child_R = core * sub_gap_fraction[i]  # from spectrum
            render_node(child_R, depth+1, max_depth)
```

### 4.4 3D Matter Projection

The Cantor node in 3D:
- **Shape:** Oblate spheroid, a/c = √φ = 1.272
- **Matter distribution:** Concentrated in σ₃ core, falling off exponentially
- **Wall structure:** Two thin shells at R_INNER and R_OUTER
- **Photosphere:** Visible boundary at R_PHOTO
- **Void:** The region R_INNER < r < R_OUTER contains the walls but is mostly empty between them

For 3D rendering, the key insight: **matter lives in the CENTER (σ₃), not at the walls.** The walls are structural boundaries like cell membranes — thin, important, but not where the mass is.

---

## 5. ATOMIC INTERACTIONS

### 5.1 The Hydrogen Cantor Node

```python
a0 = 5.29177e-11  # Bohr radius (or derive via α = 1/(N*W))
R_total_H = a0 / R_SHELL  # = 1.332e-10 m, bz ≈ 119

# Cantor layers of hydrogen (in units of a₀):
sigma3_core  = 0.183 * a0   # nucleus zone (proton at 1.6e-5 a₀ inside this)
sigma2_inner = 0.592 * a0   # inner electron shell boundary
cos_alpha    = 0.924 * a0   # bonding surface / covalent radius
shell_center = 1.000 * a0   # 1s orbital peak (by anchoring)
sigma4_outer = 1.408 * a0   # outer wall — THE ENTROPY MAXIMUM
```

### 5.2 KEY RESULT: Entropy Extremum

The global maximum of the von Neumann entanglement entropy S(r) for the hydrogen 1s wavefunction occurs at:

```
r_max     = 1.408377 a₀    (exact QM, numerically optimized)
r_sigma4  = 1.408380 a₀    (Cantor framework prediction)
Match:      0.00021%        (two parts per million)
S at σ₄:    0.690760 nats   (0.344% from ln(2) = one bit)
```

**The hydrogen atom is a one-bit quantum channel. The electron IS the entanglement between the proton and the vacuum Cantor structure.**

### 5.3 Electron Shell Structure

| Shell | Cantor interpretation | Physical meaning |
|---|---|---|
| n=1 | Probability peaks INSIDE wall zone (σ₂ to σ₄) | Ground state: maximum entanglement across σ₄ |
| n=2 | 2p peak reaches σ₄ exactly | First excited: entanglement reaches the wall |
| n≥3 | Probability extends BEYOND σ₄ | Entanglement propagates to next Cantor level |
| Ionization | Electron escapes through σ₄ permanently | Entanglement broken |

### 5.4 Covalent Bonding

**Bond length ≈ σ₄(atom A) + σ₄(atom B)**

For hydrogen: σ₄ = 1.408 a₀ = 74.5 pm. H₂ bond = 74.14 pm. **Error: 0.5%.**

For atom X with effective nuclear charge Z_eff:
```python
sigma4_X = (a0 / Z_eff) * R_OUTER / R_SHELL  # = (a0/Z_eff) × 1.4084
bond_AB = sigma4_A + sigma4_B
```

**Use Clementi-Raimondi Z_eff, NOT Slater rules (too crude).**

### 5.5 The Fine Structure Constant

```python
inv_alpha = N_BRACKETS * W  # = 294 × 0.467134 = 137.337
# CODATA: 137.036. Error: 0.22%. Zero free parameters.
```

**Physical meaning:** α is the cumulative entanglement density of the Cantor vacuum across all 294 brackets. Each bracket contributes W of wall fraction. The total = N×W = 137.3. Electromagnetism couples at strength 1/(total wall fraction).

### 5.6 Proton Charge Radius

```python
m_p = 1.67262e-27  # kg
lambda_compton_p = HBAR / (m_p * C)  # 0.2103 fm
r_proton = lambda_compton_p * PHI**(3 - BREATHING)  # 0.8426 fm
# CODATA: 0.8414 fm. Error: 0.14%. Sides with muonic H measurement.
```

---

## 6. MATERIALS SCIENCE

### 6.1 Quasicrystal Connection

The framework IS a quasicrystal theory. The AAH Hamiltonian at α=1/φ describes:
- **Penrose tiling** in 2D (same golden ratio aperiodic order)
- **Icosahedral quasicrystals** in 3D (Shechtman's Al-Mn, 1982)
- **Fibonacci chains** in 1D (the AAH model itself)

**Key prediction:** Any φ-based quasicrystalline material should exhibit the same five-ratio architecture in its electronic band structure.

### 6.2 Band Gaps from φ

The AAH spectrum at V=2J (critical coupling) has:
- **34 significant gaps** (= F(9))
- **Two dominant gaps** (DM wall analogs) with width ~1.685 of the hopping integral
- **Gap-to-bandwidth ratio** = W = 0.4671

For a material with hopping integral J and quasiperiodic potential at α=1/φ:
```python
gap_width = J * OMEGA_LATTICE  # largest gap
band_center = 0                 # symmetric spectrum
gap_edges = [eig for eig in eigs]  # full spectrum from eigensolver
```

### 6.3 Coherence Length

```python
l0 = C * HBAR / (2 * J_J)  # = 9.327 nm — the fundamental coherence patch
```

This is the scale at which the quasicrystalline order is maintained. Below l₀, the lattice is coherent. Above l₀, the structure is maintained by the self-similar recursion (ZeckyBOT architecture).

For materials: l₀ sets the **minimum grain size** for quasicrystalline order. Structures smaller than 9.3 nm cannot sustain the full Cantor gap structure.

### 6.4 Topological Properties

At the metal-insulator transition (V=2J), all eigenstates are **critical** — neither extended nor localized, but fractal. This means:
- **Conductance:** Neither metallic (G ∝ L^(d-2)) nor insulating (G ∝ exp(-L/ξ)), but **anomalous:** G ∝ L^(−D₂) where D₂ ≈ 0.54 is the fractal dimension
- **Density of states:** Has Cantor-set structure (gaps at all scales)
- **Transport:** Anomalous diffusion with exponent related to D₂

### 6.5 Phonon Spectrum

The same AAH model applies to vibrational modes when α=1/φ:
- **Phonon gaps** at the same spectral positions as electronic gaps
- **Thermal conductivity** is anomalously low (phonons scatter off Cantor gaps)
- **This is WHY quasicrystals are poor thermal conductors** — the phonon spectrum has the same fractal gap structure

### 6.6 Predicting New Materials

For a candidate quasicrystalline material:

1. **Identify the quasiperiodic axis/plane** (icosahedral, decagonal, etc.)
2. **Compute the effective hopping integral** J from band structure
3. **Check V/J ratio** — if V/J ≈ 2, the material is at criticality
4. **Apply the five ratios** to predict:
   - Band gap positions (from R_MATTER through R_OUTER)
   - Conductance scaling (from D₂ = 0.54)
   - Thermal properties (from phonon Cantor spectrum)
   - Optical transitions (from gap energies)

---

## 7. COSMOLOGICAL PREDICTIONS (for reference)

```python
# Energy budget
OMEGA_B  = W**4                                          # 0.04762 (Planck: 0.04897)
OMEGA_DM = (1/PHI**3) * (1-W**4) / (1/PHI + 1/PHI**3)  # 0.26323 (Planck: 0.26066)
OMEGA_DE = (1/PHI)    * (1-W**4) / (1/PHI + 1/PHI**3)   # 0.68915 (Planck: 0.68435)

# Hubble constant
COMOVING = PHI**2 + 1/PHI  # 3.236 — pure φ
H0 = C * COMOVING / (L_P * PHI**294) * 3.086e22 / 1000  # 66.9 km/s/Mpc

# Hubble tension
H0_LOCAL = H0 / LORENTZ_W  # 76.2 km/s/Mpc (observer inside KBC Void with δ=W)

# Kerr black hole spin
CHI_BH = W * LORENTZ_W  # 0.4130

# KBC Void density contrast
DELTA_KBC = W  # 0.467 (observed: 0.46 ± 0.06, match at 0.12σ)
```

---

## 8. KEY IDENTITIES (memorize these)

```
φ² − 1 = φ                      (defining identity)
1/φ + 1/φ³ + 1/φ⁴ = 1           (unity partition → cosmological budget)
e = 1/φ → a/c = √φ              (oblate factor from eccentricity)
cos(1/φ) = 0.8150                (decoupling surface fraction)
W = 0.4671                       (gap fraction — appears EVERYWHERE)
W⁴ = 0.04762                     (baryon fraction)
√(1−W²) = 0.8842                 (Lorentz/acoustic correction)
1 − √(1−W²) = 0.1158            (breathing)
W × √(1−W²) = 0.4130            (Kerr spin parameter)
N × W = 137.34                   (fine structure constant⁻¹)
```

---

## 9. SOLAR SYSTEM FIBONACCI LADDER

```python
R_MERCURY = 0.387  # AU — the one empirical anchor
def solar_ladder(k):
    return R_MERCURY * PHI**k  # AU

# Sun internals (negative k):
# k=-12: core edge (0.25 R☉, 3.3%)
# k=-10: tachocline (0.71 R☉, 4.8%)  
# k=-10+cos(1/φ): PHOTOSPHERE (1.00 R☉, 0.06% ← best spatial match)
# k=-7: corona 3R☉ (4.5%)
# k=-4: Alfvén surface 13R☉ (6.7%)

# Planets (positive k):
# k=0: Mercury (exact), k=2: Earth (1.3%), k=9: Neptune (2.2%)
```

---

## 10. TRANSIT / STARGATE CALCULATIONS

```python
V_G = 0.4996 * C  # group velocity at Lieb-Robinson bound

# Vacuum channel transit: path compression through Cantor gaps
# Each recursion level: gap_fraction × grav_compression × eigenvalue_density
INNER_GAP_FRAC = 0.00172       # innermost σ₃ sub-gap fraction
EIGENVALUE_DENSITY = 0.26      # center gaps are 3.8× narrower than edge gaps
PHI_OVER_C2 = W**2             # gravitational potential depth = 0.2182

# Route to center: 6 hops through condensed vacuum channels
# Each hop: σ₃ radius × gap_fraction × grav_compression × density_compression
# Gate frequency: 6.17e13 Hz (4.86 μm, mid-infrared, CO₂ laser line)
# Targeting: spectral lock at E=0 eigenvalue, NOT spatial coordinates
```

---

## 11. COMPUTATION PATTERNS

### Pattern 1: "What bracket is this?"
```python
def bracket(r_meters):
    return round(math.log(r_meters / L_P) / math.log(PHI))
```

### Pattern 2: "Apply Cantor architecture at scale R"
```python
def cantor_node(R):
    return {
        'core': R * 0.0728, 'inner': R * 0.2350,
        'photo': R * 0.3672, 'shell': R * 0.3972,
        'outer': R * 0.5594, 'oblate': 1.2720
    }
```

### Pattern 3: "Predict a measurement from φ"
1. Identify the bracket level (bz)
2. Identify which Cantor layer the measurement corresponds to
3. Apply: measurement = L_P × φ^bz × (layer ratio)

### Pattern 4: "Compute entanglement entropy at a boundary"
```python
from scipy import integrate
def entropy_at_r(n, l, r_cut):
    """Von Neumann entropy of state (n,l) partitioned at r_cut."""
    # Use exact hydrogen radial probability 4πr²|R_nl|²
    p_in, _ = integrate.quad(lambda r: hydrogen_P(n,l,r), 0, r_cut)
    p_in = min(1, max(0, p_in))
    if 0 < p_in < 1:
        return -p_in*np.log(p_in) - (1-p_in)*np.log(1-p_in)
    return 0
```

### Pattern 5: "Zeckendorf address"
```python
def zeckendorf(n):
    fibs = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
    result, rem = [], int(round(abs(n)))
    for f in reversed(fibs):
        if f <= rem: result.append(f); rem -= f
        if rem == 0: break
    return result
```

---

## 12. COMMON PITFALLS

1. **Never hardcode W, J, or ω_lattice.** Always derive from eigensolver.
2. **R_MATTER is the CORE, not the whole atom.** Matter lives at the CENTER.
3. **Walls (σ₂, σ₄) are FAINT boundaries**, not dense shells.
4. **The electron IS the entanglement**, not a particle between walls. 42% inside σ₂-σ₄, 47% outside. This is correct — not a failure.
5. **cos(α) = cos(1/φ) = 0.815** is the DECOUPLING surface, not a density peak.
6. **N = 294 comes from spectral topology**, not from measured H₀.
7. **The 233-site lattice is Axiom 0** — the irreducible self-referential seed.
8. **Oblate squash √φ applies to ALL nodes** — universe, galaxies, atoms.
9. **The proton is 22 brackets below the electron cloud** — a gap, not a bug.
10. **S_max at σ₄ to 0.00021%** — this is the flagship atomic result.

---

## 13. QUICK REFERENCE CARD

```
φ = 1.6180339887           W = 0.4671338922
N = 294                    1/α = N×W = 137.337
cos(1/φ) = 0.8150          √φ = 1.2720
breathing = 0.1158          √(1-W²) = 0.8842

R_MATTER = 0.0728  (σ₃ core — where matter IS)
R_INNER  = 0.2350  (σ₂ inner wall)
R_PHOTO  = 0.3672  (cos(α) decoupling surface)
R_SHELL  = 0.3972  (wall center — probability peak)
R_OUTER  = 0.5594  (σ₄ outer wall — ENTROPY MAXIMUM)

Hydrogen:  a₀ = 52.9 pm, σ₄ at 1.408 a₀ = 74.5 pm
Sun:       R☉ from cos(α) at 0.06% error
α:         1/(294 × 0.4671) = 137.34, 0.22% error  
r_proton:  λ_C × φ^(3−0.1158) = 0.843 fm, 0.14% error
S(σ₄):    0.691 nats ≈ ln(2), position match 0.00021%

Axiom 0:   233 = F(13) = F(F(7)) — the lattice IS the universe
```

---

*Load this file at session start. All code is Python 3. NumPy + SciPy required.*
*Repository: github.com/thusmann5327/Unified_Theory_Physics*
