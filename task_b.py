import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree
from sklearn.metrics import mean_squared_error

from simulation_math import SimulationMath
from initial_state import InitialState
from concentration import Concentration

class TaskB(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()

        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.Ny = 1
        self.Np_list = np.arange(1000, 100000, 10000)

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

                self.substance[sub_type] = self.euler(self.substance[sub_type], velocity=0, array_size=len(self.substance[sub_type]))

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

        file = 'data_file/reference_solution_1D.dat'
        self.ref_sol= self.extract_data(file)
        self.figure, self.axes = plt.subplots()

        plot_dict = {'marker':["-bo", "-go", "-co"], 
                     'label':['Run 1', 'Run 2', 'Run 3'], 
                    'color':['blue', 'green', 'cyan']}
        plot_test = []

        if self.plot_1D == True:

            for i, run in enumerate(plot_dict['label']):

                start  = time.process_time()

                self.substance = {"sub_1": [], "sub_2": []}

                # Here you can choose to switch between task A and task B initial state
                self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state(self.Np)
                #print(len(self.substance["sub_1"]))
    
                self.run_simulation()

                concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

                x_grid = np.linspace(-1,1,self.Nx)

                concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)

                if i == 0:
                    self.axes.plot(*zip(*self.ref_sol), color="red", label='Reference Solution')
                
                self.axes.plot(*zip(*concentration_list),plot_dict['marker'][i], color=plot_dict['color'][i], markersize=3, label=run)
                self.axes.legend()

                self.axes.set_title('1D Diffusion Problem')
                self.axes.set_xlabel('x')
                self.axes.set_ylabel('Concentration')

                print("[INFO] Simulation status : Success")
                print("[INFO] The time taken to complete the simulation is {time}".format(time=(time.process_time() - start)))

            plt.show()

        if self.rmse_plot == True:
            
            for n_particles in self.Np_list:
                start  = time.process_time()

                self.substance = {"sub_1": [], "sub_2": []}

                self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state(n_particles)

                self.run_simulation()

                concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

                x_grid = np.linspace(-1,1,self.Nx)

                concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)

                observed_data = np.array(*[concentration_list])
                reference_solution = np.array(*[self.ref_sol])

                actual_concentration = observed_data[:,1]
                predicted_concentration = np.interp(observed_data[:,0], reference_solution[:,0], reference_solution[:,1])

                RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)

                print("The RMSE value with time step {num} is {value}".format(num=n_particles, value=RMSE))

                plot_test.append((n_particles, RMSE))

            plt.yscale('log')
            plt.xscale('log')
            plt.xlim([1e3, 1e6])
            plt.ylim([1e-3, 1])
            plt.title('RMSE vs Number of particles plot')
            plt.xlabel('Number of particles')
            plt.ylabel('RMSE')

            plt.scatter(*zip(*plot_test))

            plt.show()