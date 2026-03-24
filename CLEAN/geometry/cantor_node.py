"""
cantor_node.py — The universal Cantor node at any scale
========================================================

Any structure at radius R has this architecture:
    r_core   = R × 0.0728     σ₃ — matter concentrates here
    r_inner  = R × 0.2350     σ₂ — inner confinement membrane
    r_photo  = R × 0.3672     cos(α) — decoupling/bonding surface
    r_shell  = R × 0.3972     wall centre — density/probability peak
    r_outer  = R × 0.5594     σ₄ — outer confinement membrane
    oblate   = √φ = 1.272     squash polar axis

Recursion: σ₃ contains 9 sub-gaps → 5 child nodes → same equation.
Depth 0→6 gives 19,531 nodes (universe → planets) in <100ms.
"""

import math

from core.constants import PHI, L_PLANCK, SQRT_PHI
from core.spectrum import R_MATTER, R_INNER, R_PHOTO, R_SHELL, R_OUTER


def cantor_node(R):
    """
    Compute the five-layer Cantor node at radius R.

    Returns dict with absolute positions and the oblate squash factor.
    """
    return {
        'R': R,
        'core': R * R_MATTER,      # σ₃ — matter
        'inner': R * R_INNER,      # σ₂ — confinement membrane
        'photo': R * R_PHOTO,      # cos(α) — decoupling
        'shell': R * R_SHELL,      # wall centre
        'outer': R * R_OUTER,      # σ₄ — entropy maximum
        'oblate': SQRT_PHI,        # polar squash factor
    }


def bracket_address(r_meters):
    """
    Compute bracket address: bz = round[log(R/l_P) / log(φ)].

    Bounded to [1, 294] (Planck length to Hubble radius).
    """
    if r_meters <= 0:
        return 1
    bz = round(math.log(r_meters / L_PLANCK) / math.log(PHI))
    return max(1, min(294, bz))


def zeckendorf(n):
    """
    Zeckendorf decomposition: unique sum of non-adjacent Fibonacci numbers.

    This is the Cantor lattice address — the binary encoding of which
    Fibonacci shells the structure occupies.
    """
    fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    result = []
    rem = int(round(abs(n)))
    for f in reversed(fibs):
        if f <= rem:
            result.append(f)
            rem -= f
        if rem == 0:
            break
    return result


# ═══════════════════════════════════════════════════════════════════
# SCALE TABLE — Cantor node at every scale
# ═══════════════════════════════════════════════════════════════════

SCALE_TABLE = [
    ("Observable universe", 4.5e26, 294),
    ("Galaxy cluster",      1e23,   269),
    ("Galaxy",              5e20,   256),
    ("Stellar system",      1e15,   243),
    ("Star",                7e8,    214),
    ("Brain",               0.28,   164),
    ("Microtubule",         12.5e-9, 128),
    ("Atom (H)",            1.3e-10, 119),
    ("Nucleus",             2e-15,   96),
    ("Proton",              8e-16,   94),
]


def print_scale_table():
    """Print Cantor node at representative scales."""
    print(f"  {'Scale':>22s}  {'R (m)':>10s}  {'bz':>4s}  {'Zeckendorf':>24s}")
    print("  " + "-" * 68)
    for name, R, bz in SCALE_TABLE:
        zeck = zeckendorf(bz)
        zeck_str = "+".join(str(z) for z in zeck)
        bz_calc = bracket_address(R)
        print(f"  {name:>22s}  {R:>10.1e}  {bz_calc:>4d}  {zeck_str:>24s}")
