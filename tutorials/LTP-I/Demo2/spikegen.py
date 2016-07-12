from numpy import *
import numpy as np

def CreateSpikeTrain( nn, ngr, t, dt, signal):

    '''
    Create spike trains for 'nn' Neurons in 'ngr' groups.
    t: Time array (sec)
    dt (ms)
    signal: Matrix with 'ngr' signals - one for each group.
    '''
    ns = 0	# No. of spikes
    spiketrain = []
    refr_left = np.zeros(nn)
    refr_period = 5 # ms
    tlen = len(t)
    sizeofgrp = int(nn/ngr)
    for tm in range(tlen):
    	if mod(tm,1000)==0:
    	   print tm*100/tlen ,'% complete for spiketrain'
        for cell in range(nn):
	    grp = int(cell/sizeofgrp)
            if (refr_left[cell] <= 0 and np.random.rand() < signal[grp, tm]) :
                spiketrain.append([cell,t[tm]])	#Cell spikes : cell no., spiketime saved
                refr_left[cell] = refr_period	#Start refractory period
                ns += 1 
            refr_left[cell] +=  (-dt)
            
    print ns
    print np.shape(spiketrain)
    return spiketrain
        
		
