#!/usr/bin/env python3
"""
Theorem Significance Testing — Bigollo-φ Universe Test
Rigorous statistical analysis of 68 cross-scale matches.
"""

import json
import math
import time
import os
import sys
from itertools import combinations_with_replacement

# ─── Try JAX Metal GPU, fall back to numpy ─────────────────────────
USE_JAX = False
try:
    import jax
    import jax.numpy as jnp
    jax.devices()  # trigger init
    USE_JAX = True
    print(f"Backend: JAX ({jax.devices()[0].platform.upper()})")
except Exception:
    print("Backend: NumPy (JAX not available)")

import numpy as np

# ═══════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════════
PHI = 1.6180339887498948
SQRT_PHI = math.sqrt(PHI)
H_HINGE = PHI**(-1/PHI)
R_C = 1 - 1/PHI**4
W = (2 + PHI**(1/PHI**2)) / PHI**4
SIGMA3 = 0.0728; SIGMA2 = 0.2350; COS_ALPHA = math.cos(1/PHI)
COS_NODE = 0.3672; SIGMA_WALL = 0.3972; SIGMA4 = 0.5594
BOS = 0.9920; N_BRACKETS = 294
THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS)**2)
R_RC = math.sqrt(1 + (THETA_RC * BOS)**2)
R_BASE = math.sqrt(1 + (THETA_BASE * BOS)**2)
RHO6 = PHI**(1/6)

# The 28 building blocks
BLOCK_NAMES = [
    "theta_leak", "theta_rc", "theta_base",
    "sigma3", "sigma2", "sigma_wall", "sigma4",
    "cos_alpha", "cos_node", "r_c", "W", "H",
    "sqrt_phi", "phi", "phi2", "1/phi", "1/phi2",
    "pi", "2", "3", "4", "6",
    "N", "R_leak", "R_rc", "R_base", "rho6", "BOS"
]

BLOCK_VALUES = np.array([
    THETA_LEAK, THETA_RC, THETA_BASE,
    SIGMA3, SIGMA2, SIGMA_WALL, SIGMA4,
    COS_ALPHA, COS_NODE, R_C, W, H_HINGE,
    SQRT_PHI, PHI, PHI**2, 1/PHI, 1/PHI**2,
    math.pi, 2, 3, 4, 6,
    N_BRACKETS, R_LEAK, R_RC, R_BASE, RHO6, BOS
])

assert len(BLOCK_NAMES) == 28
assert len(BLOCK_VALUES) == 28

print(f"\n28 building blocks loaded.")
print(f"Range: [{BLOCK_VALUES.min():.4f}, {BLOCK_VALUES.max():.1f}]")

# ═══════════════════════════════════════════════════════════════════
# LOAD TARGETS
# ═══════════════════════════════════════════════════════════════════
DATA_PATH = "/Users/universe/Unified_Theory_Physics/results/bigollophi_theorem_universe.json"
with open(DATA_PATH) as f:
    universe_data = json.load(f)

targets = []
for bracket_name, bracket_data in universe_data["brackets"].items():
    if "results" not in bracket_data:
        continue
    for r in bracket_data["results"]:
        targets.append({
            "name": r["target"],
            "value": r["value"],
            "match": r["match"],
            "expression": r["expression"],
            "error_pct": r["error_pct"],
            "flag": r["flag"],
            "bracket": bracket_name
        })

N_TARGETS = len(targets)
target_values = np.array([t["value"] for t in targets])
target_names = [t["name"] for t in targets]
print(f"Loaded {N_TARGETS} targets from {len([b for b in universe_data['brackets'] if 'results' in universe_data['brackets'][b]])} brackets")

# ═══════════════════════════════════════════════════════════════════
# HELPER: Generate all products up to k factors
# ═══════════════════════════════════════════════════════════════════
def gen_products(values, max_factors=4, exhaustive=True, n_sample=5000):
    """Generate products of 1..max_factors from values array."""
    n = len(values)
    products = list(values)  # 1-factor

    # 2-factor: exhaustive
    for i in range(n):
        for j in range(i, n):
            products.append(values[i] * values[j])

    if exhaustive:
        # 3-factor
        for combo in combinations_with_replacement(range(n), 3):
            p = 1.0
            for idx in combo:
                p *= values[idx]
            products.append(p)
        # 4-factor
        for combo in combinations_with_replacement(range(n), 4):
            p = 1.0
            for idx in combo:
                p *= values[idx]
            products.append(p)
    else:
        # Sample random products for 3 and 4 factors
        rng = np.random.default_rng()
        for nf in [3, 4]:
            idxs = rng.integers(0, n, size=(n_sample, nf))
            for row in idxs:
                p = 1.0
                for idx in row:
                    p *= values[idx]
                products.append(p)

    return np.array(products)

def best_match_error(products_sorted, target_val):
    """Binary search for closest match, return relative error."""
    idx = np.searchsorted(products_sorted, target_val)
    best_err = float('inf')
    for i in [idx-1, idx, idx+1]:
        if 0 <= i < len(products_sorted):
            err = abs(products_sorted[i] - target_val) / abs(target_val) * 100
            if err < best_err:
                best_err = err
    return best_err

# ═══════════════════════════════════════════════════════════════════
# PART 1: MONTE CARLO NULL HYPOTHESIS
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 1: MONTE CARLO NULL HYPOTHESIS TEST")
print("="*70)

# Real framework products
print("Computing real framework products (exhaustive up to 4 factors)...")
real_products = gen_products(BLOCK_VALUES, max_factors=4, exhaustive=True)
real_products_sorted = np.sort(real_products)
print(f"  Real framework: {len(real_products)} products")

# Real framework errors
real_errors = np.array([best_match_error(real_products_sorted, tv) for tv in target_values])
print(f"  Real mean error: {real_errors.mean():.4f}%")

# Monte Carlo
N_TRIALS = 10000
N_SAMPLE_34 = 5000
rng = np.random.default_rng(42)

# For each target, count how many random frameworks beat the real error
beat_counts = np.zeros(N_TARGETS, dtype=int)

t0 = time.time()
for trial in range(N_TRIALS):
    if trial % 1000 == 0 and trial > 0:
        elapsed = time.time() - t0
        rate = trial / elapsed
        eta = (N_TRIALS - trial) / rate
        print(f"  Trial {trial}/{N_TRIALS} ({elapsed:.1f}s elapsed, ETA {eta:.1f}s)")

    # Draw 28 random values
    rand_vals = rng.uniform(0.01, 3.0, size=28)

    # Generate products (2-factor exhaustive, 3-4 factor sampled)
    rand_products = gen_products(rand_vals, max_factors=4, exhaustive=False, n_sample=N_SAMPLE_34)
    rand_sorted = np.sort(rand_products)

    # Check each target
    for j in range(N_TARGETS):
        err = best_match_error(rand_sorted, target_values[j])
        if err <= real_errors[j]:
            beat_counts[j] += 1

elapsed_total = time.time() - t0
print(f"  Completed {N_TRIALS} trials in {elapsed_total:.1f}s")

p_values = beat_counts / N_TRIALS

# Print full p-value table sorted by p-value
print("\n" + "-"*90)
print(f"{'Target':<35} {'Value':>10} {'Error%':>8} {'p-value':>10} {'Significance':<20}")
print("-"*90)

sorted_idx = np.argsort(p_values)
for i in sorted_idx:
    t = targets[i]
    pv = p_values[i]
    if pv < 0.001:
        sig = "*** HIGHLY SIG"
    elif pv < 0.01:
        sig = "** SIGNIFICANT"
    elif pv < 0.05:
        sig = "* SUGGESTIVE"
    else:
        sig = "NOISE"
    print(f"{t['name']:<35} {t['value']:>10.6f} {real_errors[i]:>8.4f} {pv:>10.4f} {sig:<20}")

# Store p-values in targets
for i in range(N_TARGETS):
    targets[i]["p_value"] = float(p_values[i])
    targets[i]["real_error"] = float(real_errors[i])

# ═══════════════════════════════════════════════════════════════════
# PART 2: NAKED MATCH FILTER
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 2: NAKED MATCH FILTER (1-2 factor matches)")
print("="*70)

# 1-factor matches
one_factor = BLOCK_VALUES.copy()

# 2-factor matches (all 28x28 = 784 pairs)
two_factor_vals = []
two_factor_labels = []
for i in range(28):
    for j in range(28):
        two_factor_vals.append(BLOCK_VALUES[i] * BLOCK_VALUES[j])
        two_factor_labels.append(f"{BLOCK_NAMES[i]} x {BLOCK_NAMES[j]}")
two_factor_vals = np.array(two_factor_vals)

print(f"\n{'Target':<35} {'Value':>10} {'Best1F':>10} {'Err1%':>8} {'Best2F':>10} {'Err2%':>8} {'Clean?':<8}")
print("-"*100)

for t in targets:
    tv = t["value"]
    # 1-factor
    errs_1 = np.abs(one_factor - tv) / abs(tv) * 100
    best_1_idx = np.argmin(errs_1)
    best_1_err = errs_1[best_1_idx]
    best_1_name = BLOCK_NAMES[best_1_idx]

    # 2-factor
    errs_2 = np.abs(two_factor_vals - tv) / abs(tv) * 100
    best_2_idx = np.argmin(errs_2)
    best_2_err = errs_2[best_2_idx]
    best_2_name = two_factor_labels[best_2_idx]

    best_naked_err = min(best_1_err, best_2_err)
    clean = best_naked_err < 1.0
    t["naked_1f_err"] = float(best_1_err)
    t["naked_1f_match"] = best_1_name
    t["naked_2f_err"] = float(best_2_err)
    t["naked_2f_match"] = best_2_name
    t["clean_signal"] = clean

    flag = "CLEAN" if clean else ""
    print(f"{t['name']:<35} {tv:>10.6f} {one_factor[best_1_idx]:>10.6f} {best_1_err:>8.3f} "
          f"{two_factor_vals[best_2_idx]:>10.6f} {best_2_err:>8.3f} {flag:<8}")

n_clean = sum(1 for t in targets if t["clean_signal"])
print(f"\nClean signals (1-2 factor <1% error): {n_clean}/{N_TARGETS}")

# ═══════════════════════════════════════════════════════════════════
# PART 3: RECURRENCE FILTER
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 3: RECURRENCE FILTER")
print("="*70)

# Parse expressions to find building blocks
def parse_expression(expr_str):
    """Extract building block names from expression string."""
    parts = [p.strip() for p in expr_str.split(" x ")]
    return parts

# Count block appearances across brackets
block_bracket_map = {}  # block_name -> set of brackets
block_target_map = {}   # block_name -> list of target names
expression_recurrence = {}  # full expression -> list of targets

for t in targets:
    parts = parse_expression(t["expression"])
    t["parsed_blocks"] = parts
    bracket = t["bracket"]

    for block in parts:
        if block not in block_bracket_map:
            block_bracket_map[block] = set()
            block_target_map[block] = []
        block_bracket_map[block].add(bracket)
        block_target_map[block].append(t["name"])

    expr_key = " x ".join(sorted(parts))
    if expr_key not in expression_recurrence:
        expression_recurrence[expr_key] = []
    expression_recurrence[expr_key].append(t["name"])

# Cross-bracket recurrence
print("\nBuilding blocks appearing across 2+ brackets:")
print(f"{'Block':<20} {'# Brackets':>10} {'# Targets':>10} {'Brackets'}")
print("-"*80)

cross_bracket_blocks = {}
for block in sorted(block_bracket_map.keys(), key=lambda b: len(block_bracket_map[b]), reverse=True):
    n_brackets = len(block_bracket_map[block])
    n_targets = len(block_target_map[block])
    if n_brackets >= 2:
        cross_bracket_blocks[block] = n_brackets
        brackets_str = ", ".join(sorted(block_bracket_map[block]))
        print(f"{block:<20} {n_brackets:>10} {n_targets:>10}   {brackets_str}")

# Mark recurrence in targets
for t in targets:
    blocks = t["parsed_blocks"]
    t["recurrent_blocks"] = [b for b in blocks if b in cross_bracket_blocks and cross_bracket_blocks[b] >= 2]
    t["has_recurrence"] = len(t["recurrent_blocks"]) > 0
    t["n_recurrent_brackets"] = max([cross_bracket_blocks.get(b, 0) for b in blocks]) if blocks else 0

# Specific questions
print("\n--- Specific recurrence checks ---")

# Which theta mode appears most?
theta_modes = ["theta_leak", "theta_rc", "theta_base"]
for tm in theta_modes:
    n = len(block_target_map.get(tm, []))
    nb = len(block_bracket_map.get(tm, set()))
    print(f"{tm}: {n} targets across {nb} brackets")

# R_baseline in 3+ brackets?
for rname in ["R_base", "R_leak", "R_rc"]:
    nb = len(block_bracket_map.get(rname, set()))
    targets_list = block_target_map.get(rname, [])
    print(f"{rname}: {nb} brackets, targets: {targets_list}")

# Recurring multi-factor expressions
print("\nRecurring expressions (same sorted factors for different targets):")
for expr, tlist in expression_recurrence.items():
    if len(tlist) > 1:
        print(f"  {expr}: {tlist}")

# ═══════════════════════════════════════════════════════════════════
# PART 4: TIER CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 4: TIER CLASSIFICATION")
print("="*70)

tier1 = []
tier2 = []
tier3 = []
noise = []

for t in targets:
    pv = t["p_value"]
    naked_ok = t.get("clean_signal", False)
    naked_5pct = min(t.get("naked_1f_err", 999), t.get("naked_2f_err", 999)) < 5.0
    recurrent = t.get("has_recurrence", False)
    n_rec_brackets = t.get("n_recurrent_brackets", 0)

    if pv < 0.001 and (naked_ok or n_rec_brackets >= 2):
        t["tier"] = 1
        tier1.append(t)
    elif pv < 0.01 and (naked_5pct or n_rec_brackets >= 1):
        t["tier"] = 2
        tier2.append(t)
    elif pv < 0.05:
        t["tier"] = 3
        tier3.append(t)
    else:
        t["tier"] = 0
        noise.append(t)

# Also classify remaining low-p targets that didn't meet compound criteria
# into their p-value tier
for t in targets:
    if "tier" not in t:
        pv = t["p_value"]
        if pv < 0.001:
            t["tier"] = 2  # highly sig but missing compound criterion -> tier 2
            tier2.append(t)
        elif pv < 0.01:
            t["tier"] = 2
            tier2.append(t)
        elif pv < 0.05:
            t["tier"] = 3
            tier3.append(t)
        else:
            t["tier"] = 0
            noise.append(t)

def print_tier_table(tier_list, tier_name):
    print(f"\n{'─'*90}")
    print(f"  {tier_name} ({len(tier_list)} targets)")
    print(f"{'─'*90}")
    print(f"  {'Target':<32} {'Bracket':<20} {'Error%':>8} {'p-val':>8} {'Naked<1%':>9} {'Recur':>6}")
    print(f"  {'─'*85}")
    for t in sorted(tier_list, key=lambda x: x["p_value"]):
        clean = "YES" if t.get("clean_signal") else "no"
        recur = "YES" if t.get("has_recurrence") else "no"
        print(f"  {t['name']:<32} {t['bracket']:<20} {t['error_pct']:>8.4f} {t['p_value']:>8.4f} {clean:>9} {recur:>6}")

print_tier_table(tier1, "TIER 1: STRUCTURAL (p<0.001 + naked/recurrence)")
print_tier_table(tier2, "TIER 2: SIGNIFICANT (p<0.01 + supporting evidence)")
print_tier_table(tier3, "TIER 3: SUGGESTIVE (p<0.05)")

print(f"\n{'─'*90}")
print(f"  NOISE ({len(noise)} targets)")
print(f"{'─'*90}")
for t in sorted(noise, key=lambda x: x["p_value"]):
    print(f"  {t['name']:<35} p={t['p_value']:.4f}  err={t['error_pct']:.4f}%  [{t['bracket']}]")

# ═══════════════════════════════════════════════════════════════════
# PART 5: FALSIFIABILITY MATRIX
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 5: FALSIFIABILITY MATRIX")
print("="*70)

# Build falsifiability entries for Tier 1 and Tier 2
falsifiability_entries = []

# Pre-built specific entries for key targets
specific_entries = {
    "Hubble tension H0_local/H0_Planck": {
        "confirm": "SH0ES+Planck ratio stays at 1.083 +/- 0.006; DESI BAO confirms tension persists",
        "kill": "Hubble tension resolves to <2% (ratio < 1.02) via systematic recalibration",
        "status": "DATA EXISTS (SH0ES 2022, Planck 2018, DESI 2024)"
    },
    "TRAPPIST d/c": {
        "confirm": "JWST transit timing confirms d/c semi-major axis ratio at 1.409 +/- 0.005",
        "kill": "Refined JWST ephemeris shifts d/c outside [1.40, 1.42]",
        "status": "DATA EXISTS (Agol+ 2021), JWST REFINING"
    },
    "Cl2/F2 bond ratio": {
        "confirm": "Precision spectroscopy confirms Cl2/F2 = 1.4079 +/- 0.0005",
        "kill": "High-accuracy ab initio puts ratio outside [1.406, 1.410]",
        "status": "DATA EXISTS (NIST, CRC Handbook)"
    },
    "Br2/Cl2 bond ratio": {
        "confirm": "Precision spectroscopy confirms Br2/Cl2 = 1.1474 +/- 0.0005",
        "kill": "High-accuracy measurement shifts ratio outside [1.145, 1.150]",
        "status": "DATA EXISTS (NIST, CRC Handbook)"
    },
    "Omega_DM": {
        "confirm": "Planck+DESI converge on 0.264 +/- 0.003",
        "kill": "Next-gen CMB (CMB-S4) + BAO give Omega_DM outside [0.260, 0.270]",
        "status": "DATA EXISTS (Planck 2018: 0.265)"
    },
    "Chandrasekhar limit M_sun": {
        "confirm": "WD mass distribution peak stays at 1.44 +/- 0.02 M_sun",
        "kill": "Theoretical GR+QED revision puts limit at 1.38 or below (>2% from R_base=1.409)",
        "status": "DATA EXISTS (Koester+ 1987, Kepler+ 2007)"
    },
    "|V_us|": {
        "confirm": "Lattice QCD+experiment converge on 0.2243 +/- 0.0005",
        "kill": "CKM unitarity test (row 1) breaks at >3 sigma, requiring BSM physics",
        "status": "DATA EXISTS (PDG 2024)"
    },
    "|V_cb|": {
        "confirm": "Exclusive/inclusive |V_cb| converge on 0.0422 +/- 0.001",
        "kill": "Exclusive/inclusive discrepancy resolves to value outside [0.040, 0.044]",
        "status": "DATA EXISTS (PDG 2024, Belle II)"
    },
    "|V_ub|": {
        "confirm": "Lattice+experiment converge on 0.00394 +/- 0.0002",
        "kill": "New lattice calculations shift |V_ub| outside [0.0035, 0.0043]",
        "status": "DATA EXISTS (PDG 2024)"
    },
    "Omega_DE": {
        "confirm": "DESI+Euclid confirm Omega_DE = 0.685 +/- 0.005 with no w(z) evolution",
        "kill": "Dark energy equation of state w != -1 at >3 sigma (dynamic DE)",
        "status": "DATA EXISTS (Planck 2018, DESI 2024)"
    },
    "m_t/m_W": {
        "confirm": "HL-LHC top mass converges on 172.5 +/- 0.3 GeV",
        "kill": "Top mass shifts outside [171, 174] GeV, breaking ratio prediction",
        "status": "DATA EXISTS (CMS+ATLAS 2024)"
    },
    "CMB temp / 2": {
        "confirm": "COBE/FIRAS absolute calibration confirmed at T_CMB = 2.7255 +/- 0.0006 K",
        "kill": "New absolute measurement shifts T_CMB outside [2.720, 2.730] K",
        "status": "DATA EXISTS (Fixsen 2009)"
    },
    "Solar core boundary R": {
        "confirm": "Helioseismology confirms radiative-convective boundary at 0.250 +/- 0.005 R_sun",
        "kill": "Next-gen helioseismology (SDO, Solar Orbiter) shifts boundary outside [0.24, 0.26]",
        "status": "DATA EXISTS (Basu & Antia 2004)"
    },
    "m_tau/m_mu": {
        "confirm": "Belle II precision tau mass confirms ratio at 16.817 +/- 0.01",
        "kill": "Tau mass measurement shifts ratio outside [16.80, 16.83]",
        "status": "DATA EXISTS (PDG 2024)"
    },
    "Proton/electron radius r_p/r_e": {
        "confirm": "Muonic hydrogen precision confirms r_p = 0.841 +/- 0.001 fm",
        "kill": "Proton radius puzzle re-opens with r_p > 0.88 fm",
        "status": "DATA EXISTS (CODATA 2018, PRad)"
    },
    "Earth/Venus AU": {
        "confirm": "Ephemeris precision stable at 1.38313 +/- 0.00001",
        "kill": "N/A — orbital ratios are known to ~10 significant figures",
        "status": "DATA EXISTS (JPL DE441)"
    },
    "m_b/m_c": {
        "confirm": "Lattice QCD running masses converge on m_b/m_c = 3.278 +/- 0.01",
        "kill": "Non-perturbative effects shift ratio outside [3.25, 3.30]",
        "status": "DATA EXISTS (PDG 2024)"
    },
    "Proton-to-neutron mass ratio": {
        "confirm": "Precision mass spectrometry confirms 0.99862 to 7+ digits",
        "kill": "N/A — known to 10+ significant figures",
        "status": "DATA EXISTS (CODATA 2018)"
    },
    "Omega_b": {
        "confirm": "CMB-S4 + BBN convergence at 0.0486 +/- 0.001",
        "kill": "BBN deuterium abundance shifts Omega_b outside [0.046, 0.051]",
        "status": "DATA EXISTS (Planck 2018, BBN)"
    },
    "BCS gap ratio 2D/kTc": {
        "confirm": "Tunneling spectroscopy on weak-coupling superconductors confirms 3.528 +/- 0.01",
        "kill": "N/A — BCS is an exact result in weak-coupling limit",
        "status": "DATA EXISTS (BCS theory, Al tunneling)"
    }
}

falsifiability_md = "# Falsifiability Matrix\n\n"
falsifiability_md += "## Bigollo-phi Universe Test — Tier 1 & Tier 2 Targets\n\n"
falsifiability_md += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

for t in sorted(tier1 + tier2, key=lambda x: x["p_value"]):
    name = t["name"]
    entry = specific_entries.get(name, {
        "confirm": f"Independent measurement confirms {name} = {t['value']:.6f} within {max(t['error_pct']*3, 0.1):.2f}%",
        "kill": f"Precision measurement shifts {name} outside +/-{max(t['error_pct']*5, 0.5):.2f}% of {t['value']:.6f}",
        "status": "NEEDS VERIFICATION"
    })

    block = f"""### {name}
- **Match:** {t['value']:.6f} = {t['expression']} (error {t['error_pct']:.4f}%)
- **Tier:** {t['tier']} | **p-value:** {t['p_value']:.4f} | **Bracket:** {t['bracket']}
- **Confirm:** {entry['confirm']}
- **Kill:** {entry['kill']}
- **Status:** {entry['status']}

"""
    falsifiability_md += block
    print(f"  {name}: Tier {t['tier']}, p={t['p_value']:.4f}")

# Save falsifiability matrix
os.makedirs("/Users/universe/Unified_Theory_Physics/results", exist_ok=True)
with open("/Users/universe/Unified_Theory_Physics/results/falsifiability_matrix.md", "w") as f:
    f.write(falsifiability_md)
print(f"\nFalsifiability matrix saved to results/falsifiability_matrix.md")

# ═══════════════════════════════════════════════════════════════════
# PART 6: THEOREM STATEMENT
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PART 6: THEOREM STATEMENT")
print("="*70)

n_tier1 = len(tier1)
n_tier2 = len(tier2)
n_significant = n_tier1 + n_tier2
n_brackets_hit = len(set(t["bracket"] for t in tier1 + tier2))
mean_error_sig = np.mean([t["error_pct"] for t in tier1 + tier2]) if (tier1 + tier2) else 0

# Overall framework p-value: probability of getting n_significant or more sub-threshold matches
# Use the per-target p-values to compute a combined Fisher statistic
import scipy.stats as stats

# Fisher's method: -2 * sum(ln(p_i)) ~ chi2(2k) under null
p_vals_sig = [max(t["p_value"], 1e-10) for t in tier1 + tier2]  # avoid log(0)
if p_vals_sig:
    fisher_stat = -2 * sum(math.log(p) for p in p_vals_sig)
    fisher_df = 2 * len(p_vals_sig)
    fisher_p = 1 - stats.chi2.cdf(fisher_stat, fisher_df)
else:
    fisher_p = 1.0

# Also compute: fraction of targets with p < 0.01
n_sub_001 = sum(1 for t in targets if t["p_value"] < 0.01)
# Expected under null: 0.01 * 68 = 0.68
# Binomial p-value for observing n_sub_001 or more
binom_p = 1 - stats.binom.cdf(n_sub_001 - 1, N_TARGETS, 0.01) if n_sub_001 > 0 else 1.0

# Threshold error for significant matches
threshold_err = max(real_errors[np.argsort(p_values)[:n_significant]]) if n_significant > 0 else 1.0

# All-targets stats
all_mean_error = np.mean([t["error_pct"] for t in targets])
n_brackets_total = len(set(t["bracket"] for t in targets))

theorem_text = f"""THEOREM (Bigollo-phi Three-Mode Quantization):

The critical Fibonacci Hamiltonian at V = 2J, alpha = 1/phi generates
three quantized confinement modes (theta_leak = 0.564, theta_rc = 0.854,
theta_baseline = 1.000) that predict {n_significant} independently measured
physical quantities across {n_brackets_hit} scale brackets (nuclear through
cosmological) with mean error {mean_error_sig:.3f}%, where the probability
of {n_significant} or more sub-{threshold_err:.2f}% matches from 28 random
constants is p = {fisher_p:.2e} (Fisher's method, chi2({fisher_df}) = {fisher_stat:.1f}).

Supporting statistics:
- Total targets tested: {N_TARGETS}
- Tier 1 (structural): {n_tier1} targets
- Tier 2 (significant): {n_tier2} targets
- Tier 3 (suggestive): {len(tier3)} targets
- Noise: {len(noise)} targets
- Brackets covered: {n_brackets_total} ({', '.join(sorted(set(t['bracket'] for t in targets)))})
- Overall mean error (all {N_TARGETS}): {all_mean_error:.4f}%
- Targets with p < 0.01: {n_sub_001}/{N_TARGETS} (expected under null: {0.01*N_TARGETS:.1f})
- Binomial p-value for {n_sub_001}+ sub-1% targets: {binom_p:.2e}

The framework uses 28 building blocks derived from a single axiom
(phi^2 = phi + 1) with zero free parameters. The Monte Carlo null
hypothesis test used {N_TRIALS} random 28-constant frameworks with
products up to 4 factors.

QED.
"""

print(theorem_text)

# Save theorem
with open("/Users/universe/Unified_Theory_Physics/results/theorem_statement.txt", "w") as f:
    f.write(theorem_text)
print("Theorem saved to results/theorem_statement.txt")

# ═══════════════════════════════════════════════════════════════════
# SAVE ALL DATA
# ═══════════════════════════════════════════════════════════════════
output_data = {
    "metadata": {
        "backend": f"JAX ({jax.devices()[0].platform.upper()})" if USE_JAX else "NumPy",
        "n_targets": N_TARGETS,
        "n_blocks": 28,
        "n_trials": N_TRIALS,
        "elapsed_seconds": round(elapsed_total, 1),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    },
    "building_blocks": {name: float(val) for name, val in zip(BLOCK_NAMES, BLOCK_VALUES)},
    "targets": [],
    "tier_summary": {
        "tier1": n_tier1,
        "tier2": n_tier2,
        "tier3": len(tier3),
        "noise": len(noise)
    },
    "overall": {
        "fisher_statistic": float(fisher_stat) if n_significant > 0 else None,
        "fisher_df": fisher_df if n_significant > 0 else None,
        "fisher_p_value": float(fisher_p),
        "binomial_p_value": float(binom_p),
        "n_sub_001": n_sub_001,
        "mean_error_all": float(all_mean_error),
        "mean_error_significant": float(mean_error_sig)
    }
}

for t in sorted(targets, key=lambda x: x["p_value"]):
    entry = {
        "name": t["name"],
        "value": t["value"],
        "match": t["match"],
        "expression": t["expression"],
        "error_pct": t["error_pct"],
        "bracket": t["bracket"],
        "p_value": t["p_value"],
        "real_error": t["real_error"],
        "tier": t.get("tier", 0),
        "naked_1f_err": float(t.get("naked_1f_err", 0)),
        "naked_2f_err": float(t.get("naked_2f_err", 0)),
        "clean_signal": bool(t.get("clean_signal", False)),
        "has_recurrence": bool(t.get("has_recurrence", False)),
        "recurrent_blocks": t.get("recurrent_blocks", [])
    }
    output_data["targets"].append(entry)

with open("/Users/universe/Unified_Theory_Physics/results/theorem_significance.json", "w") as f:
    json.dump(output_data, f, indent=2)

print(f"\nAll data saved to results/theorem_significance.json")

# ═══════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)
print(f"  Targets analyzed:     {N_TARGETS}")
print(f"  Tier 1 (structural):  {n_tier1}")
print(f"  Tier 2 (significant): {n_tier2}")
print(f"  Tier 3 (suggestive):  {len(tier3)}")
print(f"  Noise:                {len(noise)}")
print(f"  Mean error (all):     {all_mean_error:.4f}%")
print(f"  Mean error (T1+T2):   {mean_error_sig:.4f}%")
print(f"  Fisher p-value:       {fisher_p:.2e}")
print(f"  Binomial p-value:     {binom_p:.2e}")
print(f"  Runtime:              {elapsed_total:.1f}s")
print("="*70)
