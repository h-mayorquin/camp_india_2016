import numpy as np
from brian2 import *
import seaborn as sns
sns.set(font_scale=2.0)

N = 50

# Neuron Parameters
g_l = 0.05 * msiemens / cm2
Cm = 1.0 * ufarad / cm2  # Specific membrane capacitance
E_l = -60 * mV   # Resting potential
V_t = -50 * mV  # Threshold
tau_w = 600 * ms  # Adaptation time constant of w
Delta = 2.5 * mV  # Steep when approaching the threshold
S = 20000 * um2  # Membrane area

f_m = g_l / Cm
# tau_ m = 1 / f_m
aux = S * Cm

# Syanpses parameters
tau_e = 5 * ms
tau_i = 10 * ms

E_inh = -80 * mV
E_exc = 0 * mV

ge_max = 6 * nsiemens
gi_max = 67 * nsiemens

I_0 = (0.25 * namp) / (aux)

# Let's build the networks

a_tc = 0.04 * usiemens
b_tc = 0.0 * namp


eqs_tc = """
dv / dt = -(g_l / Cm) * (v - E_l) + (g_l / Cm) * Delta * exp((v - V_t) / Delta) - (w / aux) - (ge /aux) * (v - E_exc) - (gi / aux) *(v - E_inh): volt (unless refractory)
dw / dt = (1 / tau_w) * (a_tc * (v - E_l) - w) :  amp
dge/dt = -ge/tau_e : siemens
dgi/dt = -gi/tau_i : siemens
"""

reset_tc = '''
v = E_l
w += b_tc
'''

a_re = 0.08 * usiemens
b_re = 0.03 * namp


eqs_re = """
dv / dt = -(g_l / Cm) * (v - E_l) + (g_l / Cm) * Delta * exp((v - V_t) / Delta) - (w / aux) - (ge /aux) * (v - E_exc) - (gi / aux) *(v - E_inh): volt (unless refractory)
dw / dt = (1 / tau_w) * (a_re * (v - E_l) - w) :  amp
dge/dt = -ge/tau_e : siemens
dgi/dt = -gi/tau_i : siemens
"""

reset_re = '''
v = E_l
w += b_re
'''
TC = NeuronGroup(N, eqs_tc, threshold='v > V_t', reset=reset_tc, refractory=2.5*ms, method='euler')
RE = NeuronGroup(N, eqs_re, threshold='v > V_t', reset=reset_re, refractory=2.5*ms, method='euler')

M_tc = StateMonitor(TC, ['v', 'w', 'ge'], record=0)
spikes_tc = SpikeMonitor(TC)

M_re = StateMonitor(RE, ['v', 'w', 'ge'], record=0)
spikes_re = SpikeMonitor(RE)

# Initialization input
frequency = 400 * Hz
dt_array = 0.1
t_stimuli = 50
values = np.arange(0, 1000, dt_array)
values[values <= t_stimuli] = 1
values[values > t_stimuli] = 0

input_rates = TimedArray(values * frequency, dt=0.1*ms)
init_input = PoissonGroup(N=1, rates='input_rates(t)')

if True:
    S_init_tc = Synapses(init_input, TC, on_pre='ge += ge_max')
    S_init_tc.connect(p=0.1)
    S_init_re = Synapses(init_input, RE, on_pre='ge += ge_max')
    S_init_re.connect(p=0.1)

# Connect the populations
if True:
    S_exc = Synapses(TC, RE, on_pre='ge += ge_max')
    S_exc.connect(p=0.2)

    S_inh = Synapses(RE, TC, on_pre='gi += gi_max')
    S_inh.connect(p=0.8)

    S_rec = Synapses(RE, RE, on_pre='gi += gi_max')
    S_inh.connect(p=0.8)


run(1000 * ms)

if True:
    # run(1000 * ms)

    # Plot here
    fig = plt.figure(figsize=(16, 12))

    ax1 = fig.add_subplot(211)

    ax1.plot(spikes_re.t / ms, spikes_re.i, '*')

    # ax1.set_ylim([-80, -45])
    ax1.set_xlim([0, 1000])

    ax2 = fig.add_subplot(212, sharex=ax1)

    ax2.plot(spikes_tc.t / ms, spikes_tc.i, '*')

    ax2.set_xlabel('Time (ms)')
    ax2.set_xlim([0, 1000])

    plt.setp(ax1.get_xticklabels(), visible=False)

    plt.show()

if True:

    # Plot here
    fig = plt.figure(figsize=(16, 12))

    ax1 = fig.add_subplot(221)
    ax1.plot(M_tc.t / ms, (M_tc.ge[0]))

    ax2 = fig.add_subplot(222)
    ax2.plot(M_re.t / ms, (M_re.ge[0]))

    ax3 = fig.add_subplot(223)
    ax3.plot(M_tc.t / ms, M_tc.v[0] / mV)

    ax4 = fig.add_subplot(224)
    ax4.plot(M_re.t / ms, M_re.v[0] / mV)

    plt.show()


# Synapes equation
