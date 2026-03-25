"""
shape_operator.py — Bracket-dependent face weighting for emergent evolution
=============================================================================

The shape of matter at each scale EMERGES from anisotropic stiffness.
At nuclear brackets (94), s-face stiffness dominates → spherical.
At galaxy brackets (230), d-face stiffness dominates → disc.
At cosmic brackets (294), outer-face stiffness dominates → filaments.

The only input is the bracket number (94–294). Everything else derives
from φ²=φ+1.

Face types and their counts on an icosahedron:
    s-faces:  2  (polar caps — along rotation axis)
    p-faces:  6  (tropical belt — intermediate)
    d-faces: 10  (equatorial disc — in the disc plane)
    f-faces:  2  (outer polar — filament connectors)

Usage:
    from simulation.shape_operator import bracket_stiffness_weights
    weights = bracket_stiffness_weights(bracket=119)  # atom scale
    # Returns per-pair weight multipliers based on bond direction
"""

import numpy as np
import math

# ── Framework constants ──────────────────────────────────────────
PHI = (1 + 5**0.5) / 2
W = 0.4671338922
LEAK = 1.0 / PHI**4
R_C = 1.0 - 1.0 / PHI**4

# ── Bracket range ────────────────────────────────────────────────
BZ_NUCLEUS = 94
BZ_ATOM = 119
BZ_REFERENCE = 119       # zero-offset reference (atom scale)
BZ_MOLECULE = 160
BZ_SOLAR = 200
BZ_GALAXY = 230
BZ_CLUSTER = 260
BZ_UNIVERSE = 294
BZ_RANGE = 50.0           # normalization half-width

BRACKET_LABELS = {
    94:  'Nucleus',
    119: 'Atom',
    160: 'Molecule',
    200: 'Solar System',
    230: 'Galaxy',
    260: 'Cluster',
    294: 'Universe',
}


def face_weights(bracket):
    """Compute face-type stiffness multipliers for a given bracket.

    The b_offset measures distance from the atom scale (119).
    Negative offset → nuclear (s-faces dominate).
    Positive offset → cosmic (d-faces dominate).

    Returns dict with face-type weights:
        s: polar axis stiffness     (2 faces)
        p: tropical stiffness       (6 faces)
        d: equatorial disc stiffness (10 faces)
        f: outer filament stiffness  (2 faces)
    """
    b_offset = (bracket - BZ_REFERENCE) / BZ_RANGE

    # Exponents scaled to overcome the 10:2 face count asymmetry.
    # At b_offset = -0.5 (nuclear): s/d per face ≈ PHI^4.5 ≈ 9.0
    # → total s×2 / d×10 ≈ 1.8 → spherical
    # At b_offset = +2.2 (galaxy): d/s per face ≈ PHI^9.9 → very flat disc
    weights = {
        's': PHI ** (-5.0 * b_offset),    # s dominates at LOW brackets (nuclear)
        'p': PHI ** (-1.5 * b_offset),    # p intermediate
        'd': PHI ** (+4.0 * b_offset),    # d dominates at HIGH brackets (galaxy)
        'f': PHI ** (+1.0 * b_offset),    # f intermediate-high
    }

    return weights


def bond_face_character(dr_vectors, axis=None):
    """Classify bond directions into face characters.

    Each bond gets a weight that interpolates between s-face (along axis)
    and d-face (perpendicular to axis).

    Parameters
    ----------
    dr_vectors : (M, 3) array — bond direction vectors (not normalized)
    axis : (3,) array — rotation/symmetry axis. If None, uses z-axis.

    Returns
    -------
    face_chars : dict with arrays for each face type
        's_frac': (M,) — fraction of s-face character per bond
        'd_frac': (M,) — fraction of d-face character per bond
        'p_frac': (M,) — fraction of p-face character per bond
        'f_frac': (M,) — fraction of f-face character per bond
    """
    if axis is None:
        axis = np.array([0.0, 0.0, 1.0])
    axis = axis / (np.linalg.norm(axis) + 1e-15)

    # Normalize bond directions
    r = np.sqrt(np.sum(dr_vectors**2, axis=1, keepdims=True)) + 1e-15
    dr_hat = dr_vectors / r

    # cos(θ) between bond direction and axis
    cos_theta = np.abs(np.dot(dr_hat, axis))  # (M,) — abs for both poles

    # Face character from angle:
    #   cos_θ ≈ 1 → along axis → s-face (polar)
    #   cos_θ ≈ 0 → perpendicular → d-face (equatorial)
    #   intermediate → p-face or f-face
    sin_theta = np.sqrt(1.0 - cos_theta**2 + 1e-15)

    # Smooth partition into face types using powers of cos/sin
    # s: strongly axial (cos²θ)
    # d: strongly equatorial (sin²θ)
    # p: intermediate axial (2 cos θ sin θ = sin 2θ)
    # f: weakly equatorial (sin θ × cos θ / 2)
    s_frac = cos_theta**2
    d_frac = sin_theta**2
    # p and f share the cross-term
    cross = 2.0 * cos_theta * sin_theta
    p_frac = cross * 0.6   # 6/10 of cross goes to p
    f_frac = cross * 0.4   # 4/10 of cross goes to f

    # Normalize so fractions sum to ~1
    total = s_frac + d_frac + p_frac + f_frac + 1e-15
    s_frac /= total
    d_frac /= total
    p_frac /= total
    f_frac /= total

    return {
        's_frac': s_frac,
        'd_frac': d_frac,
        'p_frac': p_frac,
        'f_frac': f_frac,
    }


def bracket_stiffness_modifiers(bracket, dr_vectors, axis=None):
    """Compute per-bond stiffness multipliers from bracket + bond direction.

    This is the main entry point. For each bond, the stiffness is modified
    by the bracket-dependent face weights, weighted by the bond's face
    character (determined by its direction relative to the symmetry axis).

    Parameters
    ----------
    bracket : int — bracket level (94–294)
    dr_vectors : (M, 3) array — bond displacement vectors
    axis : (3,) array or None — symmetry axis

    Returns
    -------
    modifiers : (M,) array — multiply these with the base stiffness
    """
    fw = face_weights(bracket)
    fc = bond_face_character(dr_vectors, axis)

    # Weighted combination: each bond's modifier is the face-weighted sum
    modifiers = (
        fc['s_frac'] * fw['s'] +
        fc['d_frac'] * fw['d'] +
        fc['p_frac'] * fw['p'] +
        fc['f_frac'] * fw['f']
    )

    return modifiers


def detect_symmetry_axis(positions, types=None):
    """Detect the principal axis of a vertex distribution.

    Uses PCA on the BGS (matter) vertices if types provided,
    otherwise on all vertices. The axis with LEAST variance
    is the rotation axis (oblate → short axis = rotation axis).

    Returns the axis as a unit vector.
    """
    if types is not None:
        mask = np.array([t == 'BGS' for t in types])
        if mask.sum() > 10:
            pos = positions[mask]
        else:
            pos = positions
    else:
        pos = positions

    pos_centered = pos - pos.mean(axis=0)
    cov = np.cov(pos_centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Shortest axis = rotation axis (oblate squash)
    return eigenvectors[:, 0].copy()


def bracket_info(bracket):
    """Return human-readable info about a bracket level."""
    b_offset = (bracket - BZ_REFERENCE) / BZ_RANGE
    fw = face_weights(bracket)

    # Per-face weight ratio: d_weight / s_weight
    # This is the anisotropy that drives shape in the evolution
    disc_sphere = fw['d'] / (fw['s'] + 1e-15)

    # Find nearest label
    label = BRACKET_LABELS.get(bracket, '')
    if not label:
        nearest = min(BRACKET_LABELS.keys(), key=lambda k: abs(k - bracket))
        if abs(nearest - bracket) < 10:
            label = f'near {BRACKET_LABELS[nearest]}'

    return {
        'bracket': bracket,
        'b_offset': b_offset,
        'label': label,
        'face_weights': fw,
        'disc_sphere_ratio': disc_sphere,
        'expected_shape': (
            'spherical' if disc_sphere < 0.5 else
            'oblate' if disc_sphere < 2.0 else
            'disc' if disc_sphere < 10.0 else
            'filamentary'
        ),
    }


if __name__ == '__main__':
    print("\n  Shape Operator — Bracket-Dependent Face Weighting")
    print("  ═══════════════════════════════════════════════════")
    print(f"  Reference bracket: {BZ_REFERENCE} (Atom)")
    print(f"  Range: {BZ_NUCLEUS} (Nucleus) → {BZ_UNIVERSE} (Universe)\n")

    for bz in [94, 119, 160, 200, 230, 260, 294]:
        info = bracket_info(bz)
        fw = info['face_weights']
        print(f"  bz={bz:3d} ({info['label']:15s}): "
              f"s={fw['s']:.3f}  p={fw['p']:.3f}  "
              f"d={fw['d']:.3f}  f={fw['f']:.3f}  "
              f"disc/sphere={info['disc_sphere_ratio']:.2f}  "
              f"→ {info['expected_shape']}")
    print()
