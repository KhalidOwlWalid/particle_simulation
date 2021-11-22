# Add comment
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree

from simulation_math import SimulationMath


class TaskA(SimulationMath):

    def __init__(self):
        super().__init__()
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_2", "sub_1"]

        self.field_coordinates, self.vector_field_data = self.read_data_file('velocityCMM3.dat', [0,1], [2,3])
        self.spatial_field = cKDTree(self.field_coordinates)

        

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

    def run_simulation(self):
        
        self.steps = int(self.tEnd / self.h)

        for step in range(self.steps):
            if self.include_velocity:
                for i, sub_type in enumerate(self.substance_list):
                    
                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))
                    self.interpolated_velocities = self.vector_field_data[self.index]
 
                    self.substance[sub_type][:,0] = self.euler(self.substance[sub_type][:,0], velocity=self.interpolated_velocities[:,0], array_size=len(self.substance[sub_type][:,0]), time_step=self.h)
                    self.substance[sub_type][:,1] = self.euler(self.substance[sub_type][:,1],  velocity=self.interpolated_velocities[:,1], array_size=len(self.substance[sub_type][:,1]), time_step=self.h)

            else:
                for i, sub_type in enumerate(self.substance_list):

                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))
                    self.interpolated_velocities = self.vector_field_data[self.index]
 
                    self.substance[sub_type][:,0] = self.euler(self.substance[sub_type][:,0],velocity=0, array_size=len(self.substance[sub_type][:,0]), time_step=self.h)
                    self.substance[sub_type][:,1] = self.euler(self.substance[sub_type][:,1], velocity=0, array_size=len(self.substance[sub_type][:,1]), time_step=self.h)


    def plot_condition(self,x,y,color,row = 0, col = 0):

        if row == 0 and col == 0:
            self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
            self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
            self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
            self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
            self.axes.scatter(x,y, s=self.size, c=color)
            
    # Obviously
    def plot_solution(self, plot_2D=True):
        
        self.figure, self.axes = plt.subplots()

        if plot_2D:
            for i, sub_type in enumerate(self.substance_list):

                color = None 
                print("[INFO] Plotting for ", sub_type)

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

        axes.set_title('Concentration Plot for time {num} \n with time step {h}'.format(num=self.tEnd, h = self.h))
        axes.set_xlabel('x')
        axes.set_ylabel('y')

        heatmap.set_cmap('brg')
        figure.colorbar(matplotlib.cm.ScalarMappable(cmap='brg'))

    def save_to_txt(self,array):

        for i,element in enumerate(array): #you wouldn't need to write this since you are already in a loop
            file1 = open("observed_data/concentration_grid.txt","a") 
            file1.write("{grid}\n".format(grid=element[:])) 
            file1.close()


    def main(self):

        start = time.process_time()

        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()

        print("[INFO] Running the simulation...")
        self.run_simulation()

        if self.plot_2D_particle:
        # print("[INFO] Plotting the solution for time : {solution}".format(solution=self.tEnd))
            self.plot_solution()
        
        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        self.concentration_plot(concentration_grid)

        if self.debug:
            print("[DEBUG] The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))

        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=round((time.process_time() - start), 2)))

        plt.show()
