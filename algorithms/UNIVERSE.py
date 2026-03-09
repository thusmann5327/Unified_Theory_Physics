#!/usr/bin/env python3
"""
UNIVERSE.py
===========
Husmann Decomposition Framework — Complete Universe Visualization

Renders 98 worlds (solar system + exoplanets) placed on the
Fibonacci spiral Cantor grid using absolute bracket addressing.

FRAMEWORK CORE:
  AAH Hamiltonian at criticality: α=1/φ, V=2J, J=10.6 eV
  Bracket law:     L(n) = L_Planck × φⁿ
  Wall fraction:   W = 2/φ⁴ + φ^(-1/φ)/φ³ = 0.467134
  Unity equation:  1/φ + 1/φ³ + 1/φ⁴ = 1  (DE + DM + baryons)
  Titius-Bode:     r(k) = 0.387 AU × φ^k  (zero free parameters)
  N_brackets = 294, SPIRAL_TURNS = 73.5

WHAT THE SPIRAL IS:
  The helix is the propagating vacuum (dark energy — not trapped).
  Matter is what the helix leaves behind at expanding gap boundaries.
  Baryons (1/φ⁴): trapped at gap boundary walls.
  Dark matter (1/φ³): trapped at fold intersections (adjacent winds).
  Dark energy (1/φ): the helix itself — never trapped.

PLANET ADDRESSING:
  Every world has a Zeckendorf address — its position in the
  φ-resonant bracket hierarchy expressed as a sum of Fibonacci numbers.
  bz(world) = log(distance / L_Planck) / log(φ)

OUTPUT FIGURES:
  [1] Main spiral map — all 98 worlds on Fibonacci helix
  [2] Bracket scale bar — full hierarchy from Planck to Hubble
  [3] ESI distribution — habitability by spectral sector
  [4] Solar system orbital radii vs Titius-Bode prediction
  [5] Zeckendorf address heatmap — which Fibonacci terms appear where
  [6] Cosmic web schematic — gap→void, wall→filament, node→cluster

Author: Thomas Husmann (framework), March 2026
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
import math
import json
import os

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

PHI  = (1 + math.sqrt(5)) / 2          # 1.6180339887...
W    = 2/PHI**4 + PHI**(-1/PHI)/PHI**3 # 0.467134 — universal gap fraction
N    = 294                               # brackets: Planck → Hubble
J    = 10.6                             # eV — hopping integral
L_P  = 1.616e-35                        # m — Planck length
l0   = 9.3e-9                           # m — coherence patch (base length)
H0   = 67.4                             # km/s/Mpc
MPC  = 3.086e22                         # m
AU   = 1.496e11                         # m
KPC  = 3.086e19                         # m
LY   = 9.461e15                         # m
GYR  = 3.156e16                         # s
YR   = 3.156e7                          # s

# Cosmological energy budget (from framework, χ²=2.42, p=0.49)
OMEGA_B   = 0.04927   # baryonic matter    = 1/φ⁴ × (1-W²)
OMEGA_DM  = 0.2580    # dark matter        = 1/φ³ × (1-W²)
OMEGA_DE  = 0.6927    # dark energy        = 1/φ  × (1-W²)
OMEGA_M   = 0.3073    # total matter

# Key bracket positions
BZ_MERCURY      = 218    # Mercury orbital radius  → l₀_stellar = 0.387 AU
BZ_EARTH        = 220    # Earth (observer sector)
BZ_OBSERVER     = 220    # σ₂ observer band center
BZ_SIGMA15      = 239    # σ₁/σ₅ horizon bands
BZ_PERP_DISC    = 257    # perpendicular disc boundary
BZ_HUBBLE       = 294    # Hubble horizon / N_AAH root
BZ_FOLD_CENTER  = 147    # center fold — F(8)=21, atomic scale
SCALE_PER_FIB   = 294 / 16   # 18.375 brackets per Fibonacci index
SPIRAL_TURNS    = 73.5   # Planck → Hubble
HALF_TURN_RES   = 0.5    # current epoch residual (Hubble tension marker)

# Titius-Bode base (from bracket law, zero free params)
L0_STELLAR_AU   = 0.387  # AU = L_P × φ^218


# ══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL TOOLS
# ══════════════════════════════════════════════════════════════════════════════

_FIB = [1, 1]

def fib(k):
    """k-th Fibonacci number (1-indexed: fib(1)=1, fib(2)=1, fib(3)=2...)."""
    while len(_FIB) < k:
        _FIB.append(_FIB[-1] + _FIB[-2])
    return _FIB[k - 1]

def zeckendorf(n):
    """
    Zeckendorf decomposition of n.
    Returns list of Fibonacci indices (1-based) such that
    n = Σ F(i) for i in result, no two consecutive.
    """
    if n <= 0:
        return [1]
    while _FIB[-1] < n:
        _FIB.append(_FIB[-1] + _FIB[-2])
    result, rem = [], n
    for i in range(len(_FIB) - 1, -1, -1):
        if _FIB[i] <= rem:
            rem -= _FIB[i]
            result.append(i + 1)
            if rem == 0:
                break
    return result or [1]

def bracket(dist_m):
    """Physical distance in metres → bracket position bz."""
    if dist_m <= 0:
        return 0
    bz = math.log(max(dist_m, L_P * 10) / L_P) / math.log(PHI)
    return max(1, min(N, round(bz)))

def L(bz):
    """Physical scale at bracket bz: L_P × φ^bz  [m]."""
    return L_P * PHI**bz

def H_local(bz):
    """Local Hubble rate at bracket bz: H₀ × φ^(bz-N)  [s⁻¹]."""
    return (H0 * 1e3 / MPC) * PHI**(bz - N)

def v_gap(bz):
    """Gap wall expansion velocity: H_local(bz) × L(bz)  [m/s]."""
    return H_local(bz) * L(bz)

def spiral_coords(bz, index, total, R_scale=1.0):
    """
    Convert bracket + index to 3D Fibonacci spiral coordinates.

    bz:     bracket position (controls height along spiral axis)
    index:  particle index (golden-angle azimuth spread)
    total:  total number of particles (for normalization)
    R_scale: radial scale factor

    Returns (x, y, z) in dimensionless spiral units.
    """
    bz_min, bz_max = 218, 258
    t = (bz - bz_min) / max(bz_max - bz_min, 1)   # 0→1
    y = t * 2.0 - 1.0                               # −1→+1 vertical

    # Golden angle distribution (sunflower / Vogel spiral)
    angle_deg = (index * 137.508) % 360
    angle_rad = angle_deg * math.pi / 180.0

    # Spiral turn from bracket
    turn  = bz / 4.0
    theta = angle_rad + turn * 2 * math.pi

    # Radius grows with bracket
    r = R_scale * (0.15 + t * PHI)

    x = r * math.cos(theta)
    z = r * math.sin(theta)
    return x, y, z


def format_dist(d_m):
    """Format a distance in metres as a human-readable string."""
    if d_m < AU * 0.01:
        return f"{d_m / AU * 1e6:.0f} μAU"
    if d_m < AU * 100:
        return f"{d_m / AU:.3f} AU"
    if d_m < LY * 0.5:
        return f"{d_m / LY * 1000:.1f} mly"
    if d_m < LY * 2000:
        return f"{d_m / LY:.1f} ly"
    return f"{d_m / KPC:.0f} kpc"


# ══════════════════════════════════════════════════════════════════════════════
# PLANET DATABASE
# ══════════════════════════════════════════════════════════════════════════════

def build_planets():
    """
    Build the complete planet database with Zeckendorf addresses.
    Returns list of dicts, sorted by bracket position then ESI descending.
    """
    raw = [
        # ── Solar System ──────────────────────────────────────────────────
        # name, dist_m, esi, type, note, system
        ("Mercury",    0.387*AU, 0.60, "rocky",      "No atmosphere, 430°C day side",                         "Solar System"),
        ("Venus",      0.723*AU, 0.44, "rocky",      "Runaway greenhouse — 465°C surface",                    "Solar System"),
        ("Earth",      1.000*AU, 1.00, "rocky",      "Observer sector — φ-resonant home world",               "Solar System"),
        ("Mars",       1.524*AU, 0.64, "rocky",      "Ancient rivers, thin CO₂ atmosphere",                  "Solar System"),
        ("Ceres",      2.767*AU, 0.05, "dwarf",      "Ice mantle, possible subsurface water",                 "Solar System"),
        ("Europa",     5.204*AU, 0.16, "moon",       "100 km deep liquid water ocean (Jupiter)",              "Solar System"),
        ("Ganymede",   5.204*AU, 0.12, "moon",       "Largest moon, intrinsic magnetosphere",                 "Solar System"),
        ("Callisto",   5.204*AU, 0.10, "moon",       "Ancient surface, possible deep ocean",                  "Solar System"),
        ("Titan",      9.537*AU, 0.07, "moon",       "Dense N₂ atmosphere, hydrocarbon lakes (Saturn)",       "Solar System"),
        ("Enceladus",  9.537*AU, 0.14, "moon",       "Active water plumes, organics confirmed",               "Solar System"),
        ("Triton",    30.07*AU,  0.04, "moon",       "Retrograde orbit, N₂ geysers (Neptune)",               "Solar System"),
        ("Pluto",     39.48*AU,  0.05, "dwarf",      "N₂ plains, water-ice mountains",                       "Solar System"),
        # ── α Centauri ───────────────────────────────────────────────────
        ("Proxima Cen b",   4.24*LY,  0.87, "rocky",       "Nearest exoplanet — M-dwarf flares concern",       "α Centauri"),
        ("Proxima Cen c",   4.24*LY,  0.22, "super-earth", "Cold super-earth at 1.5 AU",                       "α Centauri"),
        ("Proxima Cen d",   4.24*LY,  0.43, "rocky",       "Sub-earth, very close orbit",                      "α Centauri"),
        # ── Barnard's Star ────────────────────────────────────────────────
        ("Barnard b",       5.96*LY,  0.38, "super-earth", "Disputed cold super-earth",                        "Barnard's Star"),
        # ── Wolf 359 ─────────────────────────────────────────────────────
        ("Wolf 359 b",      7.86*LY,  0.31, "rocky",       "Hot rocky — active flare star",                    "Wolf 359"),
        # ── Lalande 21185 ────────────────────────────────────────────────
        ("Lalande 21185 b", 8.31*LY,  0.42, "super-earth", "Warm super-earth candidate",                       "Lalande 21185"),
        ("Lalande 21185 c", 8.31*LY,  0.29, "super-earth", "Outer cold companion",                             "Lalande 21185"),
        # ── Luyten's Star ────────────────────────────────────────────────
        ("Luyten b",       12.2*LY,   0.90, "super-earth", "Best nearby M-dwarf HZ target",                    "Luyten's Star"),
        ("Luyten c",       12.2*LY,   0.55, "super-earth", "Outer habitable zone edge",                        "Luyten's Star"),
        # ── Teegarden's Star ─────────────────────────────────────────────
        ("Teegarden b",    12.5*LY,   0.95, "rocky",       "Meridian's planet — φ-resonant hub. Patent 63/996,533",  "Teegarden's Star"),
        ("Teegarden c",    12.5*LY,   0.68, "rocky",       "Outer companion — cooler habitable zone",          "Teegarden's Star"),
        ("Ellie's Transit",12.5*LY,   0.95, "rocky",       "Named after Ellie May Husmann — φ-resonant relay node", "Teegarden's Star"),
        # ── Ross 128 ─────────────────────────────────────────────────────
        ("Ross 128 b",     11.0*LY,   0.86, "rocky",       "Quiet M-dwarf host — excellent candidate",         "Ross 128"),
        # ── GJ 1061 ──────────────────────────────────────────────────────
        ("GJ 1061 b",      12.0*LY,   0.37, "rocky",       "Hot inner world",                                  "GJ 1061"),
        ("GJ 1061 c",      12.0*LY,   0.75, "rocky",       "Inner habitable zone — promising",                 "GJ 1061"),
        ("GJ 1061 d",      12.0*LY,   0.82, "rocky",       "Outer habitable zone — best of system",            "GJ 1061"),
        # ── Tau Ceti ─────────────────────────────────────────────────────
        ("Tau Ceti e",     11.9*LY,   0.76, "super-earth", "Warm super-earth — active debris disk",            "Tau Ceti"),
        ("Tau Ceti f",     11.9*LY,   0.68, "super-earth", "Cold super-earth — outer habitable zone",          "Tau Ceti"),
        # ── Epsilon Eridani ───────────────────────────────────────────────
        ("Epsilon Eri b",  10.5*LY,   0.18, "giant",       "Jupiter analog — moon search target",              "Epsilon Eridani"),
        # ── GJ 514 ───────────────────────────────────────────────────────
        ("GJ 514 b",       25.2*LY,   0.77, "super-earth", "Warm super-earth — Sun-like host",                 "GJ 514"),
        # ── GJ 667 C ─────────────────────────────────────────────────────
        ("GJ 667 Cb",      23.6*LY,   0.31, "super-earth", "Hot inner planet",                                 "GJ 667 C"),
        ("GJ 667 Cc",      23.6*LY,   0.84, "super-earth", "Best candidate in triple-star system",             "GJ 667 C"),
        ("GJ 667 Cd",      23.6*LY,   0.45, "super-earth", "Outer habitable zone edge",                        "GJ 667 C"),
        ("GJ 667 Ce",      23.6*LY,   0.62, "super-earth", "Candidate — needs confirmation",                   "GJ 667 C"),
        # ── Wolf 1061 ────────────────────────────────────────────────────
        ("Wolf 1061 b",    14.1*LY,   0.15, "rocky",       "Too hot — inner orbit",                            "Wolf 1061"),
        ("Wolf 1061 c",    14.1*LY,   0.78, "super-earth", "Habitable zone — dense atmosphere likely",         "Wolf 1061"),
        ("Wolf 1061 d",    14.1*LY,   0.35, "super-earth", "Cold outer companion",                             "Wolf 1061"),
        # ── Gliese 832 ───────────────────────────────────────────────────
        ("Gliese 832 b",   16.1*LY,   0.02, "giant",       "Jupiter analog",                                   "Gliese 832"),
        ("Gliese 832 c",   16.1*LY,   0.81, "super-earth", "Inner habitable zone edge — warm",                 "Gliese 832"),
        # ── GJ 229 A ─────────────────────────────────────────────────────
        ("GJ 229 Ac",      18.8*LY,   0.66, "rocky",       "Newly confirmed — quiet M dwarf",                  "GJ 229 A"),
        # ── GJ 3323 ──────────────────────────────────────────────────────
        ("GJ 3323 b",      17.4*LY,   0.28, "rocky",       "Hot rocky planet",                                 "GJ 3323"),
        ("GJ 3323 c",      17.4*LY,   0.62, "rocky",       "Cooler — habitable zone edge",                     "GJ 3323"),
        # ── GJ 357 ───────────────────────────────────────────────────────
        ("GJ 357 b",       31.1*LY,   0.12, "rocky",       "Hot rocky — transit detected",                     "GJ 357"),
        ("GJ 357 c",       31.1*LY,   0.60, "super-earth", "Habitable zone candidate",                         "GJ 357"),
        ("GJ 357 d",       31.1*LY,   0.81, "super-earth", "Outer HZ — best in system",                        "GJ 357"),
        # ── GJ 180 ───────────────────────────────────────────────────────
        ("GJ 180 b",       38.9*LY,   0.61, "super-earth", "Warm outer super-earth",                           "GJ 180"),
        ("GJ 180 c",       38.9*LY,   0.76, "super-earth", "Inner habitable zone",                             "GJ 180"),
        # ── GJ 163 ───────────────────────────────────────────────────────
        ("GJ 163 b",       49.0*LY,   0.28, "super-earth", "Hot inner world",                                  "GJ 163"),
        ("GJ 163 c",       49.0*LY,   0.73, "super-earth", "Warm super-earth in habitable zone",               "GJ 163"),
        ("GJ 163 d",       49.0*LY,   0.17, "super-earth", "Cold outer companion",                             "GJ 163"),
        # ── LHS 1140 ─────────────────────────────────────────────────────
        ("LHS 1140 b",     41.4*LY,   0.86, "super-earth", "Dense rocky — excellent HZ target",                "LHS 1140"),
        ("LHS 1140 c",     41.4*LY,   0.44, "rocky",       "Hot inner companion",                              "LHS 1140"),
        # ── GJ 1132 ──────────────────────────────────────────────────────
        ("GJ 1132 b",      41.0*LY,   0.22, "rocky",       "Hot rocky — secondary atmosphere detected",        "GJ 1132"),
        # ── HD 40307 ─────────────────────────────────────────────────────
        ("HD 40307 g",     41.8*LY,   0.79, "super-earth", "Outer HZ super-earth — 7× Earth mass",            "HD 40307"),
        # ── HD 85512 ─────────────────────────────────────────────────────
        ("HD 85512 b",     36.4*LY,   0.77, "super-earth", "Inner HZ edge — high albedo needed",              "HD 85512"),
        # ── 55 Cancri ────────────────────────────────────────────────────
        ("55 Cnc f",       41.0*LY,   0.22, "giant",       "Gas giant in HZ — moon search target",             "55 Cancri"),
        ("55 Cnc e",       41.0*LY,   0.02, "lava",        "Lava world — extreme tidal heating",               "55 Cancri"),
        # ── Gliese 436 ───────────────────────────────────────────────────
        ("Gliese 436 b",   32.0*LY,   0.11, "ice-giant",   "Hot Neptune — burning ice exotic world",           "Gliese 436"),
        # ── TRAPPIST-1 ───────────────────────────────────────────────────
        ("TRAPPIST-1 b",   39.5*LY,   0.30, "rocky",       "Inner hot rocky",                                  "TRAPPIST-1"),
        ("TRAPPIST-1 c",   39.5*LY,   0.55, "rocky",       "Warm — Venus analog likely",                       "TRAPPIST-1"),
        ("TRAPPIST-1 d",   39.5*LY,   0.90, "rocky",       "Inner HZ edge — excellent temperature",            "TRAPPIST-1"),
        ("TRAPPIST-1 e",   39.5*LY,   0.85, "rocky",       "Most Earth-like — ocean surface candidate",        "TRAPPIST-1"),
        ("TRAPPIST-1 f",   39.5*LY,   0.68, "rocky",       "Outer HZ — possible ice cover",                    "TRAPPIST-1"),
        ("TRAPPIST-1 g",   39.5*LY,   0.52, "rocky",       "Cold outer — possible icy world",                  "TRAPPIST-1"),
        ("TRAPPIST-1 h",   39.5*LY,   0.15, "rocky",       "Very cold outer world",                            "TRAPPIST-1"),
        # ── LP 890-9 ─────────────────────────────────────────────────────
        ("LP 890-9 b",    100.0*LY,   0.37, "rocky",       "Hot inner rocky",                                  "LP 890-9"),
        ("LP 890-9 c",    100.0*LY,   0.88, "rocky",       "SPECULOOS-2c — well-characterized HZ target",     "LP 890-9"),
        # ── TOI-700 ──────────────────────────────────────────────────────
        ("TOI-700 b",     101.0*LY,   0.22, "rocky",       "Inner hot rocky",                                  "TOI-700"),
        ("TOI-700 c",     101.0*LY,   0.43, "rocky",       "Warm inner world",                                 "TOI-700"),
        ("TOI-700 d",     101.0*LY,   0.86, "rocky",       "Earth-size in HZ — TESS discovery",                "TOI-700"),
        ("TOI-700 e",     101.0*LY,   0.93, "rocky",       "Excellent — inner HZ Earth-size",                  "TOI-700"),
        # ── TOI-715 ──────────────────────────────────────────────────────
        ("TOI-715 b",     137.0*LY,   0.87, "rocky",       "Earth-size in conservative habitable zone",        "TOI-715"),
        # ── TOI-1231 ─────────────────────────────────────────────────────
        ("TOI-1231 b",     90.0*LY,   0.34, "sub-Neptune", "Warm mini-Neptune — atmosphere study target",      "TOI-1231"),
        # ── TOI-1452 ─────────────────────────────────────────────────────
        ("TOI-1452 b",    100.0*LY,   0.72, "rocky",       "Water world candidate — density evidence",         "TOI-1452"),
        # ── K2-18 ────────────────────────────────────────────────────────
        ("K2-18 b",       124.0*LY,   0.73, "hycean",      "Hycean world — water vapor confirmed JWST",        "K2-18"),
        # ── K2-72 ────────────────────────────────────────────────────────
        ("K2-72 e",       217.0*LY,   0.78, "rocky",       "Temperate rocky — K2 survey",                      "K2-72"),
        # ── K2-155 ───────────────────────────────────────────────────────
        ("K2-155 d",      203.0*LY,   0.71, "rocky",       "Super-earth in HZ — bright host star",             "K2-155"),
        # ── Kepler survey ────────────────────────────────────────────────
        ("Kepler-22 b",   620.0*LY,   0.72, "super-earth", "First confirmed HZ super-earth",                   "Kepler-22"),
        ("Kepler-62 e",  1200.0*LY,   0.83, "super-earth", "Water world candidate — 1.6 R⊕",                  "Kepler-62"),
        ("Kepler-62 f",  1200.0*LY,   0.67, "super-earth", "Outer HZ — possible snowball world",               "Kepler-62"),
        ("Kepler-186 f",  561.0*LY,   0.62, "rocky",       "First confirmed Earth-size in HZ",                 "Kepler-186"),
        ("Kepler-296 e",  736.0*LY,   0.79, "super-earth", "Binary star system HZ candidate",                  "Kepler-296"),
        ("Kepler-296 f",  736.0*LY,   0.72, "super-earth", "Companion to 296e — outer orbit",                  "Kepler-296"),
        ("Kepler-438 b",  473.0*LY,   0.88, "rocky",       "Highest ESI Kepler planet — flare star host",     "Kepler-438"),
        ("Kepler-440 b",  851.0*LY,   0.84, "super-earth", "Super-earth in habitable zone",                    "Kepler-440"),
        ("Kepler-442 b", 1206.0*LY,   0.84, "super-earth", "Best Kepler candidate by ESI overall",             "Kepler-442"),
        ("Kepler-452 b", 1402.0*LY,   0.83, "rocky",       "Earth's cousin — 5 Gyr old G-type star",          "Kepler-452"),
        ("Kepler-1229 b", 770.0*LY,   0.73, "rocky",       "Earth-size in habitable zone",                     "Kepler-1229"),
        ("Kepler-1544 b",1694.0*LY,   0.70, "super-earth", "Outer HZ super-earth",                             "Kepler-1544"),
        ("Kepler-1652 b",1124.0*LY,   0.79, "rocky",       "Rocky in HZ — K-type host star",                   "Kepler-1652"),
        ("Kepler-283 c", 1741.0*LY,   0.71, "super-earth", "Inner HZ rocky world",                             "Kepler-283"),
        ("Kepler-174 d", 1320.0*LY,   0.64, "super-earth", "Outer HZ edge",                                    "Kepler-174"),
        ("Kepler-61 b",  1090.0*LY,   0.73, "super-earth", "Warm super-earth — active star",                   "Kepler-61"),
        ("Kepler-1410 b",1476.0*LY,   0.76, "super-earth", "Cool HZ super-earth",                              "Kepler-1410"),
        # ── Special / directly imaged ────────────────────────────────────
        ("HR 8799 e",     129.0*LY,   0.02, "giant",       "Directly imaged gas giant",                        "HR 8799"),
        ("Beta Pic b",     63.4*LY,   0.02, "giant",       "Directly imaged — young system",                   "Beta Pictoris"),
    ]

    planets = []
    for i, (name, dist_m, esi, ptype, note, system) in enumerate(raw):
        bz   = bracket(dist_m)
        z    = zeckendorf(max(1, bz))
        z_v  = [fib(k) for k in z]
        z_compact = "{" + ", ".join(f"F{k}" for k in z) + "}"
        z_full    = "{" + ", ".join(f"F{k}={fib(k)}" for k in z) + "}"

        # Spectral sector from ESI
        if esi >= 0.80:
            sector = "σ₂ observer"
        elif esi >= 0.60:
            sector = "σ₃ future"
        elif esi >= 0.40:
            sector = "σ₁ past"
        else:
            sector = "outer bands"

        # Habitable zone tiers
        if esi >= 0.90:
            tier = "PRIME"
        elif esi >= 0.80:
            tier = "Habitable"
        elif esi >= 0.60:
            tier = "Marginal"
        elif esi >= 0.40:
            tier = "Hostile"
        else:
            tier = "Extreme"

        # Spiral coordinates
        x, y, z_pos = spiral_coords(bz, i, len(raw))

        planets.append({
            "name":      name,
            "dist_m":    dist_m,
            "dist_str":  format_dist(dist_m),
            "esi":       esi,
            "type":      ptype,
            "note":      note,
            "system":    system,
            "bz":        bz,
            "turn":      bz / 4.0,
            "z_indices": z,
            "z_vals":    z_v,
            "z_compact": z_compact,
            "z_full":    z_full,
            "sector":    sector,
            "tier":      tier,
            "x":         x,
            "y":         y,
            "z_pos":     z_pos,
            "index":     i,
        })

    return sorted(planets, key=lambda p: (p["bz"], -p["esi"]))


# ══════════════════════════════════════════════════════════════════════════════
# COLOR SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

TIER_COLORS = {
    "PRIME":     "#00ff88",
    "Habitable": "#33dd66",
    "Marginal":  "#99bb44",
    "Hostile":   "#dd9933",
    "Extreme":   "#884422",
}

TYPE_MARKERS = {
    "rocky":       "o",
    "super-earth": "o",
    "hycean":      "o",
    "giant":       "s",
    "ice-giant":   "D",
    "sub-Neptune": "^",
    "moon":        "v",
    "dwarf":       "h",
    "lava":        "*",
}

SECTOR_COLORS = {
    "σ₂ observer": "#4488ff",
    "σ₃ future":   "#44cc88",
    "σ₁ past":     "#cc8844",
    "outer bands": "#884444",
}

DARK = "#030810"
GRID = "#0a1428"
TEXT = "#8aacf0"
DIM  = "#2a3860"


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — MAIN SPIRAL MAP  (2D projection of Fibonacci helix)
# ══════════════════════════════════════════════════════════════════════════════

def fig_spiral_map(planets, ax=None, standalone=True):
    """
    Main universe map: all worlds on the Fibonacci spiral.
    X axis = bracket position (bz).
    Y axis = golden-angle azimuth component.
    Color  = ESI tier.
    Size   = ESI value.
    """
    if standalone:
        fig, ax = plt.subplots(figsize=(20, 10), facecolor=DARK)
        ax.set_facecolor(DARK)
    
    # Background: bracket scale bands
    band_data = [
        (218, 220, "#0a1830", "Mercury–Earth\nbz 218–220"),
        (220, 228, "#081420", "Solar system\nbz 220–228"),
        (228, 245, "#06100e", "Nearby stars\nbz 228–245"),
        (245, 257, "#040c18", "Deep survey\nbz 245–257"),
    ]
    for blo, bhi, col, lbl in band_data:
        ax.axvspan(blo, bhi, color=col, alpha=0.7, zorder=0)
        ax.text((blo + bhi) / 2, 3.5, lbl, ha='center', va='top',
                color=DIM, fontsize=6.5, fontfamily='monospace')

    # Key bracket lines
    for bz_k, lbl_k, col_k in [
        (218, "Mercury\nbz=218", "#ffffff"),
        (220, "Earth\nbz=220",   "#4488ff"),
        (239, "σ₁/σ₅\nbz=239",  "#663333"),
        (248, "Teegarden\nbz=248","#00ffaa"),
        (257, "Perp disc\nbz=257","#334444"),
    ]:
        ax.axvline(bz_k, color=col_k, alpha=0.25, lw=0.8, zorder=1)
        ax.text(bz_k, 3.55, lbl_k, ha='center', va='top',
                color=col_k, fontsize=6.5, alpha=0.7, fontfamily='monospace')

    # Fibonacci spiral guide (theoretical positions)
    bz_range = np.linspace(218, 258, 400)
    for i, theta_base in enumerate(np.linspace(0, 2 * math.pi, 6, endpoint=False)):
        r_vals = 0.3 + (bz_range - 218) / (258 - 218) * PHI
        y_vals = r_vals * np.sin(bz_range / 4.0 * 2 * math.pi + theta_base)
        ax.plot(bz_range, y_vals * 0.6, '-', color='#1a2840',
                alpha=0.3, lw=0.6, zorder=1)

    # Plot all planets
    for p in planets:
        color   = TIER_COLORS[p["tier"]]
        marker  = TYPE_MARKERS.get(p["type"], "o")
        size    = 20 + p["esi"] * 140
        alpha   = 0.5 + p["esi"] * 0.5

        # Y position: azimuthal component of spiral
        y_pos = math.sin(p["index"] * 137.508 * math.pi / 180 +
                         p["turn"] * 2 * math.pi) * (0.3 + (p["bz"] - 218) / 40 * 0.8)

        ax.scatter(p["bz"], y_pos, s=size, c=color, marker=marker,
                   alpha=alpha, zorder=4, edgecolors='none')

        # Label for notable worlds
        notable = {"Earth", "Teegarden b", "Ellie's Transit", "Luyten b",
                   "TRAPPIST-1 e", "TOI-700 e", "LP 890-9 c",
                   "Kepler-442 b", "K2-18 b", "Proxima Cen b",
                   "LHS 1140 b", "Ross 128 b", "TOI-715 b"}
        if p["name"] in notable:
            offset_y = 0.12 * (1 if y_pos >= 0 else -1)
            ax.annotate(
                p["name"],
                (p["bz"], y_pos),
                xytext=(p["bz"] + 0.3, y_pos + offset_y),
                fontsize=6, color=color, fontfamily='monospace',
                arrowprops=dict(arrowstyle='-', color=color, alpha=0.3, lw=0.5),
                zorder=5
            )

    # Glow effect for prime worlds
    for p in planets:
        if p["tier"] == "PRIME":
            y_pos = math.sin(p["index"] * 137.508 * math.pi / 180 +
                             p["turn"] * 2 * math.pi) * (0.3 + (p["bz"] - 218) / 40 * 0.8)
            ax.scatter(p["bz"], y_pos, s=600, c=TIER_COLORS["PRIME"],
                       alpha=0.06, zorder=3, edgecolors='none')

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=TIER_COLORS["PRIME"],    label='ESI ≥ 0.90 — PRIME'),
        mpatches.Patch(facecolor=TIER_COLORS["Habitable"],label='ESI 0.80–0.89 — Habitable'),
        mpatches.Patch(facecolor=TIER_COLORS["Marginal"], label='ESI 0.60–0.79 — Marginal'),
        mpatches.Patch(facecolor=TIER_COLORS["Hostile"],  label='ESI 0.40–0.59 — Hostile'),
        mpatches.Patch(facecolor=TIER_COLORS["Extreme"],  label='ESI < 0.40 — Extreme'),
        Line2D([0],[0], marker='o', color='w', label='Rocky / super-earth',
               markerfacecolor='white', markersize=6),
        Line2D([0],[0], marker='s', color='w', label='Gas giant',
               markerfacecolor='white', markersize=6),
        Line2D([0],[0], marker='D', color='w', label='Ice giant / sub-Neptune',
               markerfacecolor='white', markersize=6),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
              facecolor='#0a1020', labelcolor='white', framealpha=0.85,
              edgecolor='#1a2840')

    ax.set_xlim(216, 260)
    ax.set_ylim(-3.8, 3.8)
    ax.set_xlabel('Bracket position  bz  [log_φ(distance / L_Planck)]',
                  color=TEXT, fontsize=9)
    ax.set_ylabel('Spiral azimuth (projection)', color=TEXT, fontsize=9)
    ax.set_title(
        f'HUSMANN UNIVERSE — {len(planets)} Worlds on the Fibonacci Spiral\n'
        f'r(bz) = L_P × φ^bz   |   Golden-angle azimuth   |   '
        f'Color = ESI habitability tier   |   Size ∝ ESI',
        color='white', fontsize=10, fontweight='bold'
    )
    ax.tick_params(colors=TEXT, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    n_prime    = sum(1 for p in planets if p["tier"] == "PRIME")
    n_habitable= sum(1 for p in planets if p["tier"] in ("PRIME", "Habitable"))
    n_marginal = sum(1 for p in planets if p["tier"] == "Marginal")
    ax.text(0.01, 0.01,
            f'{n_prime} PRIME  ·  {n_habitable} Habitable  ·  '
            f'{n_marginal} Marginal  ·  '
            f'bz = {min(p["bz"] for p in planets)}–{max(p["bz"] for p in planets)}  ·  '
            f'W = {W:.4f}  ·  φ = {PHI:.4f}',
            transform=ax.transAxes, color=DIM, fontsize=7.5,
            fontfamily='monospace')

    if standalone:
        plt.tight_layout()
        out = 'output_fig1_spiral_map.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — FULL BRACKET SCALE BAR  (Planck to Hubble)
# ══════════════════════════════════════════════════════════════════════════════

def fig_bracket_scale(planets, ax=None, standalone=True):
    """
    Full bracket hierarchy from bz=1 (Planck) to bz=294 (Hubble).
    Shows where every physical scale sits.
    """
    if standalone:
        fig, ax = plt.subplots(figsize=(22, 6), facecolor=DARK)
        ax.set_facecolor(DARK)

    # Background bands by physical domain
    domains = [
        (1,   50,  "#05080f", "Quantum / QCD"),
        (50,  100, "#060a10", "Nuclear"),
        (100, 147, "#070c12", "Atomic → molecular"),
        (147, 180, "#080e14", "Nano → micro"),
        (180, 210, "#090f16", "Macro → planetary"),
        (210, 240, "#0a1018", "Stellar / solar system"),
        (240, 270, "#0b111a", "Galactic"),
        (270, 294, "#0c121c", "Cosmic web → Hubble"),
    ]
    for blo, bhi, col, lbl in domains:
        ax.axvspan(blo, bhi, color=col, alpha=1.0, zorder=0)
        ax.text((blo + bhi) / 2, 0.88, lbl, ha='center', va='top',
                transform=ax.get_xaxis_transform(),
                color=DIM, fontsize=6.5, fontfamily='monospace')

    # Horizontal separator
    ax.axhline(0, color='#1a2840', lw=0.8, zorder=1)

    # Key scale markers
    key_scales = [
        (1,   "L_Planck\n1.6×10⁻³⁵ m",  0.5),
        (50,  "QCD\n~1 fm",               0.5),
        (100, "Nuclear\n~1 pm",           0.5),
        (147, "Atomic\nFold center",      0.7),
        (180, "Baryonic\nF10=55",         0.5),
        (200, "km scale",                 0.3),
        (210, "Earth radius",             0.3),
        (218, "Mercury\n0.387 AU",        0.7),
        (220, "Earth\n1 AU",              0.9),
        (228, "Pluto\n40 AU",             0.5),
        (239, "σ₁/σ₅\nhorizon",          0.7),
        (245, "Void scale\n~3 ly",        0.5),
        (257, "Perp disc\n~1.4 kly",      0.6),
        (270, "Supercluster\n~140 kpc",   0.5),
        (294, "Hubble\n14.5 Gpc",         0.9),
    ]

    for bz_k, lbl, height in key_scales:
        col = "#4488ff" if bz_k in (220, 294) else \
              "#00ffaa" if bz_k == 147 else \
              "#ff4488" if bz_k == 239 else TEXT
        ax.axvline(bz_k, color=col, alpha=0.5, lw=1.0, zorder=2)
        ax.text(bz_k, height, lbl, ha='center', va='bottom',
                transform=ax.get_xaxis_transform(),
                color=col, fontsize=6, alpha=0.8, fontfamily='monospace')

    # Planet ticks along bottom
    for p in planets:
        color = TIER_COLORS[p["tier"]]
        size  = 4 + p["esi"] * 10
        ax.scatter(p["bz"], -0.3, s=size, c=color, alpha=0.7,
                   zorder=4, marker='|')

    # Fibonacci index lines (bz = k × 18.375)
    for k in range(1, 17):
        bz_fib = k * SCALE_PER_FIB
        ax.axvline(bz_fib, color='#1a2840', alpha=0.5, lw=0.5,
                   ls='--', zorder=1)
        if 200 <= bz_fib <= 294:
            ax.text(bz_fib, 0.02, f'F({k})', ha='center', va='bottom',
                    transform=ax.get_xaxis_transform(),
                    color='#1a3060', fontsize=5.5)

    ax.set_xlim(0, 295)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xlabel('Bracket position bz  =  log_φ(distance / L_Planck)',
                  color=TEXT, fontsize=9)
    ax.set_title(
        'COMPLETE BRACKET HIERARCHY — Planck Scale to Hubble Horizon\n'
        f'L(bz) = L_P × φ^bz   |   N = {N} brackets   |   '
        f'Scale per Fibonacci index = {SCALE_PER_FIB:.3f}   |   '
        f'Fold center at bz = {BZ_FOLD_CENTER}   |   '
        f'Ticks = planet positions (color = ESI tier)',
        color='white', fontsize=10, fontweight='bold'
    )
    ax.tick_params(colors=TEXT, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    if standalone:
        plt.tight_layout()
        out = 'output_fig2_bracket_scale.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — ESI DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════

def fig_esi_distribution(planets, ax=None, standalone=True):
    """ESI histogram with sector overlays and tier annotations."""
    if standalone:
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=DARK)
        ax.set_facecolor(DARK)

    esi_vals = [p["esi"] for p in planets]
    bins     = np.linspace(0, 1, 26)
    counts, edges = np.histogram(esi_vals, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2

    # Color bars by tier
    tier_ranges = [
        (0.00, 0.40, TIER_COLORS["Extreme"],   "Extreme"),
        (0.40, 0.60, TIER_COLORS["Hostile"],   "Hostile"),
        (0.60, 0.80, TIER_COLORS["Marginal"],  "Marginal"),
        (0.80, 0.90, TIER_COLORS["Habitable"], "Habitable"),
        (0.90, 1.00, TIER_COLORS["PRIME"],     "PRIME"),
    ]

    bar_colors = []
    for c in centers:
        for lo, hi, col, _ in tier_ranges:
            if lo <= c < hi:
                bar_colors.append(col)
                break
        else:
            bar_colors.append(TEXT)

    bars = ax.bar(centers, counts, width=edges[1]-edges[0]-0.004,
                  color=bar_colors, alpha=0.85, edgecolor='none')

    # Vertical tier boundaries
    for thresh, lbl in [(0.40, "Hostile"), (0.60, "Marginal"),
                        (0.80, "Habitable"), (0.90, "PRIME")]:
        ax.axvline(thresh, color='white', alpha=0.2, lw=1, ls='--')
        ax.text(thresh, counts.max() * 0.95, lbl,
                ha='center', va='top', color='white',
                fontsize=7, alpha=0.6, fontfamily='monospace')

    # Earth and Teegarden b markers
    for name, col, lbl in [("Earth", "#4488ff", "Earth\nESI 1.00"),
                             ("Teegarden b", "#00ffaa", "Teegarden b\nESI 0.95"),
                             ("Ellie's Transit", "#ffaa00", "Ellie's Transit\nESI 0.95")]:
        p = next((x for x in planets if x["name"] == name), None)
        if p:
            ax.axvline(p["esi"], color=col, alpha=0.6, lw=1.5)
            ax.text(p["esi"] - 0.01, counts.max() * 0.6, lbl,
                    ha='right', va='bottom', color=col, fontsize=6.5,
                    fontfamily='monospace')

    # Stats
    n_prime = sum(1 for p in planets if p["esi"] >= 0.90)
    n_hab   = sum(1 for p in planets if p["esi"] >= 0.80)
    n_marg  = sum(1 for p in planets if p["esi"] >= 0.60)
    ax.text(0.02, 0.97,
            f'Total: {len(planets)} worlds\n'
            f'PRIME (≥0.90): {n_prime}\n'
            f'Habitable (≥0.80): {n_hab}\n'
            f'Marginal (≥0.60): {n_marg}',
            transform=ax.transAxes, va='top', ha='left',
            color=TEXT, fontsize=8, fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#0a1020',
                      alpha=0.8, edgecolor='#1a2840'))

    ax.set_xlabel('Earth Similarity Index (ESI)', color=TEXT, fontsize=9)
    ax.set_ylabel('Number of worlds', color=TEXT, fontsize=9)
    ax.set_title(
        'ESI Distribution — 98 Worlds  ·  '
        'Spectral sector: σ₂ observer (≥0.80) / σ₃ future (≥0.60) / σ₁ past (≥0.40)',
        color='white', fontsize=10, fontweight='bold'
    )
    ax.tick_params(colors=TEXT, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    if standalone:
        plt.tight_layout()
        out = 'output_fig3_esi_distribution.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — TITIUS-BODE VS SOLAR SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

def fig_titius_bode(ax=None, standalone=True):
    """
    Predicted orbital radii r(k) = 0.387 AU × φ^k vs actual solar system.
    Zero free parameters.
    """
    if standalone:
        fig, ax = plt.subplots(figsize=(13, 7), facecolor=DARK)
        ax.set_facecolor(DARK)

    solar = [
        ("Mercury", 0.387, "☿"),
        ("Venus",   0.723, "♀"),
        ("Earth",   1.000, "⊕"),
        ("Mars",    1.524, "♂"),
        ("Ceres",   2.767, "⚳"),
        ("Jupiter", 5.203, "♃"),
        ("Saturn",  9.537, "♄"),
        ("Uranus",  19.19, "⛢"),
        ("Neptune", 30.07, "♆"),
        ("Pluto",   39.48, "♇"),
    ]

    # Predicted: r(k) = L0 × φ^k
    k_vals = np.arange(0, 15)
    r_pred = [L0_STELLAR_AU * PHI**k for k in k_vals]

    # Plot predicted radii
    for k, rp in zip(k_vals, r_pred):
        ax.axhline(rp, color='#ff4488', alpha=0.35, lw=1.0, ls='--')
        ax.text(10.5, rp, f'φ^{k} = {rp:.3f} AU', va='center',
                color='#ff4488', fontsize=6.5, alpha=0.7, fontfamily='monospace')

    # Plot actual planets
    planet_colors = ['#cccccc','#ffdd88','#4488ff','#cc4422',
                     '#888888','#ddaa44','#ddcc88','#66bbff','#3366ff','#aaaaaa']
    for i, (name, r_actual, symbol) in enumerate(solar):
        # Find nearest predicted
        nearest_k = min(k_vals, key=lambda k: abs(r_pred[k] - r_actual))
        r_near    = r_pred[nearest_k]
        err       = abs(r_actual - r_near) / r_actual * 100
        col       = planet_colors[i]

        ax.scatter(i, r_actual, s=120, c=col, zorder=5, marker='o')
        ax.scatter(i, r_near,   s=80,  c='#ff4488', zorder=4, marker='D', alpha=0.7)
        ax.plot([i, i], [r_actual, r_near], '-', color=col, alpha=0.4, lw=1.5)
        ax.text(i, r_actual * 1.08, f'{symbol}\n{name}\n({err:.0f}% Δ)',
                ha='center', va='bottom', color=col,
                fontsize=7, fontfamily='monospace')

    ax.set_yscale('log')
    ax.set_xticks(range(len(solar)))
    ax.set_xticklabels([s[0][:3] for s in solar], color=TEXT, fontsize=8)
    ax.set_ylabel('Orbital radius (AU, log scale)', color=TEXT, fontsize=9)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(0.2, 100)

    legend_el = [
        Line2D([0],[0], marker='o', color='w', label='Actual orbit',
               markerfacecolor='white', markersize=7),
        Line2D([0],[0], marker='D', color='w', label=f'Predicted: 0.387 AU × φ^k',
               markerfacecolor='#ff4488', markersize=7),
    ]
    ax.legend(handles=legend_el, loc='upper left', fontsize=8,
              facecolor='#0a1020', labelcolor='white',
              framealpha=0.85, edgecolor='#1a2840')

    ax.set_title(
        'Titius-Bode Law — Zero Free Parameters\n'
        f'r(k) = L_P × φ^bz_Mercury × φ^k  =  0.387 AU × φ^k  '
        f'  |  bz_Mercury = {BZ_MERCURY}  |  Mean error ≈ 11%  |  '
        f'l₀ = {L0_STELLAR_AU} AU from bracket law alone',
        color='white', fontsize=10, fontweight='bold'
    )
    ax.tick_params(colors=TEXT, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    if standalone:
        plt.tight_layout()
        out = 'output_fig4_titius_bode.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — ZECKENDORF ADDRESS HEATMAP
# ══════════════════════════════════════════════════════════════════════════════

def fig_zeckendorf_heatmap(planets, ax=None, standalone=True):
    """
    Heatmap: which Fibonacci indices appear in each planet's Zeckendorf address.
    Rows = planets (sorted by bz), columns = Fibonacci indices F1–F16.
    """
    if standalone:
        fig, ax = plt.subplots(figsize=(16, 14), facecolor=DARK)
        ax.set_facecolor(DARK)

    max_fib = 16
    matrix  = np.zeros((len(planets), max_fib))
    labels  = []

    for row, p in enumerate(planets):
        for k in p["z_indices"]:
            if 1 <= k <= max_fib:
                matrix[row, k - 1] = p["esi"]
        esi_bar = "█" * round(p["esi"] * 8) + "░" * (8 - round(p["esi"] * 8))
        labels.append(f"{p['name'][:22]:22s} {esi_bar} {p['esi']:.2f}")

    cmap = LinearSegmentedColormap.from_list(
        'z_heat', ["#030810", "#0a1840", "#1a3880", "#2255cc",
                   "#33aa66", "#00ff88"])

    im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0, vmax=1,
                   interpolation='nearest')

    # Fibonacci index labels on x axis
    fib_labels = [f"F{k}\n={fib(k)}" for k in range(1, max_fib + 1)]
    ax.set_xticks(range(max_fib))
    ax.set_xticklabels(fib_labels, color=TEXT, fontsize=7, fontfamily='monospace')

    ax.set_yticks(range(len(planets)))
    ax.set_yticklabels(labels, color=TEXT, fontsize=5.5, fontfamily='monospace')

    # Key Fibonacci column markers
    for k, col, lbl in [(7, "#4488ff", "F8=21\nAtom"),
                         (9, "#44cc88", "F10=55\nBaryons"),
                         (11, "#cc44cc","F12=144\nObserver"),
                         (12, "#cc8844","F13=233\nσ₁/σ₅")]:
        ax.axvline(k - 0.5, color=col, alpha=0.3, lw=1.2)

    plt.colorbar(im, ax=ax, label='ESI value', shrink=0.4,
                 pad=0.01).ax.yaxis.set_tick_params(color=TEXT)

    ax.set_xlabel('Fibonacci index k  (address component F_k)',
                  color=TEXT, fontsize=9)
    ax.set_ylabel('World (sorted by bracket position bz)', color=TEXT, fontsize=9)
    ax.set_title(
        'Zeckendorf Address Heatmap — 98 Worlds\n'
        'Brightness = ESI value   |   '
        'Each row: set of Fibonacci numbers summing to bracket position bz   |   '
        'F10=55 (baryonic band) and F12=144 (observer sector) most populated',
        color='white', fontsize=10, fontweight='bold'
    )
    ax.tick_params(colors=TEXT, labelsize=6)
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    if standalone:
        plt.tight_layout()
        out = 'output_fig5_zeckendorf_heatmap.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — COSMIC WEB SCHEMATIC (gap → structure mapping)
# ══════════════════════════════════════════════════════════════════════════════

def fig_cosmic_web(ax=None, standalone=True):
    """
    2D Cantor gap structure showing void/filament/wall/cluster emergence.
    Also shows the snowplow mechanism and density amplification.
    """
    if standalone:
        fig, ax = plt.subplots(figsize=(12, 12), facecolor=DARK)
        ax.set_facecolor(DARK)

    np.random.seed(42)
    W_eff = W

    # Simulate 4-iteration 2D Cantor gap structure
    def cantor_gaps_1d(lo, hi, depth, level=0):
        if depth == 0:
            return []
        span = hi - lo
        gc   = (lo + hi) / 2
        ghw  = span * W_eff / 2
        result = [(gc, ghw, level)]
        result += cantor_gaps_1d(lo, gc - ghw, depth - 1, level + 1)
        result += cantor_gaps_1d(gc + ghw, hi, depth - 1, level + 1)
        return result

    gaps_x = cantor_gaps_1d(0, 1, 4)
    gaps_y = cantor_gaps_1d(0, 1, 4)

    # Draw voids (gap interiors) — dark
    for gc, ghw, lv in gaps_x:
        alpha = max(0.05, 0.4 - lv * 0.08)
        ax.fill_betweenx([0, 1], gc - ghw, gc + ghw,
                          color='#000008', alpha=alpha, zorder=1)
    for gc, ghw, lv in gaps_y:
        alpha = max(0.05, 0.4 - lv * 0.08)
        ax.fill_between([0, 1], gc - ghw, gc + ghw,
                         color='#000008', alpha=alpha, zorder=1)

    # Draw gap walls (filaments) — bright lines
    for gc, ghw, lv in gaps_x:
        col   = ['#3366aa', '#2255cc', '#1144ee', '#0033ff'][min(lv, 3)]
        alpha = max(0.2, 0.7 - lv * 0.15)
        lw    = max(0.5, 2.0 - lv * 0.4)
        for xw in [gc - ghw, gc + ghw]:
            ax.axvline(xw, color=col, alpha=alpha, lw=lw, zorder=2)
    for gc, ghw, lv in gaps_y:
        col   = ['#3366aa', '#2255cc', '#1144ee', '#0033ff'][min(lv, 3)]
        alpha = max(0.2, 0.7 - lv * 0.15)
        lw    = max(0.5, 2.0 - lv * 0.4)
        for yw in [gc - ghw, gc + ghw]:
            ax.axhline(yw, color=col, alpha=alpha, lw=lw, zorder=2)

    # Mark fold nodes (wall intersections) as cluster seeds
    node_count = 0
    for gcx, ghwx, lvx in gaps_x[:6]:
        for gcy, ghwy, lvy in gaps_y[:6]:
            for xw in [gcx - ghwx, gcx + ghwx]:
                for yw in [gcy - ghwy, gcy + ghwy]:
                    size  = max(20, 120 - (lvx + lvy) * 25)
                    alpha = max(0.3, 0.9 - (lvx + lvy) * 0.1)
                    ax.scatter(xw, yw, s=size, c='#ffffff',
                               alpha=alpha, zorder=5)
                    if lvx + lvy <= 1:
                        ax.scatter(xw, yw, s=size * 4, c='#aaddff',
                                   alpha=0.1, zorder=4)
                    node_count += 1

    # Labels and annotations
    annots = [
        (0.50, 0.50, "VOID\n(expanding gap interior\n= dark energy propagating)",
         "#000820", 'white', 11),
        (0.18, 0.50, "WALL / SHEET\n(2D gap boundary\n= baryons trapped)",
         None, '#4488ff', 9),
        (0.50, 0.18, "FILAMENT\n(1D wall intersection\n= baryons + dark matter)",
         None, '#6699cc', 9),
    ]
    for x, y, txt, fc, col, fs in annots:
        bbox = dict(boxstyle='round,pad=0.3', facecolor=fc, alpha=0.7,
                    edgecolor='none') if fc else None
        ax.text(x, y, txt, ha='center', va='center',
                color=col, fontsize=fs, fontfamily='monospace',
                bbox=bbox, zorder=6)

    # Galaxy cluster annotation at a prominent node
    gcx0, ghwx0, _ = gaps_x[0]
    gcy0, ghwy0, _ = gaps_y[0]
    xnode = gcx0 - ghwx0
    ynode = gcy0 - ghwy0
    ax.annotate("GALAXY CLUSTER\n(0D fold node\n= max density)",
                xy=(xnode, ynode), xytext=(xnode + 0.15, ynode + 0.15),
                color='white', fontsize=8.5, fontfamily='monospace',
                arrowprops=dict(arrowstyle='->', color='white', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a2040',
                          edgecolor='white', alpha=0.8),
                zorder=7)

    # Snowplow arrow
    ax.annotate("", xy=(0.25, 0.72), xytext=(0.50, 0.72),
                arrowprops=dict(arrowstyle='->', color='#ff4488',
                                lw=2, mutation_scale=12))
    ax.text(0.375, 0.74, "Snowplow\nv_gap = H₀·L_P·φ^(2bz-N)",
            ha='center', va='bottom', color='#ff4488',
            fontsize=7.5, fontfamily='monospace', zorder=7)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        'COSMIC WEB = 2D Cantor Gap Structure  ·  bz = 245\n'
        'Voids (gap interior) → Sheets (2D walls) → Filaments (1D intersections) → '
        'Clusters (0D fold nodes)\n'
        f'W = {W:.4f} gap fraction   |   '
        f'Snowplow amplification: 1.75× per Cantor iteration   |   '
        f'5 iterations → 100× cluster density contrast',
        color='white', fontsize=9.5, fontweight='bold'
    )
    for sp in ax.spines.values():
        sp.set_color('#1a2840')

    if standalone:
        plt.tight_layout()
        out = 'output_fig6_cosmic_web.png'
        plt.savefig(out, dpi=150, facecolor=DARK, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {out}")
    return ax


# ══════════════════════════════════════════════════════════════════════════════
# MASTER FIGURE — ALL SIX PANELS
# ══════════════════════════════════════════════════════════════════════════════

def fig_master(planets):
    """Render all six panels in a single large figure."""
    fig = plt.figure(figsize=(28, 36), facecolor=DARK)
    fig.suptitle(
        'HUSMANN DECOMPOSITION FRAMEWORK — UNIVERSE VISUALIZATION\n'
        f'AAH Hamiltonian α=1/φ, V=2J   ·   W={W:.4f}   ·   φ={PHI:.6f}   ·   '
        f'N={N} brackets   ·   χ²=2.42 (3 dof)   ·   '
        f'Ω_b={OMEGA_B:.3f}  Ω_DM={OMEGA_DM:.3f}  Ω_DE={OMEGA_DE:.3f}',
        color='white', fontsize=13, fontweight='bold', y=0.995
    )

    gs = gridspec.GridSpec(4, 2, figure=fig,
                           hspace=0.35, wspace=0.28,
                           left=0.06, right=0.97,
                           top=0.975, bottom=0.02)

    print("  Panel 1: Spiral map...")
    ax1 = fig.add_subplot(gs[0, :])
    fig_spiral_map(planets, ax=ax1, standalone=False)

    print("  Panel 2: Bracket scale bar...")
    ax2 = fig.add_subplot(gs[1, :])
    fig_bracket_scale(planets, ax=ax2, standalone=False)

    print("  Panel 3: ESI distribution...")
    ax3 = fig.add_subplot(gs[2, 0])
    fig_esi_distribution(planets, ax=ax3, standalone=False)

    print("  Panel 4: Titius-Bode...")
    ax4 = fig.add_subplot(gs[2, 1])
    fig_titius_bode(ax=ax4, standalone=False)

    print("  Panel 5: Zeckendorf heatmap...")
    ax5 = fig.add_subplot(gs[3, 0])
    fig_zeckendorf_heatmap(planets, ax=ax5, standalone=False)

    print("  Panel 6: Cosmic web...")
    ax6 = fig.add_subplot(gs[3, 1])
    fig_cosmic_web(ax=ax6, standalone=False)

    fig.text(0.5, 0.004,
        f'Thomas Husmann · Husmann Decomposition Framework · March 2026   ·   '
        f'{len(planets)} worlds indexed   ·   '
        f'l₀ = {L0_STELLAR_AU} AU = L_P × φ^{BZ_MERCURY} (Mercury orbit, zero free params)   ·   '
        f'v_gap(bz) = H₀·L_P·φ^(2bz-N)   ·   '
        f'github.com/thusmann5327/Unified_Theory_Physics',
        ha='center', va='bottom', color=DIM, fontsize=7.5
    )

    out = '/mnt/user-data/outputs/UNIVERSE_master.png'
    plt.savefig(out, dpi=130, bbox_inches='tight', facecolor=DARK)
    plt.close()
    print(f"  Saved master: {out}")
    return out


# ══════════════════════════════════════════════════════════════════════════════
# TEXT REPORT
# ══════════════════════════════════════════════════════════════════════════════

def print_universe_report(planets):
    """Print a compact text report of all worlds and key framework numbers."""

    def esi_bar(esi):
        n = round(esi * 12)
        return "█" * n + "░" * (12 - n)

    print("\n" + "="*80)
    print("HUSMANN UNIVERSE REPORT")
    print("="*80)
    print(f"φ = {PHI:.8f}   W = {W:.6f}   N = {N}   l₀ = {L0_STELLAR_AU} AU")
    print(f"Unity: 1/φ + 1/φ³ + 1/φ⁴ = {1/PHI + 1/PHI**3 + 1/PHI**4:.8f}")
    print(f"Spiral turns Planck→Hubble: {SPIRAL_TURNS}  (half-turn residual: {HALF_TURN_RES})")
    print(f"Titius-Bode: r(k) = {L0_STELLAR_AU} AU × φ^k  (bz_Mercury = {BZ_MERCURY})")
    print(f"Snowplow amplification (1 iter): {2*W/(1-W):.3f}×")
    print()

    # Summary stats
    by_tier = {}
    for p in planets:
        by_tier.setdefault(p["tier"], []).append(p)

    print(f"{'Tier':12s} {'Count':6s}")
    print("-"*20)
    for tier in ["PRIME", "Habitable", "Marginal", "Hostile", "Extreme"]:
        n = len(by_tier.get(tier, []))
        print(f"{tier:12s} {n:6d}")
    print(f"{'TOTAL':12s} {len(planets):6d}")
    print()

    # Full table
    print(f"{'#':4s} {'Name':22s} {'System':18s} {'bz':4s} "
          f"{'Zeckendorf':22s} {'ESI':6s} {'Tier':10s} {'Dist':12s}")
    print("-"*105)

    for i, p in enumerate(planets, 1):
        z_compact = "{" + ",".join(f"F{k}" for k in p["z_indices"]) + "}"
        print(f"{i:4d} {p['name'][:22]:22s} {p['system'][:18]:18s} "
              f"{p['bz']:4d} {z_compact:22s} {p['esi']:5.2f}  "
              f"{p['tier']:10s} {p['dist_str']}")

    print()
    print("KEY FRAMEWORK RESULTS:")
    print(f"  χ² = 2.42 (3 dof, p=0.49) — cosmological energy budget")
    print(f"  G×m_p²/(k_e×e²) = (1/φ)^172.69 = 8.12×10⁻³⁷ (measured 8.10×10⁻³⁷, 0.22% error)")
    print(f"  Black hole eccentricity: e = √(1−1/φ) = 1/φ = 0.6180 (exact)")
    print(f"  c = 2Jl₀/ℏ = {2*J*1.6e-19*l0/(1.055e-34):.4e} m/s  (actual 3.00×10⁸)")
    print(f"  π = 4·arctan(1/φ) + 4·arctan(1/φ³) (exact identity)")
    print(f"  Titius-Bode mean error: 11% (zero free parameters)")
    print(f"  Simulation: σ 0.722→3.509 (4.86×), void 21%→79%, 100% peak-wall alignment")
    print("="*80)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("UNIVERSE.py — Husmann Decomposition Framework")
    print(f"φ={PHI:.6f}  W={W:.6f}  N={N}")
    print()

    # Build planet database
    print("Building planet database...")
    planets = build_planets()
    print(f"  {len(planets)} worlds indexed")
    print(f"  bz range: {min(p['bz'] for p in planets)}–{max(p['bz'] for p in planets)}")
    print(f"  PRIME targets: {sum(1 for p in planets if p['tier']=='PRIME')}")
    print()

    # Parse arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "report":
        print_universe_report(planets)

    elif mode == "spiral":
        print("Generating spiral map...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_spiral_map(planets)

    elif mode == "scale":
        print("Generating bracket scale bar...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_bracket_scale(planets)

    elif mode == "esi":
        print("Generating ESI distribution...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_esi_distribution(planets)

    elif mode == "tb":
        print("Generating Titius-Bode comparison...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_titius_bode()

    elif mode == "zeck":
        print("Generating Zeckendorf heatmap...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_zeckendorf_heatmap(planets)

    elif mode == "web":
        print("Generating cosmic web schematic...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        fig_cosmic_web()

    else:  # "all" — master figure
        print("Generating master figure (all 6 panels)...")
        os.makedirs('/mnt/user-data/outputs', exist_ok=True)
        print_universe_report(planets)
        out = fig_master(planets)
        print(f"\nDone. Output: {out}")
        print("Usage: python3 UNIVERSE.py [all|report|spiral|scale|esi|tb|zeck|web]")
