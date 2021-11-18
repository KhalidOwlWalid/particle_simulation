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

from scipy.optimize import curve_fit

class TaskTest(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()

        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.Ny = 1
        
        self.Np_list = np.arange(self.lower_Np, self.higher_Np, 10000)

        
        self.time_step_list = np.linspace(self.lower_h, self.higher_h, 30)

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
    def run_simulation(self, time_step):
        
        u,v = 0, 0

        # Run the simulation until time ends
        for step in range(self.steps):
        
            for i, sub_type in enumerate(self.substance_list):

                self.substance[sub_type] = self.euler(self.substance[sub_type], velocity=0, array_size=len(self.substance[sub_type]),
                                                      time_step=time_step)

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
                print("[INFO] Plotting for ", sub_type)

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

    def save_to_txt(self,array, filename):

        for element in array: #you wouldn't need to write this since you are already in a loop
            file1 = open(filename,"a") 
            file1.write("{x} {y}\n".format(x=round(element[0], 7), y=element[1])) 
            file1.close()

    def main(self):

        file = 'data_file/reference_solution_1D.dat'
        self.ref_sol= self.extract_data(file)

        rmse_figure, rmse_axes= plt.subplots(1,2,figsize=(9,9))
        rmse_figure.set_size_inches(13,13)
        
        x_grid = np.linspace(-1,1,self.Nx)

        self.substance = {"sub_1": [], "sub_2": []}

        self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state(self.Np)

        self.run_simulation(self.h)

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)

        observed_data = np.array(*[concentration_list])
        reference_solution = np.array(*[self.ref_sol])

        actual_concentration = observed_data[:,1]
        predicted_concentration = np.interp(observed_data[:,0], reference_solution[:,0], reference_solution[:,1])

        RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)


        print("[INFO] The RMSE value with time step {num} is {value}".format(num=round(self.h,4), value=round(RMSE, 4)))

    def rmse_analysis(self,rmse_data,diff_particles=False,diff_time_step=False):

        rmse_data = np.array(rmse_data)

        if diff_particles:
            x = rmse_data[:,0]
            y = rmse_data[:,1]
            popt, pcov = curve_fit(lambda fx,a,b: a*fx**-b,  x,  y)
            power_y = popt[0]*x**-popt[1]

        if diff_time_step:
            x = rmse_data[:,0]
            y = rmse_data[:,1]
            popt, pcov = curve_fit(lambda fx,a,b: a * np.log(fx) + b,  x,  y)
            power_y = popt[0] * np.log(x) + popt[1]

        return list(zip(x,power_y))