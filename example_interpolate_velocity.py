import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

"""
Reference:
https://stackoverflow.com/questions/58691789/how-to-interpolate-a-vector-field-with-python
"""

x_interval = np.arange(-1.03125,1.03125,0.0001)
y_interval = np.arange(-1.03125,1.03125,0.0001)


def extract_data():

    file=open("data_file/velocityCMM3.dat")
    data=file.read()

    data = []
    x = []
    y = []
    u = []
    v =[]

    for line in open('data_file/velocityCMM3.dat', 'r'):
        try:
            lines = [i for i in line.split()]
            data.append((float(lines[0]), float(lines[1]), float(lines[2]), float(lines[3])))
        except:
            pass

    for i in data:
        x.append(i[0])
        y.append(i[1])
        u.append(i[2])
        v.append(i[3])

    return x, y, u, v

x, y, u, v = extract_data()

plt.figure(1)
plt.quiver(x, y, u, v)

#xx = np.arange(-1,1, 0.001)
#yy =  np.arange(-1,1, 0.001)
xx = np.linspace(-1,1,4)
yy = np.linspace(-1,1,4)
xx, yy = np.meshgrid(xx, yy)
points = np.transpose(np.vstack((x, y)))

u_interp = interpolate.griddata(points, u, (xx, yy), method='linear')
v_interp = interpolate.griddata(points, v, (xx, yy), method='linear')

plt.figure(2)
plt.quiver(xx, yy, u_interp, v_interp)

grid_list = []

for i in range(4):
    grid_list.append([0 for j in range(4)])

print(xx)

for i in range(4):
    for j in range(4):
        grid_list[i][j] = ((xx[i][j], yy[i][j]))

print(np.array(grid_list))

plt.show()