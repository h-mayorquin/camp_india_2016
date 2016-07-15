import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


v = np.arange(-100, 100, 0.1)


def alpha_m(v):
    tau_m = 1
    return (-0.5 / tau_m) * (v + 22.0) / (np.exp(-(v + 22) / 10) - 1)


def beta_m(v):
    tau_m = 1
    return (20 / tau_m) * np.exp(-((v) + 47) / 18)

def fix_point_m(v):
    return alpha_m(v) / (alpha_m(v) + beta_m(v))


# Gating variables for m
if True:
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.plot(v, alpha_m(v), label='alpha_m')
    ax.hold(True)
    ax.plot(v, beta_m(v), label='beta_m')
    ax.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(v, fix_point_m(v), label='fix point')
    ax2.legend()

    plt.show()

eqs = """
dm_s/dt = (1 - m_s)
"""
