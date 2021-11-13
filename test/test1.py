from numpy.lib.function_base import interp
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


def read_data_file(file, *args):
    return [np.loadtxt(file, usecols=tuple(c)) for c in args]

def extract(file):
    n_line = 0
    data = []
    for line in open(file , 'r'):
        
        if line == "\n":
            n_line += 1
        else:
            lines = [i for i in line.split()]
            data.append((float(lines[0]), float(lines[1])))

    return np.array(data)

def root_mean_squared_error(actual, predicted):

    return np.sqrt(np.sum(np.square(np.subtract(actual, predicted)))/len(actual))



reference_solution = extract('data_file/reference_solution_1D.dat')

spatial_field = cKDTree(reference_solution)

observed_data = extract('observed_data/observed_concentration_v2.txt')

actual_concentration = observed_data[:,1]
predicted_concentration = np.interp(observed_data[:,0], reference_solution[:,0], reference_solution[:,1])

RMSE = mean_squared_error(predicted_concentration, actual_concentration, squared=False)

print(RMSE)





plt.show()