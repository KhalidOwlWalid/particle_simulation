"""
This file handles all the concentration problem. 

calculate_concentration : calculate concentration for both 1D and 2D case. If self.Ny is set to 1, then its a 1D case. Need to improve
assgin_concentration : Assign concentration to each respective particles and this function is meant for task B

"""

import numpy as np

from globals import Globals

class Concentration(Globals):

    def __init__(self):
        super().__init__()

        self.x_grid = np.linspace(-1,1,self.Nx)
        self.y_grid = np.linspace(1,-1,self.Ny)

        self.sub_1 = None
        self.sub_2 = None
        
    def calculate_concentration(self, sub_1, sub_2):
        
        print("[INFO] Calculating concentration...")
        # Populate a "grid" with zeros
        grid_list = []
        
        self.sub_1 = sub_1
        self.sub_2 = sub_2

        zero_div_err = 0

        grid_position = lambda x, i : x > self.x_grid[i] and x < self.x_grid[i+1] 


        grid_list.append([0 for j in range(self.Nx - 1)])

        for n in range(len(self.x_grid) - 1):
            
            try:
                n_sub_2 = 0 

                for particle in sub_1:
                    if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                        grid_list[0][n] += 1

                for particle in sub_2:
                    if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                        n_sub_2 += 1

            except IndexError:
                print("[DEBUG] Index out of range which is the {n}th column".format(n=n))

            try:
                grid_list[0][n] = grid_list[0][n]/(grid_list[0][n] + n_sub_2)

            except ZeroDivisionError:
                print("[WARN] ZeroDivisionError : Not enough particles to calculate")

            except IndexError:
                print("[WARN] IndexError")
                
        return np.array(grid_list)

    # This one is actually meant for the use of task B, but I have created it and tested it on task A
    def assign_concentration(self, sub_1, sub_2, concentration_grid, x_grid):
        
        concentration_plot = []
        
        
        print(concentration_grid)
        # try:
        for i, concentration in enumerate(concentration_grid) :
            avg_x_coordinates = []
            print(concentration)
            for particle in sub_1:
                if particle > x_grid[i] and particle < x_grid[i+1]:
                    avg_x_coordinates.append(particle)

            for particle in sub_2:
                if particle > x_grid[i] and particle < x_grid[i+1]:
                    avg_x_coordinates.append(particle)

            avg_x = np.mean(avg_x_coordinates)

            concentration_plot.append((avg_x, concentration))
                
        # except IndexError:
        #     print("[DEBUG] Index Error write something here")

        return concentration_plot
