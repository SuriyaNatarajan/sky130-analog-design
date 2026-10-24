import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def write_netlists():
    vgs_netlist = '''**.subckt prob01_ekv
XM1 Vd Vg vss vss sky130_fd_pr__nfet_01v8 L=0.15 W=1 nf=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 mult=1
VGS Vg vss 0
VDS Vd vss 1.8
VSS vss 0 0
.lib /home/suriya/pdk/sky130A/libs.tech/combined/sky130.lib.spice tt
.control
save all
dc VGS 0 1.8 0.001
set filetype=ascii
write id_vgs.raw
.endc
.end
'''
    vds_netlist = '''**.subckt prob01_ekv
XM1 Vd Vg vss vss sky130_fd_pr__nfet_01v8 L=0.15 W=1 nf=1 ad=0.29 as=0.29 pd=2.58 ps=2.58 nrd=0.29 nrs=0.29 sa=0 sb=0 sd=0 mult=1
VGS Vg vss 0
VDS Vd vss 1.8
VSS vss 0 0
.lib /home/suriya/pdk/sky130A/libs.tech/combined/sky130.lib.spice tt
.control
save all
dc VDS 0 1.8 0.001 VGS 0 1.6 0.4
set filetype=ascii
write id_vds.raw
.endc
.end
'''
    with open('id_vgs.spice', 'w') as f: f.write(vgs_netlist)
    with open('id_vds.spice', 'w') as f: f.write(vds_netlist)

def run_ngspice():
    subprocess.run(['ngspice', '-b', 'id_vgs.spice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ngspice', '-b', 'id_vds.spice'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def parse_ascii_raw(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    var_start = lines.index('Variables:\n') + 1
    val_start = lines.index('Values:\n') + 1
    
    vars = []
    for line in lines[var_start:val_start-1]:
        parts = line.split()
        vars.append(parts[1])
        
    num_vars = len(vars)
    vals = []
    for line in lines[val_start:]:
        parts = line.split()
        if len(parts) > 0:
            if len(parts) == 2 and parts[0].isdigit():
                vals.append(float(parts[1]))
            else:
                vals.append(float(parts[0]))
                
    vals = np.array(vals).reshape(-1, num_vars)
    
    data = {}
    for i, v in enumerate(vars):
        data[v] = vals[:, i]
    return data

def plot_and_cleanup():
    # 1. Plot ID vs VGS
    data_vgs = parse_ascii_raw('id_vgs.raw')
    vgs = data_vgs['v(v-sweep)']
    # Get current (ngspice saves current as negative for sourcing V sources)
    # Drain current flows into Vd, so VDS supplies it. i(VDS) is negative of drain current.
    # Actually ngspice saves branch currents. Let's just take abs() to be safe.
    id_vgs = np.abs(data_vgs['i(vds)'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Linear scale
    ax1.plot(vgs, id_vgs * 1e6, linewidth=2, color='blue')
    ax1.set_xlabel('VGS (V)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('ID (uA)', fontsize=12, fontweight='bold')
    ax1.set_title('ID vs VGS (Linear)', fontsize=14, fontweight='bold')
    ax1.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Log scale
    ax2.semilogy(vgs, id_vgs, linewidth=2, color='red')
    ax2.set_xlabel('VGS (V)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('ID (A)', fontsize=12, fontweight='bold')
    ax2.set_title('ID vs VGS (Log) - EKV Subthreshold', fontsize=14, fontweight='bold')
    ax2.grid(True, which='both', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('plot_id_vgs_python.png', dpi=300)
    plt.close()
    
    # 2. Plot ID vs VDS for multiple VGS
    data_vds = parse_ascii_raw('id_vds.raw')
    vds_all = data_vds['v(v-sweep)']
    id_vds_all = np.abs(data_vds['i(vds)'])
    
    # We swept VGS 0 to 1.6 step 0.4 -> 5 traces
    # VDS swept 0 to 1.8 step 0.001 -> 1801 points
    num_vgs_steps = 5
    pts_per_trace = len(vds_all) // num_vgs_steps
    
    plt.figure(figsize=(10, 6))
    vgs_values = [0, 0.4, 0.8, 1.2, 1.6]
    
    for i in range(num_vgs_steps):
        start = i * pts_per_trace
        end = start + pts_per_trace
        
        # Ngspice sweeps 2D variables. Check outer variable logic.
        vds_trace = vds_all[start:end]
        id_trace = id_vds_all[start:end]
        plt.plot(vds_trace, id_trace * 1e6, linewidth=2, label=f'VGS = {vgs_values[i]:.1f} V')
        
    plt.xlabel('VDS (V)', fontsize=12, fontweight='bold')
    plt.ylabel('ID (uA)', fontsize=12, fontweight='bold')
    plt.title('Output Characteristics (ID vs VDS) showing CLM', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('plot_id_vds_python.png', dpi=300)
    plt.close()

    # Cleanup raw files
    os.remove('id_vgs.raw')
    os.remove('id_vds.raw')
    os.remove('id_vgs.spice')
    os.remove('id_vds.spice')

if __name__ == '__main__':
    os.chdir('/home/suriya/analog_lab/scripts/')
    write_netlists()
    run_ngspice()
    plot_and_cleanup()
