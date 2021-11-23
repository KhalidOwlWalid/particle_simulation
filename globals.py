##################
# USER INTERFACE #
##################

class Globals:

    def __init__(self):

        ########
        # Task #
        ########
        """
        Please use capital letters!
        OPTION : A, B, D
        """
        self.task_type = {'A':0, 'B':1, 'D':2}
        self.task = 'D'

        #######################
        # Number of particles #
        #######################
        """
        Set any number of particles you want
        NOTE : Generally, it will take 10 minutes for 150000 particles
        """
        self.Np = 150000

        ###################
        # Time conditions #
        ###################
        """
        self.h = Time step
        self.tEnd = Time End

        By default, task B's tEnd is set to t=0.2
        """

        """
        INFO : For h = 0.001 with 100 grids and 150000 particles, it takes 600 seconds to plot
        """
        self.h = 0.001
        self.tEnd = 0.5

        #########
        # Grids #
        #########
        """
        Choose your desired grid size
        NOTE : For Task B, self.Ny is set to 1 by default
        """
        self.grid_size = 100
        self.Nx = self.grid_size
        self.Ny = self.grid_size
        
        ############################
        # Initial position (Task A)#
        ############################
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
        
        ########################
        # Diffusivity (Task A) #
        ########################
        self.D = 1
        
        ####################
        # Velocity (Task A)#
        ####################
        """
        True : Include the velocity inside the calculation 
        False : No velocity
        """
        self.include_velocity = True
        
        #################
        # Plot settings #
        #################
        # For size of scatter plots, increase the value to get bigger point size
        self.plot_2D_particle = True
        self.size = 5
        
        #############################
        # Only for 1D plot (Task B) #
        #############################
        """
        True : Gives 1D plot of concentration vs x coordinate
        False : Does not plot 1D plot
        """
        self.plot_1D = True

        """
        True : Plots the RMSE vs parameter (number of particles and different time step)
        False : No plot
        """
        self.rmse_plot = False
        
        #########
        # Debug #
        #########
        """"
        If you wish to see any extra information in the terminal, set self.debug to True.
        """
        self.debug = True

    def getTask(self):
        return self.task_type[self.task]  

        