##################
# USER INTERFACE #
##################

import numpy as np

class Globals:

    def __init__(self):

        ########
        # Task #
        ########
        """
        Please use capital letters!
        OPTION : A, B, D, E
        """
        self.task_type = {'A':0, 'B':1, 'D':2}
        self.task = 'B'
        
        ####################
        # Initial position #
        ####################
        """
        self.offset_x || self.offset_y = Position the particle anywhere inside the domain
        """
        self.radius = 0.1
        self.offset_x = 0.4
        self.offset_y = 0.4
        
        ##########
        # Domain #
        ##########
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        #######################
        # Number of particles #
        #######################
        """
        Set any number of particles you want
        NOTE : Generally, it will take 10 minutes for 150000 particles
        """
        self.Np = 15000

        ###############
        # Diffusivity #
        ###############
        self.D = 0.1
        
        ############
        # Velocity #
        ############
        """
        True : Include the velocity inside the calculation 
        False : No velocity
        """
        self.include_velocity = False

        ###################
        # Time conditions #
        ###################
        """
        self.h = Time step
        self.tEnd = Time End
        """
        self.h = 0.001
        self.tEnd = 0.2
        
        #########
        # Grids #
        #########
        """
        Choose your desired grid size
        NOTE : For Task B, self.Ny is set to 1 by default
        """
        self.grid_size = 64
        self.Nx = self.grid_size
        self.Ny = self.grid_size

        # For size of scatter plots, increase the value to get bigger scatter size
        self.size = 10
        
        #############################
        # Only for 1D plot (Task B) #
        #############################
        """
        True : Gives 1D plot of concentration vs x coordinate
        False : Does not plot 1D plot
        """
        self.plot_1D = False

        """
        True : Plots the RMSE vs parameter (number of particles and different time step)
        False : No plot
        """
        self.rmse_plot = True

        self.lower_Np = 1000
        self.higher_Np = 160000
        
        self.lower_h = 0.001
        self.higher_h = 0.1
        
        #########
        # Debug #
        #########
        """"
        If you wish to see any extra information in the terminal, set self.debug to True.
        """
        self.debug = False

        