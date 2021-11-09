import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time

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

        print(self.substance["sub_1"])
        # Run the simulation until time ends
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
                        print("Particle {num} of {type} at {time}".format(num=j, type=sub_type, time=self.time))

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

                if sub_type == "sub_1":
                    color = "red"
                else:
                    color = "blue"

                self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
                self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
                self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
                self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
                self.axes.scatter(*zip(*self.substance[sub_type]), s=self.size, c=color)

    
    # This produces a pixelated concentration plot
    def concentration_plot(self, grid):
        print("[INFO] Creating concentration plot...")

        figure, axes = plt.subplots()

        heatmap = axes.imshow(grid, extent=(self.xMin, self.xMax, self.yMin, self.yMax))

        axes.set_title('Concentration Plot')
        axes.set_xlabel('x')
        axes.set_ylabel('y')

        heatmap.set_cmap('brg')
        figure.colorbar(matplotlib.cm.ScalarMappable(cmap='brg'))
        # x_axis_labels = np.linspace(self.xMin, self.xMax, 10)
        # y_axis_labels = np.linspace(self.yMin, self.yMax, 10)

        # # gist_ncar, seismic, coolwarm, brg
        # # https://matplotlib.org/stable/gallery/color/colormap_reference.html
        # sns.heatmap(grid, cmap='brg', xticklabels=x_axis_labels, yticklabels=y_axis_labels)


    def main(self):

        start = time.process_time()

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

        print("The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))
        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=(time.process_time() - start)))

        plt.show()



