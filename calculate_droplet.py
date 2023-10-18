import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Init Code


pygame.init()
display = (int(1000),int(1000))
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

