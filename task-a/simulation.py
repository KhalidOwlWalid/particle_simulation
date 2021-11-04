import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from simulation_math import SimulationMath
from initial_state import InitialState
from concentration import Concentration

class TaskA(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.figure, self.axes = plt.subplots()

    # Checks if a particle is going outside the boundary
    def boundary_conditions(self, next_pos_x, next_pos_y):

        if next_pos_x > 1:
            distanceFromMax = next_pos_x - self.xMax
            next_pos_x = next_pos_x - 2 * distanceFromMax

        elif next_pos_x < -1:
            distanceFromMax = next_pos_x - self.xMin
            next_pos_x = next_pos_x - 2 * distanceFromMax

        if next_pos_y > 1:
            distanceFromMax = next_pos_y - self.yMax
            next_pos_y = next_pos_y - 2 * distanceFromMax

        elif next_pos_y < -1:
            distanceFromMax = next_pos_y - self.yMin
            next_pos_y = next_pos_y - 2 * distanceFromMax

        return next_pos_x, next_pos_y

    # Runs the simulation 
    def run_simulation(self):
        
        u,v = 0, 0

        # Run the simulation until time ends
        #while self.time < self.tEnd:
        for step in range(self.steps):
            if self.include_velocity:
                for i, sub_type in enumerate(self.substance_list):
                    for j, coordinate in enumerate(self.substance[sub_type]):
                        x, y = coordinate[0], coordinate[1]
                        
                        u,v = self.bilinear_interpolation(x,y)
                        # Calculate using euler's equation
                        next_pos_x = self.euler(x,vel = u ,vel_type=True)
                        next_pos_y = self.euler(y, vel = v, vel_type=True)

                        x, y = self.boundary_conditions(next_pos_x, next_pos_y)

                        # Update our particle's coordinate 
                        self.substance[sub_type][j] = (next_pos_x, next_pos_y)

            else:
                for i, sub_type in enumerate(self.substance_list):
                    for j, coordinate in enumerate(self.substance[sub_type]):
                        x, y = coordinate[0], coordinate[1]
                        
                        # Calculate using euler's equation
                        next_pos_x = self.euler(x)
                        next_pos_y = self.euler(y)

                        x, y = self.boundary_conditions(next_pos_x, next_pos_y)

                        # Update our particle's coordinate 
                        self.substance[sub_type][j] = (next_pos_x, next_pos_y)

            self.time += self.h
            print("[INFO] Time: ", round(self.time,3))

    # Sets all the plot condition on the graph
    def plot_condition(self,x,y,color,row = 0, col = 0):

        if row == 0 and col == 0:
            self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
            self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
            self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
            self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
            self.axes.scatter(x,y, s=self.size, c=color)
            
    # Obviously
    def plot_solution(self, plot_2D=True):

        if plot_2D:
            for i, sub_type in enumerate(self.substance_list):

                color = None 
                print("Plotting for ", sub_type)

                # for j, coordinate in enumerate(self.substance[sub_type]):

                if sub_type == "sub_1":
                    color = "red"
                else:
                    color = "blue"

                #     print(j)
                #     x, y = coordinate[0], coordinate[1]

                #     self.plot_condition(x,y, color)
                #     plt.savefig('diagram/plot_solution.png')
                self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
                self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
                self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
                self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
                self.axes.scatter(*zip(*self.substance[sub_type]), s=self.size, c=color)
            

        else:
            pass
    
    # This produces a pixelated concentration plot
    def concentration_plot(self, grid):
        print("[INFO] Creating concentration plot...")

        # gist_ncar, seismic
        sns.heatmap(grid, cmap='seismic')


    def main(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()

        print("[INFO] Running the simulation...")
        self.run_simulation()

        print("[INFO] Plotting the solution for time : {solution}".format(solution=self.tEnd))
        self.plot_solution()
        fig1 = plt.figure()

        

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])
        
        print(concentration_grid)
        self.concentration_plot(concentration_grid)
        plt.savefig('diagram/concentration_plot.png')

        plt.show()


        print("The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))
        print("[INFO] Simulation status : Success")


        
test = TaskA()

test.main()


