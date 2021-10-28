# Define all variable here
import numpy as np


class Globals:

    def __init__(self):
        
        # Boundaries
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        # Number of particles
        self.Np = 50000

        # Diffusivity
        self.D = 0.01

        # Conditions
        self.h = 0.025
        self.time = 0.0
        self.tEnd = 0.025
        
        # Grids
        self.Nx = 64
        self.Ny = 64

        # Create the particles
        self.x = np.random.uniform(low=-1, high=1, size=self.Np)
        self.y = np.random.uniform(low=-1, high=1, size=self.Np)

        # For plots
        self.size = 0.5

        