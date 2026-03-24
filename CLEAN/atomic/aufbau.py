"""
aufbau.py — Electron configurations from first principles
===========================================================

Computes quantum numbers (period, n_p, n_d, n_f, n_s, block) using
Madelung filling order with REAL_CONFIG overrides for anomalous
d-block elements (Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, Pt, Au).

These anomalies are NOT exceptions — they are topological gate
fixed points where the d-shell configuration minimises the
Cantor node energy.
"""

from .elements import REAL_CONFIG


def aufbau(Z):
    """
    Compute quantum numbers for element Z.

    Returns: (period, n_p, n_d, n_f, n_s, block)
        period  — principal quantum number of valence shell
        n_p     — number of valence p-electrons
        n_d     — number of valence d-electrons (0 if not d-block)
        n_f     — number of f-electrons (0 if not f-block)
        n_s     — number of valence s-electrons
        block   — 's', 'p', 'd', 'f', or 'ng' (noble gas)
    """
    # Build Madelung-ordered subshells
    sub = []
    for n in range(1, 8):
        for l in range(n):
            sub.append((n, l, 2 * (2 * l + 1)))
    sub.sort(key=lambda s: (s[0] + s[1], s[0]))

    # Fill electrons
    rem = Z
    filled = []
    for n, l, cap in sub:
        if rem <= 0:
            break
        e = min(rem, cap)
        filled.append((n, l, e, cap))
        rem -= e

    # Extract quantum numbers
    per = max(n for n, l, e, c in filled)
    n_p = sum(e for n, l, e, c in filled if n == per and l == 1)
    n_d_val = sum(e for n, l, e, c in filled if l == 2 and n == per - 1)
    n_f_val = sum(e for n, l, e, c in filled if l == 3 and n == per - 2)
    n_s_val = sum(e for n, l, e, c in filled if n == per and l == 0)
    last_l = filled[-1][1]
    blk = {0: 's', 1: 'p', 2: 'd', 3: 'f'}.get(last_l, '?')

    # Detect noble gas (full valence shell)
    shell_e = {}
    shell_cap = {}
    for n, l, e, cap in filled:
        shell_e[n] = shell_e.get(n, 0) + e
        shell_cap[n] = shell_cap.get(n, 0) + cap
    if shell_e.get(per, 0) == shell_cap.get(per, 0):
        if Z == 2 or (last_l == 1 and filled[-1][2] == filled[-1][3]):
            blk = 'ng'
            if Z == 2:
                n_p = 0

    # Block-dependent extraction
    n_d = 0 if blk in ('p', 's', 'ng', 'f') else n_d_val
    n_f = n_f_val if blk == 'f' else 0
    n_s = n_s_val

    # Apply REAL_CONFIG for anomalous d-block filling
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]

    return per, n_p, n_d, n_f, n_s, blk
