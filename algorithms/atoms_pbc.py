#!/usr/bin/env python3
"""
3D AAH — Periodic vs Open Boundary Conditions
The critical test: does the surface state survive when the lattice edge is removed?
"""
import numpy as np
from scipy.sparse import kron, eye, diags, lil_matrix
from scipy.sparse.linalg import eigsh
import math, time

PHI = (1 + math.sqrt(5)) / 2
A_S = 1.0 / (1 + math.sqrt(2))
A_G = 1.0 / PHI
A_B = 1.0 / ((3 + math.sqrt(13)) / 2)

def aah_open(N, a):
    """Open boundary conditions — sites 0 to N-1, no wrapping"""
    return diags([np.ones(N-1), 2*np.cos(2*np.pi*a*np.arange(N)), np.ones(N-1)],
                 [-1, 0, 1], shape=(N, N))

def aah_periodic(N, a):
    """Periodic boundary conditions — site N-1 connects to site 0"""
    H = lil_matrix((N, N))
    for n in range(N):
        H[n, n] = 2 * np.cos(2 * np.pi * a * n)
        H[n, (n+1) % N] += 1.0
        H[n, (n-1) % N] += 1.0
    return H.tocsr()

def h3d(N, ax, ay, az, periodic=False):
    build = aah_periodic if periodic else aah_open
    I = eye(N)
    return kron(kron(build(N,ax),I),I) + kron(kron(I,build(N,ay)),I) + kron(I,kron(I,build(N,az)))

def rprof(psi, N):
    d = np.abs(psi.reshape(N,N,N))**2
    c = N//2
    nb = max(N//2, 12)
    x,y,z = np.mgrid[0:N,0:N,0:N]
    r = np.sqrt((x-c)**2+(y-c)**2+(z-c)**2)
    bins = np.linspace(0, c, nb+1)
    p = np.zeros(nb); cn = np.zeros(nb)
    for i in range(nb):
        m = (r>=bins[i])&(r<bins[i+1])
        if np.any(m): p[i]=np.sum(d[m]); cn[i]=np.sum(m)
    ct = (bins[:-1]+bins[1:])/2/c
    return ct, np.where(cn>0, p/cn, 0)

def run_test(N, ax, ay, az, periodic, label):
    t0 = time.time()
    H = h3d(N, ax, ay, az, periodic=periodic)
    bc = "PBC" if periodic else "OBC"
    ev, ec = eigsh(H, k=10, sigma=0.0)
    o = np.argsort(np.abs(ev)); ev, ec = ev[o], ec[:, o]
    r, rho = rprof(ec[:, 0], N)
    
    # Find peak
    peak_idx = np.argmax(rho)
    peak_r = r[peak_idx]
    peak_rho = rho[peak_idx]
    
    # Classify: center-localized, surface-localized, or distributed
    inner_mass = np.sum(rho[:len(rho)//3])
    middle_mass = np.sum(rho[len(rho)//3:2*len(rho)//3])
    outer_mass = np.sum(rho[2*len(rho)//3:])
    total = inner_mass + middle_mass + outer_mass
    
    if total > 0:
        in_frac = inner_mass / total
        mid_frac = middle_mass / total
        out_frac = outer_mass / total
    else:
        in_frac = mid_frac = out_frac = 0.33
    
    if in_frac > 0.5:
        state_type = "CENTER"
    elif out_frac > 0.5:
        state_type = "SURFACE"
    else:
        state_type = "DISTRIBUTED"
    
    elapsed = time.time() - t0
    print(f"\n  {label} [{bc}] N={N} ({elapsed:.1f}s)")
    print(f"  E near 0: {ev[:3].round(5)}")
    print(f"  Peak: r/R = {peak_r:.3f} (ρ = {peak_rho:.6f})")
    print(f"  Mass: inner {in_frac:.1%} | middle {mid_frac:.1%} | outer {out_frac:.1%} → {state_type}")
    print(f"  {'r/R':>6s}  {'ρ(r)':>10s}")
    for i in range(len(r)):
        bar = '#' * int(rho[i] / max(max(rho), 1e-10) * 40)
        if rho[i] > 0:
            print(f"  {r[i]:>6.3f}  {rho[i]:>10.6f}  {bar}")
    
    return state_type

print("=" * 65)
print("  PERIODIC vs OPEN BOUNDARY CONDITIONS")
print("  Does the surface state survive without a lattice edge?")
print("=" * 65)

# ================================================================
# N = 13: Both BC, both configs
# ================================================================
print(f"\n{'=' * 65}")
print(f"  N = 13")
print(f"{'=' * 65}")

results = {}
for periodic in [False, True]:
    for label, ax, ay, az in [("Iso bronze", A_B, A_B, A_B),
                               ("Aniso S/G/B", A_S, A_G, A_B)]:
        bc = "PBC" if periodic else "OBC"
        key = f"{label}_{bc}_13"
        results[key] = run_test(13, ax, ay, az, periodic, label)

# ================================================================
# N = 34: Both BC, both configs
# ================================================================
print(f"\n\n{'=' * 65}")
print(f"  N = 34")
print(f"{'=' * 65}")

for periodic in [False, True]:
    for label, ax, ay, az in [("Iso bronze", A_B, A_B, A_B),
                               ("Aniso S/G/B", A_S, A_G, A_B)]:
        bc = "PBC" if periodic else "OBC"
        key = f"{label}_{bc}_34"
        results[key] = run_test(34, ax, ay, az, periodic, label)

# ================================================================
# VERDICT
# ================================================================
print(f"\n\n{'=' * 65}")
print(f"  VERDICT")
print(f"{'=' * 65}")

print(f"\n  {'Config':>20s}  {'N=13 OBC':>10s}  {'N=13 PBC':>10s}  {'N=34 OBC':>10s}  {'N=34 PBC':>10s}")
print(f"  {'-' * 65}")
for label in ["Iso bronze", "Aniso S/G/B"]:
    row = f"  {label:>20s}"
    for N in [13, 34]:
        for bc in ["OBC", "PBC"]:
            key = f"{label}_{bc}_{N}"
            row += f"  {results.get(key, '?'):>10s}"
    print(row)

print(f"""

  IF anisotropic surface state DISAPPEARS with PBC:
    → Finite-size artifact. The lattice edge created a false signal.
    → The real physics is center-localized (atoms are balls).
    
  IF anisotropic surface state PERSISTS with PBC:
    → Real physics. Matter localizes at Cantor boundaries, not centers.
    → Atoms are shells. Paint sprayer model supported.
    → The most important result of the framework.
""")

