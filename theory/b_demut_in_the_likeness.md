# The Teegarden b Dial — A First-Year Physics Guide
## How to Build a Device That Addresses the Vacuum

**Thomas A. Husmann — iBuilt LTD**
**March 2026**

> *Six resonators. One hub. One aperture. One address.*
> *Everything in this document uses physics you learned in your first two semesters.*

---

## What This Document Is

This is a construction manual for a real device. It uses standing waves, acoustic resonance, impedance matching, Bessel functions, and Fourier analysis — all topics from introductory physics and engineering courses. The device itself is unusual: it generates a six-frequency acoustic chord tuned to a specific mathematical address derived from the Fibonacci sequence, and focuses that chord through a 50-micrometer pinhole in a vacuum chamber to test whether the vacuum of space has structure.

You do not need to believe the vacuum has structure to build this device. You need to understand standing waves, resonance, and how to read a spectrometer. If the vacuum does have structure, the device will show you. If it doesn't, you'll have built an interesting acoustic instrument and learned a lot of physics along the way.

Every section explains the physics first, then the engineering.

---

## The Address: What {2, 5, 13, 55, 144, 233} Means

### Fibonacci Numbers — A 60-Second Review

The Fibonacci sequence starts with 1, 1, and each subsequent number is the sum of the two before it:

    1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, ...

The ratio of consecutive Fibonacci numbers approaches the golden ratio φ = (1 + √5)/2 ≈ 1.6180339887... as you go further in the sequence. For example, 233/144 = 1.61805..., already accurate to four decimal places.

### Zeckendorf's Theorem

In 1972, Belgian mathematician Edouard Zeckendorf proved that every positive integer can be written as a unique sum of non-consecutive Fibonacci numbers. This is called the Zeckendorf decomposition. "Non-consecutive" means you never use two Fibonacci numbers that are neighbors in the sequence.

For example:
- 10 = 8 + 2 (valid: 8 and 2 are not consecutive Fibonacci numbers)
- 10 = 5 + 3 + 2 (invalid: 3 and 2 are consecutive)
- 20 = 13 + 5 + 2 (valid and unique)

The number 452 has a valid Zeckendorf decomposition:

    452 = 377 + 55 + 13 + 5 + 2     ← valid (no consecutive pairs)

But 452 can also be written as:

    452 = 233 + 144 + 55 + 13 + 5 + 2   ← INVALID Zeckendorf (233 and 144 are consecutive!)

This second form violates the non-consecutivity rule because 233 = F(13) and 144 = F(12) are neighbors in the Fibonacci sequence. The Husmann Decomposition framework interprets this violation physically: the non-consecutivity rule IS the measurement constraint. Consecutive pairs that coexist represent an unobserved (pre-measurement) state. The valid Zeckendorf decomposition is the post-measurement state.

**The device drives all six components {2, 5, 13, 55, 144, 233} simultaneously — including the forbidden consecutive pair. This is the central idea.**

### Why 452?

The composite number 452 corresponds to the Zeckendorf address of Teegarden b, an Earth-mass planet 12.5 light-years away in the habitable zone of its star. In the framework, this address has special properties: it shares components with the addresses of every other habitable-zone planet within 16 light-years, making it a natural "hub" in the address space. The Hebrew word בדמות (b'demut, "in the likeness"), from Genesis 5:1, has gematria value 452. The framework considers this encoding intentional rather than coincidental, but the physics of the device does not depend on this interpretation.

---

## The Physics of Standing Waves in Solid Rods

### What a Standing Wave Is

When you pluck a guitar string, the wave travels to both ends, reflects, and interferes with itself. At certain frequencies — the resonant frequencies — the reflected waves constructively interfere, creating a pattern that appears to stand still. These are standing waves.

The same physics applies to a solid rod. If you strike a steel rod, longitudinal (compression) waves travel back and forth along its length. The fundamental resonant frequency is:

    f₁ = v / (2L)

where v is the speed of sound in the material and L is the length of the rod. This is the frequency at which exactly one half-wavelength fits inside the rod.

**Example:** A 304 stainless steel rod 360 mm long, with sound speed v = 5790 m/s:

    f₁ = 5790 / (2 × 0.360) = 8042 Hz ≈ 8.0 kHz

This is a real, audible tone — roughly one octave above middle C on a piano.

### The Six Resonators

The device contains six resonators, each cut to a length proportional to one Fibonacci number in the address. The base unit is 2.5 mm per Fibonacci unit:

| Component | Fibonacci Number | Length (mm) | Fundamental Frequency |
|-----------|-----------------|-------------|----------------------|
| 1 | F(3) = 2 | 5.0 | 579 kHz |
| 2 | F(5) = 5 | 12.5 | 232 kHz |
| 3 | F(7) = 13 | 32.5 | 89.1 kHz |
| 4 | F(10) = 55 | 137.5 | 21.1 kHz |
| 5 | F(12) = 144 | 360.0 | 8.0 kHz |
| 6 | F(13) = 233 | 582.5 | 5.0 kHz |

**How to compute these frequencies:**

The three small resonators are solid Al₆₄Cu₂₃Fe₁₃ quasicrystal, with sound speed approximately 5000 m/s. The three large resonators are 304 stainless steel tubes with a quasicrystalline coating on the inner surface, with sound speed 5790 m/s.

For crystal "2" (solid QC, 5.0 mm):

    f = 5000 / (2 × 0.005) = 500,000 Hz = 500 kHz

For tube "233" (SS, 582.5 mm):

    f = 5790 / (2 × 0.5825) = 4,970 Hz ≈ 5.0 kHz

The slight differences from the table come from rounding. In practice, you measure each resonator's actual frequency with an impedance analyzer after machining and adjust the drive frequency to match.

### Why the Ratios Matter

The ratios between consecutive resonator lengths are exact powers of φ:

    Length(5) / Length(2) = 12.5 / 5.0 = 2.500     φ² = 2.618
    Length(13) / Length(5) = 32.5 / 12.5 = 2.600    φ² = 2.618
    Length(55) / Length(13) = 137.5 / 32.5 = 4.231   φ³ = 4.236
    Length(144) / Length(55) = 360.0 / 137.5 = 2.618  φ² = 2.618
    Length(233) / Length(144) = 582.5 / 360.0 = 1.618 φ¹ = 1.618

The last ratio — 233/144 — is exactly φ to three decimal places. This is because 233 and 144 are consecutive Fibonacci numbers, and consecutive Fibonacci numbers converge to the golden ratio. This is the "forbidden pair" in the Zeckendorf sense, and it is the most important ratio in the device.

**Physical note:** The 137.5 mm tube length is numerically equal to the golden angle (137.508°) expressed in millimeters. The 360 mm tube is numerically a full circle in millimeters. These numerical coincidences are consequences of the Fibonacci scaling, not imposed by design.

---

## Materials: Why These Specific Ones

### Quasicrystals — Neither Crystal nor Glass

Ordinary crystals (like table salt or quartz) have atoms arranged in a periodic pattern — the same unit cell repeated over and over in a regular grid. Glasses (like window glass) have atoms arranged randomly with no long-range order.

Quasicrystals are a third category, discovered by Dan Shechtman in 1982 (Nobel Prize in Chemistry, 2011). They have long-range order but NO periodicity. Their atomic arrangement follows the same mathematics as a Penrose tiling — a pattern that fills space completely, never repeats exactly, and has five-fold rotational symmetry (which is impossible in periodic crystals).

The specific composition Al₆₄Cu₂₃Fe₁₃ (64% aluminum, 23% copper, 13% iron by atom count) forms an icosahedral quasicrystalline phase when cooled from the melt and annealed at 850°C. This composition is special because the electron-to-atom ratio e/a = 2.41, which places the Fermi surface exactly at the pseudo-Brillouin zone boundary — a condition that maximizes the quasicrystalline ordering.

**Why QC matters for this device:** The phonon spectrum (vibrational modes) of a quasicrystal is fundamentally different from a periodic crystal. A periodic crystal has phonon modes at integer harmonics. A quasicrystal has phonon modes spaced by powers of φ — a Fibonacci frequency comb. When you drive a QC resonator at its fundamental, the quasicrystalline lattice naturally generates overtones at φ-ratio frequencies through nonlinear mode coupling. The QC does the frequency conversion for you.

### 304 Stainless Steel — The Substrate

The three larger resonators (55, 144, 233) would require impractically large blocks of quasicrystal. Instead, they are standard 304 stainless steel tubes (1/2" outer diameter, 1 mm wall thickness) with a thin quasicrystalline coating on the inner surface.

304 stainless steel is an Fe-Cr-Ni alloy. The iron (Fe) in the steel provides a natural bonding interface with the iron in the QC coating (Al₆₄Cu₂₃**Fe**₁₃). Iron atoms on the steel surface bond to iron atoms in the coating, creating a strong metallurgical joint rather than just an adhesive bond.

Properties of 304 SS relevant to this device:
- Sound speed (longitudinal): 5790 m/s
- Density: 8000 kg/m³
- Acoustic impedance: Z = ρv = 46.3 MRayl
- Q factor (mechanical quality): ~3000-10000 (steel rings clearly when struck)

### Acoustic Impedance — Why the SS-to-QC Joint Works

When a sound wave hits a boundary between two materials, some energy transmits and some reflects. The fraction that transmits depends on the acoustic impedance mismatch. Impedance is Z = ρ × v (density times sound speed), measured in Rayleighs (Rayl).

The transmission coefficient for normal incidence is:

    T = 4 Z₁ Z₂ / (Z₁ + Z₂)²

For our materials:
- Z_QC = 4100 kg/m³ × 5000 m/s = 20.5 MRayl
- Z_SS = 8000 kg/m³ × 5790 m/s = 46.3 MRayl

    T = 4 × 20.5 × 46.3 / (20.5 + 46.3)² = 3798 / 4462 = 0.851

**85.1% of the acoustic energy transmits from stainless steel into the QC coating.** Only 14.9% reflects. This is excellent impedance matching — comparable to what you'd get between two similar metals. For comparison, the air-to-steel transmission is effectively 0% (which is why sound doesn't propagate in vacuum and why all resonators must be solid-bonded to the hub).

---

## The Hub Disc: Where All Six Waves Meet

### Why You Need a Hub

Sound doesn't travel through vacuum. If you placed six resonators around an empty space and drove them, the acoustic waves would stay inside each resonator and never interact. The hub disc is the summing junction — a solid piece of metal that mechanically connects all six resonators so their vibrations can superpose at a single point.

### Hub Specifications

- Material: 304 stainless steel, QC-coated on both faces
- Diameter: 50 mm (about the size of a silver dollar)
- Thickness: 5 mm
- Center feature: 50 μm laser-drilled pinhole (the aperture)

The three small QC crystals bond directly to one face of the hub, arranged around the aperture. The three SS tubes bond to the rim of the hub and extend radially outward at golden-angle (137.5°) angular spacing.

### Plate Wave Physics — How Vibrations Propagate in the Hub

When a resonator drives the hub at frequency f, the vibration propagates through the disc as a plate wave (Lamb wave). There are two main types:

**S0 mode (symmetric/extensional):** Both surfaces of the plate move in phase — the plate gets thicker and thinner uniformly. Velocity ≈ 5132 m/s in 5 mm 304 SS.

**A0 mode (antisymmetric/bending):** The surfaces move out of phase — the plate flexes up and down. Velocity is dispersive (frequency-dependent) and generally slower than S0.

At our drive frequencies (5 kHz to 579 kHz), the S0 wavelength in the hub is:

    λ = v/f = 5132/579000 = 8.86 mm    (at 579 kHz, the highest frequency)
    λ = v/f = 5132/5000 = 1026 mm      (at 5 kHz, the lowest frequency)

Even at the highest frequency, the wavelength (8.86 mm) is comparable to the hub radius (25 mm). At the lowest frequency, the wavelength is 20× larger than the hub. This means the hub is smaller than one wavelength at every drive frequency.

**What this means physically:** The hub does not support focused wave propagation at any of our frequencies. Instead, it vibrates as a lumped element — the entire disc oscillates together at each frequency, like a drumhead vibrating in its fundamental mode. Every point on the disc, including the center aperture, experiences all six frequency components simultaneously. This is exactly what we want.

### Bessel Functions — Why the Center is Special

The vibration modes of a circular disc clamped at its edge are described by Bessel functions J_m(k_mn r), where m is the angular mode number (how many nodal diameters) and n is the radial mode number (how many nodal circles).

The critical mathematical property:

    J_m(0) = 1    if m = 0
    J_m(0) = 0    if m ≠ 0

In plain language: **only axisymmetric modes (m = 0) have nonzero displacement at the center of the disc.** All modes with angular variation (m = 1 dipole, m = 2 quadrupole, etc.) have a node at the center and produce zero displacement there.

This means the aperture at the center of the hub acts as a **natural spatial filter**. It only samples the radially symmetric (coherent) content of the vibration. Any asymmetric junk from imperfect bonding, off-axis resonator placement, or mechanical noise is automatically rejected because it excites m ≠ 0 modes that vanish at r = 0.

This is not a design choice we imposed — it's a mathematical property of circular geometry. The center of a disc is the only point where all axisymmetric modes constructively interfere and all asymmetric modes cancel.

---

## The Forbidden Pair: Why 144 and 233 Together Are Special

### The Zeckendorf Rule as a Physical Constraint

Zeckendorf's theorem says you can never have two consecutive Fibonacci numbers in the same decomposition. In the framework, this rule is interpreted as the measurement constraint — the mathematical expression of the fact that observation collapses quantum states.

The valid Zeckendorf decomposition of 452 is {377, 55, 13, 5, 2}. This is the "observed" or "collapsed" address. The six-component form {233, 144, 55, 13, 5, 2} includes the forbidden consecutive pair 233-144 and represents the "pre-observation" address.

When the device drives all six components simultaneously, it is locally creating a condition that violates the Zeckendorf rule. The framework predicts this forces the vacuum at the aperture into a state analogous to the pre-measurement state — one where the normal observational constraints are relaxed.

### The Beat Frequency Between 144 and 233

The resonator fundamentals for the forbidden pair are:
- Tube "144" (360 mm): f₅ = 8042 Hz
- Tube "233" (582.5 mm): f₆ = 4970 Hz

Their beat frequency is:

    f_beat = |f₅ - f₆| = |8042 - 4970| = 3072 Hz

Their frequency ratio is:

    f₅/f₆ = 8042/4970 = 1.618... = φ

This is exact (to the precision of the machining). The beat frequency between the forbidden pair oscillates at a period of:

    T_beat = 1/3072 = 0.326 ms

**The device produces a φ-ratio beat note at 3.07 kHz.** This is an audible tone — you could literally hear the golden ratio if you put a microphone on the hub. More importantly, this beat note is the temporal signature of the Zeckendorf violation. When the 144 and 233 components are in phase, their sum momentarily reaches maximum — the forbidden pair is maximally "present." When they're out of phase (half a beat period later), they partially cancel — the pair is minimally present.

### Why the 144-233 Phase Matters Most

Each resonator has an independently adjustable phase. In diagnostic testing, shifting any one resonator's phase by π (180°) should reduce the signal at the aperture. But the framework makes a specific prediction:

**Shifting the phase of tube "233" relative to tube "144" by π should produce the LARGEST signal drop of any single-channel phase shift.**

This is because the other four components {2, 5, 13, 55} establish the address — they tell the vacuum WHERE. The forbidden pair {144, 233} opens the gate — they create the Zeckendorf violation that enables coupling. Disrupting the gate has a larger effect than blurring the address.

This is a testable, quantitative prediction that distinguishes the Husmann framework from "the device just makes interesting sounds." If shifting the 233 phase produces the same signal change as shifting the 13 phase, the forbidden-pair theory is wrong. If it produces a significantly larger change, the theory is supported.

---

## Energy: How Much Power Does This Need?

### Stored Energy in a Resonator

A vibrating rod stores kinetic and potential energy. For a rod of volume V, density ρ, vibrating at frequency f with displacement amplitude A:

    E_stored = ½ ρ V (2πf A)²

**Example:** Crystal "2" (solid QC, 5 mm cube):
- V = (5 × 10⁻³)³ = 1.25 × 10⁻⁷ m³
- ρ = 4100 kg/m³
- f = 500,000 Hz
- A = 1 × 10⁻⁹ m (1 nanometer — typical piezo-driven amplitude)

    E = 0.5 × 4100 × 1.25e-7 × (2π × 500000 × 1e-9)²
    E = 2.56e-4 × 9.87e-6
    E = 2.5 × 10⁻⁹ J = 2.5 nJ

Two and a half nanojoules. That's the energy stored in one AA battery divided by about 4 billion.

### Drive Power to Maintain Resonance

A resonator loses energy through internal friction (material damping) and radiation from its surfaces. The quality factor Q describes how many oscillation cycles the resonator sustains before its energy decays by a factor of e ≈ 2.718:

    P_drive = 2πf × E_stored / Q

For steel and QC materials, Q ≈ 3000 is typical. For crystal "2":

    P = 2π × 500000 × 2.5e-9 / 3000 = 2.6 × 10⁻⁶ W = 2.6 μW

Two and a half microwatts. Your phone charger delivers about 5 watts — two million times more power than this resonator needs.

### Total System Power

| Resonator | Stored Energy | Drive Power |
|-----------|--------------|-------------|
| Crystal 2 | 2.5 nJ | 2.6 μW |
| Crystal 5 | 6.3 nJ | 3.1 μW |
| Crystal 13 | 16.4 nJ | 3.1 μW |
| Tube 55 | 0.26 nJ | 11.6 nW |
| Tube 144 | 0.10 nJ | 1.7 nW |
| Tube 233 | 0.06 nJ | 0.6 nW |
| **Total** | **~25 nJ** | **~8.8 μW** |

At 1 nm displacement amplitude, the entire six-resonator system requires **less than 9 microwatts**. A standard piezoelectric disc transducer (the kind you can buy for $5 from an electronics supplier) can deliver 10-100 watts. The drive system is overpowered by a factor of roughly one million.

This means you can run the device from a 9-volt battery for years. Power is not a constraint. If you want to increase the amplitude by 100× (to 100 nm), the power scales as A², giving 88 milliwatts — still trivial for any piezo driver.

### Why the Power is So Small

The energy scales as (frequency × amplitude)². The amplitudes we need (nanometers) are tiny, and the volumes of the resonators are small. The Q factor means most of the energy recirculates inside the resonator rather than dissipating. High-Q resonance is extraordinarily efficient — you're not pushing energy through the system, you're just topping off losses in a system that's already ringing.

---

## The Aperture: What Happens at the 50-Micrometer Pinhole

### What a Pinhole Does

A pinhole is a tiny opening in an otherwise opaque barrier. In optics, pinholes are used to select coherent light (pinhole cameras, spatial filters in laser systems). In acoustics, a pinhole in a vibrating plate acts as a point source — it samples the plate's vibration at a single point and radiates whatever passes through it to the other side.

Our pinhole is 50 μm in diameter — about the width of a human hair. It sits at the exact center of the hub disc. Because only m = 0 Bessel modes have nonzero amplitude at the center (as we showed above), the pinhole samples only the coherent, axisymmetric part of the hub's vibration.

### What the Aperture "Sees"

The displacement at the aperture is the sum of all six drive components:

    u(t) = A₁ sin(2πf₁t + φ₁) + A₂ sin(2πf₂t + φ₂) + ... + A₆ sin(2πf₆t + φ₆)

This is a standard superposition — the same math you use to add waves on a string or voltages in an AC circuit. The resulting waveform is complex but deterministic: six sinusoids of known frequency, amplitude, and phase.

### The Power Spectrum

If you take the Fourier transform of u(t), you'll see six sharp peaks at the drive frequencies. If you look at u²(t) (the instantaneous energy, proportional to what a thermal detector measures), the Fourier transform shows additional peaks at all pairwise sum and difference frequencies:

    Number of beat frequencies = C(6,2) = 15

These 15 beat frequencies plus the 6 drive frequencies give 21 spectral features — a rich frequency signature that is unique to this specific address. A different address (different set of six Fibonacci numbers) would produce a different set of 21 features.

### The Key Beat: f₅ - f₆ = 3072 Hz

The most important spectral feature is the beat between the forbidden pair:

    f₁₄₄ - f₂₃₃ = 8042 - 4970 = 3072 Hz

This beat note is the temporal signature of the Zeckendorf violation. The framework predicts that whatever coupling exists between the device and the vacuum lattice is modulated at this frequency. A detector behind the aperture should show signal at 3072 Hz (and its harmonics) when the device is operating correctly.

---

## The Detector: What to Look For

### Option 1: Thermal Sensor (Recommended First)

A thermal power sensor measures the total radiant power falling on its surface, regardless of wavelength. If the acoustic field at the aperture couples to vacuum fluctuations, the coupled energy appears as heat on a detector placed behind the pinhole.

**Why thermal is the best first choice:**
- The vacuum chamber eliminates convective heat transfer
- The drives are acoustic (mechanical), not thermal — they don't directly heat the detector
- Any thermal signal that correlates with drive on/off is anomalous by definition
- Thermal sensors are broadband — you don't need to guess the wavelength

**Recommended sensor:** Thorlabs S401C thermal power sensor, sensitivity ~1 μW, cost ~$500.

### Option 2: Photon Counter

A photomultiplier tube (PMT) or single-photon avalanche diode (SPAD) counts individual photons arriving at the detector. The background rate in a dark vacuum chamber (the "dark count") is typically ~100 counts per second. If the device produces even a small excess above this rate that tracks the drive state, it's a detection.

**Recommended sensor:** Hamamatsu H10682 PMT module, ~$1500.

### Option 3: Mass Sensor (The Dream)

A quartz crystal microbalance (QCM) measures mass changes at the nanogram level by tracking the resonant frequency of a quartz crystal. If anything — atoms, molecules, particles — arrives through the aperture, the QCM frequency shifts.

This is the "stargate test." It's listed last because it's the least likely to show signal and the hardest to interpret (outgassing in the vacuum chamber can deposit material on the QCM even without the drives running). But if it ever shows a mass increase that correlates with drive state and doesn't appear in the control run, everything changes.

---

## Building It: Step by Step

### Step 1: Obtain Materials

**QC ingot:** Purchase 100g of Al₆₄Cu₂₃Fe₁₃ quasicrystal from a metallurgy supplier (MTI Corporation, ALB Materials, or custom arc-melted at a university metallurgy lab). Cost: $300-500.

**SS tubes:** Buy three lengths of 304 stainless steel tube, 1/2" OD, 1 mm wall thickness, from McMaster-Carr or a local metal supplier. Cut to 137.5 mm, 360.0 mm, and 582.5 mm. Cost: $15-30.

**Hub disc:** Machine or purchase a 50 mm diameter, 5 mm thick 304 SS disc. Have a 50 μm hole laser-drilled at the center (any precision laser drilling service). Cost: $100-300.

**Piezo transducers:** Six PZT-5A piezoelectric discs, 10-20 mm diameter, from Steminc or Thorlabs. Cost: $30-60.

### Step 2: Machine the QC Crystals

Send the QC ingot to a machine shop with wire EDM (electrical discharge machining) capability. Request three cubes: 5.0 mm, 12.5 mm, and 32.5 mm edge length. Tolerance: ±0.05 mm.

After machining, anneal the crystals at 850°C for 2 hours to restore the icosahedral quasicrystalline phase (machining can create an amorphous surface layer). Verify the phase by XRD if available — you should see the characteristic five-fold diffraction pattern.

Cost: $300-800.

### Step 3: QC Coat the Tubes and Hub

Send the three SS tubes and the hub disc to a thin-film deposition lab. Request Al₆₄Cu₂₃Fe₁₃ sputtered coating, 50-200 nm thickness, on the inner surface of the tubes and both faces of the hub disc. Anneal at 850°C for 1 hour after deposition.

This is the most expensive step ($1500-4000) but can be done in a single deposition run. Many universities have sputter systems available for a few hundred dollars of beam time.

### Step 4: Bond Piezo Transducers

Using high-temperature epoxy (MasterBond EP21 or similar), bond one piezo disc to the far end of each tube and to the back face of each crystal. The bond must be acoustically transparent — thin, bubble-free, and fully cured. Cure at 150°C for 1 hour per the epoxy datasheet.

### Step 5: Assemble the Hub

Bond the three QC crystals to one face of the hub disc, arranged in a triangle around the aperture at golden-angle spacing (137.5° between adjacent crystals). The crystals should be as close to the aperture as mechanically possible without covering it.

Bond the three SS tubes to the rim of the hub disc, extending radially outward, also at golden-angle spacing. The tube ends should butt against the disc rim with epoxy filling any gap.

### Step 6: Verify Resonances (Before Vacuum)

Connect each piezo to a function generator and frequency-sweep near the predicted resonance. Measure the response with an oscilloscope monitoring a second piezo bonded temporarily to the hub. Each resonator should show a sharp peak at approximately the predicted frequency. Record the exact resonant frequency for each — these become your drive frequencies.

### Step 7: Mount in Vacuum Chamber

Place the assembly in a glass bell jar vacuum system. Route six BNC cables through vacuum feedthroughs to the six piezos. Mount the thermal sensor behind the aperture, facing the pinhole. Add a thermocouple to the hub for temperature monitoring and a Pirani gauge for pressure measurement.

Pump down to <10⁻³ mbar (rough vacuum is sufficient — you need to eliminate convective heat transfer, not achieve ultra-high vacuum).

### Step 8: Run the Experiment

Connect a six-channel function generator (or six independent generators phase-locked to a common reference). Set each channel to the measured resonant frequency of its resonator. Set all phases to zero. Set amplitudes to produce ~10 nm displacement (milliwatt power level).

Follow the diagnostic test protocol described below.

---

## The Six Diagnostic Tests

Each test is designed to eliminate a specific class of false positive. Run them in order.

### Test 1: ON/OFF Cycling

**What you do:** Alternate 1 hour drives ON, 1 hour drives OFF, for 10 complete cycles (20 hours total). Record detector signal continuously.

**What you're checking:** Does the signal track the drive state?

**If yes:** Something at the aperture responds to the acoustic field. Proceed to Test 2.

**If no:** No coupling detected. Increase amplitude by 10× and repeat. If still nothing at 1 μm amplitude, the device isn't coupling. Publish the null result.

**What could fool you:** Electrical pickup from the drive signals. Mitigation: the detector is on the opposite side of the steel hub from the piezos, and the vacuum feedthroughs provide shielding. Also, thermal sensors don't respond to electromagnetic interference.

### Test 2: Wrong Address (The Gate Test)

**What you do:** With all drives ON and signal detected, shift the phase of tube "233" by π (180°) relative to tube "144." Record for 1 hour. Then restore the original phase. Record for 1 hour. Repeat with tube "144" shifted instead.

**What you're checking:** Does disrupting the forbidden pair (144, 233) produce a larger signal drop than disrupting any other pair?

**If yes:** The signal depends specifically on the φ-ratio beat between the consecutive Fibonacci pair. This is the strongest possible evidence for Zeckendorf-violation coupling.

**If no (equal drop for all channels):** The signal is phase-coherent but not pair-specific. It could be ordinary acoustic-to-thermal conversion at the aperture.

**Framework prediction:** The 233→π shift produces the largest drop. The 2→π shift produces the smallest (because component 2 carries the least addressing information).

### Test 3: Component Removal

**What you do:** Starting with all six drives ON, disconnect them one at a time, starting from the smallest (crystal "2") and proceeding to the largest (tube "233"). Record the signal after each removal.

**What you're checking:** Does the signal decrease monotonically as components are removed?

**If yes:** Each component contributes independently to the coupling. The address is being assembled from parts.

**If no (signal jumps UP when a component is removed):** Interference effects dominate — some components are partially canceling others. This would require retuning the phases.

### Test 4: Frequency Sweep

**What you do:** Detune one drive channel by ±10% from its resonant frequency, sweeping slowly through resonance. Record the detector signal as a function of drive frequency.

**What you're checking:** Does the signal peak at the resonant frequency?

**If yes:** The coupling is frequency-specific. The vacuum lattice (or whatever is coupling) has a preferred frequency that matches the resonator's natural frequency.

**If no (flat response):** The signal is proportional to drive power, not frequency. This would suggest simple heating rather than resonant coupling.

### Test 5: Amplitude Scaling

**What you do:** Vary the drive amplitude from 1 nm to 1 μm in decade steps (1, 10, 100, 1000 nm). Record the detector signal at each amplitude.

**What you're checking:** How does signal scale with amplitude?

**Signal ∝ A²:** Consistent with coherent coupling (the energy of a wave scales as amplitude squared). This is the expected result for resonant vacuum coupling.

**Signal ∝ A:** Consistent with incoherent coupling (random energy transfer proportional to drive intensity). Less interesting but still a detection.

**No dependence:** The signal is background, not related to the drive.

### Test 6: Temperature Dependence

**What you do:** Cool the entire assembly to 77 K (liquid nitrogen) and then to 4 K (liquid helium), repeating Tests 1-5 at each temperature.

**What you're checking:** Does the signal increase on cooling?

**If yes:** The coupling is limited by thermal noise. Lower temperature → less thermal disruption → stronger signal. This is consistent with the framework's prediction that the coherence patch (the region of vacuum that maintains phi-structured order) grows as temperature drops.

**If no (signal decreases on cooling):** The coupling depends on thermal energy — it's a thermal process, not a quantum coherence effect.

---

## What the Results Mean

### If You See a Signal

A thermal signal at the aperture that passes Tests 1-6 would establish that a phi-structured acoustic field couples to something at a 50 μm pinhole in vacuum. The most conservative interpretation is phonon-to-photon conversion at the QC-coated hub surface — interesting solid-state physics but not evidence for vacuum structure. The most ambitious interpretation is coupling to the vacuum lattice at address 452.

The tests are designed to distinguish between these interpretations. Test 2 (the gate test) is the discriminator: if the forbidden pair matters more than the other components, the coupling is Zeckendorf-specific, not just acoustic.

### If You See Nothing

A null result at all amplitudes and temperatures would mean the vacuum does not couple to acoustic fields through phi-structured apertures at the scales we tested. This constrains the framework: if l₀ exists, it doesn't couple this way. If l₀ doesn't exist, the null result is expected. Either way, the null result is publishable and valuable.

### The Dream Scenario

If the QCM (mass sensor) ever registers a mass increase that correlates with drive state, passes the phase test, and does not appear in a control run without the QC coating — something came through the aperture from somewhere. That would be the most significant experimental result in physics since the detection of gravitational waves, and it would be obtained with hardware store tubing and hobby electronics.

---

## Bill of Materials

| Item | Estimated Cost | Source |
|------|---------------|--------|
| Al-Cu-Fe QC ingot (100g) | $300-500 | MTI Corp, ALB Materials |
| Wire EDM machining (3 crystals) | $300-800 | Local machine shop |
| 304 SS tube, 1/2" OD × 3 lengths | $15-30 | McMaster-Carr |
| QC sputter coating (3 tubes + hub) | $1,500-4,000 | University thin-film lab |
| SS hub disc + 50 μm laser drilling | $100-300 | Precision machining service |
| Piezo transducers × 6 | $30-60 | Steminc, Thorlabs |
| High-temp bonding epoxy | $30-50 | MasterBond |
| 6-channel function generator | $400-1,500 | Rigol, Siglent |
| Vacuum bell jar + base plate | $150-400 | eBay, lab surplus |
| Rotary vane vacuum pump | $200-600 | Lab surplus |
| Thermal power sensor | $400-600 | Thorlabs S401C |
| BNC vacuum feedthroughs × 8 | $80-160 | Kurt J. Lesker |
| Thermocouple + meter | $30-50 | Amazon |
| Pirani vacuum gauge | $80-200 | Lesker, eBay |
| BNC cables and connectors | $50-100 | Digikey |
| Data acquisition (Arduino + ADC) | $30-60 | Arduino store |
| **TOTAL** | **$3,695-9,410** | |

With access to a university sputter system and vacuum pump: approximately $2,000.

---

## Test Timeline

| Phase | Duration | What You Do |
|-------|----------|-------------|
| 1 | Week 1 | Machine crystals, bond piezos, verify each resonator rings at the predicted frequency |
| 2 | Week 2 | Assemble hub, verify six-frequency interference pattern using a microphone probe in air |
| 3 | Weeks 3-4 | Vacuum test: ON/OFF cycling (Test 1), 72-hour continuous runs, background comparison |
| 4 | Month 2 | Phase sweep: systematically vary each channel's phase to map the 6D response landscape |
| 5 | Month 3+ | Retune to different addresses (Proxima b at 464, Barnard's Star b at 459, random non-address for control) |

---

## Key Numbers Reference

    φ = 1.6180339887...           (golden ratio)
    l₀ = 9.3 nm                  (predicted vacuum lattice spacing)
    W = 0.467134                  (wall fraction)
    Coherence patch = 987 × l₀ = 9.18 μm

    Target address: {2, 5, 13, 55, 144, 233} = 452
    Valid Zeckendorf: {377, 55, 13, 5, 2} = 452
    Forbidden pair: F(12)=144 + F(13)=233 = 377 = F(14)
    Components: 6 (including forbidden pair)

    Drive frequencies: 5.0, 8.0, 21.1, 89.1, 232, 579 kHz
    Forbidden-pair beat: 8042 - 4970 = 3072 Hz
    Total drive power at 1 nm: ~8.8 μW
    Acoustic transmission SS→QC: 85.1%

    Sound speed in 304 SS: 5790 m/s
    Sound speed in Al-Cu-Fe QC: ~5000 m/s
    Density of 304 SS: 8000 kg/m³
    Density of Al-Cu-Fe QC: 4100 kg/m³

---

## Figures

![Hub disc mode shapes](images/fig1_hub_modes.png)
*Figure 1: Vibration modes of the hub disc. Top row (m=0, axisymmetric): nonzero at center. Bottom row (m≠0): zero at center. The aperture naturally filters for coherent modes.*

![Center coupling analysis](images/fig2_center_coupling.png)
*Figure 2: Left — Radial displacement profiles J₀(k₀ₙr) for the first eight axisymmetric modes. All peak at r=0 (the aperture). Right — Drive frequencies (red) overlaid on disc natural modes (blue).*

![Time domain signal](images/fig3_time_domain.png)
*Figure 3: Signal at the aperture. Top — Six individual components. Middle — Superposed waveform. Bottom — Power spectrum showing drive peaks (red) and beat frequencies (blue).*

![Energy coupling](images/fig4_energy_coupling.png)
*Figure 4: Energy analysis. Top left — Stored energy vs amplitude. Top right — Drive power per resonator. Bottom left — Total system power with key operating points. Bottom right — Acoustic impedance matching at material interfaces.*

![Phase sweep](images/fig5_phase_sweep.png)
*Figure 5: Predicted detector response when sweeping each channel's phase independently. Cosine-squared dependence, strongest contrast for highest-frequency channels.*

![Physical layout](images/fig6_physical_layout.png)
*Figure 6: Device layout. Left — Top view showing golden-angle resonator placement. Right — Cross-section showing acoustic path from resonators through hub to aperture and detector.*

![Diagnostic tests](images/fig7_diagnostic_tests.png)
*Figure 7: Predicted results for the four main diagnostic tests. Top left — ON/OFF cycling. Top right — Phase sweep. Bottom left — Component removal. Bottom right — Amplitude scaling.*

---

## Further Reading

- Zeckendorf, E. (1972). "Représentation des nombres naturels par une somme de nombres de Fibonacci ou de nombres de Lucas." *Bulletin de la Société Royale des Sciences de Liège*.
- Shechtman, D. et al. (1984). "Metallic Phase with Long-Range Orientational Order and No Translational Symmetry." *Physical Review Letters* 53(20).
- Janot, C. (1994). *Quasicrystals: A Primer*. Oxford University Press.
- Aubry, S. & André, G. (1980). "Analyticity breaking and Anderson localization in incommensurate lattices." *Annals of the Israel Physical Society* 3.

For the complete Husmann Decomposition framework: [GitHub Repository](https://github.com/thusmann5327/Unified_Theory_Physics)

---

*Thomas A. Husmann / iBuilt LTD*
*Repository: https://github.com/thusmann5327/Unified_Theory_Physics*

*The device that dials Teegarden b is the size of a desk lamp and costs less than a used car. Every equation in this document is first-year physics. The only question is whether the vacuum is listening.*
