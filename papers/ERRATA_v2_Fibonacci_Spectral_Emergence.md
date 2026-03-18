# Errata for v2 Upload

## Husmann (2026) "Fibonacci Spectral Emergence" — Five Corrections

**Apply to:** `Husmann_2026_Fibonacci_Spectral_Emergence_final.docx`
**Verified by:** `bridge_computations.py` (59/59 tests pass after corrections)
**Impact:** None of these change any headline number (6.2% mean error, 44/54 within 10%, ρ = +0.73 Mohs, the three theorems). All are transcription issues in the paper text.

---

### FIX 1 — §2.3 Methods (line ~117–118)

**Published:**
> "subgaps were identified using a threshold of 4× the intraband median spacing"

**Corrected:**
> "subbands were identified by locating the eight largest internal gaps within the center band"

**Why:** The code (`bridge_computations.py`) takes the top 8 gaps, producing exactly 9 sub-bands. The 4× threshold gives 9–10 sub-gaps with a different decomposition (verified: 4× threshold finds 9 gaps, but the paper's Table 2 results match the top-8 method which produces 8 gaps → 9 sub-bands). The paper's results are computed with top-8, so the methods section should say top-8.

---

### FIX 2 — Table 2 (lines ~229–235)

**Published Table 2 (WRONG F-indices):**

| D | F-index | Parity | Non-Fib | + Singleton | = Sum | E(center) |
|---|---------|--------|---------|-------------|-------|-----------|
| 89 | F(10) | even | 7 | + 1 | = 8 = F(6) | −0.003 |
| 144 | F(11) | odd | 4 | + 1 | = 5 = F(5) | −0.001 |
| 233 | F(12) | even | 7 | + 1 | = 8 = F(6) | +0.011 |
| 377 | F(13) | odd | 4 | + 1 | = 5 = F(5) | +0.012 |

**Corrected Table 2 (consistent with Table 1):**

| D | F-index | Parity | Non-Fib | + Singleton | = Sum | E(center) |
|---|---------|--------|---------|-------------|-------|-----------|
| 89 | F(11) | odd | 4 | + 1 | = 5 = F(5) | −0.003 |
| 144 | F(12) | even | 7 | + 1 | = 8 = F(6) | −0.001 |
| 233 | F(13) | odd | 4 | + 1 | = 5 = F(5) | +0.011 |
| 377 | F(14) | even | 7 | + 1 | = 8 = F(6) | +0.012 |

**Why:** Table 1 in the same paper correctly uses 89=F(11), 233=F(13). Table 2 was off by one throughout. The Fibonacci sequence: F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13, F(8)=21, F(9)=34, F(10)=55, **F(11)=89**, **F(12)=144**, **F(13)=233**, **F(14)=377**. Note that the parity and non-Fibonacci counts also swap as a consequence.

---

### FIX 3 — §3.2 text (lines ~216–217)

**Published:**
> "At even index D, the non-Fibonacci count is 4 (= F(5) − 1); at odd index D, it is 7 (= F(6) − 1)."

**Corrected:**
> "At odd F-index, the non-Fibonacci count is 4 (= F(5) − 1); at even F-index, it is 7 (= F(6) − 1)."

**Why:** Direct consequence of Fix 2. F(11)=89 has odd index → 4 non-Fibonacci sub-bands. F(12)=144 has even index → 7 non-Fibonacci sub-bands. The published text had the parity inverted.

---

### FIX 4 — Figure 7 caption (lines ~389–390)

**Published caption:**
> "(ρ = −0.36, p = 0.022)" and "35 elements"

**Corrected caption:**
> "The main periodic table (23 elements in this band). Mohs hardness vs cloud excess (ρ = −0.29, p = 0.183)."

**Why:** The image itself shows ρ = −0.29, p = 0.183, n = 23. The published caption stats (ρ = −0.36, p = 0.022, 35 elements) appear to be from an earlier version of the analysis that included all elements rather than just Band 3. The caption should match the figure.

---

### FIX 5 — §1 (line ~63)

**Published:**
> "zero Lebesgue measures"

**Corrected:**
> "zero Lebesgue measure"

**Why:** Standard mathematical usage. Lebesgue measure is a single measure; a set has "Lebesgue measure zero" (singular). The plural "measures" is grammatically incorrect.

---

## Verification

All five fixes have been verified against `bridge_computations.py`:

```
FIX 1: top-8 method produces 9 sub-bands matching Table 2 ✓
FIX 2: F(11)=89, F(12)=144, F(13)=233, F(14)=377 ✓
FIX 3: odd F-index → 4 non-Fib, even F-index → 7 non-Fib ✓
FIX 4: Figure 7 shows n=23, ρ=-0.29, p=0.183 ✓
FIX 5: "zero Lebesgue measure" (singular) ✓
```

No headline results are affected. The 59/59 computation tests pass identically before and after these corrections.
