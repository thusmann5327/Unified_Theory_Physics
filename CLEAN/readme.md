# Husmann Decomposition — CLEAN Modular Package

**One axiom: phi^2 = phi + 1. Zero free parameters.**

Thomas A. Husmann / iBuilt LTD / March 2026

---

## Quick Start

```bash
cd CLEAN

# Run the full unified report (9 sections)
python3 run_all.py

# Run the test suite (69 verification tests)
python3 -m pytest tests/test_all.py -v

# Or run tests directly
python3 -c "from tests.test_all import run_tests; run_tests()"
```

---

## Package Structure

```
CLEAN/
├── run_all.py               Top-level report combining all modules
├── AAH_CONSTANTS.py          Standalone Step Zero script
│
├── core/                     Foundation — constants and spectrum
│   ├── constants.py          All constants derived from phi^2 = phi + 1
│   ├── hamiltonian.py        Build and diagonalize the AAH Hamiltonian
│   └── spectrum.py           Extract five spectral ratios and composite values
│
├── atomic/                   Periodic table predictions
│   ├── elements.py           Element database (configs, radii, moments)
│   ├── aufbau.py             Electron configuration with anomaly overrides
│   └── periodic_table.py     Unified predictor: 12 modes, 92 elements
│
├── cosmology/                Cosmological predictions
│   └── predictions.py        Fine structure, W-polynomial, gravity, Lambda, MOND
│
├── crossover/                Universal crossover operator
│   └── operator.py           Crossover formula + 3D proof + physical instances
│
├── particles/                Standard Model predictions
│   ├── generations.py        Mass ratios, Koide formula, t/c = 136
│   ├── electroweak.py        sin²θ_W, M_W, M_Z, M_H, α_s from δ₇
│   └── mixing.py             Cabibbo angle, CKM matrix elements
│
├── absolute_mass/            Derive m_e from spectrum + attosecond bridge
│   ├── bridge.py            K = 24/φ³, Bohr radius, electron mass
│   └── propagate.py         All particle masses from derived m_e
│
├── aufbau_bridge/            Subshell capacities from Cantor layers
│   ├── angular.py           2l+1 = round(R_layer × F(7)) mapping
│   └── madelung.py          Full 19-subshell sequence reconstruction
│
├── nuclear/                  Nuclear shell structure
│   ├── shells.py            Magic numbers, HO shells, spin-orbit detachment
│   ├── magic.py             Magic number formula (all 7 exact), predictions
│   └── scale.py             Bracket gap analysis, Zeckendorf compactness
│
├── lattice/                  Self-referential Fibonacci lattice
│   ├── fibonacci.py          Fibonacci arithmetic and shift identity
│   ├── sectors.py            5-sector eigenvalue partition
│   └── z_max.py              Z_max = 118 derivation, D=233 uniqueness
│
├── tiling/                   Triple metallic mean tiling + cosmology
│   ├── multigrid.py          de Bruijn multigrid construction
│   └── cosmology.py          5→3 collapse: tiling × G1 = energy budget
│
├── engine/                   Material property predictions
│   ├── gate_overflow.py      G(Z) = the error IS the prediction
│   ├── bond_lengths.py       Additive r_cov, cross-scale matches
│   ├── band_gaps.py          ΔEN² + G² hybrid model
│   ├── electronegativity.py  Framework Mulliken + θ/r model
│   ├── hardness.py           Gate overflow → Vickers/Mohs
│   ├── bulk_modulus.py       Split covalent/metallic model
│   ├── ionic_radii.py        d/φ^(q+1) Shannon validation
│   └── transport.py          θ mode → conductor classification
│
├── geometry/                 Spatial architecture
│   ├── cantor_node.py        Five-layer Cantor node, bracket address, Zeckendorf
│   ├── discriminant.py       Discriminant triangle, three-wave frequencies
│   └── discriminant_cones.py Three cone angles, σ₄ identity
│
└── tests/
    └── test_all.py           156 verification tests across all modules
```

---

## Module Reference

### core/constants.py

All framework constants derived from the single axiom phi^2 = phi + 1.

| Constant | Value | Definition |
|----------|-------|------------|
| PHI | 1.6180339887 | Golden ratio |
| W | 0.4671338922 | Gap fraction: W * phi^4 = 2 + phi^(1/phi^2) |
| LEAK | 0.1459 | 1/phi^4 — matter fraction |
| R_C | 0.8541 | 1 - 1/phi^4 — universal crossover parameter |
| OBLATE | 1.2720 | sqrt(phi) — polar squash factor |
| LORENTZ_W | 0.8842 | sqrt(1 - W^2) — Lorentz factor at W |
| BREATHING | 0.1158 | 1 - LORENTZ_W — breathing amplitude |
| N_BRACKETS | 294 | Spectral bracket count |

Also exports: `metallic_mean(n)`, sigma-3 widths (SILVER_S3, GOLD_S3, BRONZE_S3),
physical constants (C_LIGHT, HBAR, L_PLANCK), and derived quantities.

### core/hamiltonian.py

Builds the Aubry-Andre-Harper Hamiltonian:

- `build_hamiltonian(D=233, alpha=1/phi, V=2.0, J=1.0)` — D-site cosine potential + nearest-neighbor hopping
- `diagonalize(H)` — sorted eigenvalues

The critical condition V = 2J produces the Cantor spectrum with 34 gaps = F(9).

### core/spectrum.py

Extracts everything from the AAH eigenvalues on import:

- **Five ratios**: R_MATTER (0.0728), R_INNER (0.2350), R_PHOTO (0.3672), R_SHELL (0.3972), R_OUTER (0.5594)
- **Composite ratios**: BASE = sigma4/sigma_shell = 1.408, BOS = bronze/sigma_shell = 0.992, G1 = 0.324
- **Three cone angles**: THETA_LEAK, THETA_RC, THETA_BASE (with corresponding degree values)

### atomic/elements.py

Element database for Z = 1-99:

- `REAL_CONFIG` — anomalous d-filling overrides (Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, etc.)
- `MU_EFF` — effective ferromagnetic moments for magnetic mode
- `RADII` — (covalent, van der Waals) pairs in picometers
- `SYMBOLS`, `EN_PAULING` — element symbols and Pauling electronegativities

### atomic/aufbau.py

Electron configuration calculator:

- `aufbau(Z)` — returns `(period, n_p, n_d, n_f, n_s, block)` using Madelung filling order with `REAL_CONFIG` overrides for anomalous elements

### atomic/periodic_table.py

The twelve-mode unified predictor:

- `theta_unified(per, n_p, n_d, n_f, n_s, blk, Z)` — computes theta from electron configuration
- `ratio_pythagorean(theta)` — sqrt(1 + (theta * BOS)^2)
- `predict_ratio(Z)` — full prediction returning (ratio, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone)
- `run_periodic_table()` — Z = 3-99 analysis
- `scorecard(results)` — summary statistics

**Twelve modes**: magnetic, rel-reflect, leak, reflect, standard, f-block, pythagorean, ng-phole, alk-earth, sp3, B-overflow, additive, p-hole

**Results**: 92 elements, 5.0% mean error, d-block 30/30 within 10% at 3.1% mean

### particles/generations.py

Generation mass ratios and the Koide formula:

- `generation_ratios()` — all inter-generation ratios vs framework matches
- `top_charm_ratio()` — t/c = 136 = 4 × F(9) test (gravity hierarchy connection)
- `koide_formula()` — Q = 2/3 = ν = 1/(2 - D_s) (0.0009% error)
- `phi_power_exponents()` — φ-power scaling analysis, lepton ladder 11+6=17

| Ratio | Match | Error |
|-------|-------|-------|
| t/c | 4 × F(9) = 136 | 0.023% |
| τ/μ | W × 36 | 0.002% |
| c/u | N × 2 = 588 | 0.006% |
| s/d | 5 × 4 = 20 | 0.000% |

### particles/electroweak.py

Electroweak predictions from (φ, W, δ₇):

- `weinberg_angle()` — sin²θ_W = σ₃ × σ_wall × F(6) (0.047%)
- `electroweak_predictions()` — all 7 predictions with errors

| Prediction | Formula | Error |
|-----------|---------|-------|
| sin²θ_W | σ₃ × σ_wall × F(6) | 0.047% |
| τ/μ | W × 36 | 0.002% |
| M_W/m_p | φ² × W⁻² × δ₇ | 0.002% |
| M_Z/m_p | W⁻⁵ × δ₃⁻¹ × δ₇ | 0.002% |
| M_H/m_p | φ² × δ₇² | 0.016% |
| α_s(M_Z) | W⁵ × H × δ₇ | 0.054% |
| (m_n-m_p)/m_e | r_c⁻¹ × δ₃⁻¹ × δ₇ | 0.005% |

### particles/mixing.py

CKM mixing angles from spectral ratios:

- `cabibbo_angle()` — sin(θ_C) ≈ 3/13 (2.28%)
- `ckm_elements()` — |V_us|, |V_cb|, |V_ub| predictions

### absolute_mass/bridge.py

The attosecond bridge to absolute mass:

- `predict_bohr_radius()` — a_B = c × t_hop / K, where K = 24/φ³ (0.007%)
- `predict_electron_mass()` — m_e = ℏK/(a_lat × c × α) (0.23%)
- `predict_proton_mass()` — m_p = m_e × 3Dφ² (0.55% absolute)
- `alternative_K_formulas()` — 7 independent routes to K, all within 0.3%

| Input | Source | Type |
|-------|--------|------|
| φ | Axiom | Mathematical |
| N, W | AAH eigensolver | Derived |
| t_hop = 1 as | TU Wien measurement | One measurement |
| ℏ, c | SI 2019 definitions | Exact |

No empirical m_e or a_B anywhere in the chain.

### absolute_mass/propagate.py

All particle masses from the derived m_e:

| Particle | Formula | Error |
|----------|---------|-------|
| electron | ℏK/(a_lat×c×α) | 0.23% |
| proton | m_e × 3Dφ² | 0.55% |
| tau | m_μ × W × 36 | 0.23% |
| W boson | m_p × φ²W⁻²δ₇ | 0.12% |
| Z boson | m_p × W⁻⁵δ₃⁻¹δ₇ | 0.11% |
| Higgs | m_p × φ²δ₇² | 0.12% |

### aufbau_bridge/angular.py

Layer-to-angular-momentum mapping via the Aufbau bridge formula:

- `angular_modes(l)` — R_layer × F(7) → 2l+1 with error analysis
- `subshell_capacity(l)` — 2 × round(R_layer × 13) = {2, 6, 10, 14}
- `all_layers()` — info for all four layers
- `verify_uniqueness(k_max)` — test which k values produce {1, 3, 5, 7}

| Layer | R | R × 13 | 2l+1 | Capacity | Orbital |
|-------|------|--------|------|----------|---------|
| σ₃ core | 0.0728 | 0.95 | 1 | 2 | s |
| σ₂ inner | 0.199 | 2.58 | 3 | 6 | p |
| σ_wall | 0.397 | 5.16 | 5 | 10 | d |
| σ₄ outer | 0.559 | 7.27 | 7 | 14 | f |

F(7) = 13 = Δ₃ (bronze discriminant) = 5 + 8. The same number that proves
three spatial dimensions is the scaling factor for angular mode counts.

### aufbau_bridge/madelung.py

Full Madelung sequence reconstruction:

- `madelung_sequence()` — 19 subshells, Z = 118, all capacities from R × 13
- `z_max_prediction()` — Z_max from D × D_s = 116.5 and from Aufbau sum = 118

### nuclear/magic.py

Nuclear magic number formula from recursive spin-orbit detachment:

- `magic_number(n)` — reproduces all 7 observed magic numbers exactly
- `magic_sequence(n_shells)` — list of first n magic numbers
- `detachment_analysis()` — detachment sequence 8, 10, 12, 14 (arithmetic, step 2)
- `sqrt_rc_proximity()` — magic/Fibonacci ratios vs √R_C (82/89 matches to 0.3%)

| n | magic(n) | Name | Method |
|---|----------|------|--------|
| 0 | 2 | HO(0) | Cumulative HO |
| 1 | 8 | HO(1) | Cumulative HO |
| 2 | 20 | HO(2) | Cumulative HO |
| 3 | 28 | SO onset | +detach(3) = 8 |
| 4 | 50 | | +remain(3) + detach(4) |
| 5 | 82 | | +remain(4) + detach(5) |
| 6 | 126 | | +remain(5) + detach(6) |
| 7 | **184** | **Prediction** | +remain(6) + detach(7) |

Connection to atomic physics: d-capacity = detach(N=4) = 10 = 2×round(R_SHELL×13),
f-capacity = detach(N=6) = 14 = 2×round(R_OUTER×13).

### lattice/fibonacci.py

Fibonacci arithmetic and the shift identity:

- `fib(n)` — 1-indexed Fibonacci number (extensible table)
- `fib_index(val)` — inverse lookup: value → index
- `shift_identity(k_range)` — verifies round(F(k)/φ⁴) = F(k-4) for all k ≥ 5

### lattice/sectors.py

5-sector eigenvalue partition of the AAH spectrum:

- `sector_partition(D)` — partition D-site AAH eigenvalues into 5 sectors
- `sector_pattern_check(n_range)` — verify pattern F(n-3)|F(n-4)|F(n-3)|F(n-4)|F(n-3)

At D = 233: sectors = [55, 34, 55, 34, 55] = [F(10), F(9), F(10), F(9), F(10)].

### lattice/z_max.py

Z_max = 118 from the Fibonacci lattice:

- `z_max_formula()` — Z_max = 2F(9) + F(10) - F(5) = 68 + 55 - 5 = 118
- `d233_uniqueness()` — D = 233 = F(13) = F(F(7)) is the unique self-referential lattice
- `zd_limit()` — Z/D → 1 - 2/φ³ - 1/φ⁸ = 0.5066

### tiling/multigrid.py

de Bruijn multigrid construction for the triple metallic mean tiling:

- `build_triple_tiling()` — construct 3 grids (gold 5-fold, silver 4-fold, bronze 13-fold)
- `analyze_vertices(vertices)` — classify and count 7 vertex types (G, S, B, GS, GB, BS, GSB)

Key result: GS fraction = 14.6% ≈ LEAK = 1/φ⁴ (0.3% error).

### tiling/cosmology.py

5→3 collapse: tiling vertex fractions → cosmological budget:

- `collapse_budget(vertex_fractions)` — Ω_b, Ω_DM, Ω_DE from tiling × G1

| Budget | Formula | Predicted | Planck | Error |
|--------|---------|-----------|--------|-------|
| Ω_b | LEAK × G1 | 4.73% | 4.76% | 0.6% |
| Ω_DM | (LEAK - W⁴) + (GB+BS)×G1 | 26.7% | 26.5% | 0.8% |
| Ω_DE | Remainder | 68.5% | 68.5% | 0.1% |

### nuclear/shells.py

Nuclear shell structure from Cantor spectral ratios:

- `ho_shell_capacities()` — HO shell capacities = n(n+1) = 2 × triangular numbers
- `spin_orbit_detachment()` — detaching sublevel capacities 10, 12, 14 (arithmetic, step 2)
- `magic_fibonacci_proximity()` — distance from each magic number to nearest Fibonacci

| Magic | Nearest F | Offset | Exact? |
|-------|-----------|--------|--------|
| 2 | F(3) = 2 | 0 | Yes |
| 8 | F(6) = 8 | 0 | Yes |
| 20 | F(8) = 21 | -1 | No |
| 28 | F(8) = 21 | +7 | No |
| 50 | F(10) = 55 | -5 | No |
| 82 | F(11) = 89 | -7 | No |
| 126 | F(12) = 144 | -18 | No |

### nuclear/scale.py (UNDER DEVELOPMENT)

Nuclear-to-atomic scale transition analysis:

- `bracket_gap()` — bracket address gap between nuclear and atomic radii ≈ F(8) = 21
- `zeckendorf(n)` — non-adjacent Fibonacci decomposition
- `zeckendorf_compactness()` — island of stability prediction via Fibonacci alignment

126 has the most compact Zeckendorf representation (3 terms: 89 + 34 + 3) among
island-of-stability candidates (114, 120, 126, 184), predicting enhanced stability.

### cosmology/predictions.py

Four hierarchy predictions from three constants (phi, W, N):

| Prediction | Formula | Error |
|-----------|---------|-------|
| Fine structure | 1/alpha = N * W = 137.3 | 0.22% |
| Baryon fraction | Omega_b = W^4 = 0.048 | 2.8% |
| Gravity weakness | (sqrt(1-W^2)/phi)^136 = 10^-35.7 | 1.1% log |
| Cosmological Lambda | (1/phi)^588 = 10^-122.9 | 0.7% log |

Plus: W-polynomial dark energy budget (sums to exactly 1), MOND acceleration a0.

### crossover/operator.py

The universal Cantor crossover operator:

- `cantor_crossover(x, x_c=R_C, gamma=4, d_full=3)` — control parameter to effective dimension
- `discriminant_fibonacci_chain()` — proves exactly 3 spatial dimensions
- `alpha_nsma(r)` — N-SmA heat capacity exponent (solved open problem, 40+ years)
- `kappa_qh()`, `kappa_qah()` — quantum Hall temperature scaling
- `nu_noninteracting()`, `nu_interacting()` — plateau exponents
- `verify_sqrt5_identity()` — phi^2 * r_c = sqrt(5) (exact)
- `nsma_test()` — comparison against 11 experimental compounds

### geometry/cantor_node.py

Universal five-layer architecture at any scale:

- `cantor_node(R)` — core, inner, photo, shell, outer at radius R
- `bracket_address(r_meters)` — bz = round[log(R/l_P) / log(phi)]
- `zeckendorf(n)` — non-adjacent Fibonacci decomposition (lattice address)
- `print_scale_table()` — Cantor node from universe (4.5e26 m) to proton (8e-16 m)

### engine/gate_overflow.py

The error IS the prediction:

- `gate_overflow(Z)` — compute G(Z) for element Z
- `gate_overflow_all()` — G for all elements with radii data

G < 0 means compact cloud → energy into bonding → HARD material.
G > 0 means extended cloud → SOFT, metallic.

### engine/bond_lengths.py

Additive bond length: d_AB = r_cov(A) + r_cov(B), R² = 0.90.

Cross-scale matches:
- Benzene CC / BOS = R_BASELINE (0.01%)
- Graphite interlayer / Diamond CC = Omega_DE / Omega_M (0.4%)

### engine/hardness.py

Compound hardness from gate overflow product |G_A| x |G_B|.
5-feature model achieves R² = 0.84 on log(Vickers) for 22 compounds.
Period 2 (B, C, N) has no sigma-3 gate — makes everything superhard.

### engine/bulk_modulus.py

Bulk modulus from log(1/r_cov) + theta + |G|. R² > 0.67 on 25 elements.

### engine/ionic_radii.py

Ionic radius: r_ion(+q) = 2 x r_cov / phi^(q+1). Shannon validation for +1, +2, +3 ions.

### engine/transport.py

Transport classification by theta mode: leak = electron conductor (Ag, Cu, Au),
baseline = phonon (diamond), p-hole = semiconductor.

### geometry/discriminant_cones.py

Three cone angles from the spectral ratios:
- `cone_angles()` — leak (29°), rc (40°), baseline (45°)
- `verify_sigma4_identity()` — THETA_LEAK x BOS = sigma-4 (0.03%)
- `cone_deviation(theta)` — angular deviation as hardness predictor

### geometry/discriminant.py

The discriminant Pythagorean triangle:

- `discriminant_triangle()` — (sqrt5)^2 + (sqrt8)^2 = (sqrt13)^2, maps to Dirac E^2 = p^2*c^2 + m^2*c^4
- `three_wave_frequencies()` — gold/silver/bronze metallic mean frequencies
- `schrodinger_interpolation(v_over_c)` — Delta_eff(v) = 8 + 5(v/c)^2

---

## Test Coverage

156 tests across 15 sections:

| Section | Tests | What it verifies |
|---------|-------|-----------------|
| Core Constants | 11 | Axiom, W theorem, unity partition, identities |
| Hamiltonian & Spectrum | 18 | Matrix properties, ratios, cones, z=1 identity |
| Periodic Table | 11 | Aufbau, key elements (Ni 0.1%, Pd 0.2%), scorecard |
| Crossover Operator | 11 | Boundaries, Fibonacci chain, sqrt5, QH, N-SmA |
| Cosmology | 7 | Fine structure, W-polynomial, gravity, Lambda, MOND |
| Geometry | 11 | Cantor node, brackets, Zeckendorf, discriminant |
| Engine | 10 | Gate overflow, bond R², cross-scale, hardness, transport, g-factor |
| Cone Geometry | 4 | Three angles, leak ~29°, baseline ~45°, σ₄ identity |
| Particles | 12 | t/c=136, Koide=2/3, τ/μ=W×36, sin²θ_W, M_W, M_H, α_s, CKM |
| Aufbau Bridge | 11 | R×13 rounds to {1,3,5,7}, capacities, full Madelung, Z=118 |
| Absolute Mass | 10 | K=24/φ³, a_B 0.007%, m_e 0.23%, all boson masses <0.2% |
| Nuclear (dev) | 10 | HO shells, spin-orbit, magic/Fibonacci, bracket gap, Zeckendorf |
| Nuclear Magic | 11 | All 7 magic numbers, detachment step 2, R×13 caps, √R_C, predicts 184 |
| Lattice | 13 | Shift identity, sector partition, Z_max=118, D=233 uniqueness, Z/D limit |
| Tiling | 6 | Multigrid construction, GS ≈ LEAK, collapse budget Ω_b/Ω_DM/Ω_DE |

---

## The Framework in One Paragraph

The golden ratio phi = (1+sqrt5)/2 satisfies phi^2 = phi + 1 — this is the only axiom.
Building a 233-site Aubry-Andre-Harper Hamiltonian at irrational frequency alpha = 1/phi
and critical coupling V = 2J produces a Cantor spectrum with 34 gaps.
Five spectral ratios define a universal five-layer node that repeats at every scale
from the Hubble radius to the proton.
The gap fraction W = 0.467 generates the cosmological energy budget (Omega_DE = W^2+W),
the fine structure constant (1/alpha = 294*W), the gravity hierarchy ((sqrt(1-W^2)/phi)^136),
and the cosmological constant ((1/phi)^588).
The discriminant Fibonacci chain 5+8=13 proves exactly three spatial dimensions
and — via 2l+1 = round(R_layer × 13) — generates the Madelung subshell capacities {2, 6, 10, 14}.
The crossover operator f_dec(x) = ((x-r_c)/(1-r_c))^4 solves the 40-year-old N-SmA
universality problem and predicts quantum Hall scaling.
All from one equation. Zero free parameters.

---

## Universe Seed Model

The [universe_seed.py](../model/universe_seed.py) script builds a universe from the axiom and measures it.
It integrates all CLEAN modules into an 8-step pipeline:

1. **Tiling** — builds the triple metallic mean spatial manifold (7,962 vertices)
2. **Brackets** — assigns Zeckendorf addresses across 60 orders of magnitude
3. **Atomic** — derives subshell capacities, Madelung sequence, 92 element radii (5.0% mean)
4. **Nuclear** — reproduces all 7 magic numbers exactly, predicts 184
5. **Forces** — α⁻¹ = 137.337, α_s = 0.118, G/F_EM = 10⁻³⁵·⁷, 7 electroweak predictions
6. **Cosmology** — Ω_DE = 0.6853 (0.05%), tiling collapse budget at sub-percent
7. **t_hop** — derives 232 attosecond traversal (0.005%)
8. **Lattice** — proves D = F(F(7)) self-reference, Z_max = 118

**Scorecard: 9 exact + 11 sub-1% + 15 sub-5% = 26 measurements from ONE axiom.**

```bash
python3 model/universe_seed.py
```

---

*Copyright 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Patent Pending: US 19/560,637*
