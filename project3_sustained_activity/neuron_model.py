import numpy as np
import brian2 as brian
from brian2 import *

print(10 * brian.mV)

N = 1

# Neuron Parameters
g_l = 0.05 * msiemens / cm2
Cm = 1.0 * ufarad / cm2  # Specific membrane capacitance
E_l = -60 * mV   # Resting potential
V_t = -50 * mV  # Threshold
tau_w = 600 * ms  # Adaptation time constant of w
Delta = 2.5 * mV  # Steep when approaching the threshold
S = 20000 * um2  # Membrane area

a = 0.001 * usiemens  # dynamics of adaptation
b = 0.04 * namp  # w increases by this value at each spike

f_m = g_l / Cm
# tau_ m = 1 / f_m
aux = S * Cm


I = 0.25 * namp

start_scope()
# Equations
eqs = """
dv / dt = -f_m * (v - E_l) + f_m * Delta * exp((v - V_t) / Delta) - (w / aux) + (I / aux) : volt (unless refractory)
dw / dt = (1 / tau_w) * (a * (v - E_l) - w) :  amp
"""

reset = '''
v = E_l
w += b
'''

V_avg = -55 * mV
w_avg = a * (V_avg - E_l)


# Define neuron
G = brian.NeuronGroup(N, eqs, threshold='v > V_t', reset=reset, refractory=2.5*ms, method='euler')

# State monitor
M = brian.StateMonitor(G, ['v', 'w'], record=0)

# Run this
if True:
    brian.run(500 * ms)

    subplot(211)
    brian.plot(M.t/ms, (M.v[0] / mV),label='voltage')
    brian.xlabel('Time (ms)')
    brian.ylabel('v')
    ylim([-65, -45])

    subplot(212)
    brian.plot(M.t/ms, (M.w[0]),label='w')
    brian.axhline(w_avg / amp, label='V = -55 mV', color='black')
    brian.xlabel('Time (ms)')
    brian.ylabel('w')

    legend()
    brian.show()
