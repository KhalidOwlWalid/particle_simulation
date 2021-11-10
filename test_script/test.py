import numpy as np
from scipy.interpolate import griddata

def generate_random_number(array_size):

    x_rand = np.random.normal(0,1, array_size)
    y_rand = np.random.normal(0,1, array_size)

    random = np.stack((x_rand, y_rand), axis=1)

    return random


random = generate_random_number(10)
print(random)

