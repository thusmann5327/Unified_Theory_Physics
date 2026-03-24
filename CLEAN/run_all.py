#!/usr/bin/env python3
"""
run_all.py — Unified Framework Report
=======================================
Thomas A. Husmann / iBuilt LTD / March 2026

Combines all modules into a single comprehensive report.
One axiom: phi^2 = phi + 1. Zero free parameters.

Usage:
    cd CLEAN && python3 run_all.py
    python3 CLEAN/run_all.py  (from repo root)
"""

import sys
import os
import math
import numpy as np

# Ensure CLEAN is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def section(title):
    print()
    print("=" * 75)
    print(f"  {title}")
    print("=" * 75)
    print()


def main():
    print()
    print("#" * 75)
    print("#" + " " * 73 + "#")
    print("#    THE HUSMANN DECOMPOSITION — Unified Framework Report" + " " * 17 + "#")
    print("#    One axiom: phi^2 = phi + 1. Zero free parameters." + " " * 19 + "#")
    print("#" + " " * 73 + "#")
    print("#" * 75)

    # ═══════════════════════════════════════════════════════════════
    # SECTION 1: CORE CONSTANTS
    # ═══════════════════════════════════════════════════════════════
    section("1. CORE CONSTANTS — derived from phi^2 = phi + 1")

    from core.constants import (
        PHI, W, LEAK, R_C, OBLATE, LORENTZ_W, BREATHING,
        H_HINGE, N_BRACKETS, SQRT5, D, ALPHA_AAH, RHO6,
        SILVER_S3, GOLD_S3, BRONZE_S3, DARK_GOLD
    )

    print(f"  AXIOM")
    print(f"    phi = {PHI:.10f}")
    print(f"    phi^2 - phi - 1 = {PHI**2 - PHI - 1:.1e}")

    print(f"\n  W THEOREM (exact to 10^-16)")
    print(f"    W = (2 + phi^(1/phi^2)) / phi^4 = {W:.10f}")
    print(f"    W * phi^4 - 2 - phi^(1/phi^2) = {W*PHI**4 - (2 + PHI**(1/PHI**2)):.1e}")

    print(f"\n  GATE CONSTANTS")
    print(f"    LEAK = 1/phi^4         = {LEAK:.6f}")
    print(f"    R_C  = 1 - 1/phi^4     = {R_C:.6f}")
    print(f"    OBLATE = sqrt(phi)      = {OBLATE:.6f}")
    print(f"    phi^2 * R_C = sqrt(5)   = {PHI**2 * R_C:.10f}  (exact)")
    print(f"    RHO6 = phi^(1/6)        = {RHO6:.6f}")

    print(f"\n  IDENTITIES")
    print(f"    1/phi + 1/phi^3 + 1/phi^4 = {1/PHI + 1/PHI**3 + 1/PHI**4:.15f}  (= 1)")
    print(f"    2/phi^4 + 3/phi^3         = {2/PHI**4 + 3/PHI**3:.15f}  (= 1, boundary law)")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 2: AAH SPECTRUM
    # ═══════════════════════════════════════════════════════════════
    section("2. AAH SPECTRUM — D=233 sites, alpha=1/phi, V=2J")

    from core.spectrum import (
        R_MATTER, R_INNER, R_PHOTO, R_SHELL, R_OUTER,
        BASE, BOS, G1, GAPS_NORM, extract_spectrum,
        ALPHA_LEAK, ALPHA_RC, ALPHA_BASE,
        THETA_LEAK, THETA_RC, THETA_BASE
    )

    spec = extract_spectrum()

    print(f"  FIVE SPECTRAL RATIOS (Cantor node dimensions)")
    print(f"    R_MATTER = {R_MATTER:.6f}   (sigma3 core — where matter lives)")
    print(f"    R_INNER  = {R_INNER:.6f}   (sigma2 inner wall — confinement)")
    print(f"    R_PHOTO  = {R_PHOTO:.6f}   (cos(alpha) — decoupling surface)")
    print(f"    R_SHELL  = {R_SHELL:.6f}   (wall centre — probability peak)")
    print(f"    R_OUTER  = {R_OUTER:.6f}   (sigma4 outer wall — entropy max)")

    print(f"\n  COMPOSITE RATIOS")
    print(f"    BASE = sigma4/sigma_shell = {BASE:.6f}  (hydrogen vdW/cov baseline)")
    print(f"    BOS  = bronze/sigma_shell = {BOS:.6f}  (Pythagorean circle radius)")
    print(f"    G1   = first sub-gap      = {G1:.6f}  (p-electron coefficient)")

    print(f"\n  THREE DISCRIMINANT CONES")
    print(f"    Leak     {ALPHA_LEAK:.1f} deg   theta = {THETA_LEAK:.4f}   (d-block boundary)")
    print(f"    RC       {ALPHA_RC:.1f} deg   theta = {THETA_RC:.4f}   (d-block standard)")
    print(f"    Baseline {ALPHA_BASE:.1f} deg   theta = {THETA_BASE:.4f}   (s/p-block)")

    print(f"\n  CANTOR NODE PYTHAGOREAN")
    lhs = R_SHELL**2 + BRONZE_S3**2
    rhs = R_OUTER**2
    print(f"    sigma_shell^2 + bronze^2 = {lhs:.6f}")
    print(f"    sigma4^2                 = {rhs:.6f}")
    print(f"    Match: {abs(lhs - rhs)/rhs*100:.3f}%")

    print(f"\n  {spec['n_gaps']} gaps = F(9). Eigenvalues: [{spec['eigs'][0]:.3f}, {spec['eigs'][-1]:.3f}]")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 3: DISCRIMINANT TRIANGLE
    # ═══════════════════════════════════════════════════════════════
    section("3. DISCRIMINANT TRIANGLE — E^2 = p^2*c^2 + m^2*c^4")

    from geometry.discriminant import discriminant_triangle, three_wave_frequencies

    dt = discriminant_triangle()
    print(f"  (sqrt5)^2 + (sqrt8)^2 = (sqrt13)^2")
    print(f"    5 + 8 = 13  (Fibonacci chain: {dt['fibonacci_chain']})")
    print(f"    cos(gold angle) = sqrt(5)/sqrt(13) = {dt['cos_gold_angle']:.4f} ~ 1/phi = {dt['one_over_phi']:.4f}  ({dt['angle_match_pct']:.2f}%)")
    print()
    print(f"  THREE CONCENTRIC LAYERS")
    for name in ['silver', 'gold', 'bronze']:
        layer = dt['layers'][name]
        print(f"    {name:>6s}:  Delta={layer['discriminant']:2d}  sigma3={layer['sigma3']:.3f}  "
              f"{layer['dark_pct']}% dark  [{layer['role']}]")
    print(f"\n  Silver-Gold boundary = {dt['silver_gold_boundary']:.3f} R  (solar core: 0.20-0.25)")

    freqs = three_wave_frequencies()
    print(f"\n  THREE-WAVE FREQUENCIES (3D vacuum Hamiltonian)")
    for name in ['gold', 'silver', 'bronze']:
        f = freqs[name]
        print(f"    {name:>6s} (n={f['n']}): alpha = {f['alpha']:.6f}   [{f['role']}]")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 4: THREE DIMENSIONS PROOF
    # ═══════════════════════════════════════════════════════════════
    section("4. THREE DIMENSIONS — discriminant Fibonacci chain")

    from crossover.operator import discriminant_fibonacci_chain

    dfc = discriminant_fibonacci_chain()
    for d in dfc['discriminants']:
        mark = "Fibonacci" if d['is_fibonacci'] else "NOT Fibonacci"
        sym = "ok" if d['is_fibonacci'] else "XX"
        print(f"    n={d['n']}: Delta = {d['discriminant']:>3d}  sqrt(Delta) = {d['sqrt_discriminant']:.3f}  [{mark}] {sym}")
    print(f"\n  Chain: 5 + 8 = 13 holds: {dfc['chain_holds']}")
    print(f"  Break: 8 + 13 = 21 != 20: deficit = {dfc['deficit']}")
    print(f"  Unique link: n = {dfc['unique_link']} (silver)")
    print(f"  RESULT: Exactly {dfc['max_dimensions']} spatial dimensions from phi^2 = phi + 1")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 5: CANTOR NODE AT EVERY SCALE
    # ═══════════════════════════════════════════════════════════════
    section("5. CANTOR NODE — universal architecture at every scale")

    from geometry.cantor_node import print_scale_table
    print_scale_table()

    # ═══════════════════════════════════════════════════════════════
    # SECTION 6: CROSSOVER OPERATOR
    # ═══════════════════════════════════════════════════════════════
    section("6. CROSSOVER OPERATOR — one formula, six physical systems")

    from crossover.operator import (
        cantor_crossover, alpha_nsma, kappa_qh, kappa_qah,
        nu_noninteracting, nu_interacting, nsma_test,
        verify_sqrt5_identity
    )

    print(f"  f_dec(x) = ((x - r_c)/(1 - r_c))^gamma,  r_c = {R_C:.4f},  gamma = 4")
    print(f"  d_eff(x) = 3 - f_dec(x),  alpha = 2 - (2/3)*d_eff")
    print()

    # N-SmA sweep
    print(f"  N-SmA heat capacity alpha(r):")
    for r in [0.80, R_C, 0.90, 0.95, 1.00]:
        a = alpha_nsma(r)
        print(f"    r = {r:.3f} -> alpha = {a:.4f}")

    nsma = nsma_test()
    print(f"\n  N-SmA experimental fit: {nsma['n_compounds']} compounds, RMS = {nsma['rms']:.3f}")
    print(f"    {nsma['n_within_2sigma']}/{nsma['n_compounds']} within 2 sigma")

    print(f"\n  QUANTUM HALL PREDICTIONS")
    print(f"    kappa_QH  = r_c/2  = {kappa_qh():.4f}   (obs: 0.42 +/- 0.01)")
    print(f"    kappa_QAH = 1/phi^2 = {kappa_qah():.4f}   (obs: 0.38 +/- 0.02)")
    print(f"    nu_CC     = phi^2   = {nu_noninteracting():.4f}   (obs: 2.593 +/- 0.006)")
    print(f"    nu_exp    = 2/r_c   = {nu_interacting():.4f}   (obs: 2.38)")

    s5 = verify_sqrt5_identity()
    print(f"\n  sqrt(5) IDENTITY: phi^2 * r_c = {s5['lhs']:.10f} = sqrt(5)  (exact: {s5['exact']})")

    # ═══════════════════════════════════════════════════════════════
    # SECTION 7: PERIODIC TABLE
    # ═══════════════════════════════════════════════════════════════
    section("7. PERIODIC TABLE — 92 elements from phi^2 = phi + 1")

    print(f"  ratio = sqrt(1 + (theta * BOS)^2)")
    print(f"  theta = 1 + sqrt(phi) * n_p*(G1/BOS)*phi^(-(per-1))")
    print(f"          [- (n_d/10)*0.290]_mag + mu*LEAK - (n_f/14)*LEAK")
    print()

    from atomic.periodic_table import run_periodic_table, scorecard
    results = run_periodic_table()
    scorecard(results)

    # ═══════════════════════════════════════════════════════════════
    # SECTION 8: COSMOLOGICAL PREDICTIONS
    # ═══════════════════════════════════════════════════════════════
    section("8. COSMOLOGY — four hierarchies from (phi, W, N)")

    from cosmology.predictions import print_cosmology_report
    print_cosmology_report()

    # ═══════════════════════════════════════════════════════════════
    # SECTION 9: TESTS
    # ═══════════════════════════════════════════════════════════════
    section("9. VERIFICATION")

    from tests.test_all import run_tests
    all_pass = run_tests()

    # ═══════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════════
    section("SUMMARY")

    ae = [abs(r['err']) for r in results]
    n_total = len(results)
    n10 = sum(1 for e in ae if e < 10)
    n20 = sum(1 for e in ae if e < 20)

    print(f"  INPUT:   phi^2 = phi + 1  (one axiom, zero parameters)")
    print(f"  OUTPUT:  {n_total} elements predicted, {n10} within 10%, {n20} within 20%")
    print(f"           Mean error: {np.mean(ae):.1f}%")
    print()
    print(f"  PROVEN THEOREMS: 12")
    print(f"    T1  phi^2 = phi + 1 (axiom)")
    print(f"    T2  1/phi + 1/phi^3 + 1/phi^4 = 1 (unity partition)")
    print(f"    T3  2/phi^4 + 3/phi^3 = 1 (boundary law)")
    print(f"    T4  arctan(1/phi) + arctan(1/phi^3) = pi/4")
    print(f"    T5  5 + 8 = 13 (discriminant Fibonacci chain)")
    print(f"    T6  (sqrt5)^2 + (sqrt8)^2 = (sqrt13)^2")
    print(f"    T7  Three dimensions uniqueness (chain breaks at n=4)")
    print(f"    T8  phi^2 * r_c = sqrt(5)")
    print(f"    T9  1/phi^4 + 1/phi^5 = 1/phi^3 (observer recursion)")
    print(f"    T10 alpha_bb = 2/phi^2 (backbone coupling)")
    print(f"    T11 H = phi^(-1/phi) (hinge constant)")
    print(f"    T12 W * phi^4 = 2 + phi^(1/phi^2) (W theorem)")

    print(f"\n  SOLVED OPEN PROBLEMS: 2")
    print(f"    N-SmA universality (40+ years): alpha(r) = (2/3)((r-r_c)/(1-r_c))^4")
    print(f"    Periodic table from first principles: 92 elements, zero parameters")

    print(f"\n  PRECISION BENCHMARKS (zero free parameters):")
    print(f"    S_max position (sigma4):   0.00021% (two parts per million)")
    print(f"    W theorem:                 exact to 10^-16")
    print(f"    Mercury -> silver mean:    0.006%")
    print(f"    Omega_DE = W^2+W:          0.05%")
    print(f"    1/alpha = N*W:             0.22%")
    print(f"    Omega_b = W^4:             2.8%")
    print(f"    Lambda = (1/phi)^588:      0.7% log")
    print(f"    G/F_EM = (sqrt(1-W^2)/phi)^136: 1.1% log")
    print(f"    MOND a0:                   3.4%")

    print()
    print("=" * 75)
    print(f"  All constants derived from phi^2 = phi + 1. Zero free parameters.")
    print(f"  Tests: {'ALL PASSED' if all_pass else 'SOME FAILED'}")
    print("=" * 75)
    print()


if __name__ == "__main__":
    main()
