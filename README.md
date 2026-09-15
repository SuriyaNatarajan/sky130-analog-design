# Analog LeetCode Lab

## ⚠️ CRITICAL RULE: How to Launch Xschem ⚠️

Because the SkyWater 130nm PDK configuration file (\xschemrc\) is located in the **root** of this repository, you must **always** launch Xschem from the root directory. 

If you \cd\ into a subfolder (like \phase0_device_physics\) and run \xschem\, the tool will not find the \xschemrc\ file, and the component libraries will completely fail to load.

### The Correct Workflow:
Always keep your terminal in the root directory (\~/analog_lab\). To create or open a schematic in a subfolder, pass the relative path directly to the command:

\\ash
# 1. Ensure you are in the root directory
cd ~/analog_lab

# 2. Launch Xschem while pointing it to the subfolder
xschem phase0_device_physics/prob01_ekv.sch
\
This ensures Xschem reads the root configuration file to load the Sky130 PDK, while keeping your actual \.sch\ files cleanly organized in their respective phase folders.
