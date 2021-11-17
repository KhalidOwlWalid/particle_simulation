import numpy as np
import math
from scipy import interpolate
from scipy.spatial import cKDTree

from globals import Globals

class SimulationMath(Globals):

    def __init__(self):
        super().__init__()

    def read_data_file(self, file, *args):
        return [np.loadtxt(file, usecols=tuple(c)) for c in args]
    
    def extract_data(self, file):

        data = []

        n_line = 0
            
        if file == "data_file/reference_solution_1D.dat":

            for line in open(file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    data.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=file))
        print("[INFO] There is {num} empty lines".format(num=n_line))

        return data

    def generate_random_number(self, array_size):
        return np.random.normal(0,1, array_size)

    def euler(self, coordinate, velocity, array_size, time_step):
        
        # This causes the grid to be moved to 
        random = self.generate_random_number(array_size)
        print(time_step)
        return coordinate + velocity * time_step + np.sqrt(2 * self.D) * np.sqrt(time_step) * random

