from brian2 import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=2.0)

# Neuron Parameters
g_l = 0.05 * msiemens / cm2
cm = 1.0 * ufarad / cm2  # Specific membrane capacitance
E_l = -60 * mV   # Resting potential
V_t = -50 * mV  # Threshold
tau_w = 600 * ms  # Adaptation time constant of w
Delta = 2.5 * mV  # Steep when approaching the threshold
S = 20000 * um2  # Membrane area

a = 0.001 * usiemens  # dynamics of adaptation
b = 0.04 * namp  # w increases by this value at each spike

# a = 0.03 * usiemens  # dynamics of adaptation

f_m = g_l / cm
# tau_ m = 1 / f_m
aux = S * cm

# Voltage and w stable values
v = np.linspace(-80, -40, 100) * mV
v_aux = np.linspace(-60, -50, 6) * mV
w_set = (v_aux - E_l) * a

# Current
I_o = 0.25
I = I_o * namp * np.ones(v.size)

fig = plt.figure(figsize=(16, 12))

data = 'Stability Analysis (a = ' + str(a) + ', b = ' + str(b) + ' )'
fig.suptitle(data)
# First plot
ax1 = fig.add_subplot(121)

for index, w in enumerate(w_set):
    y1 = -f_m * (v - E_l)
    y2 = f_m * Delta * np.exp((v - V_t) / Delta)
    y3 = - (w / aux)

    f = y1 + y2 + y3

    ax1.plot(v / mV, f, label='w*= ' + str(v_aux[index]))

ax1.legend()
ax1.set_ylim([-1, 10])
ax1.axhline(0, color='black')

ax1.set_xlabel('Voltage')
ax1.set_ylabel('f(v) = dv /dt')
ax1.set_title('No current')

ax1.annotate('$V_{re}$', xy=(E_l / mV, 0), xytext=(E_l / mV, -0.5),
             arrowprops=dict(facecolor='red', shrink=0.05))

ax1.annotate('$V_{th}$', xy=(V_t / mV, 0), xytext=(V_t / mV, -0.5),
             arrowprops=dict(facecolor='red', shrink=0.05))

# Second plot
ax2 = fig.add_subplot(122, sharey=ax1)

for index, w in enumerate(w_set):
    y1 = -f_m * (v - E_l)
    y2 = f_m * Delta * np.exp((v - V_t) / Delta)
    y3 = - (w / aux)

    f = y1 + y2 + y3 + (I / aux)
    ax2.plot(v / mV, f, label='w*= ' + str(v_aux[index]))

ax2.legend()
ax2.set_ylim([-1, 10])
ax2.axhline(0, color='black')

ax2.set_xlabel('Voltage')
# ax2.set_ylabel('f(v) = dv /dt')
ax2.set_title('Current I = 0.25 nAmp')

ax2.annotate('$V_{re}$', xy=(E_l / mV, 0), xytext=(E_l / mV, -0.5),
             arrowprops=dict(facecolor='red', shrink=0.05))

ax2.annotate('$V_{th}$', xy=(V_t / mV, 0), xytext=(V_t / mV, -0.5),
             arrowprops=dict(facecolor='red', shrink=0.05))

# Remove the axis
plt.setp(ax2.get_yticklabels(), visible=False)

plt.show()
