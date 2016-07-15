# based on http://moose.readthedocs.io/en/latest/user/py/quickstart/index.html

import moose
import numpy as np
import matplotlib.pyplot as plt

# model objects
model = moose.Neutral('/model') # create an umbrella path for all further moose objects
soma = moose.Compartment('/model/soma') # an equipotential compartment
pulse = moose.PulseGen('/model/pulse') # a pulse generator to inject current

# recording objects
data = moose.Neutral('/data')
vmtab = moose.Table('/data/soma_Vm')

soma.Cm = 1e-9
soma.Rm = 1e7
soma.initVm = -0.07

# connect the objects
# use moose.getFieldNames('Compartment', ['srcFinfo','destFinfo','valueFinfo')
# to get source and destination slots to connect, and object attributes
m = moose.connect(pulse, 'output', soma, 'injectMsg')
# `soma.neighbors['injectMsg']` to find connections
moose.connect(vmtab, 'requestOut', soma, 'getVm')

# run the simulations
moose.reinit()
moose.start(300e-3)

# plot the simulations
t = np.linspace(0, 300e-3, len(vmtab.vector))
plt.plot(t, vmtab.vector)
plt.show()
