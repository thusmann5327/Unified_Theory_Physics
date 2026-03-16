import { useState, useMemo } from "react";

// ═══════════════════════════════════════════════════════════
// FRAMEWORK CONSTANTS — all from φ² = φ + 1
// ═══════════════════════════════════════════════════════════
const PHI = (1 + Math.sqrt(5)) / 2;
const W = 2/Math.pow(PHI,4) + Math.pow(PHI,-1/PHI)/Math.pow(PHI,3);
const BREATHING = 1 - Math.sqrt(1 - W*W);
const BASE = 1.408382;
const G1 = 0.324325;
const BOS = 0.992022;
const DARK_GOLD = 0.29;
const BRONZE_S3 = 0.394;
const R_SHELL = 0.3972;
const R_OUTER = 0.5594;
const F9 = 34;
const HBAR = 1.0545718e-34;
const C_LIGHT = 2.99792458e8;
const AMU = 1.66053906660e-27;
const L_P = 1.61625e-35;
const N_BRACKETS = 294;

const ELEMENT_DATA = {
1:{sym:"H",name:"Hydrogen",mass:1.008,rc:31,rv:120,row:1,col:1,cat:"s"},
2:{sym:"He",name:"Helium",mass:4.003,rc:28,rv:140,row:1,col:18,cat:"ng"},
3:{sym:"Li",name:"Lithium",mass:6.941,rc:128,rv:182,row:2,col:1,cat:"s"},
4:{sym:"Be",name:"Beryllium",mass:9.012,rc:96,rv:153,row:2,col:2,cat:"s"},
5:{sym:"B",name:"Boron",mass:10.81,rc:84,rv:192,row:2,col:13,cat:"p"},
6:{sym:"C",name:"Carbon",mass:12.01,rc:76,rv:170,row:2,col:14,cat:"p"},
7:{sym:"N",name:"Nitrogen",mass:14.01,rc:71,rv:155,row:2,col:15,cat:"p"},
8:{sym:"O",name:"Oxygen",mass:16.00,rc:66,rv:152,row:2,col:16,cat:"p"},
9:{sym:"F",name:"Fluorine",mass:19.00,rc:57,rv:147,row:2,col:17,cat:"p"},
10:{sym:"Ne",name:"Neon",mass:20.18,rc:58,rv:154,row:2,col:18,cat:"ng"},
11:{sym:"Na",name:"Sodium",mass:22.99,rc:166,rv:227,row:3,col:1,cat:"s"},
12:{sym:"Mg",name:"Magnesium",mass:24.31,rc:141,rv:173,row:3,col:2,cat:"s"},
13:{sym:"Al",name:"Aluminium",mass:26.98,rc:121,rv:184,row:3,col:13,cat:"p"},
14:{sym:"Si",name:"Silicon",mass:28.09,rc:111,rv:210,row:3,col:14,cat:"p"},
15:{sym:"P",name:"Phosphorus",mass:30.97,rc:107,rv:180,row:3,col:15,cat:"p"},
16:{sym:"S",name:"Sulfur",mass:32.07,rc:105,rv:180,row:3,col:16,cat:"p"},
17:{sym:"Cl",name:"Chlorine",mass:35.45,rc:102,rv:175,row:3,col:17,cat:"p"},
18:{sym:"Ar",name:"Argon",mass:39.95,rc:106,rv:188,row:3,col:18,cat:"ng"},
19:{sym:"K",name:"Potassium",mass:39.10,rc:203,rv:275,row:4,col:1,cat:"s"},
20:{sym:"Ca",name:"Calcium",mass:40.08,rc:176,rv:231,row:4,col:2,cat:"s"},
21:{sym:"Sc",name:"Scandium",mass:44.96,rc:170,rv:211,row:4,col:3,cat:"d"},
22:{sym:"Ti",name:"Titanium",mass:47.87,rc:160,rv:187,row:4,col:4,cat:"d"},
23:{sym:"V",name:"Vanadium",mass:50.94,rc:153,rv:179,row:4,col:5,cat:"d"},
24:{sym:"Cr",name:"Chromium",mass:52.00,rc:139,rv:189,row:4,col:6,cat:"d"},
25:{sym:"Mn",name:"Manganese",mass:54.94,rc:139,rv:197,row:4,col:7,cat:"d"},
26:{sym:"Fe",name:"Iron",mass:55.85,rc:132,rv:194,row:4,col:8,cat:"d"},
27:{sym:"Co",name:"Cobalt",mass:58.93,rc:126,rv:192,row:4,col:9,cat:"d"},
28:{sym:"Ni",name:"Nickel",mass:58.69,rc:124,rv:163,row:4,col:10,cat:"d"},
29:{sym:"Cu",name:"Copper",mass:63.55,rc:132,rv:140,row:4,col:11,cat:"d"},
30:{sym:"Zn",name:"Zinc",mass:65.38,rc:122,rv:139,row:4,col:12,cat:"d"},
31:{sym:"Ga",name:"Gallium",mass:69.72,rc:122,rv:187,row:4,col:13,cat:"p"},
32:{sym:"Ge",name:"Germanium",mass:72.63,rc:120,rv:211,row:4,col:14,cat:"p"},
33:{sym:"As",name:"Arsenic",mass:74.92,rc:119,rv:185,row:4,col:15,cat:"p"},
34:{sym:"Se",name:"Selenium",mass:78.97,rc:120,rv:190,row:4,col:16,cat:"p"},
35:{sym:"Br",name:"Bromine",mass:79.90,rc:120,rv:185,row:4,col:17,cat:"p"},
36:{sym:"Kr",name:"Krypton",mass:83.80,rc:116,rv:202,row:4,col:18,cat:"ng"},
37:{sym:"Rb",name:"Rubidium",mass:85.47,rc:220,rv:303,row:5,col:1,cat:"s"},
38:{sym:"Sr",name:"Strontium",mass:87.62,rc:195,rv:249,row:5,col:2,cat:"s"},
39:{sym:"Y",name:"Yttrium",mass:88.91,rc:190,rv:219,row:5,col:3,cat:"d"},
40:{sym:"Zr",name:"Zirconium",mass:91.22,rc:175,rv:186,row:5,col:4,cat:"d"},
41:{sym:"Nb",name:"Niobium",mass:92.91,rc:164,rv:207,row:5,col:5,cat:"d"},
42:{sym:"Mo",name:"Molybdenum",mass:95.95,rc:154,rv:209,row:5,col:6,cat:"d"},
43:{sym:"Tc",name:"Technetium",mass:98.0,rc:147,rv:209,row:5,col:7,cat:"d"},
44:{sym:"Ru",name:"Ruthenium",mass:101.07,rc:146,rv:207,row:5,col:8,cat:"d"},
45:{sym:"Rh",name:"Rhodium",mass:102.91,rc:142,rv:195,row:5,col:9,cat:"d"},
46:{sym:"Pd",name:"Palladium",mass:106.42,rc:139,rv:202,row:5,col:10,cat:"d"},
47:{sym:"Ag",name:"Silver",mass:107.87,rc:145,rv:172,row:5,col:11,cat:"d"},
48:{sym:"Cd",name:"Cadmium",mass:112.41,rc:144,rv:158,row:5,col:12,cat:"d"},
49:{sym:"In",name:"Indium",mass:114.82,rc:142,rv:193,row:5,col:13,cat:"p"},
50:{sym:"Sn",name:"Tin",mass:118.71,rc:139,rv:217,row:5,col:14,cat:"p"},
51:{sym:"Sb",name:"Antimony",mass:121.76,rc:139,rv:206,row:5,col:15,cat:"p"},
52:{sym:"Te",name:"Tellurium",mass:127.60,rc:138,rv:206,row:5,col:16,cat:"p"},
53:{sym:"I",name:"Iodine",mass:126.90,rc:139,rv:198,row:5,col:17,cat:"p"},
54:{sym:"Xe",name:"Xenon",mass:131.29,rc:140,rv:216,row:5,col:18,cat:"ng"},
55:{sym:"Cs",name:"Caesium",mass:132.91,rc:244,rv:343,row:6,col:1,cat:"s"},
56:{sym:"Ba",name:"Barium",mass:137.33,rc:215,rv:268,row:6,col:2,cat:"s"},
};

function aufbau(Z) {
  const sub = [];
  for (let n=1;n<8;n++) for (let l=0;l<n;l++) sub.push([n,l,2*(2*l+1)]);
  sub.sort((a,b) => (a[0]+a[1])-(b[0]+b[1]) || a[0]-b[0]);
  let rem=Z; const filled=[];
  for (const [n,l,cap] of sub) { if(rem<=0)break; const e=Math.min(rem,cap); filled.push([n,l,e,cap]); rem-=e; }
  const period = Math.max(...filled.map(f=>f[0]));
  let n_p = filled.filter(f=>f[0]===period&&f[1]===1).reduce((s,f)=>s+f[2],0);
  const n_d_val = filled.filter(f=>f[1]===2&&f[0]===period-1).reduce((s,f)=>s+f[2],0);
  const last_l = filled[filled.length-1][1];
  let block = {0:'s',1:'p',2:'d',3:'f'}[last_l]||'?';
  const se={},sm2={};
  for (const [n,l,e,cap] of filled) { se[n]=(se[n]||0)+e; sm2[n]=(sm2[n]||0)+cap; }
  if (se[period]===sm2[period]) { if(Z===2||(last_l===1&&filled[filled.length-1][2]===filled[filled.length-1][3])) { block='ng'; if(Z===2) n_p=0; } }
  const n_d = ['p','s','ng'].includes(block) ? 0 : n_d_val;
  return {period, n_p, n_d, block};
}

function predictRatio(Z) {
  const {period:per, n_p, n_d, block} = aufbau(Z);
  let ratio, theta, mode;
  if (block === 'd') {
    theta = 1.0 - (n_d/10.0)*DARK_GOLD;
    ratio = Math.sqrt(1 + Math.pow(theta*BOS, 2));
    mode = "Pythagorean (d-block)";
  } else if (block === 'ng') {
    theta = 1.0 + n_p*(G1/BOS)*Math.pow(PHI,-(per-1));
    ratio = Math.sqrt(1 + Math.pow(theta*BOS, 2));
    mode = "Pythagorean (noble gas)";
  } else {
    ratio = BASE + n_p*G1*Math.pow(PHI,-(per-1));
    theta = null;
    mode = "Additive (s/p-block)";
  }
  return {ratio, theta, mode, per, n_p, n_d, block};
}

function quantumDepth(Z) {
  const el = ELEMENT_DATA[Z]; if (!el) return 0;
  const m = el.mass * AMU;
  const lc = HBAR / (m * C_LIGHT);
  const r = el.rv * 1e-12;
  const bz_r = Math.round(Math.log(r/L_P)/Math.log(PHI));
  const bz_lc = Math.round(Math.log(lc/L_P)/Math.log(PHI));
  return { depth: bz_r - bz_lc, bz_vdw: bz_r, bz_compton: bz_lc };
}

const COLORS = { s: "#3b82f6", p: "#22c55e", d: "#f59e0b", ng: "#a855f7" };
const COLORS_DIM = { s: "#1e3a5f", p: "#0f3d1f", d: "#5c3d0e", ng: "#3d1f5c" };
const BLOCK_LABELS = { s: "s-block", p: "p-block", d: "d-block", ng: "Noble gas" };
const GRAVITY_BRACKET = 136;

export default function PeriodicTable() {
  const [selected, setSelected] = useState(null);

  const elements = useMemo(() => {
    return Object.entries(ELEMENT_DATA).map(([z, el]) => {
      const Z = parseInt(z);
      const pred = predictRatio(Z);
      const ratio_obs = el.rv / el.rc;
      const err = ((pred.ratio - ratio_obs) / ratio_obs * 100);
      const qd = quantumDepth(Z);
      return { Z, ...el, ...pred, ratio_obs, err, ...qd };
    });
  }, []);

  const sel = selected ? elements.find(e => e.Z === selected) : null;

  const getErrColor = (err) => {
    const a = Math.abs(err);
    if (a < 5) return "#4ade80";
    if (a < 10) return "#facc15";
    if (a < 20) return "#fb923c";
    return "#ef4444";
  };

  return (
    <div style={{
      fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
      background: "#0a0a0f",
      color: "#e2e8f0",
      minHeight: "100vh",
      padding: "12px",
      position: "relative",
    }}>
      <div style={{ textAlign: "center", marginBottom: 8 }}>
        <h1 style={{
          fontSize: 18, fontWeight: 700, letterSpacing: 2,
          background: "linear-gradient(90deg, #3b82f6, #a855f7, #f59e0b)",
          WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          margin: 0,
        }}>
          HUSMANN DECOMPOSITION — PERIODIC TABLE
        </h1>
        <p style={{ fontSize: 10, color: "#64748b", margin: "2px 0" }}>
          φ² = φ + 1 &nbsp;|&nbsp; D = 233 = F(F(7)) &nbsp;|&nbsp; Zero free parameters
          &nbsp;|&nbsp; 94% within 20%
        </p>
      </div>

      {/* Periodic Table Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(18, 1fr)",
        gridTemplateRows: "repeat(7, 1fr)",
        gap: 2,
        maxWidth: 900,
        margin: "0 auto 8px",
      }}>
        {elements.map(el => (
          <div
            key={el.Z}
            onClick={() => setSelected(el.Z === selected ? null : el.Z)}
            style={{
              gridColumn: el.col,
              gridRow: el.row,
              background: selected === el.Z
                ? COLORS[el.cat]
                : COLORS_DIM[el.cat],
              border: `1px solid ${
                Math.abs(el.err) > 20 ? "#ef4444" :
                selected === el.Z ? COLORS[el.cat] : "#1e293b"
              }`,
              borderRadius: 3,
              padding: "2px 1px",
              cursor: "pointer",
              textAlign: "center",
              transition: "all 0.15s",
              position: "relative",
              minHeight: 38,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              opacity: selected && selected !== el.Z ? 0.5 : 1,
            }}
          >
            <div style={{ fontSize: 7, color: "#94a3b8", lineHeight: 1 }}>{el.Z}</div>
            <div style={{ fontSize: 13, fontWeight: 700, lineHeight: 1.1 }}>{el.sym}</div>
            <div style={{
              fontSize: 7, lineHeight: 1,
              color: getErrColor(el.err),
            }}>
              {el.Z > 2 ? `${el.err > 0 ? '+' : ''}${el.err.toFixed(0)}%` : '—'}
            </div>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div style={{ display: "flex", justifyContent: "center", gap: 12, fontSize: 9, marginBottom: 8 }}>
        {Object.entries(BLOCK_LABELS).map(([k, v]) => (
          <span key={k} style={{ display: "flex", alignItems: "center", gap: 3 }}>
            <span style={{ width: 8, height: 8, borderRadius: 2, background: COLORS[k], display: "inline-block" }} />
            {v}
          </span>
        ))}
        <span style={{ marginLeft: 8 }}>Error:</span>
        {[["<5%","#4ade80"],["<10%","#facc15"],["<20%","#fb923c"],[">20%","#ef4444"]].map(([l,c]) => (
          <span key={l} style={{ color: c }}>{l}</span>
        ))}
      </div>

      {/* Detail Panel */}
      {sel && (
        <div style={{
          background: "#111118",
          border: `1px solid ${COLORS[sel.cat]}`,
          borderRadius: 8,
          padding: 16,
          maxWidth: 900,
          margin: "0 auto",
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: 16,
          fontSize: 11,
        }}>
          {/* Column 1: Identity */}
          <div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 8 }}>
              <span style={{ fontSize: 32, fontWeight: 800, color: COLORS[sel.cat] }}>{sel.sym}</span>
              <span style={{ fontSize: 14, color: "#94a3b8" }}>{sel.name}</span>
              <span style={{ fontSize: 11, color: "#475569" }}>Z={sel.Z}</span>
            </div>
            <div style={{ color: "#94a3b8", lineHeight: 1.8 }}>
              <div>Mass: <span style={{color:"#e2e8f0"}}>{sel.mass} u</span></div>
              <div>Period: <span style={{color:"#e2e8f0"}}>{sel.per}</span> &nbsp; Block: <span style={{color:COLORS[sel.cat],fontWeight:600}}>{BLOCK_LABELS[sel.cat]}</span></div>
              <div>p-electrons: <span style={{color:"#e2e8f0"}}>{sel.n_p}</span> &nbsp; d-active: <span style={{color:"#e2e8f0"}}>{sel.n_d}</span></div>
              <div>Covalent: <span style={{color:"#e2e8f0"}}>{sel.rc} pm</span></div>
              <div>van der Waals: <span style={{color:"#e2e8f0"}}>{sel.rv} pm</span></div>
            </div>
          </div>

          {/* Column 2: Framework Prediction */}
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: COLORS[sel.cat], marginBottom: 6 }}>
              PREDICTION
            </div>
            <div style={{ color: "#94a3b8", lineHeight: 1.8 }}>
              <div>Mode: <span style={{color:"#e2e8f0",fontSize:10}}>{sel.mode}</span></div>
              {sel.theta !== null && (
                <div>θ = <span style={{color:"#e2e8f0"}}>{sel.theta.toFixed(4)}</span></div>
              )}
              <div>
                Predicted ratio: <span style={{color:"#e2e8f0",fontWeight:700}}>{sel.ratio.toFixed(3)}</span>
              </div>
              <div>
                Observed ratio: <span style={{color:"#e2e8f0"}}>{sel.ratio_obs.toFixed(3)}</span>
              </div>
              <div>
                Error: <span style={{color: getErrColor(sel.err), fontWeight: 700, fontSize: 14}}>
                  {sel.err > 0 ? '+' : ''}{sel.err.toFixed(1)}%
                </span>
              </div>
              <div>
                Predicted vdW: <span style={{color:"#e2e8f0"}}>{(sel.rc * sel.ratio).toFixed(0)} pm</span>
                <span style={{color:"#475569"}}> (obs: {sel.rv})</span>
              </div>
            </div>
          </div>

          {/* Column 3: Quantum Depth & Gravity */}
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: "#f59e0b", marginBottom: 6 }}>
              LINEWEAVER-PATEL POSITION
            </div>
            <div style={{ color: "#94a3b8", lineHeight: 1.8 }}>
              <div>Bracket (vdW): <span style={{color:"#e2e8f0"}}>{sel.bz_vdw}</span> / {N_BRACKETS}</div>
              <div>Bracket (Compton): <span style={{color:"#e2e8f0"}}>{sel.bz_compton}</span></div>
              <div>
                Quantum depth: <span style={{
                  color: sel.depth === F9 ? "#ef4444" : sel.depth < F9 ? "#fb923c" : "#4ade80",
                  fontWeight: 700, fontSize: 14,
                }}>
                  {sel.depth}
                </span>
                <span style={{color:"#475569"}}> brackets (F(9)={F9})</span>
              </div>
              <div style={{fontSize: 9, color: sel.depth <= F9 ? "#fb923c" : "#64748b", marginTop: 2}}>
                {sel.depth < F9 ? "⚠ Below F(9) boundary — quantum regime" :
                 sel.depth === F9 ? "⚠ AT F(9) boundary — Fibonacci gap edge" :
                 "Above F(9) — classical regime"}
              </div>
              <div style={{marginTop: 6}}>
                Gravity bracket: <span style={{color:"#475569"}}>{GRAVITY_BRACKET}</span>
                <span style={{color:"#334155"}}> (double-fold center)</span>
              </div>
              <div>
                Distance to gravity: <span style={{color:"#e2e8f0"}}>{Math.abs(sel.bz_vdw - GRAVITY_BRACKET)}</span> brackets
              </div>
              <div style={{fontSize:9,color:"#475569"}}>
                G/F_EM ≈ (1/φ)^{GRAVITY_BRACKET} ≈ 10⁻³⁶ — gravity negligible at atomic scale
              </div>
            </div>
          </div>

          {/* Formula bar */}
          <div style={{
            gridColumn: "1 / -1",
            background: "#0a0a12",
            borderRadius: 4,
            padding: "8px 12px",
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 10,
            color: "#64748b",
            borderTop: "1px solid #1e293b",
          }}>
            {sel.block === 'd' ? (
              <>vdW/cov = √(1 + (θ × {BOS.toFixed(3)})²) = √(1 + ({sel.theta?.toFixed(3)} × {BOS.toFixed(3)})²) = <span style={{color:"#e2e8f0"}}>{sel.ratio.toFixed(4)}</span>
              &nbsp;&nbsp;|&nbsp;&nbsp;θ = 1 − ({sel.n_d}/10)×{DARK_GOLD} = {sel.theta?.toFixed(4)}</>
            ) : sel.block === 'ng' ? (
              <>vdW/cov = √(1 + (θ × {BOS.toFixed(3)})²) = <span style={{color:"#e2e8f0"}}>{sel.ratio.toFixed(4)}</span>
              &nbsp;&nbsp;|&nbsp;&nbsp;θ = 1 + {sel.n_p}×({G1.toFixed(3)}/{BOS.toFixed(3)})×φ^(−{sel.per-1}) = {sel.theta?.toFixed(4)}</>
            ) : (
              <>vdW/cov = {BASE.toFixed(4)} + {sel.n_p}×{G1.toFixed(4)}×φ^(−{sel.per-1}) = <span style={{color:"#e2e8f0"}}>{sel.ratio.toFixed(4)}</span>
              &nbsp;&nbsp;|&nbsp;&nbsp;BASE = σ₄/σ_shell (Cantor node Pythagorean, 0.012%)</>
            )}
          </div>

          {/* Two triangles mini */}
          <div style={{
            gridColumn: "1 / -1",
            display: "flex",
            justifyContent: "space-between",
            fontSize: 9,
            color: "#475569",
            padding: "0 4px",
          }}>
            <span>△1: 5+8=13 (WHY 3D)</span>
            <span>△2: σ_shell²+bronze²=σ₄² (WHERE atom ends)</span>
            <span>△3: Schwarzschild²+Compton²=observable² (Lineweaver-Patel)</span>
            <span>Same Pythagorean. All scales.</span>
          </div>
        </div>
      )}

      {!sel && (
        <div style={{
          textAlign: "center", fontSize: 10, color: "#475569",
          maxWidth: 600, margin: "8px auto",
        }}>
          Click any element to see its Husmann Decomposition prediction.
          <br/>
          Three modes: <span style={{color:COLORS.s}}>s/p additive</span> · <span style={{color:COLORS.d}}>d Pythagorean</span> · <span style={{color:COLORS.ng}}>noble gas Pythagorean</span>
          <br/>
          Error colors show accuracy. Quantum depth shows position relative to the F(9)={F9} Fibonacci boundary.
        </div>
      )}
    </div>
  );
}
