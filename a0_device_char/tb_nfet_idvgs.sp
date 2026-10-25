* ID-VGS plot for nfet
.lib ~/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
XM1 DRN GATE 0 0 sky130_fd_pr__nfet_01v8 L=0.15 W=5
V_VGS GATE 0 DC 0.9
V_VDS DRN 0 DC 0.2  
.control
dc V_VGS 0 1.8 0.01
let id = -i(V_VDS) 
let gm = deriv(id)
let gm_id = deriv(ln(id))
let id_gm = 1/gm_id
let inv_alpha_power = deriv(id_gm)
* dont be confused with alpha male
plot id
plot id ylog
plot gm_id
plot id_gm
plot inv_alpha_power
.endc
.end