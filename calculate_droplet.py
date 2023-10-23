import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pymesh

# Init Code


## DROPLET VARIABLES

volume = 1 # mL
surfaceTension = 72 # mN/m



pygame.init()
display = (int(1000),int(1000))
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)



