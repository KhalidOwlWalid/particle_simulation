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

class TaskB(InitialState,SimulationMath,Concentration):

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

    def calculate_rmse(self,rmse_average_list, n_particles, time_step, calc_particles=False, calc_time_step=False):
        
        x_grid = np.linspace(-1,1,self.Nx)

        self.substance = {"sub_1": [], "sub_2": []}

        self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state(n_particles)

        self.run_simulation(time_step)

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        concentration_list = self.assign_concentration(self.substance["sub_1"],self.substance["sub_2"], concentration_grid[0], x_grid)

        observed_data = np.array(*[concentration_list])
        reference_solution = np.array(*[self.ref_sol])

        actual_concentration = observed_data[:,1]
        predicted_concentration = np.interp(observed_data[:,0], reference_solution[:,0], reference_solution[:,1])

        RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)


        if calc_particles == True:
            rmse_average_list.append((n_particles, RMSE))

        if calc_time_step == True:
            rmse_average_list.append((time_step, RMSE))

        return rmse_average_list

    def plot_rmse_analysis(self,axes,xlim,title,xlabel,ylabel,observed_data,fitted_data,label,
                            ylim=None,diff_nparticles=False,diff_timestep=False):

        axes.set_xscale('log')
        axes.set_xlim(xlim)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_title(title)
        observed_data_plot = axes.scatter(*zip(*observed_data))
        fitted_data_plot, = axes.plot(*zip(*fitted_data), color='red',linestyle='dashed')
        fitted_data_plot.set_label(label)
        axes.legend()

        if diff_nparticles:
            axes.set_yscale('log')
            axes.legend
        if diff_timestep:
            axes.set_ylim(ylim)

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
    
                self.run_simulation(time_step=self.h)

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
                print("[INFO] The time taken to complete the simulation is {time}".format(time=round((time.process_time() - start), 2)))

            plt.show()

        if self.rmse_plot == True:

            rmse_figure, rmse_axes= plt.subplots(1,2,figsize=(9,9))
            rmse_figure.set_size_inches(13,13)
            
            n_run = 1
            
            rmse_num_particles = []
            rmse_time_step = []

            # TODO: Create for different time step!
            for n_particles in self.Np_list:

                start  = time.process_time()
                
                rmse_average = []

                for i in range(n_run):
                    
                    rmse_average = self.calculate_rmse(rmse_average, n_particles, time_step=self.h, calc_particles=True)

                rmse_average = np.array(rmse_average)

                rmse_average = np.mean(rmse_average, axis=0)

                rmse_num_particles.append((rmse_average[0], rmse_average[1]))

                print("[INFO] The RMSE value with n_particles {num} is {value}".format(num=n_particles, value=round(rmse_average[1], 4)))

            title = 'RMSE against Number of particles for h={num}'.format(num=self.h)

            coefficient, rmse_nparticles_analysis = self.rmse_analysis(rmse_num_particles,diff_particles=True)

            fitted_eqn_particles = '{a}*Np^({b})'.format(a=round(coefficient[0],3), b=round(-coefficient[1],3))

            self.plot_rmse_analysis(axes=rmse_axes[0],xlim=[self.lower_Np - 100,self.higher_Np + 100], xlabel='Number of particles', ylabel='RMSE',title=title,label=fitted_eqn_particles,
                                    observed_data=rmse_num_particles, fitted_data=rmse_nparticles_analysis, diff_nparticles=True)

            
            for time_step in self.time_step_list:

                start  = time.process_time()
                
                rmse_average = []

                for i in range(n_run):
                    
                    rmse_average = self.calculate_rmse(rmse_average, n_particles=self.Np, time_step=time_step, calc_time_step=True)

                rmse_average = np.array(rmse_average)

                rmse_average = np.mean(rmse_average, axis=0)

                rmse_time_step.append((rmse_average[0], rmse_average[1]))

                print("[INFO] The RMSE value with time step {num} is {value}".format(num=round(time_step,4), value=round(rmse_average[1], 4)))

            title = 'RMSE against Time Step for N particles ={num}'.format(num=self.Np)

            coefficient, rmse_time_step_analysis = self.rmse_analysis(rmse_time_step,diff_time_step=True)

            fitted_time_equation = '{a} * ln(h) + {b}'.format(a=round(coefficient[0],3), b=round(coefficient[1],3))

            self.plot_rmse_analysis(axes=rmse_axes[1],xlim=[1e-4,1],ylim=[2e-3, 0.5],title=title,xlabel='Time Step (s)',ylabel='RMSE',label=fitted_time_equation,
                                    observed_data=rmse_time_step, fitted_data=rmse_time_step_analysis, diff_timestep=True)

            plt.show()

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

        return popt, list(zip(x,power_y))