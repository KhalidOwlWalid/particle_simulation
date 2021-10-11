import numpy as np
import matplotlib.pyplot as plt

class InitialState:
    
    def __init__(self):

        # Read google docs for naming convention
        self.sub_1 = []
        self.sub_2 = []
        self.Np = 5000
        self.h = 0.1
        self.time = 0.0
        self.tEnd = 0.4
        self.D = 0.1
        
        # Figure used in graph
        self.figure, self.axes = plt.subplots(nrows=2, ncols=2)
        self.circle = plt.Circle((0,0), 1, alpha=0.5)
        self.circle1 = plt.Circle((0,0), 1, alpha=0.5)

        # Generates uniformly distributed data
        self.x = np.random.uniform(low=-1,high=1,size=self.Np)
        self.y = np.random.uniform(low=-1,high=1,size=self.Np)

        self.lang = np.random.normal(loc=0, scale=1, size=self.Np)

        self.subplot_position = {"(0,1)":[(0,1)],
                                 "(1,0)":[(1,0)],
                                 "(1,1)":[(1,1)]
                                 }

        self.subplots = ["(0,1)","(1,0)","(1,1)"]

    # Calculate the next position of the particle using euler's method
    def euler(self,coordinate,i):
        return coordinate + 2*np.sqrt(2*self.D) * np.sqrt(self.h) * self.lang[i]

    # Creates the initial state for task A
    def taskA_initial_state(self):
        
        isInside = np.sqrt(self.x**2 + self.y**2) <= 1

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if self.x[i] ** 2 + self.y[i]**2 <= 1:
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(self.x[~isInside], self.y[~isInside],s=5, c="blue")
        self.axes[0,0].scatter(self.x[isInside], self.y[isInside],s=5, c="red")
        #self.axes[0,0].add_patch(self.circle)

        self.figure.tight_layout()

    # Creates the initial state for task B
    def taskB_initial_state(self):

        toTheLeft = self.x <= 0

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if self.x[i] <= 0:
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(self.x[toTheLeft], self.y[toTheLeft],s=5, c="red")
        self.axes[0,0].scatter(self.x[~toTheLeft], self.y[~toTheLeft],s=5, c="blue")

        self.figure.tight_layout()

    def estimate_next_position(self):

        for i, subplot in enumerate(self.subplots):

            row, col = self.subplot_position[subplot][0][0],self.subplot_position[subplot][0][1]

            self.time += 0.1

            # Here, we calculate the next position of each particle in further time step, h
            for i, particle in enumerate(self.sub_1):
                
                x, y = particle[0], particle[1]
                next_pos_x = self.euler(x,i)
                next_pos_y = self.euler(y,i)

                # Reassign the current particle from substance 1 (in this case), to a new position
                self.sub_1[i] = (next_pos_x, next_pos_y)
     
            # Same thing as above
            for i, particle in enumerate(self.sub_2):
                
                # Add a comment
                x, y = particle[0], particle[1]
                next_pos_x = self.euler(x,i)
                next_pos_y = self.euler(y,i)

                self.sub_2[i] = (next_pos_x, next_pos_y)

            plt.xlim(-1,1)
            plt.ylim(-1,1)
            # Plots the new coordinate of substance 1 and substance 2
            self.plot(self.sub_1, row, col)
            self.plot(self.sub_2, row, col)

    def plot(self, particle_list,row,col):

        if particle_list == self.sub_1:
            color = "red"

        elif particle_list == self.sub_2:
            color="blue"

        for i, particle in enumerate(particle_list):
            self.axes[row,col].scatter(particle_list[i][0], particle_list[i][1], s=5, c=color)

    def main(self):
        self.taskB_initial_state()
        self.estimate_next_position()
        #self.estimate_next_position()
        #self.estimate_next_position()
        plt.show()

# Test
state = InitialState()
state.main()







        


    


    

