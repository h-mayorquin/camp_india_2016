from numpy import *
from scipy import *

def GenerateSpikeTimes(rate_function, t, max_t, delta, maxFR=20, thresh=0.7):    
    
    '''
    Generate spiketimes for time t, with delta t=delta, t/delta = max_t
    rate_function gives relative instantaneous firing probability or voltage 
    rate_function averaged over 2 time bins such that max instantaneous FR is
    maxFR (HZ). 
    Spikes are generated as an inhomogenous Poisson iff: 
        avg_rate(t)/max(avg_rate)>threshold
    '''
    ## Normalized rate: Peak = 
    avg_rate = rate_function/max(rate_function)

    ## Firing rate: avg of FR(t) and FR(t+dt):  
    ## (With maximum instantaneous rate ~ maxFR (Hz)
    avg_rate[0:max_t-1] = maxFR * (rate_function[1:max_t] + rate_function[0:max_t-1])/2.0
    #### Applying threshold (not in original paper)
    probthresh = thresh*max(avg_rate)
    avg_prob = multiply((1 - exp(-avg_rate * delta)), (avg_rate >= probthresh) )
    rand_throws = random.uniform(size=max_t)
    a=arange(0,max_t)

    spiketimes = a[avg_prob >= rand_throws]
    return spiketimes

