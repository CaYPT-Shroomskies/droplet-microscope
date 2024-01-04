# Modules
import pygame
import numpy
import math as *
import droplet_service as module

# Variables
index_refraction = 1.33 # water bc air really doesnt matter
resolution = 1000
block_size = 25 # Size of black and white tiles (px)
viewpoint_height = "ADD LATER :sob:" # bc ur infinitely far away and we dont want pincushion distortion
# Runtime Variables
visualization_radius = 750 # radius of droplet in pixels

# UNSAFE - SHARED CLASS TYPE, CHECK WITH [draw_graphs.py]
class droplet_params():                                                                                                                                                                                    
    def __init__(self,volume=3,gl_se_constant=0.073,sl_se_constant=0.08):
        self.volume = volume #mL
        self.sl_se_constant = sl_se_constant # J/m^2
        self.gl_se_constant = gl_se_constant # J/m^2

two_map = [] # For any given radius position, returns the refracted position
# Calculate 2D vector relative to distance
droplet = droplet_params()
results = module.basic_solve(droplet)
derivative = results.a_curve * 2
radius = numpy.sqrt(results.height/results.a_curve)

# Just solve for a 2D parabola ray map
for i in range(int(resolution/2)):
    current_rad = radius * 2 * i / resolution
    incidence_angle = numpy.arctan(derivative*current_rad)
    light_angle = 0 # add later if there's a viewpoint height
    refracted_angle = numpy.arcsin(numpy.sin(incidence_angle)/index_refraction)
    slope = numpy.tan(refracted_angle)
    intersection_height = results.a_curve*(current_rad**2) + results.height
    final_position = current_rad + (height/slope)
    two_map.append( (final_position/radius) * visualization_radius )

# wrap to 3D and apply to grid

for y in range(resolution):
    for x in range(resolution):
        black = 0
        dist_x = abs(1000-x)
        dist_y = abs(1000-y)
        rad_dist = numpy.sqrt(dist_x**2+dist_y**2) # At a given distance of intersection, where will the point end up

        

        if (dist_x//25)%2 = (dist_y//25)%2:
            black = 1
