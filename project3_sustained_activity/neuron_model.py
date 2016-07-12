import numpy as np
from brian2 import *
import seaborn as sns
sns.set(font_scale=2.0)

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
a = 0.04 * usiemens  # dynamics of adaptation
b = 0.04 * namp  # w increases by this value at each spike
b = 0.005 * namp  # w increases by this value at each spike
b = 0 * namp  # w increases by this value at each spike

f_m = g_l / Cm
# tau_ m = 1 / f_m
aux = S * Cm


I_0 = 0.25 * namp
I_0 = -0.25 * namp

# Let's create the pulse
dt_array = 0.1
values = np.arange(0, 1000, dt_array)
values[values < 200] = 0
values[values > 600] = 0
values[(200 <= values) * (values <= 600)] = 1

I = TimedArray(values * I_0, dt=0.1*ms)

start_scope()
# Equations
eqs = """
dv / dt = -f_m * (v - E_l) + f_m * Delta * exp((v - V_t) / Delta) - (w / aux) + (I(t) / aux) : volt (unless refractory)
dw / dt = (1 / tau_w) * (a * (v - E_l) - w) :  amp
"""

reset = '''
v = E_l
w += b
'''

V_avg = -55 * mV
w_avg = a * (V_avg - E_l) / aux


# Define neuron
G = NeuronGroup(N, eqs, threshold='v > V_t', reset=reset, refractory=2.5*ms, method='euler')

# State monitor
M = StateMonitor(G, ['v', 'w'], record=0)

# Run this

# Run the model
run(1000 * ms)

# Plot here
fig = plt.figure(figsize=(16, 12))
data = 'Experiment for (a = ' + str(a) + ', b = ' + str(b) + ' )'
fig.suptitle(data)

ax1 = fig.add_subplot(211)
ax1.plot(M.t/ms, (M.v[0] / mV),label='voltage')

ax1.set_ylabel('v')
ax1.set_ylim([-80, -45])

ax1.legend()

ax2 = fig.add_subplot(212, sharex=ax1)
w_sta = a * (M.v[0] - E_l) / aux
ax2.plot(M.t/ms, (M.w[0] / aux), label='w')
ax2.plot(M.t/ms, w_sta, label='w*')
ax2.axhline(np.array(w_avg), label='w*(-55 mV)', color='black')

ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('w')

ax2.legend()

plt.setp(ax1.get_xticklabels(), visible=False)

plt.show()
