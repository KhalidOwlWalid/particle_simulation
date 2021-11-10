import numpy as np
import math
from scipy import interpolate
from scipy.spatial import cKDTree

from globals import Globals

class SimulationMath(Globals):

    def __init__(self):
        super().__init__()
        self.data = []
        self.x_data = []
        self.y_data = []
        self.u_data = []
        self.v_data = []
        self.extract_data()

    def read_data_file(self, file, *args):
        return [np.loadtxt(file, usecols=tuple(c)) for c in args]
    
    def extract_data(self):

        n_line = 0

        if self.velocity_file == "data_file/velocityCMM3.dat":
            
            for line in open(self.velocity_file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    self.data.append((float(lines[0]), float(lines[1]), float(lines[2]), float(lines[3])))
                    self.x_data.append(float(lines[0]))
                    self.y_data.append(float(lines[1]))
                    self.u_data.append(float(lines[2]))
                    self.v_data.append(float(lines[3]))

            
        if self.velocity_file == "data_file/reference_solution_1D.dat":

            for line in open(self.velocity_file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    self.data.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=self.velocity_file))
        print("[INFO] There is {num} empty lines".format(num=n_line))

        return self.data

    def generate_random_number(self, array_size):
        return np.random.normal(0,1, array_size)

    def euler_2D(self, coordinate, velocity, array_size):
        
        # This causes the grid to be moved to 
        random = self.generate_random_number(array_size)

        return coordinate + velocity * self.h + np.sqrt(2 * self.D) * np.sqrt(self.h) * random

    def euler_1D(self, x_coordinate):

        random = np.random.normal(0,1,1)

        euler_func = lambda coordinate : coordinate + np.sqrt(2 * self.D) * np.sqrt(self.h) * random[0]

        next_x_pos = euler_func(x_coordinate)

        return next_x_pos
    
