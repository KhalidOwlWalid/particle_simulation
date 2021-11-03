import numpy as np
import math
from scipy import interpolate

from globals import Globals

class SimulationMath(Globals):

    def __init__(self):
        super().__init__()
        self.data = []
        self.x_data = []
        self.y_data = []
        self.u_data = []
        self.v_data = []
        self.extract_data()
        
    
    def extract_data(self):

        n_line = 0

        if self.velocity_file == "data_file/velocityCMM3.dat":
            
            for line in open(self.velocity_file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    self.data.append((float(lines[0]), float(lines[1]), float(lines[2]), float(lines[3])))
                    self.x_data.append(float(lines[0]))
                    self.y_data.append(float(lines[1]))
                    self.u_data.append(float(lines[2]))
                    self.v_data.append(float(lines[3]))

            
        elif self.velocity_file == "data_file/reference_solution_1D.dat":

            for line in open(self.velocity_file , 'r'):
                
                if line == "\n":
                    n_line += 1
                else:
                    lines = [i for i in line.split()]
                    self.data.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=self.velocity_file))
        print("[INFO] There is {num} empty lines".format(num=n_line))

        return self.data

    def euler(self, coordinate, vel = 0, vel_type=False):

        random = np.random.normal(0,1,1)

        euler_func = lambda coordinate, vel = 0: coordinate + vel * self.h + np.sqrt(2 * self.D) * np.sqrt(self.h) * float(random)

        if vel_type:
            next_pos = euler_func(coordinate,vel)
        else:
            next_pos = euler_func(coordinate)

        return next_pos
    
    # All the functions below here are used to interpolate the velocity
    def bilinear_interpolation(self,x,y):

        x_interval = np.arange(-1.03125,1.03125,0.0625)
        y_interval = np.arange(-1.03125,1.03125,0.0625)
        
        nearest_x, nearest_y = self.find_nearest_point(x,y,x_interval, y_interval)
        nearest_velocity = self.find_corresponding_velocity(nearest_x, nearest_y, x, y)

        try:
            if nearest_velocity[0][0] == 10:
            
                u, v = nearest_velocity[0][2], nearest_velocity[0][3]
                return u, v

        except IndexError:
            u = 0
            v = 0
            return u, v


        else:
            u, v = self.interpolate_velocity(x, y, nearest_velocity)

        return u,v

    # This is only used in the case of 'emergency'
    def bilinear_interpolation_using_package(self, x_coordinate, y_coordinate):

        xx = x_coordinate
        yy = y_coordinate
        xx, yy = np.meshgrid(xx, yy)

        points = np.transpose(np.vstack((self.x_data, self.y_data)))
        u_interp = interpolate.griddata(points, self.u_data, (xx, yy), method='linear')
        v_interp = interpolate.griddata(points, self.v_data, (xx, yy), method='linear')

        return u_interp, v_interp

    # Find the nearest point to our x and y coordinate
    def find_nearest_point(self, x, y, x_list, y_list):

        nearest_x_points = []
        nearest_y_points = []

        for i, nearest_x in enumerate(x_list):

            if abs(x - nearest_x) < 0.0625:
                nearest_x_points.append(nearest_x)

        for i, nearest_y in enumerate(y_list):

            if abs(y - nearest_y) < 0.0625:
                nearest_y_points.append(nearest_y)

        # Tthe problem with the code is right here
        # Some of the points will be located at x > 0.9685 or x < -0.9685
        # This causes an issue as when taking the difference, we only get a single point

        return nearest_x_points, nearest_y_points

    # Find the velocity for the given x and y coordinate
    def find_corresponding_velocity(self, x_points, y_points, x_pos, y_pos):

        pairs = []
        velocity = []

        for i in x_points:
            for j in y_points:
                pairs.append((i,j))

        condition = lambda x_pos, y_pos : x_pos < -0.96875 or x_pos > 0.96875 or y_pos < -0.96875 or y_pos > 0.96875

        if condition(x_pos, y_pos):
            u, v = self.bilinear_interpolation_using_package(x_pos, y_pos)
            x, y = 10, 10
            velocity.append((x,y,float(u),float(v)))

        else:
            for i, coordinate in enumerate(pairs):
                
                #if condition(coordinate[0], coordinate[1]) or condition(x_pos, y_pos):
                if coordinate[0] > 0.96875 or coordinate[0] < -0.96875 or coordinate[1] < -0.96875 or coordinate[1] > 0.96875:
                        u, v = self.bilinear_interpolation_using_package(x_pos, y_pos)
                        x, y = None, None
                        velocity.append((x,y,u,v))
                        break

                else:
                    for j, points in enumerate(self.data):

                        if len(pairs) == 4:
                            if coordinate[0] == points[0] and coordinate[1] == points[1]:
                                velocity.append(points)

        return velocity

    
    # Perform the calculation for our velocity interpolation
    def interpolate_velocity(self,x,y,nearest_velocity):

        velocity_type = ["x", "y"]

        try:
            for type in velocity_type:
                
                if type == "x":
                    
                    # Sets the velocity as None to any particles that have no nearest velocity
                    if nearest_velocity[0][1] == None:
                        u = 0

                    else:
                        x1, y1, q11 = nearest_velocity[0][0], nearest_velocity[0][1], nearest_velocity[0][2]
                        x4,y4, q21 = nearest_velocity[1][0], nearest_velocity[1][1], nearest_velocity[1][2]
                        x3, y3, q12 = nearest_velocity[2][0], nearest_velocity[2][1], nearest_velocity[2][2]
                        x2, y2, q22 = nearest_velocity[3][0], nearest_velocity[3][1], nearest_velocity[3][2]

                        u = self.calculate_velocity(x,y,x1,x2,y1,y2,q11,q12,q21,q22)

                if type == "y":

                    if nearest_velocity[0][0] == None:
                        v = 0

                    else:
                        x1, y1, q11 = nearest_velocity[0][0], nearest_velocity[0][1], nearest_velocity[0][3]
                        x4,y4, q21 = nearest_velocity[1][0], nearest_velocity[1][1], nearest_velocity[1][3]
                        x3, y3, q12 = nearest_velocity[2][0], nearest_velocity[2][1], nearest_velocity[2][3]
                        x2, y2, q22 = nearest_velocity[3][0], nearest_velocity[3][1], nearest_velocity[3][3]

                        v = self.calculate_velocity(x,y,x1,x2,y1,y2,q11,q12,q21,q22)

        except IndexError:
            print("Index error inside interpolate_velocity")
            u = 0
            v = 0

        return float(u), float(v)   

    # The interpolation's math
    def calculate_velocity(self,x,y,x1,x2,y1,y2,q11,q12,q21,q22):

        a = np.array([[x2-x ,x-x1]])
        b = np.array([[q11,q12], [q21, q22]])
        c = np.array([[y2-y], [y-y1]])
        denominator = 1/((x2-x1) * (y2-y1))

        A = np.dot(a,b)
        B = np.dot(A, c)
        C = denominator * B

        return C
        