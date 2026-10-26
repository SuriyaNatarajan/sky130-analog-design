# A1: NMOS common-source amp, hand calc

## Spec
| Device | Load | VDD | Id | CL | fu | \|Av\| |
|---|---|---|---|---|---|---|
| nfet_01v8, tt, 27 °C | ideal current source (no PMOS yet) | 1.8 V | 10 µA | 1 pF | ≥ 20 MHz | ≥ 40 V/V |

## Assumptions
- Cpar ≪ CL, so fu ≈ gm/(2*pi*CL)
- Held constant: VDS = 0.9 V, VSB = 0 V, corner TT, T = 27 °C

## Steps
1. gm ≥ 2*pi*fu*CL = 126 µS
2. gm/Id ≥ 126uS / 10uA = 12.6 /V, because of fu requirements
3. L (at gm/Id = 12.6 /V): L = 0.15 → gain 20 · L = 0.5 → gain 100 → chose L = 0.5 µm, because gain will be greater than 40
4. W = ID / (ID/W) = 10uA/(6uA/um) =  1.66 µm

## Result
gm/Id = 12.6 /V · L = 0.5 µm · W = 1.66 µm

## Open checks
- run simulation to check device capacitor impacts ugb. (making sure that assumption 1 works fairly well)
- check with spice.
