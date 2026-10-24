import numpy as np
import matplotlib.pyplot as plt
from pygmid import Lookup as lk

# 1. Load the LUT
nfet = lk('simulation/nfet_01v8.mat')

L = 0.5 #length in um
V_DS = 0.9 #VDS in V
gm_gds_target = 10 # instrisinc gain gm/gds in V/V
gm = 1e-3 #gm in S
gmid_sweep = np.linspace(1, 20, 1000)
gm_gds = nfet.lookup('GM_GDS', GM_ID=gmid_sweep, VDS=V_DS, L=L)
print(f"L={L}um, VDS={V_DS}V, GM={gm:.2e}S, GM_GDS target={gm_gds_target} V/V")


crossing_indices = np.where(np.diff(np.sign(gm_gds - gm_gds_target)) != 0)[0]
if crossing_indices.size == 0:
	print(f'GM_GDS target {gm_gds_target} V/V is not reached in the sweep.')
else:
	crossing_gm_ids = []
	for index in crossing_indices:
		crossing_gm_id = np.interp(
			gm_gds_target,
			gm_gds[index:index + 2],
			gmid_sweep[index:index + 2],
		)
		crossing_gm_ids.append(crossing_gm_id)
		print(f'GM_GDS={gm_gds_target} V/V at GM_ID={crossing_gm_id:.4f} 1/V')

plt.plot(gmid_sweep, gm_gds, label=f'L={L}um, VDS={V_DS}V')
plt.axhline(gm_gds_target, color='tab:red', linestyle='--', label=f'Target={gm_gds_target} V/V')
if crossing_indices.size > 0:
	plt.scatter(crossing_gm_ids, [gm_gds_target] * len(crossing_gm_ids), color='tab:red', zorder=3)
plt.xlabel('GM_ID')
plt.ylabel('GM_GDS')
plt.legend()
plt.savefig('gain_plot.png')
ID = gm/crossing_gm_id
print("ID =", ID*1e6, 'uA')  # Convert to uA/um for better readability
ID_W = nfet.lookup('ID_W', GM_ID=crossing_gm_id, VDS=V_DS, L=L)
W = ID/ID_W
print("W =", W, 'um')  # Convert to um for better readability
print(nfet._Lookup__DATA['TEMP'])  # Print the keys of the __DATA dictionary


