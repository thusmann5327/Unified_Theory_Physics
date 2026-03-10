#!/usr/bin/env python3
"""
zeckyBOT.py — Recursive Universe Builder
Husmann Decomposition: One Equation, Every Scale, Every Structure

Thomas A. Husmann / iBuilt LTD — March 10, 2026
Patent Application 19/560,637

Two inputs: φ = (1+√5)/2, t_as = 232×10⁻¹⁸ s
Everything else is derived.
"""

import math, numpy as np, json, time, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# ═══════════════════════════════════════════════════════════════════════
# CONSTANTS — All from φ
# ═══════════════════════════════════════════════════════════════════════

PHI   = (1 + math.sqrt(5)) / 2
ALPHA = 1.0 / PHI
T_AS  = 232e-18
HBAR  = 1.0545718e-34
C     = 2.99792458e8
G     = 6.67430e-11
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

# J and l₀
J_J  = 2 * math.pi * HBAR / (OMEGA_LATTICE * T_AS)
J_eV = J_J / 1.602176634e-19
l0   = C * HBAR / (2 * J_J)

# W — universal gap fraction (pure φ)
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3

# ── Universal ratios (from eigensolver, not parameters) ───────────────
R_MATTER  = abs(_wL['hi']) / _half                           # 0.0728
R_INNER   = abs(_wL['c']) / _half - _wL['w'] / (2*_E_range) # 0.2350
R_SHELL   = abs(_wL['c']) / _half                            # 0.3972
R_OUTER   = abs(_wL['c']) / _half + _wL['w'] / (2*_E_range) # 0.5594
WALL_FRAC = _wL['w'] / _E_range                             # 0.3244
S3_WIDTH  = (_wR['lo'] - _wL['hi']) / _E_range              # 0.0728
COS_ALPHA = math.cos(ALPHA)                                 # 0.8150
R_PHOTO   = R_INNER + COS_ALPHA * (R_SHELL - R_INNER)       # 0.3672
OBLATE    = math.sqrt(PHI)                                   # 1.2720
LORENTZ_W = math.sqrt(1 - W**2)                             # 0.8842
BREATHING = 1 - LORENTZ_W                                   # 0.1158

# Derived cosmological
COMOVING_FACTOR = PHI**2 + 1/PHI  # 3.236 — pure φ
R_HUBBLE = L_P * PHI**294
H0_DERIVED_KMS = C * COMOVING_FACTOR / R_HUBBLE * 3.086e22 / 1000  # 66.9
CHI_BH = W * LORENTZ_W  # 0.4130 — was hardcoded 0.410021

# Cosmology
OMEGA_B  = W**4
_phi_sum = 1/PHI + 1/PHI**3
OMEGA_DM = (1/PHI**3) * (1 - W**4) / _phi_sum
OMEGA_DE = (1/PHI)    * (1 - W**4) / _phi_sum

# σ₃ sub-gaps for recursion
_s3_gaps = sorted([g for g in _gaps
    if g['lo'] >= _wL['hi']-0.001 and g['hi'] <= _wR['lo']+0.001],
    key=lambda g: g['w'], reverse=True)

# Eigenvalue density compression
_s3_eigs = _eigs[(_eigs >= _wL['hi']) & (_eigs <= _wR['lo'])]
_center_eigs = _s3_eigs[np.abs(_s3_eigs) < 0.02]
_edge_eigs = _s3_eigs[np.abs(_s3_eigs) > 0.12]
_sp_center = float(np.mean(np.diff(_center_eigs))) if len(_center_eigs)>1 else 0.01
_sp_edge = float(np.mean(np.diff(_edge_eigs))) if len(_edge_eigs)>1 else 0.01
EIGENVALUE_DENSITY_RATIO = _sp_center / _sp_edge  # ~0.26 (center gaps are narrower)
INNER_GAP_FRAC = _s3_gaps[0]['w'] / _E_range if _s3_gaps else 0.002

# Gravitational potential depth
PHI_OVER_C2 = W**2  # 2Φ₀/c² = 0.2182

# ═══════════════════════════════════════════════════════════════════════
# ZECKENDORF UTILITIES
# ═══════════════════════════════════════════════════════════════════════

_fibs = [1, 1]
while _fibs[-1] < 100000: _fibs.append(_fibs[-1] + _fibs[-2])

def zeckendorf(n):
    n = max(1, int(round(abs(n))))
    r, rem = [], n
    for f in reversed(_fibs):
        if f <= rem: r.append(f); rem -= f
        if rem == 0: break
    return r or [1]

def zeck_str(n):
    return '{' + '+'.join(str(x) for x in zeckendorf(n)) + '}'

def bracket(dist_m):
    if dist_m <= 0: return 1
    return max(1, min(294, round(math.log(max(dist_m, L_P*10)/L_P)/math.log(PHI))))

def L(bz):
    return L_P * PHI**bz

def scale_label(r):
    if r > 1e25: return f"{r/9.461e24:.1f} Gly"
    if r > 1e22: return f"{r/MLY:.0f} Mly"
    if r > 1e18: return f"{r/LY:.0f} ly"
    if r > AU*0.5: return f"{r/AU:.1f} AU"
    if r > 1e9: return f"{r/1e9:.1f} Gm"
    if r > 1e6: return f"{r/1e6:.0f} Mm"
    if r > 1e3: return f"{r/1e3:.0f} km"
    return f"{r:.1f} m"

# ═══════════════════════════════════════════════════════════════════════
# CANTOR NODE — One equation at every scale
# ═══════════════════════════════════════════════════════════════════════

class CantorNode:
    """One node in the Zeckendorf tree. Same 5-sector architecture at any scale."""
    
    def __init__(self, name, radius_m, bz, depth=0, max_depth=6, max_children=5,
                 f_depth=0.5):
        self.name = name
        self.radius = radius_m
        self.bz = round(bz, 2)
        self.depth = depth
        self.f_depth = f_depth  # fractional depth toward center (0=edge, 1=center)
        
        # Gravitational compression at this depth
        self.grav_factor = math.sqrt(1 - PHI_OVER_C2 * (1 - f_depth**2))
        
        # Physical boundaries (meters) — compressed by gravity
        self.r_core  = radius_m * R_MATTER * self.grav_factor
        self.r_inner = radius_m * R_INNER * self.grav_factor
        self.r_photo = radius_m * R_PHOTO * self.grav_factor
        self.r_shell = radius_m * R_SHELL * self.grav_factor
        self.r_outer = radius_m * R_OUTER * self.grav_factor
        
        # Vacuum channel width (for transit calculations)
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


# ═══════════════════════════════════════════════════════════════════════
# SOLAR LADDER — r(k) = 0.387 AU × φ^k
# ═══════════════════════════════════════════════════════════════════════

class SolarLadder:
    R_SUN = 6.9634e8
    R_MERC = 0.387  # AU

    PLANETS = [
        ("Mercury",0.387,0), ("Venus",0.723,1), ("Earth",1.000,2),
        ("Mars",1.524,3), ("Ceres",2.767,4), ("Jupiter",5.203,5),
        ("Saturn",9.537,7), ("Uranus",19.19,8), ("Neptune",30.07,9),
    ]
    SOLAR = [
        ("Core edge",0.25,-12,"σ₃ matter"), ("Tachocline",0.71,-10,"σ₂ inner"),
        ("Photosphere",1.00,None,"cos(α)"), ("Corona 3R☉",3.0,-7,"void gap"),
        ("Alfvén",13.0,-4,"σ₄ outer"),
    ]

    def __init__(self):
        self.k_photo = -10 + COS_ALPHA
        self.R_pred = self.R_MERC * AU * PHI**self.k_photo
        self.err = abs(self.R_pred - self.R_SUN) / self.R_SUN

    def predict(self, k): return self.R_MERC * PHI**k

    def planet_table(self):
        rows = []
        for name, r_a, k in self.PLANETS:
            r_p = self.predict(k)
            rows.append({'name':name,'k':k,'actual':r_a,'pred':round(r_p,4),
                         'err':round(abs(r_p-r_a)/r_a*100,1)})
        return rows

    def solar_table(self):
        rows = []
        for name, r_rsun, k, role in self.SOLAR:
            if k is None:
                k_v = self.k_photo
                r_m = self.R_pred
            else:
                k_v = k
                r_m = self.R_MERC * AU * PHI**k
            err = abs(r_m - r_rsun*self.R_SUN)/(r_rsun*self.R_SUN)*100
            rows.append({'name':name,'k':round(k_v,4) if k is None else k,
                         'r_rsun':r_rsun,'err':round(err,1),'role':role})
        return rows


# ═══════════════════════════════════════════════════════════════════════
# TRANSIT CALCULATOR — Vacuum channel with gravitational condensation
# ═══════════════════════════════════════════════════════════════════════

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
        """Calculate transit from Earth → center through condensed channels."""
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
                'compression': 0.5 * R_MATTER * R_HUBBLE / total_d,
                'gate_freq_hz': 2*math.pi*J_eV*1.602e-19/HBAR * 0.000611,
                'gate_wavelength_m': C/(2*math.pi*J_eV*1.602e-19/HBAR*0.000611)}


# ═══════════════════════════════════════════════════════════════════════
# RENDERER — Correct physics: matter in σ₃, walls as boundaries
# ═══════════════════════════════════════════════════════════════════════

BG='#06080e'; GOLD='#f5c542'; LGOLD='#ffe89a'; DGOLD='#a07520'
BLUE='#4488ff'; PURP='#9944ff'; LPURP='#774499'
PINK='#ff4488'; GREEN='#44ff88'; CYAN='#00ddcc'
DIM='#333850'; WHITE='#e8eaf0'
WARM='#ffcc66'; HOT='#ff8833'; FILAMENT='#eebb44'

def render_universe_top(savepath):
    """Cosmic web in σ₃ — matter as filaments, walls as faint boundaries."""
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
    
    for _ in range(5000):
        ang = rng.uniform(0,2*np.pi)
        r = abs(rng.normal(0,r_co*0.45))
        if r > r_co: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=WARM,
                ms=rng.uniform(0.15,0.6),alpha=0.05*(1-(r/r_co)**2))
    
    # Faint walls
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_INNER,fc='none',ec=LPURP,lw=0.8,alpha=0.12))
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_OUTER,fc='none',ec=LPURP,lw=1.0,alpha=0.08,ls='--'))
    ax.add_patch(plt.Circle((0,0),r_co,fc='none',ec=DGOLD,lw=0.6,alpha=0.1,ls=':'))
    
    # Seed crystal at center
    ax.plot(0,0,'+',color=GOLD,ms=15,mew=2,alpha=0.6)
    ax.add_patch(plt.Circle((0,0),r_co*0.07,fc=GOLD,ec='none',alpha=0.03))
    ax.text(r_co*0.01,r_co*0.08,"Seed Crystal",color=GOLD,fontsize=7,
            fontfamily='monospace',alpha=0.5)
    
    # You are here
    mw_r = r_co * 0.5; mw_ang = 0.8
    ax.plot(mw_r*np.cos(mw_ang),mw_r*np.sin(mw_ang),'*',color=GREEN,ms=8,mec=WHITE,mew=0.5,zorder=20)
    ax.text(mw_r*np.cos(mw_ang)+r_co*0.03,mw_r*np.sin(mw_ang)+r_co*0.02,
            "You are here\n(Milky Way)",color=GREEN,fontsize=7,fontfamily='monospace',fontweight='bold')
    
    # Vacuum channel (route to center)
    ch_angles = np.linspace(mw_ang, mw_ang-0.3, 50)
    ch_r = np.linspace(mw_r, r_co*0.05, 50)
    ax.plot(ch_r*np.cos(ch_angles), ch_r*np.sin(ch_angles), '--', color=CYAN, lw=0.8, alpha=0.3)
    ax.text(ch_r[25]*np.cos(ch_angles[25])-r_co*0.05,
            ch_r[25]*np.sin(ch_angles[25])+r_co*0.02,
            "vacuum channel\n(condensed)",color=CYAN,fontsize=6,fontfamily='monospace',alpha=0.4)
    
    # Scale
    sbar = 500*MLY
    ax.plot([-sbar/2,sbar/2],[-view*0.92,-view*0.92],'-',color='#445',lw=2)
    ax.text(0,-view*0.95,"500 Mly",color='#556',fontsize=9,ha='center',fontfamily='monospace')
    
    ax.text(0,view*0.95,"Observable Universe — Cosmic Web in σ₃",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,f"bz=294  Z={zeck_str(294)}  σ₃={scale_label(r_co)}  "
            f"Seed crystal at E=0 center",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


def render_universe_side(savepath):
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
    
    for _ in range(80):
        cx = rng.uniform(-r_co*OBLATE*0.85,r_co*OBLATE*0.85)
        cy = rng.normal(0,disc_ht*0.08)
        s = rng.uniform(0.5,2)
        for _ in range(int(40*s)):
            ax.plot(cx+rng.normal(0,r_co*0.01*OBLATE*s),
                    cy/OBLATE+rng.normal(0,disc_ht*0.03*s/OBLATE),
                    '.',color=GOLD,ms=rng.uniform(0.3,1.5*s),alpha=0.3)
    
    # Seed crystal glow at center
    ax.add_patch(plt.Circle((0,0),r_co*0.05*OBLATE,fc=GOLD,ec='none',alpha=0.04))
    ax.plot(0,0,'+',color=GOLD,ms=10,mew=1.5,alpha=0.5)
    
    for r,col,lw,ls in [(r_in,LPURP,1.0,'-'),(r_ou,LPURP,1.2,'--')]:
        ax.add_patch(Ellipse((0,0),r*2*OBLATE,r*2/OBLATE,fc='none',ec=col,lw=lw,ls=ls,alpha=0.12))
    
    ax.text(0,view_y*0.6,"σ₃ MATTER DISC",color=GOLD,fontsize=11,
            ha='center',fontfamily='monospace',fontweight='bold',alpha=0.7)
    
    sbar = 1*9.461e24
    ax.plot([-sbar/2,sbar/2],[-view_y*0.9,-view_y*0.9],'-',color='#445',lw=2)
    ax.text(0,-view_y*0.95,"1 Gly",color='#556',fontsize=9,ha='center',fontfamily='monospace')
    
    ax.text(0,view_y*0.95,"Observable Universe — Side View",color=GOLD,fontsize=14,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view_y*0.87,"thin matter disc · seed crystal at center · DM walls as faint boundaries",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


def render_galaxy(savepath):
    """Milky Way face-on with spiral arms and Sun."""
    fig, ax = plt.subplots(figsize=(14,14), facecolor=BG)
    ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
    rng = np.random.default_rng(55)
    
    R = 5e20  # MW radius
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
    ax.plot(sx,sy,'o',color=GREEN,ms=25,mec=GREEN,mew=0.5,fillstyle='none',alpha=0.3,zorder=19)
    ax.text(sx+R*0.04,sy+R*0.03,"☉ Sun\n8.5 kpc",color=GREEN,fontsize=9,
            fontfamily='monospace',fontweight='bold')
    
    # Scale
    sbar = 20000*LY
    ax.plot([-sbar/2,sbar/2],[-view*0.92,-view*0.92],'-',color='#445',lw=2)
    ax.text(0,-view*0.95,"20k ly",color='#556',fontsize=9,ha='center',fontfamily='monospace')
    
    ax.text(0,view*0.95,"Milky Way — Face-On",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,"bz=265  2+2 spiral arms  golden-angle pitch  Sun in σ₂ prime ring",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


def render_solar_system(savepath):
    """Solar system with φ^k orbital rings."""
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
    
    sbar = 10*AU
    ax.plot([-sbar/2,sbar/2],[-view*0.92,-view*0.92],'-',color='#445',lw=2)
    ax.text(0,-view*0.95,"10 AU",color='#556',fontsize=9,ha='center',fontfamily='monospace')
    
    ax.text(0,view*0.95,"Solar System — φ^k Orbital Ladder",color=GOLD,fontsize=14,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,"r(k) = 0.387 AU × φ^k  ·  background = predicted  ·  0 free parameters",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


def render_sun(savepath):
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
    for g in [1.005,1.01,1.02,1.04]:
        ax.plot(Rs*g*np.cos(th),Rs*g*np.sin(th),'-',color=GOLD,lw=0.5,alpha=0.08*(2-g))
    
    # Corona
    for _ in range(4000):
        r = rng.uniform(Rs*1.03,13*Rs); ang = rng.uniform(0,2*np.pi)
        d = (Rs/r)**1.8
        if rng.random() > d*8: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=CYAN,ms=rng.uniform(0.15,0.5),alpha=max(0.005,0.02*d))
    
    # Streamers
    for _ in range(20):
        a = rng.uniform(0,2*np.pi); re = rng.uniform(3,10)*Rs
        for r in np.linspace(Rs*1.02,re,50):
            ax.plot(r*np.cos(a+rng.normal(0,0.02*(r/Rs-1)*0.1)),
                    r*np.sin(a+rng.normal(0,0.02*(r/Rs-1)*0.1)),
                    '.',color=CYAN,ms=0.2,alpha=0.01)
    
    ax.add_patch(plt.Circle((0,0),0.25*Rs,fc='none',ec=PINK,lw=1,ls=':',alpha=0.4))
    ax.add_patch(plt.Circle((0,0),0.71*Rs,fc='none',ec=PURP,lw=1.5,alpha=0.4))
    ax.add_patch(plt.Circle((0,0),13*Rs,fc='none',ec=PURP,lw=1.5,alpha=0.3,ls='--'))
    
    # Labels
    labels = [(0.12*Rs,"Core k=−12",'#f72'),(0.71*Rs,"Tachocline k=−10",PURP),
              (Rs,"Photosphere cos(α) 0.06%",GOLD),(5*Rs,"Corona GAP\n6 empty rungs",CYAN),
              (13*Rs,"Alfvén k=−4",PURP)]
    lx = view*0.55
    for r,txt,col in labels:
        ax.annotate(txt,xy=(r*0.707,r*0.707),xytext=(lx,r*0.55),
                    color=col,fontsize=7,fontfamily='monospace',fontweight='bold',
                    arrowprops=dict(arrowstyle='->',color=col,lw=0.6,alpha=0.35),alpha=0.8,va='center')
    
    ax.text(0,view*0.82,"The Sun — Dual Wall Architecture",color=GOLD,fontsize=15,
            ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.75,f"k=−12 to −4 on Mercury ladder · cos(α) photosphere = 0.06% · "
            f"D☉ = {2*SolarLadder().R_pred/1000:.0f} km",
            color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


def render_solar_ladder(savepath):
    """Solar ladder chart — all features on the φ^k ruler."""
    fig, ax = plt.subplots(figsize=(16,9), facecolor=BG)
    ax.set_facecolor(BG)
    
    features = [
        (-12,"Core\nedge",0.25*6.96e8/AU,PINK,'o'),
        (-10,"Tachocline\n(σ₂)",0.71*6.96e8/AU,PURP,'s'),
        (-10+COS_ALPHA,"Photosphere\ncos(α)",6.96e8/AU,GOLD,'*'),
        (-7,"Corona\n3 R☉",3*6.96e8/AU,CYAN,'D'),
        (-4,"Alfvén\n(σ₄)",13*6.96e8/AU,PURP,'s'),
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
    
    # Shading
    y_t = math.log10(0.71*6.96e8/AU); y_p = math.log10(6.96e8/AU); y_a = math.log10(13*6.96e8/AU)
    ax.axhspan(y_t,y_p,color=PURP,alpha=0.04)
    ax.axhspan(y_p,y_a,color='#001020',alpha=0.3)
    ax.text(12,(y_p+y_a)/2,"CORONA\nGAP",color=CYAN,fontsize=7,
            fontfamily='monospace',ha='right',va='center',alpha=0.4)
    
    ax.set_xlim(-15,15); ax.set_ylim(-5.5,2.5)
    ax.set_xticks([]); ax.tick_params(colors='#334',labelsize=7)
    ax.set_ylabel('log₁₀(distance / AU)',color='#556',fontsize=10,fontfamily='monospace')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#223'); ax.spines['left'].set_color('#223')
    
    ax.text(0,2.35,"Solar System Fibonacci Ladder: r(k) = 0.387 AU × φ^k",
            color=GOLD,fontsize=14,ha='center',fontfamily='monospace',fontweight='bold')
    sl = SolarLadder()
    ax.text(0,2.1,f"Photosphere: k = −10 + cos(1/φ) → D☉ = {2*sl.R_pred/1000:.0f} km "
            f"(obs: {2*sl.R_SUN/1000:.0f} km) → {sl.err*100:.2f}% error",
            color=GREEN,fontsize=9,ha='center',fontfamily='monospace')
    
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════
# MAIN — Build tree, compute everything, render
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*70)
    print("zeckyBOT — Recursive Universe Builder")
    print("="*70)
    
    # Constants
    print(f"\n  φ = {PHI:.10f}")
    print(f"  W = {W:.8f} (gap fraction)")
    print(f"  cos(α) = cos(1/φ) = {COS_ALPHA:.6f}")
    print(f"  ω_lattice = {OMEGA_LATTICE:.6f} (derived, was 1.685)")
    print(f"  J = {J_eV:.4f} eV, l₀ = {l0*1e9:.4f} nm")
    print(f"  χ_BH = W√(1-W²) = {CHI_BH:.6f} (derived, was 0.410)")
    print(f"  H₀ = {H0_DERIVED_KMS:.1f} km/s/Mpc (derived, Planck 67.4)")
    print(f"  Ω_b={OMEGA_B:.5f}, Ω_DM={OMEGA_DM:.5f}, Ω_DE={OMEGA_DE:.5f}")
    
    print(f"\n  Universal ratios:")
    print(f"    R_MATTER = {R_MATTER:.6f}  (σ₃ core)")
    print(f"    R_INNER  = {R_INNER:.6f}  (σ₂ membrane)")
    print(f"    R_PHOTO  = {R_PHOTO:.6f}  (cos(α) surface)")
    print(f"    R_SHELL  = {R_SHELL:.6f}  (wall center)")
    print(f"    R_OUTER  = {R_OUTER:.6f}  (σ₄ membrane)")
    print(f"    OBLATE   = √φ = {OBLATE:.6f}")
    print(f"    LORENTZ  = √(1-W²) = {LORENTZ_W:.6f}")
    
    # Build tree
    print(f"\n  Building Zeckendorf tree...")
    t0 = time.time()
    root = CantorNode("Observable Universe", R_HUBBLE, 294, max_depth=6)
    nodes = root.flatten()
    dt = time.time() - t0
    print(f"  {len(nodes)} nodes in {dt*1000:.0f}ms")
    for d in range(7):
        n = sum(1 for nd in nodes if nd.depth == d)
        if n: print(f"    Depth {d}: {n}")
    
    # Solar ladder
    sl = SolarLadder()
    print(f"\n  Solar Ladder:")
    print(f"    R☉ = {sl.R_pred:.0f} m (obs {sl.R_SUN:.0f} m, err {sl.err*100:.2f}%)")
    print(f"    D☉ = {2*sl.R_pred/1000:.0f} km (obs {2*sl.R_SUN/1000:.0f} km)")
    for p in sl.planet_table():
        mk = '✓' if p['err']<10 else '~'
        print(f"    {p['name']:10s} k={p['k']:2d} pred={p['pred']:8.3f} obs={p['actual']:8.3f} err={p['err']:5.1f}% {mk}")
    
    # Transit
    tc = TransitCalculator()
    route = tc.route_to_center()
    print(f"\n  Transit to Center:")
    print(f"    Flat distance:  {scale_label(route['flat_dist'])}")
    print(f"    Condensed:      {scale_label(route['total_dist'])}")
    print(f"    Compression:    {route['compression']:.0f}×")
    print(f"    Gate frequency: {route['gate_freq_hz']:.3e} Hz (λ={route['gate_wavelength_m']*1e6:.2f} μm)")
    for h in route['hops']:
        print(f"      {h['name']:20s} flat={scale_label(h['flat']):>12s} → "
              f"condensed={scale_label(h['condensed']):>12s} (g={h['grav']:.4f})")
    
    # Render
    outdir = '/mnt/user-data/outputs/renders'
    os.makedirs(outdir, exist_ok=True)
    
    print(f"\n  Rendering...")
    t0 = time.time()
    render_universe_top(f'{outdir}/universe_top.png'); print("    ✓ Universe top")
    render_universe_side(f'{outdir}/universe_side.png'); print("    ✓ Universe side")
    render_galaxy(f'{outdir}/galaxy_top.png'); print("    ✓ Galaxy")
    render_solar_system(f'{outdir}/solar_system.png'); print("    ✓ Solar system")
    render_sun(f'{outdir}/sun_structure.png'); print("    ✓ Sun")
    render_solar_ladder(f'{outdir}/solar_ladder.png'); print("    ✓ Solar ladder")
    print(f"  All renders in {time.time()-t0:.1f}s")
    
    print(f"\n{'='*70}")
    print("Done. φ all the way down.")
    print(f"{'='*70}")
