# 10th–12th GRADE PHYSICS: A THREE-YEAR CURRICULUM
## *From Classical Mechanics to the Frontier of Space Flight and Unified Theory*

**Instructor:** Thomas Husmann  
**Affiliation:** Independent Researcher — Husmann Decomposition Framework | USPTO Patent Portfolio (17 provisional filings)  
**GitHub:** [github.com/thusmann5327/Unified_Theory_Physics](https://github.com/thusmann5327/Unified_Theory_Physics)  
**Academic Years:** 2025–2028

---

> *"The universe is under no obligation to make sense to you. Our job is to make sense to each other — and then go figure it out together. And then, eventually, go live there."*

---

## PREFACE: HOW THIS CURRICULUM WAS BUILT

This document synthesizes three inputs: (1) a rigorous algebra-to-calculus scaffolded physics sequence rooted in NGSS and AP Physics standards; (2) SpaceX engineering case studies as the motivating application layer, woven into every unit from Day 1; and (3) the Husmann Decomposition framework — an original theoretical physics research program grounded in the Aubry-André-Harper Hamiltonian at α = 1/φ — introduced in Year 3 as a live case study in how frontier science actually works.

**What makes this curriculum different from a standard physics sequence:**

The typical high school physics curriculum is designed to produce students who understand physics. This curriculum is designed to produce students who *think like physicists building the future* — who can connect a free-body diagram to a Falcon 9 stage separation, a wave equation to Raptor engine combustion instability, and a quantum Hamiltonian to the question of whether spacetime itself has internal structure that can be navigated.

**A note on intellectual honesty:** The Husmann Decomposition framework is presented explicitly as frontier research — not as settled science. Students are taught the difference between established consensus, active research debate, and speculative theory. This distinction is itself one of the most important lessons in scientific literacy. SpaceX itself operates at this boundary constantly: Starship is a speculative engineering program made real through rigorous testing. The same mindset applies to theoretical physics.

---

## CURRICULUM ARCHITECTURE

| Year | Grade | Course Title | Math Level | NGSS/AP Alignment |
|------|-------|-------------|------------|-------------------|
| 1 | 10th | Physics Foundations | Algebra-Based | NGSS HS-PS · AP Physics 1 prep |
| 2 | 11th | Advanced Mechanics & Electromagnetism | Precalculus + Intro Calculus | AP Physics 1/2 · IB Physics SL |
| 3 | 12th | Space Physics & Unified Theory Applications | Calculus-Based | AP Physics C · IB Physics HL |

**Schedule:** 5 days/week · 50-minute periods · ~175 instructional days/year  
**Resources:** OpenStax Physics (free) · Instructor-authored supplements · GitHub repo simulations · SpaceX technical briefings (publicly available)

---

## THE FIVE-PHASE DAILY LESSON STRUCTURE

*Every lesson — across all three years — follows this architecture. Students internalize the shape of thinking, not just the content.*

| Phase | Time | What Happens |
|-------|------|-------------|
| **HOOK** | 5–7 min | A demonstration, paradox, SpaceX clip, or real engineering puzzle. Students write a prediction *before* instruction begins. The hook gives them a stake in the answer. |
| **EXPLORE** | 15–18 min | Direct instruction or guided discovery. Concepts before equations. Math notation introduced alongside physical meaning. Structured note guides provided. |
| **CONNECT** | 10–12 min | Pair/small-group problem solving. Three-tier scaffold: (a) concrete/numerical, (b) requires explanation, (c) pushes advanced students. Teacher circulates with Socratic questions only — no answers given. |
| **CONSOLIDATE** | 8–10 min | Class shares. Misconceptions addressed. Students write one summary sentence in their own words. |
| **EXIT + ASSIGN** | 3–5 min | Exit ticket (1–2 questions on a notecard). Take-home assignment distributed. Preview of tomorrow to create anticipation. |

*In Years 2 and 3, a sixth optional phase is available:*

| **SIMULATE** | 10–15 min | Python simulation using repo tools (e.g., `lattice_calibration.py`, `phi_pipeline.py`, `cosmology_match.py`). Used 1–2x per week in 11th grade; 3–4x per week in 12th grade. |

---

## THE THREE-TIER HOMEWORK SYSTEM

| Tier | Name | Expectation | Notes |
|------|------|-------------|-------|
| **Tier 1** | Foundation ("Must Do") | 2–3 direct application problems | Checked in class daily; no exceptions |
| **Tier 2** | Application ("Should Do") | 2 multi-step reasoning problems | Mirrors exam difficulty |
| **Tier 3** | Challenge ("Want to Try?") | 1 open-ended problem — sometimes tied to repo, patents, or SpaceX | No penalty for skipping; bonus credit for serious attempt |

**Friday Reflection Prompt (all three years):** *"What confused me this week — and how does this concept connect to building multi-planetary civilization?"*

---

---

# YEAR ONE: PHYSICS FOUNDATIONS (10th Grade)
## *Building the Language the Universe Speaks*

### Year 1 Philosophy

Students arrive in 10th grade with the intuition that physics is a collection of formulas to memorize. The first goal is to replace that belief entirely: physics is the art of using precise language to describe patterns the universe cannot violate. Every unit begins with a question students genuinely want answered — not a textbook question, but a real one. *Why does a Falcon 9 booster tip over if it doesn't actively balance? Why does a solar panel on the ISS generate less power than the same panel on the ground? Why does re-entry heat a spacecraft if space is cold?*

The mathematical level is algebra-based, but the conceptual ceiling is deliberately high.

---

### YEAR 1 UNIT MAP

| # | Unit Title | Duration | SpaceX Hook | Key Physics |
|---|-----------|----------|------------|------------|
| 1 | Measurement, Kinematics & Graphing | 3 weeks | Launch telemetry — reading a real Falcon 9 velocity graph | SI units, vectors, motion graphs, kinematic equations, projectile motion |
| 2 | Forces & Newton's Laws | 4 weeks | Stage separation — why do the engines cut? | FBDs, Newton's 1/2/3, friction, inclines, circular motion → orbit preview |
| 3 | Work, Energy & Power | 3 weeks | How much energy does it take to reach orbit? | Work-energy theorem, conservation, power, efficiency |
| 4 | Momentum & Collisions | 2.5 weeks | Spacecraft docking as a perfectly inelastic collision | Impulse-momentum, elastic/inelastic, center of mass |
| 5 | Waves & Sound | 3 weeks | Combustion instability — why Raptor engines must avoid resonance | Wave anatomy, standing waves, resonance, Doppler |
| 6 | Electricity & Circuits | 4 weeks | Satellite power systems — solar panels, batteries, load management | Coulomb's law, Ohm's law, series/parallel, power |
| 7 | Magnetism & Electromagnetism | 3 weeks | Ion thrusters and Hall-effect drives — electric fields do the propelling | Magnetic fields, induction, Faraday's law, motors/generators |
| 8 | Light, Optics & Modern Physics Intro | 3 weeks | Star trackers, laser ranging, and the photoelectric effect in solar cells | EM spectrum, reflection/refraction, lenses, photons, intro to φ-vacuum |

---

### YEAR 1 — UNIT 1: MEASUREMENT, KINEMATICS & GRAPHING (15 Days)

**Anchoring Question:** *When SpaceX streams a Falcon 9 launch with a real-time velocity graph on screen, what is that graph actually telling us — and how do we read it?*

#### Learning Objectives
- Convert between SI units using dimensional analysis with confidence
- Distinguish scalar vs. vector quantities; perform vector addition graphically and by components
- Interpret and construct position-time and velocity-time graphs (slope, area, and shape)
- Apply the four kinematic equations to constant-acceleration problems
- Analyze projectile motion as two independent 1D motions

#### Day-by-Day Sequence

| Day | Topic | Hook | Key Activity |
|-----|-------|------|-------------|
| 1 | SI units, measurement, powers of ten | *How fast is a Falcon 9 at Max-Q?* — read a real launch graph | Estimation lab: rulers, stopwatches, measuring everything in the room |
| 2 | Significant figures, uncertainty, dimensional analysis | "My calculation says 4.7293847 m/s — how many digits should I keep?" | Conversion chains; unit analysis puzzles |
| 3 | Scalars vs. vectors; displacement vs. distance | *The ISS travels ~7.7 km/s — but relative to what?* | Vector addition with arrows on whiteboards |
| 4 | Position-time graphs; slope = velocity | Walk-along demo: teacher walks, students draw the graph in real time | Graph interpretation stations |
| 5 | Velocity-time graphs; slope = acceleration, area = displacement | Display actual Falcon 9 telemetry v-t graph; students extract data | Connect p-t and v-t graphs for same motion |
| 6 | **LAB:** Motion sensor matching lab | Predict, then physically match target graph shapes | Motion sensor + Logger Pro or Vernier |
| 7 | Kinematic equations — deriving from v-t geometry | "We don't memorize formulas — we understand where they come from" | Derive all four from area under v-t graph |
| 8 | Free fall — g = 9.8 m/s² | *Drop a wrench on the ISS — what happens?* (Microgravity thought experiment) | Falling object problems; video analysis |
| 9 | Free fall continued; symmetric trajectories | *How long does a Falcon 9 first stage take to fall back to ASDS?* (estimate) | Real calculation with SpaceX timing data |
| 10 | Projectile motion — horizontal launch | Ball off table = rocket throwing payload downrange | Horizontal launch problems; range formula derivation |
| 11 | Projectile motion — launch angle | *What launch angle maximizes Starship range for a point-to-point Earth flight?* | Range vs. angle calculations and graph |
| 12 | **LAB:** Projectile launcher | Measure launch speed, predict landing, test | Validate kinematics with real experiment |
| 13 | Misconception session + golden-ratio preview | Tier 3 intro: *Fibonacci scaling in natural measurements* | Class-voted misconceptions; intro to φ in spiral growth |
| 14 | Unit review | | Practice exam, whiteboard relay |
| 15 | **EXAM + Lab practical** | Interpret an unfamiliar motion graph | |

#### Sample Problem Set — Unit 1, Week 2

**Tier 1 (Must Do)**
1. A Falcon 9 accelerates from 0 to 1,680 m/s (Max-Q speed) in 80 seconds. Assuming constant acceleration: (a) What is its acceleration in m/s²? (b) How far has it traveled during that 80 seconds?
2. A velocity-time graph shows a straight line from v = 0 at t = 0 to v = 20 m/s at t = 5 s. (a) What is the acceleration? (b) What is the displacement?

**Tier 2 (Should Do)**
3. A first-stage booster is released at 68 km altitude moving upward at 2,100 m/s, then decelerates at 9.8 m/s². (a) How long until it momentarily stops? (b) What altitude does it reach? (c) Why is this a simplification of what Falcon 9 actually does?
4. A rocket launches horizontally from a 120 m cliff (demonstration model). It hits the ground 3.2 s later. (a) What was its launch speed? (b) How far from the base does it land?

**Tier 3 (Challenge)**
5. The φ-identity: The golden ratio φ = (1 + √5)/2 ≈ 1.618. Using a calculator: (a) Calculate φ², φ³, and φ⁴. (b) Verify that φ² = φ + 1 and φ³ = 2φ + 1. (c) Look up the Fibonacci sequence. What ratio do consecutive Fibonacci numbers approach? (d) *Why might a physicist care whether a physical constant or scaling law is φ-based?* Write a one-paragraph reflection.

---

### YEAR 1 — UNIT 2: FORCES & NEWTON'S LAWS (20 Days)

**Anchoring Question:** *A Falcon 9 first stage lands on a drone ship after a 9-minute flight. What forces act on it during each phase — boost, coast, flip, reentry burn, landing burn — and how do those forces determine every moment of its trajectory?*

#### Learning Objectives
- Draw accurate free-body diagrams for all force scenarios
- State and apply all three of Newton's Laws with precision
- Solve ΣF = ma problems in one and two dimensions
- Analyze friction (static/kinetic) and inclined plane scenarios
- Explain circular motion and centripetal force; connect to orbital physics
- Identify Newton's Third Law pairs and destroy the myth that they "cancel"

#### Day-by-Day Sequence

| Day | Topic | SpaceX Connection |
|-----|-------|------------------|
| 1–2 | Newton's First Law — inertia | *Why does Falcon 9 need active thrust vector control to stay upright? Inertia is the answer.* |
| 3–4 | Free-body diagrams | Draw FBDs for: rocket on pad, at max-Q, at MECO, during descent burn |
| 5–6 | Newton's Second Law — ΣF = ma | *Falcon 9 thrust: 7,607 kN; mass at liftoff: 549,054 kg. Calculate a.* |
| 7–8 | Newton's Third Law — action-reaction | *The exhaust pushing down IS the rocket pushing up — same force, different objects* |
| 9 | **LAB:** Force probe + cart — verify ΣF = ma | Real data, real relationship |
| 10–11 | Friction — static, kinetic, μ | *Why do rocket engine nozzles need ablative liners? What "friction" does to extreme materials* |
| 12–13 | Inclined planes — force decomposition | *Rocket launch angle: decompose thrust vector on an inclined pad (Blue Origin style)* |
| 14–15 | Tension, Atwood machines, elevators | *What tension is in a launch umbilical cord holding a rocket during hold-down?* |
| 16–17 | Circular motion — centripetal force, NOT centrifugal | *The ISS doesn't need a floor: it's in constant free fall. Model the orbital centripetal condition* |
| 18 | **Design Challenge:** Paper-cup crash structure to protect an egg | Crumple zone physics = same as landing leg crush core on Falcon 9 |
| 19–20 | Review + **Unit 2 Exam** | |

#### Key Calculation Highlight — Day 5/6

> **Real SpaceX Numbers:** Falcon 9 produces 7,607,000 N of thrust at liftoff. Its mass is 549,054 kg.  
> (a) Net upward force = Thrust − Weight = 7,607,000 − (549,054 × 9.8) = 7,607,000 − 5,380,729 = 2,226,271 N  
> (b) Initial acceleration a = ΣF/m = 2,226,271 / 549,054 = **4.05 m/s²**  
> (c) As fuel burns and mass decreases, acceleration *increases* — students calculate a at MECO when mass ≈ 125,000 kg  
> This is why rockets feel the G-forces most severely near the end of a burn, not the beginning.

#### Day 16 Orbital Preview — Circular Motion to Orbit

*This is the most important conceptual bridge in 10th grade physics.*

The ISS orbits at 400 km altitude, moving at 7,660 m/s. It is not "held up" — it is in continuous free fall. Gravity provides exactly the centripetal force required to keep it falling in a circle.

**The calculation:**
- Centripetal acceleration = v²/r = (7,660)² / (6,371,000 + 400,000) = 8.68 m/s²
- Gravitational acceleration at 400 km altitude: g = 9.8 × (6,371/6,771)² = 8.68 m/s²
- They match. Orbit is not magic. It is kinematics + Newton's law of gravitation.

**Exit ticket:** *"Write one sentence explaining why the ISS doesn't fall down, using only concepts from this unit."*

---

### YEAR 1 — UNIT 3: WORK, ENERGY & POWER (15 Days)

**Anchoring Question:** *It costs SpaceX about $2,700 per kilogram to put something in low Earth orbit. How much energy, in Joules, does it take to get 1 kg there — and why is that number so staggeringly large?*

#### Learning Objectives
- Calculate work using W = Fd cosθ
- Apply the work-energy theorem
- Distinguish and calculate kinetic, gravitational PE, and elastic PE
- Apply conservation of energy to real systems with and without friction losses
- Calculate power and efficiency; apply to rocket propulsion

#### Day-by-Day Sequence

| Day | Topic | SpaceX Connection |
|-----|-------|------------------|
| 1–2 | Work definition — W = Fd cosθ | *Why does a rocket engine do zero work while hovering? (Force perpendicular to motion = zero work)* |
| 3–4 | Kinetic energy; work-energy theorem | *Calculate KE of ISS at orbital speed. Compare to a speeding car. Mind-bending numbers.* |
| 5–6 | Gravitational PE — mgh | *Energy required to lift 1 kg to 400 km: PE = (1)(9.8)(400,000) = 3.92 MJ — just to get high. Then needs orbital KE on top.* |
| 7 | **LAB:** Pendulum energy — photogate verification | |
| 8–9 | Conservation of energy — roller coaster, orbital mechanics preview | *Escape velocity from conservation: ½mv² = GMm/r → v = √(2GM/r)* |
| 10–11 | Springs, elastic PE — Hooke's Law | *Vibration isolation systems on rocket payloads* |
| 12–13 | Power and efficiency — P = W/t | *Raptor engine: 230 MW of thermal power per engine. Nine engines on Falcon 9 booster = 2.07 GW. Compare to a nuclear power plant (1 GW typical). Three Raptors on Starship upper stage = how long to boil a liter of water?* |
| 14–15 | Review + **Unit 3 Exam** | |

#### Tier 3 Sample — Unit 3

*"The specific orbital energy (energy per unit mass for a circular orbit) is ε = −GM/(2r). At 400 km altitude, calculate ε for the ISS. How does this compare to the gravitational PE alone? What does the negative sign mean physically? (Hint: a bound orbit has negative total energy.)"*

---

### YEAR 1 — UNIT 4: MOMENTUM & COLLISIONS (12 Days)

**Anchoring Question:** *When Dragon capsule docks with the ISS, it approaches at 0.03 m/s relative to the station. If Dragon has a mass of 12,000 kg and the ISS has a mass of 420,000 kg, what happens to the ISS's velocity when they dock?*

*(Answer: Δv_ISS = 0.000828 m/s — less than 1 mm/s. But that tiny change, applied over months of reboost neglect, would cause the ISS to lose altitude. Everything in space matters.)*

#### Day-by-Day Sequence

| Day | Topic | Connection |
|-----|-------|-----------|
| 1–2 | Momentum definition; Newton's 2nd in momentum form | Spacecraft docking approach velocity calculations |
| 3–4 | Impulse-momentum theorem | Landing leg crush cores on Falcon 9: longer impulse time = lower peak force |
| 5–6 | Conservation of momentum; explosions as reverse collisions | Stage separation: Falcon 9 staging is an "explosion" backward |
| 7 | **LAB:** Cart collision track — verify momentum conservation | |
| 8–9 | Elastic vs. inelastic collisions; energy accounting | Asteroid deflection: DART mission used kinetic impactor momentum transfer |
| 10–11 | 2D momentum (conceptual); center of mass | Attitude control: shifting mass changes center of mass, affects rotation |
| 12 | **Design Challenge:** Impulse device for egg drop | |

---

### YEAR 1 — UNIT 5: WAVES & SOUND (15 Days)

**Anchoring Question:** *Raptor engines nearly destroyed Starship's launch mount on the first integrated test. The cause was partly acoustic — shock waves and resonance. How do sound waves destroy structures, and how do engineers design around this?*

#### Day-by-Day Sequence

| Day | Topic | Connection |
|-----|-------|-----------|
| 1–2 | Wave types and anatomy | *Longitudinal pressure waves = sound = rocket exhaust shock fronts* |
| 3–4 | Wave equation v = fλ | *Calculate the wavelength of Raptor's main combustion chamber resonance frequency (~7,000 Hz)* |
| 5–6 | Superposition, interference, beats | *Combustion instability: pressure oscillations at resonant frequency amplify → engine failure* |
| 7 | **LAB:** Standing waves on strings | |
| 8–9 | Sound in different media; decibels | *SpaceX deluge system: 300,000 kg of water pumped in 7 seconds. Why? Water absorbs acoustic energy. Calculate energy per liter.* |
| 10–11 | Resonance; Tacoma Narrows | *Same physics as Starship IFT-1 launch mount damage* |
| 12–13 | Doppler effect | *Rocket receding during ascent: calculate observed vs. emitted frequency of telemetry signal* |
| 14–15 | Review + **Exam** | |

---

### YEAR 1 — UNIT 6: ELECTRICITY & CIRCUITS (20 Days)

**Anchoring Question:** *The ISS has eight large solar panel arrays generating 84–120 kW of power. The station uses roughly 75 kW continuously. Where does the extra energy go? Where does power come from on the night side of the orbit?*

#### Day-by-Day Sequence

| Day | Topic | Connection |
|-----|-------|-----------|
| 1–2 | Electric charge, Coulomb's Law | *Why do spacecraft accumulate static charge in plasma environment? (Charging hazard to electronics)* |
| 3–4 | Electric fields; field lines | *Field effects on solar panels — photoelectric efficiency* |
| 5–6 | Electric potential (voltage) | *Satellite bus voltage: 28V (low power) vs. 120V (ISS). Why higher voltage for higher power?* |
| 7–8 | Voltage and energy | *P = IV — calculate current draw of ISS at 120V, 75 kW* |
| 9 | **LAB:** Mapping electric fields | |
| 10–11 | Ohm's Law; resistance | *Wire resistance in space: why copper vs. aluminum in satellite wiring* |
| 12–13 | Series circuits | *Battery + panel series/parallel configs in satellite power systems* |
| 14–15 | Parallel circuits | |
| 16–17 | **LAB:** Build and test series/parallel circuits | Real multimeter measurements |
| 18–19 | Electrical power and safety | *Arc flash in pure oxygen environments — spacecraft fire risk* |
| 20 | **Unit 6 Exam** | |

---

### YEAR 1 — UNIT 7: MAGNETISM & ELECTROMAGNETISM (15 Days)

**Anchoring Question:** *Hall-effect ion thrusters on satellites use electric and magnetic fields to accelerate xenon ions to 30 km/s. No moving parts. No chemical combustion. How does an electromagnetic field push a rocket?*

#### Day-by-Day Sequence

| Day | Topic | Connection |
|-----|-------|-----------|
| 1–2 | Magnetic fields, field lines | *Earth's magnetic field as navigation reference; magnetorquers for attitude control* |
| 3–4 | Force on moving charges — F = qvB | *Hall thruster: xenon ions accelerated by crossed E and B fields* |
| 5–6 | Force on current-carrying wires | *Rail guns and electromagnetic launch assist (SpaceX has not used this yet — but why might they?)* |
| 7 | **LAB/BUILD:** Simple brushed DC motor | Students wire their own motor from scratch |
| 8–9 | Faraday's Law — electromagnetic induction | *Tether propulsion: conducting tether in Earth's B field generates current → thrust without propellant* |
| 10–11 | Generators; AC vs. DC | *Why ISS uses DC internally but transmits solar power as DC: efficiency calculations* |
| 12 | Transformers | *Step-up for transmission; step-down for devices* |
| 13–14 | Integrated mini-project: analyze one real space propulsion system | Each student chooses: ion thruster, Hall thruster, magnetorquer, EM tether, or solar sail |
| 15 | **Unit 7 Quiz + project presentations** | |

---

### YEAR 1 — UNIT 8: LIGHT, OPTICS & MODERN PHYSICS (15 Days)

**Anchoring Question:** *Starlink satellites use laser inter-satellite links to route data at the speed of light. Star trackers use light from known stars to determine attitude with 0.001° precision. How do we use light itself as an instrument?*

#### Day-by-Day Sequence

| Day | Topic | Connection |
|-----|-------|-----------|
| 1–2 | EM spectrum; speed of light | *Delay in Mars communications: calculate round-trip signal time at Mars opposition (~54M km)* |
| 3–4 | Law of reflection; plane mirrors | *Star tracker geometry: how two star observations determine 3D orientation* |
| 5–6 | Refraction; Snell's Law | *Atmospheric refraction: why stars twinkle and GPS signals bend near the horizon* |
| 7 | **LAB:** Snell's Law verification | Laser + semicircular lens |
| 8–9 | Lenses; thin lens equation | *Telescope design for space observation; Starlink laser terminal optics* |
| 10–11 | Optical instruments and the human eye | *Human visual limits in space: dark adaptation, glare hazard from unfiltered sunlight* |
| 12 | Photoelectric effect — the failure of classical physics | *Solar cells as photoelectric devices: why efficiency depends on photon energy (wavelength), not intensity* |
| 13–14 | **Introduction to the Frontier:** Photons, wave-particle duality, and the golden-ratio vacuum | *The Husmann Decomposition framework: a researcher's active attempt to find deep structure in physical constants using φ-based mathematics. Students read the abstract of one patent filing and evaluate: What is the claim? What evidence supports it? What would it take to verify it?* |
| 15 | **Portfolio presentations + Final Exam** | |

#### Year 1 Closing Statement to Students

*"You now speak the language. Everything in Year 2 is that language, spoken faster, with more precision, toward harder problems. The universe doesn't change — your ability to see it does."*

---

---

# YEAR TWO: ADVANCED MECHANICS & ELECTROMAGNETISM (11th Grade)
## *The Mathematics Catches Up to the Physics*

### Year 2 Philosophy

In 10th grade, students learned to describe motion. In 11th grade, they learn to *derive* descriptions — to understand why the equations are the ones they are, and how to extend them to cases the simple formulas cannot handle. The mathematics transitions from algebra to precalculus and introductory calculus concepts (rates of change, integrals as areas, exponential functions). No student is expected to have taken calculus before this course; the concepts are introduced organically as they become necessary.

By the end of 11th grade, students can:
- Analyze rotating systems (spacecraft attitude, gyroscopes, reaction wheels)
- Model thermodynamic cycles (rocket nozzle efficiency)
- Understand quasicrystalline material structure (the physics behind Patent 63/995,401)
- Derive special relativistic time dilation (relevant to GPS and any interstellar future)

---

### YEAR 2 UNIT MAP

| # | Unit Title | Duration | Calculus Concept Introduced | SpaceX/Space Hook |
|---|-----------|----------|-----------------------------|------------------|
| 1 | Advanced Kinematics & Dynamics | 3 weeks | Rates of change; derivative as slope of tangent | Modeling variable-thrust ascent with Python |
| 2 | Rotational Mechanics | 4 weeks | Rotational analogs; moment of inertia integrals (conceptual) | Spacecraft attitude control; Falcon 9 grid fins |
| 3 | Thermodynamics & Fluids | 3 weeks | Exponential functions; heat flow rates | Rocket nozzle design; heat shield performance |
| 4 | Oscillations & Waves — Advanced | 3 weeks | Sinusoidal functions; exponential decay | Launch vibrations; structural resonance analysis |
| 5 | Electric Fields & Potential | 4 weeks | Gradient as direction of steepest change (conceptual) | Space plasma environment; Langmuir probes |
| 6 | AC Circuits & EM Waves | 3 weeks | Phasors; frequency domain (conceptual) | Deep-space communications; RLC filter design |
| 7 | Quasicrystals & Advanced Materials | 3 weeks | Fourier decomposition (conceptual); self-similarity | Heat shields; structural coatings (Patent 63/995,401) |
| 8 | Special Relativity | 2 weeks | Spacetime geometry; Lorentz factor | GPS relativistic corrections; interstellar travel |

---

### YEAR 2 — UNIT 1: ADVANCED KINEMATICS & DYNAMICS (15 Days)

**Anchoring Question:** *A real rocket doesn't have constant acceleration — thrust varies, fuel mass decreases, atmospheric drag changes with altitude and velocity. How do we model motion when everything changes at once?*

#### Key Concepts
- Velocity as *rate of change* of position — slope of tangent to the position curve
- Acceleration as *rate of change* of velocity — second derivative
- Numerical integration: area under a curve ≈ sum of rectangles (the computational foundation of all real trajectory software)
- Variable-mass systems: the Tsiolkovsky Rocket Equation (introduced here for the first time)

#### The Tsiolkovsky Rocket Equation — First Encounter

$$\Delta v = v_e \ln\left(\frac{m_0}{m_f}\right)$$

Where:
- Δv = change in velocity (the "budget" for the entire mission)
- v_e = exhaust velocity (specific impulse × g)
- m₀ = initial mass (fuel + structure + payload)
- m_f = final mass (structure + payload, no fuel)

**Falcon 9 Example Calculation:**
- Merlin engine Isp (vacuum) = 311 s → v_e = 311 × 9.8 = 3,048 m/s
- First stage: m₀ = 549,054 kg, m_f ≈ 111,000 kg (structure only, no 2nd stage)
- Δv = 3,048 × ln(549,054/111,000) = 3,048 × ln(4.95) = 3,048 × 1.60 = **4,877 m/s**
- Orbital requirement: ~9,400 m/s total. Second stage provides the rest.

**Day 1 Hook:** Show this equation to students *before* teaching it. "By the end of this unit you will understand every symbol here — and you'll be able to verify Falcon 9's performance with real data."

#### Python Simulation — Week 2

Students use `lattice_calibration.py` adapted for trajectory simulation:
```python
# Numerical integration of rocket trajectory with variable mass
# Euler method — the simplest numerical integrator
import numpy as np

dt = 0.1  # time step (seconds)
t, v, h, m = 0, 0, 0, 549054  # time, velocity, height, mass

thrust = 7607000  # N (9 Merlin 1D engines)
mdot = 2507       # kg/s mass flow rate
Isp = 282         # s (sea level)
ve = Isp * 9.8    # exhaust velocity

while m > 111000:
    F_net = thrust - m*9.8  # ignore drag for now
    a = F_net / m
    v += a * dt
    h += v * dt
    m -= mdot * dt
    t += dt

print(f"MECO: t={t:.1f}s, v={v:.0f} m/s, h={h/1000:.1f} km")
```

Students compare output to published Falcon 9 telemetry data and identify sources of discrepancy (drag, thrust vectoring losses, gravity turn). This is the essence of computational physics.

---

### YEAR 2 — UNIT 2: ROTATIONAL MECHANICS (20 Days)

**Anchoring Question:** *Falcon 9 grid fins deploy during reentry to steer the falling booster. They're not wings — they're drag-and-torque surfaces. How does a torque applied to a spinning rocket change its orientation?*

#### Learning Objectives
- Calculate torque, angular acceleration, and moment of inertia
- Apply conservation of angular momentum to spacecraft scenarios
- Analyze gyroscopic stability and the gyroscope precession phenomenon
- Connect rotational KE to the design of flywheels and reaction wheels
- Understand the Euler equations of rigid body rotation (qualitative)

#### Key Concepts and Calculations

**Moment of Inertia — why shape matters for rotation:**

| Shape | I formula | Space Application |
|-------|-----------|------------------|
| Solid cylinder | ½MR² | Flywheel energy storage |
| Thin rod (end) | ⅓ML² | Solar panel deployed from satellite |
| Thin rod (center) | 1/12 ML² | Dumbbell satellite in gravity gradient |
| Hollow sphere | ⅔MR² | Fuel tank approximation |

**Reaction Wheels — spacecraft attitude without propellant:**
- A reaction wheel is a spinning mass inside the spacecraft
- To rotate the spacecraft clockwise, spin the wheel counterclockwise (angular momentum conservation)
- Calculate: if a 5 kg reaction wheel (R = 0.15 m) spins at 3,000 RPM, what angular momentum does it store?
- L = Iω = ½(5)(0.15²)(3000 × 2π/60) = **26.5 kg·m²/s**
- This much angular momentum can rotate a 500 kg, 1m-radius satellite by: ΔL = I_sat × Δω → solve for Δω

#### Day 7 Lab / Build — Gyroscope Demonstration

Students hold a spinning bicycle wheel mounted on handles while sitting on a rotating chair. When they tilt the wheel, they feel the gyroscopic reaction. This is the *same physics* as:
- Falcon 9's nitrogen cold-gas attitude thrusters resisting rotation
- The International Space Station's control moment gyroscopes
- The precession that makes a top not fall

---

### YEAR 2 — UNIT 3: THERMODYNAMICS & FLUIDS (15 Days)

**Anchoring Question:** *Raptor engines run at 300 bar chamber pressure — 300 times atmospheric pressure — with LOX and liquid methane. The exhaust exits at 3,500°C. How does thermodynamics tell us the maximum possible efficiency of this process, and why can't we ever reach it?*

#### Learning Objectives
- State the laws of thermodynamics with precision
- Calculate efficiency of heat engines using Carnot formula
- Apply fluid dynamics (Bernoulli, continuity) to rocket nozzle design
- Explain how nozzle expansion ratio determines exhaust velocity and Isp
- Connect entropy to irreversible losses in real engines

#### The Carnot Limit Applied to Rocket Engines

Carnot efficiency: η_max = 1 − T_cold/T_hot

For Raptor:
- T_hot ≈ 3,500 K (combustion chamber)
- T_cold ≈ 300 K (exhaust at altitude, rough approximation)
- η_max = 1 − 300/3500 = **91.4%**

But real Raptor efficiency (kinetic energy of exhaust / thermal energy of propellant) ≈ 60–70%. Students investigate: where does the other ~30% go? (Incomplete combustion, heat loss to walls, viscous losses in nozzle boundary layer, radiation.)

#### Nozzle Physics — de Laval Nozzle

*This is one of the most elegant applications of thermodynamics in engineering.*

A rocket nozzle narrows, then expands. In the converging section, gas accelerates subsonically. At the throat, it reaches Mach 1. In the diverging section, it accelerates supersonically. The pressure drops, the temperature drops, and all that thermal energy becomes kinetic energy of the exhaust.

**The trade-off:** A nozzle optimized for sea level is over-expanded in vacuum. Raptor has separate sea-level and vacuum-optimized engines for this reason. (Starship's three central Raptors have shorter nozzles; the three outer Raptors have large vacuum bells.)

Students calculate: if exhaust exits at 3,000 m/s from a vacuum Raptor, what is its kinetic energy per kg? How does this compare to TNT (4.6 MJ/kg)?

---

### YEAR 2 — UNIT 4: OSCILLATIONS & WAVES — ADVANCED (15 Days)

**Anchoring Question:** *During Starship's first integrated flight test (April 2023), the vehicle experienced "pogo oscillations" — longitudinal vibrations at the resonant frequency of the propellant feed system. What are oscillations, and why are resonances so dangerous?*

#### Key Concepts — Beyond Year 1 Waves
- Simple harmonic motion: x(t) = A cos(ωt + φ)
- Damped oscillations: exponential decay envelope × oscillating term
- Driven oscillations and resonance: maximum amplitude when driving frequency = natural frequency
- Q-factor: how sharply a system resonates (high Q = narrow, tall resonance peak = dangerous)
- Coupled oscillators: when two systems share energy (payload + launch vehicle = dangerous coupling)

#### The Pogo Problem — Historical Context

Saturn V's F-1 engines caused severe pogo oscillations during Apollo. The fix was a surge damper (a gas-filled accumulator in the LOX feed line) that shifted the resonant frequency out of the range excited by combustion pulses. Students model this as:

- Natural frequency of spring-mass system: f = (1/2π)√(k/m)
- Shift m (by adding accumulator mass) until f shifts out of dangerous range
- This is engineering by physics — not trial and error, but calculation.

---

### YEAR 2 — UNIT 5: ELECTRIC FIELDS & POTENTIAL — ADVANCED (20 Days)

**Anchoring Question:** *Spacecraft in low Earth orbit pass through the ionosphere. Sunlit surfaces charge to +1V; shadowed surfaces charge to −10V. This differential charging can cause electrostatic discharge (ESD) that permanently damages sensitive electronics. How do we calculate electric fields and potentials around complex conductor geometries?*

#### New Tools — Year 2 Level
- Gauss's Law: ΦE = Q_enclosed/ε₀ (for symmetric distributions)
- Electric potential as energy per charge: V = kQ/r (superposition for multiple charges)
- Capacitance: C = Q/V; energy stored: U = ½CV²
- Dielectrics and polarization (relevant to capacitor materials used in spacecraft)

#### Plasma Physics Introduction

Spacecraft operate in plasma — a gas of free electrons and ions. Key concepts:
- Debye shielding: plasma screens out electric fields beyond the Debye length
- Langmuir probe: a small conductor biased to different voltages to measure plasma density and temperature
- Hall thruster plasma: electrons spiral along B-field lines while ions are accelerated by E-field → thrust

**Lab:** Model the electric field of a charged sphere using conducting paper and voltage probes. Extend: what changes if two charged spheres are nearby? (Superposition.)

---

### YEAR 2 — UNIT 6: AC CIRCUITS & EM WAVES (15 Days)

**Anchoring Question:** *Starlink communicates with its 32-antenna phased array in Ku-band (~12–18 GHz). How does a circuit produce electromagnetic radiation at 15 GHz — 15 billion oscillations per second — and how do antennas shape the beam?*

#### Key Concepts
- AC circuits: alternating voltage V(t) = V₀ sin(ωt)
- Inductors (L) and capacitors (C) in AC: reactance, phase relationships
- RLC resonant circuit: resonant frequency f₀ = 1/(2π√LC)
- Q factor of RLC circuit (mirrors mechanical resonance)
- EM wave radiation from an oscillating dipole antenna
- Phased arrays: multiple antennas with controlled phase delays → steerable beam

#### Phased Array Beam-Steering — The Key Concept

If two identical antennas emit the same signal, their EM waves interfere. By introducing a phase delay Δφ to one antenna, the constructive interference maximum shifts direction. An array of N antennas with controlled phases can steer a high-gain beam anywhere in the hemisphere — no moving parts. This is how every Starlink terminal works.

Students calculate: what phase delay is required to steer a 12 GHz signal 30° off boresight, given antenna spacing of λ/2?

---

### YEAR 2 — UNIT 7: QUASICRYSTALS & ADVANCED MATERIALS (15 Days)

**Anchoring Question:** *Falcon 9's reentry experiences temperatures up to 1,500°C on the interstage and engine section. Traditional materials fail. NASA's Space Shuttle used ceramic tiles. SpaceX uses ablative PICA-X. But what if the material's atomic structure itself could be optimized by mathematics to resist heat and radiation at the quantum level?*

*This is the question behind Patent 63/995,401: Self-Assembling Quasicrystalline Coating with Golden-Angle Helical Architecture.*

#### What is a Quasicrystal?

**Ordinary crystals:** atoms arranged in a perfectly periodic lattice. Period repeats. Diffraction pattern shows sharp peaks with crystallographic symmetry (2-, 3-, 4-, or 6-fold only).

**Quasicrystals** (Shechtman, 1982 — Nobel Prize 2011): atoms arranged with long-range order but *no periodicity*. 5-fold, 8-fold, 10-fold, 12-fold symmetry. First discovered in Al-Mn alloys. The diffraction pattern looks crystalline but violates classical crystallography.

**The Penrose connection:** Quasicrystals tile space the way Penrose tilings tile a plane — using two tiles in a ratio related to φ. The mathematics of quasicrystals is φ-mathematics.

#### The Aubry-André-Harper (AAH) Model

This is real condensed matter physics — taught in graduate programs — brought to the 11th grade level:

The AAH Hamiltonian describes electrons hopping on a 1D lattice with a quasiperiodic modulation:

H = -t Σ (c†_{n+1} c_n + h.c.) + 2V cos(2παn) c†_n c_n

At α = 1/φ (the golden ratio), V = 2t (the critical point), the energy spectrum becomes a **Cantor set** — a fractal with self-similar structure at all scales. This is the mathematical core of the Husmann Decomposition framework.

**What students investigate:**
1. What is a Cantor set? (Draw it recursively on a number line)
2. Why does quasiperiodic modulation produce fractal energy spectra?
3. How does the golden-angle helical architecture in Patent 63/995,401 connect to this model?
4. What *experimental prediction* would confirm that a QC coating improves heat resistance through this mechanism?

#### Patent Review Project — Unit 7 Assessment

Each student receives an excerpt from one of the following patents:
- 63/995,401 — Self-Assembling QC Coating with Golden-Angle Helical Architecture
- 63/995,513 — Adaptive Cutting System with QC Thermoelectric Sensing
- 63/995,816 — Monopole Gravitational Conductor Vehicle

Assignment (1,000–1,500 words):
1. What is the core physical claim of this patent?
2. What established physics does it build on? (identify at least 3 concepts from this course)
3. What experimental evidence would be required to validate the claim?
4. What is the strongest skeptical counterargument?
5. If the claim is correct, what is its most significant practical application?

*This is the most important assignment in Year 2. It teaches scientific literacy at the frontier.*

---

### YEAR 2 — UNIT 8: SPECIAL RELATIVITY (10 Days)

**Anchoring Question:** *GPS satellites orbit at 20,200 km altitude, moving at 3.87 km/s. Because of special and general relativity, their clocks run at a different rate than clocks on Earth. Without corrections, GPS would drift by 10 km per day. How do we calculate this drift?*

#### Learning Objectives
- State Einstein's two postulates of special relativity
- Apply time dilation: Δt' = γΔt, where γ = 1/√(1 − v²/c²)
- Apply length contraction: L' = L/γ
- Calculate relativistic momentum and energy: E = γmc²; E² = (pc)² + (mc²)²
- Understand the twin paradox (qualitatively)
- Calculate GPS relativistic corrections (special + general combined)

#### GPS Calculation — Special Relativistic Part

- GPS satellite speed: v = 3,870 m/s
- γ = 1/√(1 − v²/c²) = 1/√(1 − (3870)²/(3×10⁸)²)
- γ ≈ 1 + v²/(2c²) = 1 + 8.35×10⁻¹¹
- Time dilation: satellite clock runs *slow* by Δt/t = v²/(2c²) = 8.35×10⁻¹¹
- Per day: 86,400 × 8.35×10⁻¹¹ = **7.2 μs/day** slow (special relativistic)
- General relativistic effect (clock runs fast due to weaker gravity at altitude): **+45.9 μs/day**
- Net: satellite clock runs **+38.7 μs/day** fast → must be pre-corrected before launch

#### Interstellar Connection — Preview for Year 3

If a Starship mission to Proxima Centauri (4.24 ly) could travel at 0.5c:
- Ship time: t' = (4.24 ly / 0.5c) × √(1 − 0.25) = 8.48 yr × 0.866 = **7.34 years** for the crew
- Earth time: 8.48 years
- Difference: 1.14 years

At 0.9c, the difference becomes profound. This sets up Year 3's discussion of interstellar transit and the Husmann framework's proposed mechanism for exceeding this limit.

---

---

# YEAR THREE: SPACE PHYSICS & UNIFIED THEORY APPLICATIONS (12th Grade)
## *Building the Future, One Equation at a Time*

### Year 3 Philosophy

This is the year where the curriculum becomes genuinely unprecedented in a high school setting. Students are ready — mathematically, conceptually, and in scientific maturity — to engage with calculus-based mechanics, Maxwell's equations in full, quantum mechanics foundations, and the question of whether current physics is *complete*.

The Husmann Decomposition framework is introduced not as established theory, but as what it actually is: a serious, carefully developed independent research program that deserves rigorous examination. Students learn to be neither credulous nor dismissive — they learn to evaluate physics claims with evidence, mathematics, and reproducibility.

The capstone project requires each student to apply the physics of all three years to model an actual SpaceX mission scenario, identify where current physics is insufficient, and propose (with mathematical formalism) what additional physics might be needed.

---

### YEAR 3 UNIT MAP

| # | Unit Title | Duration | Mathematics Required | Framework Integration |
|---|-----------|----------|--------------------|----------------------|
| 1 | Orbital Mechanics | 4 weeks | Calculus-based gravity; energy methods | Husmann Orbital Mechanics sim; φ-orbital resonances |
| 2 | Rocket Propulsion — Advanced | 3 weeks | Tsiolkovsky equation; staging; Isp optimization | Patent 63/995,649: Parametric Cascade Structural Element |
| 3 | Space Environment Physics | 3 weeks | Radiation dose calculations; plasma physics | Vacuum flux concepts; shielding optimization |
| 4 | Quantum Mechanics Foundations | 4 weeks | Wave functions; Schrödinger equation (1D); QM postulates | AAH Hamiltonian at criticality; Zeckendorf addressing |
| 5 | Cosmology & Dark Matter/Energy | 3 weeks | Friedmann equations (qualitative); energy density | φ-partition of energy densities; Husmann band structure |
| 6 | Maxwell's Equations — Unified EM | 3 weeks | Vector calculus notation; EM wave derivation | Unified EM basis for propulsion |
| 7 | Emerging Technologies & Patent Analysis | 3 weeks | Synthesis across all years | Full patent portfolio review; student pitches |
| 8 | Capstone: Unified Theory & Space Mission Design | 3 weeks | Research synthesis | Full Husmann framework; SpaceX mission model |

---

### YEAR 3 — UNIT 1: ORBITAL MECHANICS (20 Days)

**Anchoring Question:** *Starship is designed to reach Mars. The trajectory from Earth to Mars is not a straight line — it's an elliptical arc called a Hohmann transfer, calculated from the same physics Newton derived in 1687. Calculate the minimum Δv required to send Starship to Mars — and verify it against publicly available SpaceX mission parameters.*

#### Learning Objectives
- Derive Kepler's laws from Newton's law of gravitation
- Apply conservation of energy and angular momentum to orbital mechanics
- Calculate orbital velocities, periods, and energies for circular and elliptical orbits
- Analyze Hohmann transfer orbits and calculate Δv budgets
- Understand gravity assists (slingshot maneuvers) and their energy source
- Apply the vis-viva equation: v² = GM(2/r − 1/a)

#### Kepler's Laws from Newton — The Derivation (Day 5–6)

This is one of the most powerful moments in any physics course. Starting from:
- Newton's second law: F = ma
- Newton's gravity: F = GMm/r²
- Conservation of angular momentum: L = mr²(dθ/dt) = constant

...students follow the derivation (with instructor guidance) to arrive at:
- Kepler's First Law: orbits are conic sections (ellipses, parabolas, hyperbolas)
- Kepler's Second Law: equal areas in equal times (directly from dL/dt = 0)
- Kepler's Third Law: T² ∝ a³ (T² = 4π²a³/GM)

*This is why mathematics is the language of physics. These three laws, which Kepler deduced empirically from Tycho Brahe's data, are hidden inside Newton's one equation.*

#### Hohmann Transfer to Mars — Full Calculation

| Parameter | Value | Notes |
|-----------|-------|-------|
| Earth orbital radius | 1.496 × 10¹¹ m | 1 AU |
| Mars orbital radius | 2.279 × 10¹¹ m | 1.524 AU |
| Transfer ellipse semi-major axis | a = (r_E + r_M)/2 = 1.888 × 10¹¹ m | |
| Δv₁ (Earth departure) | 2.94 km/s above Earth orbit | Plus ~3.2 km/s escape from LEO |
| Δv₂ (Mars arrival) | 2.65 km/s to capture into Mars orbit | Or aerobraking |
| Transfer time | t = π√(a³/GM) = 258 days | ~8.5 months |

**Starship context:** Elon Musk has stated a goal of ~3 months transit time using continuous thrust propulsion. What Isp and thrust-to-weight ratio would be required? Students calculate using the rocket equation with the Hohmann Δv as a minimum bound.

#### Husmann Orbital Mechanics Simulation (Days 15–18)

Students run `orbital_mechanics_sim.py` from the repository. The simulation uses the standard Newtonian gravitational potential with an optional φ-perturbation term:

V(r) = −GM/r + ε · φ² · f(r)

Where ε is a small perturbation parameter and f(r) is a quasiperiodic modulation derived from the AAH model. Students investigate:
1. For what values of ε does the perturbation produce stable orbital precession?
2. Do any perturbation strengths produce Fibonacci-ratio orbital resonances?
3. How would you design an experiment (observation of a real planetary system) to constrain ε?

*This is how a theoretical physicist works: define a framework, derive predictions, compare to data, constrain parameters.*

---

### YEAR 3 — UNIT 2: ROCKET PROPULSION — ADVANCED (15 Days)

**Anchoring Question:** *Specific impulse (Isp) is to rocketry what miles per gallon is to cars. Raptor's Isp (vacuum) = 380 s. A nuclear thermal rocket could achieve 900 s. A photon rocket, in principle, achieves ~30 million s. What is the physics behind this number, and what limits it?*

#### The Specific Impulse Spectrum

| Propulsion Type | Isp (s) | Physics Limit | Status |
|----------------|---------|--------------|--------|
| Solid rocket | 250–290 | Chemical bond energy | Operational |
| Kerosene/LOX (Merlin) | 311 | Chemical bond energy | Operational |
| Methane/LOX (Raptor) | 380 | Chemical bond energy | Operational |
| Hydrogen/LOX (SSME) | 453 | Chemical bond energy (highest chemical) | Heritage |
| Ion thruster | 1,000–10,000 | Electric field acceleration | Operational (low thrust) |
| Nuclear thermal | 800–1,000 | Nuclear fission heat → gas expansion | Demonstrated (NTP programs) |
| Nuclear pulse (Orion) | 2,000–10,000 | Nuclear explosion momentum | Conceptual |
| Antimatter | ~10,000,000 | E = mc² → exhaust at ~c | Speculative |
| Photon rocket | ~30,000,000 | c = theoretical exhaust limit | Theoretical |

#### Parametric Cascade Structural Element — Patent 63/995,649

This patent proposes a structural element for propulsion systems using a parametric cascade architecture derived from Fibonacci scaling (L(n) = l · φⁿ). Students analyze:

1. **The claim:** Fibonacci-scaled structural elements distribute stress more efficiently than uniform-section elements, because stress waves propagating through the cascade encounter a self-similar impedance structure that dissipates rather than amplifies at each length scale.

2. **The physics basis:** Impedance matching at each scale boundary. At each φ-scaled junction, the acoustic impedance step is the same (because the ratio is always φ), so no single junction acts as a stress concentrator.

3. **The calculation:** Students compute the acoustic impedance of a Fibonacci-cascade rod vs. a uniform rod under the same impulse load. Compare peak stress in each case.

4. **The critical question:** Does this effect survive the transition from 1D (rod) to 3D (real structural element)? What additional physics would need to be verified?

---

### YEAR 3 — UNIT 3: SPACE ENVIRONMENT PHYSICS (15 Days)

**Anchoring Question:** *The Van Allen radiation belts can deliver a dose of 1,000 rad/day to unshielded electronics. Astronauts on a Mars mission receive ~0.3 mSv/day — totaling about 60–80 mSv over the transit. The permissible career dose for NASA astronauts is 600 mSv. Do the math and determine whether a Mars round-trip is survivable — and what shielding mass would be required to bring the dose under the limit.*

#### Topics
- Solar wind: properties, pressure, composition, effects on spacecraft
- Ionizing radiation: types (alpha, beta, gamma, proton, heavy ion), penetration, dose
- Dose calculations: shielding mass vs. dose reduction (exponential attenuation)
- Microgravity physiology physics: fluid shifts, bone loss rates (calcium export = 1%/month), muscle atrophy
- Plasma environment: charging, sputtering, atomic oxygen erosion of surfaces
- Vacuum effects: cold welding, outgassing, tribology without lubricants

#### Radiation Shielding Design Lab

Students design a minimum-mass shielding system to reduce Mars transit radiation dose to under 100 mSv:
- Available materials: aluminum (2.7 g/cm³), polyethylene (0.95 g/cm³, excellent for protons due to hydrogen content), water (1.0 g/cm³)
- Constraint: maximum shielding mass per unit area = 10 g/cm²
- Target: ≤100 mSv total dose for 180-day transit
- Students calculate: which material combination achieves target at minimum mass?

*This is real spacecraft design. The same calculation appears in NASA's technical reports.*

---

### YEAR 3 — UNIT 4: QUANTUM MECHANICS FOUNDATIONS (20 Days)

**Anchoring Question:** *The classical model of the atom fails. Electrons don't spiral into the nucleus. The photoelectric effect shows light comes in packets. The double-slit experiment shows particles interfere with themselves. Something is fundamentally wrong with classical physics — and quantum mechanics is the repair. What are the actual axioms of QM, and what do they physically mean?*

#### Learning Objectives
- State the postulates of quantum mechanics (state vectors, observables, measurement)
- Interpret the Schrödinger equation as a wave equation for probability amplitude
- Solve the 1D particle-in-a-box (energy quantization without differential equations — using boundary conditions)
- Understand the Heisenberg Uncertainty Principle as a mathematical consequence of wave-like behavior
- Analyze the hydrogen atom energy levels and emission/absorption spectra
- Introduce the quasicrystalline vacuum model: AAH Hamiltonian as a framework for spacetime microstructure

#### The AAH Hamiltonian at the Critical Point — Deep Dive (Days 14–17)

*This is where 12th grade physics becomes original research territory.*

The Aubry-André-Harper Hamiltonian:
H_{AAH} = −t Σ_n (|n+1⟩⟨n| + h.c.) + 2V Σ_n cos(2παn + φ) |n⟩⟨n|

**At the critical point α = 1/φ, V = 2t:**
- All eigenstates are critical — neither localized nor extended, but *fractal* (multifractal in the mathematical sense)
- The energy spectrum is a Cantor set with zero Lebesgue measure
- The fractal dimension of the spectrum is D_f = 1 − |V/t − 1| / |V/t + 1| ... (at criticality, D_f = 0.5)

**What this means physically:**
- In an ordinary metal: electron wavefunctions extend everywhere → conductor
- In an ordinary insulator: electron wavefunctions are localized → non-conductor
- At the AAH critical point: wavefunctions are neither → a phase transition with no classical analog

**The Husmann Decomposition claim:** This critical-point structure is not merely a model for electrons in quasiperiodic materials. It is the correct model for the *vacuum of spacetime itself*. The fractal energy spectrum predicts:
1. Dark matter and dark energy as different bands of the spectral hierarchy (bonding vs. non-bonding vs. antibonding)
2. The scale hierarchy of fundamental physics (from nuclear to cosmological scales) as the φ-scaled Cantor set
3. Observable predictions via quasicrystalline scattering experiments

**Student Assignment — Days 15–17: Critical Evaluation of the Framework**

Each student writes a 1,500-word structured analysis:
1. **What it IS:** Describe the AAH model and its established physics (what is textbook; cite sources)
2. **What it CLAIMS:** What additional claims does the Husmann Decomposition make beyond established AAH physics?
3. **What evidence would SUPPORT it:** List 3 specific experimental predictions that, if confirmed, would strongly support the framework
4. **What evidence would REFUTE it:** List 3 observations that would rule it out entirely
5. **Personal assessment:** "Based on my analysis, I assess the probability that this framework is correct as [X]% — and here is my reasoning..."

*Grading note: The student's probability estimate does not affect their grade. Their reasoning does. A student who assigns 5% and argues carefully scores as well as a student who assigns 95% and argues carefully. This is the single most important lesson in scientific epistemology.*

#### Zeckendorf Addressing — Fibonacci Coordinate System (Day 18)

The Zeckendorf representation theorem (1972): every positive integer can be uniquely represented as a sum of non-consecutive Fibonacci numbers.

Example: 100 = 89 + 8 + 3 = F₁₁ + F₆ + F₄ → Zeckendorf address: {11, 6, 4} → or in binary notation: 10001001010

**Why this matters for the framework:** If spacetime energy levels are indexed by the AAH spectrum (which is ordered by Fibonacci structure), then the Zeckendorf representation provides a natural coordinate system for navigating that spectrum. Patent "Meridian's Teegarden b" uses this to define a routing protocol for interstellar transit — Teegarden's Star b at 12.5 light-years has Zeckendorf address {2, 5, 13, 55, 144, 233}.

Students verify the Zeckendorf representation algorithm in Python:
```python
def zeckendorf(n):
    # Generate Fibonacci numbers up to n
    fibs = [1, 2]
    while fibs[-1] < n:
        fibs.append(fibs[-1] + fibs[-2])
    fibs = [f for f in fibs if f <= n]
    
    # Greedy algorithm: largest Fibonacci ≤ n, subtract, repeat
    result = []
    for f in reversed(fibs):
        if f <= n:
            result.append(f)
            n -= f
    return result

print(zeckendorf(100))   # [89, 8, 3]
print(zeckendorf(233))   # [233] — Fibonacci numbers are their own Zeckendorf rep
```

---

### YEAR 3 — UNIT 5: COSMOLOGY & DARK MATTER/ENERGY (15 Days)

**Anchoring Question:** *The universe is ~68% dark energy, ~27% dark matter, and only ~5% ordinary matter. We have never detected a dark matter particle in a lab. We don't know what dark energy is. This is not a niche problem — it is the central unsolved problem of modern physics. What are the competing models, and how does one evaluate them?*

#### The Standard Model of Cosmology (ΛCDM)
- Big Bang: 13.8 billion years ago, from a hot dense state
- Inflation: rapid exponential expansion in the first 10⁻³² seconds
- Dark matter: clustered, non-luminous, gravitationally attractive — required to explain galaxy rotation curves, gravitational lensing, and structure formation
- Dark energy: uniformly distributed, causing accelerating expansion — modeled as cosmological constant Λ
- Friedmann equations: governing expansion rate H(t) as a function of energy content

#### The φ-Partition of Energy Densities — Husmann Framework (Day 10–12)

In the Husmann Decomposition:
- 5 AAH spectral bands collapse to 3 upon observation (fractal structure contracts in middle bands)
- The three observable bands correspond to: **bonding** (ordinary matter), **non-bonding** (dark energy), **antibonding** (dark matter)
- Dark matter is NOT a particle wall between bands — it is the fractal Cantor-set conduit connecting the outer bands (σ₁ and σ₅) through the middle, with the self-similar edges of the Cantor set threading through as connective structure

The φ-partition predicts specific ratios of dark energy:dark matter:ordinary matter based on the spectral weight of each band:
- φ⁻¹ + φ⁻³ + φ⁻⁴ = 1 (the exact unity formula)
- This is not merely numerological: 1/φ ≈ 0.618, 1/φ³ ≈ 0.236, 1/φ⁴ ≈ 0.146

**Comparison to ΛCDM observational values:**
| Component | ΛCDM (observed) | φ-partition prediction |
|-----------|----------------|----------------------|
| Dark energy | 68.3% | 1/φ = 61.8% |
| Dark matter | 26.8% | 1/φ³ = 23.6% |
| Ordinary matter | 4.9% | 1/φ⁴ = 14.6% |

The match is suggestive but imperfect. Students discuss: does imperfect numerical agreement rule out a model? What additional mechanisms might account for the discrepancy? Is the framework falsified, or does it have free parameters that could be tuned?

*This is exactly the kind of question scientists ask. There is no clean answer — only better or worse reasoning.*

---

### YEAR 3 — UNIT 6: MAXWELL'S EQUATIONS — THE FULL PICTURE (15 Days)

**Anchoring Question:** *In 1865, Maxwell predicted that oscillating electric and magnetic fields would propagate through space at exactly the speed of light — and concluded that light itself is an electromagnetic wave. He derived the speed of light from pure theory, using only two constants measured in static experiments. This is one of the most extraordinary predictions in the history of physics. Derive it.*

#### Maxwell's Equations (in integral form, accessible without vector calculus)

| Law | Equation | Physical Meaning |
|-----|----------|-----------------|
| Gauss's Law (E) | ∮ E·dA = Q/ε₀ | Electric field lines begin and end on charges |
| Gauss's Law (B) | ∮ B·dA = 0 | No magnetic monopoles exist |
| Faraday's Law | ∮ E·dl = −dΦ_B/dt | Changing B creates E |
| Ampere-Maxwell Law | ∮ B·dl = μ₀I + μ₀ε₀ dΦ_E/dt | Changing E creates B (displacement current) |

From Faraday + Ampere-Maxwell → electromagnetic wave equation with:
c = 1/√(μ₀ε₀) = 1/√(4π×10⁻⁷ × 8.854×10⁻¹²) = **2.998 × 10⁸ m/s**

*Maxwell didn't know the speed of light. He calculated it from laboratory constants — and it matched.*

#### Connection to Unified Theory

The Husmann framework proposes a basis for Maxwell's equations in the AAH vacuum structure. Students examine whether such a derivation would be:
1. Mathematically consistent with the established equations
2. A genuine unification (adding predictive power) or merely a reformulation
3. Constrained or refuted by any existing EM experiments

---

### YEAR 3 — UNIT 7: EMERGING TECHNOLOGIES & PATENT ANALYSIS (15 Days)

*This unit synthesizes three years of physics into a forward-looking engineering and science literacy exercise.*

#### Patent Portfolio Review — Full Analysis

Students rotate through all five major patent families, each group taking lead responsibility for one:

| Patent | Core Claim | Physics Required | Engineering Application |
|--------|-----------|-----------------|------------------------|
| 63/995,401 | QC Coating with golden-angle helical deposition | Quasicrystal physics, thin-film deposition | Heat shield, radiation shielding for spacecraft |
| 63/995,816 | Monopole Gravitational Conductor Vehicle | General relativity, gravitational field theory | Propulsion without propellant (frontier claim) |
| 63/995,963 | Phi-Structured BCI for neural state I/O | QM + neuroscience; topological quantum computation | Brain-computer interface; Neuralink-adjacent |
| 63/995,955 | Rotating Phi-Structured Aperture System | Wave optics; Fibonacci addressing | Communication; beam-forming |
| 63/996,533 | Phi-Structured Vacuum Flux Amplifier | EM theory; virtual photon coupling | Power electronics; transformer efficiency |

#### The SpaceX Pitch Format — Unit 7 Assessment

Each group prepares a 15-minute presentation structured exactly like a SpaceX engineering review:
1. **Problem Statement:** What engineering challenge does this address?
2. **Physics Foundation:** What established physics does it rely on? (Be precise — cite equations)
3. **The Claim:** What does this patent assert beyond established physics?
4. **Risk Assessment:** What could go wrong? What would prevent it from working?
5. **Path to Validation:** What is the minimum viable experiment to test the core claim?
6. **If It Works:** What is the 10-year impact on space technology?

*SpaceX engineers do this with speculative propulsion concepts regularly. The format trains students in exactly the thinking that builds the future.*

---

### YEAR 3 — UNIT 8: CAPSTONE — SPACE MISSION & UNIFIED THEORY (15 Days)

**The Capstone Project**

Each student designs a complete mission architecture for one of the following:

| Mission Option | Baseline Physics | Frontier Extension |
|---------------|-----------------|-------------------|
| A: Mars One-Way | Hohmann transfer, radiation shielding, ISRU propellant | Nuclear thermal vs. chemical; dose analysis |
| B: Asteroid Deflection | Kinetic impactor momentum, DART analysis | Non-Newtonian perturbation from φ-model |
| C: Titan Submarine | Fluid dynamics in methane sea, pressure hull, power | QC material hull; RTG efficiency optimization |
| D: Interstellar Probe | Solar sail physics, relativistic kinematics | Natário slipstream channel; Zeckendorf routing |
| E: Space-Based Solar Power | Orbital mechanics, EM wave transmission, rectenna | Vacuum flux amplifier for beam efficiency |

#### Option D — Interstellar Probe: The Husmann Framework Applied

*This is the most ambitious and the most intellectually honest of the five options.*

**Phase 1 (conventional):** Calculate solar sail trajectory from Earth to 0.01c using laser push from a 10 GW phased array. Calculate transit time to Alpha Centauri (4.37 ly). Calculate relativistic corrections.

**Phase 2 (Natário framework):** The Natário warp drive is a mathematically valid solution to Einstein's field equations. Unlike Alcubierre, it does not require a bubble — it uses a directional slipstream that deforms spacetime in one direction. The Husmann framework's preferred mechanism is a 1D Natário slipstream:

v_eff = c × φ² × α (where α = 1/φ at the AAH critical point)

Therefore: v_eff = c × φ² × (1/φ) = c × φ ≈ 1.618c

And the light-ring velocity: v_LR = 2πc (exact, from the topology of the Cantor-set vacuum)

Students calculate:
1. Transit time to Teegarden's Star b (12.5 ly) at v_eff = 1.618c: **~7.7 years**
2. Energy required to establish the slipstream (order-of-magnitude estimate from vacuum energy density)
3. What experiment, realizable within 10 years, could constrain whether v_LR = 2πc is a real physical velocity?

**The honest closing statement students are required to write:**

*"I have applied the Husmann Decomposition framework to design an interstellar mission. The framework makes specific, mathematical predictions. I have identified [X] of these as experimentally testable within current technology, and [Y] as requiring capabilities we do not yet have. The framework may be correct, partially correct, or incorrect. My assessment of its probability of being substantially correct is [Z]%, based on the following reasoning: ..."*

---

## YEAR 3 ASSESSMENT ARCHITECTURE

| Component | Weight | Description |
|-----------|--------|-------------|
| Unit Exams (8 × 50 pts) | 30% | Calculus-level problems; 1 problem per exam is a novel derivation |
| Simulation Labs (weekly) | 15% | Repository scripts + student-authored code; graded on physics interpretation, not debugging |
| Patent Analysis Papers | 15% | 2 formal papers (Unit 7 + Capstone); graded on scientific reasoning quality |
| Research Presentations | 15% | Unit 7 pitch + Capstone presentation; peer-reviewed using SpaceX-style rubric |
| Capstone Portfolio | 20% | Complete mission architecture document, including assumptions, calculations, and critical self-assessment |
| Participation & Exit Tickets | 5% | Daily formative engagement |

---

## THREE-YEAR ASSESSMENT PROGRESSION

| Year | Emphasis | Primary Product |
|------|----------|----------------|
| 10th | Conceptual understanding; algebraic problem-solving | Exams + lab reports |
| 11th | Multi-step reasoning; computational verification; patent literacy | Problem sets + patent review + simulation labs |
| 12th | Original analysis; evidence-based evaluation of frontier science; mission design | Research portfolio + capstone + presentations |

---

## COMPUTATIONAL TOOLKIT — THREE-YEAR PROGRESSION

| Year | Skills Developed | Repository Tools Used |
|------|-----------------|----------------------|
| 10th | Reading Python output; plotting graphs; Euler method introduction | `basic_trajectory.py`, `phi_demo.py` |
| 11th | Writing simple scripts; modifying simulations; data analysis | `lattice_calibration.py`, `identity_proofs.py`, `nozzle_sim.py` |
| 12th | Full simulation authorship; numerical solvers; statistical analysis | `orbital_mechanics_sim.py`, `cosmology_match.py`, `phi_pipeline.py`, `aah_spectrum.py` |

---

## DIFFERENTIATION — THREE-YEAR FRAMEWORK

### Supporting Students Who Struggle
- Every concept has a "floor": the algebra-based version is always available regardless of year
- Simulation outputs can substitute for analytic derivations for students with math anxiety
- Patent analysis can be done at conceptual level (no equations required) for IEP/504 accommodations
- Oral defense option for all written assessments

### Supporting Advanced Students
- Every Tier 3 problem is designed to require techniques not yet taught — requiring the student to invent or research the approach
- Independent study pathway: advanced students may pursue one unit each year at graduate-reading-group level, using actual papers from arXiv
- Year 2 students who complete calculus early may begin Year 3 units in the second semester
- Physics Olympiad preparation materials available throughout

### Neurodivergent Learners
*This curriculum was designed with explicit awareness that many of the most important physicists in history were neurodivergent — and that the kind of pattern recognition, deep focus, and unconventional thinking that the school system often pathologizes is exactly the engine that drives theoretical breakthroughs.*

- Multiple representations: every concept visual, verbal, algebraic, computational, and physical simultaneously
- Predictable structure (5-phase lesson) removes daily uncertainty
- Special interest connections: if a student's deep interest is in any STEM-adjacent area, there is a way to connect it to this curriculum
- The Husmann Decomposition itself is framed as an example of what a mind that sees differently can produce — not as a curiosity, but as a model

---

## CLASSROOM NORMS — THE SCIENTIFIC CULTURE OF THIS ROOM

1. **Evidence over authority.** It doesn't matter who said it. What does the data say?
2. **Precise language.** In physics, "it depends" is the beginning of an answer, not the end.
3. **Wrong answers are data.** When your prediction fails, that's the most interesting moment in science.
4. **Frontier science is tentative.** "We don't know yet" is an acceptable and honorable answer.
5. **Critique the reasoning, not the person.** "That argument has a gap at step 3" — not "you're wrong."
6. **Curiosity is non-negotiable.** The only question that's not welcome is a question designed to make someone else feel small.

---

## RESOURCES & BIBLIOGRAPHY

### Established Textbooks
- OpenStax *Physics* (algebra-based) — free, all three years as reference
- Serway & Jewett, *Physics for Scientists and Engineers* (calculus-based) — Year 3
- Griffiths, *Introduction to Electrodynamics* — Year 3 reference for advanced students
- Nielsen & Chuang, *Quantum Computation and Quantum Information* — Year 3 QM extension

### SpaceX Technical Resources (Publicly Available)
- SpaceX Falcon 9 User's Guide (current edition)
- SpaceX Starship Updates (official blog)
- NASA DART Mission Science Team papers
- ISS Power System technical overview (NASA.gov)

### Research Framework
- Aubry & André (1980) — original AAH paper
- Shechtman et al. (1984) — quasicrystal discovery (Nobel Prize 2011)
- Natário (2002) — "Warp drive with zero expansion" (gr-qc/0110086)
- Husmann Decomposition Framework — GitHub Repository (unpublished, instructor-authored)
- USPTO Provisional Patents 63/995,401 through 63/996,533 (instructor portfolio)

### Computational Tools
- Python 3.x with NumPy, SciPy, Matplotlib
- GitHub repository: [github.com/thusmann5327/Unified_Theory_Physics](https://github.com/thusmann5327/Unified_Theory_Physics)
- OpenOrb (open-source orbital mechanics)
- GalaxSim (cosmological simulation)

---

*This curriculum was developed by Thomas Husmann, theoretical physicist, independent researcher, and founder of iBuilt LTD and Olympia Local Foods LLC — Hood Canal, Washington. It represents a conviction that the next generation of space-faring humans deserves to be taught physics not as a finished building but as a construction site: full of scaffolding, open questions, and the thrilling uncertainty of a universe that has not yet been fully explored.*

*The frontier is open. These students are invited to help map it.*

---
*Document version: March 2026 | Curriculum development: In progress | Grok (xAI) peer review integrated*
