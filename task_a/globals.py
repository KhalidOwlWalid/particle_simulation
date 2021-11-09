# Define all variable here
import numpy as np


class Globals:

    def __init__(self):

        # Substance Attribtue
        self.radius = 0.4
        self.offset_x = 0.4
        self.offset_y = 0.4
        
        # Boundaries
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        # Number of particles
        self.Np = 7500

        # Diffusivity
        self.D = 0.01

        # Conditions
        self.h = 0.025
        self.time = 0.0
        self.tEnd = 0.025

        self.steps = int(self.tEnd / self.h)
        
        # Grids
        self.Nx = 70
        self.Ny = 70

        # Create the particles
        self.x = np.random.uniform(low=-1, high=1, size=self.Np)
        self.y = np.random.uniform(low=-1, high=1, size=self.Np)

        # For size of scatter plots, increase the value to get bigger scatter size
        self.size = 20

        self.velocity_file = 'data_file/velocityCMM3.dat'

        self.include_velocity = True

        