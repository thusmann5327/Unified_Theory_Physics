"""
Absolute mass — Derive m_e from the AAH spectrum + attosecond bridge.

The electron mass requires NO empirical m_e or a_B input. The entire
derivation rests on:
  1. The axiom φ² = φ + 1  (gives all spectral constants)
  2. One measurement: t_hop = 1 attosecond  (gives a_lattice = c × t_hop)
  3. SI definitions: ℏ, c  (unit conversions, not measurements)

The bridge constant K = 24/φ³ converts the lattice spacing to the
Bohr radius: a_B = a_lattice / K.

Modules:
    bridge      — K constant, a_B derivation, m_e prediction
    propagate   — All particle masses from m_e + spectral ratios
"""

from .bridge import (
    K_BRIDGE, A_LATTICE, T_HOP,
    predict_bohr_radius, predict_electron_mass, predict_proton_mass,
)
from .propagate import mass_table
