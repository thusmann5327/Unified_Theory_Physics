#!/usr/bin/env python3
"""
gamma_fast.py — Fast γ convergence (NO Voronoi), JAX-accelerated, DB-backed
============================================================================

Skips the Voronoi bottleneck entirely. Uses only:
  1. JAX 6D→3D cut-and-project (GPU)
  2. assign_types for BGS classification
  3. Two-point correlation ξ(r) on BGS cloud
  4. Power-law fit for γ

Runs N_half = 3..10 and stores everything in PostgreSQL.

Run: python3 simulation/gamma_fast.py
"""

import sys, os, time, warnings
import numpy as np
from scipy.spatial.distance import pdist
from scipy.optimize import curve_fit

warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'CLEAN'))
sys.path.insert(0, ROOT)

from core.constants import PHI
from core.spectrum import R_OUTER
from geometry.voronoi_qc import assign_types, build_projection_matrices

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── JAX setup ────────────────────────────────────────────────────
try:
    import jax
    import jax.numpy as jnp
    JAX_OK = True
    _dev = jax.devices()[0]
    print(f"  JAX {jax.__version__} on {_dev.platform.upper()}")
except ImportError:
    JAX_OK = False
    print("  JAX not available — numpy fallback")

# ── Database ─────────────────────────────────────────────────────
try:
    from database.universe_db import UniverseDB
    DB_OK = True
except ImportError:
    DB_OK = False
    print("  Database module not available — results to JSON only")

VIZDIR = os.path.join(ROOT, 'simulation', 'visualizations')
os.makedirs(VIZDIR, exist_ok=True)

GAMMA_TARGET = 1.8
GAMMA_FRAMEWORK = 1.0 / R_OUTER  # 1.788


# ── JAX-accelerated QC generation (NO Voronoi) ──────────────────

def build_qc_jax(N_half, target_range=(2000, 5000)):
    """Generate icosahedral QC via 6D→3D projection, JAX-accelerated."""
    P_par, P_perp = build_projection_matrices()

    t0 = time.time()
    if JAX_OK:
        coords = jnp.arange(-N_half, N_half + 1, dtype=jnp.float32)
        grids = jnp.meshgrid(*([coords] * 6), indexing='ij')
        lattice = jnp.stack([g.ravel() for g in grids], axis=1)

        P_par_j = jnp.array(P_par.T, dtype=jnp.float32)
        P_perp_j = jnp.array(P_perp.T, dtype=jnp.float32)

        par = lattice @ P_par_j
        perp = lattice @ P_perp_j
        perp_norms = jnp.linalg.norm(perp, axis=1)

        # Auto-tune acceptance radius
        R_accept = float(jnp.max(perp_norms)) * 0.5
        for _ in range(40):
            count = int(jnp.sum(perp_norms < R_accept))
            if count < target_range[0]:
                R_accept *= 1.05
            elif count > target_range[1]:
                R_accept *= 0.95
            else:
                break

        mask = perp_norms < R_accept
        par_np = np.array(par[mask], dtype=np.float64)
        perp_np = np.array(perp[mask], dtype=np.float64)
        del lattice, grids, par, perp, perp_norms, mask
    else:
        coords = np.arange(-N_half, N_half + 1)
        grids = np.meshgrid(*([coords] * 6), indexing='ij')
        lattice = np.stack([g.ravel() for g in grids], axis=1).astype(np.float64)

        par = lattice @ P_par.T
        perp = lattice @ P_perp.T
        perp_norms = np.linalg.norm(perp, axis=1)

        R_accept = np.max(perp_norms) * 0.5
        for _ in range(40):
            count = (perp_norms < R_accept).sum()
            if count < target_range[0]:
                R_accept *= 1.05
            elif count > target_range[1]:
                R_accept *= 0.95
            else:
                break

        mask = perp_norms < R_accept
        par_np = par[mask]
        perp_np = perp[mask]

    dt = time.time() - t0
    return par_np, perp_np, R_accept, dt


def correlation_function(pts, n_bins=40, n_sample=4000, n_random_mult=3):
    """Two-point ξ(r) via Landy-Szalay estimator with random catalog.

    ξ(r) = (DD - 2DR + RR) / RR

    Uses a random catalog matching the data geometry (sphere) to
    properly handle edge corrections.
    """
    n = len(pts)
    if n < 30:
        return np.array([]), np.array([]), 0.0, 0.0, np.array([], dtype=bool)

    if n > n_sample:
        np.random.seed(42)
        idx = np.random.choice(n, n_sample, replace=False)
        sample = pts[idx]
    else:
        sample = pts.copy()

    n_s = len(sample)

    # Generate random catalog in same volume (sphere)
    center = np.mean(sample, axis=0)
    radii = np.linalg.norm(sample - center, axis=1)
    R_eff = np.percentile(radii, 95)

    n_rand = n_s * n_random_mult
    rng = np.random.RandomState(123)
    # Uniform in sphere via rejection sampling
    rand_pts = []
    while len(rand_pts) < n_rand:
        batch = rng.uniform(-R_eff, R_eff, size=(n_rand * 2, 3)) + center
        r_batch = np.linalg.norm(batch - center, axis=1)
        good = batch[r_batch < R_eff]
        rand_pts.append(good)
    rand_pts = np.vstack(rand_pts)[:n_rand]

    # Pair distances
    dd_dists = pdist(sample)
    rr_dists = pdist(rand_pts)

    # Cross distances (subsample for speed)
    from scipy.spatial.distance import cdist
    dr_dists = cdist(sample, rand_pts).ravel()

    # Log-spaced bins
    r_min = np.percentile(dd_dists, 1)
    r_max = np.percentile(dd_dists, 50)
    r_bins = np.logspace(np.log10(max(r_min, 1e-10)), np.log10(r_max), n_bins + 1)
    r_centers = np.sqrt(r_bins[:-1] * r_bins[1:])

    DD = np.histogram(dd_dists, bins=r_bins)[0].astype(float)
    RR = np.histogram(rr_dists, bins=r_bins)[0].astype(float)
    DR = np.histogram(dr_dists, bins=r_bins)[0].astype(float)

    # Normalize counts
    n_dd = n_s * (n_s - 1) / 2.0
    n_rr = n_rand * (n_rand - 1) / 2.0
    n_dr = n_s * n_rand

    DD_norm = DD / max(n_dd, 1)
    RR_norm = RR / max(n_rr, 1)
    DR_norm = DR / max(n_dr, 1)

    # Landy-Szalay estimator
    xi = np.where(RR_norm > 1e-15,
                  (DD_norm - 2 * DR_norm + RR_norm) / RR_norm,
                  0)

    # Power-law fit in intermediate range
    n_skip = max(3, n_bins // 6)
    n_end = max(2, n_bins // 5)
    fit_mask = (xi > 0.01) & (np.arange(n_bins) >= n_skip)
    fit_mask[-n_end:] = False

    gamma = 0.0
    r0 = 0.0
    if fit_mask.sum() > 5:
        log_r = np.log10(r_centers[fit_mask])
        log_xi = np.log10(np.clip(xi[fit_mask], 1e-10, None))
        coeffs = np.polyfit(log_r, log_xi, 1)
        gamma = -coeffs[0]
        r0 = 10**(coeffs[1] / max(gamma, 0.01))

    return r_centers, xi, gamma, r0, fit_mask


def main():
    print("=" * 70)
    print("  FAST GAMMA CONVERGENCE (No Voronoi, JAX-accelerated)")
    print(f"  Target: γ = {GAMMA_TARGET}")
    print(f"  Framework prediction: 1/σ₄ = {GAMMA_FRAMEWORK:.4f}")
    print("=" * 70)
    sys.stdout.flush()

    # ── Database setup ───────────────────────────────────────────
    db = None
    if DB_OK:
        try:
            db = UniverseDB()
            db.init_schema()
            print("  Database: connected")
        except Exception as e:
            print(f"  Database: {e} — results to JSON only")
            db = None
    sys.stdout.flush()

    # ── Progressive sizes ────────────────────────────────────────
    sizes = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []

    for N_half in sizes:
        n_lattice = (2 * N_half + 1) ** 6
        print(f"\n  N_half={N_half}: 6D lattice ({n_lattice:,} points)...")
        sys.stdout.flush()

        # Scale target range with N_half
        base = 3000
        scale = (N_half / 3.0) ** 3
        lo = int(base * scale * 0.8)
        hi = int(base * scale * 1.5)

        try:
            pts, pts_perp, R_accept, dt_gen = build_qc_jax(
                N_half, target_range=(lo, hi))
        except Exception as e:
            print(f"    FAILED: {e}")
            import traceback
            traceback.print_exc()
            break

        n_pts = len(pts)
        print(f"    QC points: {n_pts:,} ({dt_gen:.1f}s)")
        sys.stdout.flush()

        # Type assignment (fast — no Voronoi)
        t1 = time.time()
        types = assign_types(pts_perp, R_accept)
        dt_types = time.time() - t1

        bgs_mask = types == 'BGS'
        n_bgs = int(bgs_mask.sum())
        bgs_frac = n_bgs / max(n_pts, 1)
        print(f"    BGS: {n_bgs:,} ({bgs_frac*100:.1f}%) [{dt_types:.1f}s]")
        sys.stdout.flush()

        # Interior clip (avoid boundary artifacts)
        r_pts = np.linalg.norm(pts, axis=1)
        clip = r_pts < 0.75 * np.max(r_pts)
        bgs_interior = pts[bgs_mask & clip]
        n_bgs_int = len(bgs_interior)
        print(f"    Interior BGS: {n_bgs_int:,}")

        # Two-point correlation
        t2 = time.time()
        r_centers, xi, gamma, r0, fit_mask = correlation_function(bgs_interior)
        dt_corr = time.time() - t2

        # Also on all interior points
        all_interior = pts[clip]
        _, _, gamma_all, _, _ = correlation_function(all_interior)

        print(f"    γ_BGS = {gamma:.3f}  γ_all = {gamma_all:.3f}  [{dt_corr:.1f}s]")
        sys.stdout.flush()

        total_time = dt_gen + dt_types + dt_corr

        # Store in database
        if db is not None:
            try:
                batch_id = db.store_points(pts, pts_perp, types, N_half)
                db.store_gamma(N_half, n_bgs_int, float(gamma))
                db.store_computation(
                    N_half, n_pts, n_bgs, float(bgs_frac),
                    float(gamma), float(gamma_all), float(total_time))
                print(f"    Stored in database (batch {batch_id})")
            except Exception as e:
                db.conn.rollback()
                print(f"    DB store failed: {e}")
        sys.stdout.flush()

        results.append({
            'N_half': N_half,
            'n_pts': n_pts,
            'n_bgs': n_bgs,
            'n_bgs_int': n_bgs_int,
            'bgs_frac': bgs_frac,
            'gamma_bgs': gamma,
            'gamma_all': gamma_all,
            'r0': r0,
            'r_centers': r_centers,
            'xi': xi,
            'fit_mask': fit_mask,
            'time_s': total_time,
        })

    if not results:
        print("\n  No results!")
        return

    # ── Summary table ────────────────────────────────────────────
    print(f"\n  {'='*70}")
    print(f"  CONVERGENCE SUMMARY")
    print(f"  {'='*70}")
    print(f"  {'N':>4} {'Points':>8} {'BGS':>7} {'BGS_int':>8} "
          f"{'γ_BGS':>8} {'γ_all':>8} {'Δγ':>7} {'Time':>7}")
    print(f"  {'─'*4} {'─'*8} {'─'*7} {'─'*8} "
          f"{'─'*8} {'─'*8} {'─'*7} {'─'*7}")
    for r in results:
        dg = abs(r['gamma_bgs'] - GAMMA_TARGET)
        print(f"  {r['N_half']:4d} {r['n_pts']:8,} {r['n_bgs']:7,} "
              f"{r['n_bgs_int']:8,} {r['gamma_bgs']:8.3f} "
              f"{r['gamma_all']:8.3f} {dg:7.3f} {r['time_s']:6.1f}s")

    print(f"\n  Target γ = {GAMMA_TARGET}")
    print(f"  Framework 1/σ₄ = {GAMMA_FRAMEWORK:.4f}")

    # ── Extrapolation ────────────────────────────────────────────
    ns = np.array([r['N_half'] for r in results])
    gs = np.array([r['gamma_bgs'] for r in results])

    # Use N_half >= 4 for fits (N=3 is too small)
    use = ns >= 4
    gamma_inf = None
    fit_params = None

    if use.sum() >= 3:
        def convergence_model(N, g_inf, A, beta):
            return g_inf + A * N**(-beta)

        try:
            popt, pcov = curve_fit(
                convergence_model, ns[use], gs[use],
                p0=[1.8, 10, 1.0],
                bounds=([0.5, 0, 0.1], [5.0, 200, 5.0]),
                maxfev=10000)
            gamma_inf, A, beta = popt
            g_err = np.sqrt(pcov[0, 0]) if pcov[0, 0] > 0 else 0
            fit_params = popt

            print(f"\n  Power-law extrapolation:")
            print(f"    γ(∞) = {gamma_inf:.4f} ± {g_err:.4f}")
            print(f"    A = {A:.2f}, β = {beta:.2f}")
            pct = abs(gamma_inf - GAMMA_TARGET) / GAMMA_TARGET * 100
            print(f"    Error vs target: {pct:.1f}%")
            pct_f = abs(gamma_inf - GAMMA_FRAMEWORK) / GAMMA_FRAMEWORK * 100
            print(f"    Error vs 1/σ₄:  {pct_f:.1f}%")
        except Exception as e:
            print(f"\n  Power-law fit failed: {e}")

        # Linear fallback
        coeffs_lin = np.polyfit(1.0 / ns[use], gs[use], 1)
        gamma_lin = coeffs_lin[1]
        print(f"    Linear extrapolation: γ(∞) = {gamma_lin:.4f}")

    sys.stdout.flush()

    # ── Visualization ────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. γ convergence vs N_half
    ax = axes[0, 0]
    ax.plot(ns, gs, 'o-', color='#FF4444', markersize=10, lw=2, label='γ_BGS')
    ga = [r['gamma_all'] for r in results]
    ax.plot(ns, ga, 's--', color='#4444FF', markersize=8, lw=1.5, label='γ_all')
    ax.axhline(GAMMA_TARGET, color='green', lw=2, ls='--',
               label=f'Galaxy surveys γ={GAMMA_TARGET}')
    ax.axhline(GAMMA_FRAMEWORK, color='gold', lw=2, ls=':',
               label=f'1/σ₄={GAMMA_FRAMEWORK:.3f}')
    if fit_params is not None:
        ns_ext = np.linspace(ns[use].min(), 30, 100)
        ax.plot(ns_ext, convergence_model(ns_ext, *fit_params),
                '--', color='#FF4444', alpha=0.4, lw=1)
        ax.scatter([30], [gamma_inf], marker='*', s=200, color='#FF4444',
                   zorder=5, label=f'γ(∞) = {gamma_inf:.2f}')
    ax.set_xlabel('N_half', fontsize=13)
    ax.set_ylabel('γ', fontsize=13)
    ax.set_title('Galaxy Correlation Exponent Convergence\n(No Voronoi)', fontsize=14)
    ax.legend(fontsize=9)

    # 2. ξ(r) at each size
    ax = axes[0, 1]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
              '#FFEAA7', '#DDA0DD', '#FF9F43', '#6C5CE7']
    for i, r in enumerate(results):
        mask = r['xi'] > 0
        if mask.sum() > 0:
            ax.loglog(r['r_centers'][mask], r['xi'][mask], 'o-',
                      color=colors[i % len(colors)], markersize=3, lw=1.5,
                      alpha=0.8,
                      label=f"N={r['N_half']} ({r['n_bgs_int']} BGS) γ={r['gamma_bgs']:.2f}")
    r_ref = np.linspace(0.5, 10, 100)
    ax.loglog(r_ref, (r_ref / 2.0)**(-GAMMA_TARGET), 'k--', lw=1,
              alpha=0.5, label=f'r⁻¹·⁸')
    ax.set_xlabel('r (lattice units)', fontsize=13)
    ax.set_ylabel('ξ(r)', fontsize=13)
    ax.set_title('Two-Point Correlation Functions', fontsize=14)
    ax.legend(fontsize=8)
    ax.set_ylim(1e-2, 1e2)

    # 3. γ vs 1/N (extrapolation view)
    ax = axes[1, 0]
    inv_ns = 1.0 / ns
    ax.plot(inv_ns, gs, 'o-', color='#FF4444', markersize=10, lw=2, label='Measured γ')
    ax.axhline(GAMMA_TARGET, color='green', lw=2, ls='--',
               label=f'Target {GAMMA_TARGET}')
    ax.axhline(GAMMA_FRAMEWORK, color='gold', lw=2, ls=':',
               label=f'1/σ₄={GAMMA_FRAMEWORK:.3f}')
    if gamma_inf is not None:
        ax.scatter([0], [gamma_inf], marker='*', s=200, color='#FF4444',
                   zorder=5, label=f'γ(∞) = {gamma_inf:.2f}')
    ax.set_xlabel('1/N_half → 0', fontsize=13)
    ax.set_ylabel('γ', fontsize=13)
    ax.set_title('Extrapolation to N → ∞', fontsize=14)
    ax.set_xlim(left=-0.02)
    ax.legend(fontsize=10)

    # 4. BGS fraction and point scaling
    ax = axes[1, 1]
    n_halfs = [r['N_half'] for r in results]
    bgs_fracs = [r['bgs_frac'] * 100 for r in results]
    ax.plot(n_halfs, bgs_fracs, 'o-', color='#FF4444', markersize=10, lw=2,
            label='BGS fraction')
    ax.axhline(100 / PHI**3, color='gold', lw=2, ls='--',
               label=f'1/φ³ = {100/PHI**3:.1f}%')
    ax.set_xlabel('N_half', fontsize=13)
    ax.set_ylabel('BGS fraction (%)', fontsize=13)
    ax.set_title('Matter Fraction vs Lattice Size', fontsize=14)
    ax.legend(fontsize=11)

    plt.suptitle('Fast Gamma Convergence (JAX, No Voronoi)',
                 fontsize=16, y=1.02)
    plt.tight_layout()
    outpath = os.path.join(VIZDIR, '14_gamma_convergence_fast.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n  Saved: {outpath}")

    # ── Save JSON ────────────────────────────────────────────────
    import json
    res_dir = os.path.join(ROOT, 'results', 'simulation')
    os.makedirs(res_dir, exist_ok=True)
    res_path = os.path.join(res_dir, 'gamma_fast.json')
    save_data = [{
        'N_half': r['N_half'], 'n_pts': r['n_pts'],
        'n_bgs': r['n_bgs'], 'n_bgs_int': r['n_bgs_int'],
        'bgs_frac': round(r['bgs_frac'], 4),
        'gamma_bgs': round(r['gamma_bgs'], 4),
        'gamma_all': round(r['gamma_all'], 4),
        'time_s': round(r['time_s'], 1),
    } for r in results]
    if gamma_inf is not None:
        save_data.append({'extrapolation': {
            'gamma_inf': round(float(gamma_inf), 4),
            'target': GAMMA_TARGET,
            'framework': round(GAMMA_FRAMEWORK, 4),
        }})
    with open(res_path, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"  Saved: {res_path}")

    # ── Database stats ───────────────────────────────────────────
    if db is not None:
        print(f"\n  {'='*40}")
        db.stats()
        db.close()


if __name__ == '__main__':
    main()
