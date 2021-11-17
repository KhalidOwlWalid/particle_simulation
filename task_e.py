import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree
from sklearn.metrics import mean_squared_error

from task_a import TaskA

from simulation_math import SimulationMath
from initial_state import InitialState
from concentration import Concentration

from sklearn import linear_model

class TaskE(TaskA):

    def __init__(self):
        super().__init__()

    def main(self):

        start = time.process_time()

        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()

        print("[INFO] Running the simulation...")
        self.run_simulation()

        # print("[INFO] Plotting the solution for time : {solution}".format(solution=self.tEnd))
        self.plot_solution()

        concentration_grid = self.calculate_concentration(self.substance["sub_1"])

        self.concentration_plot(concentration_grid)
        plt.savefig('diagram/concentration_plot.png')

        if self.debug:
            print("[DEBUG] The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))

        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=round((time.process_time() - start), 2)))

        plt.show()

    def calculate_concentration(self, sub_1):
        
        print("[INFO] Calculating concentration... This may take awhile...")
        print("[INFO] Set self.debug = True if you wish to see which grid the programme is currenly calculating")
        
        # Populate a "grid" with zeros
        grid_list = []
        
        self.sub_1 = sub_1

        zero_div_err = 0

        grid_position = lambda x, y, i, j: x > self.x_grid[i] and x < self.x_grid[i+1] and y < self.y_grid[j] and y > self.y_grid[j+1]
        
        for i in range(self.Nx - 1):
            grid_list.append([0 for j in range(self.Ny - 1)])

        for i in range(len(self.x_grid)- 1):
            for j in range(len(self.y_grid) - 1):

                for particle in sub_1:
                    # Check corner
                    if grid_position(particle[0], particle[1], i, j):
                        grid_list[j][i] += 1

                try:
                    # TODO : Add maths equation here
                    pass

                except ZeroDivisionError:
                    zero_div_err += 1
                    #print("[WARN] ZeroDivisionError : Not enough particles to calculate")

                except IndexError:
                    print("[WARN] IndexError: Out of boundaries at column {col}, row {row}".format(col=i, row=j))

                if self.debug:  
                    print("[DEBUG] Grid {num}".format(num=(i,j)))

        if self.debug:  
            print("[DEBUG] Number of empty pixels : {num}".format(num=zero_div_err))    
                    
        return np.array(grid_list)



