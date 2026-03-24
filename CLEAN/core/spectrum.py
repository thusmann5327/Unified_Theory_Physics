"""
spectrum.py — Five-band partition and spectral ratios
======================================================

Diagonalizes the AAH Hamiltonian and extracts:
  - Five Cantor node ratios (R_MATTER through R_OUTER)
  - σ₃ sub-gap hierarchy (G1, G2, ...)
  - Composite ratios (BASE, BOS, DARK_GOLD)
  - Three cone angles

These ratios appear at every scale from protons to the observable universe.
"""

import numpy as np
import math

from .constants import PHI, LEAK, R_C, OBLATE, BRONZE_S3, DARK_GOLD
from .hamiltonian import build_hamiltonian, diagonalize


def extract_spectrum(D=233):
    """
    Diagonalize the AAH Hamiltonian and extract all spectral ratios.

    Returns dict with:
        eigs        — sorted eigenvalues (233 values)
        E_range     — full bandwidth
        n_gaps      — total gap count (34 = F(9))
        R_MATTER    — σ₃ core position (0.0728)
        R_INNER     — σ₂ inner wall (0.2350)
        R_PHOTO     — cos(α) decoupling surface (0.3672)
        R_SHELL     — wall centre (0.3972)
        R_OUTER     — σ₄ outer wall (0.5594)
        G1          — first σ₃ sub-gap fraction (0.3243)
        gaps_norm   — all σ₃ sub-gap fractions
        BASE        — σ₄/σ_shell = 1.408382
        BOS         — bronze_σ₃/σ_shell = 0.99202
    """
    H = build_hamiltonian(D)
    eigs = diagonalize(H)
    E_range = eigs[-1] - eigs[0]
    half = E_range / 2

    # Find all gaps
    diffs = np.diff(eigs)
    med = np.median(diffs)
    all_gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
    ranked = sorted(all_gaps, key=lambda g: g[1], reverse=True)

    # Two dominant gaps (width > 1.0)
    dominant = [g for g in ranked if g[1] > 1.0]
    wL = min(dominant, key=lambda g: eigs[g[0]] + eigs[g[0] + 1])

    # Five spectral ratios
    R_MATTER = abs(eigs[wL[0] + 1]) / half
    R_INNER = abs(eigs[wL[0]] + eigs[wL[0] + 1]) / (2 * E_range)
    R_SHELL = (abs(eigs[wL[0]]) + abs(eigs[wL[0] + 1])) / (2 * half)
    R_OUTER = R_SHELL + wL[1] / (2 * E_range)
    cos_alpha = math.cos(1.0 / PHI)
    R_PHOTO = R_INNER + cos_alpha * (R_SHELL - R_INNER)

    # σ₃ sub-gap hierarchy
    abs_eigs = np.abs(eigs)
    centre_idx = np.sort(np.argsort(abs_eigs)[:55])
    centre_eigs = eigs[centre_idx]
    s3_width = centre_eigs[-1] - centre_eigs[0]
    s3_diffs = np.diff(centre_eigs)
    s3_med = np.median(s3_diffs)
    s3_gaps = sorted(
        [s3_diffs[i] for i in range(len(s3_diffs)) if s3_diffs[i] > 4 * s3_med],
        reverse=True
    )
    G1 = s3_gaps[0] / s3_width if s3_gaps else 0.3243
    gaps_norm = [g / s3_width for g in s3_gaps]

    # Composite ratios
    BASE = R_OUTER / R_SHELL
    BOS = BRONZE_S3 / R_SHELL

    return {
        'eigs': eigs,
        'E_range': E_range,
        'n_gaps': len(all_gaps),
        'R_MATTER': R_MATTER,
        'R_INNER': R_INNER,
        'R_PHOTO': R_PHOTO,
        'R_SHELL': R_SHELL,
        'R_OUTER': R_OUTER,
        'G1': G1,
        'gaps_norm': gaps_norm,
        'BASE': BASE,
        'BOS': BOS,
        's3_width': s3_width,
    }


# ═══════════════════════════════════════════════════════════════════
# Module-level extraction (run once on import)
# ═══════════════════════════════════════════════════════════════════

_SPEC = extract_spectrum()

R_MATTER = _SPEC['R_MATTER']
R_INNER  = _SPEC['R_INNER']
R_PHOTO  = _SPEC['R_PHOTO']
R_SHELL  = _SPEC['R_SHELL']
R_OUTER  = _SPEC['R_OUTER']
G1       = _SPEC['G1']
GAPS_NORM = _SPEC['gaps_norm']
BASE     = _SPEC['BASE']
BOS      = _SPEC['BOS']

# Three cone angles
THETA_LEAK = math.sqrt((1 + LEAK)**2 - 1) / BOS
THETA_RC   = R_C
THETA_BASE = 1.0

ALPHA_LEAK = math.degrees(math.atan(THETA_LEAK * BOS))   # ~29.2°
ALPHA_RC   = math.degrees(math.atan(THETA_RC * BOS))     # ~40.3°
ALPHA_BASE = math.degrees(math.atan(THETA_BASE * BOS))   # ~44.8°
