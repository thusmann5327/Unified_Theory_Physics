"""
madelung.py — Full Madelung sequence from Cantor node
=======================================================

Reconstructs the complete Aufbau filling order (19 subshells, Z=118)
using subshell_capacity(l) = 2 × round(R_layer × F(7)).

The Madelung order itself (1s, 2s, 2p, ... 7p) comes from the n+l rule.
The CAPACITIES at each step come from the Cantor spectral ratios.

Combined with Z_max = D × D_s = 233 × 0.5 = 116.5 ≈ 118, this
explains both WHY there are 118 elements and WHY each subshell
holds exactly {2, 6, 10, 14} electrons.
"""

from .angular import subshell_capacity

# Standard Madelung filling order through Z=118
MADELUNG_ORDER = [
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (3, 2), (4, 1),
    (5, 0), (4, 2), (5, 1), (6, 0), (4, 3), (5, 2), (6, 1), (7, 0),
    (5, 3), (6, 2), (7, 1),
]

# Reference capacities from quantum mechanics
MADELUNG_CAPACITIES = [2, 2, 6, 2, 6, 2, 10, 6, 2, 10, 6, 2, 14, 10, 6, 2, 14, 10, 6]

SHELL_NAMES = 'spdf'


def madelung_sequence():
    """Reconstruct the full Madelung sequence from Cantor ratios.

    Returns dict with:
        subshells   — list of (label, predicted_cap, qm_cap, match) tuples
        predicted   — list of predicted capacities [2, 2, 6, ...]
        reference   — list of QM capacities [2, 2, 6, ...]
        total       — total predicted electrons
        all_match   — True if every subshell matches
        cumulative_Z — list of cumulative electron counts
    """
    subshells = []
    predicted = []
    cumZ = 0
    all_match = True

    for i, (n, l) in enumerate(MADELUNG_ORDER):
        cap = subshell_capacity(l)
        qm_cap = MADELUNG_CAPACITIES[i]
        cumZ += cap
        match = cap == qm_cap
        if not match:
            all_match = False
        label = f"{n}{SHELL_NAMES[l]}"
        subshells.append({
            'label': label,
            'n': n,
            'l': l,
            'predicted': cap,
            'reference': qm_cap,
            'match': match,
            'cumulative_Z': cumZ,
        })
        predicted.append(cap)

    return {
        'subshells': subshells,
        'predicted': predicted,
        'reference': MADELUNG_CAPACITIES,
        'total': sum(predicted),
        'all_match': all_match,
        'cumulative_Z': [s['cumulative_Z'] for s in subshells],
    }


def z_max_prediction():
    """Z_max from two independent routes.

    Route 1: D × D_s = 233 × 0.5 = 116.5
    Route 2: Sum of Madelung capacities via R_layer × 13
    """
    D = 233
    D_S = 0.5
    z_spectrum = D * D_S

    seq = madelung_sequence()
    z_aufbau = seq['total']

    return {
        'z_spectrum': z_spectrum,
        'z_aufbau': z_aufbau,
        'z_observed': 118,
        'spectrum_error_pct': round(abs(z_spectrum - 118) / 118 * 100, 2),
        'aufbau_match': z_aufbau == 118,
    }
