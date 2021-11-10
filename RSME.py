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

        return np.array(data)


# Please make sure the your file's path is in the same folder as the python script that you are running
data_v1 = extract_data("observed_data/observed_concentration_v1.txt")
ref_sol = extract_data("data_file/reference_solution_1D.dat")

print(data_v1)
print(data_v1[-1])
print(data_v1[-1][0])


# Plots all the data into a single figure
plt.plot(*zip(*data_v1), '-bo', markersize=size)
plt.plot(*zip(*ref_sol), 'r', markersize=size)

plt.show()

