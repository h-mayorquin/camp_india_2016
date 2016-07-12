### Code written for STDP tutorial @ CAMP 2016
### Adapted from Song et al 2000 (Competitive Hebbian Learning through spike-timing-dependent synaptic plasticity)
### With independent Poisson inputs (relevant figures : Fig 2)

### Author: Harsha Gurnani
### Date: June 15, 2016
#######################################


from brian2 import *
from time import time
set_device('cpp_standalone')


#### Simulation parameters ####
simtime = 150 *second
delta = 0.1*ms

defaultclock.dt = delta

########################
#### Model Parameters
########################


### Neuron and synapses:

taum = 20*ms		# Membrane time constant
Vrest = -70*mV		# Resting membrane potential
Erev = 0*mV         	# Excitatory synapse - reversal potential
Irev = -70*mV       	# Inhibitory synapse - reversal potential
taue = 5*ms		# Excitatory time constants
taui = 5*ms		# Inhibitory time constants

gmax = 0.015        	#Max excitatory conductance //in unnits of leak conductance
ginh = 0.05          	#Inhibitory conductance

Vt = -54*mV         	# Spike threshold
Vr = -60*mV         	# Reset potential


#### How does no. of synapses/ ratio influence firing rates?
Ne = 1000           	#No. of excitatory synapses
Ni = 200             	#No. of ihibitory synapses

# How does final distribution of weights depend on presynaptic firing rates? Why???
FRe = 15*Hz         	#Firing rate (FR) for excitatory input
FRi = 10*Hz         	#FR for inhibitory input

### Neuron model
eqs = Equations('''

    dV/dt = ( (Vrest - V) + ge*(Erev - V) + gi*(Irev - V) )/taum :volt
    dge/dt = -ge/taue :1        #Conductance of exc synapse
    dgi/dt = -gi/taui :1        #Conductance of inh synapse
''')

NRN = NeuronGroup(1, model=eqs, threshold = 'V>Vt', reset = 'V=Vr', method='euler')



########################
#### Synapses and STDP
########################

## STDP parameters for excitatory synapses
taupre = 20*ms		# Time constant of potentiation for pre-post pairing
taupost = 20*ms		# Time constant of depression for post-pre pairing
Weakratio = 1.05        # Apost*taupost/(Apre*taupre)
                        # Depression:Potentiation ratio (slightly greater than 1 for stabilising network)
Apre = 0.005            # %Strengthening with pre-post pair
Apost = Apre*(taupre/taupost)*Weakratio

### Excitatory Synapse Model:
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

### Poisson Input at Excitatory synapses, at firing rate FRe
InpE = PoissonGroup(Ne, rates = FRe)

S_exc = Synapses(InpE, NRN, model=syneqs, on_pre=preeqs, on_post=posteqs )
S_exc.connect()				# Connect all
S_exc.gsyn[:] = gmax*rand(Ne)    	# Initialise uniformly between 0 and gmax

### Inhibitory synapses:
InpI = PoissonGroup(Ni, rates = FRi)

S_inh = Synapses(InpI, NRN, model = ' ', on_pre = '''gi_post += ginh''')	# Constant inhibitory conductance = ginh
S_inh.connect()

################
### Monitors
################

VMon = StateMonitor( NRN, 'V', record = 0 )			## Membrane potential
FR = PopulationRateMonitor(NRN)					## Firing rate of NRN
Weights = StateMonitor( S_exc, 'gsyn', record = [0,Ne-1])	## Two example synaptic weights

run( simtime, report='text')

figure()
### Histogram of sinal synaptic weights
subplot(211)
hist(S_exc.gsyn[:] /gmax, 20)
ylabel('No. of synapses')
xlabel('Normalised synaptic weight')

### Initial membrane potential trace
subplot(223)
plot(VMon.t[0:3000] /ms, VMon.V[0,0:3000] /mV)
ylim([-80,-40])
ylabel('Membrane potential (mV)')
legend('Initial V')

### Final membrane potential trace
subplot(224)
plot(VMon.t[-3000:-1] /ms, VMon.V[0,-3000:-1] /mV)
ylim([-80,-40])
legend('Final V')

figure()
### Evolution of Firing rate in time
subplot(211)
plot(FR.t /second, FR.smooth_rate(window='gaussian', width=100*ms)/Hz)
ylabel('Firing rate (Hz)')

### Evolution of two example synaptic weights
subplot(212)
plot(Weights.t /second, Weights.gsyn[0,:], 'b', label='Synapse 1')
plot(Weights.t /second, Weights.gsyn[1,:], 'g', label='Synapse N')
xlabel('Time (second)')
ylabel('Synaptic weight')

tight_layout()
show()
