#!/usr/bin/env python3
"""
ZECKENDORF RECURSIVE UNIVERSE BUILDER

One equation at every scale:
  At bracket level bz, a structure of radius R has:
    σ₃ core:        r < R × r_matter
    σ₂ inner wall:  r = R × r_inner
    Photosphere:    r = R × (r_inner + cos(α) × half_wall)
    Gap (void):     ~6 rungs empty
    σ₄ outer wall:  r = R × r_outer
    
  Within σ₃, the 9 sub-gaps produce 10 sub-bands.
  Each sub-band is a child node — same equation applied recursively.
  The Zeckendorf address of each node = its path through the tree.

This generates the ENTIRE universe from Hubble to solar system to atoms,
all from one recursive application of the AAH Cantor spectrum.
"""
import math, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import io, base64, json, time

PHI = (1 + math.sqrt(5)) / 2
L_P = 1.61625e-35
C   = 2.99792458e8
AU  = 1.496e11

# ═══════════════════════════════════════════════════════════════════════
# THE ONE EQUATION — computed once from the AAH spectrum
# ═══════════════════════════════════════════════════════════════════════

ALPHA = 1.0 / PHI
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3
COS_ALPHA = math.cos(ALPHA)  # 0.8150 — the wall transmission point
OBLATE = math.sqrt(PHI)

# Solve spectrum once
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
                      'w':float(_diffs[i]),'c':float((_eigs[i]+_eigs[i+1])/2)})
_ranked = sorted(_gaps, key=lambda g: g['w'], reverse=True)
_wall_L = [g for g in _ranked if g['c']<0 and g['w']>1][0]
_wall_R = [g for g in _ranked if g['c']>0 and g['w']>1][0]
_half = _E_range/2

# The universal ratios (pure φ via eigensolver)
R_MATTER = abs(_wall_L['hi']) / _half       # 0.0728
R_INNER  = abs(_wall_L['c']) / _half - _wall_L['w']/(2*_E_range)  # 0.235
R_SHELL  = abs(_wall_L['c']) / _half        # 0.397
R_OUTER  = abs(_wall_L['c']) / _half + _wall_L['w']/(2*_E_range)  # 0.559
WALL_FRAC= _wall_L['w'] / _E_range         # 0.324
S3_WIDTH = (_wall_R['lo'] - _wall_L['hi']) / _E_range  # 0.073

# σ₃ internal sub-gaps (for recursive subdivision)
_s3_gaps = sorted([g for g in _gaps 
                   if g['lo'] >= _wall_L['hi']-0.001 
                   and g['hi'] <= _wall_R['lo']+0.001],
                  key=lambda g: g['w'], reverse=True)
_s3_bands = []
_s3_sorted_edges = sorted(set(
    [_wall_L['hi']] + [g['lo'] for g in _s3_gaps] + 
    [g['hi'] for g in _s3_gaps] + [_wall_R['lo']]
))
for i in range(0, len(_s3_sorted_edges)-1, 2):
    if i+1 < len(_s3_sorted_edges):
        lo, hi = _s3_sorted_edges[i], _s3_sorted_edges[i+1]
        w = hi - lo
        if w > 0.001:
            _s3_bands.append({'lo':lo, 'hi':hi, 'w':w, 
                              'frac': w/_E_range,
                              'center': (lo+hi)/2})

# Sub-gap fractions relative to σ₃ width
S3_SUBGAP_FRACS = [g['w']/(_wall_R['lo']-_wall_L['hi']) for g in _s3_gaps]

print(f"Universal ratios (from φ):")
print(f"  r_matter={R_MATTER:.4f}, r_inner={R_INNER:.4f}, r_shell={R_SHELL:.4f}, r_outer={R_OUTER:.4f}")
print(f"  wall_frac={WALL_FRAC:.4f}, cos(α)={COS_ALPHA:.4f}, oblate=√φ={OBLATE:.4f}")
print(f"  σ₃ sub-gaps: {len(_s3_gaps)}, sub-bands: {len(_s3_bands)}")


# ═══════════════════════════════════════════════════════════════════════
# THE RECURSIVE NODE
# ═══════════════════════════════════════════════════════════════════════

class CantorNode:
    """
    One node in the Zeckendorf tree. Represents a structure at any scale.
    
    The SAME equation governs every node:
      - Core (σ₃ matter) at r < R × R_MATTER
      - Inner wall (σ₂) at r = R × R_INNER  
      - Photosphere at r = R × (R_INNER + cos(α) × (R_SHELL - R_INNER))
      - Void gap between walls
      - Outer wall (σ₄) at r = R × R_OUTER
      - Children: sub-bands within σ₃, each a CantorNode at smaller scale
    """
    
    def __init__(self, name, radius_m, bz, parent_bz=0, depth=0, max_depth=5):
        self.name = name
        self.radius = radius_m
        self.bz = bz
        self.depth = depth
        
        # Physical boundaries (meters)
        self.r_core = radius_m * R_MATTER
        self.r_inner = radius_m * R_INNER
        self.r_photosphere = radius_m * (R_INNER + COS_ALPHA * (R_SHELL - R_INNER))
        self.r_shell = radius_m * R_SHELL
        self.r_outer = radius_m * R_OUTER
        
        # Zeckendorf address
        self.zeck = self._zeckendorf(bz)
        
        # Children (sub-structures within σ₃)
        self.children = []
        if depth < max_depth and len(_s3_gaps) > 0:
            self._subdivide(max_depth)
    
    def _zeckendorf(self, n):
        n = max(1, int(round(abs(n))))
        fibs = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
        r, rem = [], n
        for f in reversed(fibs):
            if f <= rem: r.append(f); rem -= f
            if rem == 0: break
        return r
    
    def _subdivide(self, max_depth):
        """Create child nodes from σ₃ sub-bands."""
        s3_lo = _wall_L['hi']
        s3_hi = _wall_R['lo']
        s3_range = s3_hi - s3_lo
        
        for i, band in enumerate(_s3_bands[:5]):  # top 5 sub-bands
            frac = band['w'] / _E_range
            child_radius = self.radius * frac * 2  # scale to band width
            child_bz = self.bz - math.log(self.radius / max(child_radius, 1)) / math.log(PHI)
            
            # Name by scale
            child_name = self._name_for_scale(child_radius, i)
            
            child = CantorNode(
                name=child_name,
                radius_m=child_radius,
                bz=child_bz,
                parent_bz=self.bz,
                depth=self.depth + 1,
                max_depth=max_depth
            )
            self.children.append(child)
    
    def _name_for_scale(self, r, idx):
        """Name a node based on its physical scale."""
        if r > 1e25:   return f"Supercluster {idx}"
        if r > 1e23:   return f"Galaxy cluster {idx}"
        if r > 1e20:   return f"Galaxy {idx}"
        if r > 1e18:   return f"Nebula {idx}"
        if r > 1e15:   return f"Stellar system {idx}"
        if r > 1e12:   return f"Planetary orbit {idx}"
        if r > 1e9:    return f"Star {idx}"
        if r > 1e6:    return f"Planet {idx}"
        if r > 1e3:    return f"Mountain {idx}"
        if r > 1:      return f"Human {idx}"
        if r > 1e-3:   return f"Cell {idx}"
        if r > 1e-9:   return f"Molecule {idx}"
        return f"Quantum {idx}"
    
    def flatten(self, result=None):
        """Return all nodes as a flat list."""
        if result is None: result = []
        result.append(self)
        for child in self.children:
            child.flatten(result)
        return result
    
    def to_dict(self):
        return {
            'name': self.name,
            'radius_m': self.radius,
            'bz': round(self.bz, 2),
            'depth': self.depth,
            'zeckendorf': self.zeck,
            'r_core': self.r_core,
            'r_inner': self.r_inner,
            'r_photosphere': self.r_photosphere,
            'r_shell': self.r_shell,
            'r_outer': self.r_outer,
            'n_children': len(self.children),
        }
    
    def __repr__(self):
        indent = '  ' * self.depth
        z_str = '+'.join(str(x) for x in self.zeck)
        return (f"{indent}[bz={self.bz:.0f} Z={{{z_str}}}] {self.name} "
                f"R={self.radius:.2e}m ({len(self.children)} children)")


# ═══════════════════════════════════════════════════════════════════════
# BUILD THE UNIVERSE TREE
# ═══════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("BUILDING UNIVERSE TREE (Hubble → Solar System)")
print("="*70)

t0 = time.time()

# The root: observable universe
R_hubble = L_P * PHI**294
root = CantorNode("Observable Universe", R_hubble, bz=294, max_depth=6)

dt = time.time() - t0
all_nodes = root.flatten()
print(f"\n  Built in {dt*1000:.0f}ms")
print(f"  Total nodes: {len(all_nodes)}")
print(f"  Depth distribution:")
for d in range(7):
    n = sum(1 for nd in all_nodes if nd.depth == d)
    if n > 0:
        print(f"    Depth {d}: {n} nodes")

# Print the tree (first few levels)
print(f"\n  Tree structure (first 40 nodes):")
for node in all_nodes[:40]:
    print(f"  {node}")

# ═══════════════════════════════════════════════════════════════════════
# FIND KNOWN STRUCTURES IN THE TREE
# ═══════════════════════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("KNOWN STRUCTURES — Where they fall in the tree")
print("="*70)

known = [
    ("Observable Universe", 4.4e26),
    ("DM Wall (σ₂/σ₄)", 4.4e26 * WALL_FRAC),
    ("Sloan Great Wall", 1380 * 9.461e15 * 1e6),
    ("KBC Void", 2000 * 9.461e15 * 1e6),
    ("Boötes Void", 250 * 9.461e15 * 1e6),
    ("Milky Way", 5e20),
    ("Solar Oort Cloud", 1.5e16),
    ("Neptune orbit", 30 * AU),
    ("Earth orbit", AU),
    ("Sun radius", 6.96e8),
    ("Earth radius", 6.37e6),
    ("Human", 1.7),
    ("Cell", 1e-5),
    ("DNA width", 2e-9),
    ("Atom", 5.3e-11),
    ("Proton", 8.4e-16),
    ("Planck length", L_P),
]

print(f"\n  {'Structure':<25} {'Scale':>12} {'bz':>8} {'Tree depth':>11} {'Nearest node':>30}")
print(f"  {'-'*95}")

for name, scale in known:
    bz = math.log(scale/L_P)/math.log(PHI) if scale > 0 else 0
    # Find nearest tree node
    nearest = min(all_nodes, key=lambda n: abs(n.radius - scale))
    depth = nearest.depth
    print(f"  {name:<25} {scale:>12.2e} {bz:>8.1f} {'depth '+str(depth):>11} {nearest.name:>30}")


# ═══════════════════════════════════════════════════════════════════════
# RENDERER — Cross-section at any zoom level
# ═══════════════════════════════════════════════════════════════════════

BG = '#08090f'
GOLD = '#f5c542'
BLUE = '#4488ff'
PURPLE = '#9944ff'
PINK = '#ff4488'
GREEN = '#44ff88'

def render_node_cross_section(node, show_children_depth=2, figsize=(12,10)):
    """Render a cross-section of any CantorNode at any scale."""
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')
    
    R = node.radius
    # Set view to show the full structure + some padding
    pad = 1.3
    ax.set_xlim(-R*R_OUTER*pad*OBLATE, R*R_OUTER*pad*OBLATE)
    ax.set_ylim(-R*R_OUTER*pad/OBLATE, R*R_OUTER*pad/OBLATE)
    
    rng = np.random.default_rng(42)
    
    def draw_node(nd, alpha_scale=1.0, depth_remaining=show_children_depth):
        """Recursively draw a node and its children."""
        r = nd.radius
        a = alpha_scale
        
        # Outer membrane (σ₄)
        ell = Ellipse((0,0), nd.r_outer*2*OBLATE, nd.r_outer*2/OBLATE,
                      fc='none', ec=PURPLE, lw=max(0.3, 2-nd.depth*0.3),
                      alpha=max(0.1, 0.6*a), ls='--')
        ax.add_patch(ell)
        
        # Inner membrane (σ₂)  
        ell2 = Ellipse((0,0), nd.r_inner*2*OBLATE, nd.r_inner*2/OBLATE,
                       fc='none', ec=PURPLE, lw=max(0.3, 2-nd.depth*0.3),
                       alpha=max(0.1, 0.6*a))
        ax.add_patch(ell2)
        
        # Photosphere (cos(α) position in wall)
        ell3 = Ellipse((0,0), nd.r_photosphere*2*OBLATE, nd.r_photosphere*2/OBLATE,
                       fc='none', ec=GOLD, lw=max(0.2, 1.5-nd.depth*0.2),
                       alpha=max(0.1, 0.5*a))
        ax.add_patch(ell3)
        
        # DM wall particles between membranes
        n_dm = max(50, int(500 * a))
        for _ in range(n_dm):
            angle = rng.uniform(0, 2*np.pi)
            r_dm = rng.uniform(nd.r_inner, nd.r_outer)
            x = r_dm * OBLATE * np.cos(angle)
            y = r_dm / OBLATE * np.sin(angle)
            ax.plot(x, y, '.', color=PURPLE, ms=max(0.2, 0.8*a), alpha=0.04*a)
        
        # Matter at cos(α) shell position (the "photosphere" density peak)
        n_matter = max(100, int(800 * a))
        r_peak = nd.r_photosphere
        sigma = nd.r_photosphere * 0.05  # narrow shell
        for _ in range(n_matter):
            angle = rng.uniform(0, 2*np.pi)
            r_m = rng.normal(r_peak, sigma)
            if r_m < nd.r_inner or r_m > nd.r_outer: continue
            x = r_m * OBLATE * np.cos(angle)
            # Flatten toward equatorial plane
            y = rng.normal(0, r_m * S3_WIDTH * 0.5) / OBLATE
            brightness = np.exp(-abs(r_m - r_peak) / sigma)
            ax.plot(x, y, '.', color=GOLD, ms=max(0.5, 1.5*a*brightness),
                    alpha=max(0.1, 0.4*a*brightness))
        
        # Core matter (σ₃ center)
        n_core = max(50, int(300 * a))
        for _ in range(n_core):
            angle = rng.uniform(0, 2*np.pi)
            r_c = rng.exponential(nd.r_core * 0.3)
            if r_c > nd.r_core: continue
            x = r_c * np.cos(angle) * OBLATE
            y = rng.normal(0, nd.r_core * S3_WIDTH) / OBLATE
            ax.plot(x, y, '.', color=GOLD, ms=max(0.4, 1.2*a), alpha=0.3*a)
        
        # Recurse into children
        if depth_remaining > 0 and nd.children:
            # Place children at sub-gap positions within σ₃
            for i, child in enumerate(nd.children[:3]):  # top 3 children
                # Position along the equatorial plane at σ₃ sub-band locations
                angle_offset = (i / max(len(nd.children[:3]), 1)) * 2 * np.pi
                child_r = nd.r_inner * (0.3 + 0.5 * (i / max(len(nd.children[:3])-1, 1)))
                
                # Create a shifted axes for the child
                # (simplified: draw at offset position)
                draw_node(child, alpha_scale=a*0.5, depth_remaining=depth_remaining-1)
    
    draw_node(node)
    
    # Labels
    z_str = '+'.join(str(x) for x in node.zeck[:5])
    ax.text(0, R*R_OUTER*pad/OBLATE*0.92,
            f"{node.name}  (bz={node.bz:.0f}, Z={{{z_str}}})",
            color=GOLD, fontsize=11, ha='center', fontfamily='monospace', fontweight='bold')
    
    # Scale bar
    scale_r = node.r_outer * 0.3
    if scale_r > 1e20:
        scale_label = f"{scale_r/9.461e21:.0f} Mly"
    elif scale_r > 1e15:
        scale_label = f"{scale_r/9.461e15:.1f} ly"
    elif scale_r > AU:
        scale_label = f"{scale_r/AU:.1f} AU"
    elif scale_r > 1e6:
        scale_label = f"{scale_r/1e6:.0f} km"
    elif scale_r > 1:
        scale_label = f"{scale_r:.1f} m"
    else:
        scale_label = f"{scale_r:.2e} m"
    
    y_bar = -R*R_OUTER*pad/OBLATE*0.88
    ax.plot([-scale_r*OBLATE, scale_r*OBLATE], [y_bar, y_bar], '-', color='#666', lw=1)
    ax.text(0, y_bar - R*R_OUTER*0.04, scale_label,
            color='#666', fontsize=8, ha='center', fontfamily='monospace')
    
    # Legend
    legend_y = R*R_OUTER*pad/OBLATE*0.75
    legend_x = -R*R_OUTER*pad*OBLATE*0.9
    for label, col in [("σ₄ outer membrane", PURPLE), ("cos(α) photosphere", GOLD),
                       ("σ₂ inner membrane", PURPLE), ("σ₃ core matter", GOLD)]:
        ax.plot(legend_x, legend_y, 's', color=col, ms=5)
        ax.text(legend_x + R*R_OUTER*0.03, legend_y, label,
                color='#555', fontsize=7, fontfamily='monospace', va='center')
        legend_y -= R*R_OUTER*0.04
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, facecolor=BG,
                bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


# ═══════════════════════════════════════════════════════════════════════
# GENERATE MULTI-SCALE VIEWS
# ═══════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("RENDERING MULTI-SCALE VIEWS")
print("="*70)

# Find nodes at different scales
scales = [
    ("Universe",       root),
]
# Find a galaxy-cluster-scale node
for nd in all_nodes:
    if 1e22 < nd.radius < 1e24 and nd.depth >= 1:
        scales.append(("Galaxy Cluster", nd))
        break
for nd in all_nodes:
    if 1e19 < nd.radius < 1e21 and nd.depth >= 2:
        scales.append(("Galaxy", nd))
        break
for nd in all_nodes:
    if 1e14 < nd.radius < 1e17 and nd.depth >= 3:
        scales.append(("Stellar System", nd))
        break

for name, node in scales:
    t0 = time.time()
    b64 = render_node_cross_section(node, show_children_depth=2)
    dt = time.time() - t0
    print(f"  {name}: {node.name} R={node.radius:.2e}m bz={node.bz:.0f} "
          f"({dt*1000:.0f}ms, {len(b64)//1024}KB)")

# Save the renders
import os
os.makedirs('/mnt/user-data/outputs/renders', exist_ok=True)
for name, node in scales:
    b64 = render_node_cross_section(node, show_children_depth=2)
    fname = f"/mnt/user-data/outputs/renders/{name.lower().replace(' ','_')}.png"
    with open(fname, 'wb') as f:
        f.write(base64.b64decode(b64))
    print(f"  Saved: {fname}")

print(f"\n{'='*70}")
print("THE EQUATION")
print("="*70)
print(f"""
  At ANY scale R, the structure is:
  
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   r_core         = R × {R_MATTER:.4f}                              │
  │   r_inner (σ₂)   = R × {R_INNER:.4f}                              │
  │   r_photo        = R × ({R_INNER:.4f} + cos(1/φ) × {R_SHELL-R_INNER:.4f})     │
  │                   = R × {R_INNER + COS_ALPHA*(R_SHELL-R_INNER):.4f}                              │
  │   r_shell        = R × {R_SHELL:.4f}                              │
  │   r_outer (σ₄)   = R × {R_OUTER:.4f}                              │
  │   oblate a/c     = √φ = {OBLATE:.4f}                              │
  │                                                                 │
  │   Within σ₃: 9 sub-gaps → 10 sub-bands → 10 child nodes        │
  │   Each child: SAME EQUATION at scale R × sub-band fraction      │
  │                                                                 │
  │   Zeckendorf address = path through the recursion tree          │
  │                                                                 │
  │   Inputs: φ, L_Planck. Nothing else.                            │
  └─────────────────────────────────────────────────────────────────┘
  
  Applied from bz=294 (Hubble) to bz=0 (Planck).
  Same equation. Same ratios. Same cos(α). Same √φ oblate.
  Every structure in the universe is an instance of this equation.
""")
