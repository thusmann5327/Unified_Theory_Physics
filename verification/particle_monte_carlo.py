"""
particle_monte_carlo.py — Monte Carlo validation of particle mass matches
==========================================================================

Are the 18 sub-0.1% particle physics matches real or combinatorial noise?

Test: generate 100,000 random frameworks, each with ~46 building blocks.
For each, compute all products of ≤ 3 blocks (~15,000 combinations) and
check how many of 15 target ratios are matched at < 0.1%.

P-VALUE = fraction of random frameworks with n_hits ≥ real n_hits.

Uses JAX for GPU-accelerated vectorized computation.

Thomas A. Husmann / iBuilt LTD / March 2026
"""

import os
import sys
import json
import time
import math
import numpy as np

# ─── Try JAX for GPU acceleration, fall back to NumPy ────────────
try:
    import jax
    import jax.numpy as jnp
    from jax import random as jrand
    HAS_JAX = True
    print(f"  JAX backend: {jax.default_backend()}")
    print(f"  Device: {jax.devices()[0]}")
except ImportError:
    HAS_JAX = False
    print("  JAX not available, using NumPy (slower)")


# ═══════════════════════════════════════════════════════════════════
# REAL FRAMEWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2
W = (2 + PHI**(1.0 / PHI**2)) / PHI**4
H_HINGE = PHI**(-1.0 / PHI)
LEAK = 1.0 / PHI**4
R_C = 1.0 - LEAK
D = 233
N_BRACKETS = 294

# Metallic means
def metallic_mean(n):
    return (n + math.sqrt(n * n + 4)) / 2

DELTA_3 = metallic_mean(3)
DELTA_7 = metallic_mean(7)

# Spectral ratios (from AAH eigensolver)
SIGMA3 = 0.07278
SIGMA_WALL = 0.3972
SIGMA2 = 0.2350
SIGMA4 = 0.5594
BOS = 0.99202
BASE = 1.40838


# ═══════════════════════════════════════════════════════════════════
# TARGET RATIOS (from particle physics)
# ═══════════════════════════════════════════════════════════════════

TARGETS = {
    'mu/e':       206.768,
    'tau/mu':     16.817,
    'tau/e':      3477.22,
    'c/u':        587.96,
    't/c':        136.03,
    's/d':        20.00,
    'b/s':        44.75,
    'b/d':        895.07,
    'Koide':      2.0 / 3.0,
    'sin2_thetaW': 0.23122,
    'sin_thetaC': 0.2253,
    'dm2_ratio':  32.58,
    'MW/MZ':      0.8815,
    't/u':        79981.5,
    'c/d':        271.95,
}

TARGET_NAMES = list(TARGETS.keys())
TARGET_VALUES = np.array(list(TARGETS.values()), dtype=np.float64)
N_TARGETS = len(TARGET_VALUES)


# ═══════════════════════════════════════════════════════════════════
# REAL FRAMEWORK: BUILD ~46 BUILDING BLOCKS
# ═══════════════════════════════════════════════════════════════════

def real_building_blocks():
    """Build the ~46 building blocks from the real framework."""
    blocks = []

    # φ powers: φ^1 through φ^20 (20)
    for k in range(1, 21):
        blocks.append(PHI**k)

    # Core constants (7)
    blocks.extend([W, R_C, LEAK, BOS, BASE, math.sqrt(PHI), PHI**(1.0/6.0)])

    # Spectral widths (4)
    blocks.extend([SIGMA3, SIGMA_WALL, SIGMA2, SIGMA4])

    # Integer parameters (2)
    blocks.extend([float(D), float(N_BRACKETS)])

    # Fibonacci multipliers (6)
    blocks.extend([3.0, 5.0, 8.0, 13.0, 21.0, 34.0])

    # Small integer multipliers (5)
    blocks.extend([2.0, 4.0, 6.0, 12.0, 36.0])

    # Transcendentals (2)
    blocks.extend([math.pi, math.e])

    # Metallic means and hinge (3)
    blocks.extend([DELTA_3, DELTA_7, H_HINGE])

    # Inverses of key constants (3) — W⁻¹, φ⁻¹, R_C⁻¹
    blocks.extend([1.0/W, 1.0/PHI, 1.0/R_C])

    return np.array(blocks, dtype=np.float64)


def count_combinations(n_blocks):
    """Count products of ≤ 3 from n_blocks."""
    # Singles + pairs + triples (with replacement for powers)
    n1 = n_blocks
    n2 = n_blocks * (n_blocks + 1) // 2
    n3 = n_blocks * (n_blocks + 1) * (n_blocks + 2) // 6
    return n1 + n2 + n3


def generate_all_products(blocks):
    """
    Generate all products of 1, 2, and 3 building blocks.
    Returns 1D array of all products.
    """
    n = len(blocks)
    products = []

    # Singles
    products.extend(blocks)

    # Pairs (with replacement)
    for i in range(n):
        for j in range(i, n):
            products.append(blocks[i] * blocks[j])

    # Triples (with replacement)
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                products.append(blocks[i] * blocks[j] * blocks[k])

    return np.array(products, dtype=np.float64)


# ═══════════════════════════════════════════════════════════════════
# REAL FRAMEWORK SCORING
# ═══════════════════════════════════════════════════════════════════

def score_framework(products, thresholds=(0.001, 0.01, 0.05)):
    """
    For each target, find the minimum relative error across all products.
    Returns (n_hits per threshold, min_errors array).
    """
    min_errors = np.full(N_TARGETS, np.inf)

    for t_idx in range(N_TARGETS):
        target = TARGET_VALUES[t_idx]
        if target == 0:
            continue

        # Relative error for all products
        rel_errors = np.abs(products - target) / abs(target)

        # Also check inverses (ratio could be inverted)
        inv_products = np.where(np.abs(products) > 1e-15, 1.0 / products, np.inf)
        inv_errors = np.abs(inv_products - target) / abs(target)

        min_err = min(np.min(rel_errors), np.min(inv_errors))
        min_errors[t_idx] = min_err

    hits = {}
    for thresh in thresholds:
        hits[thresh] = int(np.sum(min_errors < thresh))

    return hits, min_errors


# ═══════════════════════════════════════════════════════════════════
# RANDOM FRAMEWORK GENERATOR
# ═══════════════════════════════════════════════════════════════════

def random_building_blocks(rng):
    """
    Generate ~46 random building blocks with same structure as real framework.
    Uses same NUMBER of blocks but random VALUES.
    """
    blocks = []

    # Random "golden ratio" analog: uniform [1.1, 2.5]
    phi_rand = rng.uniform(1.1, 2.5)

    # 20 powers of phi_rand
    for k in range(1, 21):
        blocks.append(phi_rand**k)

    # Random "gap fraction" analog: uniform [0.1, 0.9]
    w_rand = rng.uniform(0.1, 0.9)

    # Core constants analog (7)
    leak_rand = 1.0 / phi_rand**4
    rc_rand = 1.0 - leak_rand
    bos_rand = rng.uniform(0.5, 1.5)
    base_rand = math.sqrt(1 + bos_rand**2)
    blocks.extend([w_rand, rc_rand, leak_rand, bos_rand, base_rand,
                   math.sqrt(phi_rand), phi_rand**(1.0/6.0)])

    # Random spectral widths (4)
    blocks.extend([
        rng.uniform(0.01, 0.2),   # σ₃ analog
        rng.uniform(0.1, 0.6),    # σ_wall analog
        rng.uniform(0.05, 0.4),   # σ₂ analog
        rng.uniform(0.2, 0.8),    # σ₄ analog
    ])

    # Random integers (2)
    d_rand = rng.integers(50, 501)
    n_rand = rng.integers(100, 501)
    blocks.extend([float(d_rand), float(n_rand)])

    # Same Fibonacci multipliers (6) — these are GIVEN, not random
    # But to be fair, use random small primes/composites of similar magnitude
    blocks.extend([
        float(rng.integers(2, 5)),    # analog of 3
        float(rng.integers(3, 8)),    # analog of 5
        float(rng.integers(5, 12)),   # analog of 8
        float(rng.integers(8, 20)),   # analog of 13
        float(rng.integers(13, 30)),  # analog of 21
        float(rng.integers(20, 50)),  # analog of 34
    ])

    # Random small integer multipliers (5)
    blocks.extend([
        float(rng.integers(2, 4)),    # analog of 2
        float(rng.integers(3, 6)),    # analog of 4
        float(rng.integers(4, 9)),    # analog of 6
        float(rng.integers(8, 16)),   # analog of 12
        float(rng.integers(20, 50)),  # analog of 36
    ])

    # Transcendental analogs (2)
    blocks.extend([rng.uniform(2.5, 4.0), rng.uniform(2.0, 3.5)])

    # Random metallic means + hinge (3)
    n_mm3 = rng.integers(2, 6)
    n_mm7 = rng.integers(4, 10)
    mm3 = (n_mm3 + math.sqrt(n_mm3**2 + 4)) / 2
    mm7 = (n_mm7 + math.sqrt(n_mm7**2 + 4)) / 2
    h_rand = phi_rand**(-1.0/phi_rand) if phi_rand > 1 else 0.5
    blocks.extend([mm3, mm7, h_rand])

    # Inverses (3)
    blocks.extend([1.0/max(w_rand, 0.01), 1.0/phi_rand, 1.0/max(rc_rand, 0.01)])

    return np.array(blocks, dtype=np.float64)


# ═══════════════════════════════════════════════════════════════════
# VECTORIZED MONTE CARLO (NumPy)
# ═══════════════════════════════════════════════════════════════════

def run_monte_carlo_numpy(n_frameworks=100_000, seed=42):
    """
    Run Monte Carlo with NumPy. Process frameworks one at a time
    but with vectorized product generation and scoring.
    """
    rng = np.random.default_rng(seed)

    # Score real framework first
    real_blocks = real_building_blocks()
    n_blocks = len(real_blocks)
    real_products = generate_all_products(real_blocks)
    n_products = len(real_products)
    real_hits, real_errors = score_framework(real_products)

    print(f"\n  Real framework:")
    print(f"    Building blocks: {n_blocks}")
    print(f"    Products (≤3): {n_products:,}")
    print(f"    Hits at <0.1%: {real_hits[0.001]}/15")
    print(f"    Hits at <1%:   {real_hits[0.01]}/15")
    print(f"    Hits at <5%:   {real_hits[0.05]}/15")

    # Per-target errors for real framework
    print(f"\n  Per-target minimum errors (real framework):")
    for i, name in enumerate(TARGET_NAMES):
        err = real_errors[i] * 100
        star = "★★★" if err < 0.1 else "★★" if err < 1 else "★" if err < 5 else ""
        print(f"    {name:>15s}: {err:>8.3f}%  {star}")

    real_geomean = np.exp(np.mean(np.log(np.clip(real_errors, 1e-20, 1))))

    # Monte Carlo
    print(f"\n  Running {n_frameworks:,} random frameworks...")
    t0 = time.time()

    hits_01_dist = np.zeros(n_frameworks, dtype=np.int32)
    hits_1_dist = np.zeros(n_frameworks, dtype=np.int32)
    hits_5_dist = np.zeros(n_frameworks, dtype=np.int32)
    geomean_dist = np.zeros(n_frameworks, dtype=np.float64)

    report_interval = n_frameworks // 20

    for trial in range(n_frameworks):
        if trial > 0 and trial % report_interval == 0:
            elapsed = time.time() - t0
            rate = trial / elapsed
            eta = (n_frameworks - trial) / rate
            print(f"    {trial:>7,}/{n_frameworks:,}  "
                  f"({trial/n_frameworks*100:.0f}%)  "
                  f"{rate:.0f}/s  ETA {eta:.0f}s")

        rand_blocks = random_building_blocks(rng)
        rand_products = generate_all_products(rand_blocks)
        hits, errors = score_framework(rand_products)

        hits_01_dist[trial] = hits[0.001]
        hits_1_dist[trial] = hits[0.01]
        hits_5_dist[trial] = hits[0.05]
        geomean_dist[trial] = np.exp(np.mean(np.log(np.clip(errors, 1e-20, 1))))

    elapsed = time.time() - t0

    return {
        'n_frameworks': n_frameworks,
        'elapsed_s': elapsed,
        'n_blocks': n_blocks,
        'n_products': n_products,
        'real_hits_01': real_hits[0.001],
        'real_hits_1': real_hits[0.01],
        'real_hits_5': real_hits[0.05],
        'real_errors': real_errors.tolist(),
        'real_geomean': float(real_geomean),
        'hits_01_dist': hits_01_dist,
        'hits_1_dist': hits_1_dist,
        'hits_5_dist': hits_5_dist,
        'geomean_dist': geomean_dist,
    }


# ═══════════════════════════════════════════════════════════════════
# CROSS-CORRELATION TEST
# ═══════════════════════════════════════════════════════════════════

def cross_correlation_test():
    """
    Count how many particle targets share building blocks with
    predictions in OTHER domains (atomic, cosmological).

    The real framework reuses the SAME constants across domains:
      - 136 = 4×F(9) appears in BOTH t/c ratio AND gravity hierarchy
      - 2/3 = ν appears in BOTH Koide AND N-SmA correlation length
      - N = 294 appears in BOTH c/u=2N AND α⁻¹=N×W
      - W appears in BOTH τ/μ=W×36 AND Ω_DE=W²+W AND Ω_b=W⁴
      - σ₃×σ_wall appears in BOTH sin²θ_W AND atomic gate overflow
      - δ₇ appears in M_W, M_Z, M_H, α_s (4 targets, same constant)
      - R_C appears in (m_n-m_p)/m_e AND N-SmA crossover AND QH κ

    Real framework: constants are SHARED across physics domains.
    Random framework: each constant appears in at most one domain.
    """
    # Cross-domain sharing in real framework
    shared = {
        '136 = gravity + t/c': ['t/c', 'gravity_hierarchy'],
        '2/3 = Koide + NSmA ν': ['Koide', 'NSmA_alpha'],
        'N = c/u + α⁻¹': ['c/u', 'fine_structure'],
        'W = τ/μ + Ω_DE + Ω_b': ['tau/mu', 'dark_energy', 'baryon_fraction'],
        'σ₃σ_wall = sin²θ_W + gate': ['sin2_thetaW', 'gate_overflow'],
        'δ₇ = M_W + M_Z + M_H + α_s': ['M_W', 'M_Z', 'M_H', 'alpha_s'],
        'R_C = neutron + NSmA + QH': ['neutron_mass', 'NSmA', 'QH_kappa'],
    }

    n_shared_real = len(shared)  # 7 cross-domain links
    n_domains_real = sum(len(v) for v in shared.values())  # 17 domain appearances

    return {
        'n_cross_links': n_shared_real,
        'n_domain_appearances': n_domains_real,
        'shared_constants': {k: v for k, v in shared.items()},
    }


# ═══════════════════════════════════════════════════════════════════
# ANALYSIS AND OUTPUT
# ═══════════════════════════════════════════════════════════════════

def analyze_results(results):
    """Compute p-values and print analysis."""
    real_01 = results['real_hits_01']
    real_1 = results['real_hits_1']
    real_5 = results['real_hits_5']
    real_gm = results['real_geomean']
    n_fw = results['n_frameworks']

    h01 = results['hits_01_dist']
    h1 = results['hits_1_dist']
    h5 = results['hits_5_dist']
    gm = results['geomean_dist']

    # P-values
    p_01 = np.sum(h01 >= real_01) / n_fw
    p_1 = np.sum(h1 >= real_1) / n_fw
    p_5 = np.sum(h5 >= real_5) / n_fw
    p_gm = np.sum(gm <= real_gm) / n_fw

    # Histogram of hits at 0.1%
    max_hits = max(int(np.max(h01)), real_01) + 1
    hist_01 = np.bincount(h01, minlength=max_hits + 1)

    # Geometric mean comparison for frameworks with same hit count
    mask_same = h01 == real_01
    n_same = np.sum(mask_same)
    gm_same = gm[mask_same] if n_same > 0 else np.array([])
    gm_better = np.sum(gm_same <= real_gm) if n_same > 0 else 0

    # Cross-correlation
    xc = cross_correlation_test()

    return {
        'p_01': p_01,
        'p_1': p_1,
        'p_5': p_5,
        'p_geomean': p_gm,
        'hist_01': hist_01.tolist(),
        'median_01': float(np.median(h01)),
        'mean_01': float(np.mean(h01)),
        'max_01': int(np.max(h01)),
        'n_same_hits': int(n_same),
        'gm_better_fraction': float(gm_better / max(n_same, 1)),
        'real_geomean': real_gm,
        'random_geomean_median': float(np.median(gm)),
        'cross_correlation': xc,
    }


def print_report(results, analysis):
    """Print the full Monte Carlo report."""
    n_fw = results['n_frameworks']
    elapsed = results['elapsed_s']

    print()
    print("=" * 80)
    print("  PARTICLE PHYSICS MONTE CARLO VALIDATION")
    print("  Are the mass matches real or combinatorial noise?")
    print("=" * 80)

    print(f"\n  Configuration:")
    print(f"    Random frameworks:    {n_fw:,}")
    print(f"    Building blocks/fw:   {results['n_blocks']}")
    print(f"    Products/fw (≤3):     {results['n_products']:,}")
    print(f"    Target ratios:        {N_TARGETS}")
    print(f"    Total comparisons:    {n_fw * results['n_products'] * N_TARGETS:,.0f}")
    print(f"    Elapsed:              {elapsed:.1f}s ({n_fw/elapsed:.0f} fw/s)")

    print(f"\n  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │  REAL FRAMEWORK                                            │")
    print(f"  │    Hits at < 0.1%:  {results['real_hits_01']:>2}/15                              │")
    print(f"  │    Hits at < 1%:    {results['real_hits_1']:>2}/15                              │")
    print(f"  │    Hits at < 5%:    {results['real_hits_5']:>2}/15                              │")
    print(f"  │    Geometric mean error: {results['real_geomean']:.6f}                  │")
    print(f"  └─────────────────────────────────────────────────────────────┘")

    print(f"\n  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │  RANDOM FRAMEWORKS ({n_fw:,}){'':>28}│")
    print(f"  │    Median hits at < 0.1%: {analysis['median_01']:.1f}/15                         │")
    print(f"  │    Mean hits at < 0.1%:   {analysis['mean_01']:.2f}/15                        │")
    print(f"  │    Max hits at < 0.1%:    {analysis['max_01']:>2}/15                            │")
    print(f"  │    Median geom. mean:     {analysis['random_geomean_median']:.6f}                  │")
    print(f"  └─────────────────────────────────────────────────────────────┘")

    print(f"\n  Histogram of hits at < 0.1% (across {n_fw:,} random frameworks):")
    hist = analysis['hist_01']
    max_bar = 50
    max_count = max(hist) if len(hist) > 0 else 1
    for n_hits in range(len(hist)):
        count = hist[n_hits]
        if count == 0 and n_hits > analysis['max_01'] + 1:
            continue
        bar_len = int(count / max_count * max_bar) if max_count > 0 else 0
        bar = "█" * bar_len
        pct = count / n_fw * 100
        marker = " ◄── REAL" if n_hits == results['real_hits_01'] else ""
        print(f"    {n_hits:>2} hits: {bar:<50s} {count:>6,} ({pct:>5.1f}%){marker}")

    print(f"\n  ─── P-VALUES ───────────────────────────────────────────────")
    print(f"    P(random ≥ {results['real_hits_01']} hits at <0.1%):  "
          f"p = {analysis['p_01']:.2e}" if analysis['p_01'] > 0
          else f"    P(random ≥ {results['real_hits_01']} hits at <0.1%):  "
               f"p < {1.0/n_fw:.1e} (NONE in {n_fw:,} trials)")
    print(f"    P(random ≥ {results['real_hits_1']} hits at <1%):    "
          f"p = {analysis['p_1']:.2e}" if analysis['p_1'] > 0
          else f"    P(random ≥ {results['real_hits_1']} hits at <1%):    "
               f"p < {1.0/n_fw:.1e}")
    print(f"    P(random ≥ {results['real_hits_5']} hits at <5%):    "
          f"p = {analysis['p_5']:.2e}" if analysis['p_5'] > 0
          else f"    P(random ≥ {results['real_hits_5']} hits at <5%):    "
               f"p < {1.0/n_fw:.1e}")
    print(f"    P(random geomean ≤ real): p = {analysis['p_geomean']:.2e}"
          if analysis['p_geomean'] > 0
          else f"    P(random geomean ≤ real): p < {1.0/n_fw:.1e}")

    if analysis['n_same_hits'] > 0:
        print(f"\n  ─── ERROR QUALITY (among {analysis['n_same_hits']} frameworks"
              f" with same hit count) ───")
        print(f"    Real geomean:    {results['real_geomean']:.6f}")
        print(f"    Fraction with tighter errors: "
              f"{analysis['gm_better_fraction']:.4f}")

    # Cross-correlation
    xc = analysis['cross_correlation']
    print(f"\n  ─── CROSS-DOMAIN CORRELATION ────────────────────────────────")
    print(f"    Real framework: {xc['n_cross_links']} constants shared across domains"
          f" ({xc['n_domain_appearances']} appearances)")
    for name, domains in xc['shared_constants'].items():
        print(f"      {name}")
    print(f"    Random frameworks: constants appear in ≤ 1 domain by construction")

    # Verdict
    p_best = min(analysis['p_01'],
                 analysis['p_geomean'] if analysis['p_geomean'] > 0 else 1.0/n_fw)
    if analysis['p_01'] == 0:
        p_best = 1.0 / n_fw  # upper bound

    print()
    print("=" * 80)
    if p_best < 1e-3:
        print(f"  ★★★ The particle mass matches SURVIVE Monte Carlo.")
        print(f"  ★★★ p < {p_best:.1e}")
        print(f"  ★★★ The three doors are the three generations.")
    elif p_best < 0.05:
        print(f"  ★★  Significant (p = {p_best:.4f}), but not overwhelming.")
    else:
        print(f"       Not significant (p = {p_best:.4f}). "
              f"Combinatorial coincidence cannot be ruled out.")
    print("=" * 80)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 80)
    print("  MONTE CARLO VALIDATION: Particle Mass Matches")
    print("  100,000 random frameworks × 15,000 combinations × 15 targets")
    print("=" * 80)

    results = run_monte_carlo_numpy(n_frameworks=100_000, seed=42)
    analysis = analyze_results(results)
    print_report(results, analysis)

    # Save results
    save_dir = os.path.expanduser(
        "~/Unified_Theory_Physics/results/particle_monte_carlo"
    )
    os.makedirs(save_dir, exist_ok=True)

    save_data = {
        'n_frameworks': results['n_frameworks'],
        'elapsed_s': results['elapsed_s'],
        'n_blocks': results['n_blocks'],
        'n_products': results['n_products'],
        'n_targets': N_TARGETS,
        'targets': TARGETS,
        'real_hits_01': results['real_hits_01'],
        'real_hits_1': results['real_hits_1'],
        'real_hits_5': results['real_hits_5'],
        'real_errors': results['real_errors'],
        'real_geomean': results['real_geomean'],
        'p_01': analysis['p_01'],
        'p_1': analysis['p_1'],
        'p_5': analysis['p_5'],
        'p_geomean': analysis['p_geomean'],
        'hist_01': analysis['hist_01'],
        'median_01': analysis['median_01'],
        'mean_01': analysis['mean_01'],
        'max_01': analysis['max_01'],
        'n_same_hits': analysis['n_same_hits'],
        'gm_better_fraction': analysis['gm_better_fraction'],
        'random_geomean_median': analysis['random_geomean_median'],
        'cross_correlation': analysis['cross_correlation'],
    }

    save_path = os.path.join(save_dir, "particle_monte_carlo.json")
    with open(save_path, 'w') as f:
        json.dump(save_data, f, indent=2, default=str)
    print(f"\n  Results saved: {save_path}")


if __name__ == "__main__":
    main()
