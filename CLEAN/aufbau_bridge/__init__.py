"""
Aufbau bridge — Subshell capacities from Cantor layer ratios.

The Madelung (Aufbau) filling rule emerges from a single formula:

    2l+1 = round(R_layer × F(7))

where R_layer is the spectral ratio of each Cantor layer and
F(7) = 13 = Δ₃ (bronze discriminant) = 5 + 8.

Modules:
    angular     — Layer-to-angular-momentum mapping
    madelung    — Full Madelung sequence reconstruction
"""

from .angular import angular_modes, subshell_capacity, F7
from .madelung import madelung_sequence, z_max_prediction
