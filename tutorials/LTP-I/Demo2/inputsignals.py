from numpy import *
from numpy import random as rm
import numpy as np

def GenerateInputSignalForGroup( nos, t, dt, peakf = 500, tau_f = 50, baseline=5):

	'''
	Generate the common input signal for neurons in a group. 
	Generate one for each group, hence nos in total.
	nos: No. of signals/groups
	t: Time array (sec)
	dt: Delta t (ms)
	tau_f = Time constant of filter (ms)
	peakf = Max instantaneous firing rate (Hz)
	baseline : Baseline firing rate (in Hz)
	'''
	tlen = len(t)
	### Create white noise : Uniformly sampled between +/- 0.5
	WNoise = rm.rand(nos, tlen)-0.5
	
	### Filtered noise
	FNoise = WNoise
	nfilter = exp(-dt/tau_f)
	for tm in range(1,tlen):
		FNoise[:,tm]  = FNoise[:,tm] - (FNoise[:,tm] - FNoise[:,tm-1])*nfilter
	### Rectification
	FNoise[FNoise<0] = 0
	### Normalise it to maximum instantaneous rate = peakf*HZ
	for jj in range(0,nos):
		mp = max(FNoise[jj,-tlen/2:])
		FNoise[jj,:]=FNoise[jj,:]*peakf*dt*0.001/mp
		
		
	### Make signal sparse: Remove some activity bumps
	del_next_bump = np.zeros([nos,1])	# Should I delete the next activity bump?
	last_toggle = np.zeros([nos,1])
	
	for tm in range(0,tlen-1):
		for grp in range(nos):
			if ( FNoise[grp,tm]==0 and del_next_bump[grp]==0 and (tm-last_toggle[grp]) > int(1/dt) ):
				del_next_bump[grp] = 1
				last_toggle[grp] = tm	## Start 1 ms refractory for deleting two nearby activity bumps
				
			if ( del_next_bump[grp] == 1):
				FNoise[grp,tm] = 0
				
				#Have you reached end of activity bump? Then stop deleting
				if (FNoise[grp,tm+1]==0 and (tm-last_toggle[grp] > int(0.5/dt)) ):
					del_next_bump[grp] = 0
					
	## Add baseline activity (5 Hz by default)
	FNoise = FNoise + baseline*dt/1000
					
	return FNoise
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
