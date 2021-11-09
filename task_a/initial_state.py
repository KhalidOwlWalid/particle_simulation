# Here is where the all the backends for the simulation happens
import numpy as np
import matplotlib.pyplot as plt

from globals import Globals
from simulation_math import SimulationMath

class InitialState(Globals):

    def __init__(self):
        
        super().__init__()
    
        self.sub_1 = []
        self.sub_2 = []
        
    def taskA_initial_state(self):

        isInside = lambda x_coordinate, y_coordinate, radius : (x_coordinate - self.offset_x) ** 2 + (y_coordinate - self.offset_y) ** 2 <= self.radius ** 2

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if isInside(self.x[i], self.y[i], 0.3):
                self.sub_1.append([self.x[i], self.y[i]])

            # Vice versa
            else:
                self.sub_2.append([self.x[i], self.y[i]])

        return np.array(self.sub_1), np.array(self.sub_2)

    def taskB_initial_state(self):

        toTheLeft = lambda coordinate : coordinate <= 0

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if toTheLeft(self.x[i]): 
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        return self.sub_1, self.sub_2

