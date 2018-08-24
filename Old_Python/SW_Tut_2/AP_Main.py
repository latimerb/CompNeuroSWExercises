from neuron import h
from matplotlib import pyplot
import AP_Template
h.load_file("stdgui.hoc")

# Create Vector to Record Plots
v_vec = h.Vector()
t_vec = h.Vector()
mna_vec = h.Vector()
hna_vec = h.Vector()
nk_vec = h.Vector()
gna_vec = h.Vector()
gk_vec = h.Vector()
ina_vec = h.Vector()
ik_vec = h.Vector()
il_vec = h.Vector()
ccl_i_vec = h.Vector()
vcl_i_vec = h.Vector()

## Set Simulation Parameters
h.v_init = -60
tstop = h.tstop = 100
h.dt = 0.001
h.steps_per_ms = 1000

## Create Cell
axon = AP_Template.SquidCell()

## Insert Current Clamp into Axon Soma
ccl = h.IClamp(axon.soma(0.5))
vcl = h.VVClamp(axon.soma(0.5))

# Define functions
def clear_IClamp():
    #print 'Clearing IClamp'
    ccl.delay = 0     # in ms
    ccl.dur = 0       # in ms
    ccl.amp = 0       # in nA

def update_IClamp(delay = 5, dur = 40, amp = 100):
    #print 'Update IClamp'
    clear_VClamp()
    ccl.delay = float(delay)   # in ms
    ccl.dur = float(dur)       # in ms
    ccl.amp = float(amp)       # in nA

def clear_VClamp():
    #print 'Clearing VClamp'
    for i in range(0,4):
        vcl.dur[i] = 0      # in ms
        vcl.amp[i] = 0      # in mV
    
def update_VClamp(voltage = -10):
    #print 'Update VClamp - flag = 1'
    clear_IClamp()
    vcl.dur[0] = 10         # in ms
    vcl.amp[0] = -60        # in mV
    vcl.dur[1] = 0          # in ms
    vcl.amp[1] = -60        # in mV
    vcl.dur[2] = 20         # in ms
    vcl.amp[2] = voltage    # in mV
    vcl.dur[3] = 1e9        # in ms
    vcl.amp[3] = -60        # in mV

def block_na_channel():
    axon.soma.gnabar_na = 0
    
def unblock_na_channel():
    axon.soma.gnabar_na = 0.12
    
def block_k_channel():
    axon.soma.gkbar_k = 0
    
def unblock_k_channel():
    axon.soma.gkbar_k = 0.036

def edit_config(cur_amp, cur_dur, cur_del, voltage, toggle_flag):
    # If 0 - IClamp should run
    if toggle_flag == 0:
        #print 'Edit Config - flag = 1'
        update_IClamp(cur_del, cur_dur, cur_amp)
    # If 1 - VClamp should run
    else:
        #print 'Edit Config - flag = 0'
        update_VClamp(float(voltage))

def init_val_reset():
    unblock_na_channel()
    unblock_k_channel()
    update_IClamp()

# Record for Plotting
def record_plot():
    # Record all values for plotting
    v_vec.record(axon.soma(0.5)._ref_v)
    t_vec.record(h._ref_t)
    mna_vec.record(axon.soma(0.5)._ref_m_na)
    hna_vec.record(axon.soma(0.5)._ref_h_na)
    nk_vec.record(axon.soma(0.5)._ref_n_k)
    gna_vec.record(axon.soma(0.5)._ref_gna_na)
    gk_vec.record(axon.soma(0.5)._ref_gk_k)
    ina_vec.record(axon.soma(0.5)._ref_ina)
    ik_vec.record(axon.soma(0.5)._ref_ik)
    il_vec.record(axon.soma(0.5)._ref_il_leak)
    ccl_i_vec.record(ccl._ref_i)
    vcl_i_vec.record(vcl._ref_i)

def run_simulation():
    #print "Simulation Complete."
    h.run()
    #file = open('output.txt', 'w')
    #file.write('  time\t\tvoltage\t\t   ina\t\t\tik\t\til_leak\n')
    #for i in range(0,len(v_vec)):
    #    file.write("%f\t%f\t%f\t%f\t%f\n" % (t_vec.x[i], v_vec.x[i], ina_vec.x[i], ik_vec.x[i], il_vec.x[i]))
        
    #file.close()
    # Plot/Visualize Results
    pyplot.figure(figsize=(12,8))
    pyplot.subplot(611)
    plot_v, = pyplot.plot(t_vec, v_vec,'b', label='axon.soma.v')
    pyplot.xlim(0, tstop)
    pyplot.ylabel('mV')
    pyplot.legend(handles=[plot_v])
    pyplot.title('Soma Voltage')
    pyplot.subplot(612)
    plot_gna, = pyplot.plot(t_vec, gna_vec,'r', label='axon.soma.gna')
    plot_gk, = pyplot.plot(t_vec, gk_vec, 'b', label='axon.soma.gk')
    pyplot.xlim(0, tstop)
    pyplot.ylabel('Siemens/cm^2')
    pyplot.legend(handles=[plot_gna, plot_gk])
    pyplot.title('Conductances')
    pyplot.subplot(613)
    plot_ina, = pyplot.plot(t_vec, ina_vec,'r', label='axon.soma.ina')
    plot_ik, = pyplot.plot(t_vec, ik_vec, 'b', label='axon.soma.ik')
    plot_il, = pyplot.plot(t_vec, il_vec, 'g', label='axon.soma.il')
    pyplot.xlim(0, tstop)
    pyplot.ylabel('mA/cm^2')
    pyplot.title('Current')
    pyplot.legend(handles=[plot_ina, plot_ik, plot_il])
    pyplot.subplot(614)
    plot_mna, = pyplot.plot(t_vec, mna_vec,'r', label='axon.soma.mna')
    plot_hna, = pyplot.plot( t_vec, hna_vec, 'b', label='axon.soma.hna')
    plot_nk, = pyplot.plot( t_vec, nk_vec, 'g', label='axon.soma.nk')
    pyplot.xlim(0, tstop)
    pyplot.title('mna, hna, nk')
    pyplot.legend(handles=[plot_mna, plot_hna, plot_nk])
    pyplot.subplot(615)
    plot_ccl, = pyplot.plot(t_vec, ccl_i_vec,'r', label='ccl.i')
    pyplot.xlim(0, tstop)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('nA')
    pyplot.title('Current Clamp')
    pyplot.legend(handles=[plot_ccl])
    pyplot.subplot(616)
    plot_vcl, = pyplot.plot(t_vec, vcl_i_vec,'r', label='vcl.i')
    pyplot.xlim(0, tstop)
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('nA')
    pyplot.title('Voltage Clamp')
    pyplot.legend(handles=[plot_vcl])
    pyplot.subplots_adjust(left=0.065, bottom=0.075, right=0.98, top=0.95, wspace=0.2, hspace=0.25)
    pyplot.legend()
    pyplot.show()

## Set Parameters for Current and Voltage Clamps
update_IClamp()
record_plot()

#run_simulation()
