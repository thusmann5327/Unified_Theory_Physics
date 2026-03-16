import math
import numpy as np

# The peak sites from our computation
# N=13 PBC anisotropic: peak at (6, 2, 3)
# N=34 PBC anisotropic: peak at (5, 2, 8)

# Convert to fractional position along each axis (0 to 1)
# With PBC, position is site/N

cantor = {'core': 0.073, 'inner': 0.235, 'shell': 0.397, 'outer': 0.559}

print("WHERE THE ATOM SITS vs WHERE THE WALLS ARE")
print("=" * 55)

for N, peak in [(13, (6,2,3)), (34, (5,2,8))]:
    print(f"\n  N={N}, peak site: {peak}")
    print(f"  {'Axis':>8s}  {'Site':>5s}  {'Frac':>6s}  {'Nearest wall':>15s}  {'Wall ratio':>10s}  {'Error':>8s}")
    print(f"  {'-' * 55}")
    
    names = ['x(silver)', 'y(gold)', 'z(bronze)']
    for i, name in enumerate(names):
        frac = peak[i] / N
        # Find nearest Cantor ratio
        best_name = ''
        best_err = 999
        for cname, cratio in cantor.items():
            # Also check 1-cratio (other side of symmetric structure)
            for test in [cratio, 1-cratio]:
                err = abs(frac - test)
                if err < best_err:
                    best_err = err
                    best_name = cname
                    best_ratio = test
        
        print(f"  {name:>8s}  {peak[i]:>5d}  {frac:>6.3f}  {best_name:>15s}  {best_ratio:>10.3f}  {best_err:>8.3f}")

# Now check the 1D potential: where are the valleys on each axis?
print(f"\n\nPOTENTIAL VALLEYS ON EACH AXIS")
print("=" * 55)

PHI = (1 + math.sqrt(5)) / 2
alphas = {
    'silver': 1.0 / (1 + math.sqrt(2)),
    'gold': 1.0 / PHI,
    'bronze': 1.0 / ((3 + math.sqrt(13)) / 2),
}

for N in [13, 34]:
    print(f"\n  N = {N}:")
    for name, alpha in alphas.items():
        V = [2 * math.cos(2 * math.pi * alpha * n) for n in range(N)]
        # Find the deepest valleys (most negative V)
        sorted_sites = sorted(range(N), key=lambda n: V[n])
        valleys = sorted_sites[:5]  # 5 deepest
        
        print(f"\n    {name} (α={alpha:.4f}):")
        print(f"    Deepest valleys: ", end="")
        for s in valleys:
            frac = s / N
            # Nearest Cantor ratio
            best = min(cantor.items(), key=lambda c: min(abs(frac-c[1]), abs(frac-(1-c[1]))))
            print(f"site {s} ({frac:.3f}≈{best[0]}), ", end="")
        print()

# The key insight
print(f"\n\n{'=' * 55}")
print(f"  THE QUESTION")
print(f"{'=' * 55}")
print(f"""
  The atom sits where the potential is deepest.
  The potential is V(n) = 2·cos(2πα·n).
  
  The valleys of this cosine are WHERE the comb teeth are.
  The positions of the teeth depend on the frequency α.
  
  Do the teeth of the silver comb land at Cantor node ratios?
  Do the teeth of the gold comb land at different Cantor ratios?
  Does the intersection (both teeth at same spot) give the atom?
  
  Or are the teeth just wherever cos(2πα·n) happens to be
  negative, with no special relationship to 0.073, 0.235, etc?
  
  The Cantor node ratios come from the EIGENVALUES (energy spectrum).
  The atom position comes from the EIGENVECTORS (spatial wavefunctions).
  These are related but not the same thing.
""")

# Direct test: eigenvalue gaps vs eigenstate positions
print(f"\n  DIRECT TEST: 1D silver spectrum gaps vs potential valleys")
print(f"  N=34, α_silver = {alphas['silver']:.4f}")

H_silver = np.diag(2*np.cos(2*np.pi*alphas['silver']*np.arange(34)))
H_silver += np.diag(np.ones(33), 1) + np.diag(np.ones(33), -1)
eigs_s = np.sort(np.linalg.eigvalsh(H_silver))
E_range = eigs_s[-1] - eigs_s[0]

# Find the two biggest gaps (σ₃ boundaries)
diffs = np.diff(eigs_s)
med = np.median(diffs)
gaps = sorted([(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 5*med],
              key=lambda g: g[1], reverse=True)

if len(gaps) >= 2:
    g1, g2 = gaps[0], gaps[1]
    # Gap positions in normalized energy
    gap1_E = (eigs_s[g1[0]] + eigs_s[g1[0]+1]) / 2
    gap2_E = (eigs_s[g2[0]] + eigs_s[g2[0]+1]) / 2
    
    # Normalize to [0,1]
    gap1_norm = (gap1_E - eigs_s[0]) / E_range
    gap2_norm = (gap2_E - eigs_s[0]) / E_range
    
    print(f"  Two largest gaps at normalized energy: {gap1_norm:.3f}, {gap2_norm:.3f}")
    print(f"  Cantor inner wall: 0.235")
    print(f"  Cantor outer wall: 0.559")
    print(f"  (or symmetric: {1-0.235:.3f}, {1-0.559:.3f})")

# Now: which SITES have eigenstates near these gap energies?
# The eigenstates near gap edges are the most localized
print(f"\n  Eigenstates near gap edges (most localized):")
eigvals, eigvecs = np.linalg.eigh(H_silver)

for gi, (gap_idx, gap_width) in enumerate(gaps[:2]):
    # State just below the gap
    state_below = eigvecs[:, gap_idx]
    density_below = state_below**2
    peak_site = np.argmax(density_below)
    
    # State just above the gap
    state_above = eigvecs[:, gap_idx + 1]
    density_above = state_above**2
    peak_site_above = np.argmax(density_above)
    
    print(f"  Gap {gi+1} (width {gap_width:.3f}):")
    print(f"    Below gap: peak at site {peak_site} = {peak_site/34:.3f}")
    print(f"    Above gap: peak at site {peak_site_above} = {peak_site_above/34:.3f}")

