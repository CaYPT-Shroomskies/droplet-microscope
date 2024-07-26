# Modules
import droplet_service as module
import numpy as np
import matplotlib.pyplot as plt
import math

'''
UTILIZE:
- Change which graph to display by editing the comments at the bottom. Multiple can be calculated at once.

- Change parameters for the graphs using the variables at the top of each function. 

- If things like precision need to be changed, they can be edited in the droplet_service script.

'''

# Class that our droplet_service module accepts as input
class droplet_params():                                                                                                                                                                                    
    def __init__(self,volume=3,gl_se_constant=0.073,sl_se_constant=0.08):
        self.volume = volume #mL
        self.sl_se_constant = sl_se_constant # J/m^2
        self.gl_se_constant = gl_se_constant # J/m^2


# Volume-Height Graph
def drawHeightVolume():
    # Variables
    minimum = 0.1 # mL
    maximum = 20

    step_size = 0.1

    # Calculation
    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size) ):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume=minimum+step_size*i)) .height)


    # Graphing
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.title("Volume vs. Height")
    plt.xlabel("Volume (mL)")
    plt.ylabel("Height (cm)")
    plt.show()



def drawHeightSurfaceGasEnergy():
    # Variables

    minimum = 0.01 # J/m^2
    maximum = 1

    volume = 2 # mL

    step_size = 0.01

    # Calculation

    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size) ):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume = volume, gl_se_constant=minimum+step_size*i)) .height)

    # Graphing
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.title("Liquid-Gas Energy Constant vs. Height")
    plt.suptitle("Volume: "+str(volume)+"mL")
    plt.xlabel("Liquid-Gas Energy Constant (J/m^2)")
    plt.ylabel("Height (cm)")
    plt.show()

def drawHeightSurfaceSolid():
    # Variables
    minimum = 0.01 # J/m^2
    maximum = 1

    step_size = 0.01
    volume = 2 # mL

    # Calculations
    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size)):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume = volume, sl_se_constant=minimum+step_size*i)) .height)

    # Graphing
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.title("Liquid-Solid Energy Constant vs. Height")
    plt.suptitle("Volume: "+str(volume)+"mL")
    plt.xlabel("Liquid-Surface Energy Constant (J/m^2)")
    plt.ylabel("Height (cm)")
    plt.show()

def draw_droplet():
    droplet = droplet_params()
    results = module.basic_solve(droplet)
    a = results.a_curve
    c = results.height

    x_graph = []
    y_graph = []
    intercepts = abs(math.sqrt(-4*a*c)/(2*a)) # Quadratic solve for X intercepts
    print(intercepts)
    precision = 30
    for i in range(1,precision):
        x_value = -intercepts+(intercepts*2*(i/precision))
        x_graph.append(x_value)
        y_graph.append( (a * (x_value**2)) + c )
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.title("Droplet Shape (Cross-section)")
    plt.xlabel("Length (cm)")
    plt.ylabel("Height (cm)")

    plt.xlim(-intercepts, intercepts)
    plt.ylim(0, intercepts*2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


drawHeightVolume()
drawHeightSurfaceGasEnergy()
drawHeightSurfaceSolid()
draw_droplet()
