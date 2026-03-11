#!/usr/bin/env python3
"""
zeckyBOT.py — Recursive Universe Builder (Any Metallic Mean)
═══════════════════════════════════════════════════════════════════════════
Husmann Decomposition: One Equation, Every Scale, Every Structure

Thomas A. Husmann / iBuilt LTD — March 2026
Patent Application 19/560,637
Repository: github.com/thusmann5327/Unified_Theory_Physics

═══════════════════════════════════════════════════════════════════════════
HOW TO USE:  Change METAL_N below. That's it. Everything else derives.
═══════════════════════════════════════════════════════════════════════════

METAL_N selects which metallic mean δₙ to use as the vacuum structure.
δₙ is the positive root of x² = nx + 1:

    n=1 → δ₁ = φ = (1+√5)/2 = 1.618034   (the golden ratio)
    n=2 → δ₂ = 1+√2         = 2.414214   (the silver ratio)
    n=3 → δ₃ = (3+√13)/2    = 3.302776   (the bronze ratio)
    ...
    n=k → δₖ = (k+√(k²+4))/2

The AAH Hamiltonian at α = 1/δₙ, V = 2J, D = 233 sites produces a
Cantor-set energy spectrum. From that spectrum, EVERY ratio, constant,
and structure in this file is computed. Same equation builds the
observable universe AND the internal structure of atoms.

═══════════════════════════════════════════════════════════════════════════
METALLIC MEANS PERIODIC CHART
═══════════════════════════════════════════════════════════════════════════

  n │ δₙ        │ α=1/δₙ   │ √δₙ     │ Crystal System        │ Elements
 ───┼───────────┼──────────┼─────────┼───────────────────────┼─────────────────────
  1 │ 1.618034  │ 0.618034 │ 1.27202 │ HCP (hexagonal close) │ Re, Co, Mg, Ti, Zn
  2 │ 2.414214  │ 0.414214 │ 1.55377 │ Rhombohedral          │ Hg, As, Ga, Sb, Bi
  3 │ 3.302776  │ 0.302776 │ 1.81738 │ FCC (face-centered)   │ Cu, Au, Ag, Ni, Pt
  4 │ 4.236068  │ 0.236068 │ 2.05817 │ Hex/Monoclinic        │ Te, Pu, S (mono)
  5 │ 5.192582  │ 0.192582 │ 2.27870 │ DHCP (double hex)     │ Nd, La, Pr, Ce, Am
  6 │ 6.162278  │ 0.162278 │ 2.48243 │ Rhombo/Orthorhombic   │ Bi, U, Ga, I, Br
  7 │ 7.140055  │ 0.140055 │ 2.67211 │ BCC (body-centered)   │ Li, Na, K, Fe, W, Cr
  8 │ 8.123106  │ 0.123106 │ 2.85010 │ Hex chain / Se-type   │ Se, Te (chain form)
 ───┴───────────┴──────────┴─────────┴───────────────────────┴─────────────────────

  You can also enter any FLOAT — non-integer values interpolate between
  metals and produce spectra that don't correspond to known crystal
  classes, but the math still works. Try 1.5, √2, π, e ...

═══════════════════════════════════════════════════════════════════════════
"""

import math, numpy as np, json, time, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║                                                                       ║
# ║   ██  CHANGE THIS VALUE TO SELECT YOUR METALLIC MEAN  ██             ║
# ║                                                                       ║
# ║   1 = Gold (φ, the standard framework)                               ║
# ║   2 = Silver (δ_S = 1+√2)                                           ║
# ║   3 = Bronze (δ_B = (3+√13)/2)                                      ║
# ║   4..8 = Higher metals (see chart above)                             ║
# ║   Any float works: try 1.5, √2, e, π ...                           ║
# ║                                                                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝

METAL_N = 1       # ← THE ONE KNOB. Everything below derives from this.

D = 233           # F(F(7)) = F(13) = 233. The lattice dimension.

# ═══════════════════════════════════════════════════════════════════════
# DERIVED — Everything below is COMPUTED from METAL_N and D
# ═══════════════════════════════════════════════════════════════════════

DELTA = (METAL_N + math.sqrt(METAL_N * METAL_N + 4)) / 2
ALPHA = 1.0 / DELTA
DELTA2, DELTA3, DELTA4 = DELTA**2, DELTA**3, DELTA**4

HBAR = 1.0545718e-34; C = 2.99792458e8; G = 6.67430e-11; K_B = 1.380649e-23
L_P = 1.61625e-35; AU = 1.496e11; LY = 9.461e15; MLY = LY*1e6; KPC = 3.086e19

# ── THE SPECTRUM ──────────────────────────────────────────────────────
print(f"  Computing spectrum for n={METAL_N} (δ={DELTA:.6f}, α=1/δ={ALPHA:.6f})...")
_H = np.diag(2*np.cos(2*np.pi*ALPHA*np.arange(D)))
_H += np.diag(np.ones(D-1), 1) + np.diag(np.ones(D-1), -1)
_eigs = np.sort(np.linalg.eigvalsh(_H))
_E_range = float(_eigs[-1] - _eigs[0])
_diffs = np.diff(_eigs); _med = np.median(_diffs)
_gaps = []
for i in range(len(_diffs)):
    if _diffs[i] > 8*_med:
        _gaps.append({'lo':float(_eigs[i]),'hi':float(_eigs[i+1]),
                      'w':float(_diffs[i]),'c':float((_eigs[i]+_eigs[i+1])/2)})
_ranked = sorted(_gaps, key=lambda g: g['w'], reverse=True)
_big_gaps = [g for g in _ranked if g['w'] > 0.5]
if len(_big_gaps) >= 2:
    _wL = min(_big_gaps[:2], key=lambda g: g['c'])
    _wR = max(_big_gaps[:2], key=lambda g: g['c'])
else:
    _wL = _ranked[0]; _wR = _ranked[1] if len(_ranked)>1 else _ranked[0]
_half = _E_range / 2

OMEGA_LATTICE = max(g['w'] for g in _ranked)
T_BOND = (D-1)*1e-18
J_J = 2*math.pi*HBAR/(OMEGA_LATTICE*T_BOND)
J_eV = J_J/1.602176634e-19
l0 = C*HBAR/(2*J_J)

W = 2/DELTA4 + DELTA**(-1/DELTA)/DELTA3; W2 = W**2; W4 = W**4

R_MATTER = abs(_wL['hi'])/_half
R_INNER = abs(_wL['c'])/_half - _wL['w']/(2*_E_range)
R_SHELL = abs(_wL['c'])/_half
R_OUTER = abs(_wL['c'])/_half + _wL['w']/(2*_E_range)
WALL_FRAC = _wL['w']/_E_range
S3_WIDTH = (_wR['lo']-_wL['hi'])/_E_range
COS_ALPHA = math.cos(ALPHA)
R_PHOTO = R_INNER + COS_ALPHA*(R_SHELL-R_INNER)
OBLATE = math.sqrt(DELTA)
LORENTZ_W = math.sqrt(1-W2); BREATHING = 1-LORENTZ_W
N_BRACKETS = 294
INV_ALPHA_PRED = N_BRACKETS*W; ALPHA_EM_PRED = 1.0/INV_ALPHA_PRED

COMOVING_FACTOR = DELTA2 + 1/DELTA
R_HUBBLE = L_P*DELTA**N_BRACKETS
H0_DERIVED_KMS = C*COMOVING_FACTOR/R_HUBBLE*3.086e22/1000
CHI_BH = W*LORENTZ_W
OMEGA_B = W4; _ds = 1/DELTA+1/DELTA3
OMEGA_DM = (1/DELTA3)*(1-W4)/_ds; OMEGA_DE = (1/DELTA)*(1-W4)/_ds

_s3_gaps = sorted([g for g in _gaps
    if g['lo']>=_wL['hi']-0.001 and g['hi']<=_wR['lo']+0.001],
    key=lambda g: g['w'], reverse=True)
_s3_eigs = _eigs[(_eigs>=_wL['hi'])&(_eigs<=_wR['lo'])]
_center_e = _s3_eigs[np.abs(_s3_eigs)<0.02]
_edge_e = _s3_eigs[np.abs(_s3_eigs)>0.12]
_sp_c = float(np.mean(np.diff(_center_e))) if len(_center_e)>1 else 0.01
_sp_e = float(np.mean(np.diff(_edge_e))) if len(_edge_e)>1 else 0.01
EIGENVALUE_DENSITY_RATIO = _sp_c/_sp_e if _sp_e!=0 else 0.26
INNER_GAP_FRAC = _s3_gaps[0]['w']/_E_range if _s3_gaps else 0.002
PHI_OVER_C2 = W2

# ── FIBONACCI / ZECKENDORF ────────────────────────────────────────────
_fibs = [1,1]
while _fibs[-1]<100000: _fibs.append(_fibs[-1]+_fibs[-2])
def zeckendorf(n):
    n=max(1,int(round(abs(n)))); r,rem=[],n
    for f in reversed(_fibs):
        if f<=rem: r.append(f); rem-=f
        if rem==0: break
    return r or [1]
def zeck_str(n): return '{'+'+'.join(str(x) for x in zeckendorf(n))+'}'
def bracket(dist_m):
    if dist_m<=0: return 1
    return max(1,min(N_BRACKETS,round(math.log(max(dist_m,L_P*10)/L_P)/math.log(DELTA))))
def L(bz): return L_P*DELTA**bz
def scale_label(r):
    if r>1e25: return f"{r/9.461e24:.1f} Gly"
    if r>1e22: return f"{r/MLY:.0f} Mly"
    if r>1e18: return f"{r/LY:.0f} ly"
    if r>AU*0.5: return f"{r/AU:.1f} AU"
    if r>1e9: return f"{r/1e9:.1f} Gm"
    if r>1e6: return f"{r/1e6:.0f} Mm"
    if r>1e3: return f"{r/1e3:.0f} km"
    if r>1e-3: return f"{r:.3f} m"
    if r>1e-9: return f"{r*1e9:.2f} nm"
    if r>1e-15: return f"{r*1e15:.2f} fm"
    return f"{r:.2e} m"

# ── LOOKUP TABLES ─────────────────────────────────────────────────────
METAL_NAMES = {
    1:('Gold φ','HCP','Re,Co,Mg,Ti,Zn'), 2:('Silver δ_S','Rhombohedral','Hg,As,Ga,Sb,Bi'),
    3:('Bronze δ_B','FCC','Cu,Au,Ag,Ni,Pt'), 4:('n=4','Hex/Mono','Te,Pu,S'),
    5:('n=5','DHCP','Nd,La,Pr,Ce,Am'), 6:('n=6','Rhombo/Ortho','Bi,U,Ga,I,Br'),
    7:('n=7','BCC','Li,Na,K,Fe,W,Cr'), 8:('n=8','Hex chain','Se,Te'),
}
METAL_COLORS = {
    1:('#f5c542','#ffe89a','#a07520'), 2:('#aaccee','#ddeeff','#556688'),
    3:('#dd8844','#ffbb77','#885522'), 4:('#44ddaa','#88ffcc','#227755'),
    5:('#dd44aa','#ff88cc','#882266'), 6:('#4488dd','#88bbff','#224488'),
    7:('#88dd44','#bbff88','#447722'), 8:('#dd4444','#ff8888','#882222'),
}
def _get_color():
    n_int=max(1,min(8,round(METAL_N))); return METAL_COLORS.get(n_int,METAL_COLORS[1])
def _get_name():
    n_int=max(1,min(8,round(METAL_N))); return METAL_NAMES.get(n_int,(f'n={METAL_N}','Unknown','—'))

COL, BRIGHT, DIM_COL = _get_color()
METAL_NAME, CRYSTAL, ELEMENTS = _get_name()

# ═══════════════════════════════════════════════════════════════════════
# CANTOR NODE — One equation at every scale (universe → atom)
# ═══════════════════════════════════════════════════════════════════════

class CantorNode:
    def __init__(self, name, radius_m, bz, depth=0, max_depth=6,
                 max_children=5, f_depth=0.5):
        self.name=name; self.radius=radius_m; self.bz=round(bz,2)
        self.depth=depth; self.f_depth=f_depth
        self.grav_factor = math.sqrt(1-PHI_OVER_C2*(1-f_depth**2))
        self.r_core  = radius_m*R_MATTER*self.grav_factor
        self.r_inner = radius_m*R_INNER*self.grav_factor
        self.r_photo = radius_m*R_PHOTO*self.grav_factor
        self.r_shell = radius_m*R_SHELL*self.grav_factor
        self.r_outer = radius_m*R_OUTER*self.grav_factor
        self.channel_width = radius_m*INNER_GAP_FRAC*self.grav_factor*EIGENVALUE_DENSITY_RATIO
        self.children = []
        if depth < max_depth:
            n_ch = min(max_children, len(_s3_gaps))
            for i in range(n_ch):
                child_frac = _s3_gaps[i]['w']/_E_range
                child_R = radius_m*child_frac*2.5
                child_bz = bz-math.log(max(radius_m/max(child_R,1),1))/math.log(DELTA)
                child_f = f_depth+(1-f_depth)*0.15*(i+1)/n_ch
                self.children.append(CantorNode(
                    self._name_scale(child_R,i), child_R, child_bz,
                    depth+1, max_depth, max_children, child_f))

    def _name_scale(self,r,idx):
        if r>1e25: return f"Supercluster {idx}"
        if r>1e23: return f"Galaxy cluster {idx}"
        if r>1e20: return f"Galaxy {idx}"
        if r>1e18: return f"Nebula {idx}"
        if r>1e15: return f"Stellar system {idx}"
        if r>1e12: return f"Planetary orbit {idx}"
        if r>1e9: return f"Star {idx}"
        if r>1e6: return f"Planet {idx}"
        if r>1e3: return f"Macro {idx}"
        if r>1e-3: return f"Meso {idx}"
        if r>1e-7: return f"Micro {idx}"
        if r>1e-10: return f"Molecular {idx}"
        if r>1e-13: return f"Atomic {idx}"
        if r>1e-16: return f"Nuclear {idx}"
        return f"Sub-nuclear {idx}"

    def flatten(self):
        result=[self]
        for c in self.children: result.extend(c.flatten())
        return result
    def to_dict(self):
        return {'name':self.name,'radius':self.radius,'bz':self.bz,
                'depth':self.depth,'grav':round(self.grav_factor,4),
                'r_core':self.r_core,'r_inner':self.r_inner,
                'r_shell':self.r_shell,'r_outer':self.r_outer,
                'zeckendorf':zeckendorf(max(1,int(self.bz))),
                'n_children':len(self.children)}
    def __repr__(self):
        return (f"{'  '*self.depth}[bz={self.bz:.0f} g={self.grav_factor:.3f}] "
                f"{self.name} R={scale_label(self.radius)} ({len(self.children)} ch)")

# ═══════════════════════════════════════════════════════════════════════
# SOLAR LADDER — r(k) = 0.387 AU × δ^k
# ═══════════════════════════════════════════════════════════════════════

class SolarLadder:
    R_SUN=6.9634e8; R_MERC=0.387
    PLANETS=[("Mercury",0.387,0),("Venus",0.723,1),("Earth",1.000,2),
             ("Mars",1.524,3),("Ceres",2.767,4),("Jupiter",5.203,5),
             ("Saturn",9.537,7),("Uranus",19.19,8),("Neptune",30.07,9)]
    SOLAR=[("Core edge",0.25,-12,"σ₃"),("Tachocline",0.71,-10,"σ₂"),
           ("Photosphere",1.00,None,"cos(α)"),("Corona 3R",3.0,-7,"gap"),
           ("Alfvén",13.0,-4,"σ₄")]
    def __init__(self):
        self.k_photo=-10+COS_ALPHA
        self.R_pred=self.R_MERC*AU*DELTA**self.k_photo
        self.D_pred=2*self.R_pred
        self.err=abs(self.R_pred-self.R_SUN)/self.R_SUN
    def predict(self,k): return self.R_MERC*DELTA**k
    def planet_table(self):
        rows=[]
        for name,r_a,k in self.PLANETS:
            r_p=self.predict(k)
            rows.append({'name':name,'k':k,'actual':r_a,'pred':round(r_p,4),
                         'err':round(abs(r_p-r_a)/r_a*100,1)})
        return rows

# ═══════════════════════════════════════════════════════════════════════
# TRANSIT CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

class TransitCalculator:
    V_G=0.4996*C
    ROUTE_LEVELS=[("Universe",294,0.95),("Supercluster",281,0.75),
        ("Galaxy cluster",269,0.50),("Galaxy",256,0.30),
        ("Stellar system",243,0.15),("Planetary orbit",230,0.05)]
    def route_to_center(self):
        hops=[]
        for name,bz,f_depth in self.ROUTE_LEVELS:
            sigma3=L_P*DELTA**bz*R_MATTER
            gap_flat=sigma3*INNER_GAP_FRAC
            grav=math.sqrt(1-PHI_OVER_C2*(1-f_depth**2))
            condensed=gap_flat*grav*EIGENVALUE_DENSITY_RATIO
            t=condensed/self.V_G
            hops.append({'name':name,'bz':bz,'flat':gap_flat,
                         'condensed':condensed,'grav':grav,'time_s':t})
        total_d=sum(h['condensed'] for h in hops)
        return {'hops':hops,'total_dist':total_d,'total_time_s':total_d/self.V_G,
                'flat_dist':0.5*R_MATTER*R_HUBBLE,
                'compression':0.5*R_MATTER*R_HUBBLE/total_d if total_d>0 else 0,
                'gate_freq_hz':2*math.pi*J_eV*1.602e-19/HBAR*0.000611,
                'gate_wavelength_m':C/(2*math.pi*J_eV*1.602e-19/HBAR*0.000611) if J_eV>0 else 0}

# ═══════════════════════════════════════════════════════════════════════
# SPECTRUM UTILITIES
# ═══════════════════════════════════════════════════════════════════════

def find_bands_gaps(eigs, threshold=8.0):
    diffs=np.diff(eigs); med=np.median(diffs); gaps=[]; bands=[]; bs=0
    for i in range(len(diffs)):
        if diffs[i]>threshold*med:
            gaps.append(dict(lo=float(eigs[i]),hi=float(eigs[i+1]),
                w=float(diffs[i]),c=float((eigs[i]+eigs[i+1])/2)))
            bands.append(dict(lo=float(eigs[bs]),hi=float(eigs[i]),
                w=float(eigs[i]-eigs[bs]),n=i-bs+1)); bs=i+1
    bands.append(dict(lo=float(eigs[bs]),hi=float(eigs[-1]),
        w=float(eigs[-1]-eigs[bs]),n=len(eigs)-bs))
    return bands,gaps

# ═══════════════════════════════════════════════════════════════════════
# RENDERERS
# ═══════════════════════════════════════════════════════════════════════

BG='#06080e'; PURP='#9944ff'; LPURP='#774499'
PINK='#ff4488'; GREEN='#44ff88'; CYAN='#00ddcc'
BLUE='#4488ff'; DIM='#333850'; WHITE='#e8eaf0'
WARM='#ffcc66'; HOT='#ff8833'; FILAMENT='#eebb44'; LGOLD='#ffe89a'

def render_cantor_spectrum(savepath):
    fig,axes=plt.subplots(3,1,figsize=(14,4.5),facecolor=BG,
        gridspec_kw={'height_ratios':[1,1,1],'hspace':0.35})
    for ax_i,(N_s,label) in enumerate([(5,'N=5 seed'),(55,'N=55'),(D,f'N={D} ({len(_gaps)} gaps)')]):
        ax=axes[ax_i]; ax.set_facecolor(BG)
        H=np.diag(2*np.cos(2*np.pi*ALPHA*np.arange(N_s)))
        H+=np.diag(np.ones(N_s-1),1)+np.diag(np.ones(N_s-1),-1)
        eigs=np.sort(np.linalg.eigvalsh(H))
        bands,gaps=find_bands_gaps(eigs) if N_s>5 else ([],[])
        Em,Ex=float(eigs[0]),float(eigs[-1]); Er=Ex-Em if Ex>Em else 1
        ax.barh(0,1,height=1,left=0,color='#0d0e18',edgecolor='none')
        if bands:
            for b in bands:
                x0=(b['lo']-Em)/Er; xw=b['w']/Er
                if xw>0: ax.barh(0,xw,height=1,left=x0,color=COL,alpha=0.9)
            for g in gaps:
                x0=(g['lo']-Em)/Er; xw=g['w']/Er
                ax.barh(0,xw,height=1,left=x0,color='#1a0833',alpha=0.85)
        else:
            for e in eigs:
                x=(e-Em)/Er if Er>0 else 0.5
                ax.plot(x,0.5,'|',color=COL,markersize=15,markeredgewidth=2)
        ax.set_xlim(0,1);ax.set_ylim(0,1);ax.set_yticks([]);ax.set_xticks([])
        ax.set_title(label,color='#aaa',fontsize=10,fontfamily='monospace',pad=3,loc='left')
    fig.suptitle(f'n={METAL_N}: {METAL_NAME} — Cantor Spectrum (α=1/{DELTA:.4f})',
        color=BRIGHT,fontsize=13,fontweight='bold',fontfamily='monospace',y=0.98)
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)

def render_evolved_equilibrium(savepath,elev=22,azim=38,view_label='Primary'):
    fig=plt.figure(figsize=(10,10),facecolor=BG)
    ax=fig.add_subplot(111,projection='3d',facecolor=BG)
    ax.view_init(elev=elev,azim=azim); rng=np.random.default_rng(42)
    u=np.linspace(0,2*np.pi,30);v=np.linspace(0,np.pi,20)
    for r_s,col_w,a,lw in [(R_OUTER,PURP,0.15,0.3),(R_INNER,PURP,0.25,0.4),(R_PHOTO,COL,0.2,0.5)]:
        x=r_s*OBLATE*np.outer(np.cos(u),np.sin(v))
        y=r_s*OBLATE*np.outer(np.sin(u),np.sin(v))
        z=r_s/OBLATE*np.outer(np.ones(np.size(u)),np.cos(v))
        ax.plot_wireframe(x,y,z,color=col_w,alpha=a,linewidth=lw)
    for _ in range(400):
        th=rng.uniform(0,2*np.pi);pa=rng.uniform(0,np.pi);rd=rng.uniform(R_INNER,R_OUTER)
        ax.scatter([rd*OBLATE*np.sin(pa)*np.cos(th)],[rd*OBLATE*np.sin(pa)*np.sin(th)],
            [rd/OBLATE*np.cos(pa)],c=PURP,s=2,alpha=0.08)
    rp=R_PHOTO;sig=R_PHOTO*0.05
    for _ in range(600):
        th=rng.uniform(0,2*np.pi);pa=np.clip(rng.normal(np.pi/2,0.3),0.1,np.pi-0.1)
        rm=rng.normal(rp,sig)
        if rm<R_INNER or rm>R_OUTER: continue
        b=np.exp(-abs(rm-rp)/sig)
        ax.scatter([rm*OBLATE*np.sin(pa)*np.cos(th)],[rm*OBLATE*np.sin(pa)*np.sin(th)],
            [rm/OBLATE*np.cos(pa)],c=COL,s=8*b+2,alpha=0.4*b+0.1)
    for _ in range(200):
        th=rng.uniform(0,2*np.pi);pa=rng.uniform(0,np.pi);rc=rng.exponential(R_MATTER*0.3)
        if rc>R_MATTER: continue
        ax.scatter([rc*np.sin(pa)*np.cos(th)],[rc*np.sin(pa)*np.sin(th)],
            [rc*np.cos(pa)],c=PINK,s=6,alpha=0.5)
    ax.scatter([0],[0],[0],c='white',s=100,edgecolors=COL,linewidth=2,zorder=10)
    lim=R_OUTER*OBLATE*0.6
    ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_zlim(-lim/OBLATE,lim/OBLATE)
    for p in [ax.xaxis.pane,ax.yaxis.pane,ax.zaxis.pane]: p.fill=False;p.set_edgecolor('#1a1a2a')
    ax.tick_params(colors='#333',labelsize=6);ax.grid(True,alpha=0.06)
    ax.set_title(f'n={METAL_N} {view_label}: {METAL_NAME}\ncos(1/δ)={COS_ALPHA:.4f}  oblate=√δ={OBLATE:.4f}  σ₃={R_MATTER:.4f}',
        color=BRIGHT,fontsize=13,fontfamily='monospace',pad=20)
    fig.savefig(savepath,dpi=140,facecolor=BG,bbox_inches='tight',pad_inches=0.15)
    plt.close(fig)

def render_universe_top(savepath):
    fig,ax=plt.subplots(figsize=(14,14),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off')
    rng=np.random.default_rng(42);r_co=R_HUBBLE*R_MATTER;view=r_co*1.15
    ax.set_xlim(-view,view);ax.set_ylim(-view,view)
    n_nodes=200
    nx=np.concatenate([rng.normal(0,r_co*0.3,n_nodes//2),rng.uniform(-r_co*0.9,r_co*0.9,n_nodes//2)])
    ny=np.concatenate([rng.normal(0,r_co*0.3,n_nodes//2),rng.uniform(-r_co*0.9,r_co*0.9,n_nodes//2)])
    mask=np.sqrt(nx**2+ny**2)<r_co*0.95;nx,ny=nx[mask],ny[mask]
    for i in range(len(nx)):
        d=np.sqrt((nx-nx[i])**2+(ny-ny[i])**2)
        for j in np.argsort(d)[1:4]:
            if d[j]>r_co*0.25: continue
            t=np.linspace(0,1,40);mx=(nx[i]+nx[j])/2+rng.normal(0,r_co*0.015);my=(ny[i]+ny[j])/2+rng.normal(0,r_co*0.015)
            fx=nx[i]*(1-t)**2+2*mx*t*(1-t)+nx[j]*t**2;fy=ny[i]*(1-t)**2+2*my*t*(1-t)+ny[j]*t**2
            ax.plot(fx,fy,'-',color=COL,lw=0.4,alpha=0.12)
            for k in range(0,len(t),3):
                ax.plot(fx[k]+rng.normal(0,r_co*0.003),fy[k]+rng.normal(0,r_co*0.003),'.',color=BRIGHT,ms=rng.uniform(0.3,1.8),alpha=0.35)
    for i in range(len(nx)):
        size=rng.uniform(0.5,2.0)
        for _ in range(int(40*size)):
            ax.plot(nx[i]+rng.normal(0,r_co*0.008*size),ny[i]+rng.normal(0,r_co*0.008*size),
                '.',color=BRIGHT if rng.random()>0.3 else COL,ms=rng.uniform(0.3,1.5*size),alpha=rng.uniform(0.15,0.5))
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_INNER,fc='none',ec=LPURP,lw=0.8,alpha=0.12))
    ax.add_patch(plt.Circle((0,0),R_HUBBLE*R_OUTER,fc='none',ec=LPURP,lw=1.0,alpha=0.08,ls='--'))
    ax.plot(0,0,'+',color=COL,ms=15,mew=2,alpha=0.6)
    mw_r=r_co*0.5;mw_ang=0.8
    ax.plot(mw_r*np.cos(mw_ang),mw_r*np.sin(mw_ang),'*',color=GREEN,ms=8,mec=WHITE,mew=0.5,zorder=20)
    ax.text(mw_r*np.cos(mw_ang)+r_co*0.03,mw_r*np.sin(mw_ang)+r_co*0.02,"You are here",color=GREEN,fontsize=7,fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.95,f"Observable Universe — n={METAL_N} {METAL_NAME}",color=COL,fontsize=15,ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.89,f"bz={N_BRACKETS}  σ₃={R_MATTER:.4f}  oblate=√δ={OBLATE:.4f}",color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15);plt.close(fig)

def render_solar_system(savepath):
    fig,ax=plt.subplots(figsize=(14,14),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off')
    view=42*AU;ax.set_xlim(-view,view);ax.set_ylim(-view,view)
    planets=[("Mercury",0.387,'#aaa',2.5,0.3),("Venus",0.723,'#ddc',3.5,0.8),("Earth",1.0,GREEN,4,1.2),
        ("Mars",1.524,'#d62',3,1.8),("Jupiter",5.203,'#c84',7,2.5),("Saturn",9.537,'#db6',6,3.2),
        ("Uranus",19.19,CYAN,4.5,4),("Neptune",30.07,BLUE,4.5,5.1)]
    for k in range(-1,11):
        r=0.387*DELTA**k*AU
        if r<view: ax.add_patch(plt.Circle((0,0),r,fc='none',ec='#0c1020',lw=0.6,alpha=0.5))
    ax.add_patch(plt.Circle((0,0),0.15*AU,fc=COL,ec=BRIGHT,lw=1.5,alpha=0.9))
    for name,r_au,col_p,ms,ang in planets:
        r=r_au*AU;ax.add_patch(plt.Circle((0,0),r,fc='none',ec=col_p,lw=0.5,alpha=0.15))
        px,py=r*np.cos(ang+0.5),r*np.sin(ang+0.5)
        ax.plot(px,py,'o',color=col_p,ms=ms,mec=WHITE,mew=0.4,zorder=10)
        k=round(math.log(r_au/0.387)/math.log(DELTA));pred=0.387*DELTA**k
        err=abs(pred-r_au)/r_au*100
        ax.text(px+AU*np.cos(ang+0.65),py+AU*np.sin(ang+0.65),f"{name}\nk={k} ({err:.0f}%)",color=col_p,fontsize=6.5,fontfamily='monospace',fontweight='bold',ha='center')
    ax.text(0,view*0.95,f"Solar System — δ_{METAL_N}^k Ladder",color=COL,fontsize=14,ha='center',fontfamily='monospace',fontweight='bold')
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15);plt.close(fig)

def render_sun(savepath):
    fig,ax=plt.subplots(figsize=(14,12),facecolor=BG);ax.set_facecolor(BG);ax.set_aspect('equal');ax.axis('off')
    rng=np.random.default_rng(33);Rs=6.96e8;view=16*Rs
    ax.set_xlim(-view,view);ax.set_ylim(-view*0.85,view*0.85)
    for _ in range(8000):
        r=rng.exponential(0.08*Rs)
        if r>0.25*Rs: continue
        ang=rng.uniform(0,2*np.pi);b=1-r/(0.25*Rs)
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color='#fa3' if b>0.5 else '#f72' if b>0.2 else '#c41',ms=rng.uniform(0.3,1.8)*b+0.2,alpha=0.15+0.5*b)
    for _ in range(6000):
        r=rng.uniform(0.25*Rs,0.71*Rs);ang=rng.uniform(0,2*np.pi);d=0.4*(1-(r-0.25*Rs)/(0.46*Rs))
        if rng.random()>d: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=WARM,ms=0.3+d,alpha=0.04+0.1*d)
    th=np.linspace(0,2*np.pi,800);ax.plot(Rs*np.cos(th),Rs*np.sin(th),'-',color=COL,lw=3,alpha=0.9)
    for _ in range(4000):
        r=rng.uniform(Rs*1.03,13*Rs);ang=rng.uniform(0,2*np.pi);d=(Rs/r)**1.8
        if rng.random()>d*8: continue
        ax.plot(r*np.cos(ang),r*np.sin(ang),'.',color=CYAN,ms=rng.uniform(0.15,0.5),alpha=max(0.005,0.02*d))
    ax.add_patch(plt.Circle((0,0),0.25*Rs,fc='none',ec=PINK,lw=1,ls=':',alpha=0.4))
    ax.add_patch(plt.Circle((0,0),0.71*Rs,fc='none',ec=PURP,lw=1.5,alpha=0.4))
    ax.add_patch(plt.Circle((0,0),13*Rs,fc='none',ec=PURP,lw=1.5,alpha=0.3,ls='--'))
    sl=SolarLadder()
    ax.text(0,view*0.82,f"The Sun — n={METAL_N} {METAL_NAME}",color=COL,fontsize=15,ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,view*0.75,f"cos(α)={COS_ALPHA:.4f}  D☉={sl.D_pred/1000:.0f}km  err={sl.err*100:.2f}%",color=DIM,fontsize=8,ha='center',fontfamily='monospace')
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15);plt.close(fig)

def render_solar_ladder(savepath):
    fig,ax=plt.subplots(figsize=(16,9),facecolor=BG);ax.set_facecolor(BG)
    features=[(-12,"Core",0.25*6.96e8/AU,PINK,'o'),(-10,"Tachocline",0.71*6.96e8/AU,PURP,'s'),
        (-10+COS_ALPHA,"Photosphere",6.96e8/AU,COL,'*'),(-7,"Corona",3*6.96e8/AU,CYAN,'D'),
        (-4,"Alfvén",13*6.96e8/AU,PURP,'s'),(0,"Mercury",0.387,'#aaa','o'),
        (2,"Earth",1.000,GREEN,'o'),(3,"Mars",1.524,'#d62','o'),(5,"Jupiter",5.203,'#c84','o'),
        (8,"Uranus",19.19,CYAN,'o'),(9,"Neptune",30.07,BLUE,'o')]
    for k in range(-14,12):
        r=0.387*DELTA**k;ax.axhline(math.log10(r),color='#111825',lw=0.5,alpha=0.5)
    for k,name,obs,col_f,mk in features:
        pred=0.387*DELTA**k;err=abs(pred-obs)/obs*100;xpos=hash(name)%15-5
        ax.plot([xpos],[math.log10(obs)],mk,color=col_f,ms=12,mec=WHITE,mew=0.5,zorder=10)
        lx=xpos+(2 if xpos<3 else -2);ha='left' if xpos<3 else 'right'
        ax.text(lx,math.log10(obs),f"{name}\n{err:.1f}%",color=col_f,fontsize=7,fontfamily='monospace',ha=ha,va='center',fontweight='bold',bbox=dict(boxstyle='round,pad=0.3',fc=BG,ec=col_f,alpha=0.8,lw=0.5))
    ax.set_xlim(-15,15);ax.set_ylim(-5.5,2.5);ax.set_xticks([])
    ax.tick_params(colors='#334',labelsize=7);ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
    sl=SolarLadder()
    ax.text(0,2.35,f"Solar Ladder: r(k) = 0.387 AU × {DELTA:.4f}^k  (n={METAL_N})",color=COL,fontsize=14,ha='center',fontfamily='monospace',fontweight='bold')
    ax.text(0,2.1,f"D☉ = {sl.D_pred/1000:.0f} km (obs: {2*sl.R_SUN/1000:.0f} km) → {sl.err*100:.2f}% error",color=GREEN,fontsize=9,ha='center',fontfamily='monospace')
    fig.savefig(savepath,dpi=200,facecolor=BG,bbox_inches='tight',pad_inches=0.15);plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*70)
    print(f"zeckyBOT — Recursive Universe Builder")
    print(f"  n = {METAL_N}   δ = {DELTA:.10f}   α = 1/δ = {ALPHA:.10f}")
    if round(METAL_N) in METAL_NAMES:
        nm,cr,el=METAL_NAMES[round(METAL_N)]
        print(f"  {nm}  ({cr})  Elements: {el}")
    print("="*70)
    print(f"\n  DERIVED (all from δ_{METAL_N} and D={D}):")
    print(f"    W={W:.8f}  cos(α)={COS_ALPHA:.6f}  ω={OMEGA_LATTICE:.6f}")
    print(f"    J={J_eV:.4f} eV   l₀={l0*1e9:.4f} nm   oblate=√δ={OBLATE:.6f}")
    print(f"    1/α_em = N×W = {INV_ALPHA_PRED:.3f}   H₀={H0_DERIVED_KMS:.1f} km/s/Mpc")
    print(f"    Ω_b={OMEGA_B:.5f}  Ω_DM={OMEGA_DM:.5f}  Ω_DE={OMEGA_DE:.5f}")
    print(f"\n  RATIOS (from {D}-site eigensolver):")
    print(f"    σ₃={R_MATTER:.6f}  σ₂={R_INNER:.6f}  shell={R_SHELL:.6f}  σ₄={R_OUTER:.6f}")
    print(f"    wall={WALL_FRAC:.6f}  S3_w={S3_WIDTH:.6f}  {len(_gaps)} gaps, {len(_s3_gaps)} sub-gaps")

    print(f"\n  Building tree...")
    t0=time.time()
    root=CantorNode("Observable Universe",R_HUBBLE,N_BRACKETS,max_depth=6)
    nodes=root.flatten();dt=time.time()-t0
    print(f"  {len(nodes):,} nodes in {dt*1000:.0f}ms")
    for d in range(7):
        n=sum(1 for nd in nodes if nd.depth==d)
        if n: print(f"    Depth {d}: {n:,}")

    sl=SolarLadder()
    print(f"\n  Solar: D☉={sl.D_pred/1000:.0f}km (obs {2*sl.R_SUN/1000:.0f}km) err={sl.err*100:.2f}%")
    for p in sl.planet_table():
        mk='✓' if p['err']<10 else '~' if p['err']<50 else '✗'
        print(f"    {p['name']:10s} k={p['k']:2d} pred={p['pred']:8.3f} obs={p['actual']:8.3f} err={p['err']:5.1f}% {mk}")

    tc=TransitCalculator();route=tc.route_to_center()
    print(f"\n  Transit: {route['compression']:.0f}× compression  gate λ={route['gate_wavelength_m']*1e6:.2f}μm")

    outdir='/mnt/user-data/outputs/renders';os.makedirs(outdir,exist_ok=True)
    nt=f"n{METAL_N}" if isinstance(METAL_N,int) else f"n{METAL_N:.2f}"
    print(f"\n  Rendering (n={METAL_N})...")
    t0=time.time()
    render_cantor_spectrum(f'{outdir}/{nt}_cantor.png');print("    ✓ Cantor spectrum")
    render_evolved_equilibrium(f'{outdir}/{nt}_eq_main.png',22,38,'Primary');print("    ✓ Equilibrium")
    render_evolved_equilibrium(f'{outdir}/{nt}_eq_top.png',85,0,'Top');print("    ✓ Equilibrium top")
    render_evolved_equilibrium(f'{outdir}/{nt}_eq_side.png',0,90,'Side');print("    ✓ Equilibrium side")
    render_universe_top(f'{outdir}/{nt}_universe.png');print("    ✓ Universe")
    render_solar_system(f'{outdir}/{nt}_solar_sys.png');print("    ✓ Solar system")
    render_sun(f'{outdir}/{nt}_sun.png');print("    ✓ Sun")
    render_solar_ladder(f'{outdir}/{nt}_ladder.png');print("    ✓ Solar ladder")
    print(f"  All renders in {time.time()-t0:.1f}s")

    print(f"\n  ALL 8 METALS COMPARISON:")
    print(f"  {'n':>3s} {'δₙ':>10s} {'W':>10s} {'σ₃%':>8s} {'Ω_b':>10s} {'Ω_DM':>10s} {'Ω_DE':>10s} {'1/α':>10s} {'D☉ err':>8s}")
    print(f"  {'─'*3} {'─'*10} {'─'*10} {'─'*8} {'─'*10} {'─'*10} {'─'*10} {'─'*10} {'─'*8}")
    for tn in range(1,9):
        m=(tn+math.sqrt(tn*tn+4))/2;a=1.0/m
        Ht=np.diag(2*np.cos(2*np.pi*a*np.arange(D)));Ht+=np.diag(np.ones(D-1),1)+np.diag(np.ones(D-1),-1)
        et=np.sort(np.linalg.eigvalsh(Ht));Ert=float(et[-1]-et[0]);dt2=np.diff(et)
        bg=[{'lo':float(et[i]),'hi':float(et[i+1]),'w':float(dt2[i])} for i in range(len(dt2)) if dt2[i]>0.5]
        s3t=abs(min(bg[:2],key=lambda g:(g['lo']+g['hi'])/2)['hi'])/(Ert/2) if len(bg)>=2 else 0
        Wt=2/m**4+m**(-1/m)/m**3;Obt=Wt**4;ds=1/m+1/m**3
        Odmt=(1/m**3)*(1-Wt**4)/ds;Odet=(1/m)*(1-Wt**4)/ds;iat=294*Wt
        kp=-10+math.cos(a);Rp=0.387*AU*m**kp;se=abs(Rp-6.9634e8)/6.9634e8*100
        mk=' ◄' if tn==round(METAL_N) else ''
        print(f"  {tn:3d} {m:10.6f} {Wt:10.6f} {s3t*100:7.2f}% {Obt:10.5f} {Odmt:10.5f} {Odet:10.5f} {iat:10.3f} {se:7.2f}%{mk}")

    print(f"\n{'='*70}")
    print(f"δ_{METAL_N} = {DELTA:.10f}. Same equation, every scale.")
    print(f"{'='*70}")
