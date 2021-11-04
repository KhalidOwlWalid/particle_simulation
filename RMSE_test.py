import numpy as np
import matplotlib.pyplot as plt


size = 1.5

# This will extract the data that you need where it will be in the form of 
# your_data = [(0.952937, 0.0),.....,(0.9842844, 0.0)]

def extract_data(file):

        data = []

        for line in open(file , 'r'):
            
            lines = [i for i in line.split()]
            data.append((float(lines[0]), float(lines[1])))

        print("[INFO] Extracting data from {name}".format(name=file))

        return data


# Please make sure the your file's path is in the same folder as the python script that you are running
data_v1 = extract_data("observed_concentration_v1.txt")
data_v2 = extract_data("observed_concentration_v2.txt")
data_v3 = extract_data("observed_concentration_v3.txt")
ref_sol = extract_data("reference_solution_1D.dat")

# Plots all the data into a single figure
plt.plot(*zip(*data_v1), '-bo', markersize=size)
plt.plot(*zip(*data_v2), '-co', markersize=size)
plt.plot(*zip(*data_v3), '-go', markersize=size)
plt.plot(*zip(*ref_sol), 'r', markersize=size)

plt.show()

