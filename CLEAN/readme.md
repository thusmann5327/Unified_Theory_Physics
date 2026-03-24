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
    └── test_all.py           83 verification tests across all modules
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

83 tests across 8 sections:

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
The discriminant Fibonacci chain 5+8=13 proves exactly three spatial dimensions.
The crossover operator f_dec(x) = ((x-r_c)/(1-r_c))^4 solves the 40-year-old N-SmA
universality problem and predicts quantum Hall scaling.
All from one equation. Zero free parameters.

---

*Copyright 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Patent Pending: US 19/560,637*
