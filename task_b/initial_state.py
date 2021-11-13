# Here is where the all the backends for the simulation happens
import numpy as np
import matplotlib.pyplot as plt

from globals import Globals
from simulation_math import SimulationMath

class InitialState(Globals):

    def __init__(self):
        
        super().__init__()
   
    def taskB_initial_state(self, Np):

        toTheLeft = lambda coordinate : coordinate <= 0
        self.x = np.random.uniform(low=-1, high=1, size=Np)
        self.sub_1 = []
        self.sub_2 = []

        # Divide the particles into their substance type
        for i in range(Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if toTheLeft(self.x[i]): 
                self.sub_1.append(self.x[i])

            # Vice versa
            else:
                self.sub_2.append(self.x[i])

        print((len(self.sub_1) + len(self.sub_2)))
        return np.array(self.sub_1), np.array(self.sub_2)
