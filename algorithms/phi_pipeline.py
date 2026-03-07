import numpy as np
from scipy.signal import butter, filtfilt, hilbert

phi = (1 + np.sqrt(5)) / 2
freqs = np.array([4.0, 7.0, 11.0, 18.0, 29.0, 47.0])

def full_phi_pipeline(raw_lfp, fs=20000, window_sec=0.5, long_range_depth=3):
    """Full cascade + explicit 3-level skip error correction"""
    if raw_lfp.ndim == 1:
        raw_lfp = raw_lfp.reshape(1, -1)
    n_ch, n_samp = raw_lfp.shape
    win_samples = int(window_sec * fs)
    num_windows = max(1, n_samp // win_samples)
    
    bci_phi = np.zeros(n_ch)
    cascade_unity = np.zeros(n_ch)
    vacuum_fracs = np.zeros((6, n_ch))
    
    for ch in range(n_ch):
        C_windows = []
        delta_windows = []
        
        for w in range(num_windows):
            start = w * win_samples
            end = min(start + win_samples, n_samp)
            if end - start < 200: continue
            
            inst_phase = np.zeros((6, end-start))
            for i, f in enumerate(freqs):
                b, a = butter(4, [f-1.5, f+1.5], fs=fs, btype='band', output='ba')
                filtered = filtfilt(b, a, raw_lfp[ch, start:end])
                analytic = hilbert(filtered)
                inst_phase[i] = np.unwrap(np.angle(analytic))
            
            C = np.zeros((6,6))
            delta = np.zeros((6,6))
            for j in range(6):
                for k in range(j+1,6):
                    dphi = inst_phase[j] - inst_phase[k]
                    coh = np.abs(np.mean(np.exp(1j * dphi)))
                    C[j,k] = C[k,j] = coh
                    dlt = np.mean(dphi) % (2 * np.pi)
                    delta[j,k] = delta[k,j] = dlt
            C_windows.append(C)
            delta_windows.append(delta)
        
        if not C_windows:
            continue
        
        C = np.mean(C_windows, axis=0)
        delta = np.mean(delta_windows, axis=0)
        
        # Full BCI_φ (all pairs)
        idx = np.abs(np.subtract.outer(np.arange(6), np.arange(6)))
        w = 1.0 / (phi ** idx)
        w /= w.sum()
        predicted = (2 * np.pi / phi**2) * idx
        cos_term = np.cos(delta - predicted)
        bci_phi[ch] = np.sum(w * C * cos_term)
        
        # Deeper error correction: explicit weighting for 3-level skip connections
        long_range_weight = 0.0
        if long_range_depth >= 3:
            # L1↔L4, L2↔L5, L3↔L6 (3 steps)
            for start in range(3):
                j = start
                k = start + 3
                if k < 6:
                    long_range_weight += C[j,k] * 0.618   # 1/φ strength for skip connections
        
        # Cascade Unity Score (your original identity)
        unity_score = (C[0,5] * 0.146 +          # forward 1/φ⁴
                       C[1,4] * 0.236 +          # vacuum 1/φ³
                       np.mean(C[0:3,3:6]) * 0.618 +   # gap 1/φ
                       long_range_weight)          # ← your 3-level correction
        cascade_unity[ch] = np.clip(unity_score, 0, 1.0)
        
        # Vacuum fraction
        for lev in range(6):
            adj = []
            if lev > 0: adj.append(lev-1)
            if lev < 5: adj.append(lev+1)
            if adj:
                coh = np.mean([C[lev,a] for a in adj])
                cos_m = np.mean([np.cos(delta[lev,a] - 2*np.pi/phi**2) for a in adj])
                vf = max(coh * max(cos_m, 0) * 0.45, 0)
                vacuum_fracs[lev,ch] = vf
    
    return {
        'bci_phi': np.nan_to_num(bci_phi, nan=0.0),
        'cascade_unity': np.nan_to_num(cascade_unity, nan=0.0),
        'mean_vacuum': np.nan_to_num(vacuum_fracs.mean(), nan=0.0)
    }
