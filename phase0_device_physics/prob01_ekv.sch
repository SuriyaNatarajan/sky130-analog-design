v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 40 30 40 90 {lab=vss}
N 40 0 110 0 {lab=vss}
N 110 0 110 60 {lab=vss}
N 40 60 110 60 {lab=vss}
N -80 0 0 0 {lab=Vg}
N 40 -70 40 -30 {lab=Vd}
N -200 10 -200 40 {lab=vss}
N -140 10 -140 40 {lab=vss}
N -200 -80 -200 -50 {lab=Vg}
N -140 -80 -140 -50 {lab=Vd}
N -80 -80 -40 -100 {lab=vss}
N -40 -40 -40 -30 {lab=0}
C {sky130_fd_pr/nfet_01v8.sym} 20 0 0 0 {name=M1
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_wire.sym} 40 80 0 0 {name=p1 sig_type=std_logic lab=vss}
C {lab_wire.sym} -80 0 0 0 {name=p2 sig_type=std_logic lab=Vg}
C {lab_wire.sym} 40 -70 0 0 {name=p3 sig_type=std_logic lab=Vd}
C {vsource.sym} -200 -20 0 0 {name=VGS value=0 savecurrent=false}
C {vsource.sym} -140 -20 0 0 {name=VDS value=1.8 savecurrent=false}
C {lab_pin.sym} -200 40 0 0 {name=p4 sig_type=std_logic lab=vss}
C {lab_pin.sym} -140 40 0 0 {name=p5 sig_type=std_logic lab=vss}
C {lab_pin.sym} -200 -80 0 0 {name=p6 sig_type=std_logic lab=Vg}
C {lab_pin.sym} -140 -80 0 0 {name=p7 sig_type=std_logic lab=Vd}
C {vsource.sym} -40 -70 0 0 {name=VSS value=0 savecurrent=false}
C {lab_pin.sym} -80 -80 0 0 {name=p9 sig_type=std_logic lab=vss}
C {gnd.sym} -40 -30 0 0 {name=l1 lab=0}
C {sky130_fd_pr/corner.sym} -350 100 0 0 {name=CORNER only_toplevel=false corner=tt}
C {code_shown.sym} -200 120 0 0 {name=s1 only_toplevel=false value=".controlnsave allndc VGS 0 1.8 0.01nplot -i(VDS) ylogn.endc"}
