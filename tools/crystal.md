# Crystal Structure Analysis Tool

Documentation for `crystal.py` — the element-to-metallic-mean mapping engine.

## What crystal.py Does

Analyzes crystal structure parameters (c/a ratios, packing fractions, rhombohedral angles) for all elements and maps them to metallic mean complements (1 − α) via the rule established in `theory/cosmic_nesting.md` §4.

## Key Results

- Mercury (Hg): encodes Silver mean to **0.006%** via 1/(c/a)_hex
- Rhenium (Re): encodes Gold mean to **0.16%** via a/(a+c) HCP
- All FCC metals: encode Bronze mean to **1.42%** via 1/√2
- Every metallic mean n=1–8 has at least one element match below 2%

## Usage

```python
python3 crystal.py
```

See `theory/cosmic_nesting.md` §4 (Element Analysis) for the full theoretical derivation.
See `tools/ATOMIC.md` for 3D modeling applications.

---

*© 2026 Thomas A. Husmann / iBuilt LTD*
