#!/usr/bin/env python3
"""
Four-Gate Conductivity Model — Refined (v2)

Key lessons from v1:
1. Qualitative ordering within modes is PERFECT (monotonic in all groups)
2. Period damping φ^(-(per-2)) is WRONG for conductivity
   - Cu/Ag ≈ 0.95 (nearly equal), not φ ≈ 1.62
   - The radius formula damps with period because it's a SIZE ratio
   - Conductivity depends on OVERLAP, which scales differently
3. d¹⁰s¹ (Cu, Ag, Au) are severely underpredicted in all models
4. Mn is the worst: 10-15× overpredicted — exchange penalty too weak
5. Model D had best rank correlation (ρ=0.533) despite worst absolute errors
   → barrier counting captures the right STRUCTURE

New approach: separate the ORDERING mechanism from the SCALING mechanism.
"""

import math
from collections import defaultdict

PHI = (1 + math.sqrt(5)) / 2
LEAK = 1 / PHI**4
R_C = 1 - LEAK
DARK_GOLD = 0.290
BASE = 1.408382
BOS = 0.992022
G1 = 0.324325

# ── Electron configurations (same as v1) ─────────────────────────────────
ANOMALOUS = {
    24: {'n_d': 5, 'n_s': 1},
    29: {'n_d': 10, 'n_s': 1},
    41: {'n_d': 4, 'n_s': 1},
    42: {'n_d': 5, 'n_s': 1},
    44: {'n_d': 7, 'n_s': 1},
    45: {'n_d': 8, 'n_s': 1},
    46: {'n_d': 10, 'n_s': 0},
    47: {'n_d': 10, 'n_s': 1},
}

PERIOD6_OVERRIDES = {
    55: (6, 0, 0, 1, 's'), 56: (6, 0, 0, 2, 's'),
    72: (6, 0, 2, 2, 'd'), 73: (6, 0, 3, 2, 'd'),
    74: (6, 0, 4, 2, 'd'), 75: (6, 0, 5, 2, 'd'),
    76: (6, 0, 6, 2, 'd'), 77: (6, 0, 7, 2, 'd'),
    78: (6, 0, 9, 1, 'd'), 79: (6, 0, 10, 1, 'd'),
    80: (6, 0, 10, 2, 'd'),
    81: (6, 1, 10, 2, 'p'), 82: (6, 2, 10, 2, 'p'),
}

def aufbau(Z):
    if Z <= 2:    period = 1
    elif Z <= 10: period = 2
    elif Z <= 18: period = 3
    elif Z <= 36: period = 4
    elif Z <= 54: period = 5
    elif Z <= 86: period = 6
    else:         period = 7
    noble = {2, 10, 18, 36, 54, 86}
    if Z in noble:
        configs = {2:(1,0,0,2), 10:(2,6,0,2), 18:(3,6,0,2),
                   36:(4,6,10,2), 54:(5,6,10,2), 86:(6,6,10,2)}
        p, np_, nd, ns = configs[Z]
        return (p, np_, nd, ns, 'noble_gas')
    if Z in PERIOD6_OVERRIDES:
        return PERIOD6_OVERRIDES[Z]
    if Z in ANOMALOUS:
        a = ANOMALOUS[Z]
        n_d, n_s = a['n_d'], a['n_s']
        core = {4:18, 5:36}.get(period, 18)
        n_p = max(0, Z - core - n_d - n_s)
        return (period, n_p, n_d, n_s, 'd')
    if period == 1: return (1, 0, 0, Z, 's')
    if period == 2:
        val = Z - 2
        return (2, 0, 0, val, 's') if val <= 2 else (2, val-2, 0, 2, 'p')
    if period == 3:
        val = Z - 10
        return (3, 0, 0, val, 's') if val <= 2 else (3, val-2, 0, 2, 'p')
    if period == 4:
        val = Z - 18
        if val <= 2: return (4, 0, 0, val, 's')
        elif val <= 12: return (4, 0, val-2, 2, 'd')
        else: return (4, val-12, 10, 2, 'p')
    if period == 5:
        val = Z - 36
        if val <= 2: return (5, 0, 0, val, 's')
        elif val <= 12: return (5, 0, val-2, 2, 'd')
        else: return (5, val-12, 10, 2, 'p')
    return (period, 0, 0, 0, 's')

def get_config(Z):
    if Z in PERIOD6_OVERRIDES: return PERIOD6_OVERRIDES[Z]
    return aufbau(Z)

def gate_mode(Z):
    per, n_p, n_d, n_s, block = get_config(Z)
    if block == 'noble_gas': return 'sealed'
    if block == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s: return 'leak'
        elif n_d >= 9 and not has_s: return 'reflect'
        else: return 'standard'
    if block == 'p' and n_p >= 4 and per >= 3: return 'p-hole'
    return 'additive'


# ── Experimental data ─────────────────────────────────────────────────────
CONDUCTIVITY_DATA = {
    29: ('Cu', 59.6), 30: ('Zn', 16.9), 46: ('Pd', 9.5),
    47: ('Ag', 63.0), 48: ('Cd', 13.8), 79: ('Au', 45.2), 80: ('Hg', 1.04),
    21: ('Sc', 1.8), 22: ('Ti', 2.4), 23: ('V', 5.0), 24: ('Cr', 7.9),
    25: ('Mn', 0.7), 26: ('Fe', 10.0), 27: ('Co', 17.2), 28: ('Ni', 14.3),
    39: ('Y', 1.7), 40: ('Zr', 2.4), 41: ('Nb', 7.0), 42: ('Mo', 18.7),
    43: ('Tc', 6.7), 44: ('Ru', 13.7), 45: ('Rh', 21.1),
    72: ('Hf', 3.3), 73: ('Ta', 7.6), 74: ('W', 18.9), 75: ('Re', 5.4),
    76: ('Os', 12.4), 77: ('Ir', 21.3), 78: ('Pt', 9.4),
    3: ('Li', 10.8), 4: ('Be', 25.0), 11: ('Na', 21.0), 12: ('Mg', 22.7),
    13: ('Al', 37.7), 19: ('K', 14.0), 20: ('Ca', 29.8),
    37: ('Rb', 8.0), 38: ('Sr', 7.6), 55: ('Cs', 4.8), 56: ('Ba', 2.9),
    31: ('Ga', 7.1), 32: ('Ge', 0.002), 33: ('As', 3.4),
    49: ('In', 11.6), 50: ('Sn', 9.2), 51: ('Sb', 2.6),
    81: ('Tl', 6.7), 82: ('Pb', 4.8),
}


# ══════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC: What does the data actually demand?
# ══════════════════════════════════════════════════════════════════════════

def diagnostic():
    """
    Work backward from data to find what the model MUST produce.
    """
    print("="*80)
    print("  DIAGNOSTIC: What ratios does the data demand?")
    print("="*80)
    
    # 1. Within d¹⁰ family, factor out period effects
    print("\n  ── d¹⁰ FAMILY ──")
    print("  Same-period s¹/s² ratios:")
    print(f"    Cu/Zn  (P4) = {59.6/16.9:.2f}")
    print(f"    Ag/Cd  (P5) = {63.0/13.8:.2f}")
    print(f"    Au/Hg  (P6) = {45.2/1.04:.1f}  ← relativistic anomaly")
    
    print("\n  Same-mode cross-period ratios:")
    print(f"    Cu/Ag  (s¹, P4/P5) = {59.6/63.0:.3f}")
    print(f"    Zn/Cd  (s², P4/P5) = {16.9/13.8:.3f}")
    print(f"    Ag/Au  (s¹, P5/P6) = {63.0/45.2:.3f}")
    print(f"    Cd/Hg  (s², P5/P6) = {13.8/1.04:.2f} ← relativistic")
    
    # Average s¹/s² ratio (non-relativistic)
    avg_s1_s2 = (59.6/16.9 + 63.0/13.8) / 2
    print(f"\n  Average s¹/s² = {avg_s1_s2:.2f}")
    print(f"  This is close to φ² = {PHI**2:.3f}")
    print(f"  Or (1/LEAK)^(1/2) = {(1/LEAK)**0.5:.3f}")
    print(f"  Or φ²+1 = φ³ = {PHI**3:.3f} (nah)")
    
    # The s¹/s² ratio ~ 4 suggests roughly LEAK^(-0.75)
    import math
    for label, val in [("Cu/Zn", 3.53), ("Ag/Cd", 4.57), ("avg", avg_s1_s2)]:
        exponent = math.log(val) / math.log(1/LEAK)
        print(f"    {label} = {val:.2f} → (1/LEAK)^{exponent:.3f} = φ^{exponent*4:.2f}")
    
    # 2. Within standard d-block, what controls the spread?
    print("\n  ── STANDARD d-block ──")
    std_p4 = [(24,'Cr',7.9,5,1), (25,'Mn',0.7,5,2), (26,'Fe',10.0,6,2),
              (27,'Co',17.2,7,2), (28,'Ni',14.3,8,2)]
    std_p5 = [(42,'Mo',18.7,5,1), (43,'Tc',6.7,5,2), (44,'Ru',13.7,7,1),
              (45,'Rh',21.1,8,1)]
    std_p6 = [(75,'Re',5.4,5,2), (76,'Os',12.4,6,2), (77,'Ir',21.3,7,2)]
    
    print("  Period 4 standard:")
    for Z, sym, sig, nd, ns in std_p4:
        print(f"    {sym:>2} d{nd} s{ns} → {sig:>5.1f} MS/m")
    
    print("  Period 5 standard:")
    for Z, sym, sig, nd, ns in std_p5:
        print(f"    {sym:>2} d{nd} s{ns} → {sig:>5.1f} MS/m")
    
    print("  Period 6 standard:")
    for Z, sym, sig, nd, ns in std_p6:
        print(f"    {sym:>2} d{nd} s{ns} → {sig:>5.1f} MS/m")
    
    # Key observation: within standard, conductivity INCREASES with n_d
    # (away from d⁵). This is the INVERSE of θ = 1-(n_d/10)×dg
    # θ decreases with n_d, but conductivity increases!
    # → The d-electrons that COMPRESS the radius also REDUCE scattering
    
    print("\n  KEY INSIGHT: In standard mode, σ INCREASES as d-shell fills (d⁵→d⁸)")
    print("  This means fuller d-shells REDUCE scattering, not increase it.")
    print("  The radius θ measures compression; conductivity θ measures transparency.")
    print("  θ_cond = n_d/10 (filling fraction) — OPPOSITE direction to θ_radius!")
    
    # 3. s¹ vs s² within standard
    print("\n  s¹ vs s² effect in standard d-block:")
    print(f"    Cr(d5s1)/Mn(d5s2) = {7.9/0.7:.1f}  ← s¹ is 11× better at d⁵!")
    print(f"    Mo(d5s1)/Tc(d5s2) = {18.7/6.7:.1f}")
    print(f"    Ru(d7s1)/Co(d7s2) = {13.7/17.2:.2f} ← here s¹ is WORSE")
    print(f"    Rh(d8s1)/Ni(d8s2) = {21.1/14.3:.2f}")
    
    print("\n  The s¹ advantage is HUGE at d⁵ (Cr/Mn) but diminishes at d⁷-d⁸")
    print("  → Exchange blocking at d⁵ kills s² transport but not s¹")
    print("  → At d⁸, both s¹ and s² work because exchange is weak")
    
    # 4. Alkali vs alkaline earth paradox
    print("\n  ── S-BLOCK PARADOX ──")
    print(f"    Li(s1)/Be(s2) = {10.8/25.0:.2f}  — Be is BETTER")
    print(f"    Na(s1)/Mg(s2) = {21.0/22.7:.2f}  — nearly equal")
    print(f"    K(s1)/Ca(s2)  = {14.0/29.8:.2f}  — Ca is BETTER")
    print(f"    Rb(s1)/Sr(s2) = {8.0/7.6:.2f}    — roughly equal")
    print(f"    Cs(s1)/Ba(s2) = {4.8/2.9:.2f}    — Cs is better")
    
    print("\n  In s-block, s² is often BETTER than s¹!")
    print("  This is because s-block has NO d-shell — two s-electrons = more carriers")
    print("  The s² penalty only applies when d-electrons provide exchange blocking")
    print("  → n_carriers matters when there's no scattering penalty")


# ══════════════════════════════════════════════════════════════════════════
# MODEL E: Data-informed gate model
# ══════════════════════════════════════════════════════════════════════════

def conductivity_model_E(Z):
    """
    Model E: Incorporates diagnostic lessons.
    
    Key structural changes from v1:
    1. Period scaling uses φ^(-0.5×(per-3)) not φ^(-(per-2))
       — conductivity overlap falls slower than size
    2. d-shell FILLING improves conductivity (opposite of radius θ)
    3. Exchange penalty is multiplicative and centered at d⁵
    4. s¹ vs s² depends on WHETHER there's a d-shell:
       - With d-shell: s¹ >> s² (exchange blocks paired transport)
       - Without d-shell: s² ≈ s¹ (more carriers, no exchange)
    5. n_d = 10 with s¹ is the absolute maximum (clean carrier, 
       full transparent d-shell, open gate)
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    if mode == 'sealed':
        return 0.0
    
    # ── Period factor ──
    # Weaker than radius damping because conductivity depends on 
    # orbital overlap (falls as 1/r²) not size ratio (falls as 1/r)
    # Anchor at period 4 (most data), damp outward
    P = PHI ** (-0.4 * (per - 4))
    
    # ── Gate transmission ──
    if mode == 'leak':
        if n_d >= 9:
            # d¹⁰ family: the crown jewels
            d_transparency = 1.0  # Full d-shell = spherically symmetric = transparent
            
            if n_s == 1:
                # d¹⁰s¹: maximum conductivity
                # s¹ = half-filled s-band = peak DOS at Fermi level
                s_factor = PHI**2  # φ² captures the s¹ enhancement
                gate_open = LEAK
            elif n_s == 2:
                # d¹⁰s²: gate open but s-band filled
                s_factor = 1.0
                gate_open = LEAK
            else:  # n_s == 0, shouldn't happen in leak but safety
                s_factor = LEAK
                gate_open = LEAK
            
            return gate_open * s_factor * d_transparency * P
        
        else:
            # Early d-block leak (d≤4)
            # Gate is open but d-shell is partially filled → scattering
            d_fill = n_d / 10
            d_transparency = d_fill  # Empty d-shell scatters MORE
            
            # Exchange at low d-count is weak
            exchange = math.sin(math.pi * n_d / 10)**2
            exchange_penalty = 1 - exchange * DARK_GOLD
            
            if n_s == 1:
                s_factor = PHI  # Weaker than d¹⁰ because d-shell interferes
            else:
                s_factor = 1.0
            
            return LEAK * s_factor * d_transparency * exchange_penalty * P
    
    elif mode == 'reflect':
        # No s-electron. Conduction through d-band overlap only.
        # Much weaker than s-electron transport.
        d_transparency = 1.0  # d¹⁰ = transparent
        return LEAK**2 * d_transparency * P
    
    elif mode == 'standard':
        # Mid d-block (d⁵–d⁸)
        # Conductivity INCREASES with d-filling (more screening, less scattering)
        d_fill = n_d / 10
        
        # Exchange penalty peaks at d⁵ (half-filled)
        distance_from_half = abs(n_d - 5) / 5  # 0 at d⁵, 1 at d⁰/d¹⁰
        exchange = (1 - distance_from_half)**2  # Peaks at d⁵
        exchange_penalty = 1 - exchange * DARK_GOLD * PHI  # Stronger than v1
        
        if n_s == 1:
            # s¹ in standard: advantage depends on exchange
            # At d⁵: s¹ is MUCH better (exchange blocks s² but not s¹)
            # At d⁸: s¹ is only slightly better
            s_factor = PHI * (1 + exchange * PHI)  # Scales with exchange
        else:
            s_factor = 1.0
        
        # Mn special case: d⁵s² = absolute worst
        # The exchange penalty × s²-filling = double whammy
        if n_d == 5 and n_s == 2:
            s_factor *= LEAK  # Extra penalty for s² at d⁵
        
        return LEAK * s_factor * d_fill * exchange_penalty * P
    
    elif mode == 'additive':
        if block == 's':
            # S-block: no d-shell, no exchange blocking
            # s² can be as good as or better than s¹
            if n_s == 2:
                # Two carriers, no exchange penalty
                s_factor = PHI  # Slight enhancement from 2 carriers
            else:
                s_factor = 1.0  # s¹ = one clean carrier
            
            return LEAK * s_factor * P
        
        else:
            # p-block metals
            # p-electrons create some scattering
            p_scatter = 1 - n_p / 6 * DARK_GOLD
            return LEAK * p_scatter * P
    
    elif mode == 'p-hole':
        # Late p-block: holes pull inward
        p_scatter = 1 - n_p / 6 * DARK_GOLD
        return LEAK * R_C * p_scatter * P
    
    return LEAK * P


# ══════════════════════════════════════════════════════════════════════════
# MODEL F: Composite score (barrier + filling + exchange)
# ══════════════════════════════════════════════════════════════════════════

def conductivity_model_F(Z):
    """
    Model F: Three-factor decomposition.
    
    σ ∝ T_barrier × F_fill × X_exchange × P_period
    
    T = LEAK^n  (number of Cantor barriers)
    F = d-shell filling fraction (0→1, more = more transparent)
    X = exchange penalty (1 = no penalty, 0 = total block)
    P = period damping
    
    All factors expressible in terms of φ and electron counts.
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    if mode == 'sealed':
        return 0.0
    
    # Period: anchor at period 3, mild damping
    P = PHI ** (-0.5 * abs(per - 3.5))
    
    # Number of barriers
    if mode == 'leak' and n_d >= 9 and n_s == 1:
        n_bar = 0.5   # Cleanest path: half a barrier
    elif mode == 'leak' and n_d >= 9 and n_s == 2:
        n_bar = 1.0
    elif mode == 'leak' and n_d <= 4:
        n_bar = 1.5
    elif mode == 'reflect':
        n_bar = 2.5
    elif mode == 'standard':
        n_bar = 1.0
    elif mode == 'additive' and block == 's':
        n_bar = 0.75 if n_s == 2 else 1.0
    elif mode == 'additive':
        n_bar = 1.0 + n_p * 0.2
    elif mode == 'p-hole':
        n_bar = 1.5
    else:
        n_bar = 1.0
    
    T = LEAK ** n_bar
    
    # D-shell filling (transparency)
    if block == 'd':
        F = (n_d / 10) ** 0.5  # Square root: diminishing returns
    else:
        F = 1.0  # No d-shell to scatter off
    
    # Exchange penalty
    if block == 'd':
        # Peaks at d⁵, vanishes at d⁰ and d¹⁰
        half_dist = abs(n_d - 5) / 5
        X_base = 1 - (1 - half_dist)**2 * DARK_GOLD * PHI
        
        # s¹ partially evades exchange; s² gets full penalty
        if n_s == 1:
            X = 1 - (1 - X_base) * R_C  # Reduced penalty
        elif n_s == 0:
            X = X_base * R_C  # No s-electron: d-band only
        else:
            X = X_base
    else:
        X = 1.0
    
    # s-carrier enhancement for s-block
    if block == 's' and n_s == 2 and n_d == 0:
        T *= PHI  # Two carriers bonus
    
    return T * F * X * P


# ══════════════════════════════════════════════════════════════════════════
# MODEL G: Empirically-guided zero-parameter attempt
# ══════════════════════════════════════════════════════════════════════════

def conductivity_model_G(Z):
    """
    Model G: Use the RADIUS prediction error as a conductivity proxy.
    
    Insight from the paper: soft metals (positive error) are good conductors.
    Hard metals (negative error) are insulators/poor conductors.
    The error IS the gate leakage measure.
    
    σ ∝ (1 + error)^α for metals
    where error = (predicted - observed)/observed
    
    This is genuinely zero free parameters IF α = φ.
    """
    per, n_p, n_d, n_s, block = get_config(Z)
    mode = gate_mode(Z)
    
    if mode == 'sealed':
        return 0.0
    
    # Get the radius prediction
    predicted_ratio = predict_ratio(Z)
    
    # Use the predicted ratio directly as a conductivity index
    # Lower ratio = more compressed = more leakage = better conductor?
    # No: Cu has ratio 1.146 (low) and IS the best conductor
    # Pd has ratio 1.451 (high) and conducts less
    # Noble gases have ~1.7+ and don't conduct at all
    
    # Actually: the GATE OPENNESS determines conductivity
    # Leak mode ratio = 1 + LEAK = 1.146 → gate openness = LEAK
    # Reflect mode ratio = 1.451 → gate openness = ratio - BASE ≈ 0.042 (much less)
    # Standard mode: θ captures how much d-shell absorbs
    
    # Map ratio to "effective gate openness"
    if mode == 'leak':
        # Gate is open. Openness = ratio - 1 = LEAK
        openness = abs(predicted_ratio - 1)
        # The s-electron IS the carrier
        if n_s == 1 and n_d >= 9:
            carrier = PHI**2  # Half-filled s-band peak DOS
        elif n_s == 2 and n_d >= 9:
            carrier = 1.0
        elif n_s == 1:
            carrier = PHI * (n_d / 10)
        else:
            carrier = n_d / 10
    
    elif mode == 'reflect':
        # Gate shut. Only d-band overlap.
        openness = LEAK * R_C  # Residual tunneling
        carrier = 1.0
    
    elif mode == 'standard':
        theta = 1 - (n_d / 10) * DARK_GOLD
        openness = LEAK * theta
        # Exchange at d⁵ blocks transport
        exchange = math.sin(math.pi * n_d / 10)**2
        if n_s == 1:
            carrier = PHI * (1 + exchange)
        elif n_d == 5 and n_s == 2:
            carrier = LEAK  # Mn: maximum blocking
        else:
            carrier = 1.0 - exchange * LEAK
    
    elif mode == 'additive':
        openness = LEAK
        if block == 's':
            carrier = n_s  # More s-electrons = more carriers (no d-shell)
        else:
            carrier = 1.0 - n_p / 6 * LEAK
    
    elif mode == 'p-hole':
        openness = LEAK * R_C
        carrier = 1.0 - n_p / 6 * LEAK
    
    else:
        openness = LEAK
        carrier = 1.0
    
    # Period factor
    P = PHI ** (-0.4 * (per - 4))
    
    return openness * carrier * P


def predict_ratio(Z):
    per, n_p, n_d, n_s, block = get_config(Z)
    if block == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s:
            return 1 + LEAK
        elif n_d >= 9 and not has_s:
            return BASE + DARK_GOLD / PHI**4
        else:
            theta = 1 - (n_d / 10) * DARK_GOLD
            return math.sqrt(1 + (theta * BOS)**2)
    elif block == 'noble_gas':
        theta = 1 + n_p * (G1 / BOS) * PHI**(-(per-1))
        return math.sqrt(1 + (theta * BOS)**2)
    else:
        ratio = BASE + n_p * G1 * PHI**(-(per-1))
        if block == 'p' and n_p >= 4 and per >= 3:
            ratio *= (1 - LEAK)
        return ratio


# ══════════════════════════════════════════════════════════════════════════
# TEST HARNESS
# ══════════════════════════════════════════════════════════════════════════

def rank_list(vals):
    indexed = sorted(enumerate(vals), key=lambda x: x[1])
    ranks = [0] * len(vals)
    for rank, (idx, _) in enumerate(indexed, 1):
        ranks[idx] = rank
    return ranks

def test_model(model_func, model_name, data):
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
    
    nonzero = [(Z,s,se,sp,m,p,nd,ns,b) for Z,s,se,sp,m,p,nd,ns,b in results if sp > 0 and se > 0.001]
    
    if not nonzero:
        print("No non-zero predictions!")
        return None
    
    log_ratios = [math.log(se/sp) for _,_,se,sp,_,_,_,_,_ in nonzero]
    log_sigma0 = sum(log_ratios) / len(log_ratios)
    sigma0 = math.exp(log_sigma0)
    
    print(f"\n  σ₀ = {sigma0:.2f}")
    print()
    
    print(f"  {'Z':>3} {'Sym':>3} {'Mode':<10} {'Per':>3} {'n_d':>3} {'n_s':>3} "
          f"{'σ_exp':>8} {'σ_pred':>8} {'Ratio':>7} {'|lgE|':>6}")
    print(f"  {'-'*70}")
    
    log_errors = []
    abs_ratios = []
    
    for Z, sym, se, sp_raw, mode, per, nd, ns, block in results:
        sp = sp_raw * sigma0
        if sp > 0 and se > 0.001:
            ratio = se / sp
            log_err = abs(math.log10(ratio))
            log_errors.append(log_err)
            abs_ratios.append(ratio)
            flag = " ← MISS" if log_err > 0.5 else (" ★" if log_err < 0.1 else "")
            print(f"  {Z:>3} {sym:>3} {mode:<10} {per:>3} {nd:>3} {ns:>3} "
                  f"{se:>8.2f} {sp:>8.2f} {ratio:>7.2f} {log_err:>6.3f}{flag}")
        else:
            print(f"  {Z:>3} {sym:>3} {mode:<10} {per:>3} {nd:>3} {ns:>3} "
                  f"{se:>8.3f} {sp*sigma0 if sp > 0 else 0:>8.3f} {'skip':>7}")
    
    if log_errors:
        mean_log = sum(log_errors) / len(log_errors)
        within_2x = sum(1 for r in abs_ratios if 0.5 <= r <= 2.0)
        within_3x = sum(1 for r in abs_ratios if 0.33 <= r <= 3.0)
        within_5x = sum(1 for r in abs_ratios if 0.2 <= r <= 5.0)
        n = len(abs_ratios)
        
        exp_vals = [se for _,_,se,_,_,_,_,_,_ in nonzero]
        pred_vals = [sp*sigma0 for _,_,_,sp,_,_,_,_,_ in nonzero]
        exp_rank = rank_list(exp_vals)
        pred_rank = rank_list(pred_vals)
        n_r = len(exp_rank)
        d_sq = sum((e-p)**2 for e,p in zip(exp_rank, pred_rank))
        rho = 1 - 6*d_sq/(n_r*(n_r**2-1))
        
        # Pearson correlation in log space
        log_exp = [math.log(se) for _,_,se,_,_,_,_,_,_ in nonzero]
        log_pred = [math.log(sp*sigma0) for _,_,_,sp,_,_,_,_,_ in nonzero]
        mean_le = sum(log_exp)/n_r
        mean_lp = sum(log_pred)/n_r
        cov = sum((e-mean_le)*(p-mean_lp) for e,p in zip(log_exp, log_pred))/n_r
        std_e = (sum((e-mean_le)**2 for e in log_exp)/n_r)**0.5
        std_p = (sum((p-mean_lp)**2 for p in log_pred)/n_r)**0.5
        r_pearson = cov/(std_e*std_p) if std_e > 0 and std_p > 0 else 0
        
        print(f"\n  ── Summary ──")
        print(f"  Elements:          {n}")
        print(f"  Mean |log₁₀ err|:  {mean_log:.3f}")
        print(f"  Within 2×:         {within_2x}/{n} ({100*within_2x/n:.0f}%)")
        print(f"  Within 3×:         {within_3x}/{n} ({100*within_3x/n:.0f}%)")
        print(f"  Within 5×:         {within_5x}/{n} ({100*within_5x/n:.0f}%)")
        print(f"  Spearman ρ:        {rho:.3f}")
        print(f"  Pearson r (log):   {r_pearson:.3f}")
        
        return (sigma0, mean_log, within_2x/n, rho, r_pearson)
    return None


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    diagnostic()
    
    print(f"\n\n{'#'*80}")
    print(f"#  REFINED MODEL COMPARISON (v2)")
    print(f"{'#'*80}")
    
    models = [
        (conductivity_model_E, "Model E: Data-informed gate model"),
        (conductivity_model_F, "Model F: Three-factor (barrier×fill×exchange)"),
        (conductivity_model_G, "Model G: Radius-linked gate openness"),
    ]
    
    summary = []
    for func, name in models:
        result = test_model(func, name, CONDUCTIVITY_DATA)
        if result:
            summary.append((name, *result))
    
    print(f"\n\n{'='*80}")
    print(f"  FINAL COMPARISON (v2)")
    print(f"{'='*80}")
    print(f"\n  {'Model':<48} {'σ₀':>7} {'|lg|':>5} {'2×':>5} {'ρ':>6} {'r':>6}")
    print(f"  {'-'*48} {'-'*7} {'-'*5} {'-'*5} {'-'*6} {'-'*6}")
    for name, s0, ml, w2, rho, r_p in summary:
        print(f"  {name:<48} {s0:>7.1f} {ml:>5.3f} {w2:>4.0%} {rho:>6.3f} {r_p:>6.3f}")
    
    print(f"\n  Key:")
    print(f"  σ₀ = single calibration constant (MS/m)")
    print(f"  |lg| = mean |log₁₀ error| (lower is better)")
    print(f"  2× = fraction within factor of 2")
    print(f"  ρ = Spearman rank correlation (does ordering match?)")
    print(f"  r = Pearson correlation in log-space (does magnitude track?)")
    
    # Best/worst analysis for the winning model
    print(f"\n\n{'='*80}")
    print(f"  BEST/WORST ELEMENTS (Model with best rank correlation)")
    print(f"{'='*80}")
    
    # Find best model by rho
    best = max(summary, key=lambda x: x[4])  # by rho
    print(f"  Winner: {best[0]}")
    
    # Re-run to get details
    best_func = models[[s[0] for s in summary].index(best[0])][0]
    
    results_detail = []
    for Z in sorted(CONDUCTIVITY_DATA.keys()):
        sym, se = CONDUCTIVITY_DATA[Z]
        if se < 0.001: continue
        sp_raw = best_func(Z)
        if sp_raw <= 0: continue
        sp = sp_raw * best[1]
        ratio = se / sp
        log_err = abs(math.log10(ratio))
        results_detail.append((Z, sym, se, sp, ratio, log_err, gate_mode(Z)))
    
    results_detail.sort(key=lambda x: x[5])
    
    print(f"\n  TOP 10 (closest to experiment):")
    for Z, sym, se, sp, ratio, le, mode in results_detail[:10]:
        print(f"    {sym:>2} (Z={Z:>2}) {mode:<10}  exp={se:>6.1f}  pred={sp:>6.1f}  ratio={ratio:.2f}")
    
    print(f"\n  BOTTOM 10 (furthest from experiment):")
    for Z, sym, se, sp, ratio, le, mode in results_detail[-10:]:
        print(f"    {sym:>2} (Z={Z:>2}) {mode:<10}  exp={se:>6.1f}  pred={sp:>6.1f}  ratio={ratio:.2f}")
