#!/usr/bin/env python3
"""
gamma_convergence.py — Galaxy correlation exponent convergence study (JAX-accelerated)
======================================================================================

The finite-size QC at N_half=3 gives γ≈2.6 instead of the observed 1.8.
Hypothesis: the mismatch is a finite-size effect. More BGS nodes →
proper cosmic-web filaments → correct γ.

Prediction: γ → 1/σ₄ = 1.788 as N → ∞

Uses JAX on Apple Metal GPU for the 6D lattice generation bottleneck.
Scipy handles Voronoi (no JAX equivalent).

Run: python3 simulation/gamma_convergence.py
"""

import sys, os, time, warnings
import numpy as np
from collections import Counter
from scipy.spatial.distance import pdist

warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'CLEAN'))

from core.constants import PHI
from core.spectrum import R_OUTER
from geometry.voronoi_qc import (
    assign_types, voronoi_cell_faces, icosahedral_axes,
)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── JAX setup ────────────────────────────────────────────────────
try:
    import jax
    import jax.numpy as jnp
    JAX_AVAILABLE = True
    print(f"  JAX {jax.__version__} on {jax.devices()[0].platform.upper()}")
except ImportError:
    JAX_AVAILABLE = False
    print("  JAX not available — falling back to numpy")

VIZDIR = os.path.join(ROOT, 'simulation', 'visualizations')
os.makedirs(VIZDIR, exist_ok=True)

GAMMA_TARGET = 1.8
GAMMA_FRAMEWORK = 1.0 / R_OUTER  # 1.788


# ── JAX-accelerated QC generation ────────────────────────────────

def build_projection_matrices():
    """Build 3×6 parallel/perpendicular projection matrices (Elser 1986)."""
    tau = PHI
    verts = np.array([
        [1, tau, 0], [-1, tau, 0], [1, -tau, 0], [-1, -tau, 0],
        [0, 1, tau], [0, -1, tau], [0, 1, -tau], [0, -1, -tau],
        [tau, 0, 1], [-tau, 0, 1], [tau, 0, -1], [-tau, 0, -1]
    ], dtype=np.float64)
    sel = verts[[0, 2, 4, 6, 8, 10]]
    norms = np.linalg.norm(sel, axis=1, keepdims=True)
    e_par = (sel / norms).T

    tau_conj = -1.0 / tau
    sel_conj = np.array([
        [1, tau_conj, 0], [1, -tau_conj, 0],
        [0, 1, tau_conj], [0, 1, -tau_conj],
        [tau_conj, 0, 1], [tau_conj, 0, -1],
    ], dtype=np.float64)
    norms_c = np.linalg.norm(sel_conj, axis=1, keepdims=True)
    e_perp = (sel_conj / norms_c).T

    scale = np.sqrt(2.0 / 3.0)
    return scale * e_par, scale * e_perp


def build_quasicrystal_jax(N_half, target_range=(2000, 5000)):
    """Generate icosahedral QC via cut-and-project, JAX-accelerated 6D→3D."""
    P_par, P_perp = build_projection_matrices()

    if JAX_AVAILABLE:
        # Build 6D lattice on GPU
        coords_1d = jnp.arange(-N_half, N_half + 1, dtype=jnp.float32)
        grids = jnp.meshgrid(*([coords_1d] * 6), indexing='ij')
        lattice = jnp.stack([g.ravel() for g in grids], axis=1)

        # Project on GPU (float32 for speed, sufficient for QC)
        P_par_j = jnp.array(P_par.T, dtype=jnp.float32)
        P_perp_j = jnp.array(P_perp.T, dtype=jnp.float32)

        par = lattice @ P_par_j
        perp = lattice @ P_perp_j
        perp_norms = jnp.linalg.norm(perp, axis=1)

        # Auto-tune acceptance radius (on GPU)
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
        # Transfer filtered results to numpy (for scipy Voronoi)
        par_out = np.array(par[mask], dtype=np.float64)
        perp_out = np.array(perp[mask], dtype=np.float64)

        # Free GPU memory
        del lattice, grids, par, perp, perp_norms, mask
    else:
        # Numpy fallback
        coords_1d = np.arange(-N_half, N_half + 1)
        grids = np.meshgrid(*([coords_1d] * 6), indexing='ij')
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
        par_out = par[mask]
        perp_out = perp[mask]

    return par_out, perp_out, R_accept


def correlation_function(pts, n_bins=40, n_sample=3000):
    """Two-point correlation ξ(r) with power-law fit using log-spaced bins."""
    n = len(pts)
    if n > n_sample:
        np.random.seed(42)
        idx = np.random.choice(n, n_sample, replace=False)
        sample = pts[idx]
    else:
        sample = pts.copy()

    dists = pdist(sample)
    # Log-spaced bins for better power-law sensitivity
    r_min = np.percentile(dists, 3)
    r_max = np.percentile(dists, 60)
    r_bins = np.logspace(np.log10(r_min), np.log10(r_max), n_bins + 1)
    r_centers = np.sqrt(r_bins[:-1] * r_bins[1:])  # geometric mean
    dr = np.diff(r_bins)

    counts = np.histogram(dists, bins=r_bins)[0].astype(float)

    # Expected for uniform random in a sphere
    box_extent = np.max(np.abs(sample), axis=0)
    V_box = np.prod(2 * box_extent)
    n_s = len(sample)
    rho = n_s / max(V_box, 1e-15)
    n_pairs = n_s * (n_s - 1) / 2
    # Shell volume for each log-spaced bin
    shell_vol = (4.0 / 3.0) * np.pi * (r_bins[1:]**3 - r_bins[:-1]**3)
    expected = n_pairs * shell_vol * rho / V_box

    xi = np.where(expected > 5, counts / expected - 1, 0)

    # Power-law fit: use bins where ξ > 0.01 and in intermediate range
    n_skip = max(3, n_bins // 10)
    fit_mask = (xi > 0.01) & np.arange(n_bins) >= n_skip
    fit_mask[-(n_bins // 8):] = False  # skip boundary bins
    gamma = 0.0
    r0 = 0.0
    if fit_mask.sum() > 5:
        log_r = np.log10(r_centers[fit_mask])
        log_xi = np.log10(np.maximum(xi[fit_mask], 1e-10))
        coeffs = np.polyfit(log_r, log_xi, 1)
        gamma = -coeffs[0]
        r0 = 10**(coeffs[1] / gamma) if gamma > 0 else 0

    return r_centers, xi, gamma, r0, fit_mask


def run_at_size(N_half, target_range=None):
    """Run QC generation + Voronoi + correlation at given size."""
    if target_range is None:
        base = 3000
        scale = (N_half / 3.0) ** 3
        lo = int(base * scale * 0.8)
        hi = int(base * scale * 1.5)
        target_range = (lo, hi)

    t0 = time.time()
    n_lattice = (2 * N_half + 1) ** 6
    print(f"\n  N_half={N_half}: generating 6D lattice ({n_lattice:,} points)...")
    sys.stdout.flush()

    pts, pts_perp, R_accept = build_quasicrystal_jax(N_half=N_half, target_range=target_range)
    types = assign_types(pts_perp, R_accept)
    n_pts = len(pts)
    dt_qc = time.time() - t0
    print(f"    QC points: {n_pts:,} ({dt_qc:.1f}s)")
    sys.stdout.flush()

    # Voronoi
    t1 = time.time()
    print(f"    Computing Voronoi...")
    sys.stdout.flush()
    cells = voronoi_cell_faces(pts, types)
    n_cells = len(cells)
    dt_vor = time.time() - t1
    print(f"    Interior cells: {n_cells:,} ({dt_vor:.1f}s)")
    sys.stdout.flush()

    # BGS cells
    bgs_idx = [i for i in cells if cells[i]['type'] == 'BGS']
    n_bgs = len(bgs_idx)
    bgs_frac = n_bgs / max(n_cells, 1)
    print(f"    BGS cells: {n_bgs:,} ({bgs_frac*100:.1f}%)")
    sys.stdout.flush()

    # Correlation on BGS points
    t2 = time.time()
    bgs_pts = pts[bgs_idx]
    r_centers, xi, gamma, r0, fit_mask = correlation_function(bgs_pts)
    dt_corr = time.time() - t2
    print(f"    γ = {gamma:.3f} (target: {GAMMA_TARGET}, framework: {GAMMA_FRAMEWORK:.3f})")
    print(f"    Correlation time: {dt_corr:.1f}s")

    # Also compute on ALL points for comparison
    _, _, gamma_all, _, _ = correlation_function(pts)
    print(f"    γ (all points) = {gamma_all:.3f}")

    total = time.time() - t0
    print(f"    Total: {total:.1f}s")
    sys.stdout.flush()

    return {
        'N_half': N_half,
        'n_pts': n_pts,
        'n_cells': n_cells,
        'n_bgs': n_bgs,
        'bgs_frac': bgs_frac,
        'gamma_bgs': gamma,
        'gamma_all': gamma_all,
        'r0': r0,
        'r_centers': r_centers,
        'xi': xi,
        'fit_mask': fit_mask,
        'time_s': total,
    }


def main():
    print("=" * 70)
    print("  GALAXY CORRELATION CONVERGENCE STUDY (JAX-accelerated)")
    print(f"  Target: γ = {GAMMA_TARGET}")
    print(f"  Framework prediction: 1/σ₄ = {GAMMA_FRAMEWORK:.4f}")
    print("=" * 70)
    sys.stdout.flush()

    # Progressive sizes
    sizes = [3, 4, 5, 6]
    results = []

    for N_half in sizes:
        try:
            r = run_at_size(N_half)
            results.append(r)
        except MemoryError:
            print(f"\n  N_half={N_half}: OUT OF MEMORY — stopping here")
            break
        except Exception as e:
            import traceback
            print(f"\n  N_half={N_half}: ERROR — {e}")
            traceback.print_exc()
            break

    if not results:
        print("\n  No results to plot!")
        return

    # Summary table
    print(f"\n  {'='*70}")
    print(f"  CONVERGENCE SUMMARY")
    print(f"  {'='*70}")
    print(f"  {'N_half':>6} {'Points':>8} {'Cells':>8} {'BGS':>6} {'γ_BGS':>8} {'γ_all':>8} {'Δγ':>8} {'Time':>8}")
    print(f"  {'─'*6} {'─'*8} {'─'*8} {'─'*6} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")
    for r in results:
        delta = abs(r['gamma_bgs'] - GAMMA_TARGET)
        print(f"  {r['N_half']:>6} {r['n_pts']:>8,} {r['n_cells']:>8,} {r['n_bgs']:>6,} "
              f"{r['gamma_bgs']:>8.3f} {r['gamma_all']:>8.3f} {delta:>8.3f} {r['time_s']:>7.1f}s")

    print(f"\n  Target γ = {GAMMA_TARGET}")
    print(f"  Framework 1/σ₄ = {GAMMA_FRAMEWORK:.4f}")

    # Extrapolate if we have enough points
    coeffs = None
    gamma_inf = None
    if len(results) >= 3:
        ns = [r['n_bgs'] for r in results]
        gs = [r['gamma_bgs'] for r in results]
        inv_n = [1.0 / n for n in ns]
        coeffs = np.polyfit(inv_n, gs, 1)
        gamma_inf = coeffs[1]
        print(f"\n  Linear extrapolation γ(∞) = {gamma_inf:.3f}")
        print(f"  Error vs 1.8: {abs(gamma_inf - 1.8) / 1.8 * 100:.1f}%")
        print(f"  Error vs 1/σ₄: {abs(gamma_inf - GAMMA_FRAMEWORK) / GAMMA_FRAMEWORK * 100:.1f}%")

    sys.stdout.flush()

    # ─── VISUALIZATION ────────────────────────────────────────────

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. γ convergence
    ax = axes[0, 0]
    ns = [r['n_bgs'] for r in results]
    gs_bgs = [r['gamma_bgs'] for r in results]
    gs_all = [r['gamma_all'] for r in results]
    ax.plot(ns, gs_bgs, 'o-', color='#FF4444', markersize=10, linewidth=2, label='γ (BGS only)')
    ax.plot(ns, gs_all, 's--', color='#4444FF', markersize=8, linewidth=1.5, label='γ (all points)')
    ax.axhline(GAMMA_TARGET, color='green', linewidth=2, linestyle='--', label=f'Galaxy surveys γ={GAMMA_TARGET}')
    ax.axhline(GAMMA_FRAMEWORK, color='gold', linewidth=2, linestyle=':', label=f'1/σ₄={GAMMA_FRAMEWORK:.3f}')

    if coeffs is not None:
        ns_ext = np.linspace(ns[0], ns[-1] * 5, 100)
        inv_ext = 1.0 / ns_ext
        gamma_ext = coeffs[0] * inv_ext + coeffs[1]
        ax.plot(ns_ext, gamma_ext, '--', color='#FF4444', alpha=0.4, linewidth=1)
        ax.scatter([ns_ext[-1]], [gamma_inf], marker='*', s=200, color='#FF4444', zorder=5,
                   label=f'γ(∞) = {gamma_inf:.2f}')

    ax.set_xlabel('Number of BGS cells', fontsize=13)
    ax.set_ylabel('Power-law exponent γ', fontsize=13)
    ax.set_title('Galaxy Correlation Exponent Convergence\nξ(r) ∝ r⁻ᵞ', fontsize=14)
    ax.legend(fontsize=10)
    ax.set_xscale('log')

    # 2. ξ(r) at each size
    ax = axes[0, 1]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    for idx_r, r in enumerate(results):
        mask = r['xi'] > 0
        if mask.sum() > 0:
            ax.loglog(r['r_centers'][mask], r['xi'][mask], 'o-', color=colors[idx_r % len(colors)],
                      markersize=3, linewidth=1.5, alpha=0.8,
                      label=f"N={r['N_half']} ({r['n_bgs']} BGS) γ={r['gamma_bgs']:.2f}")
    r_ref = np.linspace(0.5, 10, 100)
    xi_ref = (r_ref / 2.0) ** (-GAMMA_TARGET)
    ax.loglog(r_ref, xi_ref, 'k--', linewidth=1, alpha=0.5, label=f'r⁻¹·⁸ (galaxy)')
    ax.set_xlabel('r (lattice units)', fontsize=13)
    ax.set_ylabel('ξ(r)', fontsize=13)
    ax.set_title('Two-Point Correlation Functions', fontsize=14)
    ax.legend(fontsize=9)
    ax.set_ylim(1e-2, 1e2)

    # 3. BGS count scaling
    ax = axes[1, 0]
    n_halfs = [r['N_half'] for r in results]
    n_pts_list = [r['n_pts'] for r in results]
    n_bgs_list = [r['n_bgs'] for r in results]
    ax.semilogy(n_halfs, n_pts_list, 'o-', color='#4444FF', markersize=10, linewidth=2, label='Total QC points')
    ax.semilogy(n_halfs, n_bgs_list, 's-', color='#FF4444', markersize=10, linewidth=2, label='BGS cells')
    ax.set_xlabel('N_half', fontsize=13)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title('Point Set Scaling with N_half', fontsize=14)
    ax.legend(fontsize=11)

    # 4. BGS fraction
    ax = axes[1, 1]
    bgs_fracs = [r['bgs_frac'] * 100 for r in results]
    ax.plot(n_halfs, bgs_fracs, 'o-', color='#FF4444', markersize=10, linewidth=2)
    ax.axhline(100 / PHI**3, color='gold', linewidth=2, linestyle='--', label=f'1/φ³ = {100/PHI**3:.1f}%')
    ax.set_xlabel('N_half', fontsize=13)
    ax.set_ylabel('BGS fraction (%)', fontsize=13)
    ax.set_title('Matter Fraction vs Lattice Size', fontsize=14)
    ax.legend(fontsize=11)

    plt.suptitle('Quasicrystal Finite-Size Convergence Study (JAX-accelerated)', fontsize=16, y=1.02)
    plt.tight_layout()
    outpath = os.path.join(VIZDIR, '13_gamma_convergence.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n  Saved: {outpath}")

    # Save results
    import json
    res_dir = os.path.join(ROOT, 'results', 'simulation')
    os.makedirs(res_dir, exist_ok=True)
    res_path = os.path.join(res_dir, 'gamma_convergence.json')
    save_data = [{
        'N_half': r['N_half'], 'n_pts': r['n_pts'], 'n_cells': r['n_cells'],
        'n_bgs': r['n_bgs'], 'bgs_frac': round(r['bgs_frac'], 4),
        'gamma_bgs': round(r['gamma_bgs'], 4), 'gamma_all': round(r['gamma_all'], 4),
        'time_s': round(r['time_s'], 1)
    } for r in results]
    with open(res_path, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"  Saved: {res_path}")


if __name__ == '__main__':
    main()
