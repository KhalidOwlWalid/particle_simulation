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
        self.Np = 64000

        # Diffusivity
        self.D = 0.1

        # Conditions
        self.h = 0.025
        self.time = 0.0
        self.tEnd = 0.2

        self.steps = int(self.tEnd / self.h)
        
        # Grids
        self.Nx = 100
        self.Ny = 1

        # Create the particles
        self.x = np.random.uniform(low=-1, high=1, size=self.Np)
        self.y = np.random.uniform(low=-1, high=1, size=self.Np)

        # For size of scatter plots, increase the value to get bigger scatter size
        self.size = 10

        self.velocity_file = 'data_file/reference_solution_1D.dat'

        self.include_velocity = False

        