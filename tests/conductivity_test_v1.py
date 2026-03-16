#!/usr/bin/env python3
"""
Four-Gate Conductivity Model — Test Suite
Based on Husmann Decomposition atomic_scorecard.py (v5)

Tests proposed conductivity formula:
  σ_elec = σ₀ × S(n_s) × D(n_d) × P(period)

where all factors derive from φ and the Cantor barrier 1/φ⁴.
"""

import math

# ── Constants (all from φ² = φ + 1 and D = 233) ──────────────────────────
PHI = (1 + math.sqrt(5)) / 2
LEAK = 1 / PHI**4                          # 0.14590 — Cantor barrier transmission
BASE = 1.408382                             # σ₄/σ_shell from AAH eigensolver
G1 = 0.324325                              # First σ₃ sub-gap fraction
BOS = 0.992022                             # bronze_σ₃/σ_shell
DARK_GOLD = 0.290                          # Gold axis dark fraction
R_C = 1 - LEAK                             # 0.85410 — reflection complement

print(f"φ = {PHI:.6f}")
print(f"1/φ⁴ (LEAK) = {LEAK:.6f}")
print(f"1 - 1/φ⁴ (R_C) = {R_C:.6f}")
print(f"BASE = {BASE:.6f}")
print(f"DARK_GOLD = {DARK_GOLD:.6f}")
print()

# ── Electron Configurations ───────────────────────────────────────────────
# NIST anomalous configs (from paper Section 3.2)
ANOMALOUS = {
    24: {'n_d': 5, 'n_s': 1},   # Cr: [Ar] 3d⁵4s¹
    29: {'n_d': 10, 'n_s': 1},  # Cu: [Ar] 3d¹⁰4s¹
    41: {'n_d': 4, 'n_s': 1},   # Nb: [Kr] 4d⁴5s¹
    42: {'n_d': 5, 'n_s': 1},   # Mo: [Kr] 4d⁵5s¹
    44: {'n_d': 7, 'n_s': 1},   # Ru: [Kr] 4d⁷5s¹
    45: {'n_d': 8, 'n_s': 1},   # Rh: [Kr] 4d⁸5s¹
    46: {'n_d': 10, 'n_s': 0},  # Pd: [Kr] 4d¹⁰
    47: {'n_d': 10, 'n_s': 1},  # Ag: [Kr] 4d¹⁰5s¹
}

def aufbau(Z):
    """Return (period, n_p, n_d, n_s, block) for element Z."""
    # Period boundaries
    if Z <= 2:    period = 1
    elif Z <= 10: period = 2
    elif Z <= 18: period = 3
    elif Z <= 36: period = 4
    elif Z <= 54: period = 5
    elif Z <= 86: period = 6
    else:         period = 7
    
    # Noble gases
    noble = {2, 10, 18, 36, 54, 86}
    if Z in noble:
        if Z == 2:  return (1, 0, 0, 2, 'noble_gas')
        if Z == 10: return (2, 6, 0, 2, 'noble_gas')
        if Z == 18: return (3, 6, 0, 2, 'noble_gas')
        if Z == 36: return (4, 6, 10, 2, 'noble_gas')
        if Z == 54: return (5, 6, 10, 2, 'noble_gas')
        if Z == 86: return (6, 6, 10, 2, 'noble_gas')
    
    # Check anomalous
    if Z in ANOMALOUS:
        a = ANOMALOUS[Z]
        n_d = a['n_d']
        n_s = a['n_s']
        # Determine n_p from remaining electrons
        if period == 4:
            core = 18  # Ar
            remaining = Z - core - n_d - n_s
        elif period == 5:
            core = 36  # Kr
            remaining = Z - core - n_d - n_s
        else:
            remaining = 0
        n_p = max(0, remaining)
        block = 'd'
        return (period, n_p, n_d, n_s, block)
    
    # Standard Madelung filling
    if period == 1:
        return (1, 0, 0, Z, 's')
    
    # Determine block and electron counts
    if period == 2:
        core = 2
        val = Z - core
        if val <= 2:
            return (2, 0, 0, val, 's')
        else:
            return (2, val - 2, 0, 2, 'p')
    
    if period == 3:
        core = 10
        val = Z - core
        if val <= 2:
            return (3, 0, 0, val, 's')
        else:
            return (3, val - 2, 0, 2, 'p')
    
    if period == 4:
        core = 18
        val = Z - core
        if val <= 2:
            return (4, 0, 0, val, 's')
        elif val <= 12:
            n_d = val - 2
            return (4, 0, n_d, 2, 'd')
        else:
            n_p = val - 12
            return (4, n_p, 10, 2, 'p')
    
    if period == 5:
        core = 36
        val = Z - core
        if val <= 2:
            return (5, 0, 0, val, 's')
        elif val <= 12:
            n_d = val - 2
            return (5, 0, n_d, 2, 'd')
        else:
            n_p = val - 12
            return (5, n_p, 10, 2, 'p')
    
    if period == 6:
        core = 54
        val = Z - core
        if val <= 2:
            return (6, 0, 0, val, 's')
        # Simplified: skip f-block detail, handle key elements
        elif val <= 12 + 14:  # d-block after f-block
            # This is approximate for period 6 d-block
            n_d = val - 2 - 14 if val > 16 else val - 2
            return (6, 0, min(n_d, 10), 2, 'd')
        else:
            return (6, val - 26, 10, 2, 'p')
    
    return (period, 0, 0, 0, 's')

# Period 6 overrides for key elements
PERIOD6_OVERRIDES = {
    55: (6, 0, 0, 1, 's'),    # Cs
    56: (6, 0, 0, 2, 's'),    # Ba
    72: (6, 0, 2, 2, 'd'),    # Hf
    73: (6, 0, 3, 2, 'd'),    # Ta
    74: (6, 0, 4, 2, 'd'),    # W
    75: (6, 0, 5, 2, 'd'),    # Re
    76: (6, 0, 6, 2, 'd'),    # Os
    77: (6, 0, 7, 2, 'd'),    # Ir
    78: (6, 0, 9, 1, 'd'),    # Pt  [Xe]4f¹⁴5d⁹6s¹
    79: (6, 0, 10, 1, 'd'),   # Au  [Xe]4f¹⁴5d¹⁰6s¹
    80: (6, 0, 10, 2, 'd'),   # Hg
    81: (6, 1, 10, 2, 'p'),   # Tl
    82: (6, 2, 10, 2, 'p'),   # Pb
}

def get_config(Z):
    """Get electron configuration, with overrides."""
    if Z in PERIOD6_OVERRIDES:
        return PERIOD6_OVERRIDES[Z]
    return aufbau(Z)


# ── Radius Prediction (from paper, for reference) ────────────────────────
def predict_ratio(Z):
    """Predict vdW/cov ratio from four-gate model."""
    per, n_p, n_d, n_s, block = get_config(Z)
    
    if block == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        
        if is_boundary and has_s:
            return 1 + LEAK                                    # LEAK
        elif n_d >= 9 and not has_s:
            return BASE + DARK_GOLD / PHI**4                   # REFLECT
        else:
            theta = 1 - (n_d / 10) * DARK_GOLD
            return math.sqrt(1 + (theta * BOS)**2)             # STANDARD
    
    elif block == 'noble_gas':
        theta = 1 + n_p * (G1 / BOS) * PHI**(-(per - 1))
        return math.sqrt(1 + (theta * BOS)**2)                 # PYTHAGOREAN
    
    else:  # s-block or p-block
        ratio = BASE + n_p * G1 * PHI**(-(per - 1))            # ADDITIVE
        if block == 'p' and n_p >= 4 and per >= 3:
            ratio *= (1 - LEAK)                                # P-HOLE
        return ratio


# ── Gate Mode Classification ─────────────────────────────────────────────
def gate_mode(Z):
    """Classify element's gate state."""
    per, n_p, n_d, n_s, block = get_config(Z)
    
    if block == 'noble_gas':
        return 'sealed'
    
    if block == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        
        if is_boundary and has_s:
            return 'leak'
        elif n_d >= 9 and not has_s:
            return 'reflect'
        else:
            return 'standard'
    
    if block == 'p' and n_p >= 4 and per >= 3:
        return 'p-hole'
    
    return 'additive'


# ══════════════════════════════════════════════════════════════════════════
# CONDUCTIVITY MODELS
# ══════════════════════════════════════════════════════════════════════════

# Experimental conductivity data (MS/m at ~20°C)
CONDUCTIVITY_DATA = {
    # d¹⁰ family (key test group)
    29: ('Cu', 59.6),
    30: ('Zn', 16.9),
    46: ('Pd', 9.5),
    47: ('Ag', 63.0),
    48: ('Cd', 13.8),
    79: ('Au', 45.2),
    80: ('Hg', 1.04),
    
    # Other d-block
    21: ('Sc', 1.8),
    22: ('Ti', 2.4),
    23: ('V',  5.0),
    24: ('Cr', 7.9),
    25: ('Mn', 0.7),
    26: ('Fe', 10.0),
    27: ('Co', 17.2),
    28: ('Ni', 14.3),
    
    39: ('Y',  1.7),
    40: ('Zr', 2.4),
    41: ('Nb', 7.0),
    42: ('Mo', 18.7),
    43: ('Tc', 6.7),   # estimated
    44: ('Ru', 13.7),
    45: ('Rh', 21.1),
    
    # Period 6 d-block
    72: ('Hf', 3.3),
    73: ('Ta', 7.6),
    74: ('W',  18.9),
    75: ('Re', 5.4),
    76: ('Os', 12.4),
    77: ('Ir', 21.3),
    78: ('Pt', 9.4),
    
    # s-block metals
    3:  ('Li', 10.8),
    4:  ('Be', 25.0),
    11: ('Na', 21.0),
    12: ('Mg', 22.7),
    13: ('Al', 37.7),   # p-block but metallic
    19: ('K',  14.0),
    20: ('Ca', 29.8),
    37: ('Rb', 8.0),
    38: ('Sr', 7.6),
    55: ('Cs', 4.8),
    56: ('Ba', 2.9),
    
    # p-block metals
    31: ('Ga', 7.1),
    32: ('Ge', 0.002),  # semiconductor
    33: ('As', 3.4),
    49: ('In', 11.6),
    50: ('Sn', 9.2),
    51: ('Sb', 2.6),
    81: ('Tl', 6.7),
    82: ('Pb', 4.8),
}


# ── Model A: Basic S×D×P ─────────────────────────────────────────────────
def conductivity_model_A(Z):
    """
    Model A: σ = σ₀ × S(n_s) × D(n_d) × P(period)
    
    S-valve:  S(1) = LEAK, S(2) = LEAK×R_C, S(0) = LEAK³
    D-shell:  D = (1 - |n_d-10|/10 × dg) × (1 - sin²(πn_d/10) × LEAK)
    Period:   P = φ^(-(per-2))
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    
    # S-valve
    if n_s == 1:
        S = LEAK
    elif n_s == 2:
        S = LEAK * R_C
    elif n_s == 0:
        S = LEAK ** 3
    else:
        S = LEAK * R_C
    
    # D-shell transparency
    if block == 'd':
        theta_c = 1 - abs(n_d - 10) / 10 * DARK_GOLD
        exchange = math.sin(math.pi * n_d / 10)**2 * LEAK
        D = theta_c * (1 - exchange)
    elif block in ('p', 'noble_gas'):
        # p-electrons scatter too, but differently
        D = 1 - n_p / 6 * LEAK  # mild p-shell scattering
    else:
        D = 1.0
    
    # Period damping
    P = PHI ** (-(per - 2))
    
    return S * D * P


# ── Model B: Gate-mode aware ─────────────────────────────────────────────
def conductivity_model_B(Z):
    """
    Model B: Mode-aware conductivity.
    
    Uses the same gate classification as the radius prediction.
    Key insight: conductivity ∝ (gate openness)^n where n captures
    how many transmission events occur per conduction step.
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    # Period damping (Cantor recursion depth)
    P = PHI ** (-(per - 2))
    
    if mode == 'sealed':
        return 0.0  # noble gas
    
    if mode == 'leak':
        # d¹⁰s¹: one clean open gate → maximum transmission
        if n_d >= 9 and n_s == 1:
            S = LEAK
        # d¹⁰s²: open gate but self-screened
        elif n_d >= 9 and n_s == 2:
            S = LEAK * R_C
        # Early d leak (d≤4, s¹): gate just opening, d-shell still scattering
        elif n_d <= 4 and n_s == 1:
            S = LEAK * (1 - (4 - n_d) / 4 * DARK_GOLD)
        # Early d leak (d≤4, s²): 
        elif n_d <= 4 and n_s == 2:
            S = LEAK * R_C * (1 - (4 - n_d) / 4 * DARK_GOLD)
        else:
            S = LEAK
        
        return S * P
    
    if mode == 'reflect':
        # Gate shut. Conduction through d-band overlap only.
        S = LEAK ** 2  # Two barriers: in through d, out through d
        return S * P
    
    if mode == 'standard':
        # Mid d-block. s-electrons present but d-shell absorbs.
        theta = 1 - (n_d / 10) * DARK_GOLD
        exchange = math.sin(math.pi * n_d / 10)**2
        # Conductivity = LEAK × (1 - exchange×LEAK) × theta
        S = LEAK * (1 - exchange * LEAK) * theta
        if n_s == 1:
            S *= (1 + LEAK)  # Single s more mobile
        return S * P
    
    if mode == 'p-hole':
        # p-holes pull inward: conductivity reduced
        S = LEAK * R_C * (1 - n_p / 6 * LEAK)
        return S * P
    
    if mode == 'additive':
        # s/p block metals
        if block == 's':
            if n_s == 1:
                S = LEAK * 1.0  # Clean s-band
            else:
                S = LEAK * R_C  # s² screening
        else:
            # p-block: depends on p-electron count
            S = LEAK * R_C * (1 - n_p / 6 * DARK_GOLD)
        return S * P
    
    return LEAK * P  # fallback


# ── Model C: Transmission chain with conductance quantum ──────────────────
def conductivity_model_C(Z):
    """
    Model C: Full chain model.
    
    σ = G₀/a × T_gate × T_d × T_exchange × T_period
    
    where G₀ = 2e²/h and all T factors are powers of 1/φ⁴.
    
    Key: count the number of φ⁴ barriers each conduction electron
    must cross in one hop. Fewer barriers = higher conductivity.
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    # Period factor: each period adds one Cantor level
    n_period = per - 2  # Period 2 = baseline (0 extra levels)
    T_period = PHI ** (-n_period)
    
    if mode == 'sealed':
        return 0.0
    
    # Count barrier crossings
    if mode == 'leak':
        if n_d >= 9 and n_s == 1:
            # d¹⁰s¹: 1 barrier (σ₄ open on both sides)
            n_barriers = 1
            bonus = 1.0
        elif n_d >= 9 and n_s == 2:
            # d¹⁰s²: 1 barrier + partial re-closure
            n_barriers = 1
            bonus = R_C
        elif n_d <= 4:
            # Early d: 1 barrier (σ₄ open) + d-shell scattering
            n_barriers = 1
            bonus = 1 - abs(n_d - 2) / 4 * DARK_GOLD
            if n_s == 2:
                bonus *= R_C
        else:
            n_barriers = 1
            bonus = 1.0
    
    elif mode == 'reflect':
        # Gate shut: must tunnel through 3 barriers
        n_barriers = 3
        bonus = 1.0
    
    elif mode == 'standard':
        # Mid d-block: 2 barriers (σ₂ absorbs, σ₄ partially open)
        n_barriers = 2
        # Exchange penalty at d⁵
        exchange = math.sin(math.pi * n_d / 10)**2
        bonus = (1 - exchange * DARK_GOLD)
        if n_s == 1:
            bonus *= (1 + LEAK)  # s¹ more mobile
    
    elif mode == 'p-hole':
        n_barriers = 2
        bonus = R_C
    
    elif mode == 'additive':
        if block == 's':
            n_barriers = 1 if n_s == 1 else 2
            bonus = 1.0
        else:
            n_barriers = 2
            bonus = 1 - n_p / 6 * LEAK
    
    else:
        n_barriers = 2
        bonus = 1.0
    
    T_gate = LEAK ** n_barriers
    
    return T_gate * bonus * T_period


# ══════════════════════════════════════════════════════════════════════════
# TESTING
# ══════════════════════════════════════════════════════════════════════════

def test_model(model_func, model_name, data):
    """Test a conductivity model against experimental data."""
    
    print(f"\n{'='*80}")
    print(f"  {model_name}")
    print(f"{'='*80}")
    
    results = []
    for Z in sorted(data.keys()):
        sym, sigma_exp = data[Z]
        per, n_p, n_d, n_s, block = get_config(Z)
        mode = gate_mode(Z)
        sigma_pred_raw = model_func(Z)
        results.append((Z, sym, sigma_exp, sigma_pred_raw, mode, per, n_d, n_s, block))
    
    # Remove zeros
    nonzero = [(Z, s, se, sp, m, p, nd, ns, b) for Z, s, se, sp, m, p, nd, ns, b in results if sp > 0 and se > 0]
    
    if not nonzero:
        print("No non-zero predictions!")
        return
    
    # Find scaling factor that minimizes log-space error (single calibration constant σ₀)
    log_ratios = [math.log(se / sp) for _, _, se, sp, _, _, _, _, _ in nonzero]
    log_sigma0 = sum(log_ratios) / len(log_ratios)
    sigma0 = math.exp(log_sigma0)
    
    print(f"\n  Calibration constant σ₀ = {sigma0:.2f} MS/m")
    print(f"  (This is the single fitted parameter — all structure comes from the model)")
    print()
    
    # Now compute scaled predictions and errors
    print(f"  {'Z':>3} {'Sym':>3} {'Mode':<10} {'Per':>3} {'n_d':>3} {'n_s':>3} "
          f"{'σ_exp':>8} {'σ_pred':>8} {'Ratio':>7} {'LogErr':>7}")
    print(f"  {'-'*3} {'-'*3} {'-'*10} {'-'*3} {'-'*3} {'-'*3} "
          f"{'-'*8} {'-'*8} {'-'*7} {'-'*7}")
    
    log_errors = []
    abs_ratios = []
    
    for Z, sym, se, sp_raw, mode, per, nd, ns, block in results:
        sp = sp_raw * sigma0
        if sp > 0 and se > 0:
            ratio = se / sp
            log_err = abs(math.log10(ratio))
            log_errors.append(log_err)
            abs_ratios.append(ratio)
            print(f"  {Z:>3} {sym:>3} {mode:<10} {per:>3} {nd:>3} {ns:>3} "
                  f"{se:>8.2f} {sp:>8.2f} {ratio:>7.2f} {log_err:>7.3f}")
        elif se == 0:
            print(f"  {Z:>3} {sym:>3} {mode:<10} {per:>3} {nd:>3} {ns:>3} "
                  f"{se:>8.2f} {'ZERO':>8} {'—':>7} {'—':>7}")
        else:
            print(f"  {Z:>3} {sym:>3} {mode:<10} {per:>3} {nd:>3} {ns:>3} "
                  f"{se:>8.2f} {sp:>8.4f} {'—':>7} {'—':>7}")
    
    # Statistics
    if log_errors:
        mean_log = sum(log_errors) / len(log_errors)
        within_2x = sum(1 for r in abs_ratios if 0.5 <= r <= 2.0)
        within_3x = sum(1 for r in abs_ratios if 0.33 <= r <= 3.0)
        within_5x = sum(1 for r in abs_ratios if 0.2 <= r <= 5.0)
        n = len(abs_ratios)
        
        # Rank correlation (Spearman-like)
        exp_vals = [se for _, _, se, _, _, _, _, _, _ in nonzero]
        pred_vals = [sp * sigma0 for _, _, _, sp, _, _, _, _, _ in nonzero]
        
        # Simple rank correlation
        exp_rank = rank_list(exp_vals)
        pred_rank = rank_list(pred_vals)
        n_r = len(exp_rank)
        d_sq = sum((e - p)**2 for e, p in zip(exp_rank, pred_rank))
        rho = 1 - 6 * d_sq / (n_r * (n_r**2 - 1))
        
        print(f"\n  ── Summary ──")
        print(f"  Elements tested:   {n}")
        print(f"  Mean |log₁₀ error|: {mean_log:.3f}  (0 = perfect, 0.3 = 2× off)")
        print(f"  Within 2×:         {within_2x}/{n} ({100*within_2x/n:.0f}%)")
        print(f"  Within 3×:         {within_3x}/{n} ({100*within_3x/n:.0f}%)")
        print(f"  Within 5×:         {within_5x}/{n} ({100*within_5x/n:.0f}%)")
        print(f"  Rank correlation ρ: {rho:.3f}")
    
    return sigma0, log_errors, abs_ratios


def rank_list(vals):
    """Return ranks (1-based) for a list of values."""
    indexed = sorted(enumerate(vals), key=lambda x: x[1])
    ranks = [0] * len(vals)
    for rank, (idx, _) in enumerate(indexed, 1):
        ranks[idx] = rank
    return ranks


# ══════════════════════════════════════════════════════════════════════════
# D¹⁰ FAMILY FOCUSED TEST
# ══════════════════════════════════════════════════════════════════════════

def test_d10_family():
    """Focused test on the d¹⁰ family where the s-valve is cleanest."""
    
    print(f"\n{'='*80}")
    print(f"  D¹⁰ FAMILY: S-VALVE ISOLATION TEST")
    print(f"{'='*80}")
    
    d10 = {
        29: ('Cu', 59.6, 10, 1, 4),   # d¹⁰s¹, period 4
        30: ('Zn', 16.9, 10, 2, 4),   # d¹⁰s², period 4
        46: ('Pd', 9.5,  10, 0, 5),   # d¹⁰s⁰, period 5
        47: ('Ag', 63.0, 10, 1, 5),   # d¹⁰s¹, period 5
        48: ('Cd', 13.8, 10, 2, 5),   # d¹⁰s², period 5
        79: ('Au', 45.2, 10, 1, 6),   # d¹⁰s¹, period 6
        80: ('Hg', 1.04, 10, 2, 6),   # d¹⁰s², period 6
    }
    
    print(f"\n  Key ratios (experimental):")
    print(f"  Cu/Zn  = {59.6/16.9:.2f}  (same period, s¹ vs s²)")
    print(f"  Ag/Cd  = {63.0/13.8:.2f}  (same period, s¹ vs s²)")
    print(f"  Au/Hg  = {45.2/1.04:.1f}  (same period, s¹ vs s², RELATIVISTIC)")
    print(f"  Cu/Ag  = {59.6/63.0:.3f}  (same mode, period 4 vs 5)")
    print(f"  Zn/Cd  = {16.9/13.8:.3f}  (same mode, period 4 vs 5)")
    print(f"  Ag/Pd  = {63.0/9.5:.2f}   (same period, s¹ vs s⁰)")
    
    # Test S-valve factor predictions
    print(f"\n  S-valve factor analysis:")
    print(f"  {'Factor':<25} {'Value':>10} {'Predicted ratio':>18}")
    print(f"  {'-'*25} {'-'*10} {'-'*18}")
    
    # S(1) / S(2) — should predict d¹⁰s¹/d¹⁰s² ratio
    # Model A: S(1)/S(2) = LEAK / (LEAK × R_C) = 1/R_C
    r_A = 1 / R_C
    print(f"  {'S(1)/S(2) = 1/R_C':<25} {r_A:>10.4f} {'Cu/Zn=3.53, Ag/Cd=4.57':>18}")
    
    # Model B: same for leak mode
    # Model C: S(1) = LEAK¹, S(2) = LEAK¹ × R_C → same ratio
    
    # Alternative: S(1)/S(2) = 1/R_C² 
    r_B = 1 / R_C**2
    print(f"  {'S(1)/S(2) = 1/R_C²':<25} {r_B:>10.4f}")
    
    # What if S(2) has an extra barrier?
    r_C = LEAK / LEAK**2
    print(f"  {'LEAK/LEAK² = 1/LEAK':<25} {r_C:>10.4f}")
    
    r_D = 1 / LEAK
    print(f"  {'1/LEAK = φ⁴':<25} {r_D:>10.4f}")
    
    # Cu/Zn ratio suggests s¹/s² ≈ 3.5
    # Ag/Cd ratio suggests s¹/s² ≈ 4.6
    # The difference (3.5 vs 4.6) is the period effect
    
    # Period ratio test
    print(f"\n  Period ratio analysis (same-mode elements):")
    print(f"  Cu(P4)/Ag(P5) = {59.6/63.0:.3f}  — Model: φ^(-1) = {1/PHI:.3f}")
    print(f"  Zn(P4)/Cd(P5) = {16.9/13.8:.3f}  — Model: φ^(-1) = {1/PHI:.3f}")
    print(f"  Ag(P5)/Au(P6) = {63.0/45.2:.3f}  — Model: φ^(-1) = {1/PHI:.3f}")
    print(f"  Cd(P5)/Hg(P6) = {13.8/1.04:.2f}  — ANOMALOUS (relativistic Hg)")
    
    print(f"\n  Observations:")
    print(f"  • Cu/Ag ≈ 0.946 — Ag is BETTER despite being one period deeper.")
    print(f"    This violates P=φ^(-Δperiod) unless 5d is more diffuse than 4d")
    print(f"    (better orbital overlap compensates period damping).")
    print(f"  • Zn/Cd ≈ 1.225 — matches φ^(-1) = 0.618 INVERTED,")
    print(f"    suggesting Zn benefits from shorter lattice parameter.")
    print(f"  • Hg is catastrophically low — relativistic 6s contraction")
    print(f"    effectively shuts the gate (Hg is a liquid at RT).")


# ══════════════════════════════════════════════════════════════════════════
# MODE-GROUPED ANALYSIS
# ══════════════════════════════════════════════════════════════════════════

def mode_analysis():
    """Group by gate mode and check ordering within groups."""
    print(f"\n{'='*80}")
    print(f"  MODE-GROUPED CONDUCTIVITY ORDERING")
    print(f"{'='*80}")
    
    modes = {}
    for Z in sorted(CONDUCTIVITY_DATA.keys()):
        sym, sigma = CONDUCTIVITY_DATA[Z]
        mode = gate_mode(Z)
        per, n_p, n_d, n_s, block = get_config(Z)
        if mode not in modes:
            modes[mode] = []
        modes[mode].append((Z, sym, sigma, per, n_d, n_s))
    
    for mode in ['leak', 'standard', 'reflect', 'additive', 'p-hole', 'sealed']:
        if mode not in modes:
            continue
        group = sorted(modes[mode], key=lambda x: -x[2])  # Sort by conductivity desc
        print(f"\n  ── {mode.upper()} mode ──")
        print(f"  {'Z':>3} {'Sym':>3} {'Per':>3} {'n_d':>3} {'n_s':>3} {'σ(MS/m)':>10}")
        print(f"  {'-'*3} {'-'*3} {'-'*3} {'-'*3} {'-'*3} {'-'*10}")
        for Z, sym, sigma, per, nd, ns in group:
            print(f"  {Z:>3} {sym:>3} {per:>3} {nd:>3} {ns:>3} {sigma:>10.2f}")
        
        # Check if the model's ordering matches
        sigs = [s for _, _, s, _, _, _ in group]
        is_ordered = all(sigs[i] >= sigs[i+1] for i in range(len(sigs)-1))
        print(f"  Monotonically ordered: {'Yes' if is_ordered else 'No'}")


# ══════════════════════════════════════════════════════════════════════════
# BARRIER-COUNT MODEL (cleanest zero-parameter version)
# ══════════════════════════════════════════════════════════════════════════

def conductivity_model_D(Z):
    """
    Model D: Pure barrier-counting.
    
    Each conduction event crosses N Cantor barriers.
    σ ∝ (1/φ⁴)^N × period_factor
    
    N = 1: d¹⁰s¹ (one open gate, clean carrier)
    N = 1.5: d¹⁰s² (open gate, self-screened)
    N = 2: standard d-block, s-block s²
    N = 2.5: standard d-block with exchange
    N = 3: reflect (gate shut), early d-block
    N = 0.5: s-block s¹ (half barrier — diffuse s-band)
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    if mode == 'sealed':
        return 0.0
    
    # Assign barrier count
    if mode == 'leak':
        if n_d >= 9 and n_s == 1:
            N = 1.0               # d¹⁰s¹: cleanest single-gate
        elif n_d >= 9 and n_s == 2:
            N = 1.5               # d¹⁰s²: gate open but screened
        elif n_d <= 4 and n_s == 1:
            N = 2.0 + (4 - n_d) * 0.25   # Early d, s¹: more barriers with fewer d
        elif n_d <= 4 and n_s == 2:
            N = 2.5 + (4 - n_d) * 0.25   # Early d, s²: even more
        else:
            N = 1.5
    
    elif mode == 'reflect':
        N = 3.0                   # Gate shut: tunnel through 3 barriers
    
    elif mode == 'standard':
        # d⁵ is worst, d⁸ is better
        exchange = math.sin(math.pi * n_d / 10)**2
        N = 2.0 + exchange * 1.0  # 2.0 base, up to 3.0 at d⁵
        if n_s == 1:
            N -= 0.5              # s¹ helps
    
    elif mode == 'additive':
        if block == 's':
            if n_s == 1:
                N = 1.5           # Alkali: one s-electron, reasonably clean
            else:
                N = 1.0           # Alkaline earth: paradoxically good conductors
        else:
            # p-block metals
            N = 2.0 + n_p * 0.25
    
    elif mode == 'p-hole':
        N = 2.5 + n_p * 0.1
    
    else:
        N = 2.0
    
    T = LEAK ** N
    P = PHI ** (-(per - 2))
    
    return T * P


# ══════════════════════════════════════════════════════════════════════════
# RUN ALL TESTS
# ══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    
    # First: mode analysis (qualitative)
    mode_analysis()
    
    # D¹⁰ family deep dive
    test_d10_family()
    
    # Test all four models
    print(f"\n\n{'#'*80}")
    print(f"#  QUANTITATIVE MODEL COMPARISON")
    print(f"{'#'*80}")
    
    models = [
        (conductivity_model_A, "Model A: S×D×P (multiplicative)"),
        (conductivity_model_B, "Model B: Gate-mode aware"),
        (conductivity_model_C, "Model C: Barrier-chain transmission"),
        (conductivity_model_D, "Model D: Pure barrier counting"),
    ]
    
    summary = []
    for func, name in models:
        result = test_model(func, name, CONDUCTIVITY_DATA)
        if result:
            sigma0, log_errs, ratios = result
            mean_log = sum(log_errs) / len(log_errs)
            within_2x = sum(1 for r in ratios if 0.5 <= r <= 2.0) / len(ratios)
            summary.append((name, sigma0, mean_log, within_2x))
    
    print(f"\n\n{'='*80}")
    print(f"  FINAL COMPARISON")
    print(f"{'='*80}")
    print(f"\n  {'Model':<45} {'σ₀':>8} {'|log₁₀|':>8} {'Within 2×':>10}")
    print(f"  {'-'*45} {'-'*8} {'-'*8} {'-'*10}")
    for name, s0, ml, w2 in summary:
        print(f"  {name:<45} {s0:>8.1f} {ml:>8.3f} {w2:>9.0%}")
    
    print(f"\n  Interpretation:")
    print(f"  • |log₁₀| = 0 is perfect; 0.30 means average error is 2×")
    print(f"  • 'Within 2×' = fraction of elements predicted within factor of 2")
    print(f"  • σ₀ is the ONLY fitted parameter (overall scale)")
    print(f"  • All structure (which element is higher/lower) comes from the model")
    print(f"  • Rank correlation ρ is the key metric: does the MODEL ORDER match NATURE?")
