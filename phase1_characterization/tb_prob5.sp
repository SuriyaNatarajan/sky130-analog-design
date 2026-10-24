* Verification of Problem 5
.lib "/home/suriya/pdk/volare/sky130/versions/c6d73a35f524070e85faff4a6a9eef49553ebc2b/sky130A/libs.tech/ngspice/sky130.lib.spice" tt

Vdd vdd 0 1.8
Iload vdd vout 1u
CL vout 0 1p

* Device Under Test: W = 26.67, L = 1.0
XM1 vout gate 0 0 sky130_fd_pr__nfet_01v8 L=1.0 W=26.67

* DC Feedback: Force Vout to 0.6V (matches LUT vds=0.6)
* Gain of 1e6 ensures Vout is exactly 0.6V
E_FB ctrl 0 0.6 vout 1e6

* AC breaking loop
* Large L passes DC, blocks AC
L_break ctrl gate 1GH
* Large C passes AC, blocks DC
C_break ac_src gate 1GF
Vac ac_src 0 0 AC 1

.control
op
* Print DC parameters
let gm = @m.xm1.msky130_fd_pr__nfet_01v8[gm]
let id = @m.xm1.msky130_fd_pr__nfet_01v8[id]
let gds = @m.xm1.msky130_fd_pr__nfet_01v8[gds]
let gm_id = gm / id
let gain = gm / gds

echo "======================================"
echo "DC OP RESULTS:"
print gm_id
print gain
print v(gate)
print v(vout)
echo "======================================"

ac dec 100 100 100Meg
let vout_db = vdb(vout)
* Find GBW where gain drops to 0 dB
meas ac gbw WHEN vout_db=0

echo "======================================"
echo "AC RESULTS:"
print gbw
echo "======================================"

.endc
.end
