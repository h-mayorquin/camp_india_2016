### Code written for STDP tutorial @ CAMP 2016
### Adapted from Song et al 2000 (Competitive Hebbian Learning through spike-timing-dependent synaptic plasticity
### With independent Poisson inputs (relevant figures : Fig 2a,b,c)

### Author: Harsha Gurnani
### Date: June 15, 2016
#######################################


from brian2 import *
from time import time
#set_device('cpp_standalone')

#################
def newrun( fe = 15, fi = 15, Weakratio=1.05, simtime = 100*second, delta = 0.1*ms):

    if fe<30:
        simtime=150*second
    defaultclock.dt = delta

    taum = 20*ms
    Vrest = -70*mV
    Erev = 0*mV         	#Excitatory synapse - reversal potential
    Irev = -70*mV       	#Inhibitory synapse - reversal potential
    taue = 5*ms
    taui = 5*ms

    gmax = 0.015        	#Max excitatory conductance
    ginh = 0.05          	#Inhibitory conductance

    Vt = -54*mV         	# Spike threshold
    Vr = -60*mV         	# Reset potential


    #### How does no. of synapses/ ratio influence firing rates?
    Ne = 1000           	#No. of excitatory synapses
    Ni = 200             	#No. of ihibitory synapses

    # How does final distribution of weights depend on presynaptic firing rates? Why???
    FRe = fe*Hz         #Firing rate for excitatory input
    FRi = fi*Hz         #FR for inhibitory input

    ### Neuron model
    eqs = Equations('''

        dV/dt = ( (Vrest - V) + ge*(Erev - V) + gi*(Irev - V) )/taum :volt
        dge/dt = -ge/taue :1        #Current from exc synapse
        dgi/dt = -gi/taui :1        #Current from inh synapse
    ''')

    NRN = NeuronGroup(1, model=eqs, threshold = 'V>Vt', reset = 'V=Vr', method='euler')

    ## STDP parameters for excitatory synapses
    taupre = 20*ms
    taupost = 20*ms
    #Weakratio = 1.05        ##Apost*taupost/(Apre/taupre)
                            ##:Weakening:Strengthening ratio (slightly greater than 1 for stabilising network)
    Apre = 0.005            # %Strengthening with pre-post pair
    Apost = Apre*(taupre/taupost)*Weakratio

    ### Excitatory input and synapse model
    InpE = PoissonGroup(Ne, rates = FRe)

    syneqs = '''
        gsyn    :1
        dx/dt = -x/taupre :1	(event-driven)
        dy/dt = -y/taupost :1	(event-driven)
        '''

    preeqs = '''
        ge_post += gsyn
        x += Apre
        gsyn += -y*gmax
        gsyn = clip(gsyn, 0, gmax)
        '''

    posteqs = '''
        y += Apost
        gsyn += x*gmax
        gsyn = clip(gsyn, 0, gmax)
        '''

    S_exc = Synapses(InpE, NRN, model=syneqs, on_pre=preeqs, on_post=posteqs )
    S_exc.connect()
    S_exc.gsyn[:] = gmax*rand(Ne)    #Initialise uniformly between 0 and gmax

    #print 'Created', Ne, 'excitatory synapses with mean weight = ', float(int(mean(S_exc.gsyn[:]*10000)))/10

    ### Inhibitory synapses
    
    InpI = PoissonGroup(Ni, rates = FRi)
    S_inh = Synapses(InpI, NRN, model = ' ', on_pre = '''gi_post += ginh''')
    S_inh.connect()

    #print 'Created', Ni, 'inhibitory synapses ...'
    
    ## Monitors
    SM = SpikeMonitor(NRN)
    VMon = StateMonitor( NRN, 'V', record = 0 )
    FR = PopulationRateMonitor(NRN)

    ## Runtime
    print '\n Running for', simtime, 'at dt = ', delta, 'with excitatory inputs at', fe, 'Hz'
    run( simtime, report = 'text', report_period = 50*second)
    #device.build(directory='output', compile=True, run=True, debug=False)

    ## Plotting
    figure()
    suptitle('Excitatory firing rate = %d Hz' %(fe))
    
    ### Histogram of sinal synaptic weights
    subplot(311)
    hist(S_exc.gsyn[:] /gmax, 20)
    ylabel('No. of synapses')
    xlabel('Normalised synaptic weight')

    ### Initial membrane potential trace
    subplot(323)
    plot(VMon.t[0:3000] /ms, VMon.V[0,0:3000] /mV)
    ylim([-80,-40])
    ylabel('Membrane potential (mV)')
    legend('Initial V')

    ### Final membrane potential trace
    subplot(324)
    plot(VMon.t[-3000:-1] /ms, VMon.V[0,-3000:-1] /mV)
    ylim([-80,-40])
    legend('Final V')

    ### Evolution of Firing rate in time
    subplot(313)
    plot(FR.t /second, FR.smooth_rate(window='gaussian', width=50*ms)/Hz)
    ylabel('Firing rate (Hz)')
    tight_layout()

    poprate=FR.smooth_rate(window='gaussian', width=100*ms)
    fin_poprate = mean( poprate[-1000:-500] )
    print fin_poprate
    
    spt = SM.t[:]
    L = len(spt)
    ##Get last 500 spikes. Fixed no. of spikes instead of duration.
    if L > 500:
        spt = spt[-500:L]
        isi = spt[1:500] - spt[0:499]
        cv = sqrt(var(isi))/mean(isi)
    
    else :
        cv = NaN
        
    print ' \n'
    return fin_poprate, cv


################

fe_rates = [15,20,25,30,35,40,45]
poprates = []
cv = []

for fe in fe_rates:
    ret1, ret2 = newrun(fe)
    poprates.append(ret1)
    cv.append(ret2)

print poprates

fig = figure()
A = fig.add_subplot(111)
A.plot(fe_rates, poprates, marker ='o', color = 'b')
A.set_xlabel('Excitatory input (Hz)')
A.set_ylabel('Firing rate of postsynaptic neuron (Hz)', color='b')
for tl in A.get_yticklabels():
    tl.set_color('b')

## Different y-scales for the two plots with same x-axis
B = A.twinx()
B.plot(fe_rates, cv, marker='*', color='g')
B.set_ylabel('CV', color='g')
for tl in B.get_yticklabels():
    tl.set_color('g')


show()
