import numpy as np
from pygmid import Lookup as lk

# 1. Load the LUT (ensure this path matches where your .mat file is in WSL)
try:
    nfet = lk('simulation/nfet_01v8.mat')
except Exception as e:
    print("Error loading LUT. Are you running this from the correct directory?")
    exit()

# 2. Sweep VGS to find maximum efficiency at L=1.0um and VDS=0.9V
vgs_sweep = np.linspace(0.1, 1.8, 100)
gmid = nfet.lookup('GM_ID', VGS=vgs_sweep, VDS=0.9, L=1.0)

# 3. Print the absolute maximum gm/ID value
LENGTH = 0.2      # Length in micrometers
print(f"Length: {LENGTH} um")
print(f"Max gm/ID: {np.max(gmid):.2f} V^-1")
n = 1/(25e-3*np.max(gmid))  # Calculate the subthreshold slope factor n
print(f"Subthreshold slope factor n: {n:.2f}")
target_gmid = np.max(gmid)/2  # Target gm/ID is half of the maximum value
vt = nfet.lookupVGS(GM_ID=target_gmid, VDS=0.9, L=LENGTH)
print(f"Threshold voltage: {vt:.2f} V")
ISQ =nfet.lookup('ID_W', VGS=vt, VDS=0.9, L=LENGTH)*1  # Verify gm/ID at threshold voltage
print(f"ISQ at threshold voltage: {ISQ*1e6:.4f} uA")
