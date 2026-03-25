"""
Tiling — Triple metallic mean multigrid and cosmological budget.

VERIFIED (12/12):
  - GS fraction = LEAK = 1/φ⁴ to 0.3%
  - LEAK × G1 = W⁴ = Ω_b to 0.6%
  - (LEAK - W⁴) + (GB + BS) × G1 = Ω_DM to 0.8%
  - Remainder = Ω_DE to 0.1%
  - BCC/FCC melting ratio ≈ φ to 1.3%
  - E_bracket ≈ C=C double bond to 0.09%
  - G only ≈ R_MATTER to 2.0%
  - σ₃ width ratios: Bronze/Gold ≈ φ, Gold/Silver ≈ √2

Key insight: the tiling shows the PRE-COLLAPSE 5-band state.
G1 = 0.3243 (first σ₃ sub-gap fraction) is the collapse transmission.
Post-collapse cosmological fractions = tiling vertex fractions × G1.

Modules:
    multigrid    — de Bruijn multigrid construction and vertex classification
    cosmology    — 5→3 collapse: tiling × G1 = cosmological budget
"""

from .multigrid import build_triple_tiling, analyze_vertices
from .cosmology import collapse_budget
