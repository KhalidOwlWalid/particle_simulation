import numpy as np

from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit

from initial_state import InitialState
from concentration import Concentration

"""
This file is implements the mathematics and physics related to the fluid simulation
"""

class SimulationMath(InitialState, Concentration):

    def __init__(self):
        super().__init__()

    # Use to read data from .dat file
    def read_data_file(self, file, *args):
        return [np.loadtxt(file, usecols=tuple(c)) for c in args]
    
    # Use to read data from .dat file
    def extract_data(self, file):

        data = []

        n_line = 0
            
        if file == "reference_solution_1D.dat":

            for line in open(file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    data.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=file))

        return data

    # Generate an array of random normal distribution
    def generate_random_number(self, array_size):
        return np.random.normal(0,1, array_size)

    # Calculate particle's next position
    def euler(self, coordinate, velocity, array_size, time_step):
        
        # This causes the grid to be moved to 
        random = self.generate_random_number(array_size)

        return coordinate + velocity * time_step + np.sqrt(2 * self.D) * np.sqrt(time_step) * random

    # Calculate our RMSE value for different number of particles and time steps
    def calculate_rmse(self,rmse_average_list, n_particles, time_step, calc_particles=False, calc_time_step=False):
        
        x_grid = np.linspace(-1,1,self.Nx)

        self.substance = {"sub_1": [], "sub_2": []}

        self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state(n_particles)

        # Run the simulation for the given time step
        self.run_simulation(time_step)

        # Calculate the concentration of each grid
        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        # Assign x coordinate with their own respective concentration
        concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)


        observed_data = np.array(*[concentration_list])
        reference_solution = np.array(*[self.ref_sol])

        # Interpoolate the predicted concentration for the actual concentration
        actual_concentration = observed_data[:,1]
        predicted_concentration = np.interp(observed_data[:,0], reference_solution[:,0], reference_solution[:,1])

        # Return a list of tuples for our RMSE 
        if calc_particles:
            RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)
            rmse_average_list.append((n_particles, RMSE))
        if calc_time_step:
            RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)
            rmse_average_list.append((time_step, RMSE))
            

        return rmse_average_list

    # Perform rmse analysis
    def rmse_analysis(self,rmse_data):
        
        # Change the form of our rmse data to an array
        rmse_data = np.array(rmse_data)

        # Find the best fitted curve for our analysis
        x = rmse_data[:,0]
        y = rmse_data[:,1]
        popt, pcov = curve_fit(lambda fx,a,b: a*fx**-b,  x,  y)
        power_y = popt[0]*x**-popt[1]
        
        rmse_list = list(zip(x,power_y))

        rmse_array = np.array(rmse_list)

        min = np.min(rmse_array[:,1])
        max = np.max(rmse_array[:,1])

        return popt, rmse_list, min, max

