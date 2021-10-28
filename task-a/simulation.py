import matplotlib.pyplot as plt
import seaborn as sns

from simulation_math import SimulationMath
from initial_state import InitialState
from globals import Globals
from concentration import Concentration

class TaskA(InitialState,SimulationMath,Concentration):

    def __init__(self):
        super().__init__()
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.figure, self.axes = plt.subplots()

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
        

        # Run the simulation until time ends
        while self.time < self.tEnd:

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
            print("[INFO] Time: ", self.time)

    def plot_condition(self,x,y,color,row = 0, col = 0):

        if row == 0 and col == 0:
            self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
            self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
            self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
            self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
            self.axes.scatter(x,y, s=self.size, c=color)
            

    def plot_solution(self, plot_2D=True):

        if plot_2D:
            for i, sub_type in enumerate(self.substance_list):

                color = None 
                print("Plotting for ", sub_type)

                for j, coordinate in enumerate(self.substance[sub_type]):

                    if sub_type == "sub_1":
                        color = "red"
                    else:
                        color = "blue"

                    x, y = coordinate[0], coordinate[1]

                    self.plot_condition(x,y, color)
        else:
            pass

    def concentration_plot(self, grid):
        print("[INFO] Creating concentration plot...")
        sns.heatmap(grid, cmap='RdBu')

    def main(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()
        self.run_simulation()

        self.plot_solution()
        plt.show()
        plt.savefig('diagram/plot_solution.png')

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])
        
        print(concentration_grid)
        self.concentration_plot(concentration_grid)
        plt.savefig('diagram/concentration_plot.png')
        plt.show()
        print("[INFO] Simulation status : Success")
        

test = TaskA()

test.main()


