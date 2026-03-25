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

Verified (magic.py):
  - Recursive formula reproduces all 7 magic numbers exactly
  - Detachment 8,10,12,14 = arithmetic step 2
  - d-capacity = detach(N=4), f-capacity = detach(N=6)
  - 82/89 ≈ √R_C to 0.3%
  - Predicts magic(7) = 184

Open questions:
  - Triangular→odd number transition (why T(n) for nuclei vs 2l+1 for atoms)
  - Binding energy B/A_max at Fe-56 — no clean framework match yet

Modules:
    shells      — HO shells, spin-orbit detachment patterns
    magic       — Magic number formula (all 7 exact), predictions
    scale       — Bracket gap analysis, nuclear-atomic transition
"""

from .shells import (
    NUCLEAR_MAGIC, HO_MAGIC,
    ho_shell_capacities, spin_orbit_detachment,
    magic_fibonacci_proximity,
)
from .magic import magic_number, magic_sequence, detachment_analysis, sqrt_rc_proximity
from .scale import bracket_gap, zeckendorf_compactness
