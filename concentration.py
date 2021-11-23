"""
This file handles all the concentration problem. 

calculate_concentration : calculate concentration for both 1D and 2D case. If self.Ny is set to 1, then its a 1D case. Need to improve
assgin_concentration : Assign concentration to each respective particles and this function is meant for task B
calculate_concentration_taskE : Optimized method

"""

import numpy as np

from globals import Globals

class Concentration(Globals):

    def __init__(self):
        super().__init__()

        self.x_grid = np.linspace(-1,1,self.Nx)
        self.y_grid = np.linspace(1,-1,self.Ny)

        self.sub_1 = None
        self.sub_2 = None
        
    def calculate_concentration(self, sub_1, sub_2):
        """
        This function is responsible in calculating the concentration of each grid"

        Args:
            sub_1 = array of coordinate of the substance 1 Particles
            sub_2 = array of coordinate of substance 2 Particles
        """
        
        if self.task != 'B':
            print("[INFO] Calculating concentration... This may take awhile...")
            print("[INFO] Set self.debug = True if you wish to see which grid the programme is currenly calculating")
            
        # Populate a "grid" with zeros
        grid_list = []
        
        self.sub_1 = sub_1
        self.sub_2 = sub_2

        grid_position = lambda x, y, i, j: x > self.x_grid[i] and x < self.x_grid[i+1] and y < self.y_grid[j] and y > self.y_grid[j+1]
        
        # Responsible for handling task B
        if self.Ny == 1:

            grid_list.append([0 for j in range(self.Nx - 1)])

            for n in range(len(self.x_grid) - 1):
                
                # Check if the particle is inside the grid or not
                try:
                    n_sub_2 = 0 
                    for particle in sub_1:
                        if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                            grid_list[0][n] += 1

                    for particle in sub_2:
                        if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                            n_sub_2 += 1

                # Catch unprecedented exception where the loop went out of boundary
                except IndexError:
                    print("[DEBUG] Index out of range which is the {n}th column".format(n=n))

                # Calculate the concentration for the current grid
                try:
                    grid_list[0][n] = grid_list[0][n]/(grid_list[0][n] + n_sub_2)

                # There will be times where our grid does not have any particles, which would cause errors
                except ZeroDivisionError:
                    pass

                except IndexError:
                    print("[WARN] IndexError")
        
        # Responsible in handling task B
        elif Globals().task_type[Globals().task] == 2:
            
            # Create grids of zero of the form Nx x Ny
            for i in range(self.Nx - 1):
                grid_list.append([0 for j in range(self.Ny - 1)])
            
            print("[INFO] Checking each grid for particles...")

            # Loop through each grid and determine if the particle is inside the grid
            for i in range(len(self.x_grid)- 1):
                for j in range(len(self.y_grid) - 1):

                    check_inside_grid_x1 = np.logical_and(sub_1[:,0] > self.x_grid[i], sub_1[:,0] < self.x_grid[i+1])
                    check_inside_grid_y1 = np.logical_and(sub_1[:,1] < self.y_grid[j], sub_1[:,1] > self.y_grid[j+1])
                    grid_sub1_count = np.where(np.logical_and(check_inside_grid_x1, check_inside_grid_y1), 1, 0)
                    unique, particle_count1 = np.unique(grid_sub1_count, return_counts=True)

                    check_inside_grid_x2 = np.logical_and(sub_2[:,0] > self.x_grid[i], sub_2[:,0] < self.x_grid[i+1])
                    check_inside_grid_y2 = np.logical_and(sub_2[:,1] < self.y_grid[j], sub_2[:,1] > self.y_grid[j+1])
                    grid_sub2_count = np.where(np.logical_and(check_inside_grid_x2, check_inside_grid_y2), 1, 0)
                    unique, particle_count2 = np.unique(grid_sub2_count, return_counts=True)
                    
                    # We are only intereseted in knowing where the concentration is larger than 0.3
                    # Hence, if it is not, we will simply override the value to 0
                    if len(particle_count1) == 2:
                        try:
                            concentration = particle_count1[1]/(particle_count1[1] + particle_count2[1])

                            if concentration > 0.3:
                                grid_list[j][i] = concentration
                            else:
                                grid_list[j][i] = 0

                        except:
                            pass

                    if self.debug:
                        print("[DEBUG] Grid {num}".format(num=(i,j)))

        # Responsible for performing task A
        else:
            for i in range(self.Nx - 1):
                grid_list.append([0 for j in range(self.Ny - 1)])

            for i in range(len(self.x_grid)- 1):
                for j in range(len(self.y_grid) - 1):

                    check_inside_grid_x1 = np.logical_and(sub_1[:,0] > self.x_grid[i], sub_1[:,0] < self.x_grid[i+1])
                    check_inside_grid_y1 = np.logical_and(sub_1[:,1] < self.y_grid[j], sub_1[:,1] > self.y_grid[j+1])
                    grid_sub1_count = np.where(np.logical_and(check_inside_grid_x1, check_inside_grid_y1), 1, 0)
                    unique, particle_count1 = np.unique(grid_sub1_count, return_counts=True)

                    check_inside_grid_x2 = np.logical_and(sub_2[:,0] > self.x_grid[i], sub_2[:,0] < self.x_grid[i+1])
                    check_inside_grid_y2 = np.logical_and(sub_2[:,1] < self.y_grid[j], sub_2[:,1] > self.y_grid[j+1])
                    grid_sub2_count = np.where(np.logical_and(check_inside_grid_x2, check_inside_grid_y2), 1, 0)
                    unique, particle_count2 = np.unique(grid_sub2_count, return_counts=True)
                    
                    if len(particle_count1) == 2:
                        try:
                            grid_list[j][i] = particle_count1[1]/(particle_count1[1] + particle_count2[1])
                        except:
                            pass

                if self.debug:
                        print("[DEBUG] Grid {num}".format(num=(i,j)))
                        
        return np.array(grid_list)

    # Assign x coordinate from task B to their respective concentration
    def assign_concentration(self, sub_1, sub_2, concentration_grid, x_grid):
        
        concentration_plot = []

        # Checks if the coordinate is within the checked grid
        for i, concentration in enumerate(concentration_grid) :
            avg_x_coordinates = []
            for particle in sub_1:
                if particle > x_grid[i] and particle < x_grid[i+1]:
                    avg_x_coordinates.append(particle)

            for particle in sub_2:
                if particle > x_grid[i] and particle < x_grid[i+1]:
                    avg_x_coordinates.append(particle)

            avg_x = np.mean(avg_x_coordinates)

            concentration_plot.append((avg_x, concentration))
                
        return concentration_plot

    # Optimize method for task E
    def calculate_concentration_taskE(self,sub_1):

        grid_list = []
        
        self.sub_1 = sub_1

        for i in range(self.Nx - 1):
                grid_list.append([0 for j in range(self.Ny - 1)])

        for i in range(len(self.x_grid)- 1):
            for j in range(len(self.y_grid) - 1):
                
                # Only check for substance 1 particle's position
                check_inside_grid_x1 = np.logical_and(sub_1[:,0] > self.x_grid[i], sub_1[:,0] < self.x_grid[i+1])
                check_inside_grid_y1 = np.logical_and(sub_1[:,1] < self.y_grid[j], sub_1[:,1] > self.y_grid[j+1])
                grid_sub1_count = np.where(np.logical_and(check_inside_grid_x1, check_inside_grid_y1), 1, 0)
                unique, particle_count = np.unique(grid_sub1_count, return_counts=True)

                # The mathematical approach to solve for only 1 variable
                if len(particle_count) == 2:
                        try:
                            grid_list[j][i] = particle_count[1] /len(sub_1)

                        except:
                            pass
                    
        return np.array(grid_list)




