import numpy as np
import math

from globals import Globals

class SimulationMath(Globals):

    def __init__(self):
        super().__init__()

    def euler(self, coordinate, u = 0, vel_type=False):

        random = np.random.normal(0,1,1)

        euler_func = lambda coordinate : coordinate + u * self.h + np.sqrt(2 * self.D) * np.sqrt(self.h) * float(random)

        if vel_type:
            next_pos = euler_func(coordinate,u)
        else:
            next_pos = euler_func(coordinate)

        return next_pos
        