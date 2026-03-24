"""
Core framework — everything derives from φ² = φ + 1.

Modules:
    constants   — All framework constants from the single axiom
    hamiltonian — Build and diagonalize the AAH Hamiltonian
    spectrum    — Five-band partition and spectral ratios
"""

from .constants import *
from .hamiltonian import build_hamiltonian, diagonalize
from .spectrum import (
    extract_spectrum, R_MATTER, R_INNER, R_PHOTO, R_SHELL, R_OUTER,
    BASE, BOS, G1, GAPS_NORM
)
