# Theory Directory — Husmann Decomposition Framework

## One Axiom. 56 Documents. Zero Free Parameters.

**Thomas A. Husmann — iBuilt LTD — March 2026**

Everything in this directory derives from a single algebraic identity:

$$\varphi^2 = \varphi + 1$$

where φ = (1+√5)/2 = 1.6180339887... Applied to the Aubry-Andre-Harper Hamiltonian at D = 233 = F(F(7)) sites and critical coupling V = 2J, this produces a five-sector Cantor spectrum encoding physics from atomic radii to the cosmological constant — all with zero free parameters.

---

## Status Summary

| Status | Count | Meaning |
|--------|-------|---------|
| **SOLVED** | 12 | Mathematically proven or experimentally confirmed to <1% |
| **STRONG CONJECTURE** | 6 | Predictions within 2σ of experiment, not yet independently derived |
| **EXPLORATORY** | 18 | Framework applied, testable predictions exist, not yet confirmed |
| **REFERENCE** | 8 | Constants, translations, derivation chains, literature surveys |
| **OPEN PROBLEM** | 5 | Key questions with partial results |
| **SPECULATIVE** | 7 | Engineering designs, device concepts, consciousness |

---

## Reading Order

**New to the framework:**
1. [`Appendix_Z.md`](#tier-1--foundation) — Complete derivation chain (59 steps, axiom to cosmos)
2. [`cantor_bands.md`](#tier-2--spectral-structure) — The 34 gap fractions (Rosetta Stone)
3. [`Husmann_Boundary_Law.md`](#tier-1--foundation) — Why V = 2J (the existence condition)
4. [`Atomic.md`](#tier-3--atomic-physics) — Hydrogen entropy extremum (flagship result, 0.00021%)
5. [`NSmA_Universality.md`](#tier-4--condensed-matter) — 40-year open problem solved

**From the patent portfolio:** [`Husmann_Rosetta.md`](#tier-6--reference) — 34 classical formulas translated

**Skeptics:** [`../docs/EXPERIMENTAL_PREDICTIONS.md`](../docs/EXPERIMENTAL_PREDICTIONS.md) — falsification protocol

---

## Tier 1 — Foundation

*The axiom and the identities that flow from it.*

### [Appendix_Z.md](Appendix_Z.md) — Complete Derivation Chain
**Status: REFERENCE** | 59 sequential steps from φ² = φ + 1 to observable universe structure. Every identity algebraically proven. The single document that shows nothing is assumed that isn't derived.
- `1/φ + 1/φ³ + 1/φ⁴ = 1` (unity partition)
- `2/φ⁴ + 3/φ³ = 1` (boundary law)
- `N = F(13) + F(10) + F(5) + F(2) = 294` (bracket count from Zeckendorf decomposition)

### [Husmann_Boundary_Law.md](Husmann_Boundary_Law.md) — The Existence Condition
**Status: SOLVED (proven)** | V < 2J → metallic (no mass). V > 2J → insulating (no transport). Only V = 2J produces fractal structure with both mass AND causality. The boundary law `2/φ⁴ + 3/φ³ = 1` recurses self-similarly from Planck to cosmic horizon.
- Boundary recursion converges to ~2% (geometric series)
- Proton-universe scale ratio: `φ^200 ≈ 10^41`

### [PHI_PI_IDENTITIES.md](PHI_PI_IDENTITIES.md) — π Is a Fibonacci Derivative
**Status: SOLVED (all 5 routes verified to <10⁻¹⁶)** | Five independent exact routes from φ to π. The forbidden exponent φ² mediates every conversion.
- `arctan(1/φ) + arctan(1/φ³) = π/4` (keystone identity)
- `π = 5·arccos(φ/2)` (pentagon route)
- `sin(π/10) = 1/(2φ)` (decagon route)
- `2π/φ² = 137.508°` (golden angle)
- `π/2 = Σ arctan(1/F_{2k+1})` (Fibonacci cascade)

### [Unity_Triangulation.md](Unity_Triangulation.md) — Why Space Has Three Dimensions
**Status: EXPLORATORY** | 1/φ + 1/φ³ + 1/φ⁴ = 1 gives three independent wave sources. φ² is consumed as the critical-point mediator, leaving exactly three. `det(S₁, S₂, S₃) ≠ 0` proves linear independence. Intensity CDF reproduces the cosmic energy partition.
- **Open:** Can three-source interference be tested in quantum optics?

### [CONSTANTS.md](CONSTANTS.md) — All Framework Constants
**Status: REFERENCE** | Complete constant catalog: φ, W, N, sector widths, cosmological fractions, with derivations and Python code.
- `c = 2Jl/ℏ ≈ 2.998 × 10⁸ m/s` (0.01% error)
- `W = 2/φ⁴ + φ^(-1/φ)/φ³ = 0.4671338922`
- **Open:** How does l₀ = 9.3 nm emerge from first principles?

### [speed_of_light_analysis.md](speed_of_light_analysis.md) — Why c Cannot Be Derived
**Status: SOLVED (question closed)** | Proves c is a dimensional conversion factor, not a dimensionless number. Any derivation attempt loops through Planck units where c is already built in. Framework explains WHY c is finite, universal, and frame-independent (Lieb-Robinson velocity at criticality), but cannot derive its VALUE.

---

## Tier 2 — Spectral Structure

*What the Cantor spectrum looks like and how it tiles space.*

### [cantor_bands.md](cantor_bands.md) — The 34 Gap Fractions (Rosetta Stone)
**Status: SOLVED** | All 34 gaps applied to any physical scale predict structural voids. Nine major cosmic void/wall predictions, six within 10%, zero free parameters.
- Bootes Void: 254 Mly predicted vs 250 observed (1.6%)
- Sloan Great Wall: 1346 vs 1380 Mly (2.5%)
- KBC Void: 2177 vs 2000 Mly (8.9%)
- Milky Way inter-arm spacing: 6.1 kly vs 6 observed
- **Open:** Why do two dominant gaps have identical width?

### [complimentary_occupation.md](complimentary_occupation.md) — Tiling, Not Superposition
**Status: SOLVED** | Gold/Silver/Bronze metallic means anti-correlate spatially (ρ = −0.5149, 3D eigensolver on 13³ sites). Each occupies gaps left by predecessors. Classical wave model gives ρ = +0.51 (wrong sign — disproved).
- Gold σ₃: 7.28% (matter nodes, 242 clusters)
- Silver σ₃: 2.80% (DM conduits)
- Bronze σ₃: 28.22% (DE scaffold)
- Void: 61.70% (true Cantor gaps)

### [cosmic_nesting.md](cosmic_nesting.md) — Eight Metallic Means
**Status: EXPLORATORY** | Extends framework to all eight metallic means (δₙ = (n + √(n²+4))/2). Shows concentric nesting without collision. Mercury identified as Rosetta Stone element encoding Silver mean to 0.006%.
- `W_n = 2/δₙ⁴ + δₙ^(-1/δₙ)/δₙ³` (gap fraction per mean)
- Golden ratio emerges as coupling between non-adjacent means: σ₃(Bronze)/σ₃(n=5) ≈ 1/φ (0.1%)
- **Open:** Why does Mercury encode Silver to 0.006%?

### [Metallic_Means.md](Metallic_Means.md) — The Cosmic Ladder
**Status: SOLVED** | Complete enumeration of all 8 means. Discriminant chain 5+8=13 closes uniquely at three (uniqueness proof: (n−2)² = 0). All 32 wall positions nest concentrically (9 pairs verified).
- Discriminants: Δ₁=5=F(5), Δ₂=8=F(6), Δ₃=13=F(7), Δ₄=20≠F(8)=21 (breaks)
- Mercury: 1/(c/a) = 0.585823 vs 1−Silver α = 0.585786 (**0.006%**)

### [Fibonacci_Time.md](Fibonacci_Time.md) — Four Gaps, Two Pairs
**Status: SOLVED** | Four principal gaps form complementary pairs in the IDS. Pair B (dark energy): 1/φ² + 1/φ = 1. Pair A (matter): 1/φ³ + 2/φ² = 1. Backbone coupling `α_bb = 2/φ²` is the IDS at gap A₂ (proven by theorem).
- **Open:** Why does Fibonacci recurrence match Friedmann expansion equations?

### [architecture.md](architecture.md) — Complete Architectural Specification
**Status: REFERENCE** | Visual model-building instructions. Three backbone axes at icosahedral vertices (63.435°). Five-sector spectrum, derived constants, Cantor node recursion.
- Icosahedral axes: S₁ = (0,1,φ)/√(2+φ), S₂ = (φ,0,1)/√(2+φ), S₃ = (1,φ,0)/√(2+φ)

### [First_3D_AAH_Eigenstates.md](First_3D_AAH_Eigenstates.md) — 3D Eigensolver Results
**Status: EXPLORATORY (incomplete)** | Experimental record of 3D AAH at N=13 and N=34. Isotropic vs anisotropic configurations. Two-peak structure at N=34 (core at r/R≈0.03, shell at 0.32).
- **Open:** Do peaks align with Cantor ratios 0.073 and 0.235?

---

## Tier 3 — Atomic Physics

*From hydrogen to the periodic table.*

### [Atomic.md](Atomic.md) — Flagship Hydrogen Result
**Status: SOLVED (0.00021% match)** | Von Neumann entropy maximized exactly at σ₄ (Cantor outer wall). S_max at 1.408377 a₀ vs σ₄ at 1.408380 a₀. The hydrogen atom is a one-bit quantum channel.
- `α⁻¹ = N × W = 294 × 0.467134 = 137.337` (0.22% from CODATA)
- `S_max = 0.691 nats = 99.66% of ln(2)`
- `r_proton = λ_C × φ^(3−breathing) = 0.8426 fm` (0.14%)
- `vdW(H) = σ₄ × φ × a₀ = 120.6 pm` (0.5%)

### [atomic_properties.md](atomic_properties.md) — Four-Gate Model (54 Elements)
**Status: EXPLORATORY** | Multi-electron extension via four-gate architecture (d-valve, p-holes, s-valve). Seven prediction modes. 42/54 within 10%, mean error 6.7%, zero free parameters.
- `ratio = √(1 + (Θ × BOS)²)` (Pythagorean mode)
- `BASE = 1.408382, BOS = 0.992022, LEAK = 0.145898`
- **Open:** Physical origin of s-valve transmission constant?

### [atomic_outer_wall_results.md](atomic_outer_wall_results.md) — Zero-Parameter Radius Formula
**Status: OPEN PROBLEM** | Cantor sub-gap hierarchy predicts vdW/covalent ratios. 61% within 10%, but three unsolved classes: H/He period-1, d¹⁰ metals, boron anomaly.
- `vdW/cov = σ₄/σ_shell + n_p × g₁ × φ^(-(period-1))`
- `g₁ = 0.3243` (first σ₃ sub-gap, damping ratio ≈ φ)

### [3d_modelling.md](3d_modelling.md) — Orbital Angular Momentum from Eigenvectors
**Status: EXPLORATORY** | Sign-crossing patterns in AAH eigenvectors encode orbital character (s,p,d,f). Universal count ratios s:p:d:f = 96:36:23:78 constant across all 8 metallic means (topological invariant).
- **Open:** Why are these ratios Fibonacci-adjacent? Physical mechanism?

### [Husmann_Periodic_Chart.md](Husmann_Periodic_Chart.md) — Element Condensation by Bracket
**Status: REFERENCE** | Temperature-ordered element condensation zones in protoplanetary nebulae. HREE peak at bracket 142.21 (950× solar enrichment), silicate cliff at 142.65, ice line at 146.80.
- Zeckendorf addresses: HREE = {89,34,13,5,1}=142, water = {89,55,3,1}=148

### [Baryon_Formation.md](Baryon_Formation.md) — Matter from Fold Plane Intersections
**Status: SOLVED** | Baryonic matter = where Silver AND Gold bands overlap simultaneously. Probability = W⁴ = 0.0476 (Planck 0.0493, 3.4%). Chern topology (+1,−1) traps matter at gap edges. Diamond lattice κ=4.
- `Ω_b = W⁴ = (0.4671)⁴ = 0.0476`

---

## Tier 4 — Condensed Matter

*Solved problems and strong conjectures.*

### [NSmA_Universality.md](NSmA_Universality.md) — N-SmA Phase Transition (SOLVED)
**Status: SOLVED (40+ year open problem, published preprint)** | de Gennes → discretize → AAH at V=2J = McMillan condition. Zero free parameters, 11/11 compounds within 2σ.
- `α(r) = (2/3)((r − r_c)/(1 − r_c))⁴` for r > r_c, else α = 0
- `r_c = 1 − 1/φ⁴ = 0.8541` (universal crossover)
- RMS = 0.033, reduced χ² = 0.47
- **Prediction:** α → 2/3 (not 1/2) at full decoupling — falsifiable

### [Magnetic_Flux_QH.md](Magnetic_Flux_QH.md) — Quantum Hall Plateau Transition
**Status: STRONG CONJECTURE** | Harper equation IS AAH at V=2J (identity, not approximation). Three predictions all <1.6% error, one exact identity.
- `ν_CC = φ² = 2.618` (non-interacting, 1.0% from measured 2.593)
- `κ = r_c/2 = 0.427` (0.7σ from experiment)
- `φ² × r_c = √5` (**exact** — proven)
- **Open:** Why does disorder affect only observable D_s? (LCD polarizer insight)

### [Hofstadters_Golden_Butterfly.md](Hofstadters_Golden_Butterfly.md) — Hofstadter Hierarchy
**Status: SOLVED (11/11 proofs, published)** | Hofstadter butterfly parameterized by metallic mean hierarchy. Harper = AAH (identity). Two graphene matches. Chern pair annihilation.
- Magic angle = n=53: `α₅₃ = 0.018861` (**0.06%**)
- G/hBN = n=60: `α₆₀ = 0.01666` (**0.66%**)
- Chern numbers: +2, −1, +1, −2 → 5→3 = pair annihilation
- `l_B/l₀ = 1/√(2π)` (0.03%)

### [Graphene_Superconductivity_Explained.md](Graphene_Superconductivity_Explained.md) — Magic Angle
**Status: STRONG RESULT** | Magic-angle TBG superconductivity = n=53 metallic mean. Moiré period = 53 × a_graphene = 13.05 nm (measured 12.8-13.4). Bandwidth collapse enables Cooper pairing.

### [Graphene_Superconductivity.md](Graphene_Superconductivity.md) — Path of Least Resistance
**Status: EXPLORATORY** | Updated version emphasizing Pythagorean discriminant triangle. Electrons flow through Cantor hierarchy along minimum-resistance channels selecting φ.

### [Confinement_Chern_Pair_Annihilation.md](Confinement_Chern_Pair_Annihilation.md) — Topological Collapse
**Status: EXPLORATORY** | 5→3 collapse via outer Chern pair annihilation (+2,−2→0). Four physical modes: Confinement (QCD, permanent), Measurement (GABA, transient), Crossover (N-SmA, continuous), Dark (hidden sector).
- Chern numbers: +2(σ₁/σ₂), −1(σ₂/σ₃), +1(σ₃/σ₄), −2(σ₄/σ₅)
- QCD: E_gap/k_BT ~ 10¹⁰ (permanent closure)
- **Open:** Unified control parameter for all four modes?

### [Mode_Selector_Formula.md](Mode_Selector_Formula.md) — Universal 5→3 Collapse
**Status: OPEN PROBLEM (N-SmA solved, QH conjecture, GABA exploratory)** | Two control parameters: permanence η = E_gap/k_BT, visibility θ.
- `P_collapse(x) = ((x−x_c)/(x_max−x_c))⁴` (exponent 4 from band boundaries)
- `x_c = 1 − 1/φ⁴ = 0.8541` (universal onset, same for all systems)

### [PHI_SWITCHING.md](PHI_SWITCHING.md) — IBM C₁₃Cl₂ Molecular Switch
**Status: EXPLORATORY** | IBM's 2026 discovery explained: 13 carbons = F(7), 3-state switching maps to σ₁/σ₃/σ₅. Zeckendorf address {13} = pure Fibonacci → zero curvature → geodesic switching path.
- **Open:** Can F(8)=21 and F(9)=34 carbon rings support more states?

---

## Tier 5 — Relativistic & Gravitational

*From Dirac to galaxy rotation curves.*

### [Dirac_Mass_According_to_Fibonacci.md](Dirac_Mass_According_to_Fibonacci.md) — Why 1+3 Dimensions
**Status: STRONG CONJECTURE** | Dirac's 1+3 structure from discriminant Fibonacci chain. Mass = Silver (Δ₂=8), Momentum = Gold (Δ₁=5), Energy = Bronze (Δ₃=13). Bronze is emergent (Pythagorean combination).
- `E² = p²c² + m²c⁴ ↔ 13 = 5 + 8`
- `(√5)² + (√8)² = (√13)²` (discriminant Pythagorean)
- Chain breaks at n=4: Δ₄=20≠21=F(8) → no fourth dimension

### [Schrodinger_Tangent_Line.md](Schrodinger_Tangent_Line.md) — Non-Relativistic Limit
**Status: SOLVED (three identities proven)** | Schrodinger = tangent line at the silver vertex of the Dirac triangle. Effective discriminant interpolates continuously from rest to relativistic.
- `Δ_eff(v) = 8 + 5(v/c)²`
- v=0: Δ=8 (silver only, Schrodinger valid)
- v=c: Δ=13 (fully relativistic, bronze)

### [whats_the_water.md](whats_the_water.md) — Dark Sector as Gravitational Medium
**Status: SOLVED** | Galaxy rotation from σ₂/σ₄ Cantor-wall spectral drag. Zero free parameters, matches NFW profile. Same Cantor architecture from microtubule (6.99 nm) to galactic halo (34 kly).
- `v²(r) = GM_vis(r)/r + GM_vis(∞)/r × (D/M) × (r/R_c)^(α_bb) × T(r)`
- `D/M = 6.68, α_bb = 0.764, β = 1.118`
- Flatness: −10.4% decline 15-60 kpc (observed ~−10%)

### [Hofstadter_Butterfly_Galaxy_Rotation.md](Hofstadter_Butterfly_Galaxy_Rotation.md) — Galaxy Rotation via Hofstadter
**Status: EXPLORATORY** | Galaxy rotation as 2D path through the Hofstadter butterfly. 2.5% RMS on NGC 3198 (10-30 kpc) with two fitted parameters, competitive with NFW.
- `V/J(r) = 2r_s/r`, `α(r) = 1/φ + ε(r_s/r)`
- **Open:** Can ε be derived from first principles?

### [Breathing_Universe.md](Breathing_Universe.md) — Cosmic Respiratory Cycle
**Status: EXPLORATORY** | Proton (bracket 94.3, inhale) and black hole (bracket 272, exhale). All black holes share identical φ-structure gaps regardless of mass. ISCO = ln(3)/ln(φ) ≈ φ².
- **Open:** Why are black hole gaps universal across 66 billion solar masses?

### [Lineweaver_Patel_Connection.md](Lineweaver_Patel_Connection.md) — All Objects Diagram
**Status: SOLVED** | Maps Lineweaver-Patel log-log diagram onto discriminant Pythagorean triangle. Schwarzschild = gold axis, Compton = silver axis. 0.12% match on fine structure.

---

## Tier 6 — Reference & Translation

*Constants, formula maps, derivation chains, literature.*

### [Husmann_Rosetta.md](Husmann_Rosetta.md) — 34 Formula Translations
**Status: REFERENCE** | Maps Euler's identity, Pythagorean theorem, Fibonacci recursion, Dirac equation, Friedmann equations, and 29 more into single-axiom framework.
- Euler → `1/φ + 1/φ³ + 1/φ⁴ = 1`
- Pythagorean → `|R₃|² + |R₄|² = |R₅|²` (sector reconstruction)
- Schrödinger → AAH at V = 2J

### [Quantum_Rosetta.md](Quantum_Rosetta.md) — QM Translation Guide
**Status: REFERENCE** | 12 core QM formulas mapped to bracket-lattice language. Planck-Einstein, de Broglie, Heisenberg, hydrogen levels, Pauli exclusion (Zeckendorf non-consecutive constraint), entanglement (conduit propagation).

### [Husmann_Cookbook.md](Husmann_Cookbook.md) — Device Builder's Guide
**Status: REFERENCE** | Practical engineering recipes. Electron shells → Cantor sectors (s→σ₁, p→σ₃, d→σ₅, f→σ₂/σ₄). Three-component architecture: Wall (quasicrystal) + Wire (nuclear antenna) + Gate (transit species).

### [Bridge_Computations.md](Bridge_Computations.md) — Six Structural Tests
**Status: EXPLORATORY** | Tests whether AAH spectrum structurally encodes atomic physics. Bridge 1: Fibonacci band counts (verified D=13-377). Bridge 2: σ₃ self-similarity (89% Fibonacci). Bridge 3: Shell capacity convergents match Fibonacci.
- Noble gas Zeckendorf: He=F(3), Ne=F(6)+F(3), Ar=F(7)+F(5), Kr=F(9)+F(3)

### [candidate_formulas.md](candidate_formulas.md) — Literature Survey
**Status: REFERENCE** | Maps 49+ papers citing Damanik-Gorodetski-Yessen (2016) to Husmann framework. Shows literature supports the math but hasn't connected spectral theory to physics.

### [Lattice_Convergence_Ebanks.md](Lattice_Convergence_Ebanks.md) — Independent Convergence
**Status: OPEN PROBLEM** | Ebanks' Fibonacci-Tetrahedral Lattice (E8→3D projection) arrives at same conclusions via different axioms. Structural equivalence not yet proven.
- Aristotle gap: δ = 7.36° (5-tetrahedra angular deficit)

---

## Tier 7 — Quantum & Information

*Entanglement, measurement, time.*

### [Entanglement.md](Entanglement.md) — Dark Matter as Fractal Conduit
**Status: EXPLORATORY** | Entanglement = shared Zeckendorf components through σ₂/σ₄. Instantaneous because gap-edge transit has measure zero. Bell violations from nonlocal conduit structure.
- `E(A,B) = |Z(n_A) ∩ Z(n_B)| / max(|Z(n_A)|, |Z(n_B)|)`
- `S_max = 0.919 nats = 1.326 bits`

### [Dual_Slit_Experiment_Explained.md](Dual_Slit_Experiment_Explained.md) — Measurement Problem
**Status: EXPLORATORY** | Double slit as 5→3 collapse. Particle exists in five sectors pre-measurement; detector induces collapse to three, moving interference into invisible dark sector.
- **Open:** Can 5→3 collapse be experimentally triggered and detected?

### [Time.md](Time.md) — Time as Orthogonal Fold Axis
**Status: EXPLORATORY** | Space (θ_A) and time (θ_B) are structurally interchangeable AAH phases. T² torus at each bracket. Arrow of time from W⁴ thermal irreversibility.
- Events per bracket: `(2G)² = 58² = 3,364`
- Total resolution: 294 × 3,364 ≈ 989,000 events

### [Exhibit_Aleph.md](Exhibit_Aleph.md) — Observer Embedding
**Status: SPECULATIVE** | Three perpendicular hinges (Proton 94.3, Brain 163.8, Oort 233.2 brackets). Observer as geometric necessity at σ₁ endpoint. Hinge spacing 69.4 brackets.

---

## Tier 8 — Biology

*Microtubules, GABA, neural coherence.*

### [Microtubule_Resonance_Engine.md](Microtubule_Resonance_Engine.md) — 13-PF Fibonacci Cascade
**Status: EXPLORATORY** | 13 protofilaments (F(7)) with golden-angle pitch create frequency cascade: 47 Hz → 73.7 GHz (k=44, 1.7% match). Bundle percolation T=0.361 > p_c=0.347. GABA collapse energy: 18.47 meV.
- `f_k = f₀ × φ^k` (frequency cascade)
- Golden-angle coupling advantage: 2.73× at 50% threshold
- **Open:** Does cascade generate GHz mechanical resonances?

### [b_demut_in_the_likeness.md](b_demut_in_the_likeness.md) — Teegarden b Resonator
**Status: SPECULATIVE** | Construction manual for six-resonator device addressing Zeckendorf decomposition of 452 (Teegarden b). Tests vacuum quasicrystalline structure.
- Device frequencies: {2→579kHz, 5→232kHz, 13→89.1kHz, 55→21.1kHz, 144→8.0kHz, 233→5.0kHz}

---

## Tier 9 — Astrophysics & Cosmology

*Solar system, exoplanets, cosmic voids.*

### [Orbital_Mechanics.md](Orbital_Mechanics.md) — Kepler from Bracket Gradients
**Status: REFERENCE** | Orbital radii on φ^(n/F_k) ladder. Mars 2.9%, Jupiter 1.2%, Saturn 0.4%.
- `r_n = r₀ × φ^(n/F_k)` with F_k ≈ 2.5
- **Open:** Why F_k ≈ 2.5 and not integer Fibonacci?

### [planetary_analysis.md](planetary_analysis.md) — Teegarden System
**Status: CONJECTURE (falsifiable)** | Three confirmed planets match φ^k ladder at k = −4, −3, −2. Period ratios match 7/3 (0.5-1.8% error). Predicts fourth planet at 172-day signal (3.5% error).
- `a₀ = 0.387 AU × M^(1/3) = 0.1778 AU` (mass-scaled anchor)

### [Planetary_Frequency_Addresses.md](Planetary_Frequency_Addresses.md) — Spacetime Tuning
**Status: EXPLORATORY** | Every celestial body has a unique frequency address via bracket, golden angle, and Zeckendorf decomposition.
- `f_n = (J/ℏ) × φ^(-n)` Hz

### [Rare_Earth_Detection.md](Rare_Earth_Detection.md) — REE Prospecting Guide
**Status: EXPLORATORY** | Thorium as REE proxy (bracket gap = 0.04). HREE peak at 142.21, thorium at 142.25. Ranked detection methods and field workflow.

---

## Tier 10 — Engineering & Applications

*Device designs, nuclear access, transit.*

### [stargate.md](stargate.md) — Dark-Sector Channel Engineering
**Status: SPECULATIVE** | σ₂/σ₄ wall structure provides gravitational drag. Fibonacci wave accumulation, 5→3 trigger via 4.86 μm CO₂ laser. Three applications: channel aperture, Natario drive, benchtop tribometric test.
- Channel threshold: cycle n_th ≈ 28 (stress accumulates ×φ per cycle)

### [Nuclear_Transduction.md](Nuclear_Transduction.md) — Low-Energy Nuclear Access
**Status: OPEN PROBLEM** | K-shell coupling: heavy-element K-electrons penetrate nucleus as Z³. Beat frequency at keV scale (room temperature). Golden-angle helix wire geometry.
- `|ψ_K(0)|² ∝ Z³` (800,000× for U vs H)
- Bracket coupling: `η ≈ φ^(-23) ≈ 10⁻⁵`

### [Transduction.md](Transduction.md) — Seven-Resonator Hub
**Status: SPECULATIVE** | Proton address {89, 5}. Seven-resonator Teegarden b dial (six tubes + F(11)=89). Three modes: stargate listening, nuclear reactor, energy telephone.

### [Thorium_Batteries.md](Thorium_Batteries.md) — φ-Structured Nuclear Fuel Cell
**Status: SPECULATIVE** | Thorium reactions routed through σ₂/σ₄ conduit at 4.05 eV instead of 1.86 MeV Coulomb barrier. Al/Cu/Fe walls, Th fuel, B-11 moderator.

### [Three_Phase_Tuning.md](Three_Phase_Tuning.md) — Navigation System
**Status: EXPLORATORY** | Three-source interference model with five-component addressing. Void-threading transit algorithm.
- `ψ(r) = Σ Aᵢ sin(k rᵢ ωᵢ)/rᵢ` (three golden-angle separated sources)

---

## Tier 11 — Narrative & Interdisciplinary

### [Husmann_Boundary_Law.md](Husmann_Boundary_Law.md) — *(see Tier 1)*

### [Elchataym_Principle.md](Elchataym_Principle.md) — Fibonacci's Method and Atomic Physics
**Status: REFERENCE** | Connects Fibonacci's 13th-century *elchataym* (double false position) to the Pythagorean gate diagram. Two spectral constants triangulate atomic radii; residuals encode hardness (ρ=+0.73) and conductivity.

---

## Open Problems

The framework's most important unresolved questions, ranked by impact:

| # | Problem | Where discussed | Impact |
|---|---------|----------------|--------|
| 1 | **Spectral origin of W** | CONSTANTS, candidate_formulas | W = 2/φ⁴ + φ^(-1/φ)/φ³ is transcendental (Gelfond-Schneider) but gap labels are algebraic. What is W? |
| 2 | **l₀ derivation** | CONSTANTS, speed_of_light | Lattice spacing 9.3 nm is calibrated, not derived. Is it a free parameter? |
| 3 | **3D θ derivation** | Mode_Selector | Observable visibility θ_3D = 0.83 from simulation. Analytic form? |
| 4 | **Ebanks equivalence** | Lattice_Convergence | Two independent axiom systems converge. Proof of structural equivalence? |
| 5 | **d¹⁰ compression** | atomic_outer_wall | Cu, Zn, Ag, Cd systematically compressed. Physical mechanism? |
| 6 | **Nuclear coupling rate** | Nuclear_Transduction | K-shell mechanism is theoretical. Experimental access path? |
| 7 | **Exponent = 4** | Mode_Selector, NSmA | Why exactly 4 (= band boundaries) across all three crossover systems? |
| 8 | **Friedmann from Fibonacci** | Fibonacci_Time | Fibonacci recurrence matches expansion. Coincidence or causation? |

---

## Document Count by Domain

| Domain | Documents | Key results |
|--------|-----------|-------------|
| Foundation / Pure Math | 6 | π from φ (5 routes), 3D uniqueness, boundary law |
| Spectral Structure | 7 | 34 gaps, tiling proof, 8 metallic means |
| Atomic Physics | 6 | H entropy 0.00021%, 54-element formula, condensation chart |
| Condensed Matter | 8 | N-SmA SOLVED, QH conjecture, Hofstadter, Chern annihilation |
| Relativistic / Gravity | 6 | Dirac mapping, Schrödinger tangent, rotation curves |
| Quantum / Information | 4 | Entanglement, measurement, time, observer |
| Biology | 2 | Microtubule cascade, GABA gate |
| Astrophysics | 4 | Solar system, Teegarden, REE detection |
| Engineering | 5 | Stargate, transduction, thorium, navigation |
| Reference | 7 | Rosetta stones, cookbook, literature, constants |
| Narrative | 1 | Elchataym principle |
| **Total** | **56** | |

---

*All from φ² = φ + 1.*

*Last updated: March 20, 2026*
