# Define all variable here
import numpy as np


class Globals:

    def __init__(self):

        # Substance Attribtue
        self.radius = 0.3
        
        # Boundaries
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        # Number of particles
        self.Np = 15000

        # Diffusivity
        self.D = 0.1

        # Conditions
        self.h = 0.1
        self.time = 0.0
        self.tEnd = 0.2

        # Grids
        self.Nx = 64
        self.Ny = 1

        # Create the particles
        self.x = np.random.uniform(low=-1, high=1, size=self.Np)

        # For size of scatter plots, increase the value to get bigger scatter size
        self.size = 10

        self.velocity_file = 'data_file/reference_solution_1D.dat'

        self.Np_list = np.arange(15000,150000,10000)
        # self.h_list = [0.1, 0.01, 0.001]
        self.h_list = np.linspace(0.1,0.0001, 50)


        