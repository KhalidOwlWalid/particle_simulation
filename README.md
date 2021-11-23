# Paricle Simulation

## Running the simulation
- Set your desired input in the 'globals.py' file 
- Run the simulation in 'main.py'

### Task A
#### List of variables that needs to be set
| Variables | Description | Type | Options (example) |
| --------- | ----------- | ---- | ----------------- |
| `self.task` | Sets the task for our simulation (Please make sure that it is capitalized) | `str` | A |
| `self.Np` | Sets the number of particles involved in the simulation | `int` | 150000 |
| `self.h` | Sets the time step for our simulation | `float` | 0.01 |
| `self.tEnd` | Sets the time length for our simulation | `float` | 0.2 |
| `self.grid_size` | Sets the grid size for our concentration plot | `int` | 100 |
| `self.radius` | Sets the radius of our circle in the simulation | `float` | 0.2 |
| `self.offset_x` <br /> `self.offset_y` | Sets the offset of the circle from the origin in the simulation | `float` | 0.4, 0.4 |
| `self.xMin` <br /> `self.xMax` | Sets the boundary condition for x-axis | `float` | -1.0, 1.0 |
| `self.yMin` <br /> `self.yMax` | Sets the boundary condition for y-axis | `float` | -1.0, 1.0 |
| `self.D` | Sets the diffusivity of our substance | `float` | 0.1 |
| `self.include_velocity` | Include the velocity in our simulation | `boolean` | True/False |
| `self.plot_2D_particle (OPTIONAL)` | Visualize the particle scatter plot | `boolean` | True/False |


# Class
| Class | Description |
| Globals | Handles all the input values from the user|
| Initial State | Initialize the task according to the condition set|
| SimulationMath | Handles all the physics and mathematics related calculation for the simulation |
| Concentration | Handles all the concentration related for the simulation |

