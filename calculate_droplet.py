## MODULES
import numpy as np 
import matplotlib.pyplot as plt
import math

'''
Units used throughout: mJ, cm, mL, cm^2 unless explicitly stated otherwise

Works on the basis:
1. Droplet can be described as a parabaloid (can be changed later)
2. Droplet is rotationally symetric on z-axis

https://www.desmos.com/3d/499e8aa617
Parabaloid visualization

'''

## DROPLET VARIABLES

volume = 1 # mL
sl_se_constant = 100 # Surface energy between solid phase and liquid, measured in mJ/cm^2
gl_se_constant = 72 # Surface energy between liquid and gas phase, measured in mJ/cm^2


## PRECISION VARIABLES
initialShape = 0.25/volume # initial [a] value for the paraboloid
initialStepSize = 0.05
stepSizeGeometry = 0.5 # amount to multiply step value by at each split.
watchdogTimeoutThreshold = 10000 # Timeout counter
precision = 3 # Amount of geometric decreases in step size


gravitationalPrecision = 100
arcPrecision = 200 # amount of arcs represented in quarter parabola multiplied into area.


## FUNCTIONS

def floorEnergy(a,c):
    return - sl_se_constant * (c/a) * math.pi; # insert an actual explanation here cause yes :sob:

def gasPhaseEnergy(a,c):
    # get the surface area through a line integral of the length of the parabolic curve

    radius = math.sqrt(c/a) # Radius of base of paraboloid
    segment_length = radius/arcPrecision
    
    area = 0
    for n in range(1,arcPrecision):
        # just the pythagagorean of segment length and delta y, multiplied by circumference to get the surface area
        area += (math.pi*2*radius)* math.sqrt((segment_length**2)+( ((-a*(segment_length*n)**2)+c) -((-a*(segment_length*(n -1 ))**2)+c))**2)

    return area * gl_se_constant

def gravitationalEnergyIntegral(a,c): # a and c belong to the standard equation form ax^2 + c. k is the precision value.
    sum = 0
    k = gravitationalPrecision
    for n in range(k):
        sum -= ( (math.pi)*(c**3)*(n**2)*(0.098) ) / ( (k**3)*a )  # volume multiplied by height and gravitational constant
    print("Eg = "+str(sum))
    return sum

def drawParaboloid(a):
    # \ -a\left(x^{2}+y^{2}\ \right)+c\ \left\{z>0\right\}
    # just set the integral to be equal to the volume and solve for it :pleading_face: bro the 3d integral tho

    # nvm we just do the funny thing with the paraboloid equation
    return math.sqrt(volume*2*a/math.pi)


def getEnergy(a):
    c = drawParaboloid(a)
    e = gravitationalEnergyIntegral(a,c) + floorEnergy(a,c) + gasPhaseEnergy(a,c)
    return e,c


## RUNTIME

# Runtime Variables
watchdog = 0
geometricRepeats = 0
lastShape = initialShape
lastEnergy = 0
graph = []

stepSize = initialStepSize

# Determine Initial direction
lastEnergy,_ = getEnergy(lastShape)
upEnergy,_ = getEnergy(lastShape+stepSize)
if upEnergy > lastEnergy:
    stepSize *= -1 # If a positive step increases energy, reflect step.

# Minimization loop
while watchdog < watchdogTimeoutThreshold and geometricRepeats < precision:
    a = lastShape+stepSize
    stepEnergy,c = getEnergy(a)

    graph.append([stepEnergy,a,c]) # Energy, a, and c

    if stepEnergy > lastEnergy: # If energy is greater than the last step, reverse direction and make step smaller
        stepSize *= -(stepSizeGeometry)
        geometricRepeats += 1
    #print(str(stepEnergy)+" mJ" )
    lastEnergy,lastShape = stepEnergy,a # Update runtime values for next iteration

    watchdog += 1

if geometricRepeats >= precision:
    print("Minimum energy reached.")
    print(str(lastEnergy)+" mJ" )
    print("Used "+str(watchdog)+" steps.")
    print("Graph parameters: a = "+str(graph[-1][1])+", c = "+str(graph[-1][2]))
else:
    print("Watchdog timed out.")

exit()

#plt.plot(np.array(graph))
#plt.show()