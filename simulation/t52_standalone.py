#!/usr/bin/env python3
"""
T52 Galaxy Evolution — Standalone Reproduction Script
=====================================================

Reproduces the T52 galaxy model from scratch, no database required.
This script is self-contained: it loads initial vertex positions from
a JSON file, evolves them under the Husmann Decomposition spring physics
engine, and saves checkpoints + rendered images at regular intervals.

THE PHYSICS (no forces are coded — structure emerges from stiffness)
====================================================================

The simulation evolves ~6700 vertices in 3D, connected by springs whose
stiffness depends on vertex TYPE. There are 7 vertex types formed from
three "metals" — Bronze (B), Gold (G), Silver (S) — and their combinations:

    BGS  — all three metals, matter nodes (galaxy cores)
    BG   — bronze+gold, gravity conduits
    GS   — gold+silver, electromagnetic carriers
    BS   — bronze+silver, strong-force carriers
    B    — bronze only, dark energy scaffold
    G    — gold only, photon-like
    S    — silver only, dark matter conduit

Each pair of vertex types has a stiffness derived from the golden ratio φ:
    BGS↔BGS = 1.0          (strongest — matter attracts matter)
    BGS↔BS  = R_C = 0.854  (strong force confinement)
    BGS↔GS  = LEAK = 1/φ⁴  (electromagnetic coupling)
    B↔B     = LEAK³         (very weak — dark energy expands)
    G↔S     = 0.0           (no direct coupling — orthogonal)

These stiffnesses ARE the force hierarchy. No gravity, no EM, no strong
force is coded separately — they all emerge from the same spring network
with different coupling constants, all derived from φ² = φ + 1.

KEY MECHANISMS:
    1. Asymmetric strain: extension penalized more than compression
       for matter bonds → net infall → galaxy formation
    2. Well-fill: bonds that reach equilibrium stop applying force
       (gravity well is "full") → prevents collapse to a point
    3. Three-gate model: matter bonds (gate=1.0) feel full force,
       filament bonds (gate=R_C) are partially gated, vacuum bonds
       (gate=0) expand freely → dark energy
    4. Vortex torque: golden angle (137.508°) rotation per bracket
       step, depth-dependent → differential rotation → spiral arms
    5. Two-potential flow: photon (outward, from tension) and sound
       (inward, from compression) create radial structure
    6. Orbital mode: tangential velocity preserved (only gate drag),
       radial velocity damped → sustained rotation

T52 RECIPE:
    - Heavy damping (0.9997) — slow, controlled structure formation
    - photon_rate = φ = 1.618 — golden ratio outflow
    - sound_rate = 1.0 — unit inflow
    - vortex = 0.002 — gentle rotation
    - orbital_mode = True — preserve angular momentum
    - well_fill = True — bonds settle to equilibrium
    - 25,000 steps total, checkpoints every 5,000

STARTING STATE:
    Galaxy cluster g1733 — 6682 vertices extracted from a cosmic web
    simulation via Friends-of-Friends clustering. The cosmic web itself
    was evolved from a quasicrystal tiling based on the AAH Hamiltonian
    at the critical point V = 2J with α = 1/φ.

    Type distribution:
        BGS: 1021  (15.3%) — matter cores
        BG:  2207  (33.0%) — gravity filaments
        GS:   810  (12.1%) — EM carriers
        BS:   490  ( 7.3%) — strong force
        G:    898  (13.4%) — photon-like
        B:    964  (14.4%) — dark energy
        S:    292  ( 4.4%) — dark matter conduits

CONSTANTS (all derived from φ² = φ + 1):
    φ  = 1.6180339887...        golden ratio
    W  = 0.4671338922...        universal gap fraction
    LEAK = 1/φ⁴ = 0.1459...    leakage rate (entanglement tax)
    R_C  = 1 - 1/φ⁴ = 0.8541   crossover parameter
    SILVER_TAX = LEAK/δ_S       entanglement cost per transaction
    δ_S = 1 + √2 = 2.4142      silver metallic mean

REQUIREMENTS:
    pip install numpy jax jax-metal matplotlib scipy

USAGE:
    PYTHONUNBUFFERED=1 caffeinate -i python3 simulation/t52_standalone.py

    Optional arguments:
        --steps N       Total evolution steps (default: 25000)
        --save-every N  Checkpoint interval (default: 5000)
        --outdir PATH   Output directory (default: results/t52_standalone)
        --no-render     Skip image rendering
        --input PATH    Path to initial positions JSON or NPZ file

OUTPUT:
    results/t52_standalone/
        T52_step05000.npz   — vertex positions + types at step 5K
        T52_step05000.png   — face-on projection at step 5K
        T52_step10000.npz   — ... and so on every save_every steps
        results.json        — final metrics summary

© 2026 Thomas A. Husmann / iBuilt LTD. Patent App. 19/560,637.
"""

import argparse
import json
import os
import sys
import time

import numpy as np

# ── Path setup ─────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# The evolution engine — 1789 lines of spring physics, all from φ
from jax_evolve import evolve_jax, PHI

# ── Constants ──────────────────────────────────────────────────────
SQRT3 = 1.7320508  # √3 — speed ratio (photon/sound)


# ── Shape analysis (inlined, no database dependency) ───────────────

def classify_shape(eigenvalues):
    """Classify galaxy morphology from PCA eigenvalues [λ1 >= λ2 >= λ3].

    Returns one of: sphere, oblate, disc, prolate, filament, triaxial.
    A disc galaxy has two large eigenvalues (flat plane) and one small
    (thin along polar axis), giving c/a < 0.3.
    """
    e = sorted(eigenvalues, reverse=True)
    r12 = e[1] / (e[0] + 1e-15)
    r13 = e[2] / (e[0] + 1e-15)
    if r13 > 0.7:
        return 'sphere'
    elif r12 > 0.7 and r13 < 0.4:
        return 'oblate' if r13 < 0.3 else 'disc'
    elif r12 < 0.4:
        return 'prolate' if r13 < 0.3 else 'filament'
    return 'triaxial'


def compute_shape(positions, types_list):
    """PCA eigenvalues + shape classification.

    Uses only BGS (matter) vertices for shape determination,
    since those trace the visible galaxy structure.
    """
    bgs_mask = np.array([t == 'BGS' for t in types_list])
    pts = positions[bgs_mask] if np.sum(bgs_mask) > 5 else positions
    centered = pts - pts.mean(axis=0)
    cov = np.cov(centered.T)
    evals = np.sort(np.linalg.eigvalsh(cov))[::-1]
    return evals, classify_shape(evals)


def compute_m2(positions, types_list):
    """m=2 Fourier mode power — measures spiral arm strength.

    Projects BGS vertices onto the disc plane, computes azimuthal
    angles, and measures the cos(2θ) + sin(2θ) power. High m2 (>0.3)
    indicates two-fold symmetry (bar or two-arm spiral).
    """
    bgs_mask = np.array([t == 'BGS' for t in types_list])
    bgs_pos = positions[bgs_mask]
    if len(bgs_pos) < 10:
        return 0.0
    com = np.mean(bgs_pos, axis=0)
    r = bgs_pos - com
    _, _, Vt = np.linalg.svd(r - r.mean(axis=0))
    normal = Vt[2]
    proj = r - np.outer(r @ normal, normal)
    angles = np.arctan2(proj[:, 1], proj[:, 0])
    c2 = np.mean(np.cos(2 * angles))
    s2 = np.mean(np.sin(2 * angles))
    return float(np.sqrt(c2**2 + s2**2))


# ── Data loading ───────────────────────────────────────────────────

def load_initial_state(input_path=None):
    """Load initial vertex positions and types.

    Tries in order:
        1. Explicit input_path (JSON or NPZ)
        2. g1733.json cluster file (original source)
        3. Any existing T52 checkpoint

    Returns (positions, types_list) — both NumPy arrays/lists.
    """
    # Try explicit path
    if input_path and os.path.exists(input_path):
        if input_path.endswith('.npz'):
            data = np.load(input_path, allow_pickle=True)
            print(f"  Loaded from {input_path}")
            return data['positions'], list(data['types'])
        elif input_path.endswith('.json'):
            with open(input_path) as f:
                g = json.load(f)
            print(f"  Loaded from {input_path}")
            return np.array(g['positions']), g['types']

    # Try g1733.json (the original galaxy cluster)
    repo_root = os.path.dirname(SCRIPT_DIR)
    g1733_path = os.path.join(repo_root, 'results/universe/clusters/g1733.json')
    if os.path.exists(g1733_path):
        with open(g1733_path) as f:
            g = json.load(f)
        print(f"  Loaded from {g1733_path}")
        return np.array(g['positions']), g['types']

    # Try existing checkpoints
    for search_dir in [
        os.path.join(repo_root, 'results/candidates/T52_heavy_damp'),
        os.path.join(repo_root, 'results/t52_reproduce'),
    ]:
        for fname in ['T52_step20000.npz', 'T52_step05000.npz']:
            path = os.path.join(search_dir, fname)
            if os.path.exists(path):
                data = np.load(path, allow_pickle=True)
                print(f"  Loaded checkpoint from {path}")
                print(f"  NOTE: This is a pre-evolved state, not the raw cluster")
                return data['positions'], list(data['types'])

    raise FileNotFoundError(
        "No initial state found. Provide --input path to a JSON or NPZ file.\n"
        "Expected: results/universe/clusters/g1733.json"
    )


# ── Rendering ──────────────────────────────────────────────────────

def render(pos, types_list, name, outdir):
    """Render face-on projection of the galaxy.

    Projects onto the two principal axes (largest eigenvalue directions)
    of the BGS vertex distribution. Colors by vertex type using the
    Husmann palette:
        BGS = gold (#FFD700) — matter nodes
        BG  = dark orange     — gravity filaments
        GS  = royal blue      — EM carriers
        BS  = slate blue      — strong force
        G   = orange           — photon
        B   = peru            — dark energy
        S   = dodger blue     — dark matter
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    color_map = {
        'BGS': '#FFD700', 'BG': '#FF8C00', 'GS': '#4169E1',
        'BS': '#6A5ACD', 'G': '#FFA500', 'B': '#CD853F', 'S': '#1E90FF',
    }
    type_sizes = {
        'BGS': 8, 'BG': 2, 'GS': 4, 'BS': 3, 'G': 1.5, 'B': 1, 'S': 6,
    }
    colors = [color_map.get(t, '#FFFFFF') for t in types_list]
    sizes = [type_sizes.get(t, 2) for t in types_list]

    # PCA for face-on view
    centered = pos - pos.mean(axis=0)
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    axes = eigvecs[:, order].T

    com = pos.mean(axis=0)
    rel = pos - com
    x = rel @ axes[0]
    y = rel @ axes[1]
    lim = np.percentile(np.abs(np.concatenate([x, y])), 95) * 1.3

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(x, y, c=colors, s=sizes, alpha=0.6)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_title(name, fontsize=12, color='white')
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.tick_params(colors='gray')
    path = os.path.join(outdir, f"{name}.png")
    fig.savefig(path, dpi=150, facecolor='black', bbox_inches='tight')
    plt.close(fig)

    return path


# ── JSON encoder for NumPy types ──────────────────────────────────

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        return super().default(obj)


# ── Main ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='T52 Galaxy Evolution — Standalone Reproduction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Full T52 reproduction from raw cluster
    python3 simulation/t52_standalone.py

    # Quick test run (5K steps)
    python3 simulation/t52_standalone.py --steps 5000

    # Resume from a checkpoint
    python3 simulation/t52_standalone.py --input results/t52_standalone/T52_step10000.npz --steps 15000
        """)
    parser.add_argument('--steps', type=int, default=25000,
                        help='Total evolution steps (default: 25000)')
    parser.add_argument('--save-every', type=int, default=5000,
                        help='Save checkpoint every N steps (default: 5000)')
    parser.add_argument('--outdir', type=str, default='results/t52_standalone',
                        help='Output directory')
    parser.add_argument('--input', type=str, default=None,
                        help='Path to initial positions (JSON or NPZ)')
    parser.add_argument('--no-render', action='store_true',
                        help='Skip image rendering')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # ── Load initial state ─────────────────────────────────────────
    print("Loading initial state...")
    positions, types_list = load_initial_state(args.input)
    n_vtx = len(positions)
    from collections import Counter
    type_counts = Counter(types_list)
    print(f"  {n_vtx} vertices")
    for t in ['BGS', 'BG', 'GS', 'BS', 'G', 'B', 'S']:
        c = type_counts.get(t, 0)
        print(f"    {t:>3}: {c:>5} ({100*c/n_vtx:5.1f}%)")

    # ── Render initial state ───────────────────────────────────────
    if not args.no_render:
        render(positions, types_list, "T52_initial", args.outdir)
        print(f"  Initial state rendered to {args.outdir}/T52_initial.png")

    evals0, shape0 = compute_shape(positions, types_list)
    es0 = sorted(evals0, reverse=True)
    ca0 = es0[2] / (es0[0] + 1e-15)
    m2_0 = compute_m2(positions, types_list)
    print(f"  Initial: c/a={ca0:.3f} m2={m2_0:.3f} {shape0}")

    # ── T52 evolution ──────────────────────────────────────────────
    # These are the T52 parameters — the "recipe" that produces
    # concentric ring structure from the raw cluster.
    print(f"\n{'='*60}")
    print(f"  T52 RECIPE")
    print(f"  Steps:         {args.steps}")
    print(f"  Damping:       0.9997  (heavy — slow structure formation)")
    print(f"  Photon rate:   φ = 1.618  (golden ratio outflow)")
    print(f"  Sound rate:    1.0  (unit inflow)")
    print(f"  Vortex:        0.002  (gentle rotation)")
    print(f"  Orbital mode:  True  (preserve angular momentum)")
    print(f"  Well fill:     True  (bonds settle to equilibrium)")
    print(f"  Gate drag:     1.0  (full entanglement tax)")
    print(f"  Perturbation:  0.001  (tiny symmetry breaking)")
    print(f"  Parker spiral: False  (radial sound)")
    print(f"  Speed ratio:   √3 = {SQRT3}  (photon/sound)")
    print(f"  Save every:    {args.save_every} steps")
    print(f"{'='*60}")

    t0 = time.time()
    result = evolve_jax(
        positions.copy(),
        np.array(types_list),
        n_steps=args.steps,
        vortex_strength=0.002,      # Gentle rotation
        well_fill=True,             # Bonds settle to equilibrium
        damping=0.9997,             # HEAVY DAMPING — the T52 signature
        perturbation=0.001,         # Tiny symmetry breaking
        resume=True,                # Skip thermal phase (data already evolved)
        save_every=args.save_every, # Internal frame saves
        gate_drag=1.0,              # Full entanglement tax gradient
        orbital_mode=True,          # Preserve tangential velocity
        photon_rate=1.618,          # φ — golden ratio outflow
        sound_rate=1.0,             # Unit inflow
        speed_ratio=SQRT3,          # Photon travels √3× faster than sound
        parker_spiral=False,        # Radial sound (not spiral)
    )
    elapsed = time.time() - t0

    n_frames = len(result['frames'])
    print(f"\n  Evolution complete: {elapsed:.0f}s ({n_frames} frames)")

    # ── Save checkpoints and render ────────────────────────────────
    all_metrics = []

    for i, frame in enumerate(result['frames']):
        step = (i + 1) * args.save_every
        name = f"T52_step{step:05d}"

        # Save positions + types
        npz_path = os.path.join(args.outdir, f"{name}.npz")
        np.savez(npz_path, positions=frame, types=types_list, step=step)

        # Render
        if not args.no_render:
            render(frame, types_list, name, args.outdir)

        # Metrics
        evals, shape = compute_shape(frame, types_list)
        es = sorted(evals, reverse=True)
        ca = es[2] / (es[0] + 1e-15)
        m2 = compute_m2(frame, types_list)

        metrics = {
            'step': step,
            'ca': float(ca),
            'm2': float(m2),
            'shape': shape,
        }
        all_metrics.append(metrics)
        print(f"  [{step:>6}] c/a={ca:.3f}  m2={m2:.3f}  {shape}")

    # ── Summary ────────────────────────────────────────────────────
    final = result['frames'][-1]
    evals_f, shape_f = compute_shape(final, types_list)
    es_f = sorted(evals_f, reverse=True)
    ca_f = es_f[2] / (es_f[0] + 1e-15)
    m2_f = compute_m2(final, types_list)

    summary = {
        'recipe': 'T52',
        'n_vertices': n_vtx,
        'n_steps': args.steps,
        'elapsed_seconds': round(elapsed, 1),
        'initial': {
            'ca': float(ca0), 'm2': float(m2_0), 'shape': shape0,
        },
        'final': {
            'ca': float(ca_f), 'm2': float(m2_f), 'shape': shape_f,
        },
        'parameters': {
            'damping': 0.9997,
            'photon_rate': 1.618,
            'sound_rate': 1.0,
            'vortex_strength': 0.002,
            'orbital_mode': True,
            'well_fill': True,
            'gate_drag': 1.0,
            'perturbation': 0.001,
            'parker_spiral': False,
            'speed_ratio': SQRT3,
        },
        'constants': {
            'phi': float(PHI),
            'W': 0.4671338922,
            'LEAK': float(1.0 / PHI**4),
            'R_C': float(1.0 - 1.0 / PHI**4),
        },
        'frames': all_metrics,
    }

    results_path = os.path.join(args.outdir, 'results.json')
    with open(results_path, 'w') as f:
        json.dump(summary, f, indent=2, cls=NpEncoder)

    print(f"\n{'='*60}")
    print(f"  T52 RESULTS")
    print(f"{'='*60}")
    print(f"  Initial:  c/a={ca0:.3f}  m2={m2_0:.3f}  {shape0}")
    print(f"  Final:    c/a={ca_f:.3f}  m2={m2_f:.3f}  {shape_f}")
    print(f"  Time:     {elapsed:.0f}s")
    print(f"{'='*60}")
    print(f"  Checkpoints: {args.outdir}/T52_step*.npz")
    if not args.no_render:
        print(f"  Images:      {args.outdir}/T52_step*.png")
    print(f"  Summary:     {results_path}")
    print(f"\n  KEY METRICS:")
    print(f"    c/a  — axis ratio (low = flat disc, target < 0.3)")
    print(f"    m2   — spiral arm power (high = two-arm structure)")
    print(f"    shape — morphological classification")


if __name__ == '__main__':
    main()
