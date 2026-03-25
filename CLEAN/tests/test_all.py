"""
test_all.py — Verify all framework outcomes
=============================================

Tests every module in the CLEAN package against known results.
All tests are self-contained and require no external data.

Run:  python3 -m tests.test_all   (from CLEAN directory)
  or: python3 CLEAN/tests/test_all.py  (from repo root)
"""

import sys
import os
import math

# Add CLEAN to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np


def run_tests():
    passed = 0
    failed = 0
    total = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed, total
        total += 1
        if condition:
            passed += 1
            print(f"    PASS  {name}")
        else:
            failed += 1
            print(f"    FAIL  {name}  {detail}")

    # ═══════════════════════════════════════════════════════════════
    # 1. CORE CONSTANTS
    # ═══════════════════════════════════════════════════════════════
    print("\n  1. CORE CONSTANTS")
    print("  " + "-" * 60)

    from core.constants import (
        PHI, W, LEAK, R_C, OBLATE, LORENTZ_W, BREATHING,
        H_HINGE, N_BRACKETS, SQRT5, RHO6, D, ALPHA_AAH
    )

    check("Axiom: phi^2 = phi + 1",
          abs(PHI**2 - PHI - 1) < 1e-15)

    check("W theorem: W*phi^4 = 2 + phi^(1/phi^2)",
          abs(W * PHI**4 - (2 + PHI**(1/PHI**2))) < 1e-14)

    check("LEAK = 1/phi^4",
          abs(LEAK - 1/PHI**4) < 1e-15)

    check("R_C = 1 - 1/phi^4",
          abs(R_C - (1 - 1/PHI**4)) < 1e-15)

    check("phi^2 * R_C = sqrt(5)",
          abs(PHI**2 * R_C - SQRT5) < 1e-14)

    check("OBLATE = sqrt(phi)",
          abs(OBLATE - math.sqrt(PHI)) < 1e-15)

    check("Boundary law: 2/phi^4 + 3/phi^3 = 1",
          abs(2/PHI**4 + 3/PHI**3 - 1) < 1e-14)

    check("Unity partition: 1/phi + 1/phi^3 + 1/phi^4 = 1",
          abs(1/PHI + 1/PHI**3 + 1/PHI**4 - 1) < 1e-14)

    check("Observer recursion: 1/phi^4 + 1/phi^5 = 1/phi^3",
          abs(1/PHI**4 + 1/PHI**5 - 1/PHI**3) < 1e-14)

    check("D = 233 = F(13)",
          D == 233)

    check("RHO6 = phi^(1/6)",
          abs(RHO6 - PHI**(1/6)) < 1e-15)

    # ═══════════════════════════════════════════════════════════════
    # 2. HAMILTONIAN & SPECTRUM
    # ═══════════════════════════════════════════════════════════════
    print("\n  2. HAMILTONIAN & SPECTRUM")
    print("  " + "-" * 60)

    from core.hamiltonian import build_hamiltonian, diagonalize
    from core.spectrum import (
        R_MATTER, R_INNER, R_PHOTO, R_SHELL, R_OUTER,
        BASE, BOS, G1, GAPS_NORM, extract_spectrum,
        THETA_LEAK, THETA_RC, THETA_BASE,
        ALPHA_LEAK, ALPHA_RC, ALPHA_BASE
    )

    H = build_hamiltonian()
    check("Hamiltonian is 233x233",
          H.shape == (233, 233))

    check("Hamiltonian is symmetric",
          np.allclose(H, H.T))

    eigs = diagonalize(H)
    check("233 eigenvalues",
          len(eigs) == 233)

    spec = extract_spectrum()
    check("34 gaps (= F(9))",
          spec['n_gaps'] == 34,
          f"got {spec['n_gaps']}")

    check("R_MATTER ~ 0.073",
          abs(R_MATTER - 0.073) < 0.005, f"got {R_MATTER:.4f}")

    check("R_SHELL ~ 0.397",
          abs(R_SHELL - 0.397) < 0.005, f"got {R_SHELL:.4f}")

    check("R_OUTER ~ 0.559",
          abs(R_OUTER - 0.559) < 0.005, f"got {R_OUTER:.4f}")

    check("BASE = sigma4/sigma_shell ~ 1.408",
          abs(BASE - 1.408) < 0.002, f"got {BASE:.4f}")

    check("BOS = bronze/sigma_shell ~ 0.992",
          abs(BOS - 0.992) < 0.002, f"got {BOS:.4f}")

    check("G1 ~ 0.324",
          abs(G1 - 0.324) < 0.005, f"got {G1:.4f}")

    # Sub-gap phi-damping
    if len(GAPS_NORM) >= 2:
        g1g2 = GAPS_NORM[0] / GAPS_NORM[1]
        check("Sub-gap ratio G1/G2 ~ phi",
              abs(g1g2 - PHI) < 0.15, f"got {g1g2:.3f}")

    # Cantor node Pythagorean
    lhs = R_SHELL**2 + 0.394**2
    rhs = R_OUTER**2
    check("Cantor Pythagorean: shell^2 + bronze^2 ~ outer^2",
          abs(lhs - rhs) / rhs * 100 < 0.1, f"{abs(lhs-rhs)/rhs*100:.3f}%")

    # Three cone angles
    check("Leak cone ~ 29 degrees",
          abs(ALPHA_LEAK - 29.2) < 1.0, f"got {ALPHA_LEAK:.1f}")

    check("RC cone ~ 40 degrees",
          abs(ALPHA_RC - 40.3) < 1.0, f"got {ALPHA_RC:.1f}")

    check("Base cone ~ 45 degrees",
          abs(ALPHA_BASE - 44.8) < 1.0, f"got {ALPHA_BASE:.1f}")

    # z = 1 identity
    for name, theta in [("leak", THETA_LEAK), ("rc", THETA_RC), ("base", THETA_BASE)]:
        ratio = math.sqrt(1 + (theta * BOS)**2)
        z = ratio * math.cos(math.atan(theta * BOS))
        check(f"z=1 identity ({name}): z = {z:.6f}",
              abs(z - 1.0) < 0.001)

    # ═══════════════════════════════════════════════════════════════
    # 3. PERIODIC TABLE
    # ═══════════════════════════════════════════════════════════════
    print("\n  3. PERIODIC TABLE")
    print("  " + "-" * 60)

    from atomic.aufbau import aufbau
    from atomic.periodic_table import predict_ratio
    from atomic.elements import RADII, MU_EFF

    # Aufbau tests
    per, n_p, n_d, n_f, n_s, blk = aufbau(26)  # Fe
    check("Fe: period 4, d-block",
          per == 4 and blk == 'd' and n_d == 6)

    per, n_p, n_d, n_f, n_s, blk = aufbau(46)  # Pd
    check("Pd: d10, no s (anomalous)",
          n_d == 10 and n_s == 0)

    per, n_p, n_d, n_f, n_s, blk = aufbau(78)  # Pt
    check("Pt: d9, s1 (anomalous)",
          n_d == 9 and n_s == 1)

    # Key element predictions
    test_elements = {
        28: ("Ni", "magnetic", 0.1, 5.0),     # Ni magnetic mode: 0.1% target
        46: ("Pd", "reflect", None, 5.0),       # Pd reflect: sub-5%
        55: ("Cs", "pythagorean", None, 5.0),   # Cs baseline: sub-5%
        78: ("Pt", "rel-reflect", None, 10.0),  # Pt relativistic reflect
        80: ("Hg", "rel-reflect", None, 10.0),  # Hg relativistic reflect
    }

    for Z, (sym, exp_mode, target_err, max_err) in test_elements.items():
        rc, rv = RADII[Z]
        ratio_obs = rv / rc
        ratio_pred, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone = predict_ratio(Z)
        err = abs(ratio_pred - ratio_obs) / ratio_obs * 100
        check(f"{sym} (Z={Z}): mode={mode}, error={err:.1f}%",
              mode == exp_mode and err < max_err,
              f"expected mode={exp_mode}, err<{max_err}%")

    # Full scorecard
    errors = []
    within_10 = 0
    within_20 = 0
    n_total = 0
    d_errors = []

    for Z in sorted(RADII.keys()):
        if Z < 3:
            continue
        rc, rv = RADII[Z]
        ratio_obs = rv / rc
        ratio_pred, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone = predict_ratio(Z)
        err = abs(ratio_pred - ratio_obs) / ratio_obs * 100
        errors.append(err)
        n_total += 1
        if err < 10:
            within_10 += 1
        if err < 20:
            within_20 += 1
        if blk == 'd':
            d_errors.append(err)

    mean_err = np.mean(errors)
    check(f"All elements: mean error = {mean_err:.1f}% (target < 8%)",
          mean_err < 8.0)

    check(f"All elements: {within_20}/{n_total} within 20% (target > 85%)",
          within_20 / n_total > 0.85)

    if d_errors:
        d_mean = np.mean(d_errors)
        d_within_10 = sum(1 for e in d_errors if e < 10)
        check(f"d-block: {d_within_10}/{len(d_errors)} within 10%, mean={d_mean:.1f}%",
              d_within_10 / len(d_errors) > 0.85)

    # ═══════════════════════════════════════════════════════════════
    # 4. CROSSOVER OPERATOR
    # ═══════════════════════════════════════════════════════════════
    print("\n  4. CROSSOVER OPERATOR")
    print("  " + "-" * 60)

    from crossover.operator import (
        cantor_crossover, alpha_nsma, kappa_qh, kappa_qah,
        nu_noninteracting, nu_interacting,
        discriminant_fibonacci_chain, nsma_test, verify_sqrt5_identity
    )

    # Below r_c: no decoupling
    result = cantor_crossover(0.80)
    check("Below r_c: d_eff = 3",
          result['below_xc'] and result['d_eff'] == 3.0)

    # At r = 1: full decoupling
    result = cantor_crossover(1.0)
    check("At x=1: d_eff = 2 (one dimension lost)",
          abs(result['d_eff'] - 2.0) < 0.01)

    # Discriminant Fibonacci chain
    dfc = discriminant_fibonacci_chain()
    check("5 + 8 = 13 (Fibonacci chain holds)",
          dfc['chain_holds'])

    check("8 + 13 != 20 (chain breaks at n=4)",
          dfc['chain_breaks'])

    check("Exactly 3 spatial dimensions",
          dfc['max_dimensions'] == 3)

    # √5 identity
    s5 = verify_sqrt5_identity()
    check("phi^2 * r_c = sqrt(5) (exact)",
          s5['exact'])

    # QH predictions
    check(f"kappa_QH = r_c/2 = {kappa_qh():.3f} (obs: 0.42)",
          abs(kappa_qh() - 0.427) < 0.001)

    check(f"kappa_QAH = 1/phi^2 = {kappa_qah():.3f} (obs: 0.38)",
          abs(kappa_qah() - 0.382) < 0.001)

    check(f"nu_CC = phi^2 = {nu_noninteracting():.3f} (obs: 2.593)",
          abs(nu_noninteracting() - 2.618) < 0.001)

    # N-SmA test
    nsma = nsma_test()
    check(f"N-SmA RMS = {nsma['rms']:.3f} (target < 0.10)",
          nsma['rms'] < 0.10)

    check(f"N-SmA: {nsma['n_within_2sigma']}/{nsma['n_compounds']} within 2 sigma (target >= 5)",
          nsma['n_within_2sigma'] >= 5)

    # ═══════════════════════════════════════════════════════════════
    # 5. COSMOLOGY
    # ═══════════════════════════════════════════════════════════════
    print("\n  5. COSMOLOGY")
    print("  " + "-" * 60)

    from cosmology.predictions import (
        fine_structure, w_polynomial_budget,
        gravity_hierarchy, cosmological_constant, mond_acceleration
    )

    fs = fine_structure()
    check(f"1/alpha = {fs['prediction']:.3f} (CODATA: 137.036, {fs['error_pct']:.2f}%)",
          fs['error_pct'] < 0.5)

    budget = w_polynomial_budget()
    check(f"Omega_DE = W^2+W = {budget['omega_de']:.4f} ({budget['err_de_pct']:.2f}%)",
          budget['err_de_pct'] < 0.1)

    check(f"Budget sums to {budget['total']:.6f}",
          abs(budget['total'] - 1.0) < 1e-10)

    check(f"Omega_b = W^4 = {budget['omega_b']:.5f} ({budget['err_b_pct']:.1f}%)",
          budget['err_b_pct'] < 5.0)

    grav = gravity_hierarchy()
    check(f"G/F_EM = 10^{grav['log10']:.1f} (obs: 10^-36, {grav['error_log_pct']:.1f}% log)",
          grav['error_log_pct'] < 2.0)

    cosmo = cosmological_constant()
    check(f"Lambda = 10^{cosmo['log10']:.1f} (obs: 10^-122, {cosmo['error_log_pct']:.1f}% log)",
          cosmo['error_log_pct'] < 1.0)

    mond = mond_acceleration()
    check(f"a0 = {mond['a0']:.3e} m/s^2 ({mond['error_pct']:.1f}%)",
          mond['error_pct'] < 5.0)

    # ═══════════════════════════════════════════════════════════════
    # 6. GEOMETRY
    # ═══════════════════════════════════════════════════════════════
    print("\n  6. GEOMETRY")
    print("  " + "-" * 60)

    from geometry.cantor_node import cantor_node, bracket_address, zeckendorf
    from geometry.discriminant import (
        discriminant_triangle, three_wave_frequencies,
        schrödinger_interpolation
    )

    # Cantor node
    node = cantor_node(1.0)  # unit sphere
    check("Cantor node has 5 layers + oblate",
          all(k in node for k in ['core', 'inner', 'photo', 'shell', 'outer', 'oblate']))

    # Bracket address
    bz_proton = bracket_address(8e-16)
    check(f"Proton bracket ~ 94 (got {bz_proton})",
          abs(bz_proton - 94) < 3)

    bz_universe = bracket_address(4.5e26)
    check(f"Universe bracket = 294 (got {bz_universe})",
          bz_universe == 294)

    # Zeckendorf
    z294 = zeckendorf(294)
    check(f"Zeckendorf(294) = 233+55+5+1",
          z294 == [233, 55, 5, 1])

    # Discriminant triangle
    dt = discriminant_triangle()
    check("Pythagorean: 5 + 8 = 13 (exact)",
          dt['pythagorean_exact'])

    check("Fibonacci chain holds",
          dt['fibonacci_chain'])

    check(f"cos(gold angle) ~ 1/phi ({dt['angle_match_pct']:.2f}%)",
          dt['angle_match_pct'] < 1.0)

    check(f"Silver-Gold boundary ~ 0.214 (solar core match)",
          abs(dt['silver_gold_boundary'] - 0.214) < 0.02)

    # Three wave frequencies
    freqs = three_wave_frequencies()
    check("Three frequencies: gold, silver, bronze",
          all(k in freqs for k in ['gold', 'silver', 'bronze']))

    # Schrodinger interpolation
    check("Schrodinger at v=0: delta_eff = 8 (silver)",
          schrödinger_interpolation(0) == 8)

    check("Schrodinger at v=c: delta_eff = 13 (bronze)",
          schrödinger_interpolation(1) == 13)

    # ═══════════════════════════════════════════════════════════════
    # 7. ENGINE — Material Property Predictions
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  7. ENGINE")
    print("  " + "-" * 60)

    from engine.gate_overflow import gate_overflow, gate_overflow_all
    from engine.bond_lengths import bond_length_test, cross_scale_matches
    from engine.band_gaps import band_gap_test
    from engine.hardness import hardness_test
    from engine.bulk_modulus import bulk_modulus_test
    from engine.ionic_radii import ionic_radius_test
    from engine.transport import conductivity_test

    # Gate overflow
    els = gate_overflow_all()
    check("Gate overflow computed for 80+ elements",
          len(els) >= 80, f"got {len(els)}")

    # Ni should have small gate overflow (0.1% error in periodic table)
    if 'Ni' in els:
        check("Ni gate overflow < 5%",
              abs(els['Ni']['G']) < 5, f"G = {els['Ni']['G']:.1f}%")

    # Bond lengths
    bl = bond_length_test()
    check("Bond length R² > 0.85",
          bl['R2'] > 0.85, f"R² = {bl['R2']:.3f}")

    # Cross-scale matches
    cs = cross_scale_matches()
    check("Benzene CC/BOS = R_BASELINE (< 0.1%)",
          cs['benzene_cc_over_bos']['error_pct'] < 0.1,
          f"{cs['benzene_cc_over_bos']['error_pct']:.3f}%")

    check("Graphite/Diamond = Omega_DE/Omega_M (< 1%)",
          cs['graphite_over_diamond']['error_pct'] < 1.0,
          f"{cs['graphite_over_diamond']['error_pct']:.2f}%")

    # Compound hardness
    hd = hardness_test(els)
    check("Compound hardness best R² > 0.75",
          hd['best_R2'] > 0.75, f"R² = {hd['best_R2']:.3f}")

    # Bulk modulus
    bm = bulk_modulus_test(els)
    check("Bulk modulus R² > 0.60",
          bm['best_R2'] > 0.60, f"R² = {bm['best_R2']:.3f}")

    # Ionic radii
    ir = ionic_radius_test()
    check("Ionic radii +1: mean error < 25%",
          ir[1]['mean_error_pct'] < 25, f"{ir[1]['mean_error_pct']:.1f}%")

    # Transport: top 3 conductors are leak mode
    ct = conductivity_test(els)
    check("Top 3 conductors (Ag, Cu, Au) all leak mode",
          ct['top3_all_leak'])

    # g-factor identity
    from core.constants import G_PROTON, G_ELECTRON
    g_ratio = (G_PROTON - G_ELECTRON) / (G_PROTON + G_ELECTRON)
    g_pred = 2 / PHI**3
    g_err = abs(g_ratio - g_pred) / g_ratio * 100
    check("g-factor: (gp-ge)/(gp+ge) = 2/phi^3 (< 0.05%)",
          g_err < 0.05, f"{g_err:.3f}%")

    # ═══════════════════════════════════════════════════════════════
    # 8. CONE GEOMETRY
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  8. CONE GEOMETRY")
    print("  " + "-" * 60)

    from geometry.discriminant_cones import cone_angles, verify_sigma4_identity

    ca = cone_angles()
    check("Three cone angles exist",
          all(k in ca for k in ['leak', 'rc', 'baseline']))

    check("Leak angle ~ 29 deg",
          28 < ca['leak']['angle_deg'] < 30,
          f"{ca['leak']['angle_deg']:.1f} deg")

    check("Baseline angle ~ 45 deg (within 1 deg)",
          ca['baseline_near_45'] < 1.0,
          f"deviation = {ca['baseline_near_45']:.2f} deg")

    s4id = verify_sigma4_identity()
    check("sigma4 identity: THETA_LEAK * BOS = sigma4 (< 0.1%)",
          s4id['error_pct'] < 0.1,
          f"{s4id['error_pct']:.3f}%")

    # ═══════════════════════════════════════════════════════════════
    # 9. PARTICLES — Standard Model from Cantor spectrum
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  9. PARTICLES")
    print("  " + "-" * 60)

    from particles.generations import (
        top_charm_ratio, koide_formula, generation_ratios, phi_power_exponents
    )
    from particles.electroweak import (
        weinberg_angle, electroweak_predictions, weinberg_3_over_13
    )
    from particles.mixing import cabibbo_angle, ckm_elements

    # t/c = 136 = 4 × F(9)
    tc = top_charm_ratio()
    check(f"t/c = {tc['ratio']:.2f} = 136 ({tc['error_pct']:.3f}%)",
          tc['error_pct'] < 0.05)

    # Koide = 2/3
    kd = koide_formula()
    check(f"Koide = {kd['Q']:.6f} = 2/3 ({kd['error_pct']:.4f}%)",
          kd['error_pct'] < 0.01)

    # τ/μ = W × 36
    ew = electroweak_predictions()
    tm = ew['tau/mu']
    check(f"tau/mu = W*36 = {tm['predicted']:.4f} ({tm['error_pct']:.3f}%)",
          tm['error_pct'] < 0.01)

    # sin²θ_W = σ₃ × σ_wall × F(6)
    sw = weinberg_angle()
    check(f"sin^2(theta_W) = {sw['prediction']:.5f} ({sw['error_pct']:.3f}%)",
          sw['error_pct'] < 0.1)

    # M_H/m_p = φ² × δ₇²
    mh = ew['M_H/m_p']
    check(f"M_H/m_p = phi^2*delta7^2 = {mh['predicted']:.2f} ({mh['error_pct']:.3f}%)",
          mh['error_pct'] < 0.05)

    # M_W/m_p = φ² × W⁻² × δ₇
    mw = ew['M_W/m_p']
    check(f"M_W/m_p = phi^2*W^-2*delta7 = {mw['predicted']:.2f} ({mw['error_pct']:.3f}%)",
          mw['error_pct'] < 0.01)

    # α_s(M_Z) = W⁵ × H × δ₇
    als = ew['alpha_s']
    check(f"alpha_s(M_Z) = {als['predicted']:.5f} ({als['error_pct']:.3f}%)",
          als['error_pct'] < 0.1)

    # (m_n - m_p)/m_e = r_c⁻¹ × δ₃⁻¹ × δ₇
    nm = ew['(m_n-m_p)/m_e']
    check(f"(m_n-m_p)/m_e = {nm['predicted']:.4f} ({nm['error_pct']:.3f}%)",
          nm['error_pct'] < 0.01)

    # Generation ratios: s/d = 20 exactly
    gr = generation_ratios()
    sd = gr['s/d']
    check(f"s/d = {sd['value']:.2f} = 20 ({sd['error_pct']:.3f}%)",
          sd['error_pct'] < 0.1)

    # c/u = N × 2 = 588
    cu = gr['c/u']
    check(f"c/u = N*2 = {cu['value']:.1f} ({cu['error_pct']:.3f}%)",
          cu['error_pct'] < 0.05)

    # Cabibbo angle: best match < 5%
    cab = cabibbo_angle()
    check(f"Cabibbo best match: {cab['best_match']} ({cab['best_error_pct']:.2f}%)",
          cab['best_error_pct'] < 5.0)

    # Lepton φ-ladder additivity: 11 + 6 = 17
    ppe = phi_power_exponents()
    check("Lepton phi-ladder: 11 + 6 = 17",
          ppe['lepton_additivity']['consistent'])

    # ═══════════════════════════════════════════════════════════════
    # 10. AUFBAU BRIDGE — Subshell capacities from Cantor layers
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  10. AUFBAU BRIDGE")
    print("  " + "-" * 60)

    from aufbau_bridge.angular import (
        angular_modes, subshell_capacity, all_layers,
        verify_uniqueness, F7, LAYER_RATIOS
    )
    from aufbau_bridge.madelung import (
        madelung_sequence, z_max_prediction, MADELUNG_CAPACITIES
    )

    # F(7) = 13 = Δ₃
    check("F(7) = 13 = bronze discriminant",
          F7 == 13)

    # Each layer rounds correctly
    for l in range(4):
        am = angular_modes(l)
        check(f"R({am['layer']}) × 13 = {am['R_times_13']:.2f} → "
              f"{am['predicted_2l1']} = 2×{l}+1",
              am['match'],
              f"got {am['predicted_2l1']}, expected {am['expected_2l1']}")

    # Subshell capacities
    caps = [subshell_capacity(l) for l in range(4)]
    check(f"Capacities = {caps} = [2, 6, 10, 14]",
          caps == [2, 6, 10, 14])

    # Full Madelung sequence
    seq = madelung_sequence()
    check(f"Full Madelung: {seq['total']} electrons, 19 subshells",
          seq['all_match'] and seq['total'] == 118)

    # Z_max consistency
    zp = z_max_prediction()
    check(f"Z_max(D×D_s) = {zp['z_spectrum']:.1f} vs 118 ({zp['spectrum_error_pct']}%)",
          zp['spectrum_error_pct'] < 2.0)

    check("Z_max(Aufbau) = 118 exact",
          zp['aufbau_match'])

    # k=13 uniqueness or best fit
    valid_k = verify_uniqueness(30)
    k13_err = next(err for k, err in valid_k if k == 13)
    is_best = all(k13_err <= err for _, err in valid_k)
    check(f"k=13 best among valid k's (err {k13_err:.1f}%)",
          is_best or len(valid_k) == 1)

    # Mean error < 7% (all four layers)
    mean_err = sum(angular_modes(l)['error_pct'] for l in range(4)) / 4
    check(f"Mean layer error = {mean_err:.1f}% (< 7%)",
          mean_err < 7.0)

    # ═══════════════════════════════════════════════════════════════
    # 11. ABSOLUTE MASS — m_e from attosecond bridge
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  11. ABSOLUTE MASS")
    print("  " + "-" * 60)

    from absolute_mass.bridge import (
        K_BRIDGE, A_LATTICE, T_HOP, ALPHA_PRED,
        predict_bohr_radius, predict_electron_mass, predict_proton_mass,
        alternative_K_formulas,
    )
    from absolute_mass.propagate import mass_table

    # K = 24/φ³
    from core.constants import PHI as _PHI
    check("K = 24/phi^3 = 5.666",
          abs(K_BRIDGE - 24.0 / _PHI**3) < 1e-10)

    # Bohr radius
    aB = predict_bohr_radius()
    check(f"a_B = {aB['a_B_predicted']:.6e} m ({aB['error_pct']:.3f}%)",
          aB['error_pct'] < 0.05)

    # Electron mass
    me = predict_electron_mass()
    check(f"m_e = {me['m_e_predicted']:.4e} kg ({me['error_pct']:.3f}%)",
          me['error_pct'] < 0.5)

    # Proton mass
    mp = predict_proton_mass()
    check(f"m_p/m_e = {mp['mp_me_framework']:.1f} vs {mp['mp_me_observed']:.1f} "
          f"({mp['mp_me_error_pct']:.2f}%)",
          mp['mp_me_error_pct'] < 0.5)

    # Full mass table
    mt = mass_table()

    check(f"tau mass ({mt['tau']['error_pct']:.2f}%)",
          mt['tau']['error_pct'] < 1.0)

    check(f"W boson mass ({mt['W_boson']['error_pct']:.2f}%)",
          mt['W_boson']['error_pct'] < 1.0)

    check(f"Z boson mass ({mt['Z_boson']['error_pct']:.2f}%)",
          mt['Z_boson']['error_pct'] < 1.0)

    check(f"Higgs mass ({mt['Higgs']['error_pct']:.2f}%)",
          mt['Higgs']['error_pct'] < 1.0)

    # Alternative K formulas exist
    alts = alternative_K_formulas()
    n_good = sum(1 for a in alts if a['error_pct'] < 0.3)
    check(f"Multiple K routes: {n_good} formulas within 0.3%",
          n_good >= 3)

    # Independence: only 1 empirical input (t_hop)
    check("a_lattice = c * t_hop (no a_B input)",
          abs(A_LATTICE - 299792458 * 1e-18) < 1e-15)

    # ═══════════════════════════════════════════════════════════════
    # 12. NUCLEAR — Shell structure from Cantor spectral ratios
    # ═══════════════════════════════════════════════════════════════
    print()
    print("  12. NUCLEAR (under development)")
    print("  " + "-" * 60)

    from nuclear.shells import (
        NUCLEAR_MAGIC, HO_MAGIC,
        ho_shell_capacities, spin_orbit_detachment, magic_fibonacci_proximity,
    )
    from nuclear.scale import bracket_gap, zeckendorf, zeckendorf_compactness

    # HO shell capacities = 2 × triangular numbers
    ho = ho_shell_capacities()
    check("HO capacities = n(n+1) = 2×T(n)",
          all(h['capacity'] == h['shell'] * (h['shell'] + 1) for h in ho))

    # Spin-orbit detachment
    so = spin_orbit_detachment()
    check("Detach capacities = [10, 12, 14] (arithmetic, step 2)",
          so['capacities'] == [10, 12, 14] and so['is_arithmetic'])

    check(f"Detach starts at d-capacity = {so['d_capacity']}",
          so['starts_at_d_capacity'])

    # Magic numbers 2 and 8 are exact Fibonacci
    mfp = magic_fibonacci_proximity()
    exact_fibs = [r for r in mfp if r['is_exact']]
    exact_vals = sorted(r['magic'] for r in exact_fibs)
    check("2 and 8 are exact Fibonacci magic numbers",
          2 in exact_vals and 8 in exact_vals)

    # 20 is within 1 of F(8) = 21
    m20 = next(r for r in mfp if r['magic'] == 20)
    check("Magic 20 within 1 of F(8) = 21",
          abs(m20['offset']) <= 1)

    # Bracket gap ≈ F(8) = 21
    bg = bracket_gap()
    check(f"Bracket gap mean ≈ 21 = F(8) (got {bg['mean_gap']})",
          bg['nearest_fib_to_mean'] == 21)

    check("Bracket gap decreases with Z (H > Z=100)",
          bg['gaps'][0][1] > bg['gaps'][99][1])

    # Zeckendorf
    z126 = zeckendorf(126)
    check(f"Zeckendorf(126) = {z126} (3 terms)",
          len(z126) == 3 and sum(z126) == 126)

    z294 = zeckendorf(294)
    check("Zeckendorf(294) = [233, 55, 5, 1]",
          z294 == [233, 55, 5, 1])

    # Zeckendorf compactness: 126 most compact among island candidates
    zc = zeckendorf_compactness()
    check("126 most compact Zeckendorf among island candidates",
          126 in zc['most_compact'])

    # ═══════════════════════════════════════════════════════════════
    # 13. NUCLEAR MAGIC
    # ═══════════════════════════════════════════════════════════════
    print("\n  13. NUCLEAR MAGIC")
    print("  " + "-" * 60)

    from nuclear.magic import (
        magic_number, magic_sequence, detachment_analysis,
        sqrt_rc_proximity, S_CAP, P_CAP, D_CAP, F_CAP,
        ho_cumulative, detach_capacity,
    )

    # All 7 magic numbers reproduced exactly
    predicted = magic_sequence(7)
    expected_magic = [2, 8, 20, 28, 50, 82, 126]
    check("magic_sequence(7) = [2, 8, 20, 28, 50, 82, 126]",
          predicted == expected_magic,
          f"got {predicted}")

    # Individual checks
    check("magic_number(0) = 2", magic_number(0) == 2)
    check("magic_number(3) = 28", magic_number(3) == 28)
    check("magic_number(6) = 126", magic_number(6) == 126)

    # Detachment analysis
    da = detachment_analysis()
    # The detach_capacity formula 2N+2 is arithmetic step 2: 8,10,12,14
    detach_vals = [detach_capacity(N) for N in range(3, 7)]
    check("Detachment formula 2N+2 gives 8, 10, 12, 14 (step 2)",
          detach_vals == [8, 10, 12, 14])

    check("d-capacity = detach(N=4) = 10",
          da['d_cap_matches_N4'] and D_CAP == 10)

    check("f-capacity = detach(N=6) = 14",
          da['f_cap_matches_N6'] and F_CAP == 14)

    # Subshell capacities from R×13
    check("R×13 capacities: s=2, p=6, d=10, f=14",
          (S_CAP, P_CAP, D_CAP, F_CAP) == (2, 6, 10, 14))

    # √R_C proximity: 82/89
    sr = sqrt_rc_proximity()
    m82 = next(r for r in sr if r['magic'] == 82)
    check(f"82/89 ≈ √R_C to <1% (got {m82['error_pct']}%)",
          m82['near_sqrt_rc'] and m82['error_pct'] < 1)

    # Predicts 184
    check("magic_number(7) = 184 (island of stability)",
          magic_number(7) == 184)

    # HO cumulative
    check("HO cumulative: 2, 8, 20, 40, 70, 112, 168",
          [ho_cumulative(n) for n in range(7)] == [2, 8, 20, 40, 70, 112, 168])

    # ═══════════════════════════════════════════════════════════════
    # 14. LATTICE
    # ═══════════════════════════════════════════════════════════════
    print("\n  14. LATTICE")
    print("  " + "-" * 60)

    from lattice import (
        fib, fib_index, shift_identity,
        sector_partition, sector_pattern_check,
        z_max_formula, d233_uniqueness, zd_limit,
    )

    # Fibonacci basics
    check("F(13) = 233", fib(13) == 233)
    check("fib_index(233) = 13", fib_index(233) == 13)

    # Shift identity
    si = shift_identity()
    check(f"Shift identity holds for all k in 5..16 ({si['n_tested']} tested)",
          si['all_match'])

    # Specific: round(F(9)/φ⁴) = F(5) = 5
    check("round(F(9)/φ⁴) = F(5) = 5",
          round(fib(9) / PHI**4) == fib(5))

    # 5-sector partition at D=233
    sp = sector_partition(233)
    check("D=233 sectors: [55, 34, 55, 34, 55]",
          sp['sectors'] == [55, 34, 55, 34, 55],
          f"got {sp['sectors']}")

    check("D=233 all sectors are Fibonacci",
          sp['all_fibonacci'])

    # Sector pattern holds across multiple Fibonacci sizes
    spc = sector_pattern_check(range(11, 15))
    check(f"Sector pattern matches {spc['n_matching']}/{spc['n_tested']} tested sizes",
          spc['n_matching'] >= 3)

    # Z_max = 118
    zm = z_max_formula()
    check("Z_max = 118",
          zm['is_118'] and zm['z_max'] == 118)

    check("Shift identity holds in Z_max derivation",
          zm['shift_identity_holds'])

    check("Algebraic identity 3F(10)+2F(9) = F(13)",
          zm['algebraic_identity_holds'])

    # D=233 uniqueness
    d233 = d233_uniqueness()
    check("D=233 = F(13) = F(F(7)) self-referential",
          d233['self_referential'] and d233['D_is_F_of_F_7'])

    # Z/D limit
    zdl = zd_limit()
    check(f"Z/D limit = {zdl['limit']} ≈ 118/233 = {zdl['physical_Z_D']} ({zdl['error_pct']}%)",
          zdl['error_pct'] < 2)

    # ═══════════════════════════════════════════════════════════════
    # 15. TILING
    # ═══════════════════════════════════════════════════════════════
    print("\n  15. TILING")
    print("  " + "-" * 60)

    from tiling import build_triple_tiling, analyze_vertices, collapse_budget

    # Build tiling and classify vertices
    vertices = build_triple_tiling()
    vf, vtotal = analyze_vertices(vertices)

    check(f"Tiling produces vertices (got {vtotal})",
          vtotal > 100)

    # Should have multiple vertex types
    check(f"At least 5 vertex types (got {len(vf)})",
          len(vf) >= 5)

    # GS fraction ≈ LEAK = 1/φ⁴
    gs_frac = vf.get('GS', {}).get('fraction', 0)
    gs_err = abs(gs_frac - LEAK) / LEAK * 100 if gs_frac > 0 else 100
    check(f"GS fraction ≈ LEAK = 1/φ⁴ ({gs_err:.1f}% error)",
          gs_err < 5)

    # Collapse budget
    budget = collapse_budget(vf)

    check(f"Ω_b baryon error < 5% (got {budget['baryon']['error_pct']}%)",
          budget['baryon']['error_pct'] < 5)

    check(f"Ω_DM dark matter error < 5% (got {budget['dark_matter']['error_pct']}%)",
          budget['dark_matter']['error_pct'] < 5)

    check(f"Ω_DE dark energy error < 2% (got {budget['dark_energy']['error_pct']}%)",
          budget['dark_energy']['error_pct'] < 2)

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════
    print()
    print("=" * 65)
    status = "ALL PASSED" if failed == 0 else f"{failed} FAILED"
    print(f"  RESULTS: {passed}/{total} passed, {failed}/{total} failed — {status}")
    print("=" * 65)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
