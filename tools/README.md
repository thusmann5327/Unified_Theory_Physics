# Tools — Husmann Decomposition Implementation

Computational tools and modeling scripts for the Husmann Decomposition framework.
These implement the theoretical predictions from `/theory/` as working code.

---

## Files

### Documentation

| File | Description |
|------|-------------|
| [`ATOMIC.md`](ATOMIC.md) | Comprehensive 3D atomic modeling reference — Cantor node architecture for atoms, bond predictions, shell structure |
| [`molecules.md`](molecules.md) | Molecular geometry predictions — 25 molecules, 34 bonds, 17 angles at 1.4% mean error |
| [`microtubules.md`](microtubules.md) | Microtubule superradiance framework — bundle percolation, GABA gate, proof scorecard |
| [`quantum.md`](quantum.md) | Quantum mechanics applications of the Cantor vacuum structure |
| [`crystal.md`](crystal.md) | *(Placeholder — crystal structure predictions, in progress)* |

### Code

| File | Description |
|------|-------------|
| [`gaba_engine.py`](gaba_engine.py) | GABA neurotransmitter simulation engine v4 — anesthetic DFT proxy, bundle percolation, proof status |
| [`MolecuBOT.py`](MolecuBOT.py) | Molecular structure modeling — ZeckyBOT-derived bond length and angle predictions |
| [`crystal.py`](crystal.py) | Crystal structure predictor using baryonic electron model and metallic mean lattices |

---

## Key Results (March 2026)

- **Molecular geometry**: 1.4% mean error across 25 molecules, zero free parameters
- **Bundle percolation**: T(13,golden) = 0.361 > p_c = 0.347 — 13-PF is the ONLY MT geometry that percolates
- **GABA gate**: ΔE = 18.47 meV matches Craddock 10–25 meV range (Proof 4 RESOLVED)
- **Dephasing rate**: γ = 2.57×10¹²/s from φ alone (zero free parameters)

---

## Dependencies

```
numpy, scipy, matplotlib
```

## Related

- Theory: [`/theory/atomic.md`](/theory/atomic.md), [`/theory/Entanglement.md`](/theory/Entanglement.md)
- Verification: [`/verification/`](/verification/)
- Parent engine: [`/algorithms/UNIVERSE.py`](/algorithms/UNIVERSE.py)

---

*Husmann Decomposition — One Axiom: φ² = φ + 1*
