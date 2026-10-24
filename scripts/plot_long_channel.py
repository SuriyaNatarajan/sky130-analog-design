import os, subprocess
import numpy as np
import matplotlib.pyplot as plt

os.chdir('/home/suriya/analog_lab/scripts')

netlist = '''**.subckt prob01_ekv
XM1 Vd Vg vss vss sky130_fd_pr__nfet_01v8 L=1 W=5 nf=1 ad=1.45 as=1.45 pd=10.58 ps=10.58 nrd=0.058 nrs=0.058 sa=0 sb=0 sd=0 mult=1
VGS Vg vss 0
VDS Vd vss 1.8
VSS vss 0 0
.lib /home/suriya/pdk/sky130A/libs.tech/combined/sky130.lib.spice tt
.control
save all
dc VDS 0 1.8 0.001 VGS 0 1.6 0.4
set filetype=ascii
write id_vds_long.raw
.endc
.end
'''
with open('id_vds_long.spice', 'w') as f:
    f.write(netlist)

subprocess.run(['ngspice', '-b', 'id_vds_long.spice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def parse_ascii_raw(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    var_start = lines.index('Variables:\n') + 1
    val_start = lines.index('Values:\n') + 1
    vars = [line.split()[1] for line in lines[var_start:val_start-1]]
    vals = []
    for line in lines[val_start:]:
        parts = line.split()
        if len(parts) > 0:
            vals.append(float(parts[1] if len(parts)==2 and parts[0].isdigit() else parts[0]))
    vals = np.array(vals).reshape(-1, len(vars))
    return {v: vals[:, i] for i, v in enumerate(vars)}

data = parse_ascii_raw('id_vds_long.raw')
vds_all = data['v(v-sweep)']
id_vds_all = np.abs(data['i(vds)'])

num_vgs_steps = 5
pts_per_trace = len(vds_all) // num_vgs_steps
vgs_values = [0, 0.4, 0.8, 1.2, 1.6]

plt.figure(figsize=(10, 6))
for i in range(num_vgs_steps):
    start = i * pts_per_trace
    end = start + pts_per_trace
    plt.plot(vds_all[start:end], id_vds_all[start:end] * 1e6, linewidth=2, label=f'VGS = {vgs_values[i]:.1f} V')

plt.xlabel('VDS (V)', fontsize=12, fontweight='bold')
plt.ylabel('ID (uA)', fontsize=12, fontweight='bold')
plt.title('Output Characteristics (W=5u, L=1u) - Classic Square Law Restored!', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('plot_id_vds_long_python.png', dpi=300)
plt.close()

os.remove('id_vds_long.raw')
os.remove('id_vds_long.spice')
