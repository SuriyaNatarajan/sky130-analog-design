* ID-VDS plot for nfet
.lib ~/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
XM1 DRN GATE 0 0 sky130_fd_pr__nfet_01v8 L=0.15 W=5
V_VGS GATE 0 DC 0.9
V_VDS DRN 0 DC 0.9  
.control
dc V_VDS 0 1.8 0.01
let id = -i(V_VDS) 
let gds = deriv(id)
let ro = 1/gds
let dgds_dvds = deriv(gds)
* VDsat ruler 1: half-height of the step in dgds_dvds
let step = dgds_dvds/dgds_dvds[0]
meas dc vdsat_half when step=0.5
* VDsat ruler 2: extend the straight gds line from VDS = 0 down to gds = 0
let vdsat_ext = -gds[0]/dgds_dvds[0]
print vdsat_ext
plot id
plot id ylog
plot gds
plot ro
plot dgds_dvds
plot step
op
print @m.xm1.msky130_fd_pr__nfet_01v8[vdsat] 
.endc
.end