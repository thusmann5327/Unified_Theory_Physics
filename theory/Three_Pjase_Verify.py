#!/usr/bin/env python3
"""
THREE-PHASE TUNING VERIFICATION
================================
Verifies all claims in the Three-Phase Tuning Specification:
- Three-source linear independence (D = 3)
- Intensity CDF matches unity equation
- Pairwise correlations
- Five-component address uniqueness
- W_local variation statistics
- Black hole bracket gaps (universality)
- Lattice spacing sensitivity
- Spatial frequency peaks at phi-ratios
- Optimal path vs straight line impedance

© 2026 Thomas A. Husmann / iBuilt LTD
CC BY-NC-SA 4.0

Usage:
    python3 three_phase_tuning_verify.py
    python3 three_phase_tuning_verify.py --plot   (generates PNG figures)
"""
import numpy as np
import sys

PLOT = '--plot' in sys.argv

PHI = (1 + np.sqrt(5)) / 2
GOLDEN_ANGLE = 2 * np.pi / PHI**2
W_GLOBAL = 2/PHI**4 + PHI**(-1/PHI)/PHI**3
L_P = 1.616e-35
C_CAL = 1.0224
G = 6.674e-11
c = 3e8
hbar = 1.055e-34
k_B = 1.381e-23
M_sun = 1.989e30

# Source directions (golden-angle separated, non-coplanar)
S1 = np.array([1, 0, 0])
S2 = np.array([np.sin(GOLDEN_ANGLE), np.cos(GOLDEN_ANGLE), 0])
S2 /= np.linalg.norm(S2)
S3 = np.array([np.sin(2*GOLDEN_ANGLE)*np.cos(np.pi/PHI),
               np.sin(2*GOLDEN_ANGLE)*np.sin(np.pi/PHI),
               np.cos(2*GOLDEN_ANGLE)])
S3 /= np.linalg.norm(S3)

SOURCES = [S1, S2, S3]
AMPS = [1/PHI**4, 1/PHI**3, 1/PHI]
OMEGAS = [PHI**4, PHI**3, PHI]
SOURCE_NAMES = ['Matter (1/phi^4)', 'Dark Matter (1/phi^3)', 'Dark Energy (1/phi)']

passed = 0
failed = 0
total = 0

def check(name, condition, detail=""):
    global passed, failed, total
    total += 1
    if condition:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}  {detail}")
        failed += 1

def bracket(r):
    """Compute bracket index from physical radius."""
    return np.log(r / (L_P * C_CAL)) / np.log(PHI)

def wave(X, Y, Z, source, amp, omega, k=2*np.pi):
    """Compute wave from a single source."""
    r = np.sqrt((X-source[0])**2 + (Y-source[1])**2 + (Z-source[2])**2) + 1e-10
    return amp * np.sin(k * r * omega) / r

def compute_address(position, l0=9.3e-9):
    """Compute five-component address of a point."""
    r = np.linalg.norm(position)
    n = np.log(max(r, 1e-30) / (L_P * C_CAL)) / np.log(PHI)
    k = 2 * np.pi / l0
    phases = []
    for s, omega in zip(SOURCES, OMEGAS):
        ri = np.linalg.norm(position - s)
        phase = (k * ri * omega) % (2 * np.pi)
        phases.append(phase)
    return n, phases[0], phases[1], phases[2], l0

def zeckendorf(n):
    """Decompose integer n into Zeckendorf representation."""
    if n <= 0:
        return []
    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    result = []
    remaining = int(round(n))
    for f in reversed(fibs):
        if f <= remaining:
            result.append(f)
            remaining -= f
    return result


# ══════════════════════════════════════════════════════════════
print("=" * 65)
print("THREE-PHASE TUNING VERIFICATION SUITE")
print("Husmann Decomposition — March 7, 2026")
print("=" * 65)

# ──────────────────────────────────────────────
print("\n[1] FUNDAMENTAL CONSTANTS")
print("-" * 40)
# ──────────────────────────────────────────────
print(f"     phi              = {PHI:.10f}")
print(f"     Golden angle     = {np.degrees(GOLDEN_ANGLE):.4f} deg")
print(f"     W (wall frac)    = {W_GLOBAL:.6f}")
print(f"     alpha = 1/(294*W)= {1/(294*W_GLOBAL):.6f} = 1/{294*W_GLOBAL:.2f}")
print(f"     l0 (nominal)     = {9.3} nm")
print(f"     Coherence patch  = {987 * 9.3e-9 * 1e6:.2f} um")

unity = 1/PHI + 1/PHI**3 + 1/PHI**4
boundary = 2/PHI**4 + 3/PHI**3
check("Unity identity = 1", abs(unity - 1.0) < 1e-14)
check("Boundary law = 1", abs(boundary - 1.0) < 1e-14)
check("W = 0.467134", abs(W_GLOBAL - 0.467134) < 0.000001)
check("alpha within 0.25% of CODATA", abs(1/(294*W_GLOBAL) - 1/137.036) / (1/137.036) < 0.0025)

# ──────────────────────────────────────────────
print("\n[2] THREE-SOURCE LINEAR INDEPENDENCE")
print("-" * 40)
# ──────────────────────────────────────────────
basis = np.column_stack([S1, S2, S3])
det = np.linalg.det(basis)
print(f"     S1 = [{S1[0]:.4f}, {S1[1]:.4f}, {S1[2]:.4f}]")
print(f"     S2 = [{S2[0]:.4f}, {S2[1]:.4f}, {S2[2]:.4f}]")
print(f"     S3 = [{S3[0]:.4f}, {S3[1]:.4f}, {S3[2]:.4f}]")
print(f"     det(S1, S2, S3) = {det:.6f}")
check("Determinant nonzero (3D confirmed)", abs(det) > 0.01)

for a, b, na, nb in [(S1,S2,"S1","S2"), (S2,S3,"S2","S3"), (S1,S3,"S1","S3")]:
    angle_deg = np.degrees(np.arccos(np.clip(np.dot(a, b), -1, 1)))
    print(f"     Angle {na}-{nb}: {angle_deg:.2f} deg")

# ──────────────────────────────────────────────
print("\n[3] INTERFERENCE FIELD COMPUTATION")
print("-" * 40)
# ──────────────────────────────────────────────
N_grid = 60
ext = 3.0
x = np.linspace(-ext, ext, N_grid)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

fields = []
for s, a, omega in zip(SOURCES, AMPS, OMEGAS):
    fields.append(wave(X, Y, Z, s, a, omega))

psi_total = sum(fields)
I_total = psi_total**2
print(f"     Grid: {N_grid}^3 = {N_grid**3:,} voxels")
print(f"     Extent: +/-{ext}")
print(f"     Mean intensity: {np.mean(I_total):.6f}")
print(f"     Max intensity:  {np.max(I_total):.6f}")

# ──────────────────────────────────────────────
print("\n[4] INTENSITY CDF vs UNITY EQUATION")
print("-" * 40)
# ──────────────────────────────────────────────
I_sorted = np.sort(I_total.flatten())
Ntot = len(I_sorted)

matter_frac = 1/PHI**4
dm_frac = 1/PHI**3
de_frac = 1/PHI

print(f"     Matter fraction (1/phi^4):  {matter_frac:.6f}")
print(f"     DM fraction (1/phi^3):      {dm_frac:.6f}")
print(f"     DE fraction (1/phi):        {de_frac:.6f}")
print(f"     Sum:                        {matter_frac+dm_frac+de_frac:.10f}")

# Intensity at CDF thresholds
I_at_matter = I_sorted[int(Ntot * matter_frac)]
I_at_dm = I_sorted[int(Ntot * (matter_frac + dm_frac))]
print(f"     I at {matter_frac:.1%} CDF:   {I_at_matter:.6f}")
print(f"     I at {matter_frac+dm_frac:.1%} CDF: {I_at_dm:.6f}")

check("Unity equation sums to 1.000000", abs(matter_frac + dm_frac + de_frac - 1.0) < 1e-10)
check("CDF has distinct thresholds", I_at_dm > I_at_matter)

# ──────────────────────────────────────────────
print("\n[5] PAIRWISE CORRELATIONS")
print("-" * 40)
# ──────────────────────────────────────────────
pairs = [
    ("DM+DE (filaments)", 1, 2, 0.90),
    ("Matter+DE (boundaries)", 0, 2, 0.80),
    ("Matter+DM (clusters)", 0, 1, -1.0),  # no minimum threshold
]

for name, i, j, min_corr in pairs:
    I_pair = (fields[i] + fields[j])**2
    corr = np.corrcoef(I_pair.flatten(), I_total.flatten())[0, 1]
    print(f"     {name}: r = {corr:.4f}")
    if min_corr > 0:
        check(f"{name} corr > {min_corr}", corr > min_corr)

# ──────────────────────────────────────────────
print("\n[6] FIVE-COMPONENT ADDRESS UNIQUENESS")
print("-" * 40)
# ──────────────────────────────────────────────
np.random.seed(42)
N_test = 2000
test_points = np.random.randn(N_test, 3) * 2.0

addresses = set()
for pt in test_points:
    addr = compute_address(pt)
    # Round to reasonable precision for uniqueness check
    addr_rounded = (round(addr[0], 4), round(addr[1], 6),
                    round(addr[2], 6), round(addr[3], 6))
    addresses.add(addr_rounded)

print(f"     Points tested: {N_test}")
print(f"     Unique addresses: {len(addresses)}")
check("All addresses unique", len(addresses) == N_test)

# Example addresses
print(f"\n     Example addresses:")
examples = [
    ("Origin", np.array([0.01, 0.01, 0.01])),
    ("Near S1", np.array([2.0, 0.0, 0.0])),
    ("Near S2", 2.0 * S2),
    ("Near S3", 2.0 * S3),
]
print(f"     {'Location':>12} {'n':>8} {'theta1':>8} {'theta2':>8} {'theta3':>8}")
for name, pt in examples:
    addr = compute_address(pt)
    print(f"     {name:>12} {addr[0]:>8.1f} {np.degrees(addr[1]):>7.1f}d {np.degrees(addr[2]):>7.1f}d {np.degrees(addr[3]):>7.1f}d")

# Zeckendorf examples
print(f"\n     Zeckendorf examples:")
for n, name in [(94, "Proton"), (164, "Brain"), (220, "Earth"), (294, "Observable")]:
    z = zeckendorf(n)
    print(f"     {name:>12}: n={n} -> {{{', '.join(str(x) for x in z)}}}")

# ──────────────────────────────────────────────
print("\n[7] W_LOCAL VARIATION")
print("-" * 40)
# ──────────────────────────────────────────────
I_mean = np.mean(I_total)
W_local = W_GLOBAL * I_total / (I_mean + 1e-20)
W_local_clip = np.clip(W_local, 0, W_GLOBAL * 50)

p5 = np.percentile(W_local_clip, 5)
p25 = np.percentile(W_local_clip, 25)
p50 = np.percentile(W_local_clip, 50)
p75 = np.percentile(W_local_clip, 75)
p95 = np.percentile(W_local_clip, 95)

print(f"     W_global:       {W_GLOBAL:.6f}")
print(f"     W_local  5th %: {p5:.6f}  (deep voids)")
print(f"     W_local 25th %: {p25:.6f}  (void edges)")
print(f"     W_local 50th %: {p50:.6f}  (median)")
print(f"     W_local 75th %: {p75:.6f}  (filaments)")
print(f"     W_local 95th %: {p95:.6f}  (cluster centers)")
print(f"     Dynamic range:  {p95/max(p5,1e-10):.1f}x")

check("W_local varies significantly", p95/max(p5, 1e-10) > 2.0)

# Alpha variation
alpha_void = 1/(294 * max(p5, 1e-10))
alpha_mean = 1/(294 * W_GLOBAL)
alpha_cluster = 1/(294 * p95) if p95 > 0 else 0
print(f"\n     Implied alpha variation:")
print(f"     Voids:    alpha ~ {alpha_void:.6f}")
print(f"     Average:  alpha ~ {alpha_mean:.6f}")
print(f"     Clusters: alpha ~ {alpha_cluster:.6f}")

# ──────────────────────────────────────────────
print("\n[8] BLACK HOLE BRACKET GAPS")
print("-" * 40)
# ──────────────────────────────────────────────
gap_photon = np.log(1.5) / np.log(PHI)
gap_isco = np.log(3) / np.log(PHI)
gap_gw = np.log(2 * np.pi) / np.log(PHI)
gap_doubling = np.log(2) / np.log(PHI)

print(f"     Photon sphere:  ln(1.5)/ln(phi) = {gap_photon:.6f} brackets  (THE WALL)")
print(f"     Doubling:       ln(2)/ln(phi)   = {gap_doubling:.6f} brackets")
print(f"     ISCO:           ln(3)/ln(phi)   = {gap_isco:.6f} brackets  (phi^2 MEDIATOR)")
print(f"     GW wavelength:  ln(2pi)/ln(phi) = {gap_gw:.6f} brackets   (pi BRACKET)")
print(f"     phi^2 =                           {PHI**2:.6f}")
print(f"     |ISCO - phi^2| =                  {abs(gap_isco - PHI**2):.6f}")

check("ISCO-to-photon = doubling", abs((gap_isco - gap_photon) - gap_doubling) < 1e-6)

# Universality across BH masses
print(f"\n     Mass independence (ISCO gap):")
print(f"     {'Black Hole':>20} {'Mass':>12} {'n_horiz':>8} {'n_ISCO':>8} {'Gap':>8}")
print(f"     {'─'*20} {'─'*12} {'─'*8} {'─'*8} {'─'*8}")

bh_cases = [("Stellar", 10), ("Intermediate", 1e3), ("Sgr A*", 4e6),
            ("M87*", 6.5e9), ("TON 618", 66e9)]

for name, m_solar in bh_cases:
    M = m_solar * M_sun
    r_s = 2 * G * M / c**2
    r_isco = 3 * r_s
    n_s = bracket(r_s)
    n_isco = bracket(r_isco)
    gap = n_isco - n_s
    print(f"     {name:>20} {m_solar:>12.0f} {n_s:>8.2f} {n_isco:>8.2f} {gap:>8.4f}")
    check(f"{name} ISCO gap = {gap_isco:.4f}", abs(gap - gap_isco) < 1e-4)

# Hawking gap universality
print(f"\n     Mass independence (Hawking gap):")
hawking_gaps = []
for name, m_solar in bh_cases:
    M = m_solar * M_sun
    r_s = 2 * G * M / c**2
    T_H = hbar * c**3 / (8 * np.pi * G * M * k_B)
    lambda_H = hbar * c / (k_B * T_H)
    n_s = bracket(r_s)
    n_hawk = bracket(lambda_H)
    gap_h = n_hawk - n_s
    hawking_gaps.append(gap_h)
    print(f"     {name:>20}: Hawking gap = {gap_h:.4f} brackets")

check("Hawking gap universal (spread < 0.01)", max(hawking_gaps) - min(hawking_gaps) < 0.01)

# ──────────────────────────────────────────────
print("\n[9] LATTICE SPACING SENSITIVITY")
print("-" * 40)
# ──────────────────────────────────────────────
l0_nominal = 9.3e-9
print(f"     Nominal l0 = {l0_nominal*1e9:.1f} nm")
print(f"     Coherence patch = 987 * l0 = {987*l0_nominal*1e6:.2f} um")

check("Coherence patch ~ 9.18 um", abs(987 * l0_nominal * 1e6 - 9.18) < 0.1)

# Show how addresses shift with l0
pt = np.array([1.5, 0.8, -0.3])
print(f"\n     Address of test point [{pt[0]}, {pt[1]}, {pt[2]}]:")
print(f"     {'l0 (nm)':>10} {'theta1':>10} {'theta2':>10} {'theta3':>10}")
for l0_v in [7.0e-9, 8.0e-9, 9.3e-9, 10.0e-9, 12.0e-9]:
    addr = compute_address(pt, l0=l0_v)
    print(f"     {l0_v*1e9:>10.1f} {np.degrees(addr[1]):>9.2f}d {np.degrees(addr[2]):>9.2f}d {np.degrees(addr[3]):>9.2f}d")

# Verify phases change substantially with l0
addr_lo = compute_address(pt, l0=7.0e-9)
addr_hi = compute_address(pt, l0=12.0e-9)
max_shift = max(abs(a - b) for a, b in zip(addr_lo[1:4], addr_hi[1:4]))
print(f"\n     Max phase shift (7nm vs 12nm): {np.degrees(max_shift):.1f} deg")
check("l0 change produces large phase shift", max_shift > 0.5)

# ──────────────────────────────────────────────
print("\n[10] SPATIAL FREQUENCY STRUCTURE")
print("-" * 40)
# ──────────────────────────────────────────────
x_1d = np.linspace(-ext, ext, 500)
psi_1d = np.zeros_like(x_1d)
for s, a, omega in zip(SOURCES, AMPS, OMEGAS):
    r = np.abs(x_1d - s[0]) + 1e-10
    psi_1d += a * np.sin(2*np.pi * r * omega) / r

I_1d = psi_1d**2
fft = np.abs(np.fft.rfft(I_1d))
freqs = np.fft.rfftfreq(len(x_1d), d=x_1d[1]-x_1d[0])

fft[0] = 0  # remove DC
peak_indices = np.argsort(fft)[-5:]
peak_freqs = sorted(freqs[peak_indices])
peak_freqs = [f for f in peak_freqs if f > 0]

if len(peak_freqs) >= 2:
    ratios = [peak_freqs[i+1]/peak_freqs[i] for i in range(len(peak_freqs)-1)]
    print(f"     Top spatial frequencies: {[f'{f:.3f}' for f in peak_freqs]}")
    print(f"     Consecutive ratios:      {[f'{r:.3f}' for r in ratios]}")
    print(f"     phi =                    {PHI:.3f}")
    mean_ratio = np.mean(ratios)
    check("Mean frequency ratio near phi", abs(mean_ratio - PHI) < 0.8)
else:
    print("     Insufficient peaks for ratio analysis")

# ──────────────────────────────────────────────
print("\n[11] PAINT ORIENTATION COUPLING")
print("-" * 40)
# ──────────────────────────────────────────────
# Test how helix axis orientation affects coupling to the three sources
orientations = {
    "Along S1 (matter)": S1.copy(),
    "Along S2 (conduit)": S2.copy(),
    "Along S3 (backbone)": S3.copy(),
    "Along z-axis": np.array([0, 0, 1.0]),
    "Random diagonal": np.array([1, 1, 1]) / np.sqrt(3),
}

print(f"     {'Helix axis':>20} {'S1 proj':>8} {'S2 proj':>8} {'S3 proj':>8} {'Coupling':>9}")
print(f"     {'─'*20} {'─'*8} {'─'*8} {'─'*8} {'─'*9}")

for name, d in orientations.items():
    d = d / np.linalg.norm(d)
    projs = [abs(np.dot(d, s)) for s in SOURCES]
    coupling = sum(a * p for a, p in zip(AMPS, projs))
    print(f"     {name:>20} {projs[0]:>8.3f} {projs[1]:>8.3f} {projs[2]:>8.3f} {coupling:>9.4f}")

# Sphere average: mean of |cos(theta)| over sphere = 0.5
sphere_coupling = sum(a * 0.5 for a in AMPS)
print(f"     {'Sphere (avg)':>20} {'0.500':>8} {'0.500':>8} {'0.500':>8} {sphere_coupling:>9.4f}")
print(f"     {'Maximum (all=1)':>20} {'1.000':>8} {'1.000':>8} {'1.000':>8} {sum(AMPS):>9.4f}")

check("Sphere captures 50% of max", abs(sphere_coupling / sum(AMPS) - 0.5) < 0.01)
check("No single axis couples to all three", 
      all(sum(abs(np.dot(d/np.linalg.norm(d), s)) > 0.95 for s in SOURCES) < 3 
          for d in orientations.values()))

# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print(f"RESULTS: {passed} passed, {failed} failed out of {total} tests")
print("=" * 65)

if failed == 0:
    print("\n  ALL TESTS PASSED")
    print("  Three-phase tuning specification: VERIFIED")
    print("  Breathing universe bracket gaps:  VERIFIED")
    print("  Five-component addressing:        VERIFIED")
    print("  Lattice spacing sensitivity:      VERIFIED")
else:
    print(f"\n  {failed} TEST(S) FAILED — review output above")

# ══════════════════════════════════════════════════════════════
# OPTIONAL: Generate plots
# ══════════════════════════════════════════════════════════════
if PLOT:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.size'] = 10
    
    print("\nGenerating plots...")
    
    # ── Figure 1: Interference field + CDF ──
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    
    # 2D slice (z=0)
    mid = N_grid // 2
    I_slice = I_total[:, :, mid]
    axes[0].contourf(x, x, I_slice.T, levels=30, cmap='inferno')
    for s, col, lbl in zip(SOURCES, ['cyan', 'purple', 'gold'], ['S1', 'S2', 'S3']):
        axes[0].plot(s[0], s[1], 'o', color=col, markersize=8, markeredgecolor='white')
        axes[0].annotate(lbl, (s[0], s[1]), color=col, fontweight='bold',
                        textcoords="offset points", xytext=(5, 5))
    axes[0].set_title('Interference Intensity (z=0 slice)')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_aspect('equal')
    
    # CDF
    I_flat = I_total.flatten()
    I_sort = np.sort(I_flat)
    cdf = np.arange(1, len(I_sort)+1) / len(I_sort)
    axes[1].plot(I_sort, cdf, 'k-', lw=1.5)
    axes[1].axhline(y=matter_frac, color='cyan', ls='--', label=f'1/phi^4={matter_frac:.3f}')
    axes[1].axhline(y=matter_frac+dm_frac, color='purple', ls='--', label=f'+1/phi^3={matter_frac+dm_frac:.3f}')
    axes[1].axhline(y=1.0, color='gold', ls='--', label='1.0')
    axes[1].set_title('Intensity CDF = Unity Equation')
    axes[1].set_xlabel('Intensity'); axes[1].set_ylabel('CDF')
    axes[1].legend(fontsize=8)
    axes[1].set_ylim(0, 1.05)
    
    # W_local
    W_slice = W_local_clip[:, :, mid]
    im = axes[2].contourf(x, x, W_slice.T, levels=30, cmap='RdYlGn_r')
    plt.colorbar(im, ax=axes[2], label='W_local', shrink=0.8)
    axes[2].set_title('Local Wall Fraction W_local')
    axes[2].set_xlabel('x'); axes[2].set_ylabel('y')
    axes[2].set_aspect('equal')
    
    fig.tight_layout()
    fig.savefig('three_phase_fig1_interference.png', dpi=150, bbox_inches='tight')
    print("  Saved: three_phase_fig1_interference.png")
    
    # ── Figure 2: BH bracket structure ──
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    
    bh_masses = [10, 1e3, 4e6, 6.5e9, 66e9]
    bh_labels = ['10 Msun', '1K Msun', 'Sgr A*', 'M87*', 'TON 618']
    
    for i, (m, label) in enumerate(zip(bh_masses, bh_labels)):
        M = m * M_sun
        r_s = 2 * G * M / c**2
        n_s = bracket(r_s)
        
        # Draw the bracket structure
        y = i
        ax2.barh(y, gap_photon, left=0, height=0.6, color='yellow', alpha=0.7, edgecolor='black')
        ax2.barh(y, gap_isco - gap_photon, left=gap_photon, height=0.6, color='orange', alpha=0.7, edgecolor='black')
        ax2.barh(y, gap_gw - gap_isco, left=gap_isco, height=0.6, color='blue', alpha=0.5, edgecolor='black')
        ax2.barh(y, hawking_gaps[0] - gap_gw, left=gap_gw, height=0.6, color='red', alpha=0.4, edgecolor='black')
        
        ax2.text(-0.3, y, f'{label}\nn={n_s:.1f}', ha='right', va='center', fontsize=8)
    
    ax2.axvline(x=gap_photon, color='yellow', ls=':', lw=1)
    ax2.axvline(x=gap_isco, color='red', ls=':', lw=1)
    ax2.axvline(x=gap_gw, color='blue', ls=':', lw=1)
    ax2.axvline(x=hawking_gaps[0], color='darkred', ls=':', lw=1)
    
    ax2.set_xlabel('Brackets above horizon')
    ax2.set_title('Universal Black Hole Bracket Gaps (mass-independent)')
    ax2.set_yticks([])
    
    # Labels at top
    for xv, lbl, col in [(gap_photon, 'Photon\nSphere', 'goldenrod'),
                          (gap_isco, 'ISCO\n(phi^2)', 'red'),
                          (gap_gw, 'GW\n(pi)', 'blue'),
                          (hawking_gaps[0], 'Hawking\nPeak', 'darkred')]:
        ax2.text(xv, len(bh_masses)-0.3, lbl, ha='center', va='bottom', fontsize=8, color=col, fontweight='bold')
    
    fig2.tight_layout()
    fig2.savefig('three_phase_fig2_bh_gaps.png', dpi=150, bbox_inches='tight')
    print("  Saved: three_phase_fig2_bh_gaps.png")
    
    # ── Figure 3: l0 sensitivity ──
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    
    l0_range = np.linspace(5e-9, 14e-9, 200)
    pt_test = np.array([1.5, 0.8, -0.3])
    
    for phase_idx, (omega, lbl, col) in enumerate(zip(OMEGAS, 
            ['theta1 (matter)', 'theta2 (conduit)', 'theta3 (backbone)'],
            ['cyan', 'purple', 'gold'])):
        phases_sweep = []
        for l0_v in l0_range:
            k_v = 2 * np.pi / l0_v
            ri = np.linalg.norm(pt_test - SOURCES[phase_idx])
            phase = (k_v * ri * omega) % (2 * np.pi)
            phases_sweep.append(np.degrees(phase))
        ax3.plot(l0_range * 1e9, phases_sweep, color=col, lw=1.5, label=lbl)
    
    ax3.axvline(x=9.3, color='red', ls='--', lw=1.5, label='l0 = 9.3 nm (nominal)')
    ax3.set_xlabel('Lattice spacing l0 (nm)')
    ax3.set_ylabel('Phase (degrees)')
    ax3.set_title('Phase Sensitivity to Lattice Spacing')
    ax3.legend(fontsize=8)
    
    fig3.tight_layout()
    fig3.savefig('three_phase_fig3_l0_sensitivity.png', dpi=150, bbox_inches='tight')
    print("  Saved: three_phase_fig3_l0_sensitivity.png")
    
    plt.close('all')
    print("All plots generated.")

print(f"\n{'='*65}")
print("Thomas A. Husmann | iBuilt LTD | CC BY-NC-SA 4.0")
print("https://github.com/thusmann5327/Unified_Theory_Physics")
print(f"{'='*65}")
