"""
PHI-STRUCTURED UNIVERSE SIMULATOR
Husmann Decomposition Framework | March 6, 2026
Flask Backend with Server-Side Rendering and MS SQL Integration

Earth's sector visualization with Milky Way extrapolation
"""

from flask import Flask, render_template, jsonify, request
import math
import json
from datetime import datetime

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# ═══════════════════════════════════════════════
# PHI CONSTANTS - Single Source of Truth
# ═══════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2        # 1.6180339887...
PHI2 = PHI * PHI                     # 2.6180339887...
PHI3 = PHI2 * PHI                    # 4.2360679774...
PHI4 = PHI3 * PHI                    # 6.8541019662...
INV_PHI = 1 / PHI                    # 0.6180339887...
INV_PHI2 = 1 / PHI2                  # 0.3819660112...
INV_PHI3 = 1 / PHI3                  # 0.2360679774...
INV_PHI4 = 1 / PHI4                  # 0.1459155902...
GOLDEN_ANGLE = 360 / PHI2            # 137.5077640500...degrees

# Self-referential hinge constant
HINGE_CONST = PHI ** (-1/PHI)        # 0.7427429446...

# Wall fraction (three-layer wall impedance)
WALL_FRACTION = 2 * INV_PHI4 + HINGE_CONST / PHI3  # 0.467134

L_PLANCK = 1.616255e-35              # meters (CODATA 2018)
CALIB_FACTOR = 1.0224065900385806    # makes n=128 exactly 9.3 nm

# ═══════════════════════════════════════════════
# SOLAR SYSTEM DATA (Earth's Sector)
# ═══════════════════════════════════════════════

# Distances from Sun in AU (Astronomical Units)
SOLAR_SYSTEM = {
    'sun': {'distance_au': 0, 'radius_km': 696340, 'color': '#FFD700', 'name': 'Sun'},
    'mercury': {'distance_au': 0.387, 'radius_km': 2439.7, 'color': '#B5B5B5', 'name': 'Mercury'},
    'venus': {'distance_au': 0.723, 'radius_km': 6051.8, 'color': '#E6C229', 'name': 'Venus'},
    'earth': {'distance_au': 1.0, 'radius_km': 6371, 'color': '#4A90D9', 'name': 'Earth'},
    'mars': {'distance_au': 1.524, 'radius_km': 3389.5, 'color': '#D14B28', 'name': 'Mars'},
    'jupiter': {'distance_au': 5.203, 'radius_km': 69911, 'color': '#C88B3A', 'name': 'Jupiter'},
    'saturn': {'distance_au': 9.537, 'radius_km': 58232, 'color': '#E4C98B', 'name': 'Saturn'},
    'uranus': {'distance_au': 19.191, 'radius_km': 25362, 'color': '#7BC8D4', 'name': 'Uranus'},
    'neptune': {'distance_au': 30.069, 'radius_km': 24622, 'color': '#4B70DD', 'name': 'Neptune'},
    'pluto': {'distance_au': 39.482, 'radius_km': 1188.3, 'color': '#C9A57C', 'name': 'Pluto'},
    'kuiper_inner': {'distance_au': 30, 'radius_km': 0, 'color': '#555555', 'name': 'Kuiper Belt (inner)'},
    'kuiper_outer': {'distance_au': 50, 'radius_km': 0, 'color': '#555555', 'name': 'Kuiper Belt (outer)'},
    'oort_inner': {'distance_au': 2000, 'radius_km': 0, 'color': '#333333', 'name': 'Oort Cloud (inner)'},
    'oort_outer': {'distance_au': 100000, 'radius_km': 0, 'color': '#222222', 'name': 'Oort Cloud (outer)'},
}

# 1 AU in meters
AU_METERS = 1.496e11

# ═══════════════════════════════════════════════
# SOLAR EVOLUTION & STELLAR PHYSICS
# The Sun's luminosity evolves over main sequence lifetime
# This is critical for understanding planetary habitability
# ═══════════════════════════════════════════════

# Solar constants
L_SUN_TODAY = 3.828e26      # Watts (present-day solar luminosity)
T_SUN_SURFACE = 5778        # Kelvin
R_SUN = 6.957e8             # meters
SOLAR_AGE_GYR = 4.57        # Gyrs (age of solar system)
SOLAR_MASS_KG = 1.989e30    # kg

# Stefan-Boltzmann constant
STEFAN_BOLTZMANN = 5.670374e-8  # W/(m²·K⁴)

def solar_luminosity_at_time(time_ga):
    """
    Calculate solar luminosity at a given time in Earth's past.

    The Sun's luminosity increases ~1% per 100 Myr due to core contraction
    and increased fusion rate. At formation (4.57 Ga), L ≈ 0.70 × L_today.

    Formula: L(t) = L_today / (1 + 0.4 × (1 - t_elapsed/t_total))
    Where t_elapsed is time since formation.

    Args:
        time_ga: Time in Ga before present (0 = now, 4.57 = formation)
    Returns:
        Luminosity ratio relative to today (0.0-1.0+)
    """
    if time_ga <= 0:
        return 1.0
    if time_ga >= SOLAR_AGE_GYR:
        return 0.70  # Minimum at formation

    # Linear approximation of main sequence evolution
    # More accurate would use stellar evolution models
    t_elapsed = SOLAR_AGE_GYR - time_ga  # Time since formation
    t_fraction = t_elapsed / SOLAR_AGE_GYR

    # Luminosity increases from 0.70 to 1.0 over solar lifetime
    luminosity_ratio = 0.70 + 0.30 * t_fraction

    return luminosity_ratio

def equilibrium_temperature(distance_au, luminosity_ratio=1.0, albedo=0.3):
    """
    Calculate equilibrium temperature of a body without greenhouse effect.

    T_eq = (L × (1-A) / (16 × π × σ × d²))^0.25

    Args:
        distance_au: Distance from Sun in AU
        luminosity_ratio: Solar luminosity relative to today
        albedo: Reflectivity (0-1), Earth ≈ 0.3
    Returns:
        Equilibrium temperature in Kelvin
    """
    L = L_SUN_TODAY * luminosity_ratio
    d = distance_au * AU_METERS

    # Absorbed power per unit area
    absorbed = L * (1 - albedo) / (16 * math.pi * d * d)

    # Stefan-Boltzmann gives temperature
    T_eq = (absorbed / STEFAN_BOLTZMANN) ** 0.25

    return T_eq

def greenhouse_temperature(T_eq, co2_percent, ch4_ppm=0, h2o_relative=1.0):
    """
    Calculate surface temperature including greenhouse warming.

    Calibrated greenhouse model:
    - Present-day Earth: T_eq ≈ 255K → T_surface ≈ 288K (ΔT = 33K)
    - CO2 contributes logarithmically (~3K per doubling)
    - CH4 stronger per molecule but less abundant
    - H2O provides positive feedback

    Args:
        T_eq: Equilibrium temperature without greenhouse
        co2_percent: CO2 as percentage of atmosphere (present = 0.04%)
        ch4_ppm: Methane in ppm (present ≈ 1.9 ppm)
        h2o_relative: Water vapor relative to present (affects feedback)
    Returns:
        Surface temperature in Kelvin
    """
    # Present-day baseline greenhouse effect = 33K
    # Breakdown: CO2=7K, H2O=21K, CH4+N2O+O3=5K
    BASE_GREENHOUSE = 33.0  # Present-day total greenhouse warming

    # Present-day references
    co2_present = 0.04   # 400 ppm as percentage
    ch4_present = 1.9    # ppm

    # CO2 contribution (logarithmic sensitivity)
    # Each doubling adds ~3K (climate sensitivity)
    # At present: co2_warming = 0 (no change from baseline)
    if co2_percent > 0:
        co2_factor = math.log2(max(0.0001, co2_percent) / co2_present)
        co2_warming = 3.0 * co2_factor  # ~3K per doubling from present
    else:
        co2_warming = -30  # Nearly no atmosphere

    # Methane contribution (stronger per molecule)
    # ~0.5K per doubling from present levels
    if ch4_ppm > 0:
        ch4_factor = math.log2(max(0.1, ch4_ppm) / ch4_present)
        ch4_warming = 0.5 * ch4_factor
    else:
        ch4_warming = 0

    # Water vapor feedback
    # More water = more greenhouse, but depends on temperature
    # At h2o_relative=1.0, contribution = 0 (baseline)
    h2o_warming = 5.0 * (h2o_relative - 1.0)  # ±5K per doubling of water

    # Total greenhouse = baseline + changes from present
    delta_T = BASE_GREENHOUSE + co2_warming + ch4_warming + h2o_warming

    # Clamp to physical limits (can't have negative greenhouse in thick atmosphere)
    delta_T = max(-10, min(250, delta_T))

    return T_eq + delta_T

# ═══════════════════════════════════════════════
# TECTONIC VIABILITY MODEL
# Tectonics requires: internal heat, right viscosity, water
# ═══════════════════════════════════════════════

# Radioactive heat production (W/kg) for key isotopes
RADIOACTIVE_HEAT = {
    'U238': 9.46e-5,   # W/kg
    'U235': 5.69e-4,   # W/kg
    'Th232': 2.64e-5,  # W/kg
    'K40': 2.92e-5,    # W/kg
}

# Earth's present internal heat budget
EARTH_INTERNAL_HEAT_TW = 47  # TeraWatts total
EARTH_RADIOACTIVE_TW = 20    # TW from radioactive decay
EARTH_PRIMORDIAL_TW = 27     # TW from primordial heat (cooling)

def radioactive_heat_at_time(time_ga, ree_enrichment=1.0):
    """
    Calculate radioactive heat production at a given time in the past.

    Radioactive isotopes decay, so early Earth had MORE heat production.
    Half-lives: U238=4.47Gyr, U235=0.704Gyr, Th232=14.0Gyr, K40=1.25Gyr

    Args:
        time_ga: Time in Ga before present
        ree_enrichment: REE enrichment factor (affects U, Th abundance)
    Returns:
        Heat production ratio relative to present-day Earth
    """
    # Half-lives in Gyr
    half_lives = {'U238': 4.47, 'U235': 0.704, 'Th232': 14.0, 'K40': 1.25}

    # Present-day contributions (fractions of total radioactive heat)
    contributions = {'U238': 0.39, 'U235': 0.02, 'Th232': 0.40, 'K40': 0.19}

    total_ratio = 0
    for isotope, half_life in half_lives.items():
        # N(t) = N(0) × 2^(-t/half_life)
        # Going BACK in time, so isotopes were MORE abundant
        abundance_ratio = 2 ** (time_ga / half_life)
        total_ratio += contributions[isotope] * abundance_ratio

    # REE enrichment affects U and Th (but not K)
    ree_factor = 1.0 + 0.2 * (ree_enrichment - 1.0)  # 20% sensitivity

    return total_ratio * ree_factor

def tectonic_vigor(radius_km, mass_ratio_earth=1.0, time_ga=0,
                   ree_enrichment=1.0, water_mass_fraction=0.001):
    """
    Calculate tectonic vigor index (0-1 scale).

    Tectonics requires:
    1. Sufficient internal heat (drives mantle convection)
    2. Right planet size (too small = cooled, too large = stagnant lid)
    3. Water (lubricates subduction zones)
    4. Right mantle viscosity (composition-dependent)

    Args:
        radius_km: Planet radius
        mass_ratio_earth: Mass relative to Earth
        time_ga: Time in Ga before present
        ree_enrichment: REE/radioactive element enrichment
        water_mass_fraction: Water as fraction of planet mass
    Returns:
        Tectonic vigor (0 = no tectonics, 1 = Earth-like)
    """
    # Size factor: Earth is optimal, smaller cools faster, larger has stagnant lid
    r_ratio = radius_km / 6371
    if r_ratio < 0.4:
        size_factor = 0  # Too small (cooled solid)
    elif r_ratio < 0.7:
        size_factor = (r_ratio - 0.4) / 0.3  # Mars-size, marginal
    elif r_ratio < 1.5:
        size_factor = 1.0  # Earth to super-Earth, optimal
    elif r_ratio < 2.0:
        size_factor = 1.0 - (r_ratio - 1.5) / 0.5  # Large, approaching stagnant lid
    else:
        size_factor = 0.1  # Very large, stagnant lid likely

    # Heat factor: need enough internal heat for convection
    heat_ratio = radioactive_heat_at_time(time_ga, ree_enrichment)
    heat_factor = min(1.0, heat_ratio / 1.5)  # Normalize to ~1.5× present

    # Water factor: need water to lubricate subduction
    # Earth has ~0.023% water by mass in oceans, more in mantle
    water_ratio = water_mass_fraction / 0.001
    if water_ratio < 0.1:
        water_factor = water_ratio / 0.1  # Too dry
    elif water_ratio < 5:
        water_factor = 1.0  # Optimal range
    else:
        water_factor = max(0.3, 1.0 - (water_ratio - 5) / 20)  # Too wet can suppress

    # Combine factors
    vigor = size_factor * heat_factor * water_factor

    # Age factor: young planets need time to initiate tectonics
    # Earth's tectonics may have started ~3.8 Ga
    age_since_formation = SOLAR_AGE_GYR - time_ga
    if age_since_formation < 0.5:
        age_factor = age_since_formation / 0.5  # Ramp up over first 500 Myr
    else:
        age_factor = 1.0

    vigor *= age_factor

    return max(0, min(1, vigor))

def carbon_silicate_cycle_rate(tectonic_vigor, temperature_K, co2_partial_pressure):
    """
    Model the carbon-silicate weathering cycle.

    This is THE key feedback that stabilizes Earth's climate:
    - Weathering: CO2 + CaSiO3 → CaCO3 + SiO2 (removes CO2)
    - Volcanism: CaCO3 → CO2 + CaO (releases CO2)
    - Weathering rate increases with temperature and CO2
    - Volcanism rate depends on tectonics

    Args:
        tectonic_vigor: 0-1 scale
        temperature_K: Surface temperature
        co2_partial_pressure: CO2 pressure in bars
    Returns:
        dict with weathering and volcanism rates relative to present
    """
    # Weathering rate: increases with temperature (Arrhenius-like)
    # and with CO2 concentration (more acid rain)
    T_ref = 288  # Present Earth
    co2_ref = 4e-4  # 400 ppm in bars

    # Temperature dependence (doubles every ~10K)
    if temperature_K > 200:
        temp_factor = 2 ** ((temperature_K - T_ref) / 10)
    else:
        temp_factor = 0  # Frozen, no weathering

    # CO2 dependence (weaker, ~30% per doubling)
    if co2_partial_pressure > 0:
        co2_factor = (co2_partial_pressure / co2_ref) ** 0.3
    else:
        co2_factor = 0

    weathering_rate = temp_factor * co2_factor

    # Volcanism rate: proportional to tectonic vigor
    volcanism_rate = tectonic_vigor

    # Net CO2 flux (positive = accumulating)
    net_co2_flux = volcanism_rate - weathering_rate

    return {
        'weathering_rate': weathering_rate,
        'volcanism_rate': volcanism_rate,
        'net_co2_flux': net_co2_flux,
        'equilibrium': abs(net_co2_flux) < 0.1  # Near balance
    }

# ═══════════════════════════════════════════════
# INTEGRATED EARTH EVOLUTION MODEL
# Combines solar evolution + greenhouse + tectonics
# ═══════════════════════════════════════════════

def earth_climate_at_time(time_ga, co2_override=None, tectonic_override=None):
    """
    Calculate Earth's climate state at a given time.

    This integrates:
    1. Solar luminosity (faint young sun)
    2. Greenhouse warming (CO2, CH4, H2O)
    3. Tectonic feedback (carbon-silicate cycle)

    Args:
        time_ga: Time in Ga before present
        co2_override: Override CO2 percentage (for experiments)
        tectonic_override: Override tectonic vigor (for experiments)
    Returns:
        dict with climate state
    """
    # Solar luminosity at this time
    L_ratio = solar_luminosity_at_time(time_ga)

    # Equilibrium temperature without greenhouse
    T_eq = equilibrium_temperature(1.0, L_ratio, albedo=0.3)

    # REE enrichment (constant for Earth)
    ree = 1.44  # From formation bracket

    # Tectonic vigor at this time
    if tectonic_override is not None:
        tectonic = tectonic_override
    else:
        tectonic = tectonic_vigor(6371, 1.0, time_ga, ree, 0.001)

    # CO2 level - this is the key variable
    # Early Earth had much higher CO2 to compensate for faint sun
    if co2_override is not None:
        co2_pct = co2_override
    else:
        # Estimate historical CO2 (simplified)
        if time_ga > 4.0:
            co2_pct = 70.0  # Hadean, very high
        elif time_ga > 2.5:
            co2_pct = 10.0 + 20 * (time_ga - 2.5) / 1.5  # Archean, high
        elif time_ga > 0.6:
            co2_pct = 0.5 + 9.5 * (time_ga - 0.6) / 1.9  # Proterozoic
        elif time_ga > 0.3:
            co2_pct = 0.1 + 0.4 * (time_ga - 0.3) / 0.3  # Paleozoic
        else:
            co2_pct = 0.04 + 0.06 * (time_ga / 0.3)  # Recent

    # Methane (significant in Archean before O2)
    if time_ga > 2.4:  # Pre-GOE
        ch4_ppm = 1000 * (time_ga - 2.4) / 1.6  # Peak ~1000 ppm
    else:
        ch4_ppm = 2  # Present-like after GOE

    # Surface temperature with greenhouse
    T_surface = greenhouse_temperature(T_eq, co2_pct, ch4_ppm)

    # Water state
    if T_surface > 373:
        water_state = 'steam'
        ocean_coverage = 0
    elif T_surface > 273:
        water_state = 'liquid'
        # Ocean coverage evolved over time
        if time_ga > 4.2:
            ocean_coverage = 0
        elif time_ga > 3.8:
            ocean_coverage = 0.3 + 0.3 * (4.2 - time_ga) / 0.4
        else:
            ocean_coverage = 0.7  # Roughly constant since Archean
    else:
        water_state = 'ice'
        ocean_coverage = 0

    # Carbon cycle state
    if tectonic > 0.1 and T_surface > 273:
        co2_bars = co2_pct / 100  # Convert to bars (rough)
        carbon_cycle = carbon_silicate_cycle_rate(tectonic, T_surface, co2_bars)
    else:
        carbon_cycle = {
            'weathering_rate': 0,
            'volcanism_rate': 0,
            'net_co2_flux': 0,
            'equilibrium': False
        }

    return {
        'time_ga': time_ga,
        'solar_luminosity_ratio': L_ratio,
        'T_equilibrium_K': T_eq,
        'T_surface_K': T_surface,
        'co2_percent': co2_pct,
        'ch4_ppm': ch4_ppm,
        'tectonic_vigor': tectonic,
        'water_state': water_state,
        'ocean_coverage': ocean_coverage,
        'carbon_cycle': carbon_cycle,
        'habitable': water_state == 'liquid' and T_surface < 350,
        'radioactive_heat_ratio': radioactive_heat_at_time(time_ga, ree),

        # Derived insights
        'faint_sun_problem': L_ratio < 0.85 and T_surface > 273,
        'greenhouse_compensation_K': T_surface - T_eq,
        'climate_stable': carbon_cycle.get('equilibrium', False)
    }

def why_water_without_tectonics():
    """
    Explain why a water planet could exist without tectonics,
    and why Earth specifically has both.

    Key insight: Water and tectonics are COUPLED on Earth through
    the carbon-silicate cycle, but other water worlds are possible.
    """
    return {
        'summary': '''
The "Faint Young Sun Paradox" asks: How did early Earth have liquid water
when the Sun was 30% dimmer? The answer involves BOTH greenhouse warming
AND plate tectonics:

1. FAINT YOUNG SUN: L(4.5 Ga) = 0.70 × L(today)
   - Equilibrium temp at 1 AU: ~230K (frozen!)
   - But geological evidence shows liquid water by 4.2 Ga

2. GREENHOUSE SOLUTION: High CO2 (+ CH4) compensated
   - Early atmosphere: 10-70% CO2 (vs 0.04% today)
   - This provided ~40-60K extra warming
   - Archean CH4 from methanogens added more

3. WHY TECTONICS MATTERS: The carbon-silicate cycle
   - Volcanism releases CO2 from subducted carbonates
   - Weathering removes CO2 by dissolving silicates
   - This THERMOSTAT keeps climate stable over Gyr timescales
   - Without tectonics: no volcanic CO2 recycling → eventual freeze

4. EARTH'S SPECIAL CONDITIONS:
   - Right size: ~6000 km radius for sustained convection
   - Right REE enrichment: radioactive heat drives mantle
   - Right water: lubricates subduction zones
   - Formation bracket 144.2: rocky composition, modest REE

5. WATER WORLDS WITHOUT TECTONICS CAN EXIST:
   - Venus: had water but lost it (runaway greenhouse)
   - Mars: had water but lost it (no magnetic field, small size)
   - Europa/Enceladus: subsurface oceans, tidal heating not tectonics
   - Theoretical: planets with thick H2 atmospheres (greenhouse without CO2)

The PHI-FRAMEWORK INSIGHT:
Earth's formation bracket (144.2) placed it past the silicate cliff (142.65)
with modest REE enrichment (1.44×). This gave enough radioactive heating
for tectonics but not so much that the mantle is too hot. The COINCIDENCE
of Earth having stable surface water IS related to its formation position.
        ''',

        'water_worlds_without_tectonics': [
            {
                'type': 'Ice shell worlds',
                'examples': ['Europa', 'Enceladus', 'Titan'],
                'mechanism': 'Tidal heating, not radioactive/tectonic',
                'surface_water': False,
                'subsurface_water': True
            },
            {
                'type': 'Early hot planets',
                'examples': ['Hadean Earth', 'Young Venus'],
                'mechanism': 'Steam atmosphere → condensation',
                'surface_water': 'Transitional',
                'requires_tectonics': 'For STABILITY, not existence'
            },
            {
                'type': 'H2-greenhouse worlds',
                'examples': ['Theoretical super-Earths'],
                'mechanism': 'H2 collision-induced absorption',
                'surface_water': True,
                'requires_tectonics': 'No, but may be unstable'
            },
        ],

        'earth_tectonic_requirements': {
            'radius_km': '5000-8000 optimal',
            'ree_enrichment': '1-5× solar (provides radioactive heat)',
            'water_fraction': '0.01-1% by mass (lubricates subduction)',
            'formation_bracket': '143-146 (rocky with enough heat sources)',
            'star_type': 'F/G/K (stable luminosity evolution)'
        }
    }

# ═══════════════════════════════════════════════
# MILKY WAY REFERENCE POINTS
# ═══════════════════════════════════════════════

MILKY_WAY = {
    'galactic_center': {'distance_ly': 26000, 'name': 'Sagittarius A*'},
    'galactic_radius': {'distance_ly': 52850, 'name': 'Galaxy Radius'},
    'local_bubble': {'distance_ly': 300, 'name': 'Local Bubble'},
    'orion_arm_width': {'distance_ly': 3500, 'name': 'Orion Arm Width'},
    'nearest_star': {'distance_ly': 4.24, 'name': 'Proxima Centauri'},
    'sirius': {'distance_ly': 8.6, 'name': 'Sirius'},
    'vega': {'distance_ly': 25, 'name': 'Vega'},
}

# Light year in meters
LY_METERS = 9.461e15

# ═══════════════════════════════════════════════
# QUANTUM ROSETTA: ELEMENT CONDENSATION DATA
# From Husmann Decomposition Framework
# Elements condense in σ₃ sector (brackets 140-150)
# ═══════════════════════════════════════════════

ELEMENT_CONDENSATION = {
    # REE (Rare Earth Elements) - targeting signature {89, 34, 13}
    'ree_peak': {
        'bracket': 142.2,
        'temperature_K': 1659,
        'zeckendorf': [89, 34, 13, 5, 1],  # = 142
        'elements': ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'],
        'description': 'Rare Earth Element condensation peak'
    },
    # Silicate cliff - major phase transition
    'silicate_cliff': {
        'bracket_start': 142.6,
        'bracket_end': 142.7,
        'temperature_K': 1400,
        'zeckendorf': [89, 34, 13, 5, 2],  # = 143
        'elements': ['Si', 'O', 'Mg', 'Fe'],
        'description': 'Silicate condensation cliff (olivine, pyroxene)'
    },
    # Iron-nickel condensation
    'iron_nickel': {
        'bracket': 143.5,
        'temperature_K': 1350,
        'zeckendorf': [89, 55],  # = 144 (approximate)
        'elements': ['Fe', 'Ni', 'Co'],
        'description': 'Iron-nickel metal condensation'
    },
    # Sulfide condensation
    'sulfides': {
        'bracket': 145.0,
        'temperature_K': 700,
        'zeckendorf': [89, 55, 1],  # = 145
        'elements': ['S', 'Fe', 'Cu', 'Zn'],
        'description': 'Sulfide mineral condensation (troilite, chalcopyrite)'
    },
    # Ice line
    'ice_line': {
        'bracket': 148.0,
        'temperature_K': 170,
        'zeckendorf': [89, 55, 3, 1],  # = 148
        'elements': ['H', 'O'],
        'description': 'Water ice condensation boundary'
    },
    # Volatile ices
    'volatile_ices': {
        'bracket': 150.0,
        'temperature_K': 30,
        'zeckendorf': [89, 55, 5, 1],  # = 150
        'elements': ['N', 'C', 'O'],
        'description': 'Methane, ammonia, CO ices'
    }
}

# ═══════════════════════════════════════════════
# MINERAL DEPOSITS - EARTH SURFACE (ZOOM LEVEL 4)
# Golden angle correlations between major deposits
# ═══════════════════════════════════════════════

EARTH_MINERAL_DEPOSITS = {
    # REE Deposits - signature {89, 34, 13} in Zeckendorf
    'bayan_obo': {
        'name': 'Bayan Obo',
        'location': {'lat': 41.8, 'lon': 109.97},
        'country': 'China',
        'type': 'REE-Fe-Nb',
        'primary_elements': ['La', 'Ce', 'Nd', 'Fe', 'Nb'],
        'reserves_tons': 48000000,
        'golden_angle_ref': 'origin',
        'zeckendorf_signature': [89, 34, 13, 5, 1]
    },
    'mountain_pass': {
        'name': 'Mountain Pass',
        'location': {'lat': 35.47, 'lon': -115.53},
        'country': 'USA',
        'type': 'REE-Carbonatite',
        'primary_elements': ['Ce', 'La', 'Nd', 'Eu'],
        'reserves_tons': 2000000,
        'golden_angle_from_bayan': 134.5,  # Close to golden angle!
        'zeckendorf_signature': [89, 34, 13, 3]
    },
    'mount_weld': {
        'name': 'Mount Weld',
        'location': {'lat': -28.85, 'lon': 122.55},
        'country': 'Australia',
        'type': 'REE-Carbonatite',
        'primary_elements': ['La', 'Ce', 'Nd', 'Pr'],
        'reserves_tons': 14000000,
        'golden_angle_from_bayan': 89.2,  # F(11) = 89
        'zeckendorf_signature': [89, 34, 13, 8]
    },
    'rare_croft': {
        'name': 'Strange Lake',
        'location': {'lat': 56.33, 'lon': -64.17},
        'country': 'Canada',
        'type': 'REE-Peralkaline',
        'primary_elements': ['Y', 'Dy', 'Er', 'Yb'],
        'reserves_tons': 500000,
        'golden_angle_from_bayan': 55.7,  # F(10) = 55
        'zeckendorf_signature': [89, 34, 21]
    },
    # Platinum Group Metals
    'bushveld': {
        'name': 'Bushveld Complex',
        'location': {'lat': -25.0, 'lon': 29.0},
        'country': 'South Africa',
        'type': 'PGM-Cr-V',
        'primary_elements': ['Pt', 'Pd', 'Rh', 'Cr', 'V'],
        'reserves_tons': 63000,
        'zeckendorf_signature': [55, 34, 13]
    },
    'norilsk': {
        'name': 'Norilsk-Talnakh',
        'location': {'lat': 69.33, 'lon': 88.22},
        'country': 'Russia',
        'type': 'PGM-Ni-Cu',
        'primary_elements': ['Pt', 'Pd', 'Ni', 'Cu'],
        'reserves_tons': 35000,
        'golden_angle_from_bushveld': 136.8,  # ~Golden angle
        'zeckendorf_signature': [55, 34, 13, 3]
    },
    # Gold deposits
    'witwatersrand': {
        'name': 'Witwatersrand Basin',
        'location': {'lat': -26.2, 'lon': 27.9},
        'country': 'South Africa',
        'type': 'Au-U',
        'primary_elements': ['Au', 'U'],
        'reserves_tons': 40000,
        'zeckendorf_signature': [34, 21, 8, 3]
    },
    'carlin': {
        'name': 'Carlin Trend',
        'location': {'lat': 40.87, 'lon': -116.25},
        'country': 'USA',
        'type': 'Au-Sedimentary',
        'primary_elements': ['Au', 'As', 'Sb'],
        'reserves_tons': 3000,
        'zeckendorf_signature': [34, 21, 13]
    }
}

# ═══════════════════════════════════════════════
# ZOOM LEVELS FOR EVOLUTION DETAIL
# Level 0: Full Universe (294 brackets)
# Level 1: Galaxy (brackets 250-280)
# Level 2: Solar System (brackets 230-250)
# Level 3: Planetary (brackets 200-230)
# Level 4: Geological/Surface (brackets 140-170)
# ═══════════════════════════════════════════════

ZOOM_LEVELS = {
    0: {
        'name': 'Universe',
        'bracket_min': 0,
        'bracket_max': 294,
        'scale_label': 'Gly',
        'detail_features': ['sector_boundaries', 'hinges', 'wall'],
        'description': 'Observable universe to Planck scale'
    },
    1: {
        'name': 'Galaxy',
        'bracket_min': 250,
        'bracket_max': 280,
        'scale_label': 'kly',
        'detail_features': ['spiral_arms', 'star_clusters', 'nebulae'],
        'description': 'Milky Way galactic structure'
    },
    2: {
        'name': 'Solar System',
        'bracket_min': 230,
        'bracket_max': 250,
        'scale_label': 'AU',
        'detail_features': ['planets', 'asteroids', 'kuiper_belt', 'oort_cloud'],
        'description': 'Solar system orbital structure'
    },
    3: {
        'name': 'Planetary',
        'bracket_min': 200,
        'bracket_max': 230,
        'scale_label': 'km',
        'detail_features': ['continents', 'oceans', 'atmosphere'],
        'description': 'Planetary surface features'
    },
    4: {
        'name': 'Geological',
        'bracket_min': 140,
        'bracket_max': 170,
        'scale_label': 'm',
        'detail_features': ['mineral_deposits', 'ree_zones', 'element_condensation'],
        'description': 'Geological and mineral formations (Quantum Rosetta)'
    }
}

# REE Targeting signature - presence of {89, 34, 13} in Zeckendorf
REE_TARGETING_SIGNATURE = [89, 34, 13]

# ═══════════════════════════════════════════════
# EARTH EVOLUTION TIMELINE
# 4.54 Billion years of Earth history
# Timeline normalized to 0.0 (formation) to 1.0 (present)
# ═══════════════════════════════════════════════

EARTH_TIMELINE = {
    # Hadean Eon (4.54 - 4.0 Ga)
    'hadean_formation': {
        'time_ga': 4.54,
        'time_normalized': 0.0,
        'name': 'Earth Formation',
        'eon': 'Hadean',
        'description': 'Accretion from solar nebula, Moon-forming impact',
        'atmosphere': ['H2', 'He', 'NH3', 'CH4'],
        'surface': 'magma_ocean',
        'temperature_K': 2000,
        'ocean_coverage': 0.0,
        'life': None,
        'o2_percent': 0.0,
        'co2_percent': 95.0,
        'color': '#ff4400'
    },
    'hadean_cooling': {
        'time_ga': 4.4,
        'time_normalized': 0.031,
        'name': 'Crust Formation',
        'eon': 'Hadean',
        'description': 'First solid crust, earliest zircons',
        'atmosphere': ['CO2', 'N2', 'H2O', 'SO2'],
        'surface': 'volcanic_crust',
        'temperature_K': 500,
        'ocean_coverage': 0.0,
        'life': None,
        'o2_percent': 0.0,
        'co2_percent': 80.0,
        'color': '#cc3300'
    },
    'hadean_oceans': {
        'time_ga': 4.2,
        'time_normalized': 0.075,
        'name': 'First Oceans',
        'eon': 'Hadean',
        'description': 'Water vapor condenses, early oceans form',
        'atmosphere': ['CO2', 'N2', 'H2O'],
        'surface': 'early_ocean',
        'temperature_K': 400,
        'ocean_coverage': 0.3,
        'life': None,
        'o2_percent': 0.0,
        'co2_percent': 70.0,
        'color': '#884422'
    },

    # Archean Eon (4.0 - 2.5 Ga)
    'archean_start': {
        'time_ga': 4.0,
        'time_normalized': 0.119,
        'name': 'Archean Begins',
        'eon': 'Archean',
        'description': 'Oldest rocks, late heavy bombardment ends',
        'atmosphere': ['CO2', 'N2', 'CH4', 'H2O'],
        'surface': 'protocontinents',
        'temperature_K': 340,
        'ocean_coverage': 0.5,
        'life': None,
        'o2_percent': 0.0,
        'co2_percent': 50.0,
        'color': '#664433'
    },
    'archean_life': {
        'time_ga': 3.5,
        'time_normalized': 0.229,
        'name': 'First Life',
        'eon': 'Archean',
        'description': 'Oldest microfossils, stromatolites appear (~3.5 Ga)',
        'atmosphere': ['CO2', 'N2', 'CH4'],
        'surface': 'stromatolite_seas',
        'temperature_K': 330,
        'ocean_coverage': 0.6,
        'life': 'prokaryotes',
        'o2_percent': 0.0,
        'co2_percent': 40.0,
        'color': '#556644'
    },
    'archean_photosynthesis': {
        'time_ga': 3.2,
        'time_normalized': 0.295,
        'name': 'Photosynthesis Emerges',
        'eon': 'Archean',
        'description': 'Cyanobacteria begin producing oxygen (~3.2-2.8 Ga)',
        'atmosphere': ['CO2', 'N2', 'CH4', 'trace O2'],
        'surface': 'microbial_mats',
        'temperature_K': 320,
        'ocean_coverage': 0.65,
        'life': 'cyanobacteria',
        'o2_percent': 0.001,
        'co2_percent': 30.0,
        'color': '#447755'
    },
    'archean_cratons': {
        'time_ga': 3.0,
        'time_normalized': 0.339,
        'name': 'Cratons Form',
        'eon': 'Archean',
        'description': 'Stable continental nuclei emerge',
        'atmosphere': ['CO2', 'N2', 'CH4'],
        'surface': 'granite_cratons',
        'temperature_K': 310,
        'ocean_coverage': 0.7,
        'life': 'bacterial_mats',
        'o2_percent': 0.01,
        'co2_percent': 20.0,
        'color': '#448866'
    },

    # Proterozoic Eon (2.5 - 0.54 Ga)
    'great_oxidation': {
        'time_ga': 2.4,
        'time_normalized': 0.471,
        'name': 'Great Oxidation Event',
        'eon': 'Proterozoic',
        'description': 'Oxygen accumulates in atmosphere, banded iron formations',
        'atmosphere': ['N2', 'CO2', 'O2'],
        'surface': 'oxidized_continents',
        'temperature_K': 290,
        'ocean_coverage': 0.7,
        'life': 'aerobic_bacteria',
        'o2_percent': 2.0,
        'co2_percent': 10.0,
        'color': '#4488aa'
    },
    'snowball_earth_1': {
        'time_ga': 2.2,
        'time_normalized': 0.515,
        'name': 'Huronian Glaciation',
        'eon': 'Proterozoic',
        'description': 'First global glaciation (Snowball Earth)',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'global_ice',
        'temperature_K': 220,
        'ocean_coverage': 0.1,
        'life': 'refugia_bacteria',
        'o2_percent': 3.0,
        'co2_percent': 5.0,
        'color': '#aaddff'
    },
    'boring_billion': {
        'time_ga': 1.8,
        'time_normalized': 0.603,
        'name': 'Boring Billion',
        'eon': 'Proterozoic',
        'description': 'Stable climate, slow evolution, supercontinent Columbia',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'supercontinent',
        'temperature_K': 295,
        'ocean_coverage': 0.65,
        'life': 'eukaryotes',
        'o2_percent': 5.0,
        'co2_percent': 3.0,
        'color': '#668899'
    },
    'rodinia': {
        'time_ga': 1.0,
        'time_normalized': 0.779,
        'name': 'Rodinia Supercontinent',
        'eon': 'Proterozoic',
        'description': 'Supercontinent Rodinia forms',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'rodinia',
        'temperature_K': 290,
        'ocean_coverage': 0.6,
        'life': 'multicellular_algae',
        'o2_percent': 8.0,
        'co2_percent': 2.0,
        'color': '#559988'
    },
    'snowball_earth_2': {
        'time_ga': 0.72,
        'time_normalized': 0.841,
        'name': 'Sturtian Glaciation',
        'eon': 'Proterozoic',
        'description': 'Second Snowball Earth, Rodinia breaks up',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'global_ice',
        'temperature_K': 210,
        'ocean_coverage': 0.1,
        'life': 'surviving_eukaryotes',
        'o2_percent': 10.0,
        'co2_percent': 1.0,
        'color': '#bbddff'
    },
    'ediacaran': {
        'time_ga': 0.635,
        'time_normalized': 0.860,
        'name': 'Ediacaran Biota',
        'eon': 'Proterozoic',
        'description': 'First complex multicellular life',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'shallow_seas',
        'temperature_K': 285,
        'ocean_coverage': 0.7,
        'life': 'ediacaran_fauna',
        'o2_percent': 15.0,
        'co2_percent': 0.8,
        'color': '#66aa88'
    },

    # Phanerozoic Eon (0.54 Ga - Present)
    'cambrian_explosion': {
        'time_ga': 0.54,
        'time_normalized': 0.881,
        'name': 'Cambrian Explosion',
        'eon': 'Phanerozoic',
        'era': 'Paleozoic',
        'description': 'Rapid diversification of animal life',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'shallow_seas',
        'temperature_K': 295,
        'ocean_coverage': 0.75,
        'life': 'trilobites_arthropods',
        'o2_percent': 15.0,
        'co2_percent': 0.5,
        'color': '#55aa77'
    },
    'ordovician': {
        'time_ga': 0.485,
        'time_normalized': 0.893,
        'name': 'Ordovician',
        'eon': 'Phanerozoic',
        'era': 'Paleozoic',
        'description': 'First land plants, Great Ordovician Biodiversification',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'gondwana_seas',
        'temperature_K': 290,
        'ocean_coverage': 0.7,
        'life': 'early_fish_corals',
        'o2_percent': 14.0,
        'co2_percent': 0.45,
        'color': '#44aa88'
    },
    'silurian_devonian': {
        'time_ga': 0.42,
        'time_normalized': 0.907,
        'name': 'Age of Fishes',
        'eon': 'Phanerozoic',
        'era': 'Paleozoic',
        'description': 'Fish diversity peaks, first forests, amphibians emerge',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'forests_swamps',
        'temperature_K': 305,
        'ocean_coverage': 0.65,
        'life': 'fish_amphibians_forests',
        'o2_percent': 21.0,
        'co2_percent': 0.3,
        'color': '#339966'
    },
    'carboniferous': {
        'time_ga': 0.36,
        'time_normalized': 0.921,
        'name': 'Carboniferous',
        'eon': 'Phanerozoic',
        'era': 'Paleozoic',
        'description': 'Giant insects, coal swamps, Pangaea forms',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'coal_forests',
        'temperature_K': 295,
        'ocean_coverage': 0.6,
        'life': 'giant_insects_reptiles',
        'o2_percent': 35.0,
        'co2_percent': 0.15,
        'color': '#228855'
    },
    'permian': {
        'time_ga': 0.299,
        'time_normalized': 0.934,
        'name': 'Permian',
        'eon': 'Phanerozoic',
        'era': 'Paleozoic',
        'description': 'Pangaea complete, synapsids dominate',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'pangaea_desert',
        'temperature_K': 300,
        'ocean_coverage': 0.55,
        'life': 'synapsids_therapsids',
        'o2_percent': 30.0,
        'co2_percent': 0.2,
        'color': '#cc9955'
    },
    'permian_extinction': {
        'time_ga': 0.252,
        'time_normalized': 0.944,
        'name': 'Great Dying',
        'eon': 'Phanerozoic',
        'era': 'Mesozoic',
        'description': 'Largest mass extinction (96% species lost)',
        'atmosphere': ['N2', 'O2', 'CO2', 'H2S'],
        'surface': 'volcanic_wasteland',
        'temperature_K': 320,
        'ocean_coverage': 0.5,
        'life': 'mass_extinction',
        'o2_percent': 15.0,
        'co2_percent': 0.8,
        'color': '#884422'
    },
    'triassic': {
        'time_ga': 0.25,
        'time_normalized': 0.945,
        'name': 'Triassic Recovery',
        'eon': 'Phanerozoic',
        'era': 'Mesozoic',
        'description': 'First dinosaurs, mammals emerge',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'pangaea_recovering',
        'temperature_K': 305,
        'ocean_coverage': 0.55,
        'life': 'early_dinosaurs_mammals',
        'o2_percent': 16.0,
        'co2_percent': 0.5,
        'color': '#aa7744'
    },
    'jurassic': {
        'time_ga': 0.201,
        'time_normalized': 0.956,
        'name': 'Jurassic',
        'eon': 'Phanerozoic',
        'era': 'Mesozoic',
        'description': 'Dinosaurs dominate, Pangaea splits, first birds',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'breaking_pangaea',
        'temperature_K': 300,
        'ocean_coverage': 0.6,
        'life': 'giant_dinosaurs_birds',
        'o2_percent': 20.0,
        'co2_percent': 0.35,
        'color': '#55aa44'
    },
    'cretaceous': {
        'time_ga': 0.145,
        'time_normalized': 0.968,
        'name': 'Cretaceous',
        'eon': 'Phanerozoic',
        'era': 'Mesozoic',
        'description': 'Flowering plants, modern continents form',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'modern_continents_forming',
        'temperature_K': 295,
        'ocean_coverage': 0.65,
        'life': 'dinosaurs_flowers_mammals',
        'o2_percent': 23.0,
        'co2_percent': 0.25,
        'color': '#44bb55'
    },
    'kt_extinction': {
        'time_ga': 0.066,
        'time_normalized': 0.985,
        'name': 'K-Pg Extinction',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Asteroid impact, dinosaurs extinct',
        'atmosphere': ['N2', 'O2', 'dust', 'SO2'],
        'surface': 'impact_winter',
        'temperature_K': 270,
        'ocean_coverage': 0.65,
        'life': 'mass_extinction',
        'o2_percent': 21.0,
        'co2_percent': 0.4,
        'color': '#555555'
    },
    'paleogene': {
        'time_ga': 0.065,
        'time_normalized': 0.986,
        'name': 'Age of Mammals',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Mammals diversify, modern orders appear',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'modern_continents',
        'temperature_K': 297,
        'ocean_coverage': 0.68,
        'life': 'mammals_birds',
        'o2_percent': 21.0,
        'co2_percent': 0.1,
        'color': '#66bb66'
    },
    'miocene': {
        'time_ga': 0.023,
        'time_normalized': 0.995,
        'name': 'Miocene',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Grasslands spread, apes diversify',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'grasslands',
        'temperature_K': 292,
        'ocean_coverage': 0.7,
        'life': 'apes_grassland_animals',
        'o2_percent': 21.0,
        'co2_percent': 0.03,
        'color': '#77cc77'
    },
    'ice_ages': {
        'time_ga': 0.0026,
        'time_normalized': 0.9994,
        'name': 'Pleistocene Ice Ages',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Glacial cycles, humans evolve',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'glacial_interglacial',
        'temperature_K': 285,
        'ocean_coverage': 0.65,
        'life': 'megafauna_humans',
        'o2_percent': 21.0,
        'co2_percent': 0.028,
        'color': '#88ccdd'
    },
    'holocene': {
        'time_ga': 0.0117,
        'time_normalized': 0.9997,
        'name': 'Holocene',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Interglacial, human civilization',
        'atmosphere': ['N2', 'O2', 'CO2'],
        'surface': 'modern_earth',
        'temperature_K': 288,
        'ocean_coverage': 0.71,
        'life': 'human_civilization',
        'o2_percent': 21.0,
        'co2_percent': 0.028,
        'color': '#4488bb'
    },
    'present': {
        'time_ga': 0.0,
        'time_normalized': 1.0,
        'name': 'Present Day',
        'eon': 'Phanerozoic',
        'era': 'Cenozoic',
        'description': 'Anthropocene, human-dominated Earth',
        'atmosphere': ['N2', 'O2', 'CO2', 'trace gases'],
        'surface': 'anthropocene',
        'temperature_K': 288,
        'ocean_coverage': 0.71,
        'life': 'modern_biosphere',
        'o2_percent': 21.0,
        'co2_percent': 0.042,
        'color': '#4A90D9'
    }
}

# Earth evolution timeline as sorted list for interpolation
EARTH_TIMELINE_SORTED = sorted(EARTH_TIMELINE.items(), key=lambda x: x[1]['time_normalized'])


# ═══════════════════════════════════════════════
# CORE SCALING FUNCTIONS
# ═══════════════════════════════════════════════

def bracket_scale(n):
    """Physical scale at bracket n in meters"""
    return L_PLANCK * (PHI ** n) * CALIB_FACTOR

def bracket_from_scale(meters):
    """Bracket index from physical scale"""
    return math.log(meters / (L_PLANCK * CALIB_FACTOR)) / math.log(PHI)

def alpha_coupling(N):
    """Master coupling equation: α_eff = 1/(N × W)"""
    return 1.0 / (N * WALL_FRACTION)

def sector_widths(N):
    """Sector widths for total N brackets"""
    w1 = N / PHI4   # σ₁ = σ₅ (matter endpoints)
    w2 = N / PHI3   # σ₂ = σ₃ = σ₄ (conduit sectors)
    return {'w1': w1, 'w2': w2}

def sector_boundaries(N):
    """Sector boundaries (cumulative bracket indices)"""
    widths = sector_widths(N)
    w1, w2 = widths['w1'], widths['w2']
    return {
        'sigma1_end': w1,
        'sigma2_end': w1 + w2,
        'sigma3_end': w1 + 2 * w2,
        'sigma4_end': w1 + 3 * w2,
        'sigma5_end': N,
    }

def key_hinges(N):
    """Key hinge positions"""
    widths = sector_widths(N)
    bounds = sector_boundaries(N)
    w1, w2 = widths['w1'], widths['w2']
    return {
        'proton_hinge': w1 + w2 * HINGE_CONST,
        'brain_hinge': bounds['sigma2_end'] + w2 * HINGE_CONST,
        'oort_hinge': bounds['sigma3_end'] + w2 * HINGE_CONST,
    }

def zeckendorf(n):
    """Zeckendorf decomposition"""
    if n <= 0:
        return []
    fibs = []
    a, b = 1, 1
    while b <= n:
        fibs.append(b)
        a, b = b, a + b
    fibs.reverse()
    terms = []
    remainder = n
    for f in fibs:
        if f <= remainder:
            terms.append(f)
            remainder -= f
    return terms

def verify_unity():
    """Unity equation: must return exactly 1.0"""
    return INV_PHI4 + INV_PHI3 + INV_PHI

def has_ree_signature(zeck_list):
    """Check if Zeckendorf decomposition contains REE targeting signature {89, 34, 13}"""
    return all(fib in zeck_list for fib in REE_TARGETING_SIGNATURE)

def calculate_golden_angle_distance(lat1, lon1, lat2, lon2):
    """Calculate great circle distance and check for golden angle correlations"""
    import math
    R = 6371  # Earth radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c

    # Calculate bearing (azimuth)
    x = math.sin(delta_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    bearing = math.degrees(math.atan2(x, y))

    # Check for golden angle correlation
    golden_angle_match = abs((bearing % 360) - GOLDEN_ANGLE) < 5 or abs((bearing % 360) - (360 - GOLDEN_ANGLE)) < 5
    fibonacci_angle_match = any(abs((bearing % 360) - fib) < 3 for fib in [8, 13, 21, 34, 55, 89, 144])

    return {
        'distance_km': distance,
        'bearing_deg': bearing % 360,
        'golden_angle_match': golden_angle_match,
        'fibonacci_angle_match': fibonacci_angle_match
    }

def wall_layers():
    """Three-layer wall structure"""
    return {
        'layer1': INV_PHI4,
        'layer2': HINGE_CONST / PHI3,
        'layer3': INV_PHI4,
        'total': WALL_FRACTION,
        'remaining': 1.0 - WALL_FRACTION,
    }


# ═══════════════════════════════════════════════
# MS SQL DATABASE CONNECTION
# ═══════════════════════════════════════════════

def get_db_connection():
    """Connect to CloverReports SQL Server"""
    try:
        import pymssql
        conn = pymssql.connect(
            server='10.21.48.3',
            port=1433,
            database='CloverReports',
            user='magicwiki',
            password='NewMagicWiki36870!'
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def save_scaling_vector(vector_data):
    """Save a scaling vector to the database"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO universe_scaling_vectors
            (vector_type, scale_factor, phi_bracket, position_data, created_at)
            VALUES (%s, %s, %s, %s, GETDATE())
        """, (
            vector_data.get('type', 'position'),
            vector_data.get('scale', 1.0),
            vector_data.get('bracket', 0),
            json.dumps(vector_data.get('position', {}))
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False
    finally:
        conn.close()

def get_scaling_vectors(vector_type=None):
    """Retrieve scaling vectors from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        if vector_type:
            cursor.execute("""
                SELECT vector_type, scale_factor, phi_bracket, position_data, created_at
                FROM universe_scaling_vectors
                WHERE vector_type = %s
                ORDER BY created_at DESC
            """, (vector_type,))
        else:
            cursor.execute("""
                SELECT vector_type, scale_factor, phi_bracket, position_data, created_at
                FROM universe_scaling_vectors
                ORDER BY created_at DESC
            """)
        rows = cursor.fetchall()
        return [{
            'type': r[0],
            'scale': float(r[1]),
            'bracket': float(r[2]),
            'position': json.loads(r[3]) if r[3] else {},
            'created_at': str(r[4])
        } for r in rows]
    except Exception as e:
        print(f"Query error: {e}")
        return []
    finally:
        conn.close()


# ═══════════════════════════════════════════════
# EVOLUTION STATE PERSISTENCE
# Save/load evolution progress to continue if interrupted
# ═══════════════════════════════════════════════

def ensure_evolution_table():
    """Create evolution state table if not exists"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='universe_evolution_state' AND xtype='U')
            CREATE TABLE universe_evolution_state (
                id INT IDENTITY(1,1) PRIMARY KEY,
                session_id VARCHAR(50) NOT NULL,
                zoom_level INT NOT NULL,
                current_bracket DECIMAL(10,4) NOT NULL,
                evolved_features NVARCHAR(MAX),
                mineral_deposits NVARCHAR(MAX),
                evolution_progress DECIMAL(5,4) DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT GETDATE(),
                updated_at DATETIME NOT NULL DEFAULT GETDATE()
            )
        """)
        conn.commit()
        return True
    except Exception as e:
        print(f"Table creation error: {e}")
        return False
    finally:
        conn.close()

def save_evolution_state(session_id, state_data):
    """Save evolution state for resumability"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Check if session exists
        cursor.execute("""
            SELECT id FROM universe_evolution_state WHERE session_id = %s
        """, (session_id,))
        existing = cursor.fetchone()

        if existing:
            # Update existing
            cursor.execute("""
                UPDATE universe_evolution_state
                SET zoom_level = %s,
                    current_bracket = %s,
                    evolved_features = %s,
                    mineral_deposits = %s,
                    evolution_progress = %s,
                    updated_at = GETDATE()
                WHERE session_id = %s
            """, (
                state_data.get('zoom_level', 0),
                state_data.get('current_bracket', 0),
                json.dumps(state_data.get('evolved_features', [])),
                json.dumps(state_data.get('mineral_deposits', [])),
                state_data.get('evolution_progress', 0),
                session_id
            ))
        else:
            # Insert new
            cursor.execute("""
                INSERT INTO universe_evolution_state
                (session_id, zoom_level, current_bracket, evolved_features, mineral_deposits, evolution_progress)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                session_id,
                state_data.get('zoom_level', 0),
                state_data.get('current_bracket', 0),
                json.dumps(state_data.get('evolved_features', [])),
                json.dumps(state_data.get('mineral_deposits', [])),
                state_data.get('evolution_progress', 0)
            ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Save evolution error: {e}")
        return False
    finally:
        conn.close()

def load_evolution_state(session_id):
    """Load saved evolution state"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_id, zoom_level, current_bracket, evolved_features,
                   mineral_deposits, evolution_progress, updated_at
            FROM universe_evolution_state
            WHERE session_id = %s
        """, (session_id,))
        row = cursor.fetchone()
        if row:
            return {
                'session_id': row[0],
                'zoom_level': row[1],
                'current_bracket': float(row[2]),
                'evolved_features': json.loads(row[3]) if row[3] else [],
                'mineral_deposits': json.loads(row[4]) if row[4] else [],
                'evolution_progress': float(row[5]),
                'last_updated': str(row[6])
            }
        return None
    except Exception as e:
        print(f"Load evolution error: {e}")
        return None
    finally:
        conn.close()

def get_recent_sessions(limit=10):
    """Get recent evolution sessions"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP %s session_id, zoom_level, evolution_progress, updated_at
            FROM universe_evolution_state
            ORDER BY updated_at DESC
        """, (limit,))
        rows = cursor.fetchall()
        return [{
            'session_id': r[0],
            'zoom_level': r[1],
            'evolution_progress': float(r[2]),
            'last_updated': str(r[3])
        } for r in rows]
    except Exception as e:
        print(f"Query sessions error: {e}")
        return []
    finally:
        conn.close()


# ═══════════════════════════════════════════════
# PHYSICAL CONSTANTS FOR CONDENSATION
# ═══════════════════════════════════════════════

k_B = 1.380649e-23       # Boltzmann constant (J/K)
h_planck = 6.62607e-34   # Planck constant (J·s)
c_light = 2.998e8        # Speed of light (m/s)
L_SUN = 3.828e26         # Solar luminosity (W)

# ═══════════════════════════════════════════════
# TEMPERATURE-BRACKET CONVERSION
# Key shortcut: formation temperature → bracket → composition
# ═══════════════════════════════════════════════

def temp_to_bracket(T_kelvin):
    """Convert condensation temperature to bracket index"""
    if T_kelvin <= 0:
        return 200  # Beyond volatile ices
    E = k_B * T_kelvin
    lam = h_planck * c_light / E
    return bracket_from_scale(lam)

def bracket_to_temp(n):
    """Convert bracket index to condensation temperature"""
    lam = bracket_scale(n)
    E = h_planck * c_light / lam
    return E / k_B

# ═══════════════════════════════════════════════
# ENHANCED CONDENSATION SEQUENCE
# Complete element-by-element data for world classification
# ═══════════════════════════════════════════════

CONDENSATION_ZONES = {
    'pgm_refractory': {
        'bracket_range': [141.5, 142.2],
        'temp_range': [1700, 1900],
        'enrichment_vs_solar': 'infinite',
        'elements': ['Os', 'W', 'Re', 'Ir', 'Ru', 'Zr', 'Hf'],
        'color': '#E5E4E2',
        'description': 'Ultra-refractory PGM zone'
    },
    'hree_peak': {
        'bracket_range': [142.2, 142.3],
        'temp_range': [1650, 1700],
        'enrichment_vs_solar': 950,  # ★ PEAK
        'ree_mass_fraction': 0.454,
        'elements': ['Lu', 'Sc', 'Y', 'Tb', 'Gd', 'Er', 'Ho', 'Tm', 'Dy'],
        'zeckendorf': [89, 34, 13, 5, 1],
        'color': '#00FF88',
        'description': '★ HREE Peak: 950× solar enrichment'
    },
    'refractory_hosts': {
        'bracket_range': [142.2, 142.4],
        'temp_range': [1500, 1653],
        'elements': ['Al', 'Ti', 'Ca'],
        'color': '#FFFFFF',
        'description': 'Al-Ti-Ca refractory hosts'
    },
    'lree_zone': {
        'bracket_range': [142.3, 142.7],
        'temp_range': [1356, 1602],
        'enrichment_vs_solar': 50,
        'elements': ['Nd', 'Sm', 'Pr', 'La', 'Yb', 'Ce', 'Eu'],
        'color': '#00FFFF',
        'description': 'Light REE condensation'
    },
    'silicate_cliff': {
        'bracket_range': [142.63, 142.70],
        'temp_range': [1310, 1353],
        'cliff_width': 0.07,  # Only 0.07 brackets wide!
        'elements': ['Ni', 'Mg', 'Fe', 'Si'],
        'ree_before': 950,
        'ree_after': 1.6,
        'color': '#FF0000',
        'description': '★ THE SILICATE CLIFF: REE crashes from 950× to 1.6×'
    },
    'moderate_volatile': {
        'bracket_range': [142.7, 144.1],
        'temp_range': [600, 1300],
        'elements': ['Cr', 'Mn', 'K', 'Na', 'Cu', 'S'],
        'color': '#FFA500',
        'description': 'Moderately volatile elements'
    },
    'ice_line': {
        'bracket': 146.8,
        'temp': 182,
        'solar_au': 2.7,
        'elements': ['H2O'],
        'color': '#0088FF',
        'description': '★ ICE LINE: Rocky vs icy bodies'
    },
    'volatile_ices': {
        'bracket_range': [147.5, 151.0],
        'temp_range': [25, 130],
        'elements': ['NH3', 'CO2', 'CH4', 'N2', 'CO'],
        'color': '#88CCFF',
        'description': 'Outer solar system ices'
    }
}

# Critical bracket thresholds for quick classification
BRACKET_THRESHOLDS = {
    'ree_peak': 142.21,
    'silicate_cliff': 142.65,
    'ice_line': 146.80,
    'volatile_start': 147.50,
}

# ═══════════════════════════════════════════════
# WORLD CLASSIFICATION SHORTCUTS
# Pattern-based derivation of current conditions
# ═══════════════════════════════════════════════

def disk_temperature(r_AU, star_luminosity_ratio=1.0, T0=2000, r0=0.1, q=0.5):
    """
    Midplane temperature at radius r in AU.
    Scales with star luminosity: r_effective = r / sqrt(L_star/L_sun)
    """
    # Scale radius for star luminosity
    r_effective = r_AU / math.sqrt(star_luminosity_ratio)
    return T0 * (r_effective / r0) ** (-q)

def formation_bracket(r_AU, star_luminosity_ratio=1.0):
    """
    What bracket did material at this orbital radius condense at?
    KEY SHORTCUT: This determines the world's composition.
    """
    T = disk_temperature(r_AU, star_luminosity_ratio)
    return temp_to_bracket(T)

def ree_enrichment_factor(formation_brkt):
    """
    REE enrichment factor based on formation bracket.
    The silicate cliff creates a sharp transition.
    """
    if formation_brkt < 142.0:
        return 0  # Too hot, nothing condensed yet
    elif formation_brkt < 142.21:
        # PGM zone, some REE but diluted
        return 100 + (142.21 - formation_brkt) * 500
    elif formation_brkt < 142.65:
        # Before silicate cliff: 950× peak, declining
        cliff_progress = (formation_brkt - 142.21) / (142.65 - 142.21)
        return 950 * (1 - cliff_progress * 0.95)
    else:
        # After cliff: REE diluted by silicates
        return max(1.0, 1.6 - (formation_brkt - 142.65) * 0.1)

def brain_hinge_proximity(radius_km):
    """
    How close is this world's radius bracket to the consciousness hinge (163.8)?
    Lower = more favorable for consciousness evolution.
    """
    BRAIN_HINGE = 163.8
    radius_m = radius_km * 1000
    radius_bracket = bracket_from_scale(radius_m)
    return abs(radius_bracket - BRAIN_HINGE)

def habitability_score(world):
    """
    Quick habitability assessment based on framework patterns.
    Factors: brain hinge proximity, ice line position, REE availability.
    Returns 0-100 score.
    """
    score = 100

    # Brain hinge proximity (consciousness evolution factor)
    if 'radius_km' in world:
        hinge_dist = brain_hinge_proximity(world['radius_km'])
        # Earth is 2.6 brackets away, Pluto is 0.0
        if hinge_dist <= 3:
            score += 20  # Bonus for close match
        elif hinge_dist > 10:
            score -= 20

    # Formation bracket (determines composition)
    if 'formation_bracket' in world:
        fb = world['formation_bracket']
        # Inside ice line = rocky, potentially habitable
        if fb < BRACKET_THRESHOLDS['ice_line']:
            score += 10
        # Too close to star = no volatiles
        if fb < 142.0:
            score -= 30
        # Outside volatile zone = too cold
        if fb > 150:
            score -= 40

    # REE availability (technology potential)
    if 'ree_enrichment' in world:
        if world['ree_enrichment'] > 10:
            score += 10
        elif world['ree_enrichment'] < 2:
            score -= 5

    # Atmosphere indicator
    if world.get('has_atmosphere', False):
        score += 15

    return max(0, min(100, score))

def classify_world_type(formation_brkt):
    """
    Quick classification based on formation bracket.
    """
    if formation_brkt < 142.0:
        return 'ultra_refractory'
    elif formation_brkt < 142.65:
        return 'rocky_enriched'  # Inside silicate cliff, REE-rich
    elif formation_brkt < BRACKET_THRESHOLDS['ice_line']:
        return 'rocky_standard'  # Earth-like, normal REE
    elif formation_brkt < 150:
        return 'ice_giant'       # Uranus/Neptune type
    else:
        return 'volatile_rich'   # Kuiper belt, comets

# ═══════════════════════════════════════════════
# PLANETARY DATABASE WITH DERIVED PROPERTIES
# Scalable structure for solar system + exoplanets
# ═══════════════════════════════════════════════

def derive_planet_properties(planet_data, star_luminosity_ratio=1.0):
    """
    Derive all properties from basic orbital/physical data.
    This is the core shortcut: minimal input → complete classification.
    """
    result = {**planet_data}

    # Formation conditions
    if 'a_AU' in planet_data:
        result['formation_bracket'] = formation_bracket(
            planet_data['a_AU'], star_luminosity_ratio
        )
        result['formation_temp_K'] = disk_temperature(
            planet_data['a_AU'], star_luminosity_ratio
        )
        result['orbital_bracket'] = bracket_from_scale(
            planet_data['a_AU'] * AU_METERS
        )
        result['orbital_zeckendorf'] = zeckendorf(
            int(result['orbital_bracket'])
        )

    # Physical properties
    if 'radius_km' in planet_data:
        radius_m = planet_data['radius_km'] * 1000
        result['radius_bracket'] = bracket_from_scale(radius_m)
        result['brain_hinge_offset'] = brain_hinge_proximity(
            planet_data['radius_km']
        )

    # REE status
    if 'formation_bracket' in result:
        result['ree_enrichment'] = ree_enrichment_factor(
            result['formation_bracket']
        )
        result['world_type'] = classify_world_type(
            result['formation_bracket']
        )
        # Check for REE signature in orbital Zeckendorf
        if 'orbital_zeckendorf' in result:
            result['has_ree_orbital_signature'] = has_ree_signature(
                result['orbital_zeckendorf']
            )

    # Habitability
    result['habitability_score'] = habitability_score(result)

    return result

# Solar System planets with minimal base data
PLANETS_BASE = {
    'mercury': {'name': 'Mercury', 'a_AU': 0.387, 'radius_km': 2440, 'has_atmosphere': False},
    'venus': {'name': 'Venus', 'a_AU': 0.723, 'radius_km': 6052, 'has_atmosphere': True},
    'earth': {'name': 'Earth', 'a_AU': 1.0, 'radius_km': 6371, 'has_atmosphere': True},
    'mars': {'name': 'Mars', 'a_AU': 1.524, 'radius_km': 3390, 'has_atmosphere': True},
    'ceres': {'name': 'Ceres', 'a_AU': 2.77, 'radius_km': 473, 'has_atmosphere': False},
    'jupiter': {'name': 'Jupiter', 'a_AU': 5.203, 'radius_km': 69911, 'has_atmosphere': True},
    'saturn': {'name': 'Saturn', 'a_AU': 9.537, 'radius_km': 58232, 'has_atmosphere': True},
    'uranus': {'name': 'Uranus', 'a_AU': 19.19, 'radius_km': 25362, 'has_atmosphere': True},
    'neptune': {'name': 'Neptune', 'a_AU': 30.07, 'radius_km': 24622, 'has_atmosphere': True},
    'pluto': {'name': 'Pluto', 'a_AU': 39.48, 'radius_km': 1188, 'has_atmosphere': True},
}

# Known exoplanets of interest
EXOPLANETS_BASE = {
    'teegarden_b': {
        'name': 'Teegarden b',
        'a_AU': 0.0252,
        'radius_km': 6500,  # estimated Earth-like
        'has_atmosphere': True,  # assumed
        'star_luminosity_ratio': 0.00073,  # M6.5V dwarf
        'star_name': "Teegarden's Star",
        'distance_ly': 12.5,
    },
    'teegarden_c': {
        'name': 'Teegarden c',
        'a_AU': 0.0443,
        'radius_km': 6500,
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.00073,
        'star_name': "Teegarden's Star",
        'distance_ly': 12.5,
    },
    'proxima_b': {
        'name': 'Proxima Centauri b',
        'a_AU': 0.0485,
        'radius_km': 7100,
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.0017,
        'star_name': 'Proxima Centauri',
        'distance_ly': 4.24,
    },
    'trappist_1e': {
        'name': 'TRAPPIST-1e',
        'a_AU': 0.02928,
        'radius_km': 5797,
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.000553,
        'star_name': 'TRAPPIST-1',
        'distance_ly': 40.7,
    },
    'trappist_1f': {
        'name': 'TRAPPIST-1f',
        'a_AU': 0.03853,
        'radius_km': 6629,
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.000553,
        'star_name': 'TRAPPIST-1',
        'distance_ly': 40.7,
    },
    'lhs_1140b': {
        'name': 'LHS 1140 b',
        'a_AU': 0.0875,
        'radius_km': 10700,  # Super-Earth
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.00462,
        'star_name': 'LHS 1140',
        'distance_ly': 41.0,
    },
    'kepler_442b': {
        'name': 'Kepler-442b',
        'a_AU': 0.409,
        'radius_km': 8200,
        'has_atmosphere': True,
        'star_luminosity_ratio': 0.118,
        'star_name': 'Kepler-442',
        'distance_ly': 112,
    },
}

def get_all_worlds_derived():
    """
    Get all planets and exoplanets with derived properties.
    Single function call → complete world database.
    """
    result = {}

    # Solar system (star_luminosity_ratio = 1.0)
    for key, data in PLANETS_BASE.items():
        result[key] = derive_planet_properties(data, 1.0)
        result[key]['system'] = 'Solar System'

    # Exoplanets (use their star's luminosity)
    for key, data in EXOPLANETS_BASE.items():
        star_lum = data.get('star_luminosity_ratio', 1.0)
        result[key] = derive_planet_properties(data, star_lum)
        result[key]['system'] = data.get('star_name', 'Unknown')

    return result

# Pre-compute for efficiency
WORLDS_DERIVED = get_all_worlds_derived()

# ═══════════════════════════════════════════════
# WORLD SEARCH & FILTERING
# Find worlds meeting specific conditions
# ═══════════════════════════════════════════════

def search_worlds(criteria):
    """
    Search for worlds meeting given criteria.

    Criteria examples:
        {'world_type': 'rocky_standard'}
        {'ree_enrichment_min': 10}
        {'habitability_min': 70}
        {'brain_hinge_offset_max': 5}
        {'formation_bracket_range': [142, 147]}

    Returns list of matching worlds sorted by relevance.
    """
    matches = []

    for world_id, world in WORLDS_DERIVED.items():
        match = True
        score = 0

        # World type filter
        if 'world_type' in criteria:
            if world.get('world_type') != criteria['world_type']:
                match = False

        # REE enrichment minimum
        if 'ree_enrichment_min' in criteria:
            if world.get('ree_enrichment', 0) < criteria['ree_enrichment_min']:
                match = False
            else:
                score += world.get('ree_enrichment', 0)

        # Habitability minimum
        if 'habitability_min' in criteria:
            if world.get('habitability_score', 0) < criteria['habitability_min']:
                match = False
            else:
                score += world.get('habitability_score', 0)

        # Brain hinge proximity maximum
        if 'brain_hinge_offset_max' in criteria:
            if world.get('brain_hinge_offset', 100) > criteria['brain_hinge_offset_max']:
                match = False
            else:
                score += 10 / (1 + world.get('brain_hinge_offset', 100))

        # Formation bracket range
        if 'formation_bracket_range' in criteria:
            fb = world.get('formation_bracket', 0)
            range_min, range_max = criteria['formation_bracket_range']
            if fb < range_min or fb > range_max:
                match = False

        # Has REE orbital signature
        if criteria.get('has_ree_signature', False):
            if not world.get('has_ree_orbital_signature', False):
                match = False
            else:
                score += 50

        if match:
            matches.append({
                'id': world_id,
                'score': score,
                **world
            })

    # Sort by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

def find_earth_analogues():
    """
    Shortcut: Find worlds most similar to Earth.
    """
    earth = WORLDS_DERIVED.get('earth', {})
    return search_worlds({
        'world_type': 'rocky_standard',
        'habitability_min': 60,
        'brain_hinge_offset_max': 5,
    })

def find_ree_rich_worlds():
    """
    Shortcut: Find worlds with high REE enrichment potential.
    """
    return search_worlds({
        'ree_enrichment_min': 10,
        'formation_bracket_range': [142.0, 143.0],
    })

def find_habitable_zone_worlds():
    """
    Shortcut: Find worlds in the habitable zone (inside ice line, rocky).
    """
    return search_worlds({
        'formation_bracket_range': [142.5, 146.8],  # Post-silicate cliff, pre-ice line
        'habitability_min': 50,
    })

# ═══════════════════════════════════════════════
# GEOLOGICAL LAYER GENERATION
# For planetary cross-section visualization
# ═══════════════════════════════════════════════

def generate_geological_layers(world_id):
    """
    Generate geological layer data for visualization.
    Uses formation bracket to determine composition.
    """
    world = WORLDS_DERIVED.get(world_id)
    if not world:
        return None

    fb = world.get('formation_bracket', 143.0)
    radius_km = world.get('radius_km', 6371)
    world_type = world.get('world_type', 'rocky_standard')

    layers = []

    if world_type in ['rocky_enriched', 'rocky_standard']:
        # Rocky world: core, mantle, crust

        # Core (iron-nickel from bracket 143.5)
        core_fraction = 0.32  # Earth-like default
        if fb < 142.5:
            core_fraction = 0.50  # Mercury-like, iron-rich

        layers.append({
            'name': 'Inner Core',
            'depth_fraction': 0.0,
            'thickness_fraction': core_fraction * 0.3,
            'composition': 'Solid Fe-Ni',
            'color': '#B87333',
            'bracket': 143.5,
        })
        layers.append({
            'name': 'Outer Core',
            'depth_fraction': core_fraction * 0.3,
            'thickness_fraction': core_fraction * 0.7,
            'composition': 'Liquid Fe-Ni',
            'color': '#CD7F32',
            'bracket': 143.5,
        })

        # Mantle (silicates from bracket 142.65)
        mantle_fraction = 1.0 - core_fraction - 0.01
        layers.append({
            'name': 'Lower Mantle',
            'depth_fraction': core_fraction,
            'thickness_fraction': mantle_fraction * 0.6,
            'composition': 'Perovskite (MgSiO₃)',
            'color': '#8B4513',
            'bracket': 142.65,
        })
        layers.append({
            'name': 'Upper Mantle',
            'depth_fraction': core_fraction + mantle_fraction * 0.6,
            'thickness_fraction': mantle_fraction * 0.4,
            'composition': 'Olivine (Mg₂SiO₄)',
            'color': '#228B22',
            'bracket': 142.67,
        })

        # Crust (REE concentrated here)
        ree = world.get('ree_enrichment', 1.6)
        crust_color = '#00FF88' if ree > 10 else '#A0522D'
        layers.append({
            'name': 'Crust',
            'depth_fraction': 0.99,
            'thickness_fraction': 0.01,
            'composition': f'Granite/Basalt (REE: {ree:.1f}×)',
            'color': crust_color,
            'bracket': 142.7,
            'ree_enrichment': ree,
        })

    elif world_type == 'ice_giant':
        # Uranus/Neptune type
        layers.append({
            'name': 'Rocky Core',
            'depth_fraction': 0.0,
            'thickness_fraction': 0.25,
            'composition': 'Silicate-iron core',
            'color': '#8B4513',
            'bracket': 143.0,
        })
        layers.append({
            'name': 'Ice Mantle',
            'depth_fraction': 0.25,
            'thickness_fraction': 0.55,
            'composition': 'Water-ammonia-methane ices',
            'color': '#00CED1',
            'bracket': 147.5,
        })
        layers.append({
            'name': 'Atmosphere',
            'depth_fraction': 0.80,
            'thickness_fraction': 0.20,
            'composition': 'H₂, He, CH₄',
            'color': '#87CEEB',
            'bracket': 150.0,
        })

    elif world_type == 'volatile_rich':
        # Kuiper belt / comet type
        layers.append({
            'name': 'Rocky Core',
            'depth_fraction': 0.0,
            'thickness_fraction': 0.30,
            'composition': 'Silicate-organic mix',
            'color': '#696969',
            'bracket': 143.5,
        })
        layers.append({
            'name': 'Ice Shell',
            'depth_fraction': 0.30,
            'thickness_fraction': 0.70,
            'composition': 'N₂, CO, CH₄ ices',
            'color': '#B0E0E6',
            'bracket': 150.0,
        })

    return {
        'world_id': world_id,
        'world_name': world.get('name', world_id),
        'radius_km': radius_km,
        'world_type': world_type,
        'formation_bracket': fb,
        'layers': layers,
    }


# ═══════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════

@app.route('/')
def index():
    """Main universe simulator page"""
    # Server-side render initial data for speed
    initial_data = {
        'phi': PHI,
        'golden_angle': GOLDEN_ANGLE,
        'wall_fraction': WALL_FRACTION,
        'hinge_const': HINGE_CONST,
        'unity_check': verify_unity(),
        'wall': wall_layers(),
        'alpha_universe': alpha_coupling(294),
        'hinges': key_hinges(294),
        'boundaries': sector_boundaries(294),
        'solar_system': SOLAR_SYSTEM,
        'milky_way': MILKY_WAY,
        'element_condensation': ELEMENT_CONDENSATION,
        'mineral_deposits': EARTH_MINERAL_DEPOSITS,
        'zoom_levels': ZOOM_LEVELS,
        'ree_signature': REE_TARGETING_SIGNATURE,
        'earth_timeline': EARTH_TIMELINE,
    }
    return render_template('index.html', data=initial_data)

@app.route('/api/constants')
def api_constants():
    """Return all phi constants"""
    return jsonify({
        'phi': PHI,
        'phi2': PHI2,
        'phi3': PHI3,
        'phi4': PHI4,
        'inv_phi': INV_PHI,
        'inv_phi2': INV_PHI2,
        'inv_phi3': INV_PHI3,
        'inv_phi4': INV_PHI4,
        'golden_angle': GOLDEN_ANGLE,
        'hinge_const': HINGE_CONST,
        'wall_fraction': WALL_FRACTION,
        'l_planck': L_PLANCK,
        'calib_factor': CALIB_FACTOR,
    })

@app.route('/api/bracket/<int:n>')
def api_bracket(n):
    """Get bracket information"""
    scale = bracket_scale(n)
    bounds = sector_boundaries(294)

    # Determine sector
    sector = 'sigma5'
    if n <= bounds['sigma1_end']:
        sector = 'sigma1'
    elif n <= bounds['sigma2_end']:
        sector = 'sigma2'
    elif n <= bounds['sigma3_end']:
        sector = 'sigma3'
    elif n <= bounds['sigma4_end']:
        sector = 'sigma4'

    return jsonify({
        'bracket': n,
        'scale_meters': scale,
        'scale_formatted': format_scale(scale),
        'sector': sector,
        'zeckendorf': zeckendorf(n),
        'curvature': len(zeckendorf(n)) - 1,
        'alpha': alpha_coupling(n) if n > 0 else None,
    })

@app.route('/api/solar_system')
def api_solar_system():
    """Get solar system data with phi brackets"""
    result = {}
    for body, data in SOLAR_SYSTEM.items():
        distance_m = data['distance_au'] * AU_METERS
        bracket = bracket_from_scale(distance_m) if distance_m > 0 else 0
        result[body] = {
            **data,
            'distance_m': distance_m,
            'phi_bracket': bracket,
            'zeckendorf': zeckendorf(int(bracket)) if bracket > 0 else [],
        }
    return jsonify(result)

@app.route('/api/milky_way')
def api_milky_way():
    """Get Milky Way reference points with phi brackets"""
    result = {}
    for ref, data in MILKY_WAY.items():
        distance_m = data['distance_ly'] * LY_METERS
        bracket = bracket_from_scale(distance_m)
        result[ref] = {
            **data,
            'distance_m': distance_m,
            'phi_bracket': bracket,
            'zeckendorf': zeckendorf(int(bracket)),
        }
    return jsonify(result)

@app.route('/api/triangulate', methods=['POST'])
def api_triangulate():
    """Triangulate position from multiple reference points"""
    data = request.json
    points = data.get('points', [])

    if len(points) < 3:
        return jsonify({'error': 'Need at least 3 reference points'}), 400

    # Simple centroid calculation for now
    # More sophisticated triangulation can be added
    x_sum = sum(p.get('x', 0) for p in points)
    y_sum = sum(p.get('y', 0) for p in points)
    z_sum = sum(p.get('z', 0) for p in points)
    n = len(points)

    centroid = {
        'x': x_sum / n,
        'y': y_sum / n,
        'z': z_sum / n,
    }

    # Calculate distance from origin
    distance = math.sqrt(centroid['x']**2 + centroid['y']**2 + centroid['z']**2)
    bracket = bracket_from_scale(distance) if distance > 0 else 0

    return jsonify({
        'centroid': centroid,
        'distance_m': distance,
        'phi_bracket': bracket,
        'zeckendorf': zeckendorf(int(bracket)) if bracket > 0 else [],
    })

@app.route('/api/scaling_vectors', methods=['GET', 'POST'])
def api_scaling_vectors():
    """Get or save scaling vectors"""
    if request.method == 'POST':
        data = request.json
        success = save_scaling_vector(data)
        return jsonify({'success': success})
    else:
        vector_type = request.args.get('type')
        vectors = get_scaling_vectors(vector_type)
        return jsonify(vectors)

@app.route('/api/verify')
def api_verify():
    """Verification endpoint"""
    wall = wall_layers()
    return jsonify({
        'unity_equation': verify_unity(),
        'sector_sum': 2 * INV_PHI4 + 3 * INV_PHI3,
        'wall': wall,
        'alpha_inverse_294': 294 * wall['total'],
        'alpha_measured': 137.036,
        'error_percent': abs(294 * wall['total'] - 137.036) / 137.036 * 100,
        'hinge_const': HINGE_CONST,
        'bracket_128_scale': bracket_scale(128),
        'bracket_94_scale': bracket_scale(94),
        'bracket_164_scale': bracket_scale(164),
    })


# ═══════════════════════════════════════════════
# MINERAL EXPLORATION API
# ═══════════════════════════════════════════════

@app.route('/api/element_condensation')
def api_element_condensation():
    """Get element condensation data from Quantum Rosetta"""
    result = {}
    for zone_id, zone_data in ELEMENT_CONDENSATION.items():
        bracket = zone_data.get('bracket', zone_data.get('bracket_start', 0))
        scale = bracket_scale(bracket)
        result[zone_id] = {
            **zone_data,
            'scale_meters': scale,
            'scale_formatted': format_scale(scale),
            'has_ree_signature': has_ree_signature(zone_data.get('zeckendorf', []))
        }
    return jsonify(result)

@app.route('/api/mineral_deposits')
def api_mineral_deposits():
    """Get Earth mineral deposits with Zeckendorf signatures"""
    result = {}
    for deposit_id, deposit in EARTH_MINERAL_DEPOSITS.items():
        zeck = deposit.get('zeckendorf_signature', [])
        result[deposit_id] = {
            **deposit,
            'has_ree_signature': has_ree_signature(zeck),
            'zeckendorf_sum': sum(zeck),
            'curvature': len(zeck) - 1
        }
    return jsonify(result)

@app.route('/api/ree_targeting')
def api_ree_targeting():
    """Find deposits with REE targeting signature {89, 34, 13}"""
    ree_deposits = []
    for deposit_id, deposit in EARTH_MINERAL_DEPOSITS.items():
        zeck = deposit.get('zeckendorf_signature', [])
        if has_ree_signature(zeck):
            ree_deposits.append({
                'id': deposit_id,
                'name': deposit['name'],
                'location': deposit['location'],
                'country': deposit['country'],
                'type': deposit['type'],
                'zeckendorf': zeck,
                'elements': deposit.get('primary_elements', [])
            })
    return jsonify({
        'targeting_signature': REE_TARGETING_SIGNATURE,
        'signature_sum': sum(REE_TARGETING_SIGNATURE),
        'deposits_found': len(ree_deposits),
        'deposits': ree_deposits
    })

@app.route('/api/golden_angle_correlations')
def api_golden_angle_correlations():
    """Calculate golden angle correlations between mineral deposits"""
    correlations = []
    deposit_list = list(EARTH_MINERAL_DEPOSITS.items())

    for i, (id1, dep1) in enumerate(deposit_list):
        for j, (id2, dep2) in enumerate(deposit_list):
            if i >= j:
                continue
            loc1 = dep1['location']
            loc2 = dep2['location']
            result = calculate_golden_angle_distance(
                loc1['lat'], loc1['lon'],
                loc2['lat'], loc2['lon']
            )
            if result['golden_angle_match'] or result['fibonacci_angle_match']:
                correlations.append({
                    'from': {'id': id1, 'name': dep1['name']},
                    'to': {'id': id2, 'name': dep2['name']},
                    'distance_km': result['distance_km'],
                    'bearing_deg': result['bearing_deg'],
                    'golden_angle_match': result['golden_angle_match'],
                    'fibonacci_angle_match': result['fibonacci_angle_match']
                })

    return jsonify({
        'golden_angle': GOLDEN_ANGLE,
        'correlations_found': len(correlations),
        'correlations': correlations
    })


# ═══════════════════════════════════════════════
# ZOOM LEVELS & EVOLUTION API
# ═══════════════════════════════════════════════

@app.route('/api/zoom_levels')
def api_zoom_levels():
    """Get zoom level definitions"""
    result = {}
    for level, data in ZOOM_LEVELS.items():
        bracket_mid = (data['bracket_min'] + data['bracket_max']) / 2
        scale_min = bracket_scale(data['bracket_min'])
        scale_max = bracket_scale(data['bracket_max'])
        result[level] = {
            **data,
            'scale_min': format_scale(scale_min),
            'scale_max': format_scale(scale_max),
            'bracket_mid': bracket_mid
        }
    return jsonify(result)

@app.route('/api/evolve', methods=['POST'])
def api_evolve():
    """Evolve universe detail at a specific zoom level"""
    data = request.json
    zoom_level = data.get('zoom_level', 0)
    session_id = data.get('session_id', f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    # Ensure table exists
    ensure_evolution_table()

    # Load existing state or create new
    state = load_evolution_state(session_id)
    if not state:
        state = {
            'session_id': session_id,
            'zoom_level': zoom_level,
            'current_bracket': ZOOM_LEVELS[zoom_level]['bracket_min'],
            'evolved_features': [],
            'mineral_deposits': [],
            'evolution_progress': 0.0
        }

    # Get zoom level data
    level_data = ZOOM_LEVELS.get(zoom_level, ZOOM_LEVELS[0])
    features_to_evolve = level_data['detail_features']

    # Evolve based on level
    new_features = []
    new_deposits = []

    if zoom_level == 4:  # Geological level - add mineral exploration
        # Add element condensation zones
        for zone_id, zone_data in ELEMENT_CONDENSATION.items():
            if zone_id not in state['evolved_features']:
                new_features.append({
                    'type': 'element_condensation',
                    'id': zone_id,
                    'bracket': zone_data.get('bracket', zone_data.get('bracket_start', 0)),
                    'temperature_K': zone_data.get('temperature_K', 0),
                    'elements': zone_data.get('elements', []),
                    'has_ree': has_ree_signature(zone_data.get('zeckendorf', []))
                })

        # Add mineral deposits with REE signatures
        for deposit_id, deposit in EARTH_MINERAL_DEPOSITS.items():
            if deposit_id not in [d.get('id') for d in state['mineral_deposits']]:
                zeck = deposit.get('zeckendorf_signature', [])
                new_deposits.append({
                    'id': deposit_id,
                    'name': deposit['name'],
                    'location': deposit['location'],
                    'type': deposit['type'],
                    'elements': deposit.get('primary_elements', []),
                    'has_ree_signature': has_ree_signature(zeck),
                    'zeckendorf': zeck
                })

    elif zoom_level == 2:  # Solar system level
        for body, body_data in SOLAR_SYSTEM.items():
            if body not in state['evolved_features']:
                distance_m = body_data['distance_au'] * AU_METERS
                bracket = bracket_from_scale(distance_m) if distance_m > 0 else 0
                new_features.append({
                    'type': 'solar_body',
                    'id': body,
                    'name': body_data['name'],
                    'distance_au': body_data['distance_au'],
                    'phi_bracket': bracket,
                    'zeckendorf': zeckendorf(int(bracket)) if bracket > 0 else []
                })

    elif zoom_level == 1:  # Galaxy level
        for ref, ref_data in MILKY_WAY.items():
            if ref not in state['evolved_features']:
                distance_m = ref_data['distance_ly'] * LY_METERS
                bracket = bracket_from_scale(distance_m)
                new_features.append({
                    'type': 'galactic_reference',
                    'id': ref,
                    'name': ref_data['name'],
                    'distance_ly': ref_data['distance_ly'],
                    'phi_bracket': bracket,
                    'zeckendorf': zeckendorf(int(bracket))
                })

    # Update state
    state['evolved_features'].extend([f['id'] for f in new_features])
    state['mineral_deposits'].extend(new_deposits)
    state['zoom_level'] = zoom_level
    state['evolution_progress'] = min(1.0, state['evolution_progress'] + 0.1 * (len(new_features) + len(new_deposits)))

    # Save state for resumability
    save_evolution_state(session_id, state)

    return jsonify({
        'session_id': session_id,
        'zoom_level': zoom_level,
        'level_name': level_data['name'],
        'new_features': new_features,
        'new_deposits': new_deposits,
        'total_features': len(state['evolved_features']),
        'total_deposits': len(state['mineral_deposits']),
        'evolution_progress': state['evolution_progress'],
        'can_continue': state['evolution_progress'] < 1.0
    })

@app.route('/api/evolution/load/<session_id>')
def api_evolution_load(session_id):
    """Load a saved evolution session"""
    state = load_evolution_state(session_id)
    if state:
        return jsonify({
            'found': True,
            'state': state
        })
    return jsonify({'found': False, 'session_id': session_id})

@app.route('/api/evolution/sessions')
def api_evolution_sessions():
    """List recent evolution sessions"""
    sessions = get_recent_sessions()
    return jsonify({
        'sessions': sessions,
        'count': len(sessions)
    })


# ═══════════════════════════════════════════════
# EARTH EVOLUTION API
# ═══════════════════════════════════════════════

@app.route('/api/earth/timeline')
def api_earth_timeline():
    """Get full Earth evolution timeline"""
    result = {}
    for epoch_id, epoch in EARTH_TIMELINE.items():
        result[epoch_id] = {
            **epoch,
            'phi_bracket': bracket_from_scale(epoch['time_ga'] * 1e9 * 365.25 * 24 * 3600 * 3e8) if epoch['time_ga'] > 0 else 0,
        }
    return jsonify(result)

@app.route('/api/earth/epoch/<float:time_normalized>')
def api_earth_epoch(time_normalized):
    """Get Earth state at a specific normalized time (0.0 = formation, 1.0 = present)"""
    time_normalized = max(0.0, min(1.0, time_normalized))

    # Find bracketing epochs for interpolation
    prev_epoch = None
    next_epoch = None

    for epoch_id, epoch in EARTH_TIMELINE_SORTED:
        if epoch['time_normalized'] <= time_normalized:
            prev_epoch = (epoch_id, epoch)
        if epoch['time_normalized'] >= time_normalized and next_epoch is None:
            next_epoch = (epoch_id, epoch)

    if prev_epoch is None:
        prev_epoch = EARTH_TIMELINE_SORTED[0]
    if next_epoch is None:
        next_epoch = EARTH_TIMELINE_SORTED[-1]

    # Calculate interpolation factor
    prev_t = prev_epoch[1]['time_normalized']
    next_t = next_epoch[1]['time_normalized']

    if next_t == prev_t:
        t = 0.0
    else:
        t = (time_normalized - prev_t) / (next_t - prev_t)

    # Interpolate numerical values
    def lerp(a, b, t):
        return a + (b - a) * t

    prev_data = prev_epoch[1]
    next_data = next_epoch[1]

    # Interpolate color (hex to RGB and back)
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    prev_rgb = hex_to_rgb(prev_data['color'])
    next_rgb = hex_to_rgb(next_data['color'])
    interp_rgb = tuple(lerp(prev_rgb[i], next_rgb[i], t) for i in range(3))

    interpolated = {
        'time_normalized': time_normalized,
        'time_ga': lerp(prev_data['time_ga'], next_data['time_ga'], t),
        'temperature_K': lerp(prev_data['temperature_K'], next_data['temperature_K'], t),
        'ocean_coverage': lerp(prev_data['ocean_coverage'], next_data['ocean_coverage'], t),
        'o2_percent': lerp(prev_data['o2_percent'], next_data['o2_percent'], t),
        'co2_percent': lerp(prev_data['co2_percent'], next_data['co2_percent'], t),
        'color': rgb_to_hex(interp_rgb),
        'color_rgb': list(interp_rgb),
        # Non-interpolated values (use nearest epoch)
        'current_epoch': prev_epoch[0] if t < 0.5 else next_epoch[0],
        'epoch_name': prev_data['name'] if t < 0.5 else next_data['name'],
        'eon': prev_data['eon'] if t < 0.5 else next_data['eon'],
        'era': prev_data.get('era', prev_data['eon']),
        'description': prev_data['description'] if t < 0.5 else next_data['description'],
        'surface': prev_data['surface'] if t < 0.5 else next_data['surface'],
        'atmosphere': prev_data['atmosphere'] if t < 0.5 else next_data['atmosphere'],
        'life': prev_data['life'] if t < 0.5 else next_data['life'],
        'prev_epoch': prev_epoch[0],
        'next_epoch': next_epoch[0],
        'interpolation_t': t
    }

    return jsonify(interpolated)

@app.route('/api/earth/climate/<float:time_ga>')
def api_earth_climate(time_ga):
    """
    Get Earth's climate state at a specific time using the integrated model.

    This combines:
    - Solar luminosity evolution (faint young sun)
    - Greenhouse warming (CO2, CH4, H2O)
    - Tectonic feedback (carbon-silicate cycle)

    Args:
        time_ga: Time in Ga before present (0 = now, 4.57 = formation)
    """
    time_ga = max(0.0, min(4.57, time_ga))
    climate = earth_climate_at_time(time_ga)
    return jsonify(climate)

@app.route('/api/earth/solar-evolution')
def api_solar_evolution():
    """
    Get solar luminosity evolution over Earth's history.

    Returns luminosity at key time points from formation to present.
    """
    time_points = [4.57, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0]
    evolution = []

    for t in time_points:
        L_ratio = solar_luminosity_at_time(t)
        T_eq = equilibrium_temperature(1.0, L_ratio, albedo=0.3)
        evolution.append({
            'time_ga': t,
            'luminosity_ratio': L_ratio,
            'luminosity_watts': L_ratio * L_SUN_TODAY,
            'earth_equilibrium_K': T_eq,
            'earth_equilibrium_C': T_eq - 273.15
        })

    return jsonify({
        'description': 'Solar luminosity evolution over Earth history',
        'faint_young_sun_factor': 0.70,
        'evolution': evolution
    })

@app.route('/api/earth/tectonics/<float:time_ga>')
def api_earth_tectonics(time_ga):
    """
    Get Earth's tectonic state at a specific time.

    Includes:
    - Tectonic vigor (0-1)
    - Radioactive heat production
    - Carbon-silicate cycle state
    """
    time_ga = max(0.0, min(4.57, time_ga))

    climate = earth_climate_at_time(time_ga)

    return jsonify({
        'time_ga': time_ga,
        'tectonic_vigor': climate['tectonic_vigor'],
        'radioactive_heat_ratio': climate['radioactive_heat_ratio'],
        'carbon_cycle': climate['carbon_cycle'],
        'climate_stable': climate['climate_stable'],
        'interpretation': {
            'has_active_tectonics': climate['tectonic_vigor'] > 0.3,
            'tectonics_initiated': time_ga < 3.8,  # Tectonics probably started ~3.8 Ga
            'carbon_cycle_active': climate['carbon_cycle'].get('equilibrium', False)
        }
    })

@app.route('/api/earth/faint-sun-paradox')
def api_faint_sun_paradox():
    """
    Explain and demonstrate the Faint Young Sun Paradox.

    Shows how greenhouse warming compensated for lower solar luminosity.
    """
    explanation = why_water_without_tectonics()

    # Calculate example scenarios
    scenarios = []

    for time_ga in [4.0, 3.0, 2.0, 1.0, 0.0]:
        climate = earth_climate_at_time(time_ga)
        scenarios.append({
            'time_ga': time_ga,
            'solar_luminosity': climate['solar_luminosity_ratio'],
            'T_without_greenhouse': climate['T_equilibrium_K'],
            'T_with_greenhouse': climate['T_surface_K'],
            'greenhouse_warming': climate['greenhouse_compensation_K'],
            'co2_percent': climate['co2_percent'],
            'habitable': climate['habitable']
        })

    return jsonify({
        'summary': explanation['summary'],
        'scenarios': scenarios,
        'water_worlds_without_tectonics': explanation['water_worlds_without_tectonics'],
        'earth_requirements': explanation['earth_tectonic_requirements']
    })

@app.route('/api/earth/save', methods=['POST'])
def api_earth_save():
    """Save Earth evolution state"""
    data = request.json
    session_id = data.get('session_id', f"earth_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    # Save to database
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'})

    try:
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='earth_evolution_state' AND xtype='U')
            CREATE TABLE earth_evolution_state (
                id INT IDENTITY(1,1) PRIMARY KEY,
                session_id VARCHAR(50) NOT NULL,
                time_normalized DECIMAL(10,6) NOT NULL,
                epoch_id VARCHAR(50),
                viewed_epochs NVARCHAR(MAX),
                notes NVARCHAR(MAX),
                created_at DATETIME NOT NULL DEFAULT GETDATE(),
                updated_at DATETIME NOT NULL DEFAULT GETDATE()
            )
        """)

        # Check if session exists
        cursor.execute("SELECT id FROM earth_evolution_state WHERE session_id = %s", (session_id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE earth_evolution_state
                SET time_normalized = %s,
                    epoch_id = %s,
                    viewed_epochs = %s,
                    notes = %s,
                    updated_at = GETDATE()
                WHERE session_id = %s
            """, (
                data.get('time_normalized', 1.0),
                data.get('epoch_id', 'present'),
                json.dumps(data.get('viewed_epochs', [])),
                data.get('notes', ''),
                session_id
            ))
        else:
            cursor.execute("""
                INSERT INTO earth_evolution_state
                (session_id, time_normalized, epoch_id, viewed_epochs, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                session_id,
                data.get('time_normalized', 1.0),
                data.get('epoch_id', 'present'),
                json.dumps(data.get('viewed_epochs', [])),
                data.get('notes', '')
            ))

        conn.commit()
        return jsonify({'success': True, 'session_id': session_id})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()

@app.route('/api/earth/load/<session_id>')
def api_earth_load(session_id):
    """Load saved Earth evolution state"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'found': False, 'error': 'Database connection failed'})

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_id, time_normalized, epoch_id, viewed_epochs, notes, updated_at
            FROM earth_evolution_state
            WHERE session_id = %s
        """, (session_id,))
        row = cursor.fetchone()

        if row:
            return jsonify({
                'found': True,
                'state': {
                    'session_id': row[0],
                    'time_normalized': float(row[1]),
                    'epoch_id': row[2],
                    'viewed_epochs': json.loads(row[3]) if row[3] else [],
                    'notes': row[4],
                    'last_updated': str(row[5])
                }
            })
        return jsonify({'found': False})

    except Exception as e:
        return jsonify({'found': False, 'error': str(e)})
    finally:
        conn.close()

@app.route('/api/earth/sessions')
def api_earth_sessions():
    """List Earth evolution sessions"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'sessions': [], 'error': 'Database connection failed'})

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 20 session_id, time_normalized, epoch_id, updated_at
            FROM earth_evolution_state
            ORDER BY updated_at DESC
        """)
        rows = cursor.fetchall()

        sessions = [{
            'session_id': r[0],
            'time_normalized': float(r[1]),
            'epoch_id': r[2],
            'last_updated': str(r[3])
        } for r in rows]

        return jsonify({'sessions': sessions, 'count': len(sessions)})

    except Exception as e:
        return jsonify({'sessions': [], 'error': str(e)})
    finally:
        conn.close()


# ═══════════════════════════════════════════════
# WORLD CLASSIFICATION API ROUTES
# ═══════════════════════════════════════════════

@app.route('/api/worlds')
def api_worlds():
    """Get all worlds with derived properties"""
    return jsonify(WORLDS_DERIVED)

@app.route('/api/worlds/<world_id>')
def api_world_detail(world_id):
    """Get detailed properties for a specific world"""
    world = WORLDS_DERIVED.get(world_id)
    if not world:
        return jsonify({'error': f'World {world_id} not found'}), 404

    # Add geological layers
    layers = generate_geological_layers(world_id)

    return jsonify({
        **world,
        'geological_layers': layers.get('layers', []) if layers else [],
    })

@app.route('/api/worlds/search', methods=['POST'])
def api_worlds_search():
    """
    Search for worlds meeting specific criteria.

    POST body examples:
        {"world_type": "rocky_standard"}
        {"ree_enrichment_min": 10}
        {"habitability_min": 70}
        {"brain_hinge_offset_max": 5}
        {"formation_bracket_range": [142, 147]}
        {"has_ree_signature": true}
    """
    criteria = request.json or {}
    results = search_worlds(criteria)
    return jsonify({
        'criteria': criteria,
        'count': len(results),
        'worlds': results,
    })

@app.route('/api/worlds/earth-analogues')
def api_earth_analogues():
    """Find worlds most similar to Earth"""
    results = find_earth_analogues()
    return jsonify({
        'description': 'Worlds most similar to Earth',
        'criteria': {
            'world_type': 'rocky_standard',
            'habitability_min': 60,
            'brain_hinge_offset_max': 5,
        },
        'count': len(results),
        'worlds': results,
    })

@app.route('/api/worlds/ree-rich')
def api_ree_rich_worlds():
    """Find worlds with high REE enrichment potential"""
    results = find_ree_rich_worlds()
    return jsonify({
        'description': 'Worlds with high REE enrichment potential',
        'criteria': {
            'ree_enrichment_min': 10,
            'formation_bracket_range': [142.0, 143.0],
        },
        'count': len(results),
        'worlds': results,
    })

@app.route('/api/worlds/habitable-zone')
def api_habitable_zone():
    """Find worlds in the habitable zone"""
    results = find_habitable_zone_worlds()
    return jsonify({
        'description': 'Worlds in the habitable zone (rocky, inside ice line)',
        'criteria': {
            'formation_bracket_range': [142.5, 146.8],
            'habitability_min': 50,
        },
        'count': len(results),
        'worlds': results,
    })

@app.route('/api/worlds/<world_id>/layers')
def api_world_layers(world_id):
    """Get geological layers for a specific world"""
    layers = generate_geological_layers(world_id)
    if not layers:
        return jsonify({'error': f'World {world_id} not found'}), 404
    return jsonify(layers)

@app.route('/api/condensation-zones')
def api_condensation_zones():
    """Get all condensation zones for visualization"""
    return jsonify({
        'zones': CONDENSATION_ZONES,
        'thresholds': BRACKET_THRESHOLDS,
        'ree_signature': REE_TARGETING_SIGNATURE,
    })

@app.route('/api/derive', methods=['POST'])
def api_derive_world():
    """
    Derive properties for a custom world.

    POST body example:
        {
            "name": "My Exoplanet",
            "a_AU": 0.5,
            "radius_km": 7000,
            "has_atmosphere": true,
            "star_luminosity_ratio": 0.5
        }
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    star_lum = data.get('star_luminosity_ratio', 1.0)
    derived = derive_planet_properties(data, star_lum)

    # Add geological layers
    # Create a temporary ID for layer generation
    temp_id = f"custom_{hash(json.dumps(data, sort_keys=True)) % 10000}"
    WORLDS_DERIVED[temp_id] = derived
    layers = generate_geological_layers(temp_id)
    del WORLDS_DERIVED[temp_id]

    return jsonify({
        **derived,
        'geological_layers': layers.get('layers', []) if layers else [],
    })

@app.route('/api/formation-bracket')
def api_formation_bracket():
    """
    Calculate formation bracket for given orbital parameters.

    Query params:
        r_AU: orbital radius in AU
        star_luminosity: star luminosity ratio (default 1.0 for Sun)
    """
    r_AU = float(request.args.get('r_AU', 1.0))
    star_lum = float(request.args.get('star_luminosity', 1.0))

    fb = formation_bracket(r_AU, star_lum)
    temp_K = disk_temperature(r_AU, star_lum)
    ree = ree_enrichment_factor(fb)
    world_type = classify_world_type(fb)

    return jsonify({
        'r_AU': r_AU,
        'star_luminosity_ratio': star_lum,
        'formation_bracket': fb,
        'formation_temp_K': temp_K,
        'ree_enrichment': ree,
        'world_type': world_type,
        'zeckendorf': zeckendorf(int(fb)),
        'has_ree_signature': has_ree_signature(zeckendorf(int(fb))),
    })

@app.route('/api/compare-worlds', methods=['GET', 'POST'])
def api_compare_worlds():
    """
    Compare two worlds side by side.

    GET query params or POST JSON body:
        world1/world1_id: first world ID
        world2/world2_id: second world ID
    """
    if request.method == 'POST':
        data = request.get_json() or {}
        world1_id = data.get('world1_id') or data.get('world1', 'earth')
        world2_id = data.get('world2_id') or data.get('world2', 'mars')
    else:
        world1_id = request.args.get('world1', 'earth')
        world2_id = request.args.get('world2', 'mars')

    world1 = WORLDS_DERIVED.get(world1_id)
    world2 = WORLDS_DERIVED.get(world2_id)

    if not world1:
        return jsonify({'error': f'World {world1_id} not found'}), 404
    if not world2:
        return jsonify({'error': f'World {world2_id} not found'}), 404

    # Calculate differences
    comparison = {
        'world1': world1,
        'world2': world2,
        'differences': {
            'habitability_delta': (
                world1.get('habitability_score', 0) -
                world2.get('habitability_score', 0)
            ),
            'ree_ratio': (
                world1.get('ree_enrichment', 1) /
                max(0.1, world2.get('ree_enrichment', 1))
            ),
            'brain_hinge_closer': (
                world1_id if world1.get('brain_hinge_offset', 100) <
                world2.get('brain_hinge_offset', 100) else world2_id
            ),
            'formation_bracket_delta': (
                world1.get('formation_bracket', 0) -
                world2.get('formation_bracket', 0)
            ),
        }
    }

    return jsonify(comparison)


def format_scale(meters):
    """Format scale to human-readable units"""
    if meters < 1e-15:
        return f"{meters*1e18:.2f} am"  # attometers
    elif meters < 1e-12:
        return f"{meters*1e15:.2f} fm"  # femtometers
    elif meters < 1e-9:
        return f"{meters*1e12:.2f} pm"  # picometers
    elif meters < 1e-6:
        return f"{meters*1e9:.2f} nm"   # nanometers
    elif meters < 1e-3:
        return f"{meters*1e6:.2f} μm"   # micrometers
    elif meters < 1:
        return f"{meters*1e3:.2f} mm"   # millimeters
    elif meters < 1e3:
        return f"{meters:.2f} m"        # meters
    elif meters < 1e6:
        return f"{meters/1e3:.2f} km"   # kilometers
    elif meters < AU_METERS:
        return f"{meters/1e6:.2f} Mm"   # megameters
    elif meters < LY_METERS:
        return f"{meters/AU_METERS:.2f} AU"
    elif meters < 1e6 * LY_METERS:
        return f"{meters/LY_METERS:.2f} ly"
    else:
        return f"{meters/LY_METERS/1e6:.2f} Mly"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=False)
