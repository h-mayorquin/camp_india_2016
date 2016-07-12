import numpy as np
from pylab import *

signals=np.load('inputs.npy')
exc=np.load('spiketrain_exc.npy')
inh=np.load('spiketrain_inh.npy')
dt=0.1
s=np.shape(signals)
tlen=s[1]
t=np.arange(0, tlen*dt, dt)
figure()
plot(t, signals[0,:],'b')
plot(t, signals[1,:],'')
plot(t, signals[2,:],'k')
#plot(t, signals[1,:],'r')
#plot(t, signals[2,:],'k')
figure()
plot(exc[:,1]*dt/1000, exc[:,0]+1, 'r|')
figure()
plot(inh[:,1]*dt/1000, inh[:,0]+1, 'k|')
show()
