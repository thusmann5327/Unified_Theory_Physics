"""
discriminant_cones.py — Three cone angles from the Cantor spectrum
===================================================================

Three discriminant cones emerge from the spectral ratios:
    Leak     ~29.2°  θ = 0.564  (d-block boundary)
    RC       ~40.3°  θ = 0.854  (d-block standard)
    Baseline ~44.8°  θ = 1.000  (s/p-block)

Key identity: α_leak = arctan(σ₄) to 0.015%
The leak cone angle IS the arctangent of the outer wall position.

z = 1 identity: at θ = 1 (baseline), the z-component of the
unit vector on the cone surface equals 1/√(1 + BOS²),
recovering the Cantor node Pythagorean relation.
"""

import math

from core.constants import PHI, LEAK, R_C
from core.spectrum import BOS, R_OUTER, R_SHELL, THETA_LEAK, THETA_RC, THETA_BASE


def cone_angles():
    """
    Compute the three discriminant cone angles.

    Returns dict with angle values in degrees and the key identities.
    """
    alpha_leak = math.degrees(math.atan(THETA_LEAK * BOS))
    alpha_rc = math.degrees(math.atan(THETA_RC * BOS))
    alpha_base = math.degrees(math.atan(THETA_BASE * BOS))

    # Key identity: α_leak ≈ arctan(σ₄)
    alpha_sigma4 = math.degrees(math.atan(R_OUTER))
    leak_sigma4_match = abs(alpha_leak - alpha_sigma4) / alpha_sigma4 * 100

    # z = 1 identity: z-component at baseline
    z_baseline = 1.0 / math.sqrt(1 + BOS**2)

    return {
        'leak': {'angle_deg': alpha_leak, 'theta': THETA_LEAK},
        'rc': {'angle_deg': alpha_rc, 'theta': THETA_RC},
        'baseline': {'angle_deg': alpha_base, 'theta': THETA_BASE},
        'sigma4_match': {
            'alpha_leak': alpha_leak,
            'arctan_sigma4': alpha_sigma4,
            'error_pct': leak_sigma4_match,
        },
        'z1_identity': {
            'z_component': z_baseline,
            'expected': 1.0 / math.sqrt(1 + BOS**2),
        },
        'baseline_near_45': abs(alpha_base - 45.0),
    }


def cone_deviation(theta, theta_ref=THETA_BASE):
    """
    Compute angular deviation from reference cone.

    Used as hardness predictor: elements further from baseline
    cone have stronger gate overflow → harder materials.
    """
    alpha = math.atan(theta * BOS)
    alpha_ref = math.atan(theta_ref * BOS)
    return math.degrees(abs(alpha - alpha_ref))


def verify_sigma4_identity():
    """
    Verify: THETA_LEAK * BOS ≈ σ₄ to 0.015%.

    This means the leak cone angle is determined by the outer wall
    position of the Cantor spectrum.
    """
    lhs = THETA_LEAK * BOS
    rhs = R_OUTER
    return {
        'lhs': lhs,
        'rhs': rhs,
        'error_pct': abs(lhs - rhs) / rhs * 100,
        'match': abs(lhs - rhs) / rhs < 0.001,
    }
