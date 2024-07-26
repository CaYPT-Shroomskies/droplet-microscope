## Serves as a utility function for the droplet code.
## Code for utilizing this script can be found in droplet graph thingy
## 
## Essentially this script just acts as a module, and you can call it with a 'droplet_params' class that describes the droplet you're attempting to simulate.
##

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



## PRECISION VARIABLES ##
initialShape = - 0.1 # initial [a] value for the paraboloid
initialStepSize = 0.03
stepSizeGeometry = 0.5 # amount to multiply step value by at each split.
watchdogTimeoutThreshold = 100000 # Timeout counter
precision = 10 # Amount of geometric decreases in step size [Dont go over 30, FP limits are hit far below that]


gravitationalPrecision = 30 # Amount of slices of parabola for which Eg is calculated.
arcPrecision = 100 # amount of arcs represented in quarter parabola multiplied into area.

sigfigs = 3 # Sigfigs of the results printed


class results():
    a_curve = 0
    height = 0
    droplet_params = 0
    solve_graph = 0


## CONSTANTS ##
def basic_solve(droplet):
    volume = droplet.volume # mL

    # [[MEASURED IN J/m^2 BC ITS STANDARD]]
    sl_se_constant = droplet.sl_se_constant # Surface energy between solid phase and liquid, measured in J/m^2
    gl_se_constant = droplet.gl_se_constant # Surface energy between liquid and gas phase, measured in J/m^2

    gravity = 9.81 # m/s^s




    # Unit Conversions
    gl_se_constant *= (1000 / 10000) # mJ/J and cm^2/m^2
    sl_se_constant *= (1000 / 10000) # mJ/J and cm^2/m^2

    # Coding Values
    debug = False

    ## FUNCTIONS ##

    def floorEnergy(a,c):
        return (sl_se_constant * (-c/a) * math.pi)

    def gasPhaseEnergy(a,c):
        # get the surface area through a line integral of the length of the parabolic curve

        radius = math.sqrt(-c/a) # Radius of base of paraboloid
        segment_length = radius/arcPrecision

        area = 0
        for n in range(1,arcPrecision):
            # the pythagagorean of segment length and delta y, multiplied by circumference to get the surface area
            area += (math.pi*2*segment_length*n)* math.sqrt( (segment_length**2) +( ((-a*(segment_length*n)**2)+c) -((-a*(segment_length*(n -1 ))**2)+c))**2)
        return area * gl_se_constant


    def gravitationalEnergy(a,c): # a and c belong to the standard equation form ax^2 + c. k is the precision value.
        sum = 0
        k = gravitationalPrecision
        for n in range(k):
            sum -= ( (math.pi)*(c**3)*(n**2)*(gravity/100) ) / ( (k**3)*a )  # volsume multiplied by height and gravitational constant
        return sum

    def drawParaboloid(a):
        # \ -a\left(x^{2}+y^{2}\ \right)+c\ \left\{z>0\right\}
        # just set the integral to be equal to the volume and solve for it :pleading_face: bro the 3d integral tho

        # nvm we just do the funny thing with the paraboloid equation
        return math.sqrt( - volume*2*a/math.pi )


    def getEnergy(a):
        c = drawParaboloid(a)
        e = gravitationalEnergy(a,c) + floorEnergy(a,c) + gasPhaseEnergy(a,c)
        return e,c


    ## RUNTIME ##

    # Runtime Variables #
    watchdog = 0
    geometricRepeats = 0
    lastShape = initialShape
    lastEnergy = 0
    graph = []

    stepSize = initialStepSize

    # Determine Initial direction= 
    lastEnergy,_ = getEnergy(lastShape)
    upEnergy,_ = getEnergy(lastShape+stepSize)

    if upEnergy > lastEnergy:
        stepSize *= -1 # If a positive step increases energy, reflect step.

    # Minimization loop
    while geometricRepeats < precision:
        a = lastShape+stepSize
        stepEnergy,c = getEnergy(a)

        graph.append([stepEnergy,a,c]) # record e, a, and c

        if stepEnergy > lastEnergy: # If energy is greater than the last step, reverse direction and make step smaller
            stepSize *= -(stepSizeGeometry)
            geometricRepeats += 1

        # Some debugging lines
        if debug:
            print(str(stepEnergy)+" mJ" )
        #print("Curvature Value: "+str(a))

        lastEnergy,lastShape = stepEnergy,a # Update runtime values for next iteration

        watchdog += 1
        if watchdog > watchdogTimeoutThreshold:
            print("Watchdog timeout")
            exit()

    lastEnergy = math.floor(lastEnergy*(10**precision))/(10**precision)
    print("Minimum energy reached.\n"+str(int(lastEnergy*10**sigfigs)/10**sigfigs)+" mJ" )
    print("Used "+str(watchdog)+" steps.")
    print("Graph parameters: a = "+str(int(graph[-1][1]*10**sigfigs)/10**sigfigs)+", c = "+str(int(graph[-1][2]*10**sigfigs)/10**sigfigs)) # The last values in the graph


    return_results = results()
    return_results.height = graph[-1][2]
    return_results.a_curve = graph[-1][1]
    return_results.solve = graph
    return_results.droplet_params = droplet

    return return_results

    '''
    # show energy-[a] curve
    a_list = []
    e_list = []
    for i in graph:
        e_list.append(graph[0])

        a_list.append(graph[1])

    plt.plot(np.array(a_list),np.array(e_list))
    plt.show()
    '''

    '''
    # Graphing portion
    current_a = 0
    maximum_a = 2
    precise = 0.01 # amount to tick by

    x = []
    y = []

    while current_a < maximum_a:
        current_a += precise
        y.append(getEnergy(-current_a)[0])
        x.append(current_a)

    plt.plot(np.array(x),np.array(y))
    plt.show()

    '''
