import numpy as np
import matplotlib.pyplot as plt
import time

class InitialState:
    
    def __init__(self):

        # Important constant 
        self.sub_1 = []
        self.sub_2 = []
        self.Np = 30000
        self.h = 0.1
        self.time = 0.0
        self.tEnd = 0.4
        self.D = 0.1
        self.lower_lim = -1
        self.upper_lim = 1
        self.Nx = 64
        self.Ny = 64
        
        # Figure used in graph
        self.figure, self.axes = plt.subplots(nrows=2, ncols=2)
        self.circle = plt.Circle((0,0), 1, alpha=0.5)
        self.circle1 = plt.Circle((0,0), 1, alpha=0.5)
        self.size = 2

        # Generates uniformly distributed data
        self.x = np.random.uniform(low=-1,high=1,size=self.Np)
        self.y = np.random.uniform(low=-1,high=1,size=self.Np)

        # For plots
        self.subplot_position = {"(0,1)":[(0,1)],
                                 "(1,0)":[(1,0)],
                                 "(1,1)":[(1,1)]
                                 #"(2,0)":[(2,0)],
                                 #"(2,1)":[(2,1)]
                                 }

        self.subplots = ["(0,1)","(1,0)","(1,1)"]
        self.fig = plt.gcf()
        self.fig.set_size_inches(18.5,10.5, forward=True)
        self.type = [self.sub_1, self.sub_2]

    # Creates the initial state for task A
    def taskA_initial_state(self):
        
        isInside = self.x**2 + self.y**2 <= 0.3**2

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if self.x[i]**2 + self.y[i]**2 <= 0.3**2:
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))
                
        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(self.x[~isInside], self.y[~isInside],s=self.size, c="blue")
        self.axes[0,0].scatter(self.x[isInside], self.y[isInside],s=self.size, c="red")

        # Creates a circle patch centred at the origin 
        #self.axes[0,0].add_patch(self.circle)

        self.figure.tight_layout()

    # Creates the initial state for task B
    def taskB_initial_state(self):

        toTheLeft = self.x <= 0

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if self.x[i] <= 0:
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(self.x[toTheLeft], self.y[toTheLeft],s=self.size, c="red")
        self.axes[0,0].scatter(self.x[~toTheLeft], self.y[~toTheLeft],s=self.size, c="blue")

        self.figure.tight_layout()

    # Responsiblle in making sure that the particles are within the boundary limits 
    def boundary_conditions(self, next_pos_x, next_pos_y):

        if next_pos_x > 1:
            distanceFromMax = next_pos_x - 1
            next_pos_x = next_pos_x - 2 * distanceFromMax

        elif next_pos_x < -1:
            distanceFromMax = next_pos_x + 1
            next_pos_x = next_pos_x - 2 * distanceFromMax

        if next_pos_y > 1:
            distanceFromMax = next_pos_y - 1
            next_pos_y = next_pos_y - 2 * distanceFromMax

        elif next_pos_y < -1:
            distanceFromMax = next_pos_y + 1
            next_pos_y = next_pos_y - 2 * distanceFromMax

    def calculation(self,particles, time_step):

        for i, particle in enumerate(particles):

            lang = np.random.normal(loc=0, scale=1, size=2)
            
            x, y = particle[0], particle[1]

            # Euler's equation using lambda function
            euler = lambda coordinate, random : coordinate + 2 * np.sqrt(2 * self.D) * np.sqrt(time_step) * random
            next_pos_x = euler(x, lang[0])
            next_pos_y = euler(y, lang[1])

            # Creates a "wall" to avoid the particles from moving to places it shouldnt
            self.boundary_conditions(next_pos_x, next_pos_y)

            # Reassign the current particle from substance 1 (in this case), to a new position
            particles[i] = (next_pos_x, next_pos_y)

    # As obvious as the name is, this is to calculate the particle's next position at a time step, h
    def estimate_next_position(self):

        # Plots the particles in each subplots 
        for subplot in self.subplots:

            row, col = self.subplot_position[subplot][0][0],self.subplot_position[subplot][0][1]

            self.time += 0.1

            # self.type contains self.sub_1 and self.sub_2 which allows us to access each particle type easily
            for particle_type in self.type:
                self.calculation(particle_type, self.h)
                self.plot(particle_type, row, col)

    # Plots our particle
    def plot(self, particle_list,row,col):

        if particle_list == self.sub_1:
            color = "red"

        elif particle_list == self.sub_2:
            color="blue"

        # Sets some boundary limits to our plot
        for i, particle in enumerate(particle_list):
            self.axes[row,col].set_xbound(lower=self.lower_lim, upper=self.upper_lim)
            self.axes[row,col].set_xlim(xmin=self.lower_lim, xmax=self.upper_lim)
            self.axes[row,col].set_ybound(lower=self.lower_lim, upper=self.upper_lim)
            self.axes[row,col].set_ylim(ymin=self.lower_lim, ymax=self.upper_lim)
            self.axes[row,col].scatter(particle_list[i][0], particle_list[i][1], s=self.size, c=color)

    # This is not important as of now, so you can neglect it at the moment
    # But if you are interested to know what I am trying to do, this function is to be used to create grids so that we could calculate
    # the concentration for each grid
    # Each grid of boxes are defined as shown below depending on the size
    """
    [0,0,0,0]
    [0,0,0,0]
    [0,0,0,0]
    [0,0,0,0]

    """
    # In this case, it is 5 grids of x and 5 grids of y and the 0s represents the boxes
    # Calculation will take place in each boxes and it will then represent a value set between 0 < concentration < 1
    # We will then either use a heatmap or a contour plot to plot accordingly to its concentration value
    def single_plot(self):

        self.taskA_initial_state()

        for i in range(7):
            for type in self.type:
                self.calculation(type, self.h)

        for particle_list in self.type:
            self.plot(particle_list, 0,0)

        self.axes[0,0].set_yticks(np.linspace(-1,1,self.Ny), minor=True)
        self.axes[0,0].yaxis.grid(True, which='minor')
        self.axes[0,0].set_xticks(np.linspace(-1,1,self.Nx), minor=True)
        self.axes[0,0].xaxis.grid(True, which='minor')
        plt.show()

    def call_out_taskA(self):
        self.taskA_initial_state()
        self.estimate_next_position()
        # Saves it in a file name result, by the name task_A.png
        self.figure.savefig('result/task_A.png')
        plt.show()

    def call_out_taskB(self):
        self.taskB_initial_state()
        self.estimate_next_position()
        self.figure.savefig('result/task_B.png')
        plt.show()


state = InitialState()
start_time = time.time()
state.call_out_taskA()
# Calculate the time taken to execute our program
print("--- %s seconds ---" % (time.time() - start_time))
