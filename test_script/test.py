import numpy as np
from scipy.interpolate import griddata


def random_number(coordinate):
    return coordinate + np.random.rand(1,1)

def generate_random_number(x):

    return x + np.random.normal(0,1,1500)



x = np.zeros(1500)

new_x = generate_random_number(x)

print(new_x)