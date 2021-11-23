"""
This file handles all the concentration problem. 

calculate_concentration : calculate concentration for both 1D and 2D case. If self.Ny is set to 1, then its a 1D case. Need to improve
assgin_concentration : Assign concentration to each respective particles and this function is meant for task B

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
        
        if self.task != 'B':
            print("[INFO] Calculating concentration... This may take awhile...")
            print("[INFO] Set self.debug = True if you wish to see which grid the programme is currenly calculating")
            
        # Populate a "grid" with zeros
        grid_list = []
        
        self.sub_1 = sub_1
        self.sub_2 = sub_2

        zero_div_err = 0

        grid_position = lambda x, y, i, j: x > self.x_grid[i] and x < self.x_grid[i+1] and y < self.y_grid[j] and y > self.y_grid[j+1]
        
        if self.Ny == 1:

            grid_list.append([0 for j in range(self.Nx - 1)])

            for n in range(len(self.x_grid) - 1):
                
                try:
                    n_sub_2 = 0 
                    for particle in sub_1:
                        if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                            grid_list[0][n] += 1

                    for particle in sub_2:
                        if particle > self.x_grid[n] and particle < self.x_grid[n+1]:
                            n_sub_2 += 1

                except IndexError:
                    print("[DEBUG] Index out of range which is the {n}th column".format(n=n))

                try:
                    grid_list[0][n] = grid_list[0][n]/(grid_list[0][n] + n_sub_2)

                except ZeroDivisionError:
                    #print("[WARN] ZeroDivisionError : Not enough particles to calculate")
                    pass

                except IndexError:
                    print("[WARN] IndexError")
                
        elif Globals().task_type[Globals().task] == 2:

            for i in range(self.Nx - 1):
                grid_list.append([0 for j in range(self.Ny - 1)])
            
            print("[INFO] Checking each grid for particles...")

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
                            concentration = particle_count1[1]/(particle_count1[1] + particle_count2[1])

                            if concentration > 0.3:
                                grid_list[j][i] = concentration
                            else:
                                grid_list[j][i] = 0

                        except:
                            pass

                    if self.debug:
                        print("[DEBUG] Grid {num}".format(num=(i,j)))

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

    # This one is actually meant for the use of task B, but I have created it and tested it on task A
    def assign_concentration(self, sub_1, sub_2, concentration_grid, x_grid):
        
        concentration_plot = []

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

    def calculate_concentration_taskE(self,sub_1):

        grid_list = []
        
        self.sub_1 = sub_1

        for i in range(self.Nx - 1):
                grid_list.append([0 for j in range(self.Ny - 1)])

        for i in range(len(self.x_grid)- 1):
            for j in range(len(self.y_grid) - 1):

                check_inside_grid_x1 = np.logical_and(sub_1[:,0] > self.x_grid[i], sub_1[:,0] < self.x_grid[i+1])
                check_inside_grid_y1 = np.logical_and(sub_1[:,1] < self.y_grid[j], sub_1[:,1] > self.y_grid[j+1])
                grid_sub1_count = np.where(np.logical_and(check_inside_grid_x1, check_inside_grid_y1), 1, 0)
                unique, particle_count = np.unique(grid_sub1_count, return_counts=True)

                if len(particle_count) == 2:
                        try:
                            grid_list[j][i] = particle_count[1] /len(sub_1)

                        except:
                            pass
                    
        return np.array(grid_list)




