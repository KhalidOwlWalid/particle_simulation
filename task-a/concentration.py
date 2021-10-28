import numpy as np

from globals import Globals

class Concentration(Globals):

    def __init__(self):
        super().__init__()

        self.x_grid = np.linspace(-1,1,self.Nx)
        self.y_grid = np.linspace(-1,1,self.Ny)
        
    def calculate_concentration(self, sub_1, sub_2):
        
        print("[INFO] Calculating concentration...")
        # Populate a "grid" with zeros
        grid_list = []
        
        grid_position = lambda x, y, i, j: x > self.x_grid[i] and x < self.x_grid[i+1] and y > self.y_grid[j] and y < self.y_grid[j+1]
        
        for i in range(self.Nx - 1):
            grid_list.append([0 for j in range(self.Ny - 1)])

        for i in range(len(self.x_grid)- 1):
            for j in range(len(self.y_grid) - 1):

                n_sub_1 = 0
                
                for particle in sub_1:
                    # Check corner
                    if grid_position(particle[0], particle[1], i, j):
                        n_sub_1 += 1

                for particle in sub_2:
                    
                    # Check corner
                    if grid_position(particle[0], particle[1], i, j):
                        grid_list[i][j] += 1
                try:
                    grid_list[i][j] = grid_list[i][j]/(grid_list[i][j] + n_sub_1)
                except ZeroDivisionError:
                    print("[WARN] ZeroDivisionError : Not enough particles to calculate")

                    # Patch the "hole"
                    grid_list[i][j] = 1
                    print("[INFO] Patched")
                except IndexError:
                    print("[WARN] IndexError: Out of boundaries at column {col}, row {row}".format(col=i, row=j))

        return np.array(grid_list)
        
