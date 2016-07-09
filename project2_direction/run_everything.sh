#!/bin/bash
# A sample Bash script, by Ryan
echo Run everything
# Create sequences or directions
# Run neuron
nrniv init_sim.hoc
# Run analysis
python extract_voltage_traces.py
python extract_peaks.py
