import numpy as np
import math
from scipy import interpolate

from globals import Globals

class SimulationMath(Globals):

    def __init__(self):
        super().__init__()
        self.ref_sol = []
        self.extract_data()
        
    def extract_data(self):

        n_line = 0

        for line in open(self.velocity_file , 'r'):
            
            if line == "\n":
                n_line += 1
            else:
                lines = [i for i in line.split()]
                self.ref_sol.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=self.velocity_file))
        print("[INFO] There is {num} empty lines".format(num=n_line))

        return self.ref_sol

    # def euler(self, x_coordinate, time_step):

    #     random = np.random.normal(0,1,1)

    #     euler_func = lambda coordinate : coordinate + np.sqrt(2 * self.D) * np.sqrt(time_step) * random[0]

    #     next_x_pos = euler_func(x_coordinate)

    #     return next_x_pos

    def generate_random_number(self, array_size):
        return np.random.normal(0,1, array_size)

    def euler(self, coordinate, array_size, time_step=0.01):
        
        # This causes the grid to be moved to 
        random = self.generate_random_number(array_size)

        return coordinate + np.sqrt(2 * self.D) * np.sqrt(time_step) * random
    
  