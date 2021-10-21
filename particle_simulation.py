import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class InitialState:
    
    def __init__(self):

        # Important constant 
        self.sub_1 = []
        self.sub_2 = []
        self.Np = 1000
        self.h = 0.1
        self.time = 0.0
        self.tEnd = 0.4
        self.D = 0.1i
        self.lower_lim = -1
        self.upper_lim = 1
        self.Nx = 10
        self.Ny = 10
        
        # Figure used in graph
        self.figure, self.axes = plt.subplots(nrows=2, ncols=2)
        self.figure1, self.axes1 = plt.subplots()
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

        #self.calculate_concentration()

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

        return next_pos_x, next_pos_y

    def calculation(self,particles, time_step):

        for i, particle in enumerate(particles):

            lang = np.random.normal(loc=0, scale=1, size=2)
            
            x, y = particle[0], particle[1]

            # Euler's equation using lambda function
            euler = lambda coordinate, random : coordinate + 2 * np.sqrt(2 * self.D) * np.sqrt(time_step) * random
            next_pos_x = euler(x, lang[0])
            next_pos_y = euler(y, lang[1])

            # Creates a "wall" to avoid the particles from moving to places it shouldnt
            next_pos_x, next_pos_y = self.boundary_conditions(next_pos_x, next_pos_y)

            # Reassign the current particle from substance 1 (in this case), to a new position
            particles[i] = (next_pos_x, next_pos_y)


    def estimate_next_position(self):

        for subplot in self.subplots:

            row, col = self.subplot_position[subplot][0][0],self.subplot_position[subplot][0][1]

            self.time += 0.1

            for particle_type in self.type:
                self.calculation(particle_type, self.h)
                self.plot(particle_type, row, col)

    def plot(self, particle_list,row,col):

        if particle_list == self.sub_1:
            color = "red"

        elif particle_list == self.sub_2:
            color="blue"

        for i, particle in enumerate(particle_list):
            self.axes[row,col].set_xbound(lower=self.lower_lim, upper=self.upper_lim)
            self.axes[row,col].set_xlim(xmin=self.lower_lim, xmax=self.upper_lim)
            self.axes[row,col].set_ybound(lower=self.lower_lim, upper=self.upper_lim)
            self.axes[row,col].set_ylim(ymin=self.lower_lim, ymax=self.upper_lim)
            self.axes[row,col].scatter(particle_list[i][0], particle_list[i][1], s=self.size, c=color)

    def call_out_taskA(self):
        self.taskA_initial_state()
        self.estimate_next_position()
        self.figure.savefig('diagram/task_A.png')
        plt.show()

    def call_out_taskB(self):
        self.taskB_initial_state()
        self.estimate_next_position()
        self.figure.savefig('diagram/task_B.png')
        plt.show()

class ConcentrationPlot(InitialState):

    def __init__(self):
        super().__init__()

        self.x_grid = np.linspace(-1,1,self.Nx)
        self.y_grid = np.linspace(-1,1,self.Ny)

        self.column = self.Nx
        self.row = self.Ny

    def single_plot(self):

        self.taskA_initial_state()

        for i in range(4):
            for type in self.type:
                self.calculation(type, self.h)

        for particle_list in self.type:

            if particle_list == self.sub_1:
                color = "red"

            elif particle_list == self.sub_2:
                color="blue"


            for i, particle in enumerate(particle_list):
                self.axes1.set_xbound(lower=self.lower_lim, upper=self.upper_lim)
                self.axes1.set_xlim(xmin=self.lower_lim, xmax=self.upper_lim)
                self.axes1.set_ybound(lower=self.lower_lim, upper=self.upper_lim)
                self.axes1.set_ylim(ymin=self.lower_lim, ymax=self.upper_lim)
                self.axes1.scatter(particle[0], particle[1], s=self.size, c=color)

        self.axes1.set_yticks(np.linspace(-1,1,self.Ny), minor=True)
        self.axes1.yaxis.grid(True,linestyle='--', which='minor')
        self.axes1.set_xticks(np.linspace(-1,1,self.Nx), minor=True)
        self.axes1.xaxis.grid(True, linestyle='--', which='minor')


    def calculate_concentration(self):
        
        # Populate a "grid" with zeros
        grid_list = []

        grid_position = lambda x, y, i, j: x > self.x_grid[i] and x < self.x_grid[i+1] and y > self.y_grid[j] and y < self.y_grid[j+1]

        for i in range(self.Nx - 1):
            grid_list.append([0 for j in range(self.Ny - 1)])

        for i in range(len(self.x_grid)):
            for j in range(len(self.y_grid)):

                n_sub_1 = 0
                
                for particle in self.sub_1:
                    # Check corner
                    if grid_position(particle[0], particle[1], i, j):
                        n_sub_1 += 1

                for particle in self.sub_2:
                    
                    # Check corner
                    if grid_position(particle[0], particle[1], i, j):
                        grid_list[i][j] += 1

                try:
                    grid_list[i][j] = grid_list[i][j]/(grid_list[i][j] + n_sub_1)
                except:
                    print("Index out of bound")
        
        grid_list = np.array(grid_list)
        plt.imshow(grid_list, norm=plt.Normalize(0,1), cmap='Wistia')
        #sns.heatmap(grid_list, cmap='GnBu')
        print(grid_list)

        self.figure1.savefig('diagram/grid_plot.png')
        plt.show()

    def heatmap2d(self,arr: np.ndarray):
        plt.imshow(arr, cmap='viridis')
        plt.colorbar()



#concentration_plot = ConcentrationPlot()
initial_state = InitialState()
initial_state.call_out_taskA()
#print(concentration_plot.Np)
#concentration_plot.single_plot()
#concentration_plot.calculate_concentration()


#concentration_plot.calculate_concentration()
plt.show()
