"""
Lattice — Self-referential Fibonacci lattice properties.

VERIFIED:
  - Fibonacci shift identity: round(F(k)/φ⁴) = F(k-4) for all k ≥ 5
  - 5-sector partition: F(n-3)|F(n-4)|F(n-3)|F(n-4)|F(n-3) at all Fibonacci D
  - Z_max = 2F(9) + F(10) - F(5) = 118
  - D = 233 is unique: F(F(7)) = F(13), self-referential
  - Z/D limit: 1 - 2/φ³ - 1/φ⁸ = 0.5066

Modules:
    fibonacci    — Fibonacci arithmetic and shift identity
    sectors      — 5-sector eigenvalue partition
    z_max        — Z_max derivation and D=233 uniqueness
"""

from .fibonacci import fib, fib_index, shift_identity
from .sectors import sector_partition, sector_pattern_check
from .z_max import z_max_formula, d233_uniqueness, zd_limit
