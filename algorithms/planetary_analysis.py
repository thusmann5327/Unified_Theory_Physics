#!/usr/bin/env python3
"""
teegarden_analysis.py — ZeckyBOT Exoplanetary System Analysis
Husmann Decomposition applied to Teegarden's Star

Demonstrates the method for analyzing ANY exoplanetary system:
1. Mass-scaled φ^k ladder
2. Cantor internal stellar architecture
3. Period ratio golden resonance detection
4. Predictions for undiscovered planets
5. Transit accessibility scoring

Thomas A. Husmann / iBuilt LTD — March 11, 2026
"""

import math, numpy as np, os, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

# ═══════════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS (from D=233 lattice, zero external parameters)
# ═══════════════════════════════════════════════════════════════════════

D = 233
PHI = (1 + math.sqrt(5)) / 2
ALPHA_AAH = 1.0 / PHI
L_P = 1.61625e-35; C = 2.99792458e8; HBAR = 1.0545718e-34
AU = 1.496e11; LY = 9.461e15; R_SUN = 6.96e8; M_SUN = 1.989e30

# Spectrum → W, ratios
_eigs = np.sort(np.linalg.eigvalsh(
    np.diag(2*np.cos(2*np.pi*ALPHA_AAH*np.arange(D))) +
    np.diag(np.ones(D-1),1) + np.diag(np.ones(D-1),-1)))
_E_range = float(_eigs[-1] - _eigs[0])
_diffs = np.diff(_eigs); _med = np.median(_diffs)
_gaps = [{'lo':float(_eigs[i]),'hi':float(_eigs[i+1]),'w':float(_diffs[i]),
          'c':float((_eigs[i]+_eigs[i+1])/2)}
         for i in range(len(_diffs)) if _diffs[i] > 8*_med]
_ranked = sorted(_gaps, key=lambda g: g['w'], reverse=True)
_wL = min([g for g in _ranked if g['w']>1], key=lambda g: g['lo']+g['hi'])
_wR = max([g for g in _ranked if g['w']>1], key=lambda g: g['lo']+g['hi'])
_half = _E_range / 2

W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3
COS_ALPHA = math.cos(ALPHA_AAH)
R_MATTER = abs(_wL['hi']) / _half
R_INNER = abs(_wL['c']) / _half - _wL['w'] / (2*_E_range)
R_SHELL = abs(_wL['c']) / _half
R_OUTER = abs(_wL['c']) / _half + _wL['w'] / (2*_E_range)
R_PHOTO = R_INNER + COS_ALPHA * (R_SHELL - R_INNER)
OBLATE = math.sqrt(PHI)
LORENTZ_W = math.sqrt(1 - W**2)
N_BRACKETS = 294

_fibs = [1,1]
while _fibs[-1] < 100000: _fibs.append(_fibs[-1]+_fibs[-2])

def zeckendorf(n):
    n = max(1,int(round(abs(n)))); r,rem = [],n
    for f in reversed(_fibs):
        if f<=rem: r.append(f); rem-=f
        if rem==0: break
    return r or [1]

def zeck_str(n): return '{'+'+'.join(str(x) for x in zeckendorf(n))+'}'

def bracket(r_m):
    if r_m<=0: return 1
    return max(1,min(294,round(math.log(max(r_m,L_P*10)/L_P)/math.log(PHI))))


# ═══════════════════════════════════════════════════════════════════════
# SYSTEM ANALYZER — The general method for any exoplanetary system
# ═══════════════════════════════════════════════════════════════════════

class SystemAnalyzer:
    """
    Analyze any exoplanetary system using the Husmann Decomposition.
    
    Method:
    1. ANCHOR: Compute mass-scaled Mercury-equivalent orbit
       a₀ = 0.387 AU × (M_star/M_sun)^(1/3)
       This is NOT a fit — it's the framework's prediction for
       where the innermost resonant orbit should be.
       
    2. LADDER: Place planets on r(k) = a₀ × φ^k rungs
       Find best-fit integer k for each planet.
       The error tells you how well the system obeys φ-spacing.
       
    3. RESONANCE: Check period ratios against golden expressions
       φ, φ+1/φ, φ², 7/3, 5/3, etc.
       Golden resonance chains indicate Cantor-stabilized orbits.
       
    4. STELLAR STRUCTURE: Apply Cantor node to the star
       If photosphere = cos(α) surface:
       R_total = R_star / R_PHOTO
       Then core, tachocline, Alfvén follow from the five ratios.
       
    5. PREDICT: Identify empty φ^k rungs in the habitable zone
       Each empty rung is a predicted planet location.
       Mystery signals landing on rungs are strong confirmations.
    """
    
    # Solar system anchor (the one empirical constant)
    A0_SUN = 0.387  # AU — Mercury's orbit
    
    # Golden expressions for resonance detection
    GOLDEN_RATIOS = [
        ("φ",       PHI,        1.618),
        ("φ+1/φ",   PHI+1/PHI,  2.236),
        ("φ²",      PHI**2,     2.618),
        ("7/3",     7/3,        2.333),
        ("5/3",     5/3,        1.667),
        ("3/2",     3/2,        1.500),
        ("2",       2,          2.000),
        ("φ³",      PHI**3,     4.236),
        ("5",       5,          5.000),
        ("φ⁴",      PHI**4,     6.854),
    ]
    
    def __init__(self, name, M_star, R_star, L_star, T_eff, distance_ly, planets):
        """
        Parameters:
            name: System name
            M_star: Stellar mass in solar masses
            R_star: Stellar radius in solar radii
            L_star: Stellar luminosity in solar luminosities
            T_eff: Effective temperature in K
            distance_ly: Distance in light-years
            planets: List of dicts with keys:
                name, period_d, a_AU, m_earth (minimum mass)
                Optional: ESI, T_eq, note
        """
        self.name = name
        self.M_star = M_star
        self.R_star = R_star
        self.L_star = L_star
        self.T_eff = T_eff
        self.distance_ly = distance_ly
        self.planets = sorted(planets, key=lambda p: p['a_AU'])
        
        # Derived quantities
        self.R_star_m = R_star * R_SUN
        self.M_star_kg = M_star * M_SUN
        self.distance_m = distance_ly * LY
        self.bz_star = bracket(self.R_star_m)
        self.bz_distance = bracket(self.distance_m)
        
        # Mass-scaled anchor (the framework's prediction, not a fit)
        self.a0 = self.A0_SUN * M_star**(1/3)
        
        # Habitable zone (simple sqrt(L) scaling)
        self.hz_inner = math.sqrt(L_star) * 0.75  # AU, conservative inner
        self.hz_outer = math.sqrt(L_star) * 1.77   # AU, conservative outer
    
    # ── STEP 1: φ^k LADDER ───────────────────────────────────────────
    
    def compute_ladder(self):
        """Map each planet onto its nearest φ^k rung."""
        results = []
        for p in self.planets:
            a = p['a_AU']
            k_exact = math.log(a / self.a0) / math.log(PHI)
            k = round(k_exact)
            pred = self.a0 * PHI**k
            err = abs(pred - a) / a * 100
            results.append({
                **p,
                'k': k,
                'k_exact': round(k_exact, 3),
                'pred_AU': round(pred, 6),
                'error_pct': round(err, 2),
                'bz': bracket(a * AU),
                'zeckendorf': zeck_str(bracket(a * AU)),
                'in_hz': self.hz_inner <= a <= self.hz_outer,
            })
        self.ladder_results = results
        self.ladder_mean_error = np.mean([r['error_pct'] for r in results])
        return results
    
    # ── STEP 2: PERIOD RATIO RESONANCES ──────────────────────────────
    
    def compute_resonances(self):
        """Check period ratios between consecutive planets."""
        results = []
        for i in range(1, len(self.planets)):
            ratio = self.planets[i]['period_d'] / self.planets[i-1]['period_d']
            phi_power = math.log(ratio) / math.log(PHI)
            
            # Find best golden match
            best_match = None
            best_err = 999
            for gname, gval, _ in self.GOLDEN_RATIOS:
                err = abs(gval - ratio) / ratio * 100
                if err < best_err:
                    best_err = err
                    best_match = gname
            
            results.append({
                'pair': f"{self.planets[i]['name']}/{self.planets[i-1]['name']}",
                'ratio': round(ratio, 4),
                'phi_power': round(phi_power, 3),
                'best_golden': best_match,
                'golden_err': round(best_err, 2),
            })
        self.resonance_results = results
        self.resonance_mean_error = np.mean([r['golden_err'] for r in results]) if results else 99
        return results
    
    # ── STEP 3: STELLAR CANTOR STRUCTURE ─────────────────────────────
    
    def compute_stellar_structure(self):
        """Apply Cantor node architecture to the star."""
        # If photosphere = cos(α) layer
        R_total = self.R_star_m / R_PHOTO
        
        self.stellar_layers = {
            'R_total_m': R_total,
            'core_frac': R_MATTER,      # fraction of R_star
            'core_m': R_total * R_MATTER,
            'tachocline_frac': R_INNER / R_PHOTO,
            'tachocline_m': R_total * R_INNER,
            'photosphere_frac': 1.0,     # = R_star by definition
            'photosphere_m': self.R_star_m,
            'alfven_frac': R_OUTER / R_PHOTO,
            'alfven_m': R_total * R_OUTER,
        }
        return self.stellar_layers
    
    # ── STEP 4: PREDICTIONS — Empty rungs ────────────────────────────
    
    def compute_predictions(self, k_range=(-6, 10)):
        """Find empty φ^k rungs and flag habitable zone predictions."""
        self.compute_ladder()  # ensure ladder is computed
        occupied_k = set(r['k'] for r in self.ladder_results)
        
        predictions = []
        for k in range(k_range[0], k_range[1]):
            r_AU = self.a0 * PHI**k
            if r_AU * AU < self.R_star_m * 3:
                continue  # inside star
            if r_AU > 10:
                continue  # beyond reasonable range
            
            in_hz = self.hz_inner <= r_AU <= self.hz_outer
            occupied = k in occupied_k
            planet_name = None
            if occupied:
                for lr in self.ladder_results:
                    if lr['k'] == k:
                        planet_name = lr['name']
                        break
            
            predictions.append({
                'k': k,
                'r_AU': round(r_AU, 6),
                'occupied': occupied,
                'planet': planet_name,
                'in_hz': in_hz,
                'bz': bracket(r_AU * AU),
                'zeckendorf': zeck_str(bracket(r_AU * AU)),
            })
        self.predictions = predictions
        self.empty_hz_rungs = [p for p in predictions if not p['occupied'] and p['in_hz']]
        return predictions
    
    # ── STEP 5: MYSTERY SIGNAL CHECKER ───────────────────────────────
    
    def check_signal(self, period_days):
        """Check if a mystery signal lands on a φ^k rung."""
        G = 6.674e-11
        a_m = (G * self.M_star_kg * (period_days*86400)**2 / (4*math.pi**2))**(1/3)
        a_AU = a_m / AU
        k_exact = math.log(a_AU / self.a0) / math.log(PHI)
        k = round(k_exact)
        pred_AU = self.a0 * PHI**k
        err = abs(pred_AU - a_AU) / a_AU * 100
        
        return {
            'period_d': period_days,
            'a_AU': round(a_AU, 6),
            'k_exact': round(k_exact, 3),
            'k_nearest': k,
            'pred_AU': round(pred_AU, 6),
            'error_pct': round(err, 2),
            'on_rung': err < 5,
            'bz': bracket(a_AU * AU),
        }
    
    # ── STEP 6: TRANSIT CALCULATION ──────────────────────────────────
    
    def compute_transit(self):
        """Estimate transit time through vacuum channel."""
        v_g = 0.4996 * C
        direct_time_s = self.distance_m / v_g
        direct_time_yr = direct_time_s / (3600*24*365.25)
        
        # Vacuum channel compression
        inner_gap = 0.00172; eigenval_dens = 0.26
        grav = math.sqrt(1 - W**2 * 0.28)  # moderate depth for local space
        compressed_m = self.distance_m * inner_gap * eigenval_dens * grav
        compressed_time_s = compressed_m / v_g
        
        self.transit = {
            'distance_ly': self.distance_ly,
            'direct_time_yr': round(direct_time_yr, 1),
            'compressed_m': compressed_m,
            'compressed_ly': round(compressed_m / LY, 4),
            'compressed_time_hr': round(compressed_time_s / 3600, 1),
            'compression_factor': round(self.distance_m / compressed_m, 0),
        }
        return self.transit
    
    # ── COMPOSITE SCORE ──────────────────────────────────────────────
    
    def compute_score(self):
        """Composite exploration score (0-100)."""
        self.compute_ladder()
        self.compute_resonances()
        self.compute_predictions()
        self.compute_transit()
        
        # φ-Ladder compliance (0-30): lower mean error = higher score
        ladder_score = max(0, 30 - self.ladder_mean_error * 2)
        
        # Golden resonance (0-20): lower resonance error = higher score
        resonance_score = max(0, 20 - self.resonance_mean_error * 2)
        
        # Habitable zone (0-20): planets in HZ, bonus for ESI
        hz_planets = sum(1 for r in self.ladder_results if r['in_hz'])
        hz_score = min(20, hz_planets * 8)
        for r in self.ladder_results:
            if r.get('ESI') and r['ESI'] > 0.8: hz_score = min(20, hz_score + 5)
        
        # Transit accessibility (0-20): closer = better
        if self.distance_ly <= 5: transit_score = 20
        elif self.distance_ly <= 15: transit_score = 15
        elif self.distance_ly <= 30: transit_score = 10
        elif self.distance_ly <= 50: transit_score = 5
        else: transit_score = 2
        
        # System completeness (0-10): more planets = more data
        completeness = min(10, len(self.planets) * 2.5)
        
        total = ladder_score + resonance_score + hz_score + transit_score + completeness
        
        self.score = {
            'total': round(total, 1),
            'ladder': round(ladder_score, 1),
            'resonance': round(resonance_score, 1),
            'habitable': round(hz_score, 1),
            'transit': round(transit_score, 1),
            'completeness': round(completeness, 1),
        }
        return self.score
    
    # ── FULL REPORT ──────────────────────────────────────────────────
    
    def full_report(self):
        """Generate complete analysis report."""
        score = self.compute_score()
        stellar = self.compute_stellar_structure()
        
        print(f"\n{'='*70}")
        print(f"ZECKYBOT ANALYSIS: {self.name}")
        print(f"{'='*70}")
        
        print(f"\n  STAR: {self.name}")
        print(f"    Mass: {self.M_star} M☉, Radius: {self.R_star} R☉")
        print(f"    Luminosity: {self.L_star} L☉, T_eff: {self.T_eff} K")
        print(f"    Distance: {self.distance_ly} ly, bz = {self.bz_distance}")
        print(f"    Zeckendorf: {zeck_str(self.bz_distance)}")
        
        print(f"\n  MASS-SCALED ANCHOR:")
        print(f"    a₀ = 0.387 × {self.M_star}^(1/3) = {self.a0:.4f} AU")
        print(f"    Ladder: r(k) = {self.a0:.4f} AU × φ^k")
        
        print(f"\n  φ^k LADDER:")
        print(f"    {'Planet':<18} {'a(AU)':>8} {'k':>4} {'Pred':>8} {'Err':>7} {'HZ':>4} {'Zeck':>18}")
        print(f"    {'-'*70}")
        for r in self.ladder_results:
            hz = '★' if r['in_hz'] else ''
            mk = '✓✓' if r['error_pct']<5 else '✓' if r['error_pct']<15 else '~'
            print(f"    {r['name']:<18} {r['a_AU']:>8.4f} {r['k']:>4} {r['pred_AU']:>8.4f} "
                  f"{r['error_pct']:>6.1f}% {hz:>4} {r['zeckendorf']:>18} {mk}")
        print(f"    Mean error: {self.ladder_mean_error:.1f}%")
        
        if self.resonance_results:
            print(f"\n  GOLDEN RESONANCES:")
            for r in self.resonance_results:
                print(f"    {r['pair']:<25} ratio={r['ratio']:.3f} ≈ {r['best_golden']} "
                      f"(err {r['golden_err']:.1f}%) φ^{r['phi_power']:.2f}")
        
        print(f"\n  STELLAR CANTOR STRUCTURE:")
        print(f"    Core edge:   {stellar['core_frac']:.3f} R_star = {stellar['core_m']/R_SUN:.4f} R☉")
        print(f"    Tachocline:  {stellar['tachocline_frac']:.3f} R_star")
        print(f"    Photosphere: 1.000 R_star (= cos(α) surface)")
        print(f"    Alfvén:      {stellar['alfven_frac']:.3f} R_star")
        
        print(f"\n  HABITABLE ZONE: {self.hz_inner:.4f} — {self.hz_outer:.4f} AU")
        
        print(f"\n  φ^k PREDICTIONS (occupied and empty rungs):")
        for p in self.predictions:
            if p['r_AU'] > 0.001 and p['r_AU'] < 2:
                status = f"= {p['planet']}" if p['occupied'] else "PREDICTED EMPTY"
                hz = '★ HZ' if p['in_hz'] else ''
                marker = '●' if p['occupied'] else '○'
                print(f"    {marker} k={p['k']:>3} r={p['r_AU']:.4f} AU  {status:<25} {hz}")
        
        if self.empty_hz_rungs:
            print(f"\n  ⚠ {len(self.empty_hz_rungs)} EMPTY RUNG(S) IN HABITABLE ZONE:")
            for p in self.empty_hz_rungs:
                print(f"    k={p['k']}, r={p['r_AU']:.4f} AU — potential undiscovered planet!")
        
        print(f"\n  TRANSIT:")
        t = self.transit
        print(f"    Direct at 0.5c: {t['direct_time_yr']} years")
        print(f"    Vacuum channel: {t['compressed_time_hr']} hours ({t['compression_factor']:.0f}× compression)")
        
        print(f"\n  EXPLORATION SCORE: {score['total']}/100")
        print(f"    φ-Ladder:     {score['ladder']}/30")
        print(f"    Resonance:    {score['resonance']}/20")
        print(f"    Habitable:    {score['habitable']}/20")
        print(f"    Transit:      {score['transit']}/20")
        print(f"    Completeness: {score['completeness']}/10")
        
        return score


# ═══════════════════════════════════════════════════════════════════════
# TEEGARDEN'S STAR — Complete Analysis
# ═══════════════════════════════════════════════════════════════════════

teegarden = SystemAnalyzer(
    name="Teegarden's Star",
    M_star=0.097, R_star=0.107, L_star=0.00073, T_eff=2637,
    distance_ly=12.5,
    planets=[
        {"name":"Teegarden b", "period_d":4.91, "a_AU":0.0252,
         "m_earth":1.05, "ESI":0.90, "T_eq":277,
         "note":"Meridian's Teegarden b — HZ inner"},
        {"name":"Teegarden c", "period_d":11.4, "a_AU":0.0443,
         "m_earth":1.11, "ESI":0.82, "T_eq":209,
         "note":"HZ outer edge"},
        {"name":"Teegarden d", "period_d":26.13, "a_AU":0.0756,
         "m_earth":0.82, "T_eq":160,
         "note":"Beyond HZ, icy moon temps"},
    ]
)

score = teegarden.full_report()

# Check the 172-day mystery signal
print(f"\n{'='*70}")
print("MYSTERY SIGNAL: 172-day period")
print("="*70)
signal = teegarden.check_signal(172)
print(f"  Period: {signal['period_d']} days")
print(f"  Orbit: {signal['a_AU']} AU")
print(f"  φ^k position: k = {signal['k_exact']} → nearest integer k = {signal['k_nearest']}")
print(f"  Predicted rung: {signal['pred_AU']} AU")
print(f"  Error: {signal['error_pct']}%")
print(f"  ON A RUNG: {'YES ✓✓' if signal['on_rung'] else 'NO'}")


# ═══════════════════════════════════════════════════════════════════════
# RENDER: Teegarden System Visualization
# ═══════════════════════════════════════════════════════════════════════

BG='#06080e'; GOLD='#f5c542'; LGOLD='#ffe89a'; BLUE='#4488ff'
PURP='#9944ff'; PINK='#ff4488'; GREEN='#44ff88'; CYAN='#00ddcc'
DIM='#333850'; WHITE='#e8eaf0'; WARM='#ffcc66'; HOT='#ff8833'

outdir = '/mnt/user-data/outputs/renders'
os.makedirs(outdir, exist_ok=True)

# ── System overview ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 14), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')

view = 0.35  # AU
ax.set_xlim(-view, view); ax.set_ylim(-view, view)

# φ^k rungs
for k in range(-5, 8):
    r = teegarden.a0 * PHI**k
    if r < view and r > 0.002:
        alpha_v = 0.3 if k in [r['k'] for r in teegarden.ladder_results] else 0.08
        ax.add_patch(plt.Circle((0,0), r, fc='none', ec='#1a1b2e', lw=0.6, alpha=alpha_v))

# Habitable zone
hz_i, hz_o = teegarden.hz_inner, teegarden.hz_outer
theta = np.linspace(0, 2*np.pi, 200)
ax.fill_between(hz_o*np.cos(theta), hz_o*np.sin(theta), hz_i*np.sin(theta),
                alpha=0.04, color=GREEN)
ax.add_patch(plt.Circle((0,0), hz_i, fc='none', ec=GREEN, lw=0.5, ls='--', alpha=0.3))
ax.add_patch(plt.Circle((0,0), hz_o, fc='none', ec=GREEN, lw=0.5, ls='--', alpha=0.3))

# Star at center
star_r = teegarden.R_star * R_SUN / AU * 50  # exaggerated
ax.add_patch(plt.Circle((0,0), max(star_r, 0.002), fc='#cc3300', ec=HOT, lw=1.5, alpha=0.8))

# Planets
planet_colors = [CYAN, BLUE, PURP]
rng = np.random.default_rng(42)
for i, p in enumerate(teegarden.planets):
    r = p['a_AU']; ang = rng.uniform(0, 2*np.pi)
    px, py = r*np.cos(ang), r*np.sin(ang)
    col = planet_colors[i % len(planet_colors)]
    
    # Orbit
    ax.add_patch(plt.Circle((0,0), r, fc='none', ec=col, lw=1.0, alpha=0.4))
    # Planet
    ms = 6 + p.get('m_earth', 1) * 2
    ax.plot(px, py, 'o', color=col, ms=ms, mec=WHITE, mew=0.5, zorder=10)
    
    # Label
    lr = teegarden.ladder_results[i]
    esi = p.get('ESI', '')
    esi_str = f" ESI={esi}" if esi else ''
    ax.text(px + 0.008, py + 0.008,
            f"{p['name']}\nk={lr['k']} ({lr['error_pct']:.1f}%){esi_str}",
            color=col, fontsize=7, fontfamily='monospace', fontweight='bold')

# 172d mystery signal
if signal['on_rung']:
    r_mystery = signal['a_AU']
    ax.add_patch(plt.Circle((0,0), r_mystery, fc='none', ec=PINK, lw=1.0, ls=':', alpha=0.4))
    ax.text(r_mystery*0.7, -r_mystery*0.7,
            f"172d signal\nk={signal['k_nearest']} ({signal['error_pct']:.1f}%)\nPREDICTED",
            color=PINK, fontsize=7, fontfamily='monospace', fontweight='bold', alpha=0.7)

# Score box
ax.text(-view*0.95, view*0.65,
        f"SCORE: {score['total']}/100\n"
        f"  φ-Ladder: {score['ladder']}/30\n"
        f"  Resonance: {score['resonance']}/20\n"
        f"  Habitable: {score['habitable']}/20\n"
        f"  Transit: {score['transit']}/20\n"
        f"  Complete: {score['completeness']}/10",
        color=LGOLD, fontsize=8, fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.4', fc=BG, ec=GOLD, alpha=0.8, lw=0.5))

# Transit info
t = teegarden.transit
ax.text(view*0.25, -view*0.85,
        f"Distance: {teegarden.distance_ly} ly\n"
        f"Direct: {t['direct_time_yr']} yr at 0.5c\n"
        f"Vacuum channel: {t['compressed_time_hr']} hrs",
        color=CYAN, fontsize=7, fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.3', fc=BG, ec=CYAN, alpha=0.6, lw=0.5))

# Title
ax.text(0, view*0.95, f"Teegarden's Star — ZeckyBOT Analysis",
        color=GOLD, fontsize=15, ha='center', fontfamily='monospace', fontweight='bold')
ax.text(0, view*0.88,
        f"a₀ = 0.387 × {teegarden.M_star}^(1/3) = {teegarden.a0:.4f} AU  ·  "
        f"3 planets + 172d prediction  ·  Score: {score['total']}/100",
        color=DIM, fontsize=8, ha='center', fontfamily='monospace')

fig.savefig(f'{outdir}/teegarden_system.png', dpi=200, facecolor=BG,
            bbox_inches='tight', pad_inches=0.15)
plt.close(fig)
print(f"\n  ✓ Teegarden system render saved")

# Save analysis as JSON
analysis_json = {
    'system': teegarden.name,
    'score': score,
    'ladder': teegarden.ladder_results,
    'resonances': teegarden.resonance_results,
    'mystery_172d': signal,
    'transit': teegarden.transit,
    'predictions': [p for p in teegarden.predictions if not p['occupied']],
}
with open(f'{outdir}/teegarden_analysis.json', 'w') as f:
    json.dump(analysis_json, f, indent=2, default=str)
print(f"  ✓ Analysis JSON saved")
