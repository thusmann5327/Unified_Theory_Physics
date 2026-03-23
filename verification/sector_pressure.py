#!/usr/bin/env python3
"""
sector_pressure.py — Trace Map Pressure & Five-Sector Weighting
================================================================
Thomas A. Husmann / iBuilt LTD / March 22, 2026

Computes the topological pressure P(t) and the five-sector weighted
pressure P_W(t) using the KKT trace map dynamics.

THE KEY DISTINCTION (discovered during computation):
  - Band-width Moran equation gives D_s = 1/2 (spectral MEASURE dimension, Sütő 1989)
  - Trace-map pressure gives d_H ≈ 0.3725 (spectral SET dimension, DGY 2016)
  - The mean-field relation W ≈ 2d_H(1-d_H) uses d_H, not D_s

Method:
  For each energy E in the spectrum (233 eigenvalues of the finite chain),
  iterate the KKT trace map 13 times (F(13) = 233). At each step, record
  the Jacobian factor |2x_{k-1}| (derivative of x_{k+1} w.r.t. x_k).
  The product Π|2x_j| gives the transfer-matrix growth at energy E.

  Partition function: Z(t) = Σ_k (Π_j |2x_j(E_k)|)^t
  Pressure: P(t) = (1/n) log(Z(t)/D) where n = 13 Fibonacci levels
  Bowen root: P(d_H) = 0, i.e., Z(d_H) = D

  Weighted version: Z_W(t) = Σ_i σ_i × Σ_{k in sector i} growth_k^t
  Root: P_W(W) = 0

© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.
"""

import numpy as np
import math

PHI = (1 + 5**0.5) / 2
H_HINGE = PHI**(-1/PHI)
W_EXACT = 2/PHI**4 + H_HINGE/PHI**3
ALPHA_AAH = 1.0 / PHI

# Boundary-law sector weights
SIGMA_END = 1/PHI**4     # endpoints
SIGMA_COND = 1/PHI**3    # conduits

# IDS positions of the four principal gaps
IDS_GAPS = [1/PHI**3, 1/PHI**2, 1/PHI, 2/PHI**2]

# Fibonacci numbers
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def trace_map_growth(E, n_levels=13, V=2.0):
    """
    Compute the trace-map growth factor at energy E.

    Uses the KKT trace map: x_{k+1} = 2 x_k x_{k-1} - x_{k-2}
    Initial conditions (two-letter Fibonacci model, V_a = V, V_b = 0):
      x_{-1} = 1 (identity matrix)
      x_0 = E/2 (letter b)
      x_1 = (E - V)/2 (letter a)

    The Jacobian factor at step k is |2x_{k-1}|.
    The growth is the product of all Jacobian factors.

    Returns: log of the growth factor (sum of log|2x_j|)
    """
    # Initial traces
    xm1 = 1.0          # x_{-1}
    x0 = E / 2.0       # x_0
    x1 = (E - V) / 2.0 # x_1

    # The traces at level -1, 0, 1 give us the invariant
    # I = xm1^2 + x0^2 + x1^2 - 2*xm1*x0*x1 - 1
    # At V=2: I = (V/2)^2 = 1 for all E

    # Iterate and accumulate log-growth
    log_growth = 0.0
    traces = [xm1, x0, x1]

    # The Jacobian factor at the k-th step of the trace map is
    # related to the derivative: dx_{k+1}/dx_k = 2x_{k-1}
    # We accumulate log|2x_{k-1}| at each step

    for k in range(2, n_levels + 1):
        # At step k: x_{k} = 2 x_{k-1} x_{k-2} - x_{k-3}
        x_new = 2 * traces[-1] * traces[-2] - traces[-3]
        # Jacobian factor: |2x_{k-2}| (the "middle" trace at this step)
        jac = abs(2 * traces[-2])
        if jac > 0:
            log_growth += math.log(jac)
        traces.append(x_new)

    return log_growth, traces


def assign_sector(ids_val):
    """Assign to sector 1-5 based on IDS position."""
    if ids_val < IDS_GAPS[0]:
        return 1
    elif ids_val < IDS_GAPS[1]:
        return 2
    elif ids_val < IDS_GAPS[2]:
        return 3
    elif ids_val < IDS_GAPS[3]:
        return 4
    else:
        return 5


def find_root(func, t_lo=0.01, t_hi=3.0, tol=1e-12):
    """Bisection to find root of func(t) = 0."""
    f_lo = func(t_lo)
    f_hi = func(t_hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        t_mid = (t_lo + t_hi) / 2
        f_mid = func(t_mid)
        if abs(f_mid) < tol:
            return t_mid
        if f_lo * f_mid < 0:
            t_hi = t_mid
        else:
            t_lo = t_mid
            f_lo = f_mid
    return (t_lo + t_hi) / 2


def main():
    print("=" * 80)
    print("  TRACE MAP PRESSURE & FIVE-SECTOR WEIGHTING")
    print("  KKT trace map → DGY pressure → Bowen equation")
    print("=" * 80)
    print()

    # ── Build Hamiltonian and get eigenvalues ──
    D = 233
    V = 2.0
    n_levels = 13  # F(13) = 233

    H = np.diag(V * np.cos(2 * np.pi * ALPHA_AAH * np.arange(D)))
    H += np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1)
    eigs = np.sort(np.linalg.eigvalsh(H))

    # ── Identify five sectors by gap structure ──
    diffs = np.diff(eigs)
    med = np.median(diffs)
    gap_list = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
    gap_sorted = sorted(gap_list, key=lambda x: x[1], reverse=True)
    top4 = sorted(gap_sorted[:4], key=lambda x: x[0])

    print(f"  Chain: D = {D} = F({n_levels})")
    print(f"  Spectrum: [{eigs[0]:.4f}, {eigs[-1]:.4f}]")
    print(f"  Four principal gaps at indices: {[g[0] for g in top4]}")
    print(f"  Gap widths: {[f'{g[1]:.4f}' for g in top4]}")
    print()

    # ── Compute trace-map growth for each eigenvalue ──
    # Use the eigenvalues of the COSINE model as energy grid points
    # The trace map uses the TWO-LETTER model (V_a=2, V_b=0)
    # The spectra are related but not identical — use cosine eigs
    # as representative energies spanning the spectrum

    growths = []
    sectors = []

    for k, E in enumerate(eigs):
        lg, traces = trace_map_growth(E, n_levels, V)
        ids = (k + 0.5) / D  # IDS at this eigenvalue
        s = assign_sector(ids)
        growths.append(lg)
        sectors.append(s)

    growths = np.array(growths)
    sectors = np.array(sectors)

    # ── Display growth statistics by sector ──
    print("  TRACE-MAP GROWTH BY SECTOR:")
    print(f"  {'Sector':>8} {'Count':>6} {'Weight':>8} {'⟨log G⟩':>10}"
          f" {'σ(log G)':>10} {'min':>8} {'max':>8}")
    print("  " + "─" * 65)

    sector_names = {1: 'σ₁(C)', 2: 'σ₂(E)', 3: 'σ₃(C)',
                    4: 'σ₄(E)', 5: 'σ₅(C)'}
    sector_weights = {1: SIGMA_COND, 2: SIGMA_END, 3: SIGMA_COND,
                      4: SIGMA_END, 5: SIGMA_COND}

    for s in range(1, 6):
        mask = sectors == s
        g = growths[mask]
        w = sector_weights[s]
        print(f"  {sector_names[s]:>8} {mask.sum():6d} {w:8.4f}"
              f" {g.mean():10.4f} {g.std():10.4f} {g.min():8.3f} {g.max():8.3f}")

    print(f"  {'ALL':>8} {D:6d} {'1.0000':>8}"
          f" {growths.mean():10.4f} {growths.std():10.4f}"
          f" {growths.min():8.3f} {growths.max():8.3f}")
    print()

    # ── Compute pressure P(t) and P_W(t) ──
    # Z(t) = (1/D) Σ_k exp(t × log_growth_k) = (1/D) Σ G_k^t
    # P(t) = (1/n_levels) log Z(t)
    # Bowen root: P(d_H) = 0 ⟺ Z(d_H) = 1

    def Z_unweighted(t):
        """Unweighted partition function."""
        return np.mean(np.exp(t * growths))

    def Z_weighted(t):
        """Five-sector weighted partition function."""
        total = 0.0
        for s in range(1, 6):
            mask = sectors == s
            n_s = mask.sum()
            if n_s > 0:
                sector_Z = np.mean(np.exp(t * growths[mask]))
                total += sector_weights[s] * sector_Z
        return total

    def P_unwt(t):
        z = Z_unweighted(t)
        if z > 0:
            return math.log(z) / n_levels
        return -1e10

    def P_wt(t):
        z = Z_weighted(t)
        if z > 0:
            return math.log(z) / n_levels
        return -1e10

    # ── Scan pressure as function of t ──
    print("  PRESSURE SCAN P(t) and P_W(t):")
    print(f"  {'t':>8} {'P(t)':>12} {'P_W(t)':>12} {'Z(t)':>12} {'Z_W(t)':>12}")
    print("  " + "─" * 55)

    t_values = [0.1, 0.2, 0.3, 0.35, 0.37, 0.3725, 0.38, 0.4,
                0.45, 0.467, W_EXACT, 0.5, 0.6, 0.8, 1.0]

    for t in t_values:
        z = Z_unweighted(t)
        zw = Z_weighted(t)
        p = P_unwt(t)
        pw = P_wt(t)
        marker = ""
        if abs(t - 0.3725) < 0.001:
            marker = " ← d_H"
        elif abs(t - W_EXACT) < 0.001:
            marker = " ← W"
        print(f"  {t:8.4f} {p:12.6f} {pw:12.6f} {z:12.4f} {zw:12.4f}{marker}")

    # ── Find roots ──
    print()
    print("  FINDING ROOTS (P(t) = 0):")

    d_H_root = find_root(P_unwt, 0.01, 2.0)
    W_root = find_root(P_wt, 0.01, 2.0)

    if d_H_root:
        print(f"    Unweighted root:  d_H = {d_H_root:.8f}")
        print(f"      Literature:           ≈ 0.3725")
        print(f"      Error: {abs(d_H_root - 0.3725)/0.3725*100:.2f}%")
    else:
        print("    Unweighted root: NOT FOUND in (0.01, 2.0)")

    print()

    if W_root:
        print(f"    Weighted root:    W_root = {W_root:.8f}")
        print(f"      W theorem:     W      = {W_EXACT:.8f}")
        print(f"      Error: {abs(W_root - W_EXACT)/W_EXACT*100:.4f}%")
    else:
        print("    Weighted root: NOT FOUND in (0.01, 2.0)")

    # ── Mean-field check ──
    print()
    if d_H_root and W_root:
        mf_pred = 2 * d_H_root * (1 - d_H_root)
        print(f"  MEAN-FIELD CHECK:")
        print(f"    W_root = {W_root:.6f}")
        print(f"    2d_H(1-d_H) = {mf_pred:.6f}")
        print(f"    Match: {abs(W_root - mf_pred)/mf_pred*100:.3f}%")

    # ── Convergence study across Fibonacci levels ──
    print()
    print("=" * 80)
    print("  CONVERGENCE STUDY (n = 5..13)")
    print("=" * 80)
    print()
    print(f"  {'n':>3} {'F(n)':>6} {'d_H':>10} {'W_root':>10}"
          f" {'d_H err':>8} {'W err':>8} {'W/d_H':>8} {'2(1-d_H)':>8}")
    print("  " + "─" * 70)

    for n in range(7, 14):
        D_n = fib(n)
        if D_n < 5:
            continue

        # Build Hamiltonian
        H_n = np.diag(V * np.cos(2 * np.pi * ALPHA_AAH * np.arange(D_n)))
        H_n += np.diag(np.ones(D_n - 1), 1) + np.diag(np.ones(D_n - 1), -1)
        eigs_n = np.sort(np.linalg.eigvalsh(H_n))

        # Compute growths
        g_n = []
        s_n = []
        for k, E in enumerate(eigs_n):
            lg, _ = trace_map_growth(E, n, V)
            ids = (k + 0.5) / D_n
            g_n.append(lg)
            s_n.append(assign_sector(ids))
        g_n = np.array(g_n)
        s_n = np.array(s_n)

        # Partition functions
        def Z_u(t):
            return np.mean(np.exp(t * g_n))

        def Z_w(t):
            total = 0.0
            for s in range(1, 6):
                mask = s_n == s
                if mask.sum() > 0:
                    total += sector_weights[s] * np.mean(np.exp(t * g_n[mask]))
            return total

        def P_u(t):
            z = Z_u(t)
            return math.log(z) / n if z > 0 else -1e10

        def P_w(t):
            z = Z_w(t)
            return math.log(z) / n if z > 0 else -1e10

        d_H_n = find_root(P_u, 0.01, 3.0)
        W_n = find_root(P_w, 0.01, 3.0)

        if d_H_n and W_n:
            d_err = abs(d_H_n - 0.3725) / 0.3725 * 100
            w_err = abs(W_n - W_EXACT) / W_EXACT * 100
            ratio = W_n / d_H_n
            mf = 2 * (1 - d_H_n)
            print(f"  {n:3d} {D_n:6d} {d_H_n:10.6f} {W_n:10.6f}"
                  f" {d_err:7.2f}% {w_err:7.2f}% {ratio:8.4f} {mf:8.4f}")
        else:
            print(f"  {n:3d} {D_n:6d}  root not found")

    # ── Summary ──
    print()
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print()
    print(f"  The trace-map pressure uses Π|2x_j| as the transfer-matrix")
    print(f"  growth factor, iterated through n Fibonacci levels.")
    print()
    print(f"  Unweighted Bowen root d_H → should converge to ≈ 0.3725")
    print(f"  Weighted root W_root → should converge to W = {W_EXACT:.6f}")
    print()
    print(f"  Band-width Moran equation gives D_s = 1/2 (spectral MEASURE")
    print(f"  dimension, Sütő 1989) — a DIFFERENT quantity from d_H.")
    print("=" * 80)


if __name__ == "__main__":
    main()
