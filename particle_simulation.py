import numpy as np
import matplotlib.pyplot as plt

class InitialState:
    
    def __init__(self):

        # Read google docs for naming convention
        self.sub_1 = []
        self.sub_2 = []
        self.Np = 1000
        self.h = 0.1
        self.time = 0.0
        self.tEnd = 0.3
        self.D = 0.1
        self.lang = np.random.normal(loc=0, scale=1, size=self.Np)
        self.figure, self.axes = plt.subplots(nrows=2, ncols=2)
        self.circle = plt.Circle((0,0), 1, alpha=0.5)
        self.circle1 = plt.Circle((0,0), 1, alpha=0.5)

    # Calculate the next position of the particle using euler's method
    def euler(self,a,i):
        return a + 2*np.sqrt(2*self.D) * np.sqrt(self.h) * self.lang[i]

    # Creates the initial state
    def taskA_initial_state(self):

        plt.xlim([-10,10])
        plt.ylim([-10,10])

        #x = np.random.normal(loc=0, scale=1, size=self.data_len)
        #y = np.random.normal(loc=0, scale=1, size=self.data_len)
        x = np.random.uniform(low=0,high=3,size=self.Np)
        y = np.random.uniform(low=0,high=3,size=self.Np)

        isInside = np.sqrt(x**2 + y**2) <= 1
        isOutside = np.sqrt(x**2 + y**2) > 1

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if x[i] ** 2 + y[i]**2 <= 1:
                self.sub_1.append((x[i], y[i]))

            # Vice versa
            else:
                self.sub_2.append((x[i], y[i]))

        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(x[~isInside], y[~isInside],s=5, c="blue")
        self.axes[0,0].scatter(x[isInside], y[isInside],s=5, c="red")
        #self.axes[0,0].add_patch(self.circle)

        self.figure.tight_layout()
        

        self.next_step()

        plt.show()

    def taskB_initial_state(self):

        x = np.random.uniform(low=0,high=2,size=self.Np)
        y = np.random.uniform(low=0,high=2,size=self.Np)

        toTheLeft = x <= 1

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if x[i] <= 1:
                self.sub_1.append((x[i], y[i]))

            # Vice versa
            else:
                self.sub_2.append((x[i], y[i]))

        # Conditional statement to assign the position of the particle in the grid
        self.axes[0,0].scatter(x[toTheLeft], y[toTheLeft],s=5, c="red")
        self.axes[0,0].scatter(x[~toTheLeft], y[~toTheLeft],s=5, c="blue")
    
        self.figure.tight_layout()
    
        self.next_step()

        plt.show()


    def next_step(self):

        # Check if whether the time has reached to an end
        if self.time != self.tEnd:
            
            # Here, we calculate the next position of each particle in further time step, h
            for i, particle in enumerate(self.sub_1):
                
                x, y = particle[0], particle[1]
                next_pos_x = self.euler(x,i)
                next_pos_y = self.euler(y,i)

                # Reassign the current particle from substance 1 (in this case), to a new position
                self.sub_1[i] = (next_pos_x, next_pos_y)
            
            # Same thing as above
            for i, particle in enumerate(self.sub_2):
                
                x, y = particle[0], particle[1]
                next_pos_x = self.euler(x,i)
                next_pos_y = self.euler(y,i)

                self.sub_2[i] = (next_pos_x, next_pos_y)

            # Plots the new coordinate of substance 1 and substance 2
            self.plot(self.sub_1)
            self.plot(self.sub_2)

            # Increment the time
            self.time += 0.1

    def plot(self, particle_list):

        if particle_list == self.sub_1:
            color = "red"

        elif particle_list == self.sub_2:
            color="blue"

        for i, particle in enumerate(particle_list):
            self.axes[0,1].scatter(particle_list[i][0], particle_list[i][1], s=5, c=color)



state = InitialState()
state.taskB_initial_state()







        


    


    

