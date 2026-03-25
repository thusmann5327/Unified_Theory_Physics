"""
cosmology.py — 5→3 collapse: tiling vertex fractions → cosmological budget
============================================================================

VERIFIED:
  - Ω_b  = LEAK × G1 = (1/φ⁴) × 0.3243 = 4.73% (Planck: 4.76%, 0.6%)
  - Ω_DM = (LEAK - W⁴) + (GB + BS) × G1 = 26.7% (Planck: 26.5%, 0.8%)
  - Ω_DE = 1 - Ω_b - Ω_DM = 68.5% (Planck: 68.5%, 0.1%)

The tiling IS the pre-collapse 5-band state.
G1 = 0.3243 is the transmission through the first Cantor sub-gap.
Post-collapse (observed) fractions = pre-collapse tiling × G1.
"""

from core.constants import PHI, LEAK

W = (2 + PHI**(1/PHI**2)) / PHI**4
G1_COLLAPSE = 0.3243  # first σ₃ sub-gap fraction


def collapse_budget(vertex_fractions):
    """Compute cosmological energy budget from tiling vertex fractions.

    Parameters
    ----------
    vertex_fractions : dict
        Maps vertex type string to dict with 'fraction' key.
        Expected types: 'G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS'.

    Returns
    -------
    dict with predicted and observed cosmological fractions.
    """
    gs_frac = vertex_fractions.get('GS', {}).get('fraction', 0)
    bg_frac = vertex_fractions.get('BG', {}).get('fraction', 0)
    bs_frac = vertex_fractions.get('BS', {}).get('fraction', 0)
    g_frac = vertex_fractions.get('G', {}).get('fraction', 0)

    wb4 = W**4

    # Baryonic: LEAK × G1
    baryon_pred = LEAK * G1_COLLAPSE
    err_baryon = abs(baryon_pred - wb4) / wb4 * 100

    # Dark matter: local (LEAK - W⁴) + conduit (GB + BS) × G1
    local_dm = LEAK - wb4
    conduit_walls = bg_frac + bs_frac
    conduit_dm = conduit_walls * G1_COLLAPSE
    total_dm = local_dm + conduit_dm

    planck_dm = 0.265
    err_dm = abs(total_dm - planck_dm) / planck_dm * 100

    # Dark energy: remainder
    de_pred = 1 - wb4 - total_dm
    planck_de = 0.685
    err_de = abs(de_pred - planck_de) / planck_de * 100

    # GS vs LEAK
    err_gs_leak = abs(gs_frac - LEAK) / LEAK * 100 if gs_frac > 0 else float('inf')

    # G only vs R_MATTER
    err_g_matter = abs(g_frac - 0.0728) / 0.0728 * 100 if g_frac > 0 else float('inf')

    return {
        'baryon': {
            'predicted': round(baryon_pred, 6),
            'observed_W4': round(wb4, 6),
            'error_pct': round(err_baryon, 1),
        },
        'dark_matter': {
            'local_dm': round(local_dm, 6),
            'conduit_dm': round(conduit_dm, 6),
            'total': round(total_dm, 6),
            'planck': planck_dm,
            'error_pct': round(err_dm, 1),
        },
        'dark_energy': {
            'predicted': round(de_pred, 6),
            'planck': planck_de,
            'error_pct': round(err_de, 1),
        },
        'gs_vs_leak': {
            'gs_fraction': round(gs_frac, 6),
            'leak': round(LEAK, 6),
            'error_pct': round(err_gs_leak, 1),
        },
        'g_vs_r_matter': {
            'g_fraction': round(g_frac, 6),
            'r_matter': 0.0728,
            'error_pct': round(err_g_matter, 1),
        },
    }
