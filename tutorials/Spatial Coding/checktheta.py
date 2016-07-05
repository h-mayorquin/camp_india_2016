from numpy import *

def CheckThetaFreq(peaks, all_freq):

    idx=0
    if len(peaks)>=0:
        ThetaFreq = all_freq[peaks[idx]]
        while ( ThetaFreq < 4 & idx < len(peaks)-1 ):
            idx+=1
            ThetaFreq = all_freq[peaks[idx]]
    else:
        ThetaFreq = 0
    
    return ThetaFreq
