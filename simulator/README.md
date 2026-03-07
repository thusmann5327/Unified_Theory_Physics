# Phi-Structured Universe Simulator

**Thomas A. Husmann | iBuilt LTD**
**Version 5.0 | March 2026**

---

## Overview

A Three.js-based visualization of the Husmann Decomposition framework, demonstrating how the golden ratio (φ = 1.618033988749895) structures physical reality from Planck scale to Hubble horizon.

**Live Demo**: [universe.eldon.food](https://universe.eldon.food)

---

## The Three Unity Equations

This simulator unifies three fundamental equations:

### 1. Unity Identity (Matter Partition)
```
1/φ + 1/φ³ + 1/φ⁴ = 1
```
- **1/φ (61.8%)**: Backbone threads flowing toward gravity sources
- **1/φ³ (23.6%)**: V=2J web trapped inside nuclei (dark energy)
- **1/φ⁴ (14.6%)**: Observable collapsed matter

### 2. Boundary Law (Existence Condition)
```
2/φ⁴ + 3/φ³ = 1
```
The V=2J criticality condition at every recursion level. This is the existence threshold - below this, no stable structure forms.

### 3. Wall Fraction (Fine Structure)
```
W = 2/φ⁴ + H/φ³ = 0.467134
α = 1/(N × W) where N = 294 brackets
```
Derives α⁻¹ = 137.30 (0.19% from CODATA 137.036)

---

## Features

### Galaxy Visualization (φ-Spiral Arms)
- Milky Way rendered with golden-angle (137.5°) spiral arms
- Four major arms following logarithmic spiral pattern
- Dark matter halo visualization (1/φ³ trapped web)
- Nearby galaxies (Andromeda, Triangulum, LMC, SMC) at correct bracket positions
- "You Are Here" marker at Sun's position

### Zoom Levels
| Level | Scale | Features |
|-------|-------|----------|
| Universe | 0-294 brackets | Full φ-bracket structure, sector rings |
| Galaxy | 250-280 brackets | Milky Way spiral, nearby galaxies |
| Solar System | 230-250 brackets | Planets in ecliptic plane, golden-angle spacing |
| Planetary | 200-230 brackets | World classification, habitability |
| Geological | 140-170 brackets | Mineral deposits, REE targeting |
| Earth | 163.8 (Brain Hinge) | 4.54 Ga evolution timeline |

### Earth Evolution Timeline
- Interactive slider from formation (4.54 Ga) to present
- Atmosphere color evolution (orange → blue)
- Ocean coverage, O₂/CO₂ levels
- Key epochs: Hadean, Archean, Proterozoic, Phanerozoic
- Faint Young Sun Paradox demonstration

### World Classification
- Formation bracket determines world type
- REE enrichment calculation from Zeckendorf signature
- Habitability scoring relative to Brain Hinge (163.8)
- Geological layer generation

---

## Installation

### Requirements
- Python 3.8+
- Flask
- SQL Server (optional, for persistence)

### Setup
```bash
pip install flask
python app.py
```

Server runs on port 5200 by default.

### Nginx Configuration
```nginx
server {
    listen 443 ssl;
    server_name universe.eldon.food;

    location / {
        proxy_pass http://localhost:5200;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

---

## API Reference

### Constants
```
GET /api/constants     - All φ constants
GET /api/verify        - Verification of identities
```

### Bracket Navigation
```
GET /api/bracket/<n>   - Information for bracket n
GET /api/solar_system  - Solar system with brackets
GET /api/milky_way     - Galactic reference points
```

### World Classification
```
GET /api/worlds                      - All classified worlds
GET /api/worlds/<id>                 - World details
GET /api/worlds/earth-analogues      - Earth-similar worlds
GET /api/worlds/ree-rich             - REE-enriched worlds
POST /api/derive                     - Classify custom world
```

### Earth Evolution
```
GET /api/earth/timeline              - Full timeline
GET /api/earth/epoch/<time>          - State at time
GET /api/earth/climate/<ga>          - Climate model
GET /api/earth/faint-sun-paradox     - Faint sun explanation
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| B | Toggle bracket shells |
| H | Toggle double helix |
| W | Toggle wall layers |
| O | Toggle orbits |
| R | Reset view |
| Space | Play/Pause animation |

---

## Mathematical Foundation

The simulator visualizes the Aubry-André-Harper Hamiltonian at criticality:

```
H = Σᵢ [c†ᵢ cᵢ₊₁ + h.c.] + V Σᵢ cos(2παi + θ) c†ᵢ cᵢ
```

At **V = 2J** and **α = 1/φ**, the spectrum becomes a Cantor set with measure 1/φ⁴.

The observable universe emerges as the "gap" positions in this spectrum, with:
- Planck length at bracket 0
- Hubble horizon at bracket 294
- All physical scales mapping to specific brackets via: `L(n) = Lₚ × φⁿ × C`

---

## License

- **Academic Use**: CC BY-NC-SA 4.0
- **Commercial Use**: Contact Thomas.a.husmann@gmail.com

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
