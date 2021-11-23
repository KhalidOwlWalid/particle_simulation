# Here is where the all the backends for the simulation happens
import numpy as np

from globals import Globals

"""
This file is responsible in handling the initial state of our simulations

"""


class InitialState(Globals):
    """
    This class is responsible in constructing the intial state of our simulations

    taskA_initial_state : Will add a circle to our plot of specified radius and offsets by the user
    taskB_initial_state : Adds a rectangle that is seperated by the x = 0 axis.
    """

    def __init__(self):
        
        super().__init__()

        self.time = 0.0

        # Initialized the x and y coordinate of our particle as a random uniform distribution
        self.x = np.random.uniform(low=self.xMin, high=self.xMax, size=self.Np)
        self.y = np.random.uniform(low=self.yMin, high=self.yMax, size=self.Np)

        self.sub_1 = []
        self.sub_2 = []
        
    def taskA_initial_state(self):
        """
        Initialize task A initial state
        """

        # Conditions to check if particle is inside or outside the circle
        isInside = lambda x_coordinate, y_coordinate, radius : (x_coordinate - self.offset_x) ** 2 + (y_coordinate - self.offset_y) ** 2 <= self.radius ** 2

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if isInside(self.x[i], self.y[i], self.radius):
                self.sub_1.append([self.x[i], self.y[i]])

            # Vice versa
            else:
                self.sub_2.append([self.x[i], self.y[i]])

        # Return the list in an array form
        return np.array(self.sub_1), np.array(self.sub_2)
    
    def taskB_initial_state(self, Np):
        """
        Initialize Task B initial state
        """
        toTheLeft = lambda coordinate : coordinate <= 0

        self.sub_1 = []
        self.sub_2 = []
        self.x = np.random.uniform(low=-1, high=1, size=Np)

        # Divide the particles into their substance type
        for i in range(Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if toTheLeft(self.x[i]): 
                self.sub_1.append(self.x[i])

            # Vice versa
            else:
                self.sub_2.append(self.x[i])

        return np.array(self.sub_1), np.array(self.sub_2)

