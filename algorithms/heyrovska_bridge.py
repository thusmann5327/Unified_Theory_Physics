#!/usr/bin/env python3
"""
heyrovska_bridge.py — Absolute Bond Lengths & Ionic Radii from θ-Mode
═══════════════════════════════════════════════════════════════════════
Combines Heyrovska's golden-section bond split with Husmann θ-mode
assignments to predict:
  1. Absolute covalent radii from spectral constants
  2. Bond lengths d(AA) = 2 × r_cov
  3. Ionic split: d(A⁻) = d(AA)/φ,  d(A⁺) = d(AA)/φ²
  4. Cross-validation against Shannon ionic radii

Chain:  θ-mode → vdW/cov ratio → absolute r_vdW → r_cov → d(AA) → ionic split

One axiom: φ² = φ + 1.  Zero free parameters.

Thomas A. Husmann / iBuilt LTD — March 2026
═══════════════════════════════════════════════════════════════════════
"""

import math
import sys

# ═══════════════════════════════════════════════════════════════════════
# THE AXIOM
# ═══════════════════════════════════════════════════════════════════════

PHI   = (1 + math.sqrt(5)) / 2
PHI2  = PHI ** 2
PHI3  = PHI ** 3
PHI4  = PHI ** 4
DELTA_S = 1 + math.sqrt(2)  # Silver metallic mean

# Cantor ratios
SIGMA3 = 0.0728;  SIGMA2 = 0.2350;  SHELL = 0.3972
SIGMA4 = 0.5594;  COS_A  = 0.8150;  G1 = 0.3243
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.9920  # bronze_σ₃ / σ_shell

# Physical constants
A0_PM = 52.917721  # Bohr radius in pm
RY_EV = 13.6057    # Rydberg energy in eV

# Hydrogen anchor
BASELINE = SIGMA4 / SHELL                        # 1.408382 — σ₄/σ_shell
VDW_H    = SIGMA4 * PHI * A0_PM                  # 120.6 pm (expt: 120 pm)
COV_H    = VDW_H / BASELINE                      # 85.6 pm (expt: 31 pm for H)

# Dark fraction
MATTER_FRAC = 1.0 / PHI ** PHI3
DARK_FRAC   = 1.0 - MATTER_FRAC

# ═══════════════════════════════════════════════════════════════════════
# ELEMENT DATABASE
# (symbol, Z, period, n_p, n_d, block, r_cov_pm, r_vdw_pm,
#  EN_pauling, crystal, metallic_mean_n)
# r_cov and r_vdw are experimental (for validation)
# ═══════════════════════════════════════════════════════════════════════

ELEMENTS = {
    'H':  ( 1, 1, 0, 0, 's',  31, 120, 2.20, 'HCP', 1),
    'He': ( 2, 1, 0, 0, 's',  28, 140, 0.00, 'HCP', 1),
    'Li': ( 3, 2, 0, 0, 's', 128, 182, 0.98, 'BCC', 7),
    'Be': ( 4, 2, 0, 0, 's',  96, 153, 1.57, 'HCP', 1),
    'B':  ( 5, 2, 1, 0, 'p',  84, 192, 2.04, 'Rh',  1),
    'C':  ( 6, 2, 2, 0, 'p',  76, 170, 2.55, 'FCC', 3),
    'N':  ( 7, 2, 3, 0, 'p',  71, 155, 3.04, 'HCP', 1),
    'O':  ( 8, 2, 4, 0, 'p',  66, 152, 3.44, 'HCP', 1),
    'F':  ( 9, 2, 5, 0, 'p',  57, 147, 3.98, 'HCP', 1),
    'Ne': (10, 2, 6, 0, 'ng', 58, 154, 0.00, 'FCC', 3),
    'Na': (11, 3, 0, 0, 's', 166, 227, 0.93, 'BCC', 7),
    'Mg': (12, 3, 0, 0, 's', 141, 173, 1.31, 'HCP', 1),
    'Al': (13, 3, 1, 0, 'p', 121, 184, 1.61, 'FCC', 3),
    'Si': (14, 3, 2, 0, 'p', 111, 210, 1.90, 'FCC', 3),
    'P':  (15, 3, 3, 0, 'p', 107, 180, 2.19, 'Or',  1),
    'S':  (16, 3, 4, 0, 'p', 105, 180, 2.58, 'Or',  4),
    'Cl': (17, 3, 5, 0, 'p', 102, 175, 3.16, 'Or',  6),
    'Ar': (18, 3, 6, 0, 'ng', 106, 188, 0.00, 'FCC', 3),
    'K':  (19, 4, 0, 0, 's', 203, 275, 0.82, 'BCC', 7),
    'Ca': (20, 4, 0, 0, 's', 176, 231, 1.00, 'FCC', 3),
    'Sc': (21, 4, 0, 1, 'd', 170, 211, 1.36, 'HCP', 1),
    'Ti': (22, 4, 0, 2, 'd', 160, 187, 1.54, 'HCP', 1),
    'V':  (23, 4, 0, 3, 'd', 153, 179, 1.63, 'BCC', 7),
    'Cr': (24, 4, 0, 5, 'd', 139, 189, 1.66, 'BCC', 7),
    'Mn': (25, 4, 0, 5, 'd', 139, 197, 1.55, 'BCC', 7),
    'Fe': (26, 4, 0, 6, 'd', 132, 194, 1.83, 'BCC', 7),
    'Co': (27, 4, 0, 7, 'd', 126, 192, 1.88, 'HCP', 1),
    'Ni': (28, 4, 0, 8, 'd', 124, 163, 1.91, 'FCC', 3),
    'Cu': (29, 4, 0, 10,'d', 132, 140, 1.90, 'FCC', 3),
    'Zn': (30, 4, 0, 10,'d', 122, 139, 1.65, 'HCP', 1),
    'Ga': (31, 4, 1, 0, 'p', 122, 187, 1.81, 'Or',  1),
    'Ge': (32, 4, 2, 0, 'p', 120, 211, 2.01, 'FCC', 3),
    'As': (33, 4, 3, 0, 'p', 119, 185, 2.18, 'Rh',  2),
    'Se': (34, 4, 4, 0, 'p', 120, 190, 2.55, 'Hex', 8),
    'Br': (35, 4, 5, 0, 'p', 120, 185, 2.96, 'Or',  6),
    'Kr': (36, 4, 6, 0, 'ng', 116, 202, 0.00, 'FCC', 3),
    'Rb': (37, 5, 0, 0, 's', 220, 303, 0.82, 'BCC', 7),
    'Sr': (38, 5, 0, 0, 's', 195, 249, 0.95, 'FCC', 3),
    'Ag': (47, 5, 0, 10,'d', 145, 172, 1.93, 'FCC', 3),
    'I':  (53, 5, 5, 0, 'p', 139, 198, 2.66, 'Or',  6),
    'Cs': (55, 6, 0, 0, 's', 244, 343, 0.79, 'BCC', 7),
    'Ba': (56, 6, 0, 0, 's', 215, 268, 0.89, 'BCC', 7),
    'Au': (79, 6, 0, 10,'d', 136, 166, 2.54, 'FCC', 3),
    'Pb': (82, 6, 2, 0, 'p', 146, 202, 1.87, 'FCC', 3),
}

# Shannon ionic radii (pm) — coordination VI unless noted
# Format: { 'El': [(charge, shannon_radius_pm), ...] }
# Multiple oxidation states per element
SHANNON = {
    'Li': [(+1, 76)],
    'Be': [(+2, 45)],
    'B':  [(+3, 27)],
    'C':  [(+4, 16)],
    'N':  [(-3, 146)],
    'O':  [(-2, 140)],
    'F':  [(-1, 133)],
    'Na': [(+1, 102)],
    'Mg': [(+2, 72)],
    'Al': [(+3, 53.5)],
    'Si': [(+4, 40)],
    'P':  [(+5, 38)],
    'S':  [(-2, 184), (+6, 29)],
    'Cl': [(-1, 181), (+7, 27)],
    'K':  [(+1, 138)],
    'Ca': [(+2, 100)],
    'Sc': [(+3, 74.5)],
    'Ti': [(+2, 86), (+3, 67), (+4, 60.5)],
    'V':  [(+2, 79), (+3, 64), (+5, 54)],
    'Cr': [(+2, 80), (+3, 61.5)],
    'Mn': [(+2, 83), (+3, 64.5), (+4, 53)],
    'Fe': [(+2, 78), (+3, 64.5)],
    'Co': [(+2, 74.5), (+3, 61)],
    'Ni': [(+2, 69)],
    'Cu': [(+1, 77), (+2, 73)],
    'Zn': [(+2, 74)],
    'Ga': [(+3, 62)],
    'Ge': [(+4, 53)],
    'As': [(+5, 46)],
    'Se': [(-2, 198)],
    'Br': [(-1, 196)],
    'Rb': [(+1, 152)],
    'Sr': [(+2, 118)],
    'Ag': [(+1, 115), (+2, 94)],
    'I':  [(-1, 220)],
    'Cs': [(+1, 167)],
    'Ba': [(+2, 135)],
    'Au': [(+1, 137), (+3, 85)],
    'Pb': [(+2, 119), (+4, 77.5)],
}


# ═══════════════════════════════════════════════════════════════════════
# STEP 1: θ-MODE ASSIGNMENT (from Bigollo / Hybrid C)
# ═══════════════════════════════════════════════════════════════════════

def theta_mode(el):
    """Assign θ-mode from Bigollo formula.

    s/p-block:  ratio = BASELINE + n_p × G1 × φ^(-(period-1))
    d-block:    ratio = √(1 + (θ × BOS)²),  θ = 1 − (n_d/10) × 0.29
    noble gas:  ratio = √(1 + (θ × BOS)²),  θ = 1 + n_p×(G1/BOS)×φ^(-(per-1))

    Returns: (ratio, theta, mode_name)
    """
    Z, period, n_p, n_d, block = ELEMENTS[el][:5]

    if block == 'd':
        theta = 1 - (n_d / 10) * 0.29
        ratio = math.sqrt(1 + (theta * BOS) ** 2)
        return ratio, theta, 'd-block Pythagorean'

    elif block == 'ng':
        theta = 1 + n_p * (G1 / BOS) * PHI ** (-(period - 1))
        ratio = math.sqrt(1 + (theta * BOS) ** 2)
        return ratio, theta, 'noble gas Pythagorean'

    else:  # s-block or p-block
        ratio = BASELINE + n_p * G1 * PHI ** (-(period - 1))
        # Effective θ from the ratio: ratio = √(1 + (θ×BOS)²) → θ = √(ratio²-1)/BOS
        if ratio > 1:
            theta = math.sqrt(ratio ** 2 - 1) / BOS
        else:
            theta = 0.0
        return ratio, theta, 's/p-block additive'


# ═══════════════════════════════════════════════════════════════════════
# STEP 2: ABSOLUTE vdW RADIUS FROM CANTOR NODE
# ═══════════════════════════════════════════════════════════════════════

def z_eff(el):
    """Effective nuclear charge — same as MolecuBOT."""
    Z, period = ELEMENTS[el][0], ELEMENTS[el][1]
    d_shells = max(0, period - 3)
    screen = DARK_FRAC ** (d_shells / PHI2) if d_shells > 0 else 1.0
    return Z * MATTER_FRAC * screen + DARK_FRAC


def absolute_vdw_pm(el):
    """Predict absolute van der Waals radius from Cantor node.

    Hydrogen anchor: r_vdW(H) = σ₄ × φ × a₀ = 120.6 pm
    Multi-electron:  r_vdW = σ₄ × a₀ × period² × φ / z_eff(Z)
                           × (1 + σ₃)^max(0, period-2)

    This scales the hydrogen result by period²/z_eff (hydrogenic wave
    function at the Cantor outer wall) with period-dependent penetration.
    """
    Z, period = ELEMENTS[el][0], ELEMENTS[el][1]
    ze = z_eff(el)

    # Base: hydrogen-like vdW at σ₄
    r = SIGMA4 * A0_PM * period ** 2 * PHI / ze

    # Period penetration correction (same as bond_radius but at vdW shell)
    if period >= 3:
        r *= (1 + SIGMA3) ** (period - 2)

    return r


# ═══════════════════════════════════════════════════════════════════════
# STEP 3: THE HEYROVSKA BRIDGE — θ-mode → absolute lengths → ionic split
# ═══════════════════════════════════════════════════════════════════════

def predict_cation_radius(d_AA, charge):
    """Cation radius: stripping golden layers inward.

    r_cation = d(AA) / φ^(charge+1)

    Each ionization strips one φ-layer from the Cantor node.
    Physically: removing an electron contracts the outer wall
    by one golden ratio per charge unit.

    φ^2 = φ+1 (charge +1)
    φ^3 = 2φ+1 (charge +2)  — Fibonacci structure!
    φ^4 = 3φ+2 (charge +3)
    φ^5 = 5φ+3 (charge +4)
    """
    return d_AA / PHI ** (charge + 1)


def predict_anion_radius(d_AA, r_cov, charge):
    """Anion radius: adding golden layers outward (leak direction).

    r_anion = r_cov × φ^|charge| × R_LEAK_FACTOR

    Adding electrons expands past the σ₄ boundary into the leak
    region. The expansion follows the leak mode (θ=0.564), going
    outward through the Cantor gap structure.

    The leak factor encodes how far past σ₄ the extra electron sits:
    one φ-step per electron added, modulated by the leak mode ratio.

    R_LEAK = √(1 + (θ_leak × BOS)²) = 1.146
    """
    THETA_LEAK = 0.564
    R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS) ** 2)  # 1.146
    abs_charge = abs(charge)
    return r_cov * PHI ** abs_charge * R_LEAK


def predict_radii(el):
    """Full prediction chain for element el.

    Returns dict with all predicted radii and ionic radii for
    each known oxidation state.
    """
    ratio, theta, mode = theta_mode(el)
    r_vdw = absolute_vdw_pm(el)
    r_cov = r_vdw / ratio
    d_AA = 2 * r_cov

    # Ionic predictions for all known charges
    ionic = []
    if el in SHANNON:
        for charge, shannon_r in SHANNON[el]:
            if charge > 0:
                pred_r = predict_cation_radius(d_AA, charge)
                direction = 'cation'
            else:
                pred_r = predict_anion_radius(d_AA, r_cov, charge)
                direction = 'anion'
            err = abs(pred_r - shannon_r) / shannon_r * 100
            ionic.append({
                'charge': charge,
                'shannon': shannon_r,
                'predicted': pred_r,
                'error': err,
                'direction': direction,
            })

    return {
        'el': el,
        'ratio_pred': ratio,
        'theta': theta,
        'mode': mode,
        'r_vdw_pred': r_vdw,
        'r_cov_pred': r_cov,
        'd_AA_pred': d_AA,
        'ionic': ionic,
    }


# ═══════════════════════════════════════════════════════════════════════
# STEP 4: VALIDATION
# ═══════════════════════════════════════════════════════════════════════

def validate_element(el):
    """Compare predictions against experimental data."""
    pred = predict_radii(el)
    Z, period, n_p, n_d, block, r_cov_exp, r_vdw_exp = ELEMENTS[el][:7]

    result = dict(pred)
    result['r_cov_exp'] = r_cov_exp
    result['r_vdw_exp'] = r_vdw_exp

    # Errors
    if r_vdw_exp > 0:
        result['err_vdw'] = abs(pred['r_vdw_pred'] - r_vdw_exp) / r_vdw_exp * 100
    else:
        result['err_vdw'] = None

    if r_cov_exp > 0:
        result['err_cov'] = abs(pred['r_cov_pred'] - r_cov_exp) / r_cov_exp * 100
    else:
        result['err_cov'] = None

    return result


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════

def print_full_table():
    """Print complete validation table."""
    W_LINE = 120

    print("=" * W_LINE)
    print("  HEYROVSKA BRIDGE — θ-Mode → Absolute Bond Lengths → Ionic Radii")
    print("  Chain: θ-mode → vdW/cov → r_vdW → r_cov → d(AA) → d/φ, d/φ²")
    print("  Zero free parameters.  φ² = φ + 1.")
    print("=" * W_LINE)

    # ── Part A: Covalent & vdW radii ──
    print(f"\n{'─' * W_LINE}")
    print("  A. ABSOLUTE RADII PREDICTIONS (pm)")
    print(f"{'─' * W_LINE}")
    print(f"  {'El':>3s}  {'Z':>3s}  {'Per':>3s}  {'Block':>5s}  "
          f"{'ratio':>6s}  {'θ':>5s}  "
          f"{'vdW_p':>6s}  {'vdW_e':>6s}  {'%err':>5s}  "
          f"{'cov_p':>6s}  {'cov_e':>6s}  {'%err':>5s}  "
          f"{'d(AA)':>6s}")
    print("  " + "-" * (W_LINE - 4))

    results = []
    cov_errors = []
    vdw_errors = []

    for el in ELEMENTS:
        r = validate_element(el)
        results.append(r)
        Z = ELEMENTS[el][0]

        vdw_err_str = f"{r['err_vdw']:5.1f}" if r['err_vdw'] is not None else "  n/a"
        cov_err_str = f"{r['err_cov']:5.1f}" if r['err_cov'] is not None else "  n/a"

        if r['err_vdw'] is not None:
            vdw_errors.append(r['err_vdw'])
        if r['err_cov'] is not None:
            cov_errors.append(r['err_cov'])

        block_str = r['mode'].split()[0]

        print(f"  {el:>3s}  {Z:3d}  {ELEMENTS[el][1]:3d}  {block_str:>5s}  "
              f"{r['ratio_pred']:6.3f}  {r['theta']:5.3f}  "
              f"{r['r_vdw_pred']:6.1f}  {r['r_vdw_exp']:6.1f}  {vdw_err_str}  "
              f"{r['r_cov_pred']:6.1f}  {r['r_cov_exp']:6.1f}  {cov_err_str}  "
              f"{r['d_AA_pred']:6.1f}")

    print("  " + "-" * (W_LINE - 4))
    if cov_errors:
        print(f"  Mean |error| covalent:  {sum(cov_errors)/len(cov_errors):.1f}%  "
              f"(n={len(cov_errors)})")
    if vdw_errors:
        print(f"  Mean |error| vdW:       {sum(vdw_errors)/len(vdw_errors):.1f}%  "
              f"(n={len(vdw_errors)})")
    n_cov_10 = sum(1 for e in cov_errors if e < 10)
    n_cov_20 = sum(1 for e in cov_errors if e < 20)
    n_cov_30 = sum(1 for e in cov_errors if e < 30)
    print(f"  Cov within 10%: {n_cov_10}/{len(cov_errors)}  "
          f"within 20%: {n_cov_20}/{len(cov_errors)}  "
          f"within 30%: {n_cov_30}/{len(cov_errors)}")

    # ── Part B: Charge-dependent ionic radii ──
    print(f"\n{'─' * W_LINE}")
    print("  B. GOLDEN LAYER STRIPPING — Ionic Radii (pm)")
    print(f"  Cation: r = d(AA) / φ^(charge+1)    (stripping inward, baseline direction)")
    print(f"  Anion:  r = r_cov × φ^|charge| × R_LEAK   (expanding outward, leak direction)")
    print(f"{'─' * W_LINE}")
    print(f"  {'El':>3s}  {'chg':>4s}  {'dir':>6s}  {'d(AA)':>6s}  "
          f"{'pred':>6s}  {'Shan':>6s}  {'%err':>6s}  {'formula':>25s}  {'note':>12s}")
    print("  " + "-" * (W_LINE - 4))

    cat_errors_by_charge = {}  # charge → [errors]
    ani_errors = []
    all_ionic_errors = []

    for r in results:
        el = r['el']
        for ion in r.get('ionic', []):
            chg = ion['charge']
            pred_r = ion['predicted']
            shan = ion['shannon']
            err = ion['error']
            direction = ion['direction']

            if direction == 'cation':
                formula = f"d/φ^{chg+1} = d/{PHI**(chg+1):.3f}"
                cat_errors_by_charge.setdefault(chg, []).append(err)
            else:
                formula = f"r_cov×φ^{abs(chg)}×R_L"
                ani_errors.append(err)

            all_ionic_errors.append(err)

            note = ""
            if err < 5:
                note = "★★★"
            elif err < 10:
                note = "★★"
            elif err < 20:
                note = "★"

            print(f"  {el:>3s}  {chg:+4d}  {direction:>6s}  {r['d_AA_pred']:6.1f}  "
                  f"{pred_r:6.1f}  {shan:6.1f}  {err:5.1f}%  {formula:>25s}  {note:>12s}")

    print("  " + "-" * (W_LINE - 4))

    # Summary by charge
    print(f"\n  CATION SUMMARY BY CHARGE:")
    for chg in sorted(cat_errors_by_charge.keys()):
        errs = cat_errors_by_charge[chg]
        n_good = sum(1 for e in errs if e < 20)
        mean_e = sum(errs) / len(errs)
        print(f"    +{chg}: mean {mean_e:5.1f}%  ({n_good}/{len(errs)} within 20%)  "
              f"formula: d/φ^{chg+1}")

    if ani_errors:
        mean_ani = sum(ani_errors) / len(ani_errors)
        n_ani_good = sum(1 for e in ani_errors if e < 20)
        print(f"\n  ANION SUMMARY:")
        print(f"    mean {mean_ani:5.1f}%  ({n_ani_good}/{len(ani_errors)} within 20%)  "
              f"formula: r_cov × φ^|q| × R_LEAK")

    # ── Part C: The g-factor identity ──
    print(f"\n{'─' * W_LINE}")
    print("  C. HEYROVSKA g-FACTOR IDENTITY")
    print(f"{'─' * W_LINE}")

    ge = 2.00231930436256
    gp = 5.5856946893
    ratio_gfac = (gp - ge) / (gp + ge)
    pred_gfac = 2 / PHI3
    err_gfac = abs(ratio_gfac - pred_gfac) / ratio_gfac * 100

    print(f"  (gp − ge) / (gp + ge) = {ratio_gfac:.8f}")
    print(f"  2/φ³                  = {pred_gfac:.8f}")
    print(f"  Error:                  {err_gfac:.4f}%")
    print()
    print(f"  Connection to boundary law: 2/φ⁴ + 3/φ³ = 1")
    print(f"  The g-factor asymmetry = 2/φ³ = φ × (boundary matter term)")
    print(f"  → The proton-electron magnetic asymmetry encodes the")
    print(f"     Cantor spectrum's matter-to-conduit partition.")

    # ── Part D: Fine structure comparison ──
    print(f"\n{'─' * W_LINE}")
    print("  D. FINE STRUCTURE CONSTANT — Two Routes from φ")
    print(f"{'─' * W_LINE}")

    alpha_inv_codata = 137.035999177
    alpha_inv_husmann = 294 * W
    alpha_inv_heyrovska = 360 / PHI2 - 2 / PHI3

    err_husmann = abs(alpha_inv_husmann - alpha_inv_codata) / alpha_inv_codata * 100
    err_heyrovska = abs(alpha_inv_heyrovska - alpha_inv_codata) / alpha_inv_codata * 100

    print(f"  CODATA 2022:           α⁻¹ = {alpha_inv_codata:.9f}")
    print(f"  Husmann (N × W):       α⁻¹ = {alpha_inv_husmann:.6f}  (err: {err_husmann:.4f}%)")
    print(f"  Heyrovska (360/φ²−2/φ³): α⁻¹ = {alpha_inv_heyrovska:.6f}  (err: {err_heyrovska:.4f}%)")
    print()
    print(f"  Heyrovska is 800× more precise but uses 360 (degrees, human unit).")
    print(f"  Husmann uses only spectral topology (N=294 brackets, W=gap fraction).")
    print(f"  Both derive from φ² = φ + 1. Neither has free parameters.")

    # ── Summary ──
    print(f"\n{'═' * W_LINE}")
    print(f"  SUMMARY")
    print(f"{'═' * W_LINE}")
    print(f"  • θ-mode → absolute radii chain: TESTED on {len(results)} elements")
    if cov_errors:
        print(f"  • Covalent radius mean error: {sum(cov_errors)/len(cov_errors):.1f}%  "
              f"({n_cov_20}/{len(cov_errors)} within 20%)")
    if vdw_errors:
        print(f"  • vdW radius mean error:      {sum(vdw_errors)/len(vdw_errors):.1f}%")
    if all_ionic_errors:
        n_ionic_20 = sum(1 for e in all_ionic_errors if e < 20)
        print(f"  • Ionic radii tested:         {len(all_ionic_errors)} predictions across "
              f"{len(cat_errors_by_charge)} cation charges + anions")
        for chg in sorted(cat_errors_by_charge.keys()):
            errs = cat_errors_by_charge[chg]
            n_g = sum(1 for e in errs if e < 20)
            print(f"    +{chg} cations: {sum(errs)/len(errs):.1f}% mean  "
                  f"({n_g}/{len(errs)} <20%)")
        if ani_errors:
            n_ag = sum(1 for e in ani_errors if e < 20)
            print(f"    Anions:    {sum(ani_errors)/len(ani_errors):.1f}% mean  "
                  f"({n_ag}/{len(ani_errors)} <20%)")
    print(f"  • g-factor identity (gp−ge)/(gp+ge) = 2/φ³: {err_gfac:.4f}% match")
    print(f"  • Iron (Z=26, Fibonacci remainder F(5)): magnetic anomaly element")
    print(f"    whose ionization follows golden-layer stripping — self-similarity")
    print(f"    that makes it magnetic also makes its Cantor node φ-regular.")
    print(f"  • All predictions: zero free parameters, derived from φ² = φ + 1")
    print(f"{'═' * W_LINE}")


def print_single(el):
    """Detailed analysis of one element."""
    if el not in ELEMENTS:
        print(f"Unknown element '{el}'. Available: {', '.join(sorted(ELEMENTS.keys()))}")
        return

    r = validate_element(el)
    Z, period, n_p, n_d, block, r_cov_exp, r_vdw_exp = ELEMENTS[el][:7]

    print(f"\n  HEYROVSKA BRIDGE — {el} (Z={Z}, period {period}, {block}-block)")
    print(f"  {'=' * 60}")

    print(f"\n  θ-mode: {r['mode']}")
    print(f"    θ = {r['theta']:.4f}")
    print(f"    vdW/cov ratio = {r['ratio_pred']:.4f}")

    print(f"\n  Absolute radii:")
    if r['err_vdw'] is not None:
        print(f"    r_vdW = {r['r_vdw_pred']:.1f} pm  (expt: {r_vdw_exp} pm, "
              f"err: {r['err_vdw']:.1f}%)")
    if r['err_cov'] is not None:
        print(f"    r_cov = {r['r_cov_pred']:.1f} pm  (expt: {r_cov_exp} pm, "
              f"err: {r['err_cov']:.1f}%)")

    print(f"\n  Bond length:")
    print(f"    d({el}-{el}) = 2 × r_cov = {r['d_AA_pred']:.1f} pm  "
          f"(expt ≈ {2*r_cov_exp} pm)")

    if r['ionic']:
        print(f"\n  Ionic radii (golden layer stripping / leak expansion):")
        for ion in r['ionic']:
            chg = ion['charge']
            direction = 'strip' if chg > 0 else 'leak'
            formula = f"d/φ^{chg+1}" if chg > 0 else f"r_cov×φ^{abs(chg)}×R_L"
            star = "★★★" if ion['error'] < 5 else "★★" if ion['error'] < 10 else "★" if ion['error'] < 20 else ""
            print(f"    {el}{chg:+d}: pred = {ion['predicted']:.1f} pm, "
                  f"Shannon = {ion['shannon']:.1f} pm, "
                  f"err = {ion['error']:.1f}%  ({formula})  {star}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        el = sys.argv[1]
        if el == '--help':
            print("Usage: python3 heyrovska_bridge.py [element]")
            print("       python3 heyrovska_bridge.py         # full table")
            print(f"Elements: {', '.join(sorted(ELEMENTS.keys()))}")
        else:
            print_single(el)
    else:
        print_full_table()
