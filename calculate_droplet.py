import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pymesh

# Init Code

# Basic Geometric shape, only applies to droplets symmetric on X and Z axis

## DROPLET VARIABLES

volume = 1 # mL
surfaceTension = 72 # mJ/m^2
sl_surface_energy = -1 # Surface energy between solid phase and liquid, measured in mJ/m^2
gs_surface_energy = -1 # Surface energy between liquid and gas phase, measured in mJ/m^2




class droplet:
    def __init__(self,com,sa,energy):
        droplet.center_of_mass = com;
        droplet.surface_area = sa;
        droplet.energy = energy;
        droplet.vector = [com,energy,sa];


def CalculateSurfaceEnergy(Surface_area_floor): # Thermodynamic energy calculation
    return Surface_area*FloorHydrophobicity # insert an actual equation here cause wtf :sob:

'''
def DrawCall(COM,SA_F): # Center_of_mass (cm) (one dimensional due to symetry along other axis), Surface_area_floor (cm^2): amount of droplet touching the floor
    # Simplfiy Variable
    energy = ((COM/100)*9.8*(volume/1000))*1000 # energy calculated in mJ
    COM = center_of_mass
'''

#pygame.init()
#display = (int(1000),int(1000))
#pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
