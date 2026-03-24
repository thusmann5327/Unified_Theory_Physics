"""
discriminant.py — The discriminant Pythagorean triangle
========================================================

The metallic mean x² = nx + 1 has discriminant Δ_n = n² + 4.
For n = 1,2,3: Δ₁ = 5, Δ₂ = 8, Δ₃ = 13 — all Fibonacci.

The Fibonacci recurrence 5 + 8 = 13 holds (the axiom φ²=φ+1 again).
At n = 4: Δ₄ = 20 ≠ F(8) = 21. Chain breaks → 3 dimensions only.

The Pythagorean relation (√5)² + (√8)² = (√13)² maps to:
    E² = p²c² + m²c⁴    (Dirac equation)
    13 = 5 + 8            (discriminant triangle)

Three layers (concentric, silver innermost):
    Silver (Δ₂=8): innermost, mass, confinement, 83% dark
    Gold   (Δ₁=5): middle, momentum, propagation, 29% dark
    Bronze (Δ₃=13): outermost, observable, surface, 61% dark

Bronze is EMERGENT — the Pythagorean combination of gold + silver.
"""

import math

from core.constants import PHI, metallic_mean, SILVER_S3, GOLD_S3, BRONZE_S3


def discriminant_triangle():
    """
    Verify the discriminant Pythagorean triple and Fibonacci chain.

    Returns dict with verification results.
    """
    D1 = 1**2 + 4  # = 5
    D2 = 2**2 + 4  # = 8
    D3 = 3**2 + 4  # = 13

    # Pythagorean: (√5)² + (√8)² = (√13)²
    pythagorean = abs(D1 + D2 - D3)

    # Fibonacci chain: 5 + 8 = 13
    chain_holds = (D1 + D2 == D3)

    # Cos of the gold angle ≈ 1/φ
    cos_gold = math.sqrt(5) / math.sqrt(13)
    phi_inv = 1 / PHI

    # Three layers with dark fractions
    total_s3 = SILVER_S3 + GOLD_S3 + BRONZE_S3

    return {
        'discriminants': {'gold': D1, 'silver': D2, 'bronze': D3},
        'pythagorean_exact': pythagorean == 0,
        'fibonacci_chain': chain_holds,
        'cos_gold_angle': cos_gold,
        'one_over_phi': phi_inv,
        'angle_match_pct': abs(cos_gold - phi_inv) / phi_inv * 100,
        'layers': {
            'silver': {'discriminant': D2, 'sigma3': SILVER_S3,
                       'fraction': SILVER_S3 / total_s3,
                       'dark_pct': 83, 'role': 'mass/confinement'},
            'gold':   {'discriminant': D1, 'sigma3': GOLD_S3,
                       'fraction': GOLD_S3 / total_s3,
                       'dark_pct': 29, 'role': 'momentum/propagation'},
            'bronze': {'discriminant': D3, 'sigma3': BRONZE_S3,
                       'fraction': BRONZE_S3 / total_s3,
                       'dark_pct': 61, 'role': 'observable/surface'},
        },
        'silver_gold_boundary': SILVER_S3 / total_s3,  # 0.214 ≈ solar core
    }


def three_wave_frequencies():
    """
    The three metallic mean frequencies for the 3D vacuum Hamiltonian.

    Each axis uses a different metallic mean at V = 2J:
        x-axis: gold   α₁ = 1/φ          (depth/self-similarity)
        y-axis: silver  α₂ = 1/(1+√2)    (breadth/orthogonality)
        z-axis: bronze  α₃ = 1/δ₃        (closure/triangulation)

    Bronze is DETERMINED by gold + silver through 5 + 8 = 13.
    """
    alpha1 = 1.0 / metallic_mean(1)
    alpha2 = 1.0 / metallic_mean(2)
    alpha3 = 1.0 / metallic_mean(3)

    return {
        'gold':   {'n': 1, 'alpha': alpha1, 'role': 'depth/self-similarity'},
        'silver': {'n': 2, 'alpha': alpha2, 'role': 'breadth/orthogonality'},
        'bronze': {'n': 3, 'alpha': alpha3, 'role': 'closure/triangulation'},
    }


def schrödinger_interpolation(v_over_c):
    """
    Effective discriminant: Δ_eff(v) = 8 + 5(v/c)²

    Interpolates continuously from silver (rest mass) to bronze (relativistic).
    Schrödinger = tangent line to the discriminant triangle at the silver vertex.
    """
    return 8 + 5 * v_over_c**2
