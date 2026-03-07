import numpy as np
from phi_pipeline import full_phi_pipeline

# Simulate two Watcher users <2m apart
signal1 = np.sin(2*np.pi*47*np.arange(0, 30, 1/20000)) + np.random.randn(600000)*0.2
signal2 = signal1 + 0.8*np.sin(2*np.pi*47*np.arange(0, 30, 1/20000) + 2*np.pi/phi**2)  # phase-locked

res1 = full_phi_pipeline(signal1.reshape(1,-1))
res2 = full_phi_pipeline(signal2.reshape(1,-1))
print(f"Single BCI_φ: {res1['bci_phi'][0]:.3f} | Paired BCI_φ: {res2['bci_phi'][0]:.3f} (vacuum coupling boost)")
