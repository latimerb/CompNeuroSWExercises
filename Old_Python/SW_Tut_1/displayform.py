

def disp_form():
    # Create input text boxes and buttons for users
	gna_hh = FloatText(value=0, layout=Layout(width='100px'))
	gk_hh = FloatText(value=0, layout=Layout(width='100px'))
	gl_hh = FloatText(value=2.0e-5, layout=Layout(width='100px'))
	cur_inj = FloatText(value=1, layout=Layout(width='100px'))
	run_button = Button(description="Run Model", button_style='info')
	clear_button = Button(description="Clear Output", button_style='warning')
	# Use a form to hold the Labels and Input Boxes
	form_items =[Box([Label(value='Leak Channel (gl_hh)', layout=Layout(width='195px')), gl_hh]),
	Box([Label(value='Sodium Channel (gnabar_hh)', layout=Layout(width='195px')), gna_hh]),
	Box([Label(value='Potassium Channel (gkbar_hh)', layout=Layout(width='195px')), gk_hh]),
	Box([Label(value='Current Injection Amplitude (nA)', layout=Layout(width='195px')), cur_inj])]
	# Define the parameters of the form_items
	form = Box(form_items, layout=Layout(display='flex',flex_flow='column',align_items='initial',width='295px'))
	# Display form and buttons
	display(form, HBox([run_button, clear_button]))
	return gna_hh, gk_hh