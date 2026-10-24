# sky130 Analog Design

Analog building blocks designed by hand on the open-source SkyWater 130 nm PDK.
Each block follows the same loop: **spec → hand calculation → prediction → simulation → corners → write-up**.

## Arcs

| Arc | Block | Status |
|---|---|---|
| A0 | Device characterization (nfet/pfet gm/Id) | 🔄 in progress |
| A1 | Common-source amplifier from a spec | ⬜ |
| A2 | Current mirrors + bias with startup | ⬜ |
| A3 | Differential pair → 5-transistor OTA | ⬜ |
| A4 | Two-stage Miller OTA (corners, Monte Carlo, stability) | ⬜ |
| A5 | Noise analysis | ⬜ |
| A6 | Bandgap reference | ⬜ |
| A7 | LDO regulator | ⬜ |
| A8 | StrongARM comparator | ⬜ |
| A9 | SAR ADC | ⬜ |
| A10 | PLL | ⬜ |
| L | Layout track (DRC/LVS/PEX) | ⬜ |

Each finished arc has its own folder (`a0_…`, `a1_…`) with a README covering design decisions and results.

## Repository layout

```
a0_device_char/   current arc
lut/              gm/Id lookup tables: techsweep schematics, txt→mat notebooks, LUT examples
                  (the .mat files are generated, not committed)
scripts/          reusable helpers
xschemrc          sky130 xschem configuration (launch xschem from this folder)
requirements.txt  Python packages
```

## Setup

| Tool | Version |
|---|---|
| sky130 PDK (volare) | `c6d73a35f524070e85faff4a6a9eef49553ebc2b` |
| ngspice | 45.2 |
| xschem | 3.4.8RC |
| Python | 3.14, packages in `requirements.txt` |

```bash
export PDK_ROOT=$HOME/pdk PDK=sky130A
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Netlists include the models through the stable symlink path, never the volare version hash:
```spice
.lib ~/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
```

Launch xschem from the repository root so it picks up `xschemrc`:
```bash
xschem a0_device_char/prob01_ekv.sch
```
