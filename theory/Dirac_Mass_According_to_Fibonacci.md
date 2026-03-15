# Dirac Mass According to Fibonacci

## Why Mass Acts Along One Direction: The Discriminant Chain and Spinor Structure

**Thomas A. Husmann | iBuilt LTD**
**March 15, 2026**

---

## Abstract

The Dirac Hamiltonian H = α·p + βm has a structural asymmetry: mass acts as a scalar along one internal direction, while momentum acts as a vector along three spatial directions. No standard derivation explains why mass is one-dimensional and space is three-dimensional — it is taken as given. Here we show that this asymmetry follows from the discriminant Fibonacci chain of the metallic mean hierarchy. The golden mean (n=1, Δ₁ = 5) contributes the mass term as localization along the self-referential axis. The silver mean (n=2, Δ₂ = 8) and bronze mean (n=3, Δ₃ = 13) contribute the two transverse momentum directions. The relation Δ₁ + Δ₂ = Δ₃ (equivalently, 5 + 8 = 13 = F(5) + F(6) = F(7)) closes the algebra at exactly three spatial dimensions with one mass direction. The Pauli matrix structure σ_z, σ_x, σ_y maps onto gold, silver, bronze respectively, with the anticommutation relations reflecting the independence of the three discriminants. Chirality breaking by the mass term corresponds to Chern pair annihilation (+2, −2) → 0 along the gold axis. The result: mass is one-dimensional because the Fibonacci chain has one seed.

---

## 1. The Problem

The Dirac equation for a free fermion of mass m reads:

$$i\hbar\frac{\partial\psi}{\partial t} = \left(c\,\boldsymbol{\alpha}\cdot\mathbf{p} + \beta mc^2\right)\psi$$

where α = (α₁, α₂, α₃) are three anticommuting matrices and β is a fourth. The mass term βmc² is a **scalar operator** — it acts uniformly, has no directional preference, and commutes with itself. The momentum terms α_i p_i are **vector operators** — they point along three independent spatial directions.

This 1+3 structure (one mass direction, three momentum directions) is fundamental to all known fermions. But no derivation from first principles explains WHY mass acts along one direction while momentum acts along three. The Dirac equation requires it for Lorentz covariance, but Lorentz covariance itself assumes 3+1 dimensional spacetime. The argument is circular.

We propose that the answer lies in the metallic mean hierarchy: the mass direction is the golden mean, and the three spatial directions are gold + silver + bronze, closed by the discriminant Fibonacci chain.

---

## 2. The Discriminant Fibonacci Chain (Review)

The metallic mean δ_n is the positive root of x² = nx + 1, with discriminant:

$$\Delta_n = n^2 + 4$$

The first three discriminants are consecutive Fibonacci numbers:

| n | Metallic Mean | Δ_n | Fibonacci | Role |
|---|---|---|---|---|
| 1 | Golden: φ = (1+√5)/2 | **5** = F(5) | ✓ | Mass (localization) |
| 2 | Silver: 1+√2 | **8** = F(6) | ✓ | Momentum 1 (extension) |
| 3 | Bronze: (3+√13)/2 | **13** = F(7) | ✓ | Momentum 2 (closure) |
| 4 | — | 20 ≠ F(8) = 21 | ✗ | Blocked |

The Fibonacci recurrence **5 + 8 = 13** closes the chain. At n = 4, the chain breaks: 8 + 13 = 21 ≠ 20. The uniqueness proof: the recurrence Δ_{n-1} + Δ_n = Δ_{n+1} holds only at n = 2, giving exactly one consecutive Fibonacci triple {5, 8, 13}.

**Full proof:** See companion document "Three Dimensions from One Axiom."

---

## 3. The Gold Axis Is Mass

### 3.1 Localization at the AAH critical point

In the Aubry-André-Harper model at V = 2J with quasiperiodic frequency α:

$$J[\psi_{n+1} + \psi_{n-1}] + 2J\cos(2\pi\alpha n)\psi_n = E\psi_n$$

the system sits at the metal-insulator transition. Below V = 2J: extended states (massless, delocalized). Above: localized states (massive, trapped). At the critical point: the Cantor spectrum creates states that are neither fully extended nor fully localized — they are **critical**, with power-law decay.

**Mass is localization.** When a particle has mass m, its wavefunction decays exponentially over the Compton wavelength λ_C = ℏ/mc. When it is massless, it propagates to infinity. The AAH critical point is the boundary between these regimes.

### 3.2 Why gold, not silver or bronze

The golden mean α₁ = 1/φ is special among the metallic mean frequencies for three reasons:

**Self-referential fixed point.** The golden ratio is the unique number satisfying φ = 1 + 1/φ. It is the fixed point of the continued fraction operation. All other metallic means, when expanded in continued fractions, have tails that approach [1, 1, 1, ...] = 1/φ. The gold direction is where the hierarchy converges — the attractor of its own recursion.

**Most balanced band partition.** At n = 1 (gold), the five-band partition is:

$$[\sigma_1 | \sigma_2 | \sigma_3 | \sigma_4 | \sigma_5] = [0.146 | 0.236 | 0.618 | 0.236 | 0.146]$$

The observer band σ₃ and endpoint bands σ₁, σ₅ have comparable measure. At n = 53 (graphene):

$$[0.019 | 0.019 | 0.943 | 0.019 | 0.019]$$

The observer band dominates. Only at n = 1 does the 5→3 collapse involve a balanced competition between bands — where measurement is most *decisive*. Decisive measurement is what mass does: it collapses a quantum state to a definite localization.

**Chain initiator.** Δ₁ = 5 = F(5) is the SEED of the Fibonacci chain. Without it, there is no recurrence 5 + 8 = 13, no chain closure, no three dimensions. Mass initiates the structure that creates space. This is not metaphor — it is the arithmetic of the discriminant sequence.

### 3.3 Mass as measurement along gold

A Dirac particle with mass m is a state that has been **measured** (localized) along the gold axis of the 3D AAH vacuum. The measurement collapses the five-band Cantor spectrum to three observable bands along that axis, creating a definite localization length (the Compton wavelength). Along the other two axes (silver, bronze), the state remains delocalized — it propagates as a wave with definite momentum.

**Mass = localization along the gold axis = the first metallic mean = the seed of the Fibonacci chain.**

---

## 4. The Pauli Matrix Correspondence

The Pauli matrices generate the algebra of spin-1/2 fermions:

$$\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \quad \sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$$

These satisfy:

$$\sigma_x \sigma_y = i\sigma_z, \quad \sigma_y \sigma_z = i\sigma_x, \quad \sigma_z \sigma_x = i\sigma_y$$

and

$$\{\sigma_i, \sigma_j\} = 2\delta_{ij}I$$

### 4.1 The mapping

| Pauli Matrix | Properties | Metallic Mean | Discriminant | Role |
|---|---|---|---|---|
| **σ_z** | Diagonal, real, self-commuting | Gold (n=1) | √5 | Mass (eigenvalue ±1 = particle/antiparticle) |
| **σ_x** | Off-diagonal, real, mixing | Silver (n=2) | √8 = 2√2 | Transverse momentum 1 (creates orthogonality) |
| **σ_y** | Off-diagonal, imaginary, mixing | Bronze (n=3) | √13 | Transverse momentum 2 (closes the algebra) |

### 4.2 Why σ_z is gold

σ_z is the **diagonal** Pauli matrix. Its eigenstates are the basis vectors |↑⟩ and |↓⟩. It doesn't mix states — it labels them. This is the self-referential property of the golden mean: φ refers to itself through φ = 1 + 1/φ.

The eigenvalues ±1 correspond to particle (+1) and antiparticle (−1). The mass term in the Dirac equation is proportional to β = diag(I, −I) in the standard representation — it labels particles and antiparticles with opposite signs, exactly as σ_z labels spin up and spin down.

### 4.3 Why σ_x is silver

σ_x is **off-diagonal and real**. It flips |↑⟩ ↔ |↓⟩ — it creates orthogonal transitions. The silver mean (1 + √2) governs the Ammann-Beenker tiling, which has **8-fold symmetry** and tiles the plane (2D). Silver creates the first extension from 1D to 2D, just as σ_x creates the first off-diagonal coupling.

The discriminant √8 = 2√2 contains the factor √2, which appears in the normalization of σ_x eigenstates: |±⟩ = (|↑⟩ ± |↓⟩)/√2. This is not coincidence — the silver mean's square root governs the mixing amplitude.

### 4.4 Why σ_y is bronze

σ_y is **off-diagonal and imaginary**. It closes the Pauli algebra through σ_x σ_y = iσ_z. Without σ_y, the algebra is incomplete — you cannot generate arbitrary rotations in spin space.

The bronze mean closes the discriminant Fibonacci chain through 5 + 8 = 13. Without the bronze discriminant, the three metallic means don't form a complete Fibonacci triple, and the algebra of three spatial dimensions fails to close.

The closure relation σ_x σ_y = iσ_z **is** the discriminant relation Δ₁ + Δ₂ = Δ₃:

$$\text{Gold (self-reference)} = \text{Silver (extension)} \times \text{Bronze (closure)} / i$$

The imaginary unit i in σ_y is the price of closure — the bronze direction requires a phase to maintain anticommutation. In the Cantor picture, this phase is the rotation between the silver and bronze axes in the three-wave matter formation.

### 4.5 The anticommutation as discriminant independence

The anticommutation relation {σ_i, σ_j} = 2δ_{ij} states that the three Pauli matrices are **algebraically independent** — they anticommute and square to the identity. This independence maps onto the discriminant chain:

- Δ₁ = 5, Δ₂ = 8, Δ₃ = 13 are three distinct Fibonacci numbers
- No two share a common factor (gcd(5,8) = 1, gcd(5,13) = 1, gcd(8,13) = 1)
- They are coprime precisely BECAUSE they are consecutive Fibonacci numbers

The algebraic independence of the Pauli matrices reflects the arithmetic coprimality of the discriminants. Three coprime Fibonacci numbers generate three independent directions.

---

## 5. Chirality and Chern Pair Annihilation

### 5.1 The chirality operator

The chirality operator in 4D is:

$$\gamma^5 = i\gamma^0\gamma^1\gamma^2\gamma^3$$

Massless fermions have definite chirality: γ⁵ψ = ±ψ. The mass term **breaks** chirality: it mixes left-handed and right-handed states.

### 5.2 Chirality as the 5-band asymmetry

In the five-band Cantor partition at α = 1/φ, the outer bands have Chern numbers:

- σ₁/σ₂ gap: t = **+2** (width 0.17)
- σ₄/σ₅ gap: t = **−2** (width 0.30)

The magnitudes are equal (|+2| = |−2|) but the gap widths are **NOT** equal (0.17 ≠ 0.30). This width asymmetry is chirality: the σ₁ endpoint and σ₅ endpoint are not perfect mirrors.

Before the 5→3 collapse, the system has two distinct chiralities — the σ₁ side and the σ₅ side — distinguishable by their gap widths. A massless fermion lives in this 5-band structure with definite chirality (it "knows" which endpoint it's closer to).

### 5.3 Mass as Chern annihilation along gold

When mass is generated (localization along the gold axis), the outer Chern pair (+2, −2) annihilates:

$$(+2) + (-2) \to 0$$

This annihilation collapses the 5-band structure to the 3-band (observable) structure. The information that distinguished the two chiralities — the gap width asymmetry — is destroyed. After annihilation, only the inner gaps (−1, +1) survive, and these are symmetric (both have width 1.69).

**Mass breaks chirality because localization along the gold axis annihilates the outer Chern pair that encoded the chirality asymmetry.**

This is a topological statement: the Chern numbers are integers. You cannot "partially" break chirality. The pair annihilation is all-or-nothing, which is why mass either breaks chirality completely (Dirac mass) or doesn't break it at all (massless limit).

### 5.4 The left-right mass matrix

In the Standard Model, the Dirac mass term takes the form:

$$\mathcal{L}_m = -m(\bar{\psi}_L\psi_R + \bar{\psi}_R\psi_L)$$

It couples left to right. In the Cantor picture:

- ψ_L lives near σ₁ (Chern +2 side)
- ψ_R lives near σ₅ (Chern −2 side)
- The mass term m couples them through the conduit bands σ₂, σ₃, σ₄
- The coupling strength is proportional to the tunneling amplitude through the Cantor gaps

The mass parameter m is therefore related to the conductance through the Cantor spectrum — which is quantized in units of e²/h by the TKNN theorem. This suggests that fermion masses are not arbitrary parameters but are determined by the Cantor gap conductances at different energy scales.

---

## 6. The Dirac Equation from Three Metallic Means

### 6.1 The 3D vacuum Hamiltonian (review)

$$H = \sum_{i=1}^{3} J[\psi(n_i+1) + \psi(n_i-1)] + 2J\cos(2\pi \alpha_i n_i)\psi(\mathbf{n})$$

with α₁ = 1/φ (gold), α₂ = √2−1 (silver), α₃ = (√13−3)/2 (bronze), all at V = 2J.

### 6.2 Emergent Dirac structure

At the critical point, the low-energy excitations of the AAH Hamiltonian can be described by an effective continuum theory. Near the band edges of the Cantor spectrum, the dispersion relation is:

$$E^2 = v_1^2 k_1^2 + v_2^2 k_2^2 + v_3^2 k_3^2 + \Delta^2$$

where v_i are the group velocities along each axis and Δ is the gap parameter.

This IS the relativistic dispersion relation E² = p²c² + m²c⁴ if:

- The three momenta p_i = ℏk_i correspond to the three metallic mean directions
- The mass gap Δ corresponds to the localization along the gold axis
- The "speed of light" c is the group velocity at the Cantor band edge

The Dirac equation emerges as the linearized, first-order form of this dispersion relation — exactly as it does in condensed matter physics for graphene, topological insulators, and Weyl semimetals.

### 6.3 Why the mass gap opens along gold

The gold axis has the **smallest group velocity** at the band edge. This is because the golden mean, being the most irrational number (Hurwitz), produces the most fragmented Cantor spectrum — the most gaps per unit energy. More gaps means slower propagation means stronger localization means larger effective mass.

Along the silver and bronze axes, the spectra are also Cantor sets, but with different gap distributions. The silver mean (less irrational than gold) and bronze mean (even less so) produce spectra with fewer gaps per unit energy, allowing faster propagation.

**Mass opens along gold because gold has the most fractured spectrum — the deepest Cantor hierarchy — making it the axis of strongest localization.**

---

## 7. Predictions

### P1. Mass ratio structure

If fermion masses arise from Cantor gap conductances at different energy scales, then the mass ratios between generations should reflect the fractal self-similarity of the Cantor spectrum. Specifically, the ratio between adjacent generation masses should approach φ-related values:

$$\frac{m_{\tau}}{m_{\mu}} = 16.82, \quad \frac{m_{\mu}}{m_e} = 206.77$$

These ratios should be expressible in terms of φ powers and the band partition fractions.

### P2. Neutrino masses from conduit tunneling

Neutrinos have tiny but nonzero masses. In the Cantor picture, neutrino mass arises from tunneling through the conduit bands (σ₂, σ₄) rather than direct localization along gold. The tunneling amplitude decays exponentially with the number of Cantor levels traversed, naturally producing small masses:

$$m_\nu \sim m_{e} \cdot e^{-n_{levels}/\phi}$$

### P3. Chirality violation proportional to mass

The amount of chirality violation in weak decays should be proportional to the mass of the fermion involved, scaled by the Cantor gap width ratio:

$$\frac{\text{gap width } \sigma_1/\sigma_2}{\text{gap width } \sigma_4/\sigma_5} = \frac{0.17}{0.30} = 0.57$$

This ratio should appear in precision electroweak measurements as a correction to the V−A coupling.

### P4. Fourth generation fermion is impossible

A fourth generation would require a fourth independent metallic mean direction. The discriminant Fibonacci chain breaks at n = 4 (Δ₄ = 20 ≠ F(8) = 21). Therefore, **no fourth generation of fermions can exist** — the spinor algebra cannot be extended to four independent mass/momentum directions because the discriminant chain does not close.

This is consistent with the experimental constraint from the Z boson width, which limits the number of light neutrino generations to exactly three.

---

## 8. Connection to Standard Model

| Standard Model Structure | Discriminant Chain Origin |
|---|---|
| 3 spatial dimensions | Δ₁ + Δ₂ = Δ₃ (5 + 8 = 13, chain closes at n = 3) |
| 1 mass direction (scalar) | Gold axis: self-referential, chain initiator |
| 3 momentum directions (vector) | Gold + Silver + Bronze: three coprime Fibonacci discriminants |
| Pauli matrices σ_z, σ_x, σ_y | Gold (diagonal), Silver (real mixing), Bronze (imaginary closure) |
| Chirality (γ⁵) | 5-band asymmetry: Chern widths 0.17 ≠ 0.30 |
| Chirality breaking by mass | Outer Chern pair annihilation (+2, −2) → 0 along gold |
| 3 fermion generations | 3 Fibonacci discriminants (conjecture: one generation per discriminant) |
| No 4th generation | Δ₄ = 20 ≠ 21 = F(8): chain breaks |
| Anticommutation {σ_i, σ_j} = 2δ_{ij} | Coprimality: gcd(5,8) = gcd(5,13) = gcd(8,13) = 1 |

---

## 9. Honest Assessment

**What is proven:**
- The discriminant Fibonacci chain 5 + 8 = 13 is exact arithmetic
- The uniqueness proof (n = 2 is the only Fibonacci link) is a solved quadratic
- The Pauli matrix properties (diagonal/off-diagonal, real/imaginary) are mathematical facts
- The Chern numbers +2, −1, +1, −2 are computed from the gap labeling theorem
- Chirality breaking by mass is standard QFT

**What is a strong conjecture:**
- The mapping gold → σ_z → mass is motivated by the self-referential property and the balanced band partition, but is not derived from first principles
- The interpretation of Chern pair annihilation as chirality breaking is a physical identification, not a theorem
- The "most irrational = strongest localization" argument is qualitative

**What is speculative:**
- Mass ratios from Cantor gap conductances (P1) — no computation done yet
- Neutrino masses from conduit tunneling (P2) — qualitative only
- Three fermion generations from three discriminants (P4) — numerology without mechanism
- The Pauli matrix ↔ metallic mean correspondence may be a structural analogy rather than a derivation

**What would strengthen this:**
- Computing the low-energy effective theory of the 3D AAH Hamiltonian at triple criticality and showing it has Dirac form
- Deriving the group velocity anisotropy v_gold < v_silver < v_bronze from the fractal gap structures
- Computing actual mass ratios from Cantor conductances and comparing to lepton mass hierarchy
- Showing that the AAH critical spectrum produces exactly the γ-matrix anticommutation relations

**What could falsify it:**
- Discovery of a fourth fermion generation
- Proof that the 3D AAH effective theory does NOT have Dirac structure at low energies
- Demonstration that the Pauli matrix mapping is merely coincidental with no predictive content

---

## 10. The Chain of Logic

```
φ² = φ + 1                            (axiom)
    ↓
Metallic means: x² = nx + 1           (generalization)
    ↓
Discriminants: Δ_n = n² + 4           (quadratic formula)
    ↓
5 + 8 = 13 (chain closes at n = 3)    (Fibonacci recurrence)
    ↓
Three independent directions           (three coprime discriminants)
    ↓
Gold = mass (self-referential seed)    (initiator of chain)
Silver = momentum 1 (real extension)   (extends to 2D)
Bronze = momentum 2 (imaginary closure)(closes algebra)
    ↓
σ_z = diagonal = gold                  (Pauli structure)
σ_x = off-diagonal real = silver
σ_y = off-diagonal imaginary = bronze
    ↓
Dirac Hamiltonian:                     (emergent)
H = α·p + βm
  = (silver, bronze)·momentum + gold·mass
    ↓
Chirality = 5-band asymmetry           (Chern widths 0.17 ≠ 0.30)
Mass breaks chirality                  (outer pair annihilation along gold)
    ↓
One mass. Three momenta. No fourth.    (discriminant chain = φ² = φ + 1)
```

---

## Citation

```bibtex
@misc{husmann2026diracfib,
    author = {Husmann, Thomas A.},
    title = {Dirac Mass According to Fibonacci},
    year = {2026},
    month = {March},
    howpublished = {GitHub Repository},
    url = {https://github.com/thusmann5327/Unified_Theory_Physics},
    note = {CC BY-NC-SA 4.0. Patent Pending.}
}
```

---

*Discovered March 15, 2026*
*Part of the Unified Theory of Physics: The Husmann Decomposition*
*The Fibonacci chain has one seed. The Dirac equation has one mass.*
