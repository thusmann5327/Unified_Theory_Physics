# Universe Simulator

Interactive 3D visualization of the Husmann Decomposition framework.

## Live Demo

https://universe.eldon.food

## Features

- **Multi-scale navigation**: Planck scale to Hubble radius (294 φ-brackets)
- **Five-band spectrum**: σ₁ (Matter) → σ₅ (Dark Energy) color-coded shells
- **Unity Triangulation**: Three wave sources creating 3D space
- **Cosmic Web**: Galaxy clusters at interference peaks, filaments from DE+DM correlation
- **Solar System**: Planets with φ-bracket positions
- **Milky Way**: Spiral galaxy with golden-angle arm structure
- **Double Helix**: Backbone threads visualized as cylindrical helix

## Unity Triangulation Visualization

At Universe zoom level, the simulator shows:
- **Three source markers** (S₁, S₂, S₃) at golden-angle separation
- **Triangulation triangle** connecting the sources
- **Galaxy clusters** placed at 3-source interference peaks
- **Cosmic web filaments** weighted by DE+DM pairwise intensity (0.99 correlation)

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

Access at http://localhost:5000

## Key Files

- `app.py` - Flask application server
- `templates/index.html` - Main visualization (Three.js)
- `static/` - CSS and assets
- `BUILD_UNIVERSE.md` - Detailed build documentation

## Physics Constants

From `templates/index.html`:
```javascript
const PHI = 1.6180339887;           // Golden ratio
const BRACKET_COUNT = 294;          // log_φ(L_H/L_P)
const GOLDEN_ANGLE = 137.5077;      // 360°/φ²

// Unity Triangulation Wave Sources
const WAVE_SOURCES = {
  DE: { amplitude: 1/φ,   frequency: φ   },  // Dark Energy
  DM: { amplitude: 1/φ³,  frequency: φ³  },  // Dark Matter
  M:  { amplitude: 1/φ⁴,  frequency: φ⁴  }   // Matter
};
```

---

*Part of the Husmann Decomposition Framework*
*© 2026 Thomas A. Husmann / iBuilt LTD*
