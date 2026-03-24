"""
hamiltonian.py — Build and diagonalize the Aubry-André-Harper Hamiltonian
==========================================================================

The AAH Hamiltonian at critical coupling (V = 2J) with irrational
frequency α = 1/φ on D = 233 = F(13) sites produces a Cantor spectrum
with 34 gaps and five-band Fibonacci architecture.

Three choices, all forced by the axiom:
    D = 233 = F(13) = F(F(7))   — self-referential Fibonacci seed
    α = 1/φ                      — maximally irrational frequency
    V = 2J                        — critical coupling (existence condition)
"""

import numpy as np

from .constants import PHI, D, ALPHA_AAH


def build_hamiltonian(D=D, alpha=ALPHA_AAH, V=2.0, J=1.0):
    """
    Build the AAH Hamiltonian matrix.

    H_ij = V·cos(2π·α·i)·δ_ij + J·(δ_{i,j+1} + δ_{i,j-1})

    Returns D×D real symmetric numpy array.
    """
    H = np.diag(V * np.cos(2 * np.pi * alpha * np.arange(D)))
    H += J * (np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1))
    return H


def diagonalize(H):
    """Diagonalize and return sorted eigenvalues."""
    return np.sort(np.linalg.eigvalsh(H))
