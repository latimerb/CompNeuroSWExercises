from neuron import h
from math import pi

# Define a Class for Cell_A

class SquidCell(object):

    # Create an initialization function that runs when a cell is created
    # Define sections of the cell here and then call function to initatilize that section

    def __init__ (self):

        self.soma = soma = h.Section(name='soma',cell=self)

        self.initsoma()

    # Create a function that initializes the cells section soma

    def initsoma (self):

        soma = self.soma

        soma.nseg = 1

        soma.diam = 500

        soma.L = 500

        soma.Ra = 30

        soma.cm = 1
        
        #soma.insert('hh') 
        
        soma.insert('leak'); soma.el_leak = -60; soma.glbar_leak = 1/3333.33;

        soma.insert('na'); soma.gnabar_na = 0.12;

        soma.insert('k'); soma.gkbar_k = 0.036;