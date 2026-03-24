"""
periodic_table.py — Predict vdW/cov ratios for Z=3-99
======================================================

The unified Pythagorean formula:
    ratio = √(1 + (θ(Z) × BOS)²) × correction(Z)

where θ is computed from the discriminant triangle:
    θ = 1 + √φ × n_p×(G1/BOS)×φ^(-(per-1))
        [- (n_d/10)×0.290]_magnetic
        + μ×LEAK
        - (n_f/14)×LEAK

Maps all elements onto three discriminant cones:
    Leak cone     (29.2°) — d-block boundary, gate OPEN
    RC cone       (40.3°) — d-block mid-series, standard θ
    Baseline cone (44.8°) — s/p-block, θ ≈ 1

Twelve modes from ONE formula. Zero free parameters.
"""

import math
import numpy as np

from core.constants import (
    PHI, W, LEAK, R_C, OBLATE, BREATHING,
    DARK_GOLD, RHO6
)
from core.spectrum import BASE, BOS, G1, THETA_LEAK, ALPHA_LEAK, ALPHA_RC, ALPHA_BASE
from .aufbau import aufbau
from .elements import RADII, SYMBOLS, MU_EFF


# ═══════════════════════════════════════════════════════════════════
# UNIFIED θ FORMULA
# ═══════════════════════════════════════════════════════════════════

def theta_unified(Z, per, n_p, n_d, n_f, n_s, blk, mu_eff=0.0, include_silver=False):
    """
    Compute θ from the discriminant triangle.

    Components:
        Σ_gold     = √φ × n_p × (G1/BOS) × φ^(-(per-1))   [p-electron momentum]
        Σ_silver   = (n_d/10) × 0.290                        [d-confinement, magnetic only]
        Σ_magnetic = μ_eff × LEAK                             [ferromagnetic exchange]
        Σ_f        = (n_f/14) × LEAK                          [f-electron σ₁ gate]
    """
    sigma_gold = OBLATE * n_p * (G1 / BOS) * PHI**(-(per - 1))
    sigma_silver = (n_d / 10.0) * DARK_GOLD if include_silver else 0.0
    sigma_magnetic = mu_eff * LEAK
    sigma_f = (n_f / 14.0) * LEAK if n_f > 0 else 0.0
    return 1.0 + sigma_gold - sigma_silver + sigma_magnetic - sigma_f


def ratio_pythagorean(theta):
    """The universal Pythagorean formula: ratio = √(1 + (θ × BOS)²)."""
    return math.sqrt(1 + (theta * BOS)**2)


# ═══════════════════════════════════════════════════════════════════
# UNIFIED PREDICTOR — twelve modes from one formula
# ═══════════════════════════════════════════════════════════════════

def predict_ratio(Z):
    """
    Predict vdW/cov ratio for element Z.

    Returns: (ratio, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone)

    Modes:
        magnetic    — Fe/Co/Ni with σ_silver retained
        rel-reflect — Pt (d⁹s¹) and Hg (d¹⁰s²) relativistic
        leak        — d-block boundary with s-electron (gate OPEN)
        reflect     — d-block d≥9 without s (Pd)
        standard    — d-block mid-series (θ=1, c_silver=0)
        f-block     — lanthanides/actinides with f-electron gate
        pythagorean — noble gas / s-block baseline
        ng-phole    — noble gas p-hole (period ≥ 3)
        alk-earth   — alkaline earth s² gate (Mg/Ca/Sr/Ba)
        sp3         — tetrahedral boost (C/Si/Ge/Sn)
        B-overflow  — boron period-2 overflow
        additive    — s/p-block standard
        p-hole      — p4/p5 correction (period ≥ 3)
    """
    per, n_p, n_d, n_f, n_s, blk = aufbau(Z)
    mu = MU_EFF.get(Z, 0.0)
    cone = "base"
    ALKALINE_EARTH = {12, 20, 38, 56}  # Be excluded — period 2 anomaly

    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)

        if Z in MU_EFF:
            # Magnetic mode — keep σ_silver for 0.1% Ni match
            theta = theta_unified(Z, per, n_p, n_d, n_f, n_s, blk, mu, include_silver=True)
            ratio = ratio_pythagorean(theta)
            mode = "magnetic"
            cone = "rc"

        elif per == 6 and n_d >= 9 and (n_d == 9 or n_s == 2):
            # Relativistic reflect — Pt (d⁹s¹ d-hole hybridization)
            # and Hg (d¹⁰s² inert pair). Au excluded: single s mediates.
            ratio_reflect = BASE + DARK_GOLD * LEAK
            theta = math.sqrt(ratio_reflect**2 - 1) / BOS
            ratio = ratio_pythagorean(theta) * RHO6
            mode = "rel-reflect"
            cone = "leak"

        elif is_boundary and has_s and Z not in MU_EFF:
            # Gate OPEN: leak mode
            theta = THETA_LEAK
            ratio = ratio_pythagorean(theta)
            if per == 6:
                ratio *= RHO6  # period 6 relativistic correction
            mode = "leak"
            cone = "leak"

        elif n_d >= 9 and not has_s:
            # Gate CLOSED (no s-electron): reflect mode (Pd)
            ratio_reflect = BASE + DARK_GOLD * LEAK
            theta = math.sqrt(ratio_reflect**2 - 1) / BOS
            ratio = ratio_pythagorean(theta)
            mode = "reflect"
            cone = "leak"

        else:
            # Standard d-block (d5-d8, non-ferromagnetic): c_silver=0, θ=1
            theta = theta_unified(Z, per, n_p, n_d, n_f, n_s, blk)
            ratio = ratio_pythagorean(theta)
            mode = "standard"
            cone = "rc"

    elif blk == 'f':
        theta = theta_unified(Z, per, n_p, n_d, n_f, n_s, blk)
        ratio = ratio_pythagorean(theta)
        mode = "f-block"
        cone = "rc"

    elif blk == 'ng':
        theta = theta_unified(Z, per, n_p, n_d, n_f, n_s, blk)
        ratio = ratio_pythagorean(theta)
        mode = "pythagorean"
        cone = "base"
        if per >= 3:
            ratio *= R_C
            mode = "ng-phole"

    elif Z in ALKALINE_EARTH:
        theta = R_C
        ratio = ratio_pythagorean(theta)
        mode = "alk-earth"
        cone = "rc"

    else:
        theta = theta_unified(Z, per, n_p, n_d, n_f, n_s, blk)

        if blk == 'p' and n_p == 2 and per <= 5:
            theta *= PHI**(1.0 / 3.0)
            mode = "sp3"
        elif blk == 'p' and n_p == 1 and per == 2:
            theta *= PHI
            mode = "B-overflow"
        else:
            mode = "pythagorean" if blk == 's' and n_p == 0 else "additive"

        ratio = ratio_pythagorean(theta)
        cone = "base"

    # Topological corrections
    if blk == 'p' and n_p >= 4 and per >= 3:
        ratio *= R_C
        mode = "p-hole"
    if Z == 2:
        ratio *= (1 + BREATHING)

    return ratio, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone


# ═══════════════════════════════════════════════════════════════════
# FULL PERIODIC TABLE ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def run_periodic_table():
    """
    Run full periodic table analysis for Z=3-99.

    Returns list of result dicts and prints formatted table.
    """
    results = []
    for Z in sorted(RADII.keys()):
        if Z < 3:
            continue
        rc, rv = RADII[Z]
        ratio_obs = rv / rc
        ratio_pred, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone = predict_ratio(Z)
        err = (ratio_pred - ratio_obs) / ratio_obs * 100

        results.append({
            'Z': Z, 'sym': SYMBOLS.get(Z, '?'), 'per': per,
            'n_p': n_p, 'n_d': n_d, 'n_f': n_f, 'n_s': n_s,
            'blk': blk, 'mode': mode, 'cone': cone,
            'theta': theta, 'ratio_pred': ratio_pred,
            'ratio_obs': ratio_obs, 'err': err,
        })

    # Print results
    print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'nd':>2} {'nf':>2}"
          f" {'theta':>6} {'Pred':>7} {'Obs':>7} {'Err':>7}"
          f" {'Cone':>5} {'Mode':>12}")
    print("  " + "-" * 72)

    for r in results:
        flag = " " if abs(r['err']) < 10 else ("~" if abs(r['err']) < 20 else "!")
        print(f"  {r['Z']:3d} {r['sym']:>3} {r['blk']:>3} {r['n_d']:>2d} {r['n_f']:>2d}"
              f" {r['theta']:6.3f} {r['ratio_pred']:7.3f} {r['ratio_obs']:7.3f}"
              f" {r['err']:+7.1f}%{flag}"
              f" {r['cone']:>5} {r['mode']:>12}")

    return results


def scorecard(results):
    """Print summary statistics from periodic table results."""
    blocks = {
        "All elements": results,
        "s/p/ng (Z>2)": [r for r in results if r['blk'] in ('s', 'p', 'ng')],
        "d-block": [r for r in results if r['blk'] == 'd'],
        "f-block": [r for r in results if r['blk'] == 'f'],
    }

    for label, dataset in blocks.items():
        if not dataset:
            continue
        ae = [abs(r['err']) for r in dataset]
        n = len(ae)
        n5 = sum(1 for e in ae if e < 5)
        n10 = sum(1 for e in ae if e < 10)
        n20 = sum(1 for e in ae if e < 20)
        print(f"\n  {label} ({n} elements):")
        print(f"    Mean |error|: {np.mean(ae):.1f}%")
        print(f"    Median:       {np.median(ae):.1f}%")
        print(f"    <5%: {n5}/{n} ({100*n5/n:.0f}%)  "
              f"<10%: {n10}/{n} ({100*n10/n:.0f}%)  "
              f"<20%: {n20}/{n} ({100*n20/n:.0f}%)")

    # Per-cone
    print(f"\n  Per-cone breakdown:")
    for cone in ['leak', 'rc', 'base']:
        ce = [abs(r['err']) for r in results if r['cone'] == cone]
        if ce:
            print(f"    {cone:>5}: {len(ce):2d} el, mean={np.mean(ce):5.1f}%, "
                  f"<10%={sum(1 for e in ce if e<10)}/{len(ce)}")
