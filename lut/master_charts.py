import numpy as np
import matplotlib.pyplot as plt
from pygmid import Lookup as lk

# 1. Load the LUT
nfet = lk('simulation/nfet_01v8.mat')

# 2. Define the x-axis: Efficiency sweeping from Strong (5) to Weak (20) Inversion
gmid_sweep = np.linspace(5, 20, 100)
VDS_target = 0.9

# We will plot for three different channel lengths
lengths = [0.15, 0.5, 1.0]
colors = ['r', 'g', 'b']

# Create a figure with 3 subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

for L, color in zip(lengths, colors):
    # --- CHART 1: Transit Frequency (Speed) ---
    # GM_CGG returns radians/sec. Divide by 2*pi to get Hertz (f_T)
    omega_t = nfet.lookup('GM_CGG', GM_ID=gmid_sweep, VDS=VDS_target, L=L)
    f_T = omega_t / (2 * np.pi)
    
    axs[0].plot(gmid_sweep, f_T / 1e9, color=color, linewidth=2, label=f'L = {L}um')
    
    # --- CHART 2: Intrinsic Gain (Gain) ---
    gain = nfet.lookup('GM_GDS', GM_ID=gmid_sweep, VDS=VDS_target, L=L)
    axs[1].plot(gmid_sweep, gain, color=color, linewidth=2, label=f'L = {L}um')
    
    # --- CHART 3: Current Density (Biasing/Size) ---
    id_w = nfet.lookup('ID_W', GM_ID=gmid_sweep, VDS=VDS_target, L=L)
    # Log scale is usually best for current density
    axs[2].semilogy(gmid_sweep, id_w * 1e6, color=color, linewidth=2, label=f'L = {L}um')

# Formatting Chart 1 (Speed)
axs[0].set_title('Transit Frequency (f_T) vs. gm/ID')
axs[0].set_ylabel('f_T [GHz]')
axs[0].grid(True, which="both", ls="--", alpha=0.5)
axs[0].legend()

# Formatting Chart 2 (Gain)
axs[1].set_title('Intrinsic Gain (gm/gds) vs. gm/ID')
axs[1].set_ylabel('gm/gds [V/V]')
axs[1].grid(True, which="both", ls="--", alpha=0.5)
axs[1].legend()

# Formatting Chart 3 (Current Density)
axs[2].set_title('Current Density (ID/W) vs. gm/ID')
axs[2].set_ylabel('ID/W [uA/um]')
axs[2].set_xlabel('gm/ID [V^-1]')
axs[2].grid(True, which="both", ls="--", alpha=0.5)
axs[2].legend()

plt.tight_layout()
plt.savefig('master_charts.png')
print("Saved 'master_charts.png' to disk.")

# Print the peak f_T for L=0.15um at gm/ID = 5
fT_peak_015 = (nfet.lookup('GM_CGG', GM_ID=5.0, VDS=0.9, L=0.15)) / (2 * np.pi)
print(f"Peak f_T for L=0.15um at gm/ID=5 is: {fT_peak_015 / 1e9:.2f} GHz")
