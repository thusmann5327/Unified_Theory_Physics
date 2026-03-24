"""
mixing.py — CKM mixing angles from spectral ratios
=====================================================

Cabibbo angle:
    sin(θ_C) ≈ 3/13 (Fibonacci fraction)      (2.28%)
    sin(θ_C) ≈ W/2                             (3.52%)

Weinberg angle (see electroweak.py for the primary test):
    sin²θ_W = σ₃ × σ_wall × F(6)              (0.047%)
    sin²θ_W ≈ 3/13                              (0.195%)

CKM matrix elements:
    |V_us| ≈ 3/13                               (2.43%)
    |V_cb| ≈ σ₃/φ                               (9.74%)
    |V_ub| ≈ W⁴ × σ₃                            (9.25%)
"""

import math

from core.constants import PHI, W, LEAK
from core.spectrum import R_MATTER


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL VALUES
# ═══════════════════════════════════════════════════════════════════

THETA_CABIBBO_DEG = 13.04           # Cabibbo angle (degrees)
SIN_CABIBBO = math.sin(math.radians(THETA_CABIBBO_DEG))  # 0.2256

# CKM magnitudes (PDG 2024)
V_US_OBS = 0.2253
V_CB_OBS = 0.0410
V_UB_OBS = 0.00382


# ═══════════════════════════════════════════════════════════════════
# CABIBBO ANGLE
# ═══════════════════════════════════════════════════════════════════

def cabibbo_angle():
    """
    Test Cabibbo angle sin(θ_C) against framework constants.

    Best matches:
        3/13 (Fibonacci fraction): 2.28%
        W/2: 3.52%
        σ₂ (inner wall = 0.235): 4.15%
        1/φ³: 4.63%
    """
    candidates = {
        '3/13 (Fibonacci)': 3.0 / 13.0,
        'W/2': W / 2,
        'σ₂ (inner wall)': 0.235,
        '1/φ³': 1.0 / PHI**3,
        'LEAK + σ₃': LEAK + R_MATTER,
    }

    results = {}
    for name, pred in candidates.items():
        err = abs(pred - SIN_CABIBBO) / SIN_CABIBBO * 100
        results[name] = {
            'predicted': pred,
            'observed': SIN_CABIBBO,
            'error_pct': err,
        }

    best = min(results, key=lambda k: results[k]['error_pct'])
    return {
        'candidates': results,
        'best_match': best,
        'best_error_pct': results[best]['error_pct'],
    }


# ═══════════════════════════════════════════════════════════════════
# CKM MATRIX ELEMENTS
# ═══════════════════════════════════════════════════════════════════

def ckm_elements():
    """
    Test CKM matrix elements against framework constant products.

    |V_us| ≈ 3/13    (2.43%) — Cabibbo element
    |V_cb| ≈ σ₃/φ    (9.74%) — second-generation mixing
    |V_ub| ≈ W⁴ × σ₃ (9.25%) — third-generation mixing
    """
    results = {}

    # V_us
    v_us_pred = 3.0 / 13.0
    results['V_us'] = {
        'predicted': v_us_pred,
        'observed': V_US_OBS,
        'error_pct': abs(v_us_pred - V_US_OBS) / V_US_OBS * 100,
        'formula': '3/13',
    }

    # V_cb
    v_cb_pred = R_MATTER / PHI
    results['V_cb'] = {
        'predicted': v_cb_pred,
        'observed': V_CB_OBS,
        'error_pct': abs(v_cb_pred - V_CB_OBS) / V_CB_OBS * 100,
        'formula': 'σ₃/φ',
    }

    # V_ub
    v_ub_pred = W**4 * R_MATTER
    results['V_ub'] = {
        'predicted': v_ub_pred,
        'observed': V_UB_OBS,
        'error_pct': abs(v_ub_pred - V_UB_OBS) / V_UB_OBS * 100,
        'formula': 'W⁴ × σ₃',
    }

    return results


# ═══════════════════════════════════════════════════════════════════
# FORMATTED REPORT
# ═══════════════════════════════════════════════════════════════════

def print_mixing_report():
    """Print mixing angle analysis."""
    cab = cabibbo_angle()
    ckm = ckm_elements()

    print(f"  Cabibbo angle: sin(θ_C) = {SIN_CABIBBO:.4f}")
    for name, r in cab['candidates'].items():
        stars = "★★" if r['error_pct'] < 3 else "★"
        print(f"    {name:>25s} = {r['predicted']:.4f}  ({r['error_pct']:.2f}%)  {stars}")

    print(f"\n  CKM matrix elements:")
    for name, r in ckm.items():
        print(f"    |{name}| = {r['predicted']:.5f}  "
              f"(obs: {r['observed']:.5f}, {r['error_pct']:.2f}%)  {r['formula']}")
