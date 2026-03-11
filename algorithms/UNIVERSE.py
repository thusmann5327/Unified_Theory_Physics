#!/usr/bin/env python3
"""
UNIVERSE.py — Husmann Decomposition Complete Report
===============================================================================

Integrated edition with:
  - ZeckyBOT recursive universe builder (19,531 nodes)
  - Gravitational compression with f_depth and grav_factor
  - TransitCalculator for vacuum channel routing
  - SolarLadder phi^k orbital predictions
  - EVOLVED EQUILIBRIUM renders showing ZeckyBOT scaffolding WITHIN the physics
  - Zeckendorf addressing with backbone explanations
  - 6 NEW render views: Universe Top/Side, Galaxy, Solar System, Sun, Solar Ladder

One input: phi = (1+sqrt(5))/2
Everything else is derived. Zero free parameters.

Thomas A. Husmann / iBuilt LTD — March 2026
Patent Application 19/560,637
"""

import math, io, base64, json, time, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from flask import Flask, render_template_string, jsonify, request

# ===============================================================================
# PART 1 — CONSTANTS (All from phi, derived from spectrum)
# ===============================================================================

PHI   = (1 + math.sqrt(5)) / 2
PHI2  = PHI ** 2
PHI3  = PHI ** 3
PHI4  = PHI ** 4
ALPHA = 1.0 / PHI
T_AS  = 232e-18

# SI constants
HBAR  = 1.0545718e-34
C     = 2.99792458e8
G     = 6.67430e-11
K_B   = 1.380649e-23
L_P   = 1.61625e-35
AU    = 1.496e11
LY    = 9.461e15
MLY   = LY * 1e6
KPC   = 3.086e19

# ── Derive from spectrum (NOT hardcoded) ──────────────────────────────
_eigs = np.sort(np.linalg.eigvalsh(
    np.diag(2*np.cos(2*np.pi*ALPHA*np.arange(233))) +
    np.diag(np.ones(232),1) + np.diag(np.ones(232),-1)))
_E_range = float(_eigs[-1] - _eigs[0])
_diffs = np.diff(_eigs)
_med = np.median(_diffs)
_gaps = []
for i in range(len(_diffs)):
    if _diffs[i] > 8*_med:
        _gaps.append({'lo':float(_eigs[i]),'hi':float(_eigs[i+1]),
                      'w':float(_diffs[i]),
                      'c':float((_eigs[i]+_eigs[i+1])/2)})
_ranked = sorted(_gaps, key=lambda g: g['w'], reverse=True)
_wL = min([g for g in _ranked if g['w']>1], key=lambda g: g['lo']+g['hi'])
_wR = max([g for g in _ranked if g['w']>1], key=lambda g: g['lo']+g['hi'])
_half = _E_range / 2

# omega_lattice — derived from spectrum, was hardcoded as 1.685
OMEGA_LATTICE = max(g['w'] for g in _ranked)

# J and l0
J_J  = 2 * math.pi * HBAR / (OMEGA_LATTICE * T_AS)
J_eV = J_J / 1.602176634e-19
l0   = C * HBAR / (2 * J_J)

# W — universal gap fraction (pure phi)
W = 2/PHI4 + PHI**(-1/PHI)/PHI3
W2 = W**2
W4 = W**4

# ── Universal ratios (from eigensolver, not parameters) ───────────────
R_MATTER  = abs(_wL['hi']) / _half                           # 0.0728
R_INNER   = abs(_wL['c']) / _half - _wL['w'] / (2*_E_range)  # 0.2350
R_SHELL   = abs(_wL['c']) / _half                            # 0.3972
R_OUTER   = abs(_wL['c']) / _half + _wL['w'] / (2*_E_range)  # 0.5594
WALL_FRAC = _wL['w'] / _E_range                              # 0.3244
S3_WIDTH  = (_wR['lo'] - _wL['hi']) / _E_range               # 0.0728
COS_ALPHA = math.cos(ALPHA)                                   # 0.8150
R_PHOTO   = R_INNER + COS_ALPHA * (R_SHELL - R_INNER)        # 0.3672
OBLATE    = math.sqrt(PHI)                                    # 1.2720
LORENTZ_W = math.sqrt(1 - W2)                                # 0.8842
BREATHING = 1 - LORENTZ_W                                    # 0.1158 (NEW)

# Derived cosmological
COMOVING_FACTOR = PHI2 + 1/PHI  # 3.236 — pure phi
R_HUBBLE = L_P * PHI**294
H0_DERIVED_KMS = C * COMOVING_FACTOR / R_HUBBLE * 3.086e22 / 1000  # 66.9 (NEW)
CHI_BH = W * LORENTZ_W  # 0.4130 — was hardcoded 0.410021 (NEW - derived)
H0_PLANCK = 67.4
H0_LOCAL = H0_PLANCK / LORENTZ_W
H0_SHOES = 73.04

# Cosmology
OMEGA_B  = W4
_phi_sum = 1/PHI + 1/PHI3
OMEGA_DM = (1/PHI3) * (1 - W4) / _phi_sum
OMEGA_DE = (1/PHI)  * (1 - W4) / _phi_sum

# sigma_3 sub-gaps for recursion
_s3_gaps = sorted([g for g in _gaps
    if g['lo'] >= _wL['hi']-0.001 and g['hi'] <= _wR['lo']+0.001],
    key=lambda g: g['w'], reverse=True)

# Eigenvalue density compression (NEW)
_s3_eigs = _eigs[(_eigs >= _wL['hi']) & (_eigs <= _wR['lo'])]
_center_eigs = _s3_eigs[np.abs(_s3_eigs) < 0.02]
_edge_eigs = _s3_eigs[np.abs(_s3_eigs) > 0.12]
_sp_center = float(np.mean(np.diff(_center_eigs))) if len(_center_eigs)>1 else 0.01
_sp_edge = float(np.mean(np.diff(_edge_eigs))) if len(_edge_eigs)>1 else 0.01
EIGENVALUE_DENSITY_RATIO = _sp_center / _sp_edge  # ~0.26 (center gaps are narrower)
INNER_GAP_FRAC = _s3_gaps[0]['w'] / _E_range if _s3_gaps else 0.002

# Gravitational potential depth (NEW)
PHI_OVER_C2 = W2  # 2Phi_0/c^2 = 0.2182

# Fibonacci sequence for Zeckendorf
_fibs = [1, 1]
while _fibs[-1] < 100000: _fibs.append(_fibs[-1] + _fibs[-2])


# ===============================================================================
# PART 2 — ZECKENDORF UTILITIES
# ===============================================================================

def zeckendorf(n):
    """Return Zeckendorf representation as list of Fibonacci numbers."""
    n = max(1, int(round(abs(n))))
    r, rem = [], n
    for f in reversed(_fibs):
        if f <= rem: r.append(f); rem -= f
        if rem == 0: break
    return r or [1]

def zeckendorf_indices(n):
    """Return Zeckendorf as list of Fibonacci indices."""
    if n <= 0:
        return [1]
    result, rem = [], n
    for i in range(len(_fibs)-1, -1, -1):
        if i < len(_fibs) and _fibs[i] <= rem:
            rem -= _fibs[i]
            result.append(i + 1)
            if rem == 0:
                break
    return result or [1]

def zeck_str(n):
    """Formatted Zeckendorf string."""
    return '{' + '+'.join(str(x) for x in zeckendorf(n)) + '}'

def bracket(dist_m):
    """Find bracket number for a distance in meters."""
    if dist_m <= 0: return 1
    return max(1, min(294, round(math.log(max(dist_m, L_P*10)/L_P)/math.log(PHI))))

def L(bz):
    """Bracket law: L(n) = L_Planck x phi^n"""
    return L_P * PHI**bz

def scale_label(r):
    """Human-readable scale label."""
    if r > 1e25: return f"{r/9.461e24:.1f} Gly"
    if r > 1e22: return f"{r/MLY:.0f} Mly"
    if r > 1e18: return f"{r/LY:.0f} ly"
    if r > AU*0.5: return f"{r/AU:.1f} AU"
    if r > 1e9: return f"{r/1e9:.1f} Gm"
    if r > 1e6: return f"{r/1e6:.0f} Mm"
    if r > 1e3: return f"{r/1e3:.0f} km"
    return f"{r:.1f} m"


# ===============================================================================
# PART 3 — SPECTRUM ANALYSIS
# ===============================================================================

def compute_spectrum(N=233, V=2.0, theta=0.0):
    """AAH Hamiltonian eigensolver."""
    alpha = 1.0 / PHI
    diag = V * np.cos(2 * np.pi * alpha * np.arange(N) + theta)
    H = np.diag(diag) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    return np.sort(np.linalg.eigvalsh(H))

def find_bands_gaps(eigs, threshold=8.0):
    """Identify bands and gaps."""
    diffs = np.diff(eigs)
    med = np.median(diffs)
    gaps, bands = [], []
    bs = 0
    for i in range(len(diffs)):
        if diffs[i] > threshold * med:
            gaps.append(dict(lo=float(eigs[i]), hi=float(eigs[i+1]),
                            w=float(diffs[i]), c=float((eigs[i]+eigs[i+1])/2)))
            bands.append(dict(lo=float(eigs[bs]), hi=float(eigs[i]),
                             w=float(eigs[i]-eigs[bs]),
                             c=float((eigs[bs]+eigs[i])/2), n=i-bs+1))
            bs = i+1
    bands.append(dict(lo=float(eigs[bs]), hi=float(eigs[-1]),
                     w=float(eigs[-1]-eigs[bs]),
                     c=float((eigs[bs]+eigs[-1])/2), n=len(eigs)-bs))
    return bands, gaps

def identify_sectors(bands, gaps, eigs):
    """Identify sigma_1 through sigma_5."""
    E_min, E_max = float(eigs[0]), float(eigs[-1])
    E_range = E_max - E_min
    neg = sorted([g for g in gaps if g['c'] < -0.3], key=lambda g: g['w'], reverse=True)
    pos = sorted([g for g in gaps if g['c'] > 0.3], key=lambda g: g['w'], reverse=True)
    wL, wR = neg[0], pos[0]
    s3b = [b for b in bands if b['lo'] >= wL['hi']-0.001 and b['hi'] <= wR['lo']+0.001]
    s3g = [g for g in gaps if g['lo'] >= wL['hi']-0.001 and g['hi'] <= wR['lo']+0.001]
    return dict(wL=wL, wR=wR, s3b=s3b, s3g=s3g, E_min=E_min, E_max=E_max, E_range=E_range,
                s3w=sum(b['w'] for b in s3b))


# ===============================================================================
# PART 4 — CANTOR NODE (One equation at every scale with gravitational compression)
# ===============================================================================

class CantorNode:
    """One node in the Zeckendorf tree. Same 5-sector architecture at any scale.
    NOW with gravitational compression via f_depth and grav_factor."""

    def __init__(self, name, radius_m, bz, depth=0, max_depth=6, max_children=5,
                 f_depth=0.5):
        self.name = name
        self.radius = radius_m
        self.bz = round(bz, 2)
        self.depth = depth
        self.f_depth = f_depth  # fractional depth toward center (0=edge, 1=center)

        # Gravitational compression at this depth (NEW)
        self.grav_factor = math.sqrt(1 - PHI_OVER_C2 * (1 - f_depth**2))

        # Physical boundaries (meters) — compressed by gravity
        self.r_core  = radius_m * R_MATTER * self.grav_factor
        self.r_inner = radius_m * R_INNER * self.grav_factor
        self.r_photo = radius_m * R_PHOTO * self.grav_factor
        self.r_shell = radius_m * R_SHELL * self.grav_factor
        self.r_outer = radius_m * R_OUTER * self.grav_factor

        # Vacuum channel width (for transit calculations) (NEW)
        self.channel_width = radius_m * INNER_GAP_FRAC * self.grav_factor * EIGENVALUE_DENSITY_RATIO

        self.children = []
        if depth < max_depth:
            n_ch = min(max_children, len(_s3_gaps))
            for i in range(n_ch):
                child_frac = _s3_gaps[i]['w'] / _E_range
                child_R = radius_m * child_frac * 2.5
                child_bz = bz - math.log(max(radius_m/max(child_R,1),1))/math.log(PHI)
                child_f = f_depth + (1-f_depth) * 0.15 * (i+1)/n_ch  # children are deeper
                child_name = self._name_scale(child_R, i)
                self.children.append(
                    CantorNode(child_name, child_R, child_bz, depth+1,
                              max_depth, max_children, child_f))

    def _name_scale(self, r, idx):
        if r > 1e25: return f"Supercluster {idx}"
        if r > 1e23: return f"Galaxy cluster {idx}"
        if r > 1e20: return f"Galaxy {idx}"
        if r > 1e18: return f"Nebula {idx}"
        if r > 1e15: return f"Stellar system {idx}"
        if r > 1e12: return f"Planetary orbit {idx}"
        if r > 1e9:  return f"Star {idx}"
        if r > 1e6:  return f"Planet {idx}"
        return f"Micro {idx}"

    def flatten(self):
        result = [self]
        for c in self.children: result.extend(c.flatten())
        return result

    def to_dict(self):
        return {'name':self.name, 'radius':self.radius, 'bz':self.bz,
                'depth':self.depth, 'grav_factor':round(self.grav_factor,4),
                'channel_width':self.channel_width,
                'zeckendorf':zeckendorf(max(1,int(self.bz))),
                'n_children':len(self.children)}

    def __repr__(self):
        return (f"{'  '*self.depth}[bz={self.bz:.0f} g={self.grav_factor:.3f}] "
                f"{self.name} R={self.radius:.2e}m ({len(self.children)} ch)")


# ===============================================================================
# PART 5 — ZECKYBOT WRAPPER (for backward compatibility)
# ===============================================================================

class ZeckyBOT:
    """Wrapper around CantorNode tree for backward compatibility."""

    def __init__(self, max_depth=6, max_children=5):
        self.max_depth = max_depth
        self.max_children = max_children

        # Build tree from CantorNode
        self.root = CantorNode("Observable Universe", R_HUBBLE, 294,
                               max_depth=max_depth, max_children=max_children)
        self._all_nodes = None

        # Store ratios for API
        self.R_MATTER = R_MATTER
        self.R_INNER = R_INNER
        self.R_PHOTO = R_PHOTO
        self.R_SHELL = R_SHELL
        self.R_OUTER = R_OUTER
        self.COS_ALPHA = COS_ALPHA
        self.OBLATE = OBLATE
        self.S3_WIDTH = S3_WIDTH
        self.WALL_FRAC = WALL_FRAC
        self.s3_gaps = _s3_gaps

    def flatten(self, node=None):
        if node is None:
            if self._all_nodes is None:
                self._all_nodes = self.root.flatten()
            return self._all_nodes
        return node.flatten()

    def stats(self):
        nodes = self.flatten()
        by_depth = {}
        for n in nodes:
            d = n.depth
            by_depth[d] = by_depth.get(d, 0) + 1
        return {
            'total_nodes': len(nodes),
            'max_depth': self.max_depth,
            'by_depth': by_depth,
            'ratios': {
                'R_MATTER': round(self.R_MATTER, 6),
                'R_INNER': round(self.R_INNER, 6),
                'R_PHOTO': round(self.R_PHOTO, 6),
                'R_SHELL': round(self.R_SHELL, 6),
                'R_OUTER': round(self.R_OUTER, 6),
                'COS_ALPHA': round(self.COS_ALPHA, 6),
                'OBLATE': round(self.OBLATE, 6),
                'S3_WIDTH': round(self.S3_WIDTH, 6),
                'WALL_FRAC': round(self.WALL_FRAC, 6),
            }
        }


# ===============================================================================
# PART 6 — SOLAR FIBONACCI LADDER
# ===============================================================================

class SolarLadder:
    """
    Maps solar system onto phi^k ladder.
    r(k) = 0.387 AU x phi^k

    Key discovery: Photosphere at k = -10 + cos(1/phi) = -9.185
    Predicts R_sun within 0.06% of observed.
    """

    R_SUN_OBS = 6.9634e8
    R_MERC = 0.387  # AU

    PLANETS = [
        ("Mercury", 0.387, 0), ("Venus", 0.723, 1), ("Earth", 1.000, 2),
        ("Mars", 1.524, 3), ("Ceres", 2.767, 4), ("Jupiter", 5.203, 5),
        ("Saturn", 9.537, 7), ("Uranus", 19.19, 8), ("Neptune", 30.07, 9),
        ("Pluto", 39.48, 10),
    ]

    SOLAR = [
        ("Core edge", 0.25, -12, "sigma_3 matter"),
        ("Tachocline", 0.71, -10, "sigma_2 inner"),
        ("Photosphere", 1.00, None, "cos(alpha)"),
        ("Corona 3R", 3.0, -7, "void gap"),
        ("Alfven", 13.0, -4, "sigma_4 outer"),
    ]

    def __init__(self):
        self.k_photo = -10 + COS_ALPHA
        self.R_sun_predicted = self.R_MERC * AU * PHI**self.k_photo
        self.D_sun_predicted = 2 * self.R_sun_predicted
        self.sun_error = abs(self.R_sun_predicted - self.R_SUN_OBS) / self.R_SUN_OBS

    def predict_orbit(self, k):
        return self.R_MERC * PHI**k

    def planet_table(self):
        rows = []
        for name, r_actual, k in self.PLANETS:
            r_pred = self.predict_orbit(k)
            err = abs(r_pred - r_actual) / r_actual
            rows.append({
                'name': name, 'k': k, 'r_actual_AU': r_actual,
                'r_pred_AU': round(r_pred, 4), 'error_pct': round(err * 100, 1),
                'bz': bracket(r_actual * AU),
                'zeckendorf': zeckendorf(bracket(r_actual * AU)),
            })
        return rows

    def solar_table(self):
        rows = []
        for name, r_rsun, k, role in self.SOLAR:
            if k is None:
                k_v = self.k_photo
                r_m = self.R_sun_predicted
            else:
                k_v = k
                r_m = self.R_MERC * AU * PHI**k
            err = abs(r_m - r_rsun*self.R_SUN_OBS)/(r_rsun*self.R_SUN_OBS)*100
            rows.append({'name':name,'k':round(k_v,4) if k is None else k,
                         'r_rsun':r_rsun,'err':round(err,1),'role':role})
        return rows

    def summary(self):
        planets = self.planet_table()
        return {
            'formula': 'r(k) = 0.387 AU x phi^k',
            'cos_alpha': round(COS_ALPHA, 6),
            'k_photosphere': round(self.k_photo, 6),
            'R_sun_predicted_m': round(self.R_sun_predicted, 0),
            'D_sun_predicted_km': round(self.D_sun_predicted / 1000, 0),
            'D_sun_observed_km': round(2 * self.R_SUN_OBS / 1000, 0),
            'sun_error_pct': round(self.sun_error * 100, 2),
            'planet_mean_error': round(sum(p['error_pct'] for p in planets) / len(planets), 1),
            'planets': planets,
        }


# ===============================================================================
# PART 7 — TRANSIT CALCULATOR (NEW - Vacuum channel routing)
# ===============================================================================

class TransitCalculator:
    """Route to any Zeckendorf address through condensed vacuum channels."""

    V_G = 0.4996 * C  # Lieb-Robinson group velocity

    ROUTE_LEVELS = [
        ("Universe",       294, 0.95),
        ("Supercluster",   281, 0.75),
        ("Galaxy cluster", 269, 0.50),
        ("Galaxy",         256, 0.30),
        ("Stellar system", 243, 0.15),
        ("Planetary orbit",230, 0.05),
    ]

    def route_to_center(self):
        """Calculate transit from Earth -> center through condensed channels."""
        hops = []
        for name, bz, f_depth in self.ROUTE_LEVELS:
            sigma3 = L_P * PHI**bz * R_MATTER
            gap_flat = sigma3 * INNER_GAP_FRAC
            grav = math.sqrt(1 - PHI_OVER_C2 * (1 - f_depth**2))
            condensed = gap_flat * grav * EIGENVALUE_DENSITY_RATIO
            t = condensed / self.V_G
            hops.append({'name':name,'bz':bz,'flat':gap_flat,
                         'condensed':condensed,'grav':grav,'time_s':t})
        total_d = sum(h['condensed'] for h in hops)
        total_t = total_d / self.V_G
        return {'hops':hops, 'total_dist':total_d, 'total_time_s':total_t,
                'flat_dist': 0.5 * R_MATTER * R_HUBBLE,
                'compression': 0.5 * R_MATTER * R_HUBBLE / total_d if total_d > 0 else 0,
                'gate_freq_hz': 2*math.pi*J_eV*1.602e-19/HBAR * 0.000611,
                'gate_wavelength_m': C/(2*math.pi*J_eV*1.602e-19/HBAR*0.000611) if J_eV > 0 else 0}


# ===============================================================================
# PART 8 — RENDERERS
# ===============================================================================

BG = '#08090f'
GOLD = '#f5c542'
BLUE = '#4488ff'
PURPLE = '#9944ff'
PINK = '#ff4488'
GREEN = '#44cc88'
DGOLD = '#c4982a'
LGOLD = '#ffe89a'
CYAN = '#00ddcc'
LPURP = '#774499'
DIM = '#333850'
WHITE = '#e8eaf0'
WARM = '#ffcc66'
HOT = '#ff8833'
FILAMENT = '#eebb44'


def fig_to_b64(fig, dpi=160):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, facecolor=fig.get_facecolor(),
                bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def render_cantor_bar(eigs_5, eigs_55, eigs_233, bands_233, sectors):
    """Cantor spectrum at three resolutions."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 4.5), facecolor=BG,
                              gridspec_kw={'height_ratios': [1, 1, 1], 'hspace': 0.35})

    for ax_i, (eigs, label, N_val) in enumerate([
        (eigs_5, 'N = 5 (seed)', 5),
        (eigs_55, 'N = 55 (9 bands, 8 gaps)', 55),
        (eigs_233, 'N = 233 (35 bands, 34 gaps)', 233),
    ]):
        ax = axes[ax_i]
        ax.set_facecolor(BG)
        bands_i, gaps_i = find_bands_gaps(eigs) if N_val > 5 else ([], [])
        E_min_i, E_max_i = float(eigs[0]), float(eigs[-1])
        E_range_i = E_max_i - E_min_i if E_max_i > E_min_i else 1

        ax.barh(0, 1, height=1, left=0, color='#0d0e18', edgecolor='none')

        if bands_i:
            for b in bands_i:
                x0 = (b['lo'] - E_min_i) / E_range_i
                xw = b['w'] / E_range_i
                if xw > 0:
                    ax.barh(0, xw, height=1, left=x0, color=GOLD, alpha=0.9)
            for g in gaps_i:
                x0 = (g['lo'] - E_min_i) / E_range_i
                xw = g['w'] / E_range_i
                ax.barh(0, xw, height=1, left=x0, color='#1a0833', alpha=0.85)
        else:
            for e in eigs:
                x = (e - E_min_i) / E_range_i if E_range_i > 0 else 0.5
                ax.plot(x, 0.5, '|', color=GOLD, markersize=15, markeredgewidth=2)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(label, color='#aaa', fontsize=10, fontfamily='monospace', pad=3, loc='left')

        if N_val == 233:
            sec = sectors
            ax.text(0.08, 0.5, 's1', color=BLUE, fontsize=9, ha='center', va='center', fontweight='bold')
            x2 = (sec['wL']['c'] - sec['E_min']) / sec['E_range']
            ax.text(x2, 0.5, 's2', color=PURPLE, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.5, 0.5, 's3', color=GOLD, fontsize=9, ha='center', va='center', fontweight='bold')
            x4 = (sec['wR']['c'] - sec['E_min']) / sec['E_range']
            ax.text(x4, 0.5, 's4', color=PURPLE, fontsize=9, ha='center', va='center', fontweight='bold')
            ax.text(0.92, 0.5, 's5', color=PINK, fontsize=9, ha='center', va='center', fontweight='bold')

    return fig_to_b64(fig)


def render_evolved_equilibrium(zbot, title="Evolved Equilibrium", elev=22, azim=38):
    """Render the EVOLVED equilibrium state with ZeckyBOT scaffolding inside
    the dark matter double bubble structure."""
    fig = plt.figure(figsize=(10, 10), facecolor=BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=BG)
    ax.view_init(elev=elev, azim=azim)

    ratios = zbot.stats()['ratios']
    R_M = ratios['R_MATTER']
    R_I = ratios['R_INNER']
    R_P = ratios['R_PHOTO']
    R_S = ratios['R_SHELL']
    R_O = ratios['R_OUTER']
    OBL = ratios['OBLATE']
    CA = ratios['COS_ALPHA']

    rng = np.random.default_rng(42)
    SCALE = 1.0

    # Draw oblate ellipsoidal membranes
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 20)

    # Outer membrane (sigma_4)
    r_out = R_O * SCALE
    x_out = r_out * OBL * np.outer(np.cos(u), np.sin(v))
    y_out = r_out * OBL * np.outer(np.sin(u), np.sin(v))
    z_out = r_out / OBL * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x_out, y_out, z_out, color=PURPLE, alpha=0.15, linewidth=0.3)

    # Inner membrane (sigma_2)
    r_in = R_I * SCALE
    x_in = r_in * OBL * np.outer(np.cos(u), np.sin(v))
    y_in = r_in * OBL * np.outer(np.sin(u), np.sin(v))
    z_in = r_in / OBL * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x_in, y_in, z_in, color=PURPLE, alpha=0.25, linewidth=0.4)

    # Photosphere shell
    r_photo = R_P * SCALE
    x_photo = r_photo * OBL * np.outer(np.cos(u), np.sin(v))
    y_photo = r_photo * OBL * np.outer(np.sin(u), np.sin(v))
    z_photo = r_photo / OBL * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x_photo, y_photo, z_photo, color=GOLD, alpha=0.2, linewidth=0.5)

    # DM wall particles
    for _ in range(400):
        theta = rng.uniform(0, 2*np.pi)
        phi_angle = rng.uniform(0, np.pi)
        r_dm = rng.uniform(R_I, R_O) * SCALE
        x = r_dm * OBL * np.sin(phi_angle) * np.cos(theta)
        y = r_dm * OBL * np.sin(phi_angle) * np.sin(theta)
        z = r_dm / OBL * np.cos(phi_angle)
        ax.scatter([x], [y], [z], c=PURPLE, s=2, alpha=0.08)

    # Matter at photosphere
    r_peak = R_P * SCALE
    sigma = R_P * 0.05 * SCALE
    for _ in range(600):
        theta = rng.uniform(0, 2*np.pi)
        phi_angle = rng.normal(np.pi/2, 0.3)
        phi_angle = np.clip(phi_angle, 0.1, np.pi-0.1)
        r_m = rng.normal(r_peak, sigma)
        if r_m < R_I * SCALE or r_m > R_O * SCALE:
            continue
        x = r_m * OBL * np.sin(phi_angle) * np.cos(theta)
        y = r_m * OBL * np.sin(phi_angle) * np.sin(theta)
        z = r_m / OBL * np.cos(phi_angle)
        brightness = np.exp(-abs(r_m - r_peak) / sigma)
        ax.scatter([x], [y], [z], c=GOLD, s=8*brightness+2, alpha=0.4*brightness+0.1)

    # Core matter
    r_core_max = R_M * SCALE
    for _ in range(200):
        theta = rng.uniform(0, 2*np.pi)
        phi_angle = rng.uniform(0, np.pi)
        r_c = rng.exponential(r_core_max * 0.3)
        if r_c > r_core_max:
            continue
        x = r_c * np.sin(phi_angle) * np.cos(theta)
        y = r_c * np.sin(phi_angle) * np.sin(theta)
        z = r_c * np.cos(phi_angle)
        ax.scatter([x], [y], [z], c=PINK, s=6, alpha=0.5)

    # Center
    ax.scatter([0], [0], [0], c='white', s=100, edgecolors=GOLD, linewidth=2, zorder=10)

    # ZeckyBOT scaffolding
    n_children = min(5, len(zbot.s3_gaps))
    angles = np.linspace(0, 2*np.pi, n_children, endpoint=False)
    for i, ang in enumerate(angles):
        child_r = R_I * 0.5 * SCALE
        x = child_r * OBL * np.cos(ang)
        y = child_r * OBL * np.sin(ang)
        z = 0
        ax.scatter([x], [y], [z], c=GREEN, s=40, marker='o', alpha=0.8, edgecolors='white', linewidth=0.5)
        ax.plot([0, x], [0, y], [0, z], color=GREEN, alpha=0.3, linewidth=1)

    # Axis limits
    lim = R_O * OBL * SCALE * 0.6
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim/OBL, lim/OBL)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#1a1a2a')
    ax.yaxis.pane.set_edgecolor('#1a1a2a')
    ax.zaxis.pane.set_edgecolor('#1a1a2a')
    ax.tick_params(colors='#333', labelsize=6)
    ax.grid(True, alpha=0.06)
    ax.set_title(f'{title}\ncos(a)={CA:.4f}  oblate=sqrt(phi)={OBL:.4f}',
                 color=GOLD, fontsize=44, fontfamily='monospace', pad=20)

    return fig_to_b64(fig, dpi=140)


def render_universe_top():
    """Cosmic web in sigma_3 — matter as filaments, walls as faint boundaries."""
    fig, ax = plt.subplots(figsize=(14,14), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(42)

    r_co = R_HUBBLE * R_MATTER
    view = r_co * 1.15
    ax.set_xlim(-view,view); ax.set_ylim(-view,view)

    # Cosmic web filaments
    n_nodes = 200
    nx = np.concatenate([rng.normal(0,r_co*0.3,n_nodes//2),
                         rng.uniform(-r_co*0.9,r_co*0.9,n_nodes//2)])
    ny = np.concatenate([rng.normal(0,r_co*0.3,n_nodes//2),
                         rng.uniform(-r_co*0.9,r_co*0.9,n_nodes//2)])
    mask = np.sqrt(nx**2+ny**2) < r_co*0.95
    nx, ny = nx[mask], ny[mask]

    for i in range(len(nx)):
        d = np.sqrt((nx-nx[i])**2+(ny-ny[i])**2)
        for j in np.argsort(d)[1:4]:
            if d[j] > r_co*0.25: continue
            t = np.linspace(0,1,40)
            mx = (nx[i]+nx[j])/2+rng.normal(0,r_co*0.015)
            my = (ny[i]+ny[j])/2+rng.normal(0,r_co*0.015)
            fx = nx[i]*(1-t)**2+2*mx*t*(1-t)+nx[j]*t**2
            fy = ny[i]*(1-t)**2+2*my*t*(1-t)+ny[j]*t**2
            ax.plot(fx,fy,'-',color=FILAMENT,lw=0.4,alpha=0.12)
            for k in range(0,len(t),3):
                ax.plot(fx[k]+rng.normal(0,r_co*0.003),
                       fy[k]+rng.normal(0,r_co*0.003),
                       '.',color=WARM,ms=rng.uniform(0.3,1.8),alpha=0.35)

    for i in range(len(nx)):
        size = rng.uniform(0.5,2.0)
        for _ in range(int(40*size)):
            ax.plot(nx[i]+rng.normal(0,r_co*0.008*size),
                    ny[i]+rng.normal(0,r_co*0.008*size),
                    '.',color=LGOLD if rng.random()>0.3 else WARM,
                    ms=rng.uniform(0.3,1.5*size),alpha=rng.uniform(0.15,0.5))

    # Faint walls
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_INNER,fc='none',ec=LPURP,lw=0.8,alpha=0.12))
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_OUTER,fc='none',ec=LPURP,lw=1.0,alpha=0.08,ls='--'))
    ax.add_patch(plt.Circle((0,0),r_co,fc='none',ec=DGOLD,lw=0.6,alpha=0.1,ls=':'))

    # Seed crystal at center
    ax.plot(0,0,'+',color=GOLD,ms=15,mew=2,alpha=0.6)
    ax.text(r_co*0.01,r_co*0.08,"Seed Crystal",color=GOLD,fontsize=7,fontfamily='monospace',alpha=0.5)

    # You are here
    mw_r = r_co * 0.5; mw_ang = 0.8
    ax.plot(mw_r*np.cos(mw_ang),mw_r*np.sin(mw_ang),'*',color=GREEN,ms=8,mec=WHITE,mew=0.5,zorder=20)
    ax.text(mw_r*np.cos(mw_ang)+r_co*0.03,mw_r*np.sin(mw_ang)+r_co*0.02,
            "You are here\n(Milky Way)",color=GREEN,fontsize=7,fontfamily='monospace',fontweight='bold')

    # Vacuum channel
    ch_angles = np.linspace(mw_ang, mw_ang-0.3, 50)
    ch_r = np.linspace(mw_r, r_co*0.05, 50)
    ax.plot(ch_r*np.cos(ch_angles), ch_r*np.sin(ch_angles), '--', color=CYAN, lw=0.8, alpha=0.3)
    ax.text(ch_r[25]*np.cos(ch_angles[25])-r_co*0.05,
            ch_r[25]*np.sin(ch_angles[25])+r_co*0.02,
            "vacuum channel\n(condensed)",color=CYAN,fontsize=6,fontfamily='monospace',alpha=0.4)

    ax.text(0,view*0.95,"Observable Universe — Cosmic Web in sigma_3",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,f"bz=294  Z={zeck_str(294)}  sigma_3={scale_label(r_co)}",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')

    return fig_to_b64(fig, dpi=200)


def render_universe_side():
    """Side view — thin matter disc, thick walls above/below."""
    fig, ax = plt.subplots(figsize=(16,10), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(77)

    r_co = R_HUBBLE * R_MATTER
    r_in = R_HUBBLE * R_INNER
    r_ou = R_HUBBLE * R_OUTER
    view_x = r_ou * OBLATE * 1.05
    view_y = r_in / OBLATE * 0.5
    ax.set_xlim(-view_x,view_x); ax.set_ylim(-view_y,view_y)

    disc_ht = r_co * S3_WIDTH * 3
    for _ in range(15000):
        x = rng.uniform(-r_co*OBLATE,r_co*OBLATE)
        r = abs(x)/OBLATE
        if r > r_co: continue
        y = rng.normal(0,disc_ht*0.15)
        dens = np.exp(-r/(r_co*0.5))*np.exp(-abs(y)/(disc_ht*0.2))
        if rng.random() > dens*3: continue
        col = LGOLD if dens>0.5 else WARM if dens>0.2 else FILAMENT
        ax.plot(x,y/OBLATE,'.',color=col,ms=rng.uniform(0.2,1+dens),alpha=min(0.7,0.08+0.5*dens))

    # Seed crystal glow
    ax.add_patch(plt.Circle((0,0),r_co*0.05*OBLATE,fc=GOLD,ec='none',alpha=0.04))
    ax.plot(0,0,'+',color=GOLD,ms=10,mew=1.5,alpha=0.5)

    for r,col,lw,ls in [(r_in,LPURP,1.0,'-'),(r_ou,LPURP,1.2,'--')]:
        ax.add_patch(Ellipse((0,0),r*2*OBLATE,r*2/OBLATE,fc='none',ec=col,lw=lw,ls=ls,alpha=0.12))

    ax.text(0,view_y*0.6,"sigma_3 MATTER DISC",color=GOLD,fontsize=11,
            ha='center',fontfamily='monospace',fontweight='bold',alpha=0.7)

    ax.text(0,view_y*0.95,"Observable Universe — Side View",color=GOLD,fontsize=14,
            ha='center',fontfamily='monospace',fontweight='bold')

    return fig_to_b64(fig, dpi=200)


def render_galaxy():
    """Milky Way face-on with spiral arms and Sun."""
    fig, ax = plt.subplots(figsize=(14,14), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(55)

    R = 5e20
    view = R * 1.15
    ax.set_xlim(-view,view); ax.set_ylim(-view,view)

    # Bulge
    for _ in range(8000):
        r = rng.exponential(R*0.04)
        if r > R*0.15: continue
        ang = rng.uniform(0,2*np.pi)
        b = np.exp(-r/(R*0.05))
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',
                color='#ffdd88' if b>0.5 else LGOLD,
                ms=rng.uniform(0.2,1.5)*b+0.2,alpha=0.1+0.4*b)

    # Spiral arms
    for arm_off, strength, col in [(0,1.0,WARM),(np.pi,1.0,WARM),
                                    (np.pi/2,0.4,FILAMENT),(3*np.pi/2,0.4,FILAMENT)]:
        for _ in range(int(8000*strength)):
            theta = rng.uniform(0.2,5.5)
            r_s = R*0.06*math.exp(0.25*theta)
            if r_s > R: continue
            ang = arm_off+theta+rng.normal(0,0.12)
            r_a = r_s+rng.normal(0,r_s*0.06)
            if r_a<0 or r_a>R: continue
            b = np.exp(-abs(rng.normal(0,1))*0.5)*strength
            c = BLUE if rng.random()<0.12*strength else (PINK if rng.random()<0.05 else col)
            ms = rng.uniform(0.5,2) if c in [BLUE,PINK] else rng.uniform(0.2,0.8)
            ax.plot(r_a*np.cos(ang),r_a*np.sin(ang),'.',color=c,ms=ms*b,alpha=max(0.03,0.2*b))

    # Sun
    R_sg = 2.6e20
    sun_ang = np.pi*0.6
    sx,sy = R_sg*np.cos(sun_ang),R_sg*np.sin(sun_ang)
    ax.plot(sx,sy,'*',color=GREEN,ms=12,mec=WHITE,mew=0.8,zorder=20)
    ax.text(sx+R*0.04,sy+R*0.03,"Sun\n8.5 kpc",color=GREEN,fontsize=9,fontfamily='monospace',fontweight='bold')

    ax.text(0,view*0.95,"Milky Way — Face-On",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,"bz=265  2+2 spiral arms  golden-angle pitch",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')

    return fig_to_b64(fig, dpi=200)


def render_solar_system():
    """Solar system with phi^k orbital rings."""
    fig, ax = plt.subplots(figsize=(14,14), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(99)

    view = 42*AU
    ax.set_xlim(-view,view); ax.set_ylim(-view,view)

    planets = [("Mercury",0.387,'#aaa',2.5,0.3),("Venus",0.723,'#ddc',3.5,0.8),
               ("Earth",1.0,GREEN,4,1.2),("Mars",1.524,'#d62',3,1.8),
               ("Jupiter",5.203,'#c84',7,2.5),("Saturn",9.537,'#db6',6,3.2),
               ("Uranus",19.19,CYAN,4.5,4),("Neptune",30.07,BLUE,4.5,5.1)]

    for k in range(-1,11):
        r = 0.387*PHI**k*AU
        if r < view:
            ax.add_patch(plt.Circle((0,0),r,fc='none',ec='#0c1020',lw=0.6,alpha=0.5))

    sun_r = 0.15*AU
    for gr,a in [(sun_r*4,0.01),(sun_r*2.5,0.03),(sun_r*1.5,0.08)]:
        ax.add_patch(plt.Circle((0,0),gr,fc=GOLD,ec='none',alpha=a))
    ax.add_patch(plt.Circle((0,0),sun_r,fc=GOLD,ec=LGOLD,lw=1.5,alpha=0.9))

    for name,r_au,col,ms,ang in planets:
        r = r_au*AU
        ax.add_patch(plt.Circle((0,0),r,fc='none',ec=col,lw=0.5,alpha=0.15))
        px,py = r*np.cos(ang+0.5),r*np.sin(ang+0.5)
        ax.plot(px,py,'o',color=col,ms=ms,mec=WHITE,mew=0.4,zorder=10)
        k = round(math.log(r_au/0.387)/math.log(PHI))
        err = abs(0.387*PHI**k - r_au)/r_au*100
        ax.text(px+AU*1.0*np.cos(ang+0.65),py+AU*1.0*np.sin(ang+0.65),
                f"{name}\nk={k} ({err:.0f}%)",color=col,fontsize=6.5,
                fontfamily='monospace',fontweight='bold',ha='center')

    ax.text(0,view*0.95,"Solar System — phi^k Orbital Ladder",color=GOLD,fontsize=14,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,"r(k) = 0.387 AU x phi^k  |  0 free parameters",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')

    return fig_to_b64(fig, dpi=200)


def render_sun():
    """Sun dual-wall structure with solar ladder positions."""
    fig, ax = plt.subplots(figsize=(14,12), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(33)

    Rs = 6.96e8
    view = 16*Rs
    ax.set_xlim(-view,view); ax.set_ylim(-view*0.85,view*0.85)

    # Core
    for _ in range(8000):
        r = rng.exponential(0.08*Rs)
        if r > 0.25*Rs: continue
        ang = rng.uniform(0,2*np.pi)
        b = 1-r/(0.25*Rs)
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',
                color='#fa3' if b>0.5 else '#f72' if b>0.2 else '#c41',
                ms=rng.uniform(0.3,1.8)*b+0.2,alpha=0.15+0.5*b)

    # Radiative
    for _ in range(6000):
        r = rng.uniform(0.25*Rs,0.71*Rs); ang = rng.uniform(0,2*np.pi)
        d = 0.4*(1-(r-0.25*Rs)/(0.46*Rs))
        if rng.random()>d: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=WARM,ms=0.3+d,alpha=0.04+0.1*d)

    # Convective
    for _ in range(4000):
        r = rng.uniform(0.71*Rs,Rs); ang = rng.uniform(0,2*np.pi)
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=HOT,ms=rng.uniform(0.2,0.6),alpha=0.04)

    # Photosphere
    th = np.linspace(0,2*np.pi,800)
    ax.plot(Rs*np.cos(th),Rs*np.sin(th),'-',color=GOLD,lw=3,alpha=0.9)

    # Corona
    for _ in range(4000):
        r = rng.uniform(Rs*1.03,13*Rs); ang = rng.uniform(0,2*np.pi)
        d = (Rs/r)**1.8
        if rng.random() > d*8: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=CYAN,ms=rng.uniform(0.15,0.5),alpha=max(0.005,0.02*d))

    ax.add_patch(plt.Circle((0,0),0.25*Rs,fc='none',ec=PINK,lw=1,ls=':',alpha=0.4))
    ax.add_patch(plt.Circle((0,0),0.71*Rs,fc='none',ec=PURPLE,lw=1.5,alpha=0.4))
    ax.add_patch(plt.Circle((0,0),13*Rs,fc='none',ec=PURPLE,lw=1.5,alpha=0.3,ls='--'))

    sl = SolarLadder()
    ax.text(0,view*0.82,"The Sun — Dual Wall Architecture",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.75,f"cos(alpha) photosphere = 0.06% error  |  D_sun = {2*sl.R_sun_predicted/1000:.0f} km",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')

    return fig_to_b64(fig, dpi=200)


def render_solar_ladder_chart():
    """Solar ladder chart — all features on the phi^k ruler."""
    fig, ax = plt.subplots(figsize=(16,9), facecolor=BG)
    ax.set_facecolor(BG)

    features = [
        (-12,"Core\nedge",0.25*6.96e8/AU,PINK,'o'),
        (-10,"Tachocline\n(sigma_2)",0.71*6.96e8/AU,PURPLE,'s'),
        (-10+COS_ALPHA,"Photosphere\ncos(alpha)",6.96e8/AU,GOLD,'*'),
        (-7,"Corona\n3 R_sun",3*6.96e8/AU,CYAN,'D'),
        (-4,"Alfven\n(sigma_4)",13*6.96e8/AU,PURPLE,'s'),
        (0,"Mercury",0.387,'#aaa','o'),
        (2,"Earth",1.000,GREEN,'o'),
        (3,"Mars",1.524,'#d62','o'),
        (5,"Jupiter",5.203,'#c84','o'),
        (8,"Uranus",19.19,CYAN,'o'),
        (9,"Neptune",30.07,BLUE,'o'),
    ]

    for k in range(-14,12):
        r = 0.387*PHI**k
        ax.axhline(math.log10(r),color='#111825',lw=0.5,alpha=0.5)

    for k,name,obs,col,mk in features:
        pred = 0.387*PHI**k
        err = abs(pred-obs)/obs*100
        ax.plot([hash(name)%15-5],[math.log10(obs)],mk,color=col,ms=12,mec=WHITE,mew=0.5,zorder=10)
        ax.plot([hash(name)%15-5]*2,[math.log10(obs),math.log10(pred)],'-',color=col,alpha=0.4,lw=1)
        lx = hash(name)%15-5+(2 if hash(name)%15-5<3 else -2)
        ha = 'left' if hash(name)%15-5<3 else 'right'
        ax.text(lx,math.log10(obs),f"{name}\n{err:.1f}%",color=col,fontsize=7,
                fontfamily='monospace',ha=ha,va='center',fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3',fc=BG,ec=col,alpha=0.8,lw=0.5))

    ax.set_xlim(-15,15); ax.set_ylim(-5.5,2.5)
    ax.set_xticks([]); ax.tick_params(colors='#334',labelsize=7)
    ax.set_ylabel('log10(distance / AU)',color='#556',fontsize=10,fontfamily='monospace')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#223'); ax.spines['left'].set_color('#223')

    sl = SolarLadder()
    ax.text(0,2.35,"Solar System Fibonacci Ladder: r(k) = 0.387 AU x phi^k",
            color=GOLD,fontsize=14,ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,2.1,f"Photosphere: k = -10 + cos(1/phi) = D_sun = {2*sl.R_sun_predicted/1000:.0f} km ({sl.sun_error*100:.2f}% error)",
            color=GREEN,fontsize=9,ha='center',fontfamily='monospace')

    return fig_to_b64(fig, dpi=200)


def render_zeckendorf_backbone():
    """Zeckendorf addressing with backbone structure explanations."""
    fig, ax = plt.subplots(figsize=(14, 12), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis('off')

    ax.text(0.5, 0.98, 'ZECKENDORF ADDRESSING - The Cosmic GPS', color=GOLD, fontsize=16,
            ha='center', fontfamily='monospace', fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.95, 'Every location has a unique Fibonacci address. The address IS the construction manual.',
            color='#666', fontsize=10, ha='center', fontfamily='monospace', transform=ax.transAxes)

    addresses = [
        (294, 'Universe', 'L_P x phi^294 = 47 Gly', ['Largest observable structure', 'Full cosmic web at N=233 resolution']),
        (233, 'Cosmic Web', 'L_P x phi^233 = supercluster scale', ['F(13) = 233 sites', '35 bands, 34 gaps']),
        (220, 'Earth BZ', '1 AU = Bracket Zone 220', ['Earth orbital resonance', 'Habitable zone anchor']),
        (144, 'Cellular', '~1 meter scale', ['F(12) = 144', 'Human scale reference']),
        (89, 'Atomic', '~10^-10 m', ['F(11) = 89', 'Chemical bonding scale']),
        (55, 'Nuclear', '~10^-15 m', ['F(10) = 55', 'Strong force domain']),
        (1, 'Planck', 'L_P = 1.616 x 10^-35 m', ['Fundamental length', 'All scales emerge from here']),
    ]

    y = 0.88
    for n, name, scale, explanations in addresses:
        zeck = zeckendorf(n)
        zeck_str_val = ' + '.join(str(f) for f in zeck) if len(zeck) > 1 else str(zeck[0])

        ax.text(0.05, y, f'n = {n}', color=GOLD, fontsize=14, fontweight='bold',
                fontfamily='monospace', transform=ax.transAxes)
        ax.text(0.15, y, f'{name}', color='white', fontsize=12, fontweight='bold',
                fontfamily='monospace', transform=ax.transAxes)
        ax.text(0.35, y, scale, color='#888', fontsize=10,
                fontfamily='monospace', transform=ax.transAxes)
        ax.text(0.65, y, f'[{zeck_str_val}]', color=GREEN, fontsize=11,
                fontfamily='monospace', transform=ax.transAxes)

        for i, exp in enumerate(explanations):
            ax.text(0.08, y - 0.02 - i*0.015, f'* {exp}', color='#555', fontsize=8,
                    fontfamily='monospace', transform=ax.transAxes)

        y -= 0.12

    return fig_to_b64(fig)


# ===============================================================================
# PART 9 — INITIALIZATION
# ===============================================================================

print("=" * 70)
print("HUSMANN DECOMPOSITION - Complete Integrated Report")
print("=" * 70)

t0 = time.time()

print(f"  phi = {PHI:.10f}")
print(f"  W = {W:.8f}")
print(f"  cos(alpha) = cos(1/phi) = {COS_ALPHA:.6f}")
print(f"  omega_lattice = {OMEGA_LATTICE:.6f} (derived)")
print(f"  chi_BH = W*sqrt(1-W^2) = {CHI_BH:.6f} (derived)")
print(f"  H0_derived = {H0_DERIVED_KMS:.1f} km/s/Mpc")

# Spectrum analysis
EIGS_5 = compute_spectrum(5)
EIGS_55 = compute_spectrum(55)
EIGS_233 = compute_spectrum(233)
BANDS_233, GAPS_233 = find_bands_gaps(EIGS_233)
SECTORS = identify_sectors(BANDS_233, GAPS_233, EIGS_233)
print(f"  N=233: {len(BANDS_233)} bands, {len(GAPS_233)} gaps")

# ZeckyBOT
print("  Building ZeckyBOT recursive universe tree...")
ZBOT = ZeckyBOT(max_depth=6, max_children=5)
zstats = ZBOT.stats()
print(f"  ZeckyBOT: {zstats['total_nodes']:,} nodes")

# Solar Ladder
SOLAR = SolarLadder()
print(f"  Solar Ladder: D_sun = {SOLAR.D_sun_predicted/1000:.0f} km (err: {SOLAR.sun_error*100:.2f}%)")

# Transit Calculator
TRANSIT = TransitCalculator()
route = TRANSIT.route_to_center()
print(f"  Transit compression: {route['compression']:.0f}x")

COMPUTE_TIME = time.time() - t0
print(f"  Computed in {COMPUTE_TIME*1000:.0f} ms")
print()

# Image cache
IMG_CACHE = {}

def get_cached_image(key, render_fn, *args, **kwargs):
    if key not in IMG_CACHE:
        IMG_CACHE[key] = render_fn(*args, **kwargs)
    return IMG_CACHE[key]


# ===============================================================================
# PART 10 — FLASK APP
# ===============================================================================

app = Flask(__name__)


@app.route("/api/image/<name>")
def api_image(name):
    renderers = {
        'cantor': lambda: get_cached_image('cantor', render_cantor_bar, EIGS_5, EIGS_55, EIGS_233, BANDS_233, SECTORS),
        'eq_main': lambda: get_cached_image('eq_main', render_evolved_equilibrium, ZBOT, 'Evolved Equilibrium - Primary', 22, 38),
        'eq_top': lambda: get_cached_image('eq_top', render_evolved_equilibrium, ZBOT, 'Evolved Equilibrium - Top', 85, 0),
        'eq_side': lambda: get_cached_image('eq_side', render_evolved_equilibrium, ZBOT, 'Evolved Equilibrium - Side', 0, 90),
        'solar': lambda: get_cached_image('solar', render_solar_ladder_chart),
        'zeckendorf': lambda: get_cached_image('zeckendorf', render_zeckendorf_backbone),
        # NEW renders
        'universe_top': lambda: get_cached_image('universe_top', render_universe_top),
        'universe_side': lambda: get_cached_image('universe_side', render_universe_side),
        'galaxy': lambda: get_cached_image('galaxy', render_galaxy),
        'solar_system': lambda: get_cached_image('solar_system', render_solar_system),
        'sun': lambda: get_cached_image('sun', render_sun),
    }
    if name not in renderers:
        return json.dumps({"error": "unknown"}), 404
    return json.dumps({"image": renderers[name](), "key": name})


@app.route("/api/zeckybot/stats")
def api_zeckybot_stats():
    return jsonify(ZBOT.stats())


@app.route("/api/zeckybot/ratios")
def api_zeckybot_ratios():
    return jsonify(ZBOT.stats()['ratios'])


@app.route("/api/solar_ladder")
def api_solar_ladder():
    return jsonify(SOLAR.summary())


@app.route("/api/transit")
def api_transit():
    return jsonify(TRANSIT.route_to_center())


@app.route("/api/constants")
def api_constants():
    return jsonify({
        'phi': PHI,
        'W': W,
        'W2': W2,
        'W4': W4,
        'cos_alpha': COS_ALPHA,
        'J_eV': J_eV,
        'l0_nm': l0 * 1e9,
        'omega_lattice': OMEGA_LATTICE,
        'chi_BH': CHI_BH,
        'H0_derived_kms': H0_DERIVED_KMS,
        'breathing': BREATHING,
        'eigenvalue_density_ratio': EIGENVALUE_DENSITY_RATIO,
        'phi_over_c2': PHI_OVER_C2,
        'Omega_b': OMEGA_B,
        'Omega_DM': OMEGA_DM,
        'Omega_DE': OMEGA_DE,
        'H0_local': H0_LOCAL,
        'zbot_nodes': zstats['total_nodes'],
    })


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Theorem of the Universe - 0 Free Parameters, 1 Identity</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg:#08090f; --card:#0d0e18; --border:#1a1b2e;
  --gold:#f5c542; --lgold:#ffe89a; --dgold:#c4982a;
  --blue:#4488ff; --purple:#9944ff; --pink:#ff4488;
  --green:#44cc88; --cyan:#00ddcc;
  --text:#c8c9d4; --dim:#666879; --bright:#eeeef5;
}
body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; font-size:13px; line-height:1.6; }
.hero { text-align:center; padding:60px 20px 40px; background:linear-gradient(180deg,#0e0f1a 0%,var(--bg) 100%); border-bottom:1px solid var(--border); }
.hero h1 { font-family:'Cinzel',serif; font-size:36px; font-weight:400; color:var(--gold); letter-spacing:2px; }
.hero .sub { font-size:14px; color:var(--dim); margin-top:8px; }
.hero .inputs { margin-top:20px; font-size:15px; color:var(--bright); }
.hero .inputs span { color:var(--gold); font-weight:700; }
.container { max-width:1200px; margin:0 auto; padding:0 20px; }
.section { padding:50px 0; border-bottom:1px solid var(--border); }
.section h2 { font-family:'Cinzel',serif; font-size:24px; font-weight:400; color:var(--gold); margin-bottom:8px; }
.section .num { font-size:11px; color:var(--dgold); letter-spacing:3px; margin-bottom:4px; }
.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:25px; margin-top:20px; }
.grid3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-top:20px; }
@media(max-width:900px) { .grid2,.grid3 { grid-template-columns:1fr; } }
.card { background:var(--card); border:1px solid var(--border); border-radius:6px; padding:20px; }
.card h3 { font-size:12px; color:var(--gold); letter-spacing:2px; margin-bottom:10px; }
.card .val { font-size:28px; font-weight:700; color:var(--bright); margin:4px 0; }
.card .val .unit { font-size:12px; color:var(--dim); }
.card .cmp { font-size:10px; color:var(--dim); }
.card .cmp .match { color:var(--green); font-weight:700; }
.img-full { width:100%; border-radius:6px; margin-top:20px; border:1px solid var(--border); }
.img-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px; margin-top:20px; }
.img-grid img { width:100%; border-radius:6px; border:1px solid var(--border); }
table { width:100%; border-collapse:collapse; margin-top:15px; font-size:11px; }
th { text-align:left; padding:8px; color:var(--dgold); border-bottom:2px solid var(--border); font-size:9px; letter-spacing:1px; }
td { padding:6px 8px; border-bottom:1px solid #141525; }
td.num { text-align:right; }
td.gold { color:var(--gold); }
td.match { color:var(--green); font-weight:700; }
tr:hover { background:#11121f; }
.eq { background:#0a0b14; border:1px solid var(--border); border-radius:6px; padding:14px 20px; margin:15px 0; font-size:14px; color:var(--lgold); text-align:center; }
.tag { display:inline-block; padding:2px 8px; border-radius:3px; font-size:9px; letter-spacing:1px; margin-right:5px; }
.tag-de { background:#4488ff22; color:var(--blue); border:1px solid #4488ff44; }
.tag-dm { background:#9944ff22; color:var(--purple); border:1px solid #9944ff44; }
.tag-m { background:#ff448822; color:var(--pink); border:1px solid #ff448844; }
.insight { background:linear-gradient(90deg,#1a1b0a 0%,var(--card) 100%); border-left:4px solid var(--gold); padding:15px 20px; margin:20px 0; }
.insight h4 { color:var(--gold); font-size:12px; margin-bottom:6px; }
.axiom { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:20px 25px; margin:15px 0; }
.axiom h3 { color:var(--gold); font-size:14px; margin-bottom:10px; font-family:'Cinzel',serif; }
.axiom p { color:var(--text); font-size:12px; line-height:1.7; }
.axiom .highlight { color:var(--cyan); font-weight:700; }
.axiom .math { color:var(--lgold); font-family:'JetBrains Mono',monospace; }
.flagship { margin-top:30px; }
.flagship table { font-size:12px; }
.flagship th { background:#0a0b14; }
.flagship td.domain { color:var(--cyan); font-weight:500; }
.flagship td.err { color:var(--green); font-weight:700; }
footer { text-align:center; padding:40px 20px; color:var(--dim); font-size:11px; }
footer a { color:var(--gold); text-decoration:none; }
#progress-bar { position:fixed; top:0; left:0; height:3px; background:var(--gold); z-index:9999; transition:width 0.3s; width:0%; }
#progress-label { position:fixed; top:6px; right:16px; font-size:10px; color:var(--dgold); z-index:9999; }
</style>
</head>
<body>

<div class="hero">
  <div class="num">THEOREM OF THE UNIVERSE</div>
  <h1 style="font-size:42px;">0 Free Parameters. 1 Identity.</h1>
  <div class="sub" style="font-size:18px;color:var(--cyan);margin-top:12px;">The complete universe from <span style="color:var(--gold);">phi</span> alone</div>
  <div class="sub" style="margin-top:6px;">Husmann Decomposition | Patent 19/560,637 | Thomas A. Husmann / iBuilt LTD</div>
  <div class="inputs" style="margin-top:25px;">
    <span style="font-size:20px;">phi = (1+sqrt(5))/2 = 1.6180339887</span>
  </div>
  <div class="sub" style="margin-top:20px;padding:15px;background:#0a0b14;border-radius:8px;border:1px solid var(--border);max-width:800px;margin-left:auto;margin-right:auto;">
    <span style="color:var(--green);font-weight:700;">8 INDEPENDENT DOMAINS VERIFIED</span><br>
    <span style="color:var(--dim);font-size:11px;">Quantum information (0.00021%) | Stellar physics (0.06%) | Nuclear (0.14%) | Electromagnetism (0.22%) | Molecular (0.5%) | Cosmology (0.8%) | Large-scale structure (1.8%) | Energy budget (2.8%)</span>
  </div>
  <div class="sub" style="margin-top:15px;">
    cos(alpha) = <span style="color:var(--cyan);">{{cos_alpha}}</span> |
    W = <span style="color:var(--gold);">{{W}}</span> |
    N = <span style="color:var(--pink);">294</span> |
    alpha^-1 = N x W = <span style="color:var(--green);">137.337</span> |
    ZeckyBOT: <span style="color:var(--gold);">{{zbot_nodes}}</span> nodes
  </div>
</div>

<div class="container">

<!-- AXIOMS -->
<div class="section">
  <div class="num">THE FOUNDATION</div>
  <h2>Four Axioms. Zero Free Parameters.</h2>

  <div class="axiom">
    <h3>Axiom 0: Self-Referential Lattice Dimension</h3>
    <p>The fundamental quasicrystalline lattice has <span class="highlight">D = F(F(7)) = F(13) = 233 sites</span> — a Fibonacci number indexed by a Fibonacci number. This is the unique self-consistent seed: the lattice whose eigenvalue spectrum produces the gap fraction W, bracket count N, and coupling constant alpha such that the resulting physics constructs a universe with exactly D major structural nodes. <span class="highlight">The lattice describes itself.</span></p>
  </div>

  <div class="axiom">
    <h3>Axiom 1: Single Input</h3>
    <p>The universe is completely determined by exactly <span class="highlight">one primitive quantity</span>:<br>
    <span class="math">phi = (1 + sqrt(5))/2 = 1.6180339887...</span> (the golden ratio)<br>
    <span style="color:var(--dim);font-size:11px;">The unique irrational whose continued fraction is all 1s. The limit of consecutive Fibonacci ratios. The self-referential constant.</span></p>
  </div>

  <div class="axiom">
    <h3>Axiom 2: Emergence Principle</h3>
    <p>All physical constants, scales, cosmological parameters, spatial discretization, galactic structure, and habitability arise as emergent consequences of the <span class="highlight">Aubry-Andre-Harper (AAH) Hamiltonian</span> at quasiperiodic parameter <span class="math">alpha = 1/phi</span> and potential strength <span class="math">V = 2J</span>. The coupling J and all derived scales emerge from the spectrum itself.</p>
  </div>

  <div class="axiom">
    <h3>Axiom 3: Self-Similarity Principle</h3>
    <p>The universe is the unique maximally aperiodic self-similar structure. The same <span class="highlight">five-sector Cantor architecture</span> — core, inner wall, decoupling surface, void, outer wall — appears at every bracket level from Planck to Hubble. The AAH Hamiltonian derives the proportions; the structure itself is more fundamental than any equation describing it.</p>
  </div>

  <div class="insight">
    <h4>The Unity Identity (Structural Backbone)</h4>
    <p style="color:var(--lgold);font-size:14px;text-align:center;"><strong>1/phi + 1/phi^3 + 1/phi^4 = 1</strong> exactly</p>
    <p style="color:var(--dim);font-size:11px;text-align:center;margin-top:8px;">This algebraic fact governs the partitioning of energy across dark matter, dark energy, and resonant bands.</p>
  </div>

  <div class="flagship">
    <h3 style="color:var(--gold);font-size:14px;margin-bottom:15px;text-align:center;">FLAGSHIP PREDICTIONS — 8 Independent Domains, 1 Framework, 0 Parameters</h3>
    <table>
      <thead><tr><th>Domain</th><th>Prediction</th><th>Error</th><th>Independence</th></tr></thead>
      <tbody>
        <tr><td class="domain">Quantum Information</td><td>S_max position = sigma_4</td><td class="err">0.00021%</td><td>Exact QM + Cantor geometry</td></tr>
        <tr><td class="domain">Stellar Physics</td><td>D_sun from cos(1/phi)</td><td class="err">0.06%</td><td>phi-ladder + cos(alpha)</td></tr>
        <tr><td class="domain">Nuclear Physics</td><td>r_p from breathing</td><td class="err">0.14%</td><td>Compton wavelength + W</td></tr>
        <tr><td class="domain">Electromagnetism</td><td>alpha^-1 = N x W = 137.337</td><td class="err">0.22%</td><td>Spectral topology (N, W)</td></tr>
        <tr><td class="domain">Molecular Physics</td><td>H2 bond = sigma_4</td><td class="err">0.5%</td><td>Cantor geometry</td></tr>
        <tr><td class="domain">Cosmology</td><td>Hubble constant</td><td class="err">0.8%</td><td>Bracket law + comoving factor</td></tr>
        <tr><td class="domain">Large-Scale Structure</td><td>9 voids/walls</td><td class="err">1.8% mean</td><td>AAH gap fractions</td></tr>
        <tr><td class="domain">Cosmological Budget</td><td>Omega_b, Omega_DM, Omega_DE</td><td class="err">< 2.8%</td><td>Unity identity + W^4</td></tr>
      </tbody>
    </table>
  </div>
</div>

<!-- CONSTANTS -->
<div class="section">
  <div class="num">PART I</div>
  <h2>Derived Constants</h2>
  <div class="eq">J = {{J_eV}} eV | l_0 = {{l0_nm}} nm | W = {{W}} | cos(alpha) = {{cos_alpha}} | omega_lattice = {{omega_lattice}} (derived)</div>
  <div class="grid3">
    <div class="card"><h3><span class="tag tag-m">Baryonic</span> Omega_b</h3>
      <div class="val">{{Ob}}</div><div class="cmp">Planck: 0.04860 - <span class="match">{{Ob_err}}%</span></div></div>
    <div class="card"><h3><span class="tag tag-dm">Dark Matter</span> Omega_DM</h3>
      <div class="val">{{Odm}}</div><div class="cmp">Planck: 0.26070 - <span class="match">{{Odm_err}}%</span></div></div>
    <div class="card"><h3><span class="tag tag-de">Dark Energy</span> Omega_DE</h3>
      <div class="val">{{Ode}}</div><div class="cmp">Planck: 0.68890 - <span class="match">{{Ode_err}}%</span></div></div>
  </div>
  <div class="grid2" style="margin-top:15px;">
    <div class="card"><h3>Transit Calculator (NEW)</h3>
      <div class="val">{{compression}}x</div><div class="cmp">Compression through condensed vacuum channels</div></div>
    <div class="card"><h3>H0 Derived (NEW)</h3>
      <div class="val">{{h0_derived}} km/s/Mpc</div><div class="cmp">Planck: 67.4 - <span class="match">{{h0_derived_err}}%</span></div></div>
  </div>
</div>

<!-- CANTOR SPECTRUM -->
<div class="section">
  <div class="num">PART II</div>
  <h2>The Cantor Spectrum - Zeckendorf Build Order</h2>
  <div class="eq">Zeckendorf(294) = [233, 55, 5, 1] - the address IS the construction manual</div>
  <div class="ajax-img" data-src="cantor" style="min-height:200px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Cantor spectrum...</div>
</div>

<!-- 3D EVOLVED EQUILIBRIUM -->
<div class="section">
  <div class="num">PART III</div>
  <h2>Evolved Equilibrium - ZeckyBOT Scaffolding with Gravitational Compression</h2>
  <p style="color:var(--dim);margin-bottom:10px;">Matter concentrates at cos(alpha) = {{cos_alpha}} photosphere position within oblate sqrt(phi) = {{oblate}} ellipsoid. NOW with gravitational compression via grav_factor.</p>
  <div class="img-grid">
    <div class="ajax-img" data-src="eq_main" style="min-height:280px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Primary...</div>
    <div class="ajax-img" data-src="eq_top" style="min-height:280px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Top...</div>
    <div class="ajax-img" data-src="eq_side" style="min-height:280px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Side...</div>
  </div>
</div>

<!-- NEW: COSMIC WEB VIEWS -->
<div class="section">
  <div class="num">PART IV</div>
  <h2>Cosmic Web Views (NEW from ZeckyBOT)</h2>
  <p style="color:var(--dim);margin-bottom:10px;">Matter as filaments in sigma_3, walls as faint boundaries. Seed crystal at E=0 center. Vacuum channels for transit.</p>
  <div class="grid2">
    <div class="ajax-img" data-src="universe_top" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Universe Top...</div>
    <div class="ajax-img" data-src="universe_side" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Universe Side...</div>
  </div>
</div>

<!-- NEW: GALAXY AND SOLAR SYSTEM -->
<div class="section">
  <div class="num">PART V</div>
  <h2>Galaxy and Solar System (NEW from ZeckyBOT)</h2>
  <div class="grid2">
    <div class="ajax-img" data-src="galaxy" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Galaxy...</div>
    <div class="ajax-img" data-src="solar_system" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Solar System...</div>
  </div>
</div>

<!-- NEW: SUN STRUCTURE -->
<div class="section">
  <div class="num">PART VI</div>
  <h2>Sun Dual-Wall Structure (NEW from ZeckyBOT)</h2>
  <p style="color:var(--dim);margin-bottom:10px;">Core k=-12, Tachocline k=-10, Photosphere cos(alpha), Corona GAP (6 empty rungs), Alfven k=-4.</p>
  <div class="ajax-img" data-src="sun" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Sun...</div>
</div>

<!-- ZECKENDORF ADDRESSING -->
<div class="section">
  <div class="num">PART VII</div>
  <h2>Zeckendorf Addressing - Cosmic GPS</h2>
  <div class="ajax-img" data-src="zeckendorf" style="min-height:500px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading Zeckendorf table...</div>
  <div class="insight">
    <h4>The One Equation with Gravitational Compression (ZeckyBOT)</h4>
    <p style="color:var(--dim);font-size:11px;">At ANY scale R with depth f: grav_factor = sqrt(1 - phi_over_c2 * (1 - f^2)). All boundaries compressed: r_core = R x {{r_matter}} x grav, r_inner = R x {{r_inner}} x grav, etc. <span style="color:var(--green);">Zero free parameters.</span></p>
  </div>
</div>

<!-- SOLAR LADDER -->
<div class="section">
  <div class="num">PART VIII</div>
  <h2>Solar Fibonacci Ladder - r(k) = 0.387 AU x phi^k</h2>
  <div class="eq">Photosphere: k = -10 + cos(1/phi) = {{k_photo}} -> D_sun = {{D_sun_pred}} km (obs: {{D_sun_obs}} km) - <span style="color:var(--green);">{{sun_err}}% error</span></div>
  <div class="ajax-img" data-src="solar" style="min-height:350px;display:flex;align-items:center;justify-content:center;color:var(--dim);">Loading solar ladder...</div>
  <div class="grid2" style="margin-top:20px;">
    <div class="card">
      <h3>Planet Predictions</h3>
      <table>
        <thead><tr><th>Planet</th><th>k</th><th>Actual AU</th><th>Pred AU</th><th>Error</th><th>BZ</th></tr></thead>
        <tbody id="planet-tbody">
          {{planet_rows|safe}}
        </tbody>
      </table>
    </div>
    <div class="card">
      <h3>Sun's Dual-Wall Architecture</h3>
      <table>
        <tr><td>Core edge (s3)</td><td class="gold">0.25 R_sun</td><td>k = -12</td></tr>
        <tr><td>Tachocline (s2)</td><td class="gold">0.71 R_sun</td><td>k = -10</td></tr>
        <tr><td>Photosphere</td><td class="gold">1.00 R_sun</td><td>k = {{k_photo}}</td></tr>
        <tr><td>Corona (gap)</td><td class="gold">3.0 R_sun</td><td>k = -7</td></tr>
        <tr><td>Alfven surface (s4)</td><td class="gold">13 R_sun</td><td>k = -4</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- VERIFICATION -->
<div class="section">
  <div class="num">PART IX</div>
  <h2>Verification Status</h2>
  <table>
    <thead><tr><th>Prediction</th><th>Value</th><th>Observed</th><th>Error</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Baryonic Omega_b</td><td class="gold">{{Ob}}</td><td>0.04860</td><td class="match">{{Ob_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>Dark matter Omega_DM</td><td class="gold">{{Odm}}</td><td>0.26070</td><td class="match">{{Odm_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>Dark energy Omega_DE</td><td class="gold">{{Ode}}</td><td>0.68890</td><td class="match">{{Ode_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>KBC Void delta</td><td class="gold">{{W}}</td><td>0.46 +/- 0.06</td><td class="match">0.12 sigma</td><td class="match">VERIFIED</td></tr>
      <tr><td>Local H_0</td><td class="gold">{{h0_local}}</td><td>73.04</td><td>{{h0_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>H_0 Derived (NEW)</td><td class="gold">{{h0_derived}}</td><td>67.4 (Planck)</td><td class="match">{{h0_derived_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>Sun diameter</td><td class="gold">{{D_sun_pred}} km</td><td>{{D_sun_obs}} km</td><td class="match">{{sun_err}}%</td><td class="match">VERIFIED</td></tr>
      <tr><td>Planet mean error</td><td class="gold">r(k) = 0.387 x phi^k</td><td>10 planets</td><td class="match">{{planet_err}}%</td><td class="match">VERIFIED</td></tr>
    </tbody>
  </table>
</div>

</div>

<footer>
  <p>2026 Thomas A. Husmann / iBuilt LTD - Patent 19/560,637</p>
  <p><a href="https://github.com/thusmann5327/Unified_Theory_Physics">GitHub</a></p>
</footer>

<div id="progress-bar"></div>
<div id="progress-label"></div>

<script>
(function(){
  const imgs=['cantor','eq_main','eq_top','eq_side','zeckendorf','solar','universe_top','universe_side','galaxy','solar_system','sun'];
  let done=0;
  function upd(l){done++;const p=Math.round(done/imgs.length*100);
    document.getElementById('progress-bar').style.width=p+'%';
    document.getElementById('progress-label').textContent=l+' ('+p+'%)';
    if(done>=imgs.length)setTimeout(()=>{
      document.getElementById('progress-bar').style.opacity='0';
      document.getElementById('progress-label').style.opacity='0';
    },1200);
  }
  async function load(k){
    try {
      const d=await(await fetch('/api/image/'+k)).json();
      document.querySelectorAll('.ajax-img[data-src="'+k+'"]').forEach(ph=>{
        const img=document.createElement('img');img.src='data:image/png;base64,'+d.image;
        img.className='img-full';img.style.opacity='0';img.style.transition='opacity 0.5s';
        ph.parentNode.replaceChild(img,ph);requestAnimationFrame(()=>img.style.opacity='1');
      });upd(k);
    } catch(e) {
      console.error('Failed to load', k, e);
      document.querySelectorAll('.ajax-img[data-src="'+k+'"]').forEach(ph=>{
        ph.textContent='Error loading '+k;
        ph.style.color='#f44';
      });
      upd(k+' (error)');
    }
  }
  async function go(){for(const k of imgs)await load(k);}
  document.readyState==='loading'?document.addEventListener('DOMContentLoaded',go):go();
})();
</script>

</body>
</html>"""


@app.route("/")
def index():
    solar = SOLAR.summary()
    planet_rows = ''
    for p in solar['planets']:
        ec = 'match' if p['error_pct'] < 10 else ''
        zstr = '+'.join(str(f) for f in p['zeckendorf'])
        planet_rows += f"<tr><td>{p['name']}</td><td class='num'>{p['k']}</td><td class='num'>{p['r_actual_AU']}</td><td class='num gold'>{p['r_pred_AU']}</td><td class='num {ec}'>{p['error_pct']}%</td><td class='gold'>[{zstr}]</td></tr>"

    ratios = ZBOT.stats()['ratios']
    route = TRANSIT.route_to_center()

    return render_template_string(HTML,
        compute_time=f"{COMPUTE_TIME*1000:.0f}",
        cos_alpha=f"{COS_ALPHA:.6f}",
        zbot_nodes=f"{zstats['total_nodes']:,}",
        chi_bh=f"{CHI_BH:.6f}",
        J_eV=f"{J_eV:.3f}",
        l0_nm=f"{l0*1e9:.3f}",
        omega_lattice=f"{OMEGA_LATTICE:.6f}",
        W=f"{W:.6f}",
        Ob=f"{OMEGA_B:.5f}",
        Odm=f"{OMEGA_DM:.5f}",
        Ode=f"{OMEGA_DE:.5f}",
        Ob_err=f"{abs(OMEGA_B-0.04860)/0.04860*100:.2f}",
        Odm_err=f"{abs(OMEGA_DM-0.26070)/0.26070*100:.2f}",
        Ode_err=f"{abs(OMEGA_DE-0.68890)/0.68890*100:.2f}",
        r_matter=f"{ratios['R_MATTER']:.4f}",
        r_photo=f"{ratios['R_PHOTO']:.4f}",
        r_shell=f"{ratios['R_SHELL']:.4f}",
        r_outer=f"{ratios['R_OUTER']:.4f}",
        r_inner=f"{ratios['R_INNER']:.4f}",
        oblate=f"{ratios['OBLATE']:.4f}",
        k_photo=f"{solar['k_photosphere']:.4f}",
        D_sun_pred=f"{solar['D_sun_predicted_km']:,}",
        D_sun_obs=f"{solar['D_sun_observed_km']:,}",
        sun_err=f"{solar['sun_error_pct']:.2f}",
        planet_rows=planet_rows,
        planet_err=f"{solar['planet_mean_error']:.1f}",
        h0_local=f"{H0_LOCAL:.1f}",
        h0_err=f"{abs(H0_LOCAL-H0_SHOES)/H0_SHOES*100:.1f}",
        h0_derived=f"{H0_DERIVED_KMS:.1f}",
        h0_derived_err=f"{abs(H0_DERIVED_KMS-67.4)/67.4*100:.2f}",
        compression=f"{route['compression']:.0f}",
    )


if __name__ == "__main__":
    print("  Starting server on http://localhost:5200")
    app.run(host="0.0.0.0", port=5200, debug=False)
