from neuron import h
from IPython.display import display, clear_output
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider, HBox
import matplotlib.pyplot as plt
h.load_file('stdrun.hoc')
#import mpld3
#mpld3.enable_notebook()

def run_simulation(gl_hh = 2.0, gna_hh = 12.0, gk_hh = 1.0, cur_inj = 1.0, cap=0.2):
	#gl_hh = gl_hh*0.00010
	#gk_hh = gk_hh*0.01
	#gna_hh = gna_hh*0.001
	#print("gl_hh:",gl_hh)
	#print("gna_hh:",gna_hh)
	#print("gk_hh:",gk_hh)
	#print("cur_inj:",cur_inj)
	#Create the soma section and define the default parameters
	soma = h.Section(name='soma')
	soma.nseg = 1
	soma.diam = 200
	soma.L = 100
	soma.cm = float(cap)

	soma.insert('hh')
	soma.gl_hh = gl_hh
	soma.gnabar_hh = float(gna_hh)
	soma.gkbar_hh = float(gk_hh)
	
	
	#Insert the Hodgkin-Huxley channels and define the conductances
	
	soma.el_hh = -70

	v_init = h.v_init= -60

	#Inject current in the middle of the soma
	stim = h.IClamp(0.5)
	stim.delay = 100
	stim.dur = 500
	stim.amp = float(cur_inj)

	tstop = h.tstop = 800   #ms

	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
	#Record Results  
	h.dt = 0.025

	v0_vec = h.Vector()
	t_vec = h.Vector()
	
	v0_vec.record(soma(0.5)._ref_v)
	t_vec.record(h._ref_t)
	# Run the simulation
	
	h.run()

	
	return t_vec, v0_vec
	
def run_and_display(A):
	# Create input text boxes and buttons for users
	gna_hh = FloatText(value=0, layout=Layout(width='100px'))
	gk_hh = FloatText(value=0, layout=Layout(width='100px'))
	gl_hh = FloatText(value=2.0e-5, layout=Layout(width='100px'))
	cur_inj = FloatText(value=1, layout=Layout(width='100px'))
	run_button = Button(description="Run Model", button_style='info')
	clear_button = Button(description="Clear Output", button_style='warning')

	# Use a form to hold the Labels and Input Boxes 
	form_items = [
		Box([Label(value='Leak Channel (gl_hh)', layout=Layout(width='195px')), gl_hh]),
		Box([Label(value='Sodium Channel (gnabar_hh)', layout=Layout(width='195px')), gna_hh]),
		Box([Label(value='Potassium Channel (gkbar_hh)', layout=Layout(width='195px')), gk_hh]),
		Box([Label(value='Current Injection Amplitude (nA)', layout=Layout(width='195px')), cur_inj]),
		]

	# Define the parameters of the form_items
	form = Box(form_items, layout=Layout(
		display='flex',
		flex_flow='column',
		align_items='initial',
		width='295px'
	))
	# Display form and buttons
	
	display(form, HBox([run_button, clear_button]))
	#display(HBox([f]))
	plt.figure
	# Define functions that run when the user clicks a button
	def run_button_clicked(b):
		t,v=run_simulation(gl_hh.value, gna_hh.value, gk_hh.value, cur_inj.value)
		
		plt.plot(t,v)
		plt.show()

	def clear_button_clicked(b):
		clear_output()

	run_button.on_click(run_button_clicked)
	clear_button.on_click(clear_button_clicked)
