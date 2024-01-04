# Modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy
import sys
import time
import droplet_service as module

# Variables
index_refraction = 1.33 # water bc air really doesnt matter
resolution = 500
block_size = 50 # Size of black and white tiles (px)
viewpoint_height = "ADD LATER :sob:" # bc ur infinitely far away and we dont want pincushion distortion
# Runtime Variables
visualization_radius = 200 # radius of droplet in pixels

# UNSAFE - SHARED CLASS TYPE, CHECK WITH [draw_graphs.py]
class droplet_params():                                                                                                                                                                                    
    def __init__(self,volume=3,gl_se_constant=0.073,sl_se_constant=0.08):
        self.volume = volume #mL
        self.sl_se_constant = sl_se_constant # J/m^2
        self.gl_se_constant = gl_se_constant # J/m^2


droplet = droplet_params(
    volume = 1,
)

# General Functions
def start_progress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def end_progress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()


two_map = [] # For any given radius position, returns the refracted position
# Calculate 2D vector relative to distance
results = module.basic_solve(droplet)
derivative = results.a_curve * 2
radius = numpy.sqrt(-results.height/results.a_curve)

# Just solve for a 2D parabola ray map
for i in range(visualization_radius):
    current_rad = radius * i / visualization_radius
    incidence_angle = numpy.arctan(derivative*current_rad)
    light_angle = 0 # add later if there's a viewpoint height
    refracted_angle = numpy.arcsin(numpy.sin(incidence_angle)/index_refraction)
    slope = numpy.tan(refracted_angle)
    intersection_height = results.a_curve*(current_rad**2) + results.height
    final_position = current_rad + (intersection_height*slope)
    two_map.append( (final_position/radius) * visualization_radius )

# wrap to 3D and apply to grid
    

pygame.init()
window = pygame.display.set_mode((resolution, resolution))
window.fill((255,255,255))
pygame.display.flip
pxarray = pygame.PixelArray(window)

start_progress("Raytracing...")
timer = time.process_time()

for y in range(resolution):
    for x in range(resolution):
        color = 0
        # Move origin to center of drop
        dist_x = (resolution/2)-x
        dist_y = (resolution/2)-y

        rad_dist = int(numpy.sqrt(dist_x**2+dist_y**2))  # Distance from droplet

        if rad_dist < visualization_radius -1 and rad_dist != 0:
            magnitude = two_map[rad_dist]/rad_dist
            dist_x *= magnitude
            dist_y *= magnitude
        if rad_dist == visualization_radius:
            color = 120

        # Return origin to 0,0 for rendering
        dist_x += resolution/2
        dist_y += resolution/2

        if (dist_x//block_size)%2 == (dist_y//block_size)%2:
            color = 255
        
        pxarray[x, y] = pygame.Color(color, color, color)

    progress(int((y/resolution)*100))

end_progress()
print("Trace Time: "+str( 1000*(time.process_time()-timer))+"ms")

pxarray.close()

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break