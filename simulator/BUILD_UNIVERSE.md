# BUILD_UNIVERSE.md - Phi-Structured Universe Simulator

Complete documentation for rebuilding the Phi-Structured Universe Simulator from scratch.

**Version**: 2.0 (March 6, 2026)
**Location**: https://universe.eldon.food

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Mathematical Framework](#mathematical-framework)
3. [Infrastructure Setup](#infrastructure-setup)
4. [Backend Implementation](#backend-implementation)
5. [Frontend Implementation](#frontend-implementation)
6. [API Reference](#api-reference)
7. [Feature Modules](#feature-modules)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## System Overview

### Purpose
A 3D interactive visualization of the Husmann Decomposition Framework - a phi-based model of physical scales from Planck length to cosmic structures, with applications for:
- Understanding condensation sequences in protoplanetary disks
- Classifying worlds by formation bracket and derived properties
- Visualizing Earth's evolution with solar/tectonic models
- Identifying REE-rich worlds and habitable zone planets

### Technology Stack
- **Backend**: Python 3.10+, Flask
- **Frontend**: Three.js (r128), vanilla JavaScript
- **Database**: MS SQL Server (optional, for state persistence)
- **Web Server**: Nginx reverse proxy + Flask development server
- **Deployment**: Systemd service on GCP VM

### File Structure
```
/var/www/universe.eldon.food/
├── app.py                  # Flask backend (main application)
├── BUILD_UNIVERSE.md       # This file
├── requirements.txt        # Python dependencies
├── venv/                   # Python virtual environment
├── static/                 # Static assets (CSS, images)
└── templates/
    └── index.html          # Main Three.js visualization
```

---

## Mathematical Framework

### Core Constants

```python
# Golden Ratio
PHI = (1 + sqrt(5)) / 2  # 1.6180339887...

# Powers
PHI2 = PHI * PHI         # 2.6180339887...
PHI3 = PHI2 * PHI        # 4.2360679774...
PHI4 = PHI3 * PHI        # 6.8541019662...

# Inverse powers
INV_PHI = 1 / PHI        # 0.6180339887...
INV_PHI2 = 1 / PHI2      # 0.3819660112...
INV_PHI3 = 1 / PHI3      # 0.2360679774...
INV_PHI4 = 1 / PHI4      # 0.1459155902...

# Golden Angle
GOLDEN_ANGLE = 360 / PHI2  # 137.5077640500° degrees

# Self-referential hinge constant
HINGE_CONST = PHI ** (-1/PHI)  # 0.7427429446...

# Wall fraction (three-layer wall impedance)
WALL_FRACTION = 2 * INV_PHI4 + HINGE_CONST / PHI3  # 0.467134
```

### Unity Equation (Must Equal 1.0)
```
1/phi^4 + 1/phi^3 + 1/phi = 1.0000000000000000
```

### Master Coupling Equation
```
alpha_eff = 1 / (N * W)

Where:
  N = 294 brackets
  W = WALL_FRACTION = 0.467134

Result: alpha_eff = 1/137.38 (error: 0.19% from CODATA)
```

### Bracket Scale Function
```python
def bracket_scale(n):
    """Physical scale at bracket n in meters"""
    L_PLANCK = 1.616255e-35      # Planck length
    CALIB_FACTOR = 1.0224065900  # Calibrated so n=128 = 9.3 nm
    return L_PLANCK * (PHI ** n) * CALIB_FACTOR
```

### Five Sectors
```
N = 294 total brackets

Sector widths:
  sigma1 = N / PHI^4 = 42.9 brackets (matter endpoint)
  sigma2 = N / PHI^3 = 69.4 brackets (conduit)
  sigma3 = N / PHI^3 = 69.4 brackets (conduit, contains element condensation)
  sigma4 = N / PHI^3 = 69.4 brackets (conduit)
  sigma5 = N / PHI^4 = 42.9 brackets (matter endpoint)

Key boundaries:
  sigma1_end = 42.9
  sigma2_end = 112.3
  sigma3_end = 181.7
  sigma4_end = 251.1
  sigma5_end = 294
```

### Key Hinges
```
proton_hinge = sigma1_end + sigma2_width * HINGE_CONST = 94.4
brain_hinge  = sigma2_end + sigma2_width * HINGE_CONST = 163.8
oort_hinge   = sigma3_end + sigma2_width * HINGE_CONST = 233.2
```

### Condensation Zones (sigma3, brackets 140-150)
```
Zone                 Bracket    Temp(K)    Elements
────────────────────────────────────────────────────
PGM Refractory       141.5-142.2   1700-1900   Os, W, Re, Ir, Ru
HREE Peak            142.2-142.3   1650-1700   Lu, Sc, Y, Tb (950× solar)
Refractory Hosts     142.2-142.4   1500-1653   Al, Ti, Ca
LREE Zone            142.3-142.7   1356-1602   Nd, Sm, Pr, La, Ce
SILICATE CLIFF       142.63-142.7  1350-1400   REE crashes from 950× to 1.6×
Moderate Volatile    142.7-144.1   600-1300    Cr, Mn, K, Na, Cu, S
Major Silicates      144.1-146.8   182-600     Mg, Si, Fe (rocky planets)
ICE LINE             146.8         182         H2O ice (rocky vs icy boundary)
Volatile Zone        147.5+        <150        C, N, noble gases
```

### REE Targeting Signature
```
Zeckendorf decomposition containing {89, 34, 13} indicates REE deposits
Example: bracket 142 = {89, 34, 13, 5, 1} ✓ contains REE signature
```

---

## Infrastructure Setup

### System Requirements
```bash
# Ubuntu 22.04 LTS
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip nginx certbot

# Create application directory
sudo mkdir -p /var/www/universe.eldon.food
sudo chown $USER:$USER /var/www/universe.eldon.food
```

### Python Environment
```bash
cd /var/www/universe.eldon.food

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask
pip install pymssql  # Optional: for MS SQL persistence

# Create requirements.txt
pip freeze > requirements.txt
```

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/universe.eldon.food

server {
    listen 80;
    server_name universe.eldon.food;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name universe.eldon.food;

    ssl_certificate /etc/letsencrypt/live/universe.eldon.food/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/universe.eldon.food/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:5200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeout for long requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /var/www/universe.eldon.food/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/universe.eldon.food /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL certificate
sudo certbot --nginx -d universe.eldon.food
```

### Systemd Service
```ini
# /etc/systemd/system/universe-simulator.service

[Unit]
Description=Phi-Structured Universe Simulator
After=network.target

[Service]
Type=simple
User=farmfreshbooks
WorkingDirectory=/var/www/universe.eldon.food
Environment="PATH=/var/www/universe.eldon.food/venv/bin"
ExecStart=/var/www/universe.eldon.food/venv/bin/python app.py
Restart=always
RestartSec=5
MemoryMax=1G
CPUQuota=75%

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable universe-simulator
sudo systemctl start universe-simulator
```

---

## Backend Implementation

### Core app.py Structure

```python
"""
PHI-STRUCTURED UNIVERSE SIMULATOR
Husmann Decomposition Framework
"""

from flask import Flask, render_template, jsonify, request
import math
import json
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# ═══════════════════════════════════════════════
# PHI CONSTANTS
# ═══════════════════════════════════════════════
PHI = (1 + math.sqrt(5)) / 2
# ... (all constants as defined in Mathematical Framework)

# ═══════════════════════════════════════════════
# SOLAR EVOLUTION & STELLAR PHYSICS
# ═══════════════════════════════════════════════
L_SUN_TODAY = 3.828e26      # Watts
SOLAR_AGE_GYR = 4.57        # Gyrs

def solar_luminosity_at_time(time_ga):
    """Solar luminosity at time_ga before present (0.70-1.0)"""
    if time_ga <= 0: return 1.0
    if time_ga >= SOLAR_AGE_GYR: return 0.70
    t_fraction = (SOLAR_AGE_GYR - time_ga) / SOLAR_AGE_GYR
    return 0.70 + 0.30 * t_fraction

def equilibrium_temperature(distance_au, luminosity_ratio=1.0, albedo=0.3):
    """Equilibrium temp without greenhouse"""
    # ... implementation

def greenhouse_temperature(T_eq, co2_percent, ch4_ppm=0, h2o_relative=1.0):
    """Surface temp with greenhouse warming"""
    # ... implementation

# ═══════════════════════════════════════════════
# TECTONIC VIABILITY MODEL
# ═══════════════════════════════════════════════
def radioactive_heat_at_time(time_ga, ree_enrichment=1.0):
    """Radioactive heat vs present (isotope decay)"""
    # ... implementation

def tectonic_vigor(radius_km, mass_ratio_earth, time_ga, ree_enrichment, water_fraction):
    """Tectonic vigor index 0-1"""
    # ... implementation

def carbon_silicate_cycle_rate(tectonic_vigor, temperature_K, co2_partial_pressure):
    """Carbon-silicate weathering cycle rates"""
    # ... implementation

# ═══════════════════════════════════════════════
# WORLD CLASSIFICATION SHORTCUTS
# ═══════════════════════════════════════════════
def formation_bracket(r_AU, star_luminosity_ratio=1.0):
    """Formation bracket from orbital position"""
    T_disk = disk_temperature(r_AU, star_luminosity_ratio)
    return temp_to_bracket(T_disk)

def ree_enrichment_factor(formation_bracket):
    """REE enrichment based on formation bracket"""
    SILICATE_CLIFF = 142.65
    REE_PEAK_BRACKET = 142.21
    if formation_bracket <= REE_PEAK_BRACKET:
        return 950.0  # Peak enrichment
    elif formation_bracket <= SILICATE_CLIFF:
        # Steep decline across cliff
        t = (formation_bracket - REE_PEAK_BRACKET) / (SILICATE_CLIFF - REE_PEAK_BRACKET)
        return 950.0 * (1 - t) + 1.6 * t
    else:
        return max(1.0, 1.6 - 0.1 * (formation_bracket - SILICATE_CLIFF))

def habitability_score(world_data):
    """Composite habitability (0-100)"""
    # ... implementation

def derive_planet_properties(planet_data, star_luminosity_ratio=1.0):
    """Master function: derive all properties from orbital data"""
    # ... implementation

# ═══════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════

SOLAR_SYSTEM = {
    'mercury': {'distance_au': 0.387, 'radius_km': 2439.7, ...},
    'venus': {'distance_au': 0.723, 'radius_km': 6051.8, ...},
    'earth': {'distance_au': 1.0, 'radius_km': 6371, ...},
    # ...
}

EXOPLANETS = {
    'proxima_b': {'a_AU': 0.0485, 'radius_km': 7160, 'star_luminosity_ratio': 0.0017, ...},
    'trappist_1e': {'a_AU': 0.029, 'radius_km': 5850, 'star_luminosity_ratio': 0.00055, ...},
    # ...
}

EARTH_TIMELINE = {
    'hadean_formation': {'time_ga': 4.54, 'name': 'Earth Formation', ...},
    'archean_life': {'time_ga': 3.5, 'name': 'First Life', ...},
    'goe': {'time_ga': 2.4, 'name': 'Great Oxygenation Event', ...},
    # ...
}

CONDENSATION_ZONES = {
    'hree_peak': {'bracket_range': [142.2, 142.3], 'elements': ['Lu', 'Sc', 'Y', ...], ...},
    'silicate_cliff': {'bracket_range': [142.63, 142.7], ...},
    # ...
}

# ═══════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════

@app.route('/')
def index():
    initial_data = {
        'phi': PHI,
        'solar_system': SOLAR_SYSTEM,
        'earth_timeline': EARTH_TIMELINE,
        # ...
    }
    return render_template('index.html', data=initial_data)

# World endpoints
@app.route('/api/worlds')
@app.route('/api/worlds/<world_id>')
@app.route('/api/worlds/<world_id>/layers')
@app.route('/api/worlds/search', methods=['POST'])
@app.route('/api/worlds/earth-analogues')
@app.route('/api/worlds/ree-rich')
@app.route('/api/worlds/habitable-zone')

# Earth evolution endpoints
@app.route('/api/earth/timeline')
@app.route('/api/earth/climate/<float:time_ga>')
@app.route('/api/earth/solar-evolution')
@app.route('/api/earth/tectonics/<float:time_ga>')
@app.route('/api/earth/faint-sun-paradox')

# Utility endpoints
@app.route('/api/compare-worlds', methods=['GET', 'POST'])
@app.route('/api/condensation-zones')
@app.route('/api/derive', methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)
```

---

## Frontend Implementation

### Three.js Visualization Structure

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="app">
        <div id="hud"><!-- Heads-up display --></div>
        <div id="controls"><!-- Control panel --></div>
        <div id="world-finder"><!-- World search UI --></div>
        <div id="world-detail"><!-- Selected world details --></div>
    </div>

    <script>
        // Constants from server
        const PHI = {{ data.phi }};
        const SOLAR_SYSTEM = {{ data.solar_system | tojson }};
        const EARTH_TIMELINE = {{ data.earth_timeline | tojson }};

        // Three.js setup
        let scene, camera, renderer, controls;

        function init() {
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 2000);
            renderer = new THREE.WebGLRenderer({ antialias: true });
            controls = new THREE.OrbitControls(camera, renderer.domElement);

            // Build visualizations
            buildStarfield();
            buildBracketShells();
            buildDoubleHelix();
            buildSolarSystem();
            buildEarthEvolutionSphere();

            animate();
        }

        // Key visualization functions
        function buildBracketShells() { /* 98 icosahedron shells */ }
        function buildDoubleHelix() { /* Golden angle DNA helix */ }
        function buildSolarSystem() { /* Planets in ecliptic plane */ }
        function buildCondensationZones() { /* Element zones in sigma3 */ }
        function buildMineralDeposits() { /* REE deposits on Earth sphere */ }
        function buildEarthEvolutionSphere() { /* Time-evolving Earth */ }
        function buildGeologicalCrossSection() { /* Layer visualization */ }

        // Zoom levels
        const ZOOM_LEVELS = {
            0: 'Universe',
            1: 'Galaxy',
            2: 'Solar System',
            3: 'Planetary',
            4: 'Geological',
            5: 'Earth Evolution'
        };

        // World Finder API integration
        async function loadAllWorlds() {
            const response = await fetch('/api/worlds');
            const data = await response.json();
            worldsData = Object.entries(data.worlds).map(([id, world]) => ({id, ...world}));
        }

        async function loadGeologicalLayers(worldId) {
            const response = await fetch(`/api/worlds/${worldId}/layers`);
            const data = await response.json();
            renderLayerVisualization(data.layers);
        }
    </script>
</body>
</html>
```

---

## API Reference

### World Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/worlds` | GET | All worlds with derived properties |
| `/api/worlds/<id>` | GET | Single world details |
| `/api/worlds/<id>/layers` | GET | Geological layers |
| `/api/worlds/search` | POST | Custom criteria search |
| `/api/worlds/earth-analogues` | GET | Earth-like worlds |
| `/api/worlds/ree-rich` | GET | High REE enrichment worlds |
| `/api/worlds/habitable-zone` | GET | Rocky habitable zone worlds |
| `/api/compare-worlds` | GET/POST | Compare two worlds |

### Earth Evolution Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/earth/timeline` | GET | Full evolution timeline |
| `/api/earth/climate/<time_ga>` | GET | Climate state at time |
| `/api/earth/solar-evolution` | GET | Solar luminosity over time |
| `/api/earth/tectonics/<time_ga>` | GET | Tectonic state at time |
| `/api/earth/faint-sun-paradox` | GET | Explanation + scenarios |

### Example Responses

```json
// GET /api/worlds/earth
{
    "name": "Earth",
    "a_AU": 1.0,
    "formation_bracket": 144.21,
    "formation_temp_K": 632.46,
    "ree_enrichment": 1.44,
    "habitability_score": 100,
    "brain_hinge_offset": 35.19,
    "world_type": "rocky_standard",
    "system": "Solar System"
}

// GET /api/earth/climate/4.0
{
    "time_ga": 4.0,
    "solar_luminosity_ratio": 0.74,
    "T_equilibrium_K": 234.5,
    "T_surface_K": 310.2,
    "co2_percent": 30.0,
    "tectonic_vigor": 0.85,
    "habitable": true,
    "faint_sun_problem": true,
    "greenhouse_compensation_K": 75.7
}
```

---

## Feature Modules

### 1. Solar Evolution Model

**The Faint Young Sun Problem:**
- At formation (4.57 Ga), Sun was 70% as bright
- Earth should have been frozen, but had liquid water by 4.2 Ga

**Solution: Greenhouse + Tectonics**
```
1. High CO2/CH4 provided greenhouse warming
2. Carbon-silicate cycle (requires tectonics) stabilizes climate
3. Weathering rate: increases with T and CO2
4. Volcanism rate: proportional to tectonic vigor
5. Net effect: thermostat keeps climate stable
```

### 2. Tectonic Viability Model

**Requirements for tectonics:**
- Size: 5000-8000 km radius (optimal)
- Internal heat: radioactive decay from U, Th, K
- Water: lubricates subduction zones
- Formation bracket: 143-146 (rocky with heat sources)

**Radioactive heat over time:**
```
Half-lives: U238=4.47Gyr, U235=0.704Gyr, Th232=14.0Gyr, K40=1.25Gyr
At 4.0 Ga: ~3× present radioactive heat production
```

### 3. World Classification Shortcuts

**Formation bracket determines everything:**
```python
def derive_planet_properties(planet_data, star_luminosity_ratio):
    bracket = formation_bracket(planet_data['a_AU'], star_luminosity_ratio)

    return {
        'formation_bracket': bracket,
        'ree_enrichment': ree_enrichment_factor(bracket),
        'world_type': classify_world_type(bracket),
        'habitability_score': habitability_score(planet_data),
        'brain_hinge_offset': abs(orbital_bracket - 163.8)
    }
```

**World types by bracket:**
```
< 142.5:  ultra_refractory (Mercury-like, high refractories)
142.5-143.5: rocky_enriched (high REE potential)
143.5-147: rocky_standard (Earth/Mars/Venus)
147-150: ice_giant (Uranus/Neptune)
> 150: volatile_rich (comets, KBOs)
```

### 4. Geological Layer Generation

```python
def generate_geological_layers(world_id):
    world = WORLDS_DERIVED.get(world_id)
    bracket = world['formation_bracket']

    layers = [
        {'name': 'Inner Core', 'bracket': 143.5, 'composition': 'Solid Fe-Ni'},
        {'name': 'Outer Core', 'bracket': 143.5, 'composition': 'Liquid Fe-Ni'},
        {'name': 'Lower Mantle', 'bracket': 142.65, 'composition': 'Perovskite'},
        {'name': 'Upper Mantle', 'bracket': 142.67, 'composition': 'Olivine'},
        {'name': 'Crust', 'bracket': 142.7, 'composition': 'Granite/Basalt'},
    ]

    # Scale by planet size
    # Add REE enrichment to crust
    return layers
```

---

## Deployment

### Restart Service
```bash
sudo systemctl restart universe-simulator
sudo systemctl status universe-simulator
```

### View Logs
```bash
sudo journalctl -u universe-simulator -f
```

### Test API
```bash
curl http://localhost:5200/api/worlds | head -c 500
curl http://localhost:5200/api/earth/climate/4.0
curl http://localhost:5200/api/earth/faint-sun-paradox
```

### Full Rebuild
```bash
cd /var/www/universe.eldon.food
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart universe-simulator
```

---

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u universe-simulator -n 50
# Check for Python syntax errors
python3 -m py_compile app.py
```

### 502 Bad Gateway
```bash
# Check if Flask is running
curl http://localhost:5200/
# Check nginx config
sudo nginx -t
```

### Memory issues
```bash
# Service is limited to 1GB
# Check usage
systemctl status universe-simulator
```

---

## Changelog

### v2.1 (March 6, 2026)
- Fixed greenhouse model calibration (present-day = 288K)
- Model now correctly shows Faint Young Sun compensation:
  - 4.0 Ga: 74% solar → 66K greenhouse → 302K surface
  - Present: 100% solar → 33K greenhouse → 288K surface

### v2.0 (March 6, 2026)
- Added solar evolution model (faint young sun)
- Added tectonic viability calculations
- Added carbon-silicate cycle modeling
- Added integrated Earth climate model
- Added world finder UI with geological layers
- Added world comparison feature

### v1.0 (Initial)
- Basic phi-framework implementation
- Three.js visualization
- Earth timeline
- Condensation zones
- Mineral deposits

---

*Generated by Claude Code | Last updated: March 6, 2026*
