import numpy as np
from inputsignals import *
from pylab import *
from spikegen import *

simtime = 10 #(s)
dt = 0.1 #(ms)
t=np.arange(0,simtime,dt/1000)
ngr=8
print 'Creating input signals for', ngr, 'groups'
signals=GenerateInputSignalForGroup(ngr,t,dt)
Ne = 800
Ni=200

print 'Creating spiketrains for', Ne, 'excitatory synapse from', ngr, 'input signals'
exc=CreateSpikeTrain( Ne, ngr, t, dt, signals)
print 'Creating spiketrains for', Ni, 'inhibitory synapse from', ngr, 'input signals'
inh=CreateSpikeTrain( Ni, ngr, t, dt, signals)

f = open('inputs.npy','w')
save(f,signals)
f.close()

f2 = open('spiketrain_exc.npy','w')
save(f2,exc)
f2.close()

f3 = open('spiketrain_inh.npy','w')
save(f3,inh)
f3.close()


