import numpy as np
phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def generate_protocol_stim(protocol='A', duration=1.0, fs=20000, max_current=20e-6):
    t = np.arange(0, duration, 1/fs)
    stim = np.zeros_like(t, dtype=float)
    if protocol == 'A':  # Enhancement
        for i, f in enumerate(freqs):
            amp = max_current / phi**i
            phase = (2*np.pi / phi**2) * i
            stim += amp * np.sin(2*np.pi*f*t + phase)
    elif protocol == 'B':  # Suppression (Sapiens anti-attractor)
        anti_f = [f / phi**2 for f in freqs]
        for i, f in enumerate(anti_f):
            stim += (max_current*0.6 / phi**i) * np.sin(2*np.pi*f*t)
    elif protocol == 'C':  # Full cascade sync
        for i, f in enumerate(freqs):
            amp = max_current / phi**i
            phase = (2*np.pi / phi**2) * i
            stim += amp * np.sin(2*np.pi*f*t + phase)
    return t, stim * (max_current / np.max(np.abs(stim)))
