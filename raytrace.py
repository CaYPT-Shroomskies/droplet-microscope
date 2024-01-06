# Modules

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy
import sys
import time
import droplet_service as module

# Variables
index_refraction_water = 1.33
index_refraction_glass = 1.52

resolution = 1000
block_size = 50 # Size of black and white tiles (px)
visualization_radius = 400 # radius of droplet in pixels



viewpoint_height = 3 # Height ABOVE THE PLATFORM OF THE DROPLET (cm)
platform_height = 3 # Height of droplet platform above patterened plane (cm) (TO BOTTOM OF PLATFORM)
platform_thickness = 1 # Thickness of the glass panel


# UNSAFE - SHARED CLASS TYPE, CHECK WITH [draw_graphs.py]
class droplet_params():                                                                                                                                                                                    
    def __init__(self,volume=3,gl_se_constant=0.073,sl_se_constant=0.08):
        self.volume = volume #mL
        self.sl_se_constant = sl_se_constant # J/m^2
        self.gl_se_constant = gl_se_constant # J/m^2


droplet = droplet_params(
    volume = 1,
    sl_se_constant = 0.01
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
radius = numpy.sqrt(-results.height/results.a_curve)

# Solve for a 2D parabola ray map (see visualization)
two_map.append(0) # insert first bc scalar divides are horrible

for i in range(1,visualization_radius):

    # Current Ray Direction for a point on the droplet plane (cm)
    current_rad = radius * i / visualization_radius
    # Solve for air-to-water refraction
    intersection_height = results.a_curve*(current_rad**2) + results.height # Solve the equation
    tangent_angle = numpy.arctan(results.a_curve * 2*current_rad) # take the derivative of the current x position (always negative), then convert it to radians
    light_angle = numpy.arctan(current_rad/platform_height) # add later if there's a viewpoint height
    normalized_angle = tangent_angle+light_angle

    refracted_angle = numpy.arcsin(numpy.sin(normalized_angle)/index_refraction_water)-tangent_angle # that one guys law (shell???) # DOUBLE CHECK TANGENT ANGLE SUBTRACTION GEOMETRY #

    slope = numpy.tan(refracted_angle)
    final_position = current_rad + (intersection_height*slope) # Position when intersecting with glass

    # Glass-Water 
    refracted_angle = numpy.arcsin(numpy.sin(refracted_angle)*index_refraction_water/index_refraction_glass)
    slope = numpy.tan(refracted_angle)
    final_position += platform_thickness*slope

    # Glass-Air
    refracted_angle = numpy.arcsin(numpy.sin(refracted_angle)*index_refraction_glass)
    slope = numpy.tan(refracted_angle)
    final_position += platform_height*slope
    
    predicted_position = (current_rad/platform_height)*(platform_height+platform_thickness+viewpoint_height)
    two_map.append(final_position/predicted_position) # Append a ratio value, ratio to straight-line final position on OBJECT PLANE

# wrap to 3D and apply to grid
    

pygame.init()
window = pygame.display.set_mode((resolution, resolution))
window.fill((120,120,120))
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
            magnitude = two_map[rad_dist]
            dist_x *= magnitude
            dist_y *= magnitude
        elif rad_dist == visualization_radius:
            color = 200
        #else: # Adjust for z-height
            #dist_x *= (platform_thickness+platform_height+viewpoint_height)/viewpoint_height
            #dist_y *= (platform_thickness+platform_height+viewpoint_height)/viewpoint_height
            
        # Return origin to 0,0 for rendering
        dist_x += resolution/2
        dist_y += resolution/2

        if (dist_x//block_size)%2 == (dist_y//block_size)%2:
            color = 255
        
        pxarray[x, y] = pygame.Color(color, color, color)

    pygame.display.flip() # Remove to save like 10% of the time for interp + compi.

    progress(int((y/resolution)*100))

end_progress()
print("Trace Time: "+str( 1000*(time.process_time()-timer))+"ms")

#pxarray.close()

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break