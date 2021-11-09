import numpy as np
from scipy import interpolate
import math
from scipy.spatial import cKDTree

h = 0.01
D = 0.1

def read_data_file(file, *args):
    return [np.loadtxt(file, usecols=tuple(c)) for c in args]

def bilinear_interpolate(im, x, y):
    x = np.asarray(x)
    y = np.asarray(y)

    x0 = np.floor(x).astype(int)
    x1 = x0 + 1
    y0 = np.floor(y).astype(int)
    y1 = y0 + 1

    x0 = np.clip(x0, 0, im.shape[1]-1);
    x1 = np.clip(x1, 0, im.shape[1]-1);
    y0 = np.clip(y0, 0, im.shape[0]-1);
    y1 = np.clip(y1, 0, im.shape[0]-1);

    Ia = im[ y0, x0 ]
    Ib = im[ y1, x0 ]
    Ic = im[ y0, x1 ]
    Id = im[ y1, x1 ]

    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)

    return wa*Ia + wb*Ib + wc*Ic + wd*Id

def bilinear_interpolation_using_package(x_coordinate, y_coordinate, field_vectors, fluid_coordinate):

    xx = x_coordinate
    yy = y_coordinate
    xx, yy = np.meshgrid(xx, yy)

    u_interp = interpolate.griddata(fluid_coordinate, field_vectors[:,0], (xx, yy), method='linear')
    v_interp = interpolate.griddata(fluid_coordinate, field_vectors[:,1], (xx, yy), method='linear')

    return u_interp, v_interp



def euler(coordinate, vel = 0, vel_type=True):

    random = np.random.normal(0,1,1)

    euler_func = lambda coordinate, vel: coordinate + vel * h + np.sqrt(2 * D) * np.sqrt(h) * float(random)

    if vel_type:
        next_pos = np.where(math.isnan(vel), euler_func(coordinate,vel=0), euler_func(coordinate, vel))
    else:
        next_pos = euler_func(coordinate, vel=0)

    return next_pos

def boundary_conditions(fluid_coordinates):
    pass

def combine_data(x,y):

    fluid_coordinate = []

    for i, coordinate in enumerate(x):
        fluid_coordinate.append((x[i], y[i]))

    return np.array(fluid_coordinate)

def add_one(x):
    return x + 1

# Combine it into one array so that you wont lose any particles
x = [0.4863567556496071, 0.46071638636738976, 0.5573551069303162, 0.6770065982888989, 0.2371593198441806, 0.7741559343237026, 0.5372884106215676]
y = [0.2988271218666225, 0.7650646112783137, 0.6699900200580649, 0.5719717832264015, 0.6576435046966831, 0.5327360716644285, 0.22333818736155053]

# x = np.linspace(-1,1,10)
# y = x = np.linspace(-1,1,10)

file = 'data_file/velocityCMM3.dat'

field_coordinate, fluid_vector = read_data_file(file,[0,1], [2,3])

fluid_coordinates = combine_data(x,y)

print(combin)

spatial_field = cKDTree(field_coordinate)

_, index = spatial_field.query(fluid_coordinates)

velocity = fluid_vector[index]


euler = lambda coordinate, velocity : coordinate + velocity * 0.01

print(fluid_coordinates)
print(velocity)

fluid_coordinates[:,0], fluid_coordinates[:,1] = euler(fluid_coordinates[:,0], velocity[:,0]), euler(fluid_coordinates[:,1], velocity[:,1])

print(fluid_coordinates)