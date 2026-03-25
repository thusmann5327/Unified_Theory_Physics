"""
angular.py — Angular momentum from Cantor layer ratios
========================================================

The four Cantor node layers map to the four orbital types via:

    2l+1 = round(R_layer(l) × F(7))

    σ₃ core   (R = 0.0728) × 13 → 1 → s-orbital  (l=0, 2 electrons)
    σ₂ inner  (R = 0.2350) × 13 → 3 → p-orbital  (l=1, 6 electrons)
    σ_wall    (R = 0.3972) × 13 → 5 → d-orbital  (l=2, 10 electrons)
    σ₄ outer  (R = 0.5594) × 13 → 7 → f-orbital  (l=3, 14 electrons)

F(7) = 13 is the bronze discriminant Δ₃ = 5 + 8, the same number
that proves three spatial dimensions via the Fibonacci chain.
D = F(F(7)) = F(13) = 233.
"""

from core.spectrum import R_MATTER, R_INNER, R_SHELL, R_OUTER

F7 = 13  # F(7) = Δ₃ = bronze discriminant

# Layer-to-l mapping
LAYER_RATIOS = {
    0: R_MATTER,  # σ₃ core   → s
    1: R_INNER,   # σ₂ inner  → p
    2: R_SHELL,   # σ_wall    → d
    3: R_OUTER,   # σ₄ outer  → f
}

LAYER_NAMES = {
    0: 'σ₃ core',
    1: 'σ₂ inner',
    2: 'σ_wall',
    3: 'σ₄ outer',
}

ORBITAL_NAMES = 'spdf'


def angular_modes(l):
    """Number of angular orientations (2l+1) from Cantor layer ratio.

    Returns dict with R_layer, product R×13, rounded value, and error.
    """
    R = LAYER_RATIOS[l]
    product = R * F7
    rounded = round(product)
    expected = 2 * l + 1
    error_pct = abs(product - expected) / expected * 100

    return {
        'l': l,
        'orbital': ORBITAL_NAMES[l],
        'layer': LAYER_NAMES[l],
        'R': float(R),
        'R_times_13': float(product),
        'predicted_2l1': rounded,
        'expected_2l1': expected,
        'match': rounded == expected,
        'error_pct': round(error_pct, 3),
    }


def subshell_capacity(l):
    """Subshell electron capacity = 2 × round(R_layer × 13).

    Returns the integer capacity: 2, 6, 10, or 14.
    """
    R = LAYER_RATIOS[l]
    return 2 * round(R * F7)


def all_layers():
    """Return angular mode info for all four layers."""
    return [angular_modes(l) for l in range(4)]


def verify_uniqueness(k_max=30):
    """Test which integer k values produce {1, 3, 5, 7} from the layer ratios.

    Returns list of (k, mean_error_pct) for valid k values.
    """
    valid = []
    targets = [1, 3, 5, 7]
    for k in range(1, k_max + 1):
        rounded = [round(LAYER_RATIOS[l] * k) for l in range(4)]
        if rounded == targets:
            products = [LAYER_RATIOS[l] * k for l in range(4)]
            mean_err = sum(abs(p - t) / t for p, t in zip(products, targets)) / 4 * 100
            valid.append((k, round(mean_err, 3)))
    return valid
