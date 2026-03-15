#!/usr/bin/env python3
"""3D AAH — FULL diagonalization at L=12 (1728 sites, tractable)."""
import numpy as np
from scipy.linalg import eigvalsh
from scipy.sparse import diags, kron, eye
import math, time

PHI = (1 + math.sqrt(5)) / 2

alpha1 = (math.sqrt(5) - 1) / 2
alpha2 = math.sqrt(2) - 1
alpha3 = (math.sqrt(13) - 3) / 2

L = 12
N = L**3
print(f"3D AAH: {L}×{L}×{L} = {N} sites, FULL diagonalization")

t0 = time.time()

def aah_1d(L, alpha, V=2.0):
    diag = V * np.cos(2 * np.pi * alpha * np.arange(L))
    off = np.ones(L - 1)
    return diags([off, diag, off], [-1, 0, 1], shape=(L, L), format='csr')

Hx = aah_1d(L, alpha1)
Hy = aah_1d(L, alpha2)
Hz = aah_1d(L, alpha3)
Ix = eye(L, format='csr')

H3d = kron(kron(Hx, Ix), Ix) + kron(kron(Ix, Hy), Ix) + kron(kron(Ix, Ix), Hz)

# Convert to dense for full diagonalization
print(f"  Building dense matrix...", flush=True)
H_dense = H3d.toarray()
t1 = time.time()
print(f"  Dense matrix: {t1-t0:.1f}s")

print(f"  Diagonalizing...", flush=True)
evals = np.sort(eigvalsh(H_dense))
t2 = time.time()
print(f"  Done: {t2-t1:.1f}s")

print(f"\n  FULL SPECTRUM:")
print(f"    E range: [{evals[0]:.4f}, {evals[-1]:.4f}]")
print(f"    Bandwidth: {evals[-1]-evals[0]:.4f}")

# 1D spectra for comparison
evals_1d_gold = np.sort(eigvalsh(aah_1d(L, alpha1).toarray()))
evals_1d_silver = np.sort(eigvalsh(aah_1d(L, alpha2).toarray()))
evals_1d_bronze = np.sort(eigvalsh(aah_1d(L, alpha3).toarray()))

print(f"\n  1D bandwidths:")
print(f"    Gold:   [{evals_1d_gold[0]:.3f}, {evals_1d_gold[-1]:.3f}]  BW={evals_1d_gold[-1]-evals_1d_gold[0]:.3f}")
print(f"    Silver: [{evals_1d_silver[0]:.3f}, {evals_1d_silver[-1]:.3f}]  BW={evals_1d_silver[-1]-evals_1d_silver[0]:.3f}")
print(f"    Bronze: [{evals_1d_bronze[0]:.3f}, {evals_1d_bronze[-1]:.3f}]  BW={evals_1d_bronze[-1]-evals_1d_bronze[0]:.3f}")

# D_s via box counting on full spectrum
E_min, E_max = evals[0], evals[-1]
E_range = E_max - E_min
ds_data = []
for k in range(4, 13):
    eps = E_range / (2**k)
    boxes = len(set(int((E - E_min) / eps) for E in evals))
    ds_data.append((math.log(1/eps), math.log(boxes)))

xs = np.array([d[0] for d in ds_data])
ys = np.array([d[1] for d in ds_data])
n = len(xs)
D_s_3d = (n*np.sum(xs*ys) - np.sum(xs)*np.sum(ys)) / (n*np.sum(xs**2) - np.sum(xs)**2)
print(f"\n  D_s (3D, box counting) = {D_s_3d:.4f}")
print(f"  Target (3 × 0.5)      = 1.5000")
print(f"  Target (3D Cantor)     = depends on spectral structure")

# Gap analysis — find the MAJOR gaps
spacings = np.diff(evals)
order = np.argsort(spacings)[::-1]
print(f"\n  Top 10 gaps (out of {len(spacings)}):")
for i in range(10):
    idx = order[i]
    ids = (idx + 1) / N
    print(f"    gap {i+1}: width={spacings[idx]:.4f}  IDS={ids:.4f}  E={evals[idx]:.4f}")

# Five-band partition based on the TWO largest gaps
if len(order) >= 2:
    g1_idx = order[0]
    g2_idx = order[1]
    # Sort by position
    gap_positions = sorted([(g1_idx+1)/N, (g2_idx+1)/N])
    ids1, ids2 = gap_positions
    print(f"\n  Major gap IDS positions: {ids1:.4f}, {ids2:.4f}")
    print(f"  Three-band partition: [{ids1:.4f} | {ids2-ids1:.4f} | {1-ids2:.4f}]")
    print(f"  Golden ratio target:  [0.382 | 0.236 | 0.382]")

# Density of states — is it fractal-like?
n_bins = 200
counts, edges = np.histogram(evals, bins=n_bins)
centers = (edges[:-1] + edges[1:]) / 2

# Find regions of zero/very low DOS (gaps in the spectrum)
threshold = max(counts) * 0.05
gap_bins = np.where(counts < threshold)[0]
print(f"\n  DOS gaps (< 5% of max): {len(gap_bins)} bins out of {n_bins}")
print(f"  Fraction gapped: {len(gap_bins)/n_bins:.3f}")

# Matter fraction = filled fraction of spectrum
filled_bins = np.where(counts >= threshold)[0]
filled_range = sum(edges[i+1] - edges[i] for i in filled_bins)
total_range = edges[-1] - edges[0]
matter_frac = filled_range / total_range
print(f"  Filled fraction of spectrum: {matter_frac:.4f}")
print(f"  e⁻³ target: {math.exp(-3):.4f}")

# Comparison: all-gold 3D (same frequency on all axes)
print(f"\n  COMPARISON: all-gold 3D (α₁ on all axes):")
Hx_g = aah_1d(L, alpha1)
H3d_gold = kron(kron(Hx_g, Ix), Ix) + kron(kron(Ix, Hx_g), Ix) + kron(kron(Ix, Ix), Hx_g)
evals_gold3d = np.sort(eigvalsh(H3d_gold.toarray()))
counts_g, edges_g = np.histogram(evals_gold3d, bins=n_bins)
gap_bins_g = np.where(counts_g < max(counts_g)*0.05)[0]
filled_g = sum(edges_g[i+1]-edges_g[i] for i in np.where(counts_g >= max(counts_g)*0.05)[0])
print(f"  All-gold gapped fraction: {len(gap_bins_g)/n_bins:.3f}")
print(f"  All-gold filled fraction: {filled_g/(edges_g[-1]-edges_g[0]):.4f}")

# θ measurement: what fraction of states lie in the central 1/φ of the spectrum?
E_center = (E_max + E_min) / 2
E_half_width = E_range / (2 * PHI)  # central 1/φ fraction
sigma3_mask = (evals > E_center - E_half_width) & (evals < E_center + E_half_width)
theta = np.sum(sigma3_mask) / N
print(f"\n  θ MEASUREMENT (central 1/φ of spectrum):")
print(f"    States in central 1/φ: {np.sum(sigma3_mask)} / {N} = {theta:.4f}")
print(f"    1/φ target: {1/PHI:.4f}")

# Alternative: use the 1D Cantor structure to define bands
# The 3D spectrum is sum of three 1D spectra, so the band structure
# is the Minkowski sum of three Cantor sets
print(f"\n  CONVOLUTION ANALYSIS:")
print(f"    1D gold gaps: {sum(1 for s in np.diff(evals_1d_gold) if s > 0.1)} major")
print(f"    1D silver gaps: {sum(1 for s in np.diff(evals_1d_silver) if s > 0.1)} major")
print(f"    1D bronze gaps: {sum(1 for s in np.diff(evals_1d_bronze) if s > 0.1)} major")

# Key number: what fraction of 3D states are in the PRODUCT of the 
# three 1D observer bands?
# For each axis, the observer band is the central 1/φ fraction of states
n1d = len(evals_1d_gold)
obs_gold = set(range(int(n1d*(1-1/PHI)/2), int(n1d*(1+1/PHI)/2)))
obs_silver = set(range(int(n1d*(1-1/PHI)/2), int(n1d*(1+1/PHI)/2)))
obs_bronze = set(range(int(n1d*(1-1/PHI)/2), int(n1d*(1+1/PHI)/2)))

# Fraction of 3D states that would be in σ₃ × σ₃ × σ₃
triple_obs_frac = (len(obs_gold)/n1d) * (len(obs_silver)/n1d) * (len(obs_bronze)/n1d)
print(f"    Triple observer fraction: (1/φ)³ = {triple_obs_frac:.4f}")
print(f"    = {1/PHI**3:.4f} (analytic)")
print(f"    This IS the matter fraction if σ₃×σ₃×σ₃ = baryonic matter")

# The KEY result
omega_b_pred = 1/PHI**3
print(f"\n  ═══════════════════════════════════════")
print(f"  KEY RESULT: Ω_b = (1/φ)³ = {omega_b_pred:.4f}")
print(f"  Observed:   Ω_b = 0.0493")
print(f"  Match: {abs(omega_b_pred - 0.0493)/0.0493*100:.1f}% off")
print(f"  ═══════════════════════════════════════")
print(f"  NOTE: (1/φ)³ = 0.236, not 0.050.")
print(f"  The Cantor MEASURE (not band fraction) matters.")
print(f"  At V=2J, Lebesgue measure = 0 (Ten Martini).")
print(f"  The filled fraction from histogram: {matter_frac:.4f}")
print(f"  More refined analysis needed at larger L.")

t_final = time.time()
print(f"\n  Total time: {t_final - t0:.1f}s")
