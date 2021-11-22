import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors
import numpy as np
import time

from task_a import TaskA

class TaskD(TaskA):

    def __init__(self):
        super().__init__()

        # Initial condition for task D
        self.offset_x = 0.4
        self.offset_y = 0.4
        self.radius = 0.1
        self.D = 0.1
        self.include_velocity = True

    def concentration_plot(self, grid):

        print("[INFO] Creating concentration plot...")

        figure, axes = plt.subplots()

        heatmap = axes.imshow(grid, extent=(self.xMin, self.xMax, self.yMin, self.yMax))

        axes.set_title('Chemical Concentration for time {num} \n with time step {h}'.format(num=self.tEnd, h=self.h))
        axes.set_xlabel('x')
        axes.set_ylabel('y')

        heatmap.set_cmap('brg')
        figure.colorbar(matplotlib.cm.ScalarMappable(cmap='brg'))

    def main_task_D(self):

        start = time.process_time()

        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()

        print("[INFO] Running the simulation...")
        self.run_simulation()

        if self.plot_2D_particle:
            self.plot_solution()

        concentration_grid = self.calculate_concentration(self.substance["sub_1"],self.substance["sub_2"])

        self.concentration_plot(concentration_grid)
        # print(concentration_grid)

        if self.debug:
            print("[DEBUG] The number of particles involved: ", (len(self.substance["sub_1"]) + len(self.substance["sub_2"])))

        print("[INFO] Simulation status : Success")
        print("[INFO] The time taken to complete the simulation is {time}".format(time=round((time.process_time() - start), 2)))

        plt.show()
