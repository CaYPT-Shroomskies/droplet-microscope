import droplet_service as module
import numpy as np
import matplotlib.pyplot as plt

class droplet_params():                                                                                                                                                                                    
    def __init__(self,volume=3,gl_se_constant=0.08,sl_se_constant=0.08):
        self.volume = volume
        self.sl_se_constant = sl_se_constant
        self.gl_se_constant = gl_se_constant

def drawHeightVolume():
    minimum = 0.1 # mL
    maximum = 20

    step_size = 0.1

    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size) ):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume=minimum+step_size*i)) .height)
    
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.show()



def drawHeightSurfaceGasEnergy():
    minimum = 0.01 # J/m^2
    maximum = 1

    volume = 2 # mL

    step_size = 0.01

    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size) ):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume = volume, gl_se_constant=minimum+step_size*i)) .height)
    
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.show()

def drawHeightSurfaceSolid():
    minimum = 0.01 # J/m^2
    maximum = 1

    step_size = 0.01

    volume = 2 # mL
    
    x_graph = []
    y_graph = []
    for i in range(int((maximum-minimum)/step_size)):
        x_graph.append(minimum+step_size*i)
        y_graph.append(module.basic_solve(droplet_params(volume = volume, sl_se_constant=minimum+step_size*i)) .height)
    
    plt.plot(np.array(x_graph),np.array(y_graph))
    plt.show()



#drawHeightVolume()
#drawHeightSurfaceGasEnergy()
drawHeightSurfaceSolid()
