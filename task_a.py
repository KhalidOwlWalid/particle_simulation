# Add comment
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree

from simulation_math import SimulationMath

"""
This file is responsible in handling all Task A questions
"""
class TaskA(SimulationMath):

    def __init__(self):
        super().__init__()
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_2", "sub_1"]

        # Extract data  from the velocity file and seperate it into two arrays
        self.field_coordinates, self.vector_field_data = self.read_data_file('velocityCMM3.dat', [0,1], [2,3])

        # Creates a spatial field for the use of cKDTree algorithm
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

    # Runs the simulation for task A
    def run_simulation(self):
        
        # Calculate the time step to determine the number of iterations required
        self.steps = int(self.tEnd / self.h)


        for step in range(self.steps):
            if self.include_velocity:

                if self.debug:
                    print("[DEBUG] Calculating for timme : {time}".format(time=(step * self.h)))

                for i, sub_type in enumerate(self.substance_list):
                    
                    # Query the nearest neighbour of our simulations particle from the data file's coordinate
                    # returns an index to give the nearest neighbour from the data file
                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))

                    # Interpolates the velocity field from our data file's vector field
                    self.interpolated_velocities = self.vector_field_data[self.index]

                    # Apply euler formula to find the next position of our particle
                    self.substance[sub_type][:,0] = self.euler(self.substance[sub_type][:,0], velocity=self.interpolated_velocities[:,0], array_size=len(self.substance[sub_type][:,0]), time_step=self.h)
                    self.substance[sub_type][:,1] = self.euler(self.substance[sub_type][:,1],  velocity=self.interpolated_velocities[:,1], array_size=len(self.substance[sub_type][:,1]), time_step=self.h)

            # Euler method without the velocity
            else:
                if self.debug:
                    print("[DEBUG] Calculating for timme : {time}".format(time=(step * self.h)))

                for i, sub_type in enumerate(self.substance_list):

                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))
                    self.interpolated_velocities = self.vector_field_data[self.index]
 
                    self.substance[sub_type][:,0] = self.euler(self.substance[sub_type][:,0],velocity=0, array_size=len(self.substance[sub_type][:,0]), time_step=self.h)
                    self.substance[sub_type][:,1] = self.euler(self.substance[sub_type][:,1], velocity=0, array_size=len(self.substance[sub_type][:,1]), time_step=self.h)

    # Sets the plot condition for our axes
    def plot_condition(self,x,y,color,row = 0, col = 0):

        if row == 0 and col == 0:
            self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
            self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
            self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
            self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
            self.axes.scatter(x,y, s=self.size, c=color)
            
    # Plots our solution
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
                self.axes.set_title('Particle 2D plots for {num1} particles \n and time step {num2}'.format(num1=self.Np, num2=self.h))

    
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

    # For the use if we want to extract data from our simulation file
    def save_to_txt(self,array):

        for i,element in enumerate(array): #you wouldn't need to write this since you are already in a loop
            file1 = open("observed_data/concentration_grid.txt","a") 
            file1.write("{grid}\n".format(grid=element[:])) 
            file1.close()

    # Function to run our simulation for task A
    def main(self):

        start = time.process_time()

        # Initialized the particle's coordinate with task A conditions
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()

        print("[INFO] Running the simulation...")
        # Runs the simulation
        self.run_simulation()

        if self.plot_2D_particle:
            self.plot_solution()
        
        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        self.concentration_plot(concentration_grid)

        if self.debug:
            print("[DEBUG] The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))

        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=round((time.process_time() - start), 2)))

        plt.show()
