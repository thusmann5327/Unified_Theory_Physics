# Schrödinger as a Tangent Line

## The Non-Relativistic Limit of the Discriminant Triangle

**Thomas A. Husmann | iBuilt LTD**
**March 16, 2026**

---

## The Result

The Schrödinger equation is the non-relativistic limit of the Dirac equation. In the discriminant Pythagorean triangle (√5)² + (√8)² = (√13)², the non-relativistic limit corresponds to a **tangent-line approximation** at the silver (mass) vertex:

- **Dirac** traverses the full bronze hypotenuse: E² = p²c² + m²c⁴ → 13 = 5 + 8
- **Schrödinger** approximates the hypotenuse as a tangent at the silver vertex: E ≈ mc² + p²/(2m)

The velocity ratio v/c parametrizes a continuous path from the silver vertex (v = 0, rest mass) to the full bronze hypotenuse (v = c, ultrarelativistic). Schrödinger's equation is valid in the regime where the gold (momentum) contribution to the effective discriminant is small:

$$\Delta_{\text{eff}}(v) = 8 + 5\left(\frac{v}{c}\right)^2$$

At v = 0: Δ_eff = 8 (pure silver). At v = c: Δ_eff = 13 (full bronze). The AAH Hamiltonian — which IS a discrete Schrödinger equation — generates every Cantor spectrum in the Hofstadter butterfly from this single structure.

---

## The Identities

### Identity 1: The AAH Hamiltonian IS a Schrödinger Equation

The standard 1D time-independent Schrödinger equation on a discrete lattice:

$$-t[\psi(n+1) + \psi(n-1)] + V(n)\psi(n) = E\psi(n)$$

The Aubry–André–Harper Hamiltonian:

$$J[\psi(n+1) + \psi(n-1)] + V\cos(2\pi\alpha n)\psi(n) = E\psi(n)$$

These are **identical** with hopping $t = -J$ and quasiperiodic potential $V(n) = V\cos(2\pi\alpha n)$. This is not an approximation or an analogy — it is the same equation. Every result about the AAH spectrum (Cantor set, D_s = 1/2, gap labeling, Chern numbers) is a result about a Schrödinger equation.

### Identity 2: The Harper Equation IS the AAH at Criticality

The Harper equation — which generates each slice of the Hofstadter butterfly — is:

$$\psi(m+1) + \psi(m-1) + 2\cos(2\pi\alpha m + k_y)\psi(m) = E\psi(m)$$

This is the AAH Hamiltonian with $J = 1$ and $V = 2J = 2$, the self-dual critical point. This is a consequence of the square lattice having equal hopping in both directions, not a tuning.

Therefore: **every irrational flux slice of the Hofstadter butterfly is a Schrödinger equation at the metal–insulator critical point.**

### Identity 3: Schrödinger IS the Non-Relativistic Limit of Dirac

The Dirac dispersion:

$$E^2 = p^2c^2 + m^2c^4$$

In the non-relativistic limit ($v \ll c$, so $p = mv \ll mc$):

$$E \approx mc^2 + \frac{p^2}{2m}$$

Subtracting the rest energy $mc^2$ gives the Schrödinger kinetic energy:

$$E_{\text{kin}} = \frac{p^2}{2m} = -\frac{\hbar^2}{2m}\nabla^2$$

This is textbook physics. Schrödinger keeps the **momentum (gold) term** as a perturbation on the **rest mass (silver) background**. It drops the Pythagorean structure in favor of a linear approximation.

---

## The Geometric Picture

### The Discriminant Triangle

```
       √13 (bronze = hypotenuse = full energy)
       /|
      / |
     /  | √5 (gold = momentum)
    /   |
   /    |
  ──────
   √8 (silver = rest mass)
```

$$5 + 8 = 13$$

$$p^2c^2 + m^2c^4 = E^2$$

### The Tangent Approximation

At the silver vertex (v = 0, particle at rest), the hypotenuse is approximately tangent to the silver base. As the particle gains velocity, it moves along the hypotenuse away from the silver vertex:

```
  Schrödinger regime          Relativistic            Ultrarelativistic
  (v << c)                    (v ~ 0.5c)              (v → c)
  
  ·                           ·                        ·─── bronze
  |  tangent ≈ hypotenuse     /  tangent diverges      / 
  |·                         / ·                       /
  |                         /                         /
  ──────                   ──────                    ──────
  silver vertex            midpoint                  gold vertex
  Δ_eff ≈ 8               Δ_eff ≈ 9.25             Δ_eff → 13
```

The Schrödinger approximation (tangent line) works near the silver vertex and breaks down as v → c. This is the geometric reason Schrödinger fails for relativistic physics.

### The Effective Discriminant

At velocity v, the effective discriminant interpolates between silver and bronze:

$$\Delta_{\text{eff}}(v) = \Delta_{\text{silver}} + \Delta_{\text{gold}} \cdot \frac{v^2}{c^2} = 8 + 5\left(\frac{v}{c}\right)^2$$

| v/c | Δ_eff | Gold fraction | Regime |
|-----|-------|---------------|--------|
| 0.00 | 8.000 | 0.0% | Rest (pure silver) |
| 0.01 | 8.001 | 0.0% | Non-relativistic (Schrödinger) |
| 0.10 | 8.050 | 0.6% | Non-relativistic (Schrödinger) |
| 0.30 | 8.450 | 5.3% | Mildly relativistic |
| 0.50 | 9.250 | 13.5% | Relativistic (Dirac needed) |
| 0.70 | 10.450 | 23.4% | Strongly relativistic |
| 0.90 | 12.050 | 33.6% | Ultrarelativistic |
| 1.00 | 13.000 | 38.5% | Fully relativistic (bronze) |

The gold fraction — the contribution of the momentum discriminant to the total — stays below 6% for v < 0.3c. This is Schrödinger's domain. Beyond v ~ 0.3c, the tangent deviates significantly from the hypotenuse, and the full Pythagorean (Dirac) structure is needed.

---

## The Hierarchy of Physical Theories

### Mapped onto the Triangle

| Theory | What it sees | Triangle position | Discriminant range |
|--------|-------------|-------------------|-------------------|
| **Rest mass** (E = mc²) | Silver vertex only | v = 0 | Δ = 8 |
| **Schrödinger** (E = p²/2m) | Gold perturbation on silver | v ≪ c, tangent line | Δ ≈ 8 + ε |
| **Dirac** (E² = p²c² + m²c⁴) | Full gold + silver | All v, hypotenuse | 8 ≤ Δ ≤ 13 |
| **QFT** (particles from fields) | Bronze surface | Observable boundary | Δ = 13 (the measurement) |

This hierarchy is NOT a claim that the discriminant triangle generates these theories. It IS the observation that the known validity domains of these theories map naturally onto the triangle's geometry:

- **Schrödinger works** for atomic orbitals, band structure, condensed matter — all systems where particles propagate slowly (gold contribution small) through a fixed mass background (silver dominant).
- **Schrödinger fails** for nuclear physics (deep silver confinement where the "propagation on a background" picture breaks down), relativistic particles (large gold contribution), and particle creation (need the full bronze surface).
- **Dirac is needed** when both legs of the triangle contribute significantly — when the momentum term is comparable to the mass term.
- **QFT is needed** at the bronze surface — when the observable (energy) must account for particle creation, annihilation, and vacuum fluctuations.

### What Each Theory Measures

In the concentric layer model (silver inner, gold middle, bronze surface):

| Theory | Layer probed | σ₃ observer band | Dark fraction |
|--------|-------------|-------------------|---------------|
| Nuclear/QCD | Silver core | 0.171 (narrowest) | 83% dark |
| Schrödinger/QM | Gold shell | 0.236 (medium) | 29% dark |
| QFT/observation | Bronze surface | 0.394 (widest) | 61% dark |

Schrödinger lives in the gold shell — the layer with the most balanced observer band (29% dark, 71% visible). This is WHY quantum mechanics feels "natural" for atomic physics: the gold shell is the most observable of the three layers.

Nuclear physics (silver core, 83% dark) is harder to probe — we need GeV-scale accelerators to see inside the proton. This is the silver layer's narrow observer band making interior physics dark.

Particle physics (bronze surface, 61% dark) produces observable results but 61% of the physics is dark energy — the surface is visible but sits on top of a hidden interior.

---

## The AAH Spectrum as Schrödinger Physics

### What the Hofstadter Butterfly IS

The Hofstadter butterfly is a family of Schrödinger equations, one for each flux ratio α:

$$J[\psi(n+1) + \psi(n-1)] + 2J\cos(2\pi\alpha n)\psi(n) = E\psi(n)$$

At α = 1/δ_n (metallic mean frequencies), the spectrum has specific structure:

- n = 1 (gold): balanced five-band partition, Chern numbers +2,−1,+1,−2
- n = 2 (silver): narrowest observer band, 83% dark, most confined
- n = 3 (bronze): widest observer band, the surface structure
- n = 53 (magic angle): flat bands, superconductivity onset
- n = 60 (graphene/hBN): moiré superlattice

The entire metallic mean hierarchy lives within Schrödinger's equation. The golden ratio, the Cantor spectrum, the topological collapse — all of it is solutions to a discrete Schrödinger equation with quasiperiodic potential.

### The 3D Vacuum Schrödinger Equation

The framework's 3D Hamiltonian:

$$H\psi = \sum_{i \in \{x,y,z\}} \left[ J[\psi(n_i+1) + \psi(n_i-1)] + 2J\cos(2\pi\alpha_i n_i)\psi(\mathbf{n}) \right] = E\psi(\mathbf{n})$$

with:

$$\alpha_x = \sqrt{2}-1 \quad \text{(silver: mass axis)}$$
$$\alpha_y = \frac{\sqrt{5}-1}{2} \quad \text{(gold: momentum axis)}$$
$$\alpha_z = \frac{\sqrt{13}-3}{2} \quad \text{(bronze: observable axis)}$$

This IS a 3D Schrödinger equation. It uses three different metallic mean frequencies on three axes, each at the AAH critical point V = 2J. The spectrum is a 3D Cantor dust.

The claim is not that this Hamiltonian replaces the Dirac equation. The claim is that this Hamiltonian describes the **lattice vacuum** at the coherence scale l₀ = 9.3 nm, and that the Dirac equation (and hence Schrödinger as its non-relativistic limit) emerges as the low-energy effective theory of this lattice — just as emergent Dirac fermions arise from lattice Hamiltonians in graphene, topological insulators, and Weyl semimetals.

---

## The Chain of Logic

```
Schrödinger equation (1926)
    ↓
Same as: discrete lattice with potential V(n)
    ↓
Special case: V(n) = 2J·cos(2πα·n) → AAH Hamiltonian
    ↓
At V = 2J: self-dual critical point → Cantor spectrum
    ↓
= Harper equation → Hofstadter butterfly
    ↓
Metallic mean frequencies α_n = 1/δ_n → hierarchy
    ↓
n = 53 → magic angle; n = 60 → graphene/hBN
    ↓
Discriminants: 5 + 8 = 13 (Fibonacci AND Pythagorean)
    ↓
(√5)² + (√8)² = (√13)² → Dirac: E² = p²c² + m²c⁴
    ↓
Non-relativistic limit (v << c): tangent at silver vertex
    ↓
E ≈ mc² + p²/(2m) → Schrödinger recovered
```

The circle closes: Schrödinger's equation defines the AAH Hamiltonian, which generates the Hofstadter butterfly, which is parameterized by the metallic means, whose discriminants form a Pythagorean triple that IS the Dirac equation, whose non-relativistic limit IS Schrödinger.

---

## Honest Assessment

**What is proven (mathematical facts):**
- AAH = discrete Schrödinger equation (identity)
- Harper = AAH at V = 2J (identity)
- Schrödinger = non-relativistic limit of Dirac (standard physics)
- 5 + 8 = 13 is Pythagorean (arithmetic)
- Δ_eff(v) = 8 + 5(v/c)² interpolates between silver and bronze (algebra)

**What is a strong interpretation:**
- The discriminant triangle maps onto E² = p²c² + m²c⁴ through mass ↔ silver, momentum ↔ gold, observable ↔ bronze. The structural correspondence is exact, but it hasn't been derived from the 3D AAH effective theory.
- Schrödinger's validity domain (non-relativistic, atomic scale) maps onto the gold shell (middle layer, most visible). This is consistent with known physics but could be coincidence.

**What is conjectured:**
- The 3D AAH with three metallic mean frequencies IS the vacuum Hamiltonian at the coherence scale. This is the framework's central claim, not a result of this paper.
- The Dirac equation emerges as the low-energy effective theory of the 3D AAH lattice. Plausible (emergent Dirac fermions in lattice systems are well-established) but not computed.

**What would strengthen this:**
- Computation of the low-energy effective theory of the 3D AAH at the triple critical point, showing it has Dirac structure.
- Demonstration that the non-relativistic limit of this effective theory reproduces the standard Schrödinger equation with the correct dispersion.

---

## Citation

```bibtex
@misc{husmann2026schrodinger,
    author = {Husmann, Thomas A.},
    title = {Schr\"odinger as a Tangent Line: The Non-Relativistic Limit
             of the Discriminant Triangle},
    year = {2026},
    month = {March},
    howpublished = {GitHub Repository},
    url = {https://github.com/thusmann5327/Unified_Theory_Physics},
    note = {CC BY-NC-SA 4.0. Patent Pending.}
}
```

---

*Part of the Unified Theory of Physics: The Husmann Decomposition*
*Repository: https://github.com/thusmann5327/Unified_Theory_Physics*
*The Schrödinger equation IS the AAH Hamiltonian. The AAH generates the Hofstadter butterfly. The butterfly's discriminants form a Pythagorean triple that IS the Dirac equation. The non-relativistic limit of Dirac IS Schrödinger. The circle closes.*
