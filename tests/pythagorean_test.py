import numpy as np
from scipy.sparse import kron, eye, diags, lil_matrix
from scipy.sparse.linalg import eigsh
import math, time

PHI = (1 + math.sqrt(5)) / 2
A_S = 1.0 / (1 + math.sqrt(2))
A_G = 1.0 / PHI
A_B = 1.0 / ((3 + math.sqrt(13)) / 2)

def aah_pbc(N, a):
    H = lil_matrix((N, N))
    for n in range(N):
        H[n, n] = 2 * np.cos(2 * np.pi * a * n)
        H[n, (n+1) % N] += 1.0
        H[n, (n-1) % N] += 1.0
    return H.tocsr()

N = 34
I = eye(N)

print("=" * 60)
print("  PYTHAGOREAN TEST: H² = H_silver² + H_gold² vs H_bronze")
print(f"  N = {N}, PBC")
print("=" * 60)

# Build 1D Hamiltonians
Hs = aah_pbc(N, A_S)
Hg = aah_pbc(N, A_G)
Hb = aah_pbc(N, A_B)

# ================================================================
# TEST 1: 1D spectra — does Δ relationship hold in eigenvalues?
# ================================================================
print(f"\n  TEST 1: 1D EIGENVALUE COMPARISON")
print(f"  {'-' * 50}")

es = np.sort(np.linalg.eigvalsh(Hs.toarray()))
eg = np.sort(np.linalg.eigvalsh(Hg.toarray()))
eb = np.sort(np.linalg.eigvalsh(Hb.toarray()))

# The discriminants
D_s, D_g, D_b = 8, 5, 13

print(f"  Silver Δ={D_s}: E range [{es[0]:.4f}, {es[-1]:.4f}], width {es[-1]-es[0]:.4f}")
print(f"  Gold   Δ={D_g}: E range [{eg[0]:.4f}, {eg[-1]:.4f}], width {eg[-1]-eg[0]:.4f}")
print(f"  Bronze Δ={D_b}: E range [{eb[0]:.4f}, {eb[-1]:.4f}], width {eb[-1]-eb[0]:.4f}")

# Compare squared bandwidths
bw_s = (es[-1] - es[0])**2
bw_g = (eg[-1] - eg[0])**2
bw_b = (eb[-1] - eb[0])**2

print(f"\n  Bandwidth²: silver={bw_s:.4f}, gold={bw_g:.4f}, bronze={bw_b:.4f}")
print(f"  Silver² + Gold² = {bw_s + bw_g:.4f}")
print(f"  Bronze² = {bw_b:.4f}")
print(f"  Match: {abs(bw_s + bw_g - bw_b)/bw_b*100:.1f}%")

# Compare E² spectra
es2 = np.sort(es**2)
eg2 = np.sort(eg**2)
eb2 = np.sort(eb**2)

print(f"\n  E² spectra (first 5):")
print(f"  Silver²: {es2[:5].round(4)}")
print(f"  Gold²:   {eg2[:5].round(4)}")
print(f"  Bronze²: {eb2[:5].round(4)}")

# ================================================================
# TEST 2: 3D Pythagorean Hamiltonian
# ================================================================
print(f"\n\n  TEST 2: 3D PYTHAGOREAN HAMILTONIAN")
print(f"  {'-' * 50}")
print(f"  Building H_pythag² = (H_silver⊗I⊗I)² + (I⊗H_gold⊗I)²")
print(f"  vs H_bronze_3D = H_bronze⊗I⊗I + I⊗H_bronze⊗I + I⊗I⊗H_bronze")

t0 = time.time()

# Method: H_pythag = sqrt(H_s² + H_g²) in the tensor product space
# But we can't take sqrt of an operator easily.
# Instead compare eigenvalues:
# 
# If H = H_s⊗I + I⊗H_g (2D, silver x gold), eigenvalues are e_s(i) + e_g(j)
# If H² = H_s²⊗I + I⊗H_g², eigenvalues are e_s(i)² + e_g(j)²
#
# The Pythagorean claim: the SQUARED eigenvalues of the silver-gold
# system should match the eigenvalues of bronze.

# 2D silver x gold eigenvalues (additive)
sg_evals = np.sort(np.array([es[i] + eg[j] for i in range(N) for j in range(N)]))

# 2D silver x gold SQUARED eigenvalues  
sg2_evals = np.sort(np.array([es[i]**2 + eg[j]**2 for i in range(N) for j in range(N)]))

# 1D bronze eigenvalues
# And bronze SQUARED
eb_sorted = np.sort(eb)
eb2_sorted = np.sort(eb**2)

print(f"\n  Silver⊗Gold additive eigenvalues (first 5): {sg_evals[:5].round(4)}")
print(f"  Bronze eigenvalues (first 5): {eb_sorted[:5].round(4)}")

# Scale: silver+gold has N² eigenvalues, bronze has N
# Can't compare directly. But can compare DENSITY OF STATES.

# Histogram comparison
n_bins = 100

# Silver+Gold additive: range and histogram
sg_range = (sg_evals[0], sg_evals[-1])
sg_hist, sg_edges = np.histogram(sg_evals, bins=n_bins, range=(-6, 6))

# Silver²+Gold² (Pythagorean): range and histogram  
sg2_range = (sg2_evals[0], sg2_evals[-1])
sg2_hist, sg2_edges = np.histogram(sg2_evals, bins=n_bins)

# Bronze: histogram (need to match range)
eb_hist, eb_edges = np.histogram(eb_sorted, bins=n_bins, range=(-6, 6))
eb2_hist, eb2_edges = np.histogram(eb2_sorted, bins=n_bins, range=(0, sg2_evals[-1]))

# Normalize
sg_dos = sg_hist / max(sg_hist.max(), 1)
eb_dos = eb_hist / max(eb_hist.max(), 1)
sg2_dos = sg2_hist / max(sg2_hist.max(), 1)
eb2_dos = eb2_hist / max(eb2_hist.max(), 1)

# Correlation between DOS shapes
corr_additive = np.corrcoef(sg_dos, eb_dos)[0, 1]
corr_pythag = np.corrcoef(sg2_dos, eb2_dos)[0, 1]

print(f"\n  DENSITY OF STATES COMPARISON:")
print(f"  Correlation(Silver+Gold DOS, Bronze DOS):       {corr_additive:.4f}")
print(f"  Correlation(Silver²+Gold² DOS, Bronze² DOS):    {corr_pythag:.4f}")

print(f"\n  Time: {time.time()-t0:.1f}s")

# ================================================================
# TEST 3: Gap structure comparison
# ================================================================
print(f"\n\n  TEST 3: GAP STRUCTURE")
print(f"  {'-' * 50}")

def find_gaps(evals, threshold=5):
    d = np.diff(evals)
    m = np.median(d[d > 0])
    return sorted([(i, d[i]) for i in range(len(d)) if d[i] > threshold * m],
                  key=lambda g: g[1], reverse=True)

gaps_s = find_gaps(es)
gaps_g = find_gaps(eg)
gaps_b = find_gaps(eb)

print(f"  Number of major gaps: silver={len(gaps_s)}, gold={len(gaps_g)}, bronze={len(gaps_b)}")

# The key: gap positions in normalized energy
def gap_positions(evals, gaps):
    E_range = evals[-1] - evals[0]
    return [(evals[g[0]] - evals[0]) / E_range for g in gaps[:4]]

gp_s = gap_positions(es, gaps_s)
gp_g = gap_positions(eg, gaps_g)
gp_b = gap_positions(eb, gaps_b)

print(f"  Gap positions (normalized):")
print(f"    Silver: {[f'{x:.3f}' for x in gp_s[:4]]}")
print(f"    Gold:   {[f'{x:.3f}' for x in gp_g[:4]]}")
print(f"    Bronze: {[f'{x:.3f}' for x in gp_b[:4]]}")

# ================================================================
# TEST 4: The direct Dirac test
# ================================================================
print(f"\n\n  TEST 4: DIRECT DIRAC TEST")
print(f"  {'-' * 50}")
print(f"  E² = p²c² + m²c⁴  ↔  13 = 5 + 8")
print(f"  If Dirac holds: E_bronze² ∝ E_silver² + E_gold²")

# For each bronze eigenvalue, find the best match as sqrt(e_s² + e_g²)
matches = 0
total = len(eb)
residuals = []

for e_b in eb:
    # Find the pair (e_s, e_g) minimizing |e_b² - e_s² - e_g²|
    best = float('inf')
    for e_s in es:
        for e_g in eg:
            diff = abs(e_b**2 - e_s**2 - e_g**2)
            if diff < best:
                best = diff
    residuals.append(best)
    if best < 0.1:
        matches += 1

residuals = np.array(residuals)
print(f"\n  For each bronze eigenvalue, find best |E_b² - E_s² - E_g²|:")
print(f"  Matches within 0.1: {matches}/{total}")
print(f"  Mean residual: {residuals.mean():.4f}")
print(f"  Median residual: {np.median(residuals):.4f}")
print(f"  Min residual: {residuals.min():.6f}")
print(f"  Max residual: {residuals.max():.4f}")

# Compare with null: random frequencies
A_rand = 0.7123  # arbitrary irrational
er = np.sort(np.linalg.eigvalsh(aah_pbc(N, A_rand).toarray()))
residuals_null = []
for e_r in er:
    best = float('inf')
    for e_s in es:
        for e_g in eg:
            diff = abs(e_r**2 - e_s**2 - e_g**2)
            if diff < best:
                best = diff
    residuals_null.append(best)
residuals_null = np.array(residuals_null)

print(f"\n  NULL TEST (random α = 0.7123):")
print(f"  Mean residual: {residuals_null.mean():.4f}")
print(f"  Median residual: {np.median(residuals_null):.4f}")
print(f"\n  Bronze residual / Null residual = {residuals.mean()/residuals_null.mean():.3f}")
if residuals.mean() < residuals_null.mean():
    print(f"  → Bronze fits E²=E_s²+E_g² BETTER than random ({residuals.mean()/residuals_null.mean():.1%} of null)")
else:
    print(f"  → Bronze fits NO BETTER than random")

# ================================================================
# VERDICT
# ================================================================
print(f"\n\n{'=' * 60}")
print(f"  VERDICT")
print(f"{'=' * 60}")
print(f"""
  The Pythagorean relation 5+8=13 connects the discriminants.
  The discriminants determine the frequencies.
  
  The test: do bronze eigenvalues satisfy E_b² = E_s² + E_g²?
  
  Bronze residual:  {residuals.mean():.4f} (mean |E_b² - best(E_s²+E_g²)|)
  Random residual:  {residuals_null.mean():.4f}
  Ratio:            {residuals.mean()/residuals_null.mean():.3f}
  
  If ratio << 1: Pythagorean holds in the spectrum. Dirac is real.
  If ratio ≈ 1: Pythagorean is numerical coincidence, not spectral.
""")

