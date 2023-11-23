import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pymesh

# Init Code


## DROPLET VARIABLES

volume = 1 # mL
surfaceTension = 72 # mN/m




class droplet:
    def __init__(self,com,sa,energy):
        droplet.center_of_mass = com;
        droplet.surface_area = sa;
        droplet.energy = energy;
        droplet.vector = [com,energy,sa];


def CalculateSurfaceEnergy()


def DrawCall(COM,SA_F): # Center_of_mass (cm) (one dimensional due to symetry along other axis), Surface_area_floor (cm^2): amount of droplet touching the floor
    # Simplfiy Variable
    energy = ((COM/100)*9.8*(volume/1000))*1000 # energy calculated in mJ
    COM = center_of_mass


for i in range

pygame.init()
display = (int(1000),int(1000))
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
