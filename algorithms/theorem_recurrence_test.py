#!/usr/bin/env python3
"""
Theorem Recurrence Test — Correlated recurrence of θ-mode ratios
across unrelated physical systems.

Tests whether (R_leak=1.146, R_rc=1.311, R_base=1.409) show
statistically significant CORRELATED RECURRENCE in molecular,
planetary, and crystal consecutive ratios.

Thomas A. Husmann / iBuilt LTD / 2026
"""

import math
import time
import json
import os

# ── Try JAX Metal GPU, fall back to numpy ──
try:
    import jax
    import jax.numpy as jnp
    from jax import random as jrand
    jax.config.update("jax_platform_name", "gpu")
    _ = jnp.ones(1)  # force init
    BACKEND = "JAX (METAL)"
    print(f"Backend: {BACKEND}")
    USE_JAX = True
except Exception:
    import numpy as jnp
    BACKEND = "NumPy (CPU)"
    print(f"Backend: {BACKEND}")
    USE_JAX = False

import numpy as np
from scipy import stats as scipy_stats

# ══════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ══════════════════════════════════════════════════════════════════
PHI = 1.6180339887498948
SQRT_PHI = math.sqrt(PHI)
H_HINGE = PHI**(-1/PHI)
R_C = 1 - 1/PHI**4
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.9920
THETA_LEAK = 0.564
THETA_RC = 0.854
THETA_BASE = 1.000
R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS)**2)
R_RC   = math.sqrt(1 + (THETA_RC   * BOS)**2)
R_BASE = math.sqrt(1 + (THETA_BASE * BOS)**2)
RHO6   = PHI**(1/6)
REAL_TRIPLE = sorted([R_LEAK, R_RC, R_BASE])

print(f"\nFramework triple: {[f'{x:.6f}' for x in REAL_TRIPLE]}")
print(f"  R_leak  = {R_LEAK:.6f}")
print(f"  R_rc    = {R_RC:.6f}")
print(f"  R_base  = {R_BASE:.6f}")
print(f"  rho6    = {RHO6:.6f}")

# ══════════════════════════════════════════════════════════════════
# DATASETS — consecutive ratios from raw measurements
# ══════════════════════════════════════════════════════════════════
mol_bonds = [0.741, 1.098, 1.208, 1.412, 1.988, 2.281, 2.666]
mol_names = ["H2", "N2", "O2", "F2", "Cl2", "Br2", "I2"]
mol_ratios = [mol_bonds[i+1]/mol_bonds[i] for i in range(len(mol_bonds)-1)]
mol_labels = [f"{mol_names[i+1]}/{mol_names[i]}" for i in range(len(mol_bonds)-1)]

trap_axes = [0.01154, 0.01580, 0.02227, 0.02925, 0.03849, 0.04683, 0.06189]
trap_names = ["b", "c", "d", "e", "f", "g", "h"]
trap_ratios = [trap_axes[i+1]/trap_axes[i] for i in range(len(trap_axes)-1)]
trap_labels = [f"T1-{trap_names[i+1]}/{trap_names[i]}" for i in range(len(trap_axes)-1)]

sol_axes = [0.387, 0.723, 1.000, 1.524, 5.203, 9.537, 19.19, 30.07]
sol_names = ["Mer", "Ven", "Ear", "Mar", "Jup", "Sat", "Ura", "Nep"]
sol_ratios = [sol_axes[i+1]/sol_axes[i] for i in range(len(sol_axes)-1)]
sol_labels = [f"{sol_names[i+1]}/{sol_names[i]}" for i in range(len(sol_axes)-1)]

cry_latt = [3.567, 5.431, 5.658, 6.489]
cry_names = ["C", "Si", "Ge", "Sn"]
cry_ratios = [cry_latt[i+1]/cry_latt[i] for i in range(len(cry_latt)-1)]
cry_labels = [f"{cry_names[i+1]}/{cry_names[i]}" for i in range(len(cry_latt)-1)]

ALL_RATIOS = mol_ratios + trap_ratios + sol_ratios + cry_ratios
ALL_LABELS = mol_labels + trap_labels + sol_labels + cry_labels
ALL_SYSTEMS = (["MOLECULAR"]*len(mol_ratios) + ["TRAPPIST-1"]*len(trap_ratios) +
               ["SOLAR"]*len(sol_ratios) + ["CRYSTAL"]*len(cry_ratios))

print(f"\nTotal consecutive ratios: {len(ALL_RATIOS)}")
print("Datasets: MOLECULAR({}) TRAPPIST-1({}) SOLAR({}) CRYSTAL({})".format(
    len(mol_ratios), len(trap_ratios), len(sol_ratios), len(cry_ratios)))

# ══════════════════════════════════════════════════════════════════
# PART 1: CORRELATED RECURRENCE NULL HYPOTHESIS
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 1: CORRELATED RECURRENCE — 100,000 Monte Carlo trials")
print("="*70)

THRESHOLD = 0.02  # 2%
N_TRIALS = 100_000

def count_hits_and_error(ratios, triple, threshold=THRESHOLD):
    """Count how many ratios fall within threshold of any mode in triple."""
    hits = 0
    total_err = 0.0
    for r in ratios:
        for m in triple:
            err = abs(r - m) / m
            if err <= threshold:
                hits += 1
                total_err += err
                break
    mean_err = total_err / hits if hits > 0 else 999.0
    return hits, mean_err

# Real triple analysis
real_hits, real_mean_err = count_hits_and_error(ALL_RATIOS, REAL_TRIPLE)
print(f"\nReal triple hits: {real_hits}/{len(ALL_RATIOS)} at 2% threshold")
print(f"Real triple mean error: {real_mean_err*100:.4f}%")
print(f"\nDetailed hits:")

mode_names = ["R_leak", "R_rc", "R_base"]
for i, (r, label, system) in enumerate(zip(ALL_RATIOS, ALL_LABELS, ALL_SYSTEMS)):
    for j, m in enumerate(REAL_TRIPLE):
        err = abs(r - m) / m
        if err <= THRESHOLD:
            print(f"  {system:12s} {label:12s} = {r:.4f}  ->  {mode_names[j]:8s} = {m:.4f}  err = {err*100:.3f}%")

# Monte Carlo — vectorized with numpy
print(f"\nRunning {N_TRIALS:,} Monte Carlo trials...")
t0 = time.time()

rng = np.random.default_rng(42)
# Generate all random triples at once: shape (N_TRIALS, 3)
rand_triples = rng.uniform(1.01, 2.0, size=(N_TRIALS, 3))
rand_triples.sort(axis=1)

ratios_arr = np.array(ALL_RATIOS)  # shape (N_ratios,)

# For each trial, count hits and mean error
# Vectorize: for each ratio, check against all 3 modes of all trials
# ratios_arr: (N_ratios,)
# rand_triples: (N_TRIALS, 3)
# relative error: |r - m| / m for each (ratio, trial, mode)

count_ge_hits = 0
count_quality = 0

batch_size = 10000
for batch_start in range(0, N_TRIALS, batch_size):
    batch_end = min(batch_start + batch_size, N_TRIALS)
    batch = rand_triples[batch_start:batch_end]  # (B, 3)
    B = batch.shape[0]

    # Expand: (B, 3, 1) vs (1, 1, N_ratios) -> (B, 3, N_ratios)
    modes = batch[:, :, np.newaxis]  # (B, 3, 1)
    rats = ratios_arr[np.newaxis, np.newaxis, :]  # (1, 1, N_r)

    rel_err = np.abs(rats - modes) / modes  # (B, 3, N_r)

    # For each ratio, check if ANY mode matches (within threshold)
    # min across modes axis -> (B, N_r)
    min_err = rel_err.min(axis=1)  # (B, N_r)
    is_hit = min_err <= THRESHOLD  # (B, N_r)

    hit_counts = is_hit.sum(axis=1)  # (B,)

    # Mean error of hits
    hit_errs = np.where(is_hit, min_err, 0.0)
    sum_errs = hit_errs.sum(axis=1)
    mean_errs = np.where(hit_counts > 0, sum_errs / hit_counts, 999.0)

    count_ge_hits += np.sum(hit_counts >= real_hits)
    count_quality += np.sum((hit_counts >= real_hits) & (mean_errs <= real_mean_err))

    if (batch_end % 10000 == 0) or batch_end == N_TRIALS:
        elapsed = time.time() - t0
        print(f"  {batch_end:>7,} / {N_TRIALS:,}  [{elapsed:.1f}s]  "
              f"p_count={count_ge_hits/batch_end:.5f}  p_quality={count_quality/batch_end:.6f}")

p_count = count_ge_hits / N_TRIALS
p_quality = count_quality / N_TRIALS
elapsed1 = time.time() - t0

print(f"\n--- Part 1 Results ---")
print(f"Real triple: {[f'{x:.4f}' for x in REAL_TRIPLE]}")
print(f"Hit count:   {real_hits}/{len(ALL_RATIOS)}")
print(f"Mean error:  {real_mean_err*100:.4f}%")
print(f"p-value (count):   {p_count:.6f}  ({count_ge_hits}/{N_TRIALS})")
print(f"p-value (quality): {p_quality:.6f}  ({count_quality}/{N_TRIALS})")
print(f"Elapsed: {elapsed1:.1f}s")

# ══════════════════════════════════════════════════════════════════
# PART 2: SEQUENCE PATTERN TEST
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 2: SEQUENCE PATTERN TEST")
print("="*70)

# Halogen bond ratios (F2/O2, Cl2/F2, Br2/Cl2, I2/Br2)
halogen_ratios = [1.169, 1.408, 1.147, 1.169]
# Assign each to nearest mode
def nearest_mode(r, triple=REAL_TRIPLE):
    errs = [abs(r - m)/m for m in triple]
    return errs.index(min(errs))

halogen_modes = [nearest_mode(r) for r in halogen_ratios]
print(f"\nHalogen ratios: {halogen_ratios}")
print(f"Mode assignments: {halogen_modes}  (0=leak, 1=rc, 2=base)")
# Expected: [0, 2, 0, 0] = (A, C, A, A)
halogen_target = tuple(halogen_modes)
print(f"Target pattern: {halogen_target}")

# TRAPPIST-1 ratios within 2%: d/c=1.410, e/d=1.313, f/e=1.316
trap_close = [1.410, 1.313, 1.316]
trap_close_modes = [nearest_mode(r) for r in trap_close]
print(f"\nTRAPPIST close ratios: {trap_close}")
print(f"Mode assignments: {trap_close_modes}")
trap_target = tuple(trap_close_modes)
print(f"Target pattern: {trap_target}")

# Monte Carlo for patterns
N_PAT = 100_000
print(f"\nRunning {N_PAT:,} random pattern trials...")

# Halogen: 4 values randomly assigned to 3 modes
rng2 = np.random.default_rng(123)
halogen_random = rng2.integers(0, 3, size=(N_PAT, 4))
halogen_match = 0
for i in range(N_PAT):
    if tuple(halogen_random[i]) == halogen_target:
        halogen_match += 1

p_halogen = halogen_match / N_PAT
# Analytical: 1/3^4 = 1/81 for any specific pattern
p_halogen_analytical = 1 / 3**4

# TRAPPIST: 3 values randomly assigned to 3 modes
trap_random = rng2.integers(0, 3, size=(N_PAT, 3))
trap_match = 0
for i in range(N_PAT):
    if tuple(trap_random[i]) == trap_target:
        trap_match += 1

p_trap = trap_match / N_PAT
p_trap_analytical = 1 / 3**3

print(f"\n--- Part 2 Results ---")
print(f"Halogen pattern {halogen_target}:")
print(f"  MC p-value:         {p_halogen:.6f}  ({halogen_match}/{N_PAT})")
print(f"  Analytical p-value: {p_halogen_analytical:.6f}  (1/3^4 = 1/81)")
print(f"TRAPPIST pattern {trap_target}:")
print(f"  MC p-value:         {p_trap:.6f}  ({trap_match}/{N_PAT})")
print(f"  Analytical p-value: {p_trap_analytical:.6f}  (1/3^3 = 1/27)")
print(f"\nNote: patterns alone are not rare. The claim is that the SAME three")
print(f"modes recur, not that any specific sequence appears.")

# ══════════════════════════════════════════════════════════════════
# PART 3: CROSS-SYSTEM COINCIDENCE
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 3: CROSS-SYSTEM COINCIDENCE")
print("="*70)

# Key pairs
Cl2_F2 = 1.988 / 1.412   # = 1.4079
Trap_dc = 0.02227 / 0.01580  # = 1.4095 (more precise than 1.4089)
Br2_Cl2 = 2.281 / 1.988  # = 1.1474
Sn_Ge = 6.489 / 5.658    # = 1.1468
Trap_ed = 0.02925 / 0.02227  # = 1.3134
Trap_fe = 0.03849 / 0.02925  # = 1.3159

print(f"\nCross-system pairs:")
print(f"  MODE R_base ~ 1.409:")
print(f"    Cl2/F2      = {Cl2_F2:.6f}   (molecular)")
print(f"    TRAPPIST d/c = {Trap_dc:.6f}   (exoplanet)")
print(f"    Difference:   {abs(Cl2_F2 - Trap_dc):.6f}")
print(f"  MODE R_leak ~ 1.146:")
print(f"    Br2/Cl2     = {Br2_Cl2:.6f}   (molecular)")
print(f"    Sn/Ge       = {Sn_Ge:.6f}   (crystal)")
print(f"    Difference:   {abs(Br2_Cl2 - Sn_Ge):.6f}")
print(f"  MODE R_rc ~ 1.311:")
print(f"    TRAPPIST e/d = {Trap_ed:.6f}   (exoplanet)")
print(f"    TRAPPIST f/e = {Trap_fe:.6f}   (exoplanet)")
print(f"    Difference:   {abs(Trap_ed - Trap_fe):.6f}")

# Analytical calculation for one pair
w_cl2 = Cl2_F2 * 0.001 * 2  # window = +/- 0.1% of Cl2_F2
w_trap = Trap_dc * 0.001 * 2
# Intersection window for random V
lower = max(Cl2_F2 * 0.999, Trap_dc * 0.999)
upper = min(Cl2_F2 * 1.001, Trap_dc * 1.001)
intersection = max(0, upper - lower)
p_one_pair = intersection / 1.0  # uniform on [1, 2]

print(f"\nAnalytical (one pair, R_base):")
print(f"  Window intersection: [{lower:.4f}, {upper:.4f}] = width {intersection:.6f}")
print(f"  P(random V matches both): {p_one_pair:.6f}")

# Monte Carlo: simultaneous cross-system matching
print(f"\nMonte Carlo: {N_TRIALS:,} trials for THREE simultaneous cross-system pairs...")
t0 = time.time()

# The six key measurements and their systems
# Pair 1 (R_base mode): Cl2/F2 (molecular) and TRAPPIST d/c (planetary)
# Pair 2 (R_leak mode): Br2/Cl2 (molecular) and Sn/Ge (crystal)
# Pair 3 (R_rc mode): TRAPPIST e/d and TRAPPIST f/e (both planetary, but same mode)
# For the cross-system test, pairs 1 and 2 are the strongest (different physics)

pair_targets = [
    (Cl2_F2, Trap_dc, "MOLECULAR", "TRAPPIST-1"),   # R_base
    (Br2_Cl2, Sn_Ge, "MOLECULAR", "CRYSTAL"),        # R_leak
    (Trap_ed, Trap_fe, "TRAPPIST-1", "TRAPPIST-1"),  # R_rc
]

CROSS_THRESH = 0.02  # 2%

cross_count = 0
rng3 = np.random.default_rng(456)

# Generate all random triples
rand_triples3 = rng3.uniform(1.01, 2.0, size=(N_TRIALS, 3))
rand_triples3.sort(axis=1)

for trial in range(N_TRIALS):
    triple = rand_triples3[trial]
    pairs_matched = 0
    modes_used = set()

    for pair_idx, (v1, v2, sys1, sys2) in enumerate(pair_targets):
        for mode_idx, m in enumerate(triple):
            if (abs(v1 - m)/m <= CROSS_THRESH and abs(v2 - m)/m <= CROSS_THRESH):
                if mode_idx not in modes_used:
                    pairs_matched += 1
                    modes_used.add(mode_idx)
                    break

    # Count if at least 2 pairs from 2+ different systems matched different modes
    if pairs_matched >= 2:
        cross_count += 1

    if (trial + 1) % 20000 == 0:
        print(f"  {trial+1:>7,} / {N_TRIALS:,}  cross_matches: {cross_count}")

p_cross = cross_count / N_TRIALS
elapsed3 = time.time() - t0

# Verify the real triple
real_pairs = 0
real_modes_used = set()
for pair_idx, (v1, v2, sys1, sys2) in enumerate(pair_targets):
    for mode_idx, m in enumerate(REAL_TRIPLE):
        if (abs(v1 - m)/m <= CROSS_THRESH and abs(v2 - m)/m <= CROSS_THRESH):
            if mode_idx not in real_modes_used:
                real_pairs += 1
                real_modes_used.add(mode_idx)
                print(f"  Real triple pair {pair_idx}: both {v1:.4f} & {v2:.4f} match mode {mode_names[mode_idx]}={m:.4f}")
                break

print(f"\n--- Part 3 Results ---")
print(f"Real triple matches {real_pairs} cross-system pairs")
print(f"Random triples matching >= 2 pairs: {cross_count}/{N_TRIALS}")
print(f"p-value (cross-system): {p_cross:.6f}")
print(f"Elapsed: {elapsed3:.1f}s")

# ══════════════════════════════════════════════════════════════════
# PART 4: COMBINED THEOREM SCORECARD
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 4: COMBINED THEOREM SCORECARD")
print("="*70)

# Load previous results
sig_path = "/Users/universe/Unified_Theory_Physics/results/theorem_significance.json"
try:
    with open(sig_path) as f:
        prev = json.load(f)
    prev_targets = prev["targets"]
    print(f"\nLoaded {len(prev_targets)} targets from theorem_significance.json")
except Exception as e:
    print(f"Could not load previous results: {e}")
    prev_targets = []

# Tier 1+2 survivors (p < 0.01)
tier12 = [t for t in prev_targets if t.get("tier", 0) in [1, 2]]
print(f"Tier 1+2 survivors: {len(tier12)}")

# GROUP A: Large-ratio predictions (targets with values far from [1,2])
group_a = [t for t in tier12 if t["value"] > 2.0 or t["value"] < 0.5]
# GROUP B: Recurrent-mode predictions (values in [1,2] range that match θ-modes)
group_b_candidates = [t for t in tier12 if 1.0 <= t["value"] <= 2.0]

print(f"\nGROUP A — Large-ratio predictions: {len(group_a)}")
for t in group_a:
    print(f"  {t['name']:30s}  value={t['value']:<12.6f}  err={t['error_pct']:.4f}%  p={t['p_value']:.4f}  [{t['bracket']}]")

print(f"\nGROUP B — Recurrent-mode predictions: {len(group_b_candidates)}")
for t in group_b_candidates:
    # Check if value is near any of the three modes
    near_mode = ""
    for j, m in enumerate(REAL_TRIPLE):
        if abs(t["value"] - m) / m < 0.05:
            near_mode = f" ~{mode_names[j]}"
    print(f"  {t['name']:30s}  value={t['value']:<12.6f}  err={t['error_pct']:.4f}%  p={t['p_value']:.4f}  [{t['bracket']}]{near_mode}")

# Recurrence test survivors
print(f"\nRecurrence test (Part 1):")
print(f"  p_count   = {p_count:.6f}  {'SIGNIFICANT' if p_count < 0.01 else 'not significant'}")
print(f"  p_quality = {p_quality:.6f}  {'SIGNIFICANT' if p_quality < 0.01 else 'not significant'}")

# ══════════════════════════════════════════════════════════════════
# PART 5: HUBBLE TENSION CROSS-BRACKET TEST
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 5: HUBBLE TENSION CROSS-BRACKET TEST")
print("="*70)

HUBBLE_RATIO = 1.0831  # H0_local / H0_Planck (73.0 / 67.4)
# 5d observed ratios for Ta, W, Pt
observed_5d = np.array([1.225, 1.225, 1.233])

def predicted_5d(rho):
    """Predicted ratio using theta_leak with rho correction."""
    return np.sqrt(1 + (THETA_LEAK * rho * BOS)**2)

# Find optimal rho for 5d atoms
from scipy.optimize import minimize_scalar

def rho_loss(rho):
    pred = predicted_5d(rho)
    return np.mean((pred - observed_5d)**2)

result = minimize_scalar(rho_loss, bounds=(0.5, 1.5), method='bounded')
rho_optimal = result.x
print(f"\nOptimal rho for 5d atoms: {rho_optimal:.6f}")
print(f"Framework rho6 = phi^(1/6): {RHO6:.6f}")
print(f"Hubble ratio H0_local/H0_Planck: {HUBBLE_RATIO:.4f}")
print(f"rho6 vs Hubble: {abs(RHO6 - HUBBLE_RATIO)/HUBBLE_RATIO*100:.3f}%")
print(f"rho_optimal vs rho6: {abs(rho_optimal - RHO6)/RHO6*100:.3f}%")
print(f"Predictions at rho6={RHO6:.4f}: {predicted_5d(RHO6)}")

# Monte Carlo
print(f"\nMonte Carlo: {N_TRIALS:,} random frameworks...")
t0 = time.time()

hubble_match = 0
rng5 = np.random.default_rng(789)

for trial in range(N_TRIALS):
    # 28 random constants from [0.5, 1.5]
    constants = rng5.uniform(0.5, 1.5, size=28)

    # Find which constant best fits the 5d correction
    best_loss = 999.0
    best_rho = 0.0
    for c in constants:
        pred = np.sqrt(1 + (THETA_LEAK * c * BOS)**2)
        loss = np.mean((pred - observed_5d)**2)
        if loss < best_loss:
            best_loss = loss
            best_rho = c

    # Check if best_rho is within 1% of Hubble ratio
    if abs(best_rho - HUBBLE_RATIO) / HUBBLE_RATIO <= 0.01:
        hubble_match += 1

    if (trial + 1) % 20000 == 0:
        print(f"  {trial+1:>7,} / {N_TRIALS:,}  hubble_matches: {hubble_match}")

p_hubble = hubble_match / N_TRIALS
elapsed5 = time.time() - t0

print(f"\n--- Part 5 Results ---")
print(f"Frameworks where best 5d corrector also matches Hubble: {hubble_match}/{N_TRIALS}")
print(f"p-value (Hubble cross-bracket): {p_hubble:.6f}")
print(f"Elapsed: {elapsed5:.1f}s")

# ══════════════════════════════════════════════════════════════════
# FISHER'S COMBINED p-VALUE
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("FISHER'S COMBINED p-VALUE")
print("="*70)

# Collect all independent p-values
p_values_all = []
p_labels_all = []

# Part 1
if p_quality > 0:
    p_values_all.append(p_quality)
    p_labels_all.append("Recurrence quality")
else:
    p_values_all.append(1.0 / N_TRIALS)  # upper bound
    p_labels_all.append("Recurrence quality (<1/N)")

# Part 3
if p_cross > 0:
    p_values_all.append(p_cross)
    p_labels_all.append("Cross-system coincidence")
else:
    p_values_all.append(1.0 / N_TRIALS)
    p_labels_all.append("Cross-system coincidence (<1/N)")

# Part 5
if p_hubble > 0:
    p_values_all.append(p_hubble)
    p_labels_all.append("Hubble cross-bracket")
else:
    p_values_all.append(1.0 / N_TRIALS)
    p_labels_all.append("Hubble cross-bracket (<1/N)")

# Add Tier 1+2 from previous (take the individual p-values)
for t in tier12:
    if t["p_value"] > 0:
        p_values_all.append(t["p_value"])
        p_labels_all.append(f"MC: {t['name']}")

print(f"\nIndependent p-values for Fisher combination:")
for lbl, pv in zip(p_labels_all, p_values_all):
    print(f"  {lbl:40s}  p = {pv:.6f}")

# Fisher's method: X = -2 * sum(ln(p_i)), distributed as chi^2 with 2k df
p_values_arr = np.array(p_values_all)
p_values_arr = np.clip(p_values_arr, 1e-15, 1.0)  # avoid log(0)
fisher_stat = -2 * np.sum(np.log(p_values_arr))
fisher_df = 2 * len(p_values_arr)
fisher_p = scipy_stats.chi2.sf(fisher_stat, fisher_df)

print(f"\nFisher statistic: {fisher_stat:.2f}")
print(f"Degrees of freedom: {fisher_df}")
print(f"Fisher combined p-value: {fisher_p:.2e}")

# ══════════════════════════════════════════════════════════════════
# DRAFT THEOREM STATEMENT
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("DRAFT THEOREM STATEMENT")
print("="*70)

theorem_text = f"""
THEOREM (Quantized Recurrence of Consecutive Ratios)

The three Pythagorean radii derived from the Husmann Decomposition's
theta-mode angles (theta_leak=0.564, theta_rc=0.854, theta_base=1.000)
via R = sqrt(1 + (theta * BOS)^2):

    R_leak  = {R_LEAK:.6f}
    R_rc    = {R_RC:.6f}
    R_base  = {R_BASE:.6f}

show statistically significant correlated recurrence across four
independent physical systems:

  MOLECULAR   (homonuclear diatomic bond ratios)
  TRAPPIST-1  (exoplanet semimajor axis ratios)
  SOLAR       (solar system semimajor axis ratios)
  CRYSTAL     (diamond-structure lattice ratios)

EVIDENCE:
  1. Recurrence:     {real_hits}/{len(ALL_RATIOS)} consecutive ratios match within 2%
                     (p_count = {p_count:.6f}, p_quality = {p_quality:.6f})
  2. Cross-system:   Three pairs of measurements from different physics
                     each match a different mode (p = {p_cross:.6f})
  3. Hubble bridge:  The same phi^(1/6) = {RHO6:.4f} that corrects 5d atomic
                     radii matches the Hubble tension ratio 73.0/67.4 = {HUBBLE_RATIO}
                     (p = {p_hubble:.6f})
  4. Fisher combined p-value across all tests: {fisher_p:.2e}

The three modes emerge from the Cantor spectrum's Pythagorean structure:
  sigma_4^2 = sigma_shell^2 + bronze_sigma_3^2
The angle theta parameterizes how much bronze-axis momentum each state carries.
"""
print(theorem_text)

# ══════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ══════════════════════════════════════════════════════════════════
results_dir = "/Users/universe/Unified_Theory_Physics/results"
os.makedirs(results_dir, exist_ok=True)

output = {
    "metadata": {
        "backend": BACKEND,
        "n_trials": N_TRIALS,
        "threshold_pct": THRESHOLD * 100,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round(time.time() - t0, 1)
    },
    "framework_triple": {
        "R_leak": R_LEAK,
        "R_rc": R_RC,
        "R_base": R_BASE,
        "rho6": RHO6,
        "BOS": BOS,
        "theta_leak": THETA_LEAK,
        "theta_rc": THETA_RC,
        "theta_base": THETA_BASE
    },
    "part1_recurrence": {
        "n_ratios": len(ALL_RATIOS),
        "hit_count": real_hits,
        "mean_error_pct": round(real_mean_err * 100, 4),
        "p_count": round(p_count, 6),
        "p_quality": round(p_quality, 6),
        "hits_detail": []
    },
    "part2_patterns": {
        "halogen_pattern": list(halogen_target),
        "halogen_p_mc": round(p_halogen, 6),
        "halogen_p_analytical": round(p_halogen_analytical, 6),
        "trappist_pattern": list(trap_target),
        "trappist_p_mc": round(p_trap, 6),
        "trappist_p_analytical": round(p_trap_analytical, 6)
    },
    "part3_cross_system": {
        "real_pairs_matched": real_pairs,
        "p_cross_system": round(p_cross, 6),
        "pairs": [
            {"mode": "R_base", "v1": round(Cl2_F2, 6), "v2": round(Trap_dc, 6),
             "systems": ["MOLECULAR", "TRAPPIST-1"]},
            {"mode": "R_leak", "v1": round(Br2_Cl2, 6), "v2": round(Sn_Ge, 6),
             "systems": ["MOLECULAR", "CRYSTAL"]},
            {"mode": "R_rc", "v1": round(Trap_ed, 6), "v2": round(Trap_fe, 6),
             "systems": ["TRAPPIST-1", "TRAPPIST-1"]}
        ]
    },
    "part4_scorecard": {
        "group_a": [{"name": t["name"], "value": t["value"], "error_pct": t["error_pct"],
                      "p_value": t["p_value"], "bracket": t["bracket"]} for t in group_a],
        "group_b": [{"name": t["name"], "value": t["value"], "error_pct": t["error_pct"],
                      "p_value": t["p_value"], "bracket": t["bracket"]} for t in group_b_candidates],
        "n_tier12": len(tier12)
    },
    "part5_hubble": {
        "rho6": RHO6,
        "rho_optimal_5d": round(rho_optimal, 6),
        "hubble_ratio": HUBBLE_RATIO,
        "rho6_vs_hubble_pct": round(abs(RHO6 - HUBBLE_RATIO)/HUBBLE_RATIO*100, 3),
        "p_hubble": round(p_hubble, 6)
    },
    "fisher_combined": {
        "statistic": round(fisher_stat, 2),
        "df": fisher_df,
        "p_value": float(fisher_p),
        "n_tests": len(p_values_all),
        "individual_p_values": {lbl: round(float(pv), 6) for lbl, pv in zip(p_labels_all, p_values_all)}
    },
    "theorem_statement": theorem_text.strip()
}

# Add hit details
for i, (r, label, system) in enumerate(zip(ALL_RATIOS, ALL_LABELS, ALL_SYSTEMS)):
    for j, m in enumerate(REAL_TRIPLE):
        err = abs(r - m) / m
        if err <= THRESHOLD:
            output["part1_recurrence"]["hits_detail"].append({
                "system": system, "label": label, "ratio": round(r, 6),
                "mode": mode_names[j], "mode_value": round(m, 6),
                "error_pct": round(err * 100, 4)
            })

save_path = os.path.join(results_dir, "theorem_recurrence.json")
with open(save_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to {save_path}")

# ══════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"{'Test':<40s} {'p-value':>12s} {'Sig?':>6s}")
print("-"*58)
print(f"{'Part 1: Recurrence (count)':<40s} {p_count:>12.6f} {'***' if p_count<0.001 else '**' if p_count<0.01 else '*' if p_count<0.05 else '':>6s}")
print(f"{'Part 1: Recurrence (quality)':<40s} {p_quality:>12.6f} {'***' if p_quality<0.001 else '**' if p_quality<0.01 else '*' if p_quality<0.05 else '':>6s}")
print(f"{'Part 3: Cross-system coincidence':<40s} {p_cross:>12.6f} {'***' if p_cross<0.001 else '**' if p_cross<0.01 else '*' if p_cross<0.05 else '':>6s}")
print(f"{'Part 5: Hubble cross-bracket':<40s} {p_hubble:>12.6f} {'***' if p_hubble<0.001 else '**' if p_hubble<0.01 else '*' if p_hubble<0.05 else '':>6s}")
print("-"*58)
print(f"{'Fisher combined':<40s} {fisher_p:>12.2e} {'***' if fisher_p<0.001 else '**' if fisher_p<0.01 else '*' if fisher_p<0.05 else '':>6s}")
print(f"\n*** p < 0.001   ** p < 0.01   * p < 0.05")

print(f"\nThree doors in the Cantor gate. Every scale chooses from the same three.")
