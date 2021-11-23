import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time
from scipy.spatial import cKDTree

from simulation_math import SimulationMath

class TaskB(SimulationMath):

    def __init__(self):
        super().__init__()

        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        # Sets some variables by default
        self.Ny = 1
        self.tEnd = 0.2

        # Creates a list of data for the use of our RMSE plots
        self.Np_list = np.arange(1000,200000,10000)
        self.time_step_list = np.linspace(0.1,0.0001,20)

        

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
        
        steps = int(self.tEnd / time_step)

        # Run the simulation until time ends
        for step in range(steps):
        
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

    # Plots our rmse analysis
    def plot_rmse_analysis(self,axes,xlim,title,xlabel,ylabel,observed_data,fitted_data,label,
                            ylim=None,diff_nparticles=False,diff_timestep=False):

        axes.set_xscale('log')
        axes.set_yscale('log')
        axes.set_xlim(xlim)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_title(title)
        axes.scatter(*zip(*observed_data))
        axes.plot(*zip(*fitted_data), color='red',linestyle='dashed', label=label)
        axes.legend()
        
        if diff_nparticles:
            pass
        if diff_timestep:
            axes.set_ylim(ylim)

    def main(self):

        file = 'reference_solution_1D.dat'
        self.ref_sol= self.extract_data(file)
        

        plot_dict = {'marker':["-bo", "-go", "-co"], 
                     'label':['Run 1', 'Run 2', 'Run 3'], 
                     'color':['blue', 'green', 'cyan']}
        plot_test = []


        self.figure, self.axes = plt.subplots()

        # For our main simulation for task B
        # PLots the 1D plot
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
            
            self.axes.plot(*zip(*concentration_list),plot_dict['marker'][i], color=plot_dict['color'][i], markersize=3, label='Run 1')
            self.axes.legend()

            self.axes.set_title('1D Diffusion Problem for {num1} particles \n with time step {time}'.format(num1=self.Np, time=self.h))
            self.axes.set_xlabel('x')
            self.axes.set_ylabel('Concentration')

            print("[INFO] Run {num} Simulation status : Success".format(num=(i+1)))
            print("[INFO] The time taken to complete the simulation for Run {num} is {time}".format(num=(i+1),time=round((time.process_time() - start), 2)))

        # If user wants to see the RMSE plot, they can set this as true in the globals.py
        if self.rmse_plot:

            rmse_figure, rmse_axes= plt.subplots(1,2,figsize=(9,9))
            rmse_figure.set_size_inches(13,13)
            
            # The number of repitions for our RMSE plot for each element
            n_run = 5
            
            rmse_num_particles = []
            rmse_time_step = []

            # Runs the RMSE calculation and plots for RMSE against Number of particles
            for n_particles in self.Np_list:

                start  = time.process_time()
                
                rmse_average = []

                for i in range(n_run):
                    
                    # Get the list of RMSE values for the current element
                    rmse_average = self.calculate_rmse(rmse_average, n_particles, time_step=self.h, calc_particles=True)

                # Change the list to an array
                rmse_average = np.array(rmse_average)

                # Find the average RMSE
                rmse_average = np.mean(rmse_average, axis=0)

                rmse_num_particles.append((rmse_average[0], rmse_average[1]))

                print("[INFO] The RMSE value with n_particles {num} is {value}".format(num=n_particles, value=round(rmse_average[1], 4)))

            title = 'RMSE against Number of particles for h={num}'.format(num=self.h)

            # Perform RMSE analysis and find the fitted curve coefficient value
            coefficient, rmse_nparticles_analysis, min, max = self.rmse_analysis(rmse_num_particles)

            label = '{a} * Np ^ ({b})'.format(a=round(coefficient[0],4), b=round(-coefficient[1],4))

            # Plots our rmse analysis
            self.plot_rmse_analysis(axes=rmse_axes[0],xlim=[self.Np_list[0]- 100,self.Np_list[-1] + 100], xlabel='Number of particles', ylabel='RMSE',label=label,
                                    title=title,observed_data=rmse_num_particles, fitted_data=rmse_nparticles_analysis, diff_nparticles=True)
            
            # Runs the RMSE calculation and plots for RMSE against time steps
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

            coefficient, rmse_time_step_analysis, min, max = self.rmse_analysis(rmse_time_step)

            label = '{a} * h ^ ({b})'.format(a=round(coefficient[0],4), b=round(-coefficient[1],4))

            self.plot_rmse_analysis(axes=rmse_axes[1],xlim=[1e-5,1],ylim=[min, max],title=title,xlabel='Time Step (s)',ylabel='RMSE',label=label,
                                    observed_data=rmse_time_step, fitted_data=rmse_time_step_analysis, diff_timestep=True)

        plt.show()
