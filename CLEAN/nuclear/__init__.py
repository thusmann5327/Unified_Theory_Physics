"""
Nuclear physics — Shell structure from the Cantor node.

STATUS: UNDER DEVELOPMENT

The same spectral ratios that determine atomic subshell capacities
(R_layer × 13) connect to nuclear shell closures. Verified results:

  - HO shell capacities = 2 × triangular numbers (proven)
  - Spin-orbit detachment starts at d-capacity = 10 = 2×round(R_SHELL×13)
  - Detaching sublevel capacities: 10, 12, 14 (arithmetic, step 2)
  - Nuclear-to-atomic bracket gap ≈ F(8) = 21
  - 2 and 8 are exact Fibonacci magic numbers
  - 126 has most compact Zeckendorf (island of stability prediction)

Open questions (see TODO below):
  - Clean single-formula correction factor for magic/F(k) ratios
  - Triangular→odd number transition (why T(n) for nuclei vs 2l+1 for atoms)
  - Binding energy B/A_max at Fe-56 — no clean framework match yet
  - Spin-orbit fraction ≈ 1/3 per shell (not LEAK = 1/φ⁴)

Modules:
    shells      — Magic numbers, HO shells, spin-orbit detachment
    scale       — Bracket gap analysis, nuclear-atomic transition
"""

from .shells import (
    NUCLEAR_MAGIC, HO_MAGIC,
    ho_shell_capacities, spin_orbit_detachment,
    magic_fibonacci_proximity,
)
from .scale import bracket_gap, zeckendorf_compactness
