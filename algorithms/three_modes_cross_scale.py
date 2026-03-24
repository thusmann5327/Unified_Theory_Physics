#!/usr/bin/env python3
"""
three_modes_cross_scale.py
==========================
Tests whether the three quantized silver-vertex θ values from the Bigollo
atomic scatter plot predict structure ratios at stellar, planetary, and
galactic scales via Cantor node self-similarity.

Backend: JAX-Metal (Apple GPU) when available, else CPU JAX, else NumPy.
"""

import json, os, itertools, math, time
from pathlib import Path

# ── Backend selection ────────────────────────────────────────────────────────
try:
    import jax
    import jax.numpy as jnp
    from jax import jit
    _devs = jax.devices()
    BACKEND = "JAX-Metal" if any("METAL" in str(d).upper() for d in _devs) else "JAX-CPU"
    np = jnp                       # use jax arrays everywhere possible
    _jax = True
    print(f"[backend] {BACKEND}  devices={_devs}")
except Exception as exc:
    import numpy as jnp
    np = jnp
    BACKEND = "NumPy"
    _jax = False
    print(f"[backend] NumPy fallback ({exc})")

import numpy as onp                # always available for I/O / indexing

# ── Husmann Decomposition constants ──────────────────────────────────────────
PHI       = 1.6180339887
SQRT_PHI  = math.sqrt(PHI)          # 1.2720
H         = PHI ** (-1.0 / PHI)     # 0.7427  (hinge)
W         = 0.4671
BOS       = 0.9920
R_C       = 1.0 - 1.0 / PHI**4     # 0.8541

# Cantor node positions
SIGMA = {"σ₃": 0.0728, "σ₂": 0.2350, "cos(1/φ)": 0.3672,
         "σ_wall": 0.3972, "σ₄": 0.5594}

# Three quantized θ values (atomic scatter)
THETA = {"leak": 0.564, "rc": 0.854, "baseline": 1.000}

# Derived quantized ratios: ratio = √(1 + (θ × BOS)²)
QRATIO = {k: math.sqrt(1.0 + (v * BOS)**2) for k, v in THETA.items()}
# leak→1.146, rc→1.311, baseline→1.409

MULTIPLIERS = {"1": 1.0, "√φ": SQRT_PHI, "φ": PHI, "H": H}

# ── Helpers ──────────────────────────────────────────────────────────────────

def flag(pct):
    pct = abs(pct)
    if pct < 1.0:   return "EXACT  (<1%)"
    if pct < 5.0:   return "STRONG (<5%)"
    if pct < 10.0:  return "NOTABLE(<10%)"
    return ""

def pct_err(pred, obs):
    return 100.0 * abs(pred - obs) / obs if obs != 0 else 999.0

def section(title):
    bar = "=" * 72
    print(f"\n{bar}\n  TEST: {title}\n{bar}")

# Accumulator for all matches across tests
all_matches = []

# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 1 — STELLAR TACHOCLINE
# ═══════════════════════════════════════════════════════════════════════════════
def test1_stellar():
    section("1 — STELLAR TACHOCLINE")

    targets = {"Sun tachocline": 0.713,
               "M-dwarf conv base (low)": 0.30,
               "M-dwarf conv base (high)": 0.35,
               "Red giant conv base (low)": 0.10,
               "Red giant conv base (high)": 0.20}

    sigma_keys = list(SIGMA.keys())
    sigma_vals = list(SIGMA.values())
    theta_keys = list(THETA.keys())
    theta_vals = list(THETA.values())
    mult_keys  = list(MULTIPLIERS.keys())
    mult_vals  = list(MULTIPLIERS.values())

    # Build all 60 products  (5 σ × 3 θ × 4 mult)
    combos = []
    for si, sk in enumerate(sigma_keys):
        for ti, tk in enumerate(theta_keys):
            for mi, mk in enumerate(mult_keys):
                val = sigma_vals[si] * theta_vals[ti] * mult_vals[mi]
                combos.append((val, sk, tk, mk))

    results = {}
    for tname, tval in targets.items():
        hits = []
        for val, sk, tk, mk in combos:
            err = pct_err(val, tval)
            f = flag(err)
            if f:
                hits.append({"combo": f"{sk}×θ_{tk}×{mk}",
                             "predicted": round(val, 5),
                             "observed": tval,
                             "error_pct": round(err, 3),
                             "flag": f})
        hits.sort(key=lambda x: x["error_pct"])
        results[tname] = hits

        print(f"\n  Target: {tname} = {tval}")
        if hits:
            for h in hits:
                print(f"    {h['flag']}  {h['combo']:36s}  pred={h['predicted']:.5f}  err={h['error_pct']:.3f}%")
                all_matches.append({"test": "T1-stellar", "target": tname, **h})
        else:
            print("    (no match < 10%)")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 2 — PLANETARY ORBITAL RATIOS
# ═══════════════════════════════════════════════════════════════════════════════
def test2_planetary():
    section("2 — PLANETARY ORBITAL RATIOS")

    systems = {
        "Planets (AU)": [("Mercury", 0.387), ("Venus", 0.723), ("Earth", 1.000),
                         ("Mars", 1.524), ("Jupiter", 5.203), ("Saturn", 9.537),
                         ("Uranus", 19.19), ("Neptune", 30.07)],
        "Jovian moons (Mkm)": [("Io", 0.4216), ("Europa", 0.6709),
                                ("Ganymede", 1.0704), ("Callisto", 1.8827)],
        "Saturnian moons (Mkm)": [("Mimas", 0.1855), ("Enceladus", 0.2380),
                                   ("Tethys", 0.2947), ("Dione", 0.3774),
                                   ("Rhea", 0.5271), ("Titan", 1.2218)],
    }

    # Pre-compute basis logs for grid search
    bases = [QRATIO["leak"], QRATIO["rc"], QRATIO["baseline"], PHI]
    log_bases = onp.array([math.log(b) for b in bases])

    a_range = list(range(-2, 3))   # a,b,c ∈ {-2..2}
    d_range = list(range(-3, 4))   # d ∈ {-3..3}

    # Build exponent grid  (5^3 × 7 = 875 combos)
    exponents = onp.array(list(itertools.product(a_range, a_range, a_range, d_range)),
                          dtype=onp.float32)                          # (N,4)
    # Products via log: prod = exp(exponents @ log_bases)
    log_products = exponents @ log_bases                              # (N,)
    products = onp.exp(log_products)

    results = {}
    for sname, bodies in systems.items():
        print(f"\n  System: {sname}")
        consec_ratios = []
        for i in range(len(bodies) - 1):
            r = bodies[i+1][1] / bodies[i][1]
            consec_ratios.append((f"{bodies[i+1][0]}/{bodies[i][0]}", r))

        sys_results = []
        for rname, rval in consec_ratios:
            diffs = onp.abs(products - rval)
            best_idx = int(onp.argmin(diffs))
            best_prod = float(products[best_idx])
            best_exp  = exponents[best_idx].astype(int).tolist()
            err = pct_err(best_prod, rval)
            f = flag(err)
            entry = {"pair": rname, "observed_ratio": round(rval, 5),
                     "best_fit": round(best_prod, 5),
                     "exponents_abcd": best_exp,
                     "error_pct": round(err, 3), "flag": f}
            sys_results.append(entry)
            tag = f or "---"
            exp_str = f"a={best_exp[0]:+d} b={best_exp[1]:+d} c={best_exp[2]:+d} d={best_exp[3]:+d}"
            print(f"    {tag:14s}  {rname:22s}  obs={rval:.4f}  fit={best_prod:.4f}  err={err:.3f}%  [{exp_str}]")
            if f:
                all_matches.append({"test": "T2-planetary", "system": sname, **entry})

        results[sname] = sys_results
    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 3 — GALAXY STRUCTURE RATIOS
# ═══════════════════════════════════════════════════════════════════════════════
def test3_galaxy():
    section("3 — GALAXY STRUCTURE RATIOS")

    galaxies = {
        "Milky Way":  {"bulge_kpc": 1.0, "disk_kpc": 2.6, "halo_kpc": 200.0},
        "M31":        {"bulge_kpc": 1.5, "disk_kpc": 5.3, "halo_kpc": 250.0},
    }

    extra_ratios = {"NFW r_s/r_vir": 0.1}

    # Build product table: every pair (σ_i × θ_j) plus triple (σ_i × θ_j × mult)
    sigma_vals = list(SIGMA.values())
    sigma_keys = list(SIGMA.keys())
    theta_vals = list(THETA.values())
    theta_keys = list(THETA.keys())
    mult_keys  = list(MULTIPLIERS.keys())
    mult_vals  = list(MULTIPLIERS.values())

    prod_table = []
    # Two-factor: σ × θ
    for si, sk in enumerate(sigma_keys):
        for ti, tk in enumerate(theta_keys):
            v = sigma_vals[si] * theta_vals[ti]
            prod_table.append((v, f"{sk}×θ_{tk}"))
    # Three-factor: σ × θ × mult
    for si, sk in enumerate(sigma_keys):
        for ti, tk in enumerate(theta_keys):
            for mi, mk in enumerate(mult_keys):
                if mk == "1":
                    continue  # already covered
                v = sigma_vals[si] * theta_vals[ti] * mult_vals[mi]
                prod_table.append((v, f"{sk}×θ_{tk}×{mk}"))
    # Also powers of σ: σ^2, σ×σ' etc
    for si, sk in enumerate(sigma_keys):
        for sj, sk2 in enumerate(sigma_keys):
            v = sigma_vals[si] * sigma_vals[sj]
            prod_table.append((v, f"{sk}×{sk2}"))

    # Gather target ratios
    target_ratios = {}
    for gname, gd in galaxies.items():
        target_ratios[f"{gname} bulge/disk"] = gd["bulge_kpc"] / gd["disk_kpc"]
        target_ratios[f"{gname} disk/halo"]  = gd["disk_kpc"] / gd["halo_kpc"]
        target_ratios[f"{gname} bulge/halo"] = gd["bulge_kpc"] / gd["halo_kpc"]
    target_ratios.update(extra_ratios)

    results = {}
    for tname, tval in target_ratios.items():
        hits = []
        for pval, plabel in prod_table:
            err = pct_err(pval, tval)
            f = flag(err)
            if f:
                hits.append({"combo": plabel, "predicted": round(pval, 5),
                             "observed": round(tval, 5),
                             "error_pct": round(err, 3), "flag": f})
        hits.sort(key=lambda x: x["error_pct"])
        results[tname] = hits

        print(f"\n  Target: {tname} = {tval:.5f}")
        if hits:
            for h in hits[:8]:
                print(f"    {h['flag']:14s}  {h['combo']:36s}  pred={h['predicted']:.5f}  err={h['error_pct']:.3f}%")
                all_matches.append({"test": "T3-galaxy", "target": tname, **h})
        else:
            print("    (no match < 10%)")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 4 — THREE-FORCE MAPPING
# ═══════════════════════════════════════════════════════════════════════════════
def test4_forces():
    section("4 — THREE-FORCE MAPPING")

    # θ pairwise ratios
    theta_ratios = {
        "θ_base/θ_leak": THETA["baseline"] / THETA["leak"],
        "θ_rc/θ_leak":   THETA["rc"] / THETA["leak"],
        "θ_base/θ_rc":   THETA["baseline"] / THETA["rc"],
    }

    # φ powers to compare
    phi_powers = {}
    for n in onp.arange(-3, 4, 0.5):
        label = f"φ^({n:+.1f})" if n != int(n) else f"φ^({int(n):+d})"
        phi_powers[label] = PHI ** n

    print("\n  θ pairwise ratios vs φ powers:")
    force_results = {}
    for rname, rval in theta_ratios.items():
        best_label, best_val, best_err = None, None, 999
        for pl, pv in phi_powers.items():
            e = pct_err(pv, rval)
            if e < best_err:
                best_label, best_val, best_err = pl, pv, e
        f = flag(best_err)
        entry = {"ratio": rname, "value": round(rval, 5),
                 "closest_phi_power": best_label,
                 "phi_value": round(best_val, 5),
                 "error_pct": round(best_err, 3), "flag": f}
        force_results[rname] = entry
        print(f"    {f or '---':14s}  {rname:20s} = {rval:.5f}  ≈ {best_label} = {best_val:.5f}  err={best_err:.3f}%")
        if f:
            all_matches.append({"test": "T4-forces", **entry})

    # Coupling constant test
    print("\n  Coupling constant connections:")
    alpha_em = 1.0 / 137.036
    alpha_w  = 1.0 / 30.0
    alpha_s  = 1.0

    nw_product = 294 * W
    nw_err = pct_err(nw_product, 137.036)
    f_nw = flag(nw_err)
    print(f"    {f_nw or '---':14s}  N×W = 294×{W} = {nw_product:.4f}  vs 137.036  err={nw_err:.3f}%")
    if f_nw:
        all_matches.append({"test": "T4-forces", "target": "N×W≈137",
                            "predicted": round(nw_product, 4),
                            "observed": 137.036,
                            "error_pct": round(nw_err, 3), "flag": f_nw})

    # Check α_W/α_EM = 137/30 ≈ 4.567 vs θ products
    aw_over_em = 137.036 / 30.0
    # Try θ products
    theta_prods = {}
    for t1n, t1v in THETA.items():
        for t2n, t2v in THETA.items():
            theta_prods[f"θ_{t1n}×θ_{t2n}"] = t1v * t2v
            theta_prods[f"θ_{t1n}/θ_{t2n}"] = t1v / t2v
            theta_prods[f"(θ_{t1n}×θ_{t2n})×φ"] = t1v * t2v * PHI
            theta_prods[f"(θ_{t1n}/θ_{t2n})×φ"] = t1v / t2v * PHI

    coupling_targets = {"α_W/α_EM (≈137/30)": aw_over_em,
                        "α_S/α_W (≈30)": 30.0,
                        "α_S/α_EM (≈137)": 137.036}

    print("\n  θ-product fits to coupling ratios:")
    coupling_results = {}
    for cname, cval in coupling_targets.items():
        best_label, best_val, best_err = None, None, 999
        for tl, tv in theta_prods.items():
            e = pct_err(tv, cval)
            if e < best_err:
                best_label, best_val, best_err = tl, tv, e
        f = flag(best_err)
        entry = {"target": cname, "value": round(cval, 4),
                 "closest_theta_prod": best_label,
                 "theta_value": round(best_val, 5),
                 "error_pct": round(best_err, 3), "flag": f}
        coupling_results[cname] = entry
        print(f"    {f or '---':14s}  {cname:25s} = {cval:.4f}  ≈ {best_label} = {best_val:.5f}  err={best_err:.3f}%")
        if f:
            all_matches.append({"test": "T4-forces", **entry})

    return {"theta_vs_phi": force_results, "NxW": round(nw_product, 4),
            "coupling": coupling_results}


# ═══════════════════════════════════════════════════════════════════════════════
#  TEST 5 — JAX OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════
def test5_optimization():
    section("5 — JAX OPTIMIZATION")

    if not _jax:
        print("  [skip] JAX not available; cannot run gradient optimization.")
        return {"status": "skipped"}

    import jax
    import jax.numpy as jnp
    from jax import grad

    # ── Observed targets ─────────────────────────────────────────────────────
    tachocline_obs = 0.713
    planet_axes = onp.array([0.387, 0.723, 1.000, 1.524, 5.203, 9.537, 19.19, 30.07])
    planet_ratios_np = planet_axes[1:] / planet_axes[:-1]
    log_planet_targets = onp.log(planet_ratios_np)
    mw_bd = 1.0 / 2.6

    sigma_arr = jnp.array(list(SIGMA.values()))        # (5,)
    mult_arr  = jnp.array(list(MULTIPLIERS.values()))   # (4,)

    log_phi_val = float(math.log(PHI))
    bos_f = float(BOS)

    # Pre-build exponent grid for planetary fit (vectorized, no Python loops in trace)
    # a ∈ {-2..2}, d ∈ {-2..2}, qr_index ∈ {0,1,2}  → 5×5×3 = 75 combos
    a_grid = onp.arange(-2, 3, dtype=onp.float32)       # (5,)
    d_grid = onp.arange(-2, 3, dtype=onp.float32)       # (5,)
    q_idx  = onp.arange(3, dtype=onp.int32)              # (3,)
    # Meshgrid: (5,5,3) each
    A, D, Q = onp.meshgrid(a_grid, d_grid, q_idx, indexing='ij')
    exp_a = jnp.array(A.reshape(-1))     # (75,)
    exp_d = jnp.array(D.reshape(-1))     # (75,)
    exp_q = jnp.array(Q.reshape(-1).astype(onp.int32))  # (75,)

    log_targets_jnp = jnp.array(log_planet_targets.astype(onp.float32))  # (7,)

    def loss_fn(params):
        t1, t2, t3 = params[0], params[1], params[2]
        thetas = jnp.stack([t1, t2, t3])

        qr = jnp.sqrt(1.0 + (thetas * bos_f)**2)  # (3,)
        log_qr = jnp.log(qr)                       # (3,)

        # ── Stellar loss: best σ×θ×mult ≈ 0.713
        products = sigma_arr[:, None, None] * thetas[None, :, None] * mult_arr[None, None, :]
        stellar_loss = jnp.min((products - tachocline_obs)**2)

        # ── Planetary loss (fully vectorized)
        # log_pred = a * log_qr[q] + d * log_phi  for each of 75 combos
        log_preds = exp_a * log_qr[exp_q] + exp_d * log_phi_val  # (75,)
        # For each of 7 planet ratios, find min squared distance over 75 combos
        diffs = (log_preds[None, :] - log_targets_jnp[:, None])**2  # (7, 75)
        planet_loss = jnp.sum(jnp.min(diffs, axis=1))

        # ── Galaxy loss: some σ×θ product ≈ MW bulge/disk
        gal_products = sigma_arr[:, None] * thetas[None, :]  # (5,3)
        gal_loss = jnp.min((gal_products - mw_bd)**2)

        # ── Force loss: θ_base/θ_leak ≈ φ^(1/3)
        ratio_bl = t3 / t1
        force_loss = (ratio_bl - PHI**(1.0/3.0))**2

        total = stellar_loss + 0.1 * planet_loss + gal_loss + force_loss
        return total

    # ── Adam optimizer (manual) ──────────────────────────────────────────────
    params = jnp.array([0.564, 0.854, 1.000])
    lr = 0.001
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    m = jnp.zeros(3)
    v = jnp.zeros(3)

    grad_fn = jax.grad(loss_fn)

    # Warm up JIT
    print("  [JIT compiling loss + grad on Metal...]")
    _ = grad_fn(params)
    print("  [JIT done]")

    print(f"\n  {'Epoch':>6s}  {'θ_leak':>8s}  {'θ_rc':>8s}  {'θ_base':>8s}  {'Loss':>12s}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*12}")

    history = []
    for epoch in range(2001):
        g = grad_fn(params)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g**2
        m_hat = m / (1 - beta1**(epoch+1))
        v_hat = v / (1 - beta2**(epoch+1))
        params = params - lr * m_hat / (jnp.sqrt(v_hat) + eps)

        if epoch % 200 == 0:
            l = float(loss_fn(params))
            p = [float(x) for x in params]
            print(f"  {epoch:6d}  {p[0]:8.5f}  {p[1]:8.5f}  {p[2]:8.5f}  {l:12.6f}")
            history.append({"epoch": epoch, "params": p, "loss": l})

    final = [float(x) for x in params]
    init  = [0.564, 0.854, 1.000]
    shifts = [abs(f - i) for f, i in zip(final, init)]
    print(f"\n  Initial : {init}")
    print(f"  Final   : [{final[0]:.5f}, {final[1]:.5f}, {final[2]:.5f}]")
    print(f"  Shift   : [{shifts[0]:.5f}, {shifts[1]:.5f}, {shifts[2]:.5f}]")

    # Interpret convergence
    converged_to = []
    framework = {"σ₃": 0.0728, "σ₂": 0.2350, "cos(1/φ)": 0.3672,
                 "σ_wall": 0.3972, "σ₄": 0.5594, "W": W, "H": H,
                 "r_c": R_C, "BOS": BOS, "1/φ": 1/PHI, "1/φ²": 1/PHI**2,
                 "φ^(1/3)": PHI**(1/3)}
    for i, name in enumerate(["θ_leak", "θ_rc", "θ_baseline"]):
        best_match, best_err = None, 999
        for cname, cval in framework.items():
            e = pct_err(final[i], cval)
            if e < best_err:
                best_match, best_err = cname, e
        if best_err < 10:
            converged_to.append(f"{name}→{best_match} (err {best_err:.2f}%)")
            print(f"  {name} near {best_match} = {framework[best_match]:.5f} (err {best_err:.2f}%)")

    stayed = all(s < 0.05 for s in shifts)
    print(f"\n  Verdict: {'Parameters STAYED at atomic values (shifts < 0.05)' if stayed else 'Parameters SHIFTED — see convergence targets above.'}")

    return {"initial": init, "final": [round(x, 5) for x in final],
            "shifts": [round(x, 5) for x in shifts],
            "stayed": stayed, "converged_to": converged_to,
            "history": history}


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN — RUN ALL TESTS, SCORECARD, SAVE JSON
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    t0 = time.time()
    print(f"Three-Mode Cross-Scale Prediction Test")
    print(f"{'='*72}")
    print(f"  φ = {PHI},  √φ = {SQRT_PHI:.4f},  H = {H:.4f}")
    print(f"  θ values   : {THETA}")
    print(f"  Q-ratios   : { {k: round(v,4) for k,v in QRATIO.items()} }")
    print(f"  Cantor σ   : {SIGMA}")
    print(f"  W = {W}, BOS = {BOS}, r_c = {R_C:.4f}")

    r1 = test1_stellar()
    r2 = test2_planetary()
    r3 = test3_galaxy()
    r4 = test4_forces()
    r5 = test5_optimization()

    # ── SCORECARD ────────────────────────────────────────────────────────────
    bar = "=" * 72
    print(f"\n{bar}\n  COMBINED SCORECARD\n{bar}")

    exact   = [m for m in all_matches if "EXACT" in m.get("flag", "")]
    strong  = [m for m in all_matches if "STRONG" in m.get("flag", "")]
    notable = [m for m in all_matches if "NOTABLE" in m.get("flag", "")]

    sub5 = exact + strong
    print(f"  EXACT   (<1%) : {len(exact)}")
    print(f"  STRONG  (<5%) : {len(strong)}")
    print(f"  NOTABLE (<10%): {len(notable)}")
    print(f"  ─────────────────────────")
    print(f"  Total cross-scale predictions < 5%: {len(sub5)}")
    print(f"  Total matches < 10%: {len(all_matches)}")

    if sub5:
        print(f"\n  Top <5% matches:")
        for m in sorted(sub5, key=lambda x: x.get("error_pct", 999)):
            test = m.get("test", "?")
            tgt  = m.get("target", m.get("pair", m.get("ratio", "?")))
            comb = m.get("combo", m.get("closest_phi_power", m.get("closest_theta_prod", "?")))
            err  = m.get("error_pct", "?")
            print(f"    [{test}] {tgt:35s}  {comb:36s}  err={err}%")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.2f}s   Backend: {BACKEND}")

    # ── SAVE JSON ────────────────────────────────────────────────────────────
    out_dir = Path("/Users/universe/Unified_Theory_Physics/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "three_modes_cross_scale.json"

    # Convert numpy types for JSON serialization
    def sanitize(obj):
        if isinstance(obj, (onp.integer,)):
            return int(obj)
        if isinstance(obj, (onp.floating, float)):
            return round(float(obj), 6)
        if isinstance(obj, onp.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize(x) for x in obj]
        return obj

    payload = {
        "backend": BACKEND,
        "constants": {"phi": PHI, "sqrt_phi": round(SQRT_PHI, 4),
                      "H": round(H, 4), "W": W, "BOS": BOS,
                      "r_c": round(R_C, 4)},
        "theta_values": THETA,
        "quantized_ratios": {k: round(v, 4) for k, v in QRATIO.items()},
        "test1_stellar": sanitize(r1),
        "test2_planetary": sanitize(r2),
        "test3_galaxy": sanitize(r3),
        "test4_forces": sanitize(r4),
        "test5_optimization": sanitize(r5),
        "scorecard": {
            "exact_count": len(exact),
            "strong_count": len(strong),
            "notable_count": len(notable),
            "total_sub5pct": len(sub5),
            "total_sub10pct": len(all_matches),
        },
        "all_matches": sanitize(all_matches),
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"\n  Results saved → {out_path}")


if __name__ == "__main__":
    main()
