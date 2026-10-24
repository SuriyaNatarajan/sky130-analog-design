* ID-VGS plot for nfet
.lib ~/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
XM1 DRN GATE 0 0 sky130_fd_pr__nfet_01v8 L=0.15 W=5
V_VGS GATE 0 DC 0.9
V_VDS DRN 0 DC 0.9  
.control
dc V_VGS 0 1.8 0.01
plot -i(V_VDS)
.endc
.end