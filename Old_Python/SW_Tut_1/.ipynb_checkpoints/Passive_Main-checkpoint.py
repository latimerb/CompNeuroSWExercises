from neuron import h
from matplotlib import pyplot
h.load_file('stdrun.hoc')

#Create the soma section and define the default parameters
soma = h.Section(name='soma')
soma.nseg = 1
soma.diam = 200
soma.L = 100
soma.cm = 1.4884e-4/6.2832e-4

#Insert the Hodgkin-Huxley channels and define the conductances
soma.insert('hh')
soma.gnabar_hh = 0
soma.gkbar_hh = 0
soma.gl_hh = 2.0e-5
soma.el_hh = -70

v_init = h.v_init= -60

#Inject current in the middle of the soma
stim = h.IClamp(0.5)
stim.delay = 100
stim.dur = 500
stim.amp = 1

tstop = h.tstop = 800   #ms

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#Record Results  
h.dt = 0.025

v0_vec = h.Vector()
t_vec = h.Vector()

v0_vec.record(soma(0.5)._ref_v)
t_vec.record(h._ref_t)

def run_simulation(gl_hh = 2.0e-5, gna_hh = 0, gk_hh = 0, cur_inj = 1):
    # Run the simulation
    soma.gl_hh = float(gl_hh)
    soma.gnabar_hh = float(gna_hh)
    soma.gkbar_hh = float(gk_hh)
    stim.amp = float(cur_inj)
    h.run()

    # Plot/Visualize Results
    pyplot.figure()
    pyplot.plot(t_vec, v0_vec,'b')
    pyplot.xlim(0, tstop)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.show()