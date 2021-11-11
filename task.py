import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree

from simulation_math import SimulationMath
from initial_state import InitialState
from concentration import Concentration

class TaskA(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_2", "sub_1"]

        self.field_coordinates, self.vector_field_data = self.read_data_file('data_file/velocityCMM3.dat', [0,1], [2,3])
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

        for step in range(self.steps):
            if self.include_velocity:
                for i, sub_type in enumerate(self.substance_list):

                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))
                    self.interpolated_velocities = self.vector_field_data[self.index]
 
                    self.substance[sub_type][:,0] = self.euler_2D(self.substance[sub_type][:,0], velocity=self.interpolated_velocities[:,0], array_size=len(self.substance[sub_type][:,0]))
                    self.substance[sub_type][:,1] = self.euler_2D(self.substance[sub_type][:,1],  velocity=self.interpolated_velocities[:,1], array_size=len(self.substance[sub_type][:,1]))

            else:
                for i, sub_type in enumerate(self.substance_list):

                    unknown, self.index = self.spatial_field.query(np.array(self.substance[sub_type]))
                    self.interpolated_velocities = self.vector_field_data[self.index]
 
                    self.substance[sub_type][:,0] = self.euler_2D(self.substance[sub_type][:,0],velocity=0, array_size=len(self.substance[sub_type][:,0]))
                    self.substance[sub_type][:,1] = self.euler_2D(self.substance[sub_type][:,1], velocity=0, array_size=len(self.substance[sub_type][:,1]))


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

        axes.set_title('Concentration Plot for time {num}'.format(num=self.tEnd))
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

        print("[INFO] Plotting the solution for time : {solution}".format(solution=self.tEnd))
        self.plot_solution()

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        self.concentration_plot(concentration_grid)
        plt.savefig('diagram/concentration_plot.png')

        print("The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))
        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=(time.process_time() - start)))

        plt.show()

    def test(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()
        self.run_simulation()
        #print(np.array(self.substance["sub_1"]))

class TaskB(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()

        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.Ny = 1

        self.figure, self.axes = plt.subplots()

    # Checks if a particle is going outside the boundary
    def boundary_conditions(self, next_pos_x):

        if next_pos_x > 1:
            distanceFromMax = next_pos_x - self.xMax
            next_pos_x = next_pos_x - 2 * distanceFromMax

        elif next_pos_x < -1:
            distanceFromMax = next_pos_x - self.xMin
            next_pos_x = next_pos_x - 2 * distanceFromMax

        return next_pos_x

    # Runs the simulation 
    def run_simulation(self):
        
        u,v = 0, 0

        # Run the simulation until time ends
        for step in range(self.steps):
        
            for i, sub_type in enumerate(self.substance_list):
                for j, coordinate in enumerate(self.substance[sub_type]):
                    x = coordinate
                    
                    # Calculate using euler's equation
                    next_pos_x = self.euler_1D(x)

                    x = self.boundary_conditions(next_pos_x)

                    # Update our particle's coordinate 
                    self.substance[sub_type][j] = next_pos_x

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

                for j, coordinate in enumerate(self.substance[sub_type]):
                    
                    # Set the color of substance 1 as blue, and red otherwise
                    if sub_type == "sub_1":
                        color = "blue"
                    else:
                        color = "red"

                    x, y = coordinate[0], coordinate[1]

                    self.plot_condition(x,y, color)
        else:
            pass
    
    # This produces a pixelated concentration plot
    def concentration_plot(self, grid):
        print("[INFO] Creating concentration plot...")
        sns.heatmap(grid, cmap='RdBu')

    def save_to_txt(self,array):

        for element in array: #you wouldn't need to write this since you are already in a loop
            file1 = open("observed_data/observed_concentration_v3.txt","a") 
            file1.write("{x_avg} {concentration}\n".format(x_avg=round(element[0], 7), concentration=element[1])) 
            file1.close()

    def main(self):

        self.data = self.extract_data()

        for i in range(3):

            start  = time.process_time()

            self.substance = {"sub_1": [], "sub_2": []}

            # Here you can choose to switch between task A and task B initial state
            self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state()
            #print(len(self.substance["sub_1"]))
   
            self.run_simulation()

            # self.plot_solution(plot_2D=False)
            # plt.savefig('diagram/plot_solution.png')

            concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

            x_grid = np.linspace(-1,1,self.Nx)
            
            concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)
            
            self.axes.plot(*zip(*self.data), color="red")

            if i == 0:
                self.axes.plot(*zip(*concentration_list),'-bo', color="blue", markersize=3)
                
            if i == 1:
                self.axes.plot(*zip(*concentration_list),'-go', color="green", markersize=3)

            if i == 2:
                self.axes.plot(*zip(*concentration_list),'-co', color="cyan", markersize=3)

            plt.savefig('diagram/concentration_plot.png')
            

            print("[INFO] Simulation status : Success")
            print("[INFO] The time taken to complete the simulation is {time}".format(time=(time.process_time() - start)))

        plt.show()
