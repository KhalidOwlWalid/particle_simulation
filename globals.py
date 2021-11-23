##################
# USER INTERFACE #
##################

"""
This file is where the user will input their desired value. 
Follow the instructions that is included for each variable for more clarity.

If you are having trouble, trying to understand how the simulation generally works, 
feel free to visit https://github.com/KhalidOwlWalid/particle_simulation for more info
"""
class Globals:

    def __init__(self):

        ########
        # Task #
        ########
        """
        This is where you will set your task.

        Please use capital letters!
        OPTIONS:
            A
            B
            D
            E
        """
        self.task_type = {'A':0, 'B':1, 'D':2, 'E':3}

        # Change task here
        self.task = 'A'

        #######################
        # Number of particles #
        #######################
        """
        Set number of particles.
        NOTE : Generally, it will take 30 seconds for 150000 particles for a time step of 0.01s
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

        # Change time step here
        self.h = 0.01

        # Change the time length of your simulation
        self.tEnd = 0.2

        #########
        # Grids #
        #########
        """
        Choose your desired grid size
        NOTE : For Task B, self.Ny is set to 1 by default
        """

        # Change your grid size here
        self.grid_size = 100

        # Our grids need to be symmetrical, but for task B, Ny is set to 1 by default
        self.Nx = self.grid_size
        self.Ny = self.grid_size
        
        ############################
        # Initial position (Task A)#
        ############################
        """
        self.offset_x || self.offset_y = Position the circle anywhere from the centre
        """

        # Set your circle radius here
        self.radius = 0.2

        # Set your circle offsets from the origin here
        self.offset_x = 0.4
        self.offset_y = 0.4
        
        ##########
        # Domain #
        ##########
        """
        self.xMax || self.xMin = Sets the boundary condition for the x-axis
        self.yMax || self.yMin = Sets the boundary condition for the y-axis
        """

        # Set your boundary conditions here
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        ########################
        # Diffusivity (Task A) #
        ########################
        """
        self.D = Diffusivity coefficient

        Input higher values to see a more randomized particle movement
        """

        # Set your diffusivity coefficient here
        self.D = 0.1
        
        ####################
        # Velocity (Task A)#
        ####################
        """
        self.include_velocity = As the name suggest, you can choose either to include the velocity in your simulation or not

        OPTIONS:
            True : Include the velocity inside the calculation 
            False : No velocity

        NOTE: 
        - Task B sets this variable as False by default
        - Task D sets this variable as True by default
        """

        # Do you want your simulation to include velocity?
        self.include_velocity = True
        
        ############################
        # Plot settings (OPTIONAL) #
        ############################
        """
        self.plot_2D_particle = You can choose if you want to visualize the plot as a scatter plot (Useful for debugging purpose)
        self.size = Sets the size of the point for our scatter plot
        """
        
        # Do you want to visualize the scatter plot of our simulation?
        self.plot_2D_particle = False
        self.size = 5
        
        #############################
        # Only for 1D plot (Task B) #
        #############################

        """
        self.rmse_plot = You can choose if you want to plot the RMSE against parameter (Np and h) plot

        OPTIONS:
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
        self.debug = False

    # Gets the task input by the user
    def getTask(self):
        return self.task_type[self.task]  

        