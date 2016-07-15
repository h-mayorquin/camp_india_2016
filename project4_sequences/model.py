from brian2 import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Parameters
As = 100 * um2
Cm = 1 * ufarad / cm2
Ad = 50000 * um2

g_ls = 0.05 * msiemens / cm2  # Leak conductance for the soma
E_r = -85 * mV  # reversal potential for the leak current
g_na = 1 * msiemens / cm2  # Sodium conductance
E_na = 55 * mV   # reversal potential
g_k = 2 * msiemens / cm2  # potassium conductance
E_k = -90 * mV  # reversal potential
g_kht = 300 * msiemens / cm2   # high threnshold potassium conductance
E_kht = E_k
g_klt = 25 * msiemens / cm2   # low threshold potassium conductance
K_klt = E_k
R_c = 250 * Mohm   # Resistance of the connection between somaa and dendrite

g_ld = 0.1 * msiemens / cm2  # leak condutance fo the dendrite
E_ld = E_r  # reversal potential for the leak ucurretn
g_ca = 200 * msiemens / cm2  # leak conductance for calcium
E_ca = 120 * mV  # reversal potential of calcium
g_cak = 100 * msiemens / cm2  # calcium dependent potassium current conductance
E_cak = E_k  # calcium reversal potential

tau_ca = 100 * ms  # decay time constant for calcium dynamics
tau_syn = 5 * ms  # synaptic time constant


t_w = 1 * ms  # time constant for the gating variable w
t_l = 10 * ms  # time constant of the gating variable l

tau_m = 1.0 * ms

I_ext = 0.25 * namp  # External current
# (g_ls / Cm) * (E_r - v_s)
#ndv_s/dt =  (g_na/ Cm) * (1 ** 3) * (E_na - v_s): volt
# dv_d/dt = (g_ld / Cm) * (E_ld - v_d): volt

v_s = E_na
#
 #
eqs = """
dm_s/dt = (1 - m_s) * (-0.5 / tau_m) * ((v_s /mV) + 22.0) / (exp(-((v_s /mV) + 22) / 10) - 1) -
m_s * (20 / tau_m) * exp(-((v_s/mV) + 47)/18): 1
"""

# Create the population
# G = NeuronGroup(N, eqs, threshold='v > V_t', reset=reset, refractory=2.5*ms, method='euler')
G = NeuronGroup(1, eqs, method='euler')
G.m_s[0] = 0.5

# Monitor
# M = StateMonitor(G, ['v_s', 'v_d', 'm_s'], record=0)
M = StateMonitor(G, True, record=0)

run(100 * ms)
if False:
    fig = plt.figure(figsize=(16, 12))
    ax1 = fig.add_subplot(121)
    ax1.plot(M.t / ms, M.v_s[0]/mV)
    ax1.hold(True)
    ax1.plot(M.t / ms, M.v_d[0]/mV)

    ax2 = fig.add_subplot(122)
    ax2.plot(M.t/ms, M.m_s[0])

    fig.show()

plt.plot(M.t / ms, M.m_s[0])
plt.show()