#Import the required Libraries
from tkinter import *
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Globals:

    def __init__(self):
        

        # Offsets the chemical where +ve is to the right/up and -ve is to the left/down
        self.offset_x = 0.4
        self.offset_y = 0.4
        
        # Boundaries
        self.xMax = 1
        self.xMin = -1
        self.yMax = 1
        self.yMin = -1
        
        # Number of particles
        self.Np = 200000

        # Diffusivity
        self.D = 0.1

        # Conditions
        self.h = 0.025
        self.time = 0.0
        self.tEnd = 0.025

        self.steps = int(self.tEnd / self.h)
        
        # Grids
        self.Nx = 70
        self.Ny = 70

        # Create the particles
        self.x = np.random.uniform(low=-1, high=1, size=self.Np)
        self.y = np.random.uniform(low=-1, high=1, size=self.Np)

        # For size of scatter plots, increase the value to get bigger scatter size
        self.size = 10

        self.velocity_file = 'data_file/velocityCMM3.dat'

        self.include_velocity = False

class InitialState(Globals):

    def __init__(self):
        
        super().__init__()
    
        self.sub_1 = []
        self.sub_2 = []
        
    def taskA_initial_state(self):
        
        # The equation for circle
        isInside = lambda x_coordinate, y_coordinate, radius : (x_coordinate - self.offset_x) ** 2 + (y_coordinate - self.offset_y) ** 2 <= radius ** 2

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if isInside(self.x[i], self.y[i], 0.3):
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        return self.sub_1, self.sub_2

    def taskB_initial_state(self):

        toTheLeft = lambda coordinate : coordinate <= 0

        # Divide the particles into their substance type
        for i in range(self.Np):
            
            # If the position of the particle is within a circle of radius 1 centred at the origin, add the particle as substance 1
            if toTheLeft(self.x[i]): 
                self.sub_1.append((self.x[i], self.y[i]))

            # Vice versa
            else:
                self.sub_2.append((self.x[i], self.y[i]))

        return self.sub_1, self.sub_2


class TaskA(InitialState):

    def __init__(self):
        super().__init__()

        # Stores the substance into a dictionary 
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

    def plot_solution(self, win, plot_2D=True):

        if plot_2D:

            self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
            self.ax1 = self.figure1.add_subplot(111)

            self.ax1.scatter(*zip(*self.substance["sub_1"]), color="blue")
            self.ax1.scatter(*zip(*self.substance["sub_2"]), color="red")

            print(len(self.substance["sub_1"]))
            print(len(self.substance["sub_2"]))
            self.canvas = FigureCanvasTkAgg(self.figure1, win)
            
            self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
            
            self.canvas.draw()
 
            
    def main(self, win):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()
        self.plot_solution(win)

# Ignore this, I just need to use this as reference 
"""
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.plot(y)
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()
  """

# Same as Task A, just that now we call the taskB_initial state
class TaskB(InitialState):

    def __init__(self):
        super().__init__()

        # Stores the substance into a dictionary 
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.figure1, self.axes1 = plt.subplots()

    def plot_solution(self, plot_2D=True):

        if plot_2D:
            for i, sub_type in enumerate(self.substance_list):

                color = None 
                print("Plotting for ", sub_type)

                # for j, coordinate in enumerate(self.substance[sub_type]):

                if sub_type == "sub_1":
                    color = "red"
                else:
                    color = "blue"

                self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
                self.ax1 = self.figure1.add_subplot(111)
                self.ax1.clear()
                self.bar1 = FigureCanvasTkAgg(self.figure1, self.win)
                self.bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                self.ax1.plot(*zip(*self.substance[sub_type]))
                self.bar1.draw()
        
    def main(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state()
        self.plot_solution()


class GraphPlot(TaskA):
    
    def __init__(self):

        self.win = Tk()
        self.win.geometry("750x750")

        Button(self.win, text= "Show Graph", command= self.get_coefficient_value).pack(pady=20)

        self.Np = Entry(self.win, width=40)
        self.Np.pack(pady=30)

        button = Button(self.win, text="Enter Np", command=self.ok)
        button.pack()
        self.win.mainloop()

    def ok(self):
        pass

    def get_coefficient_value(self):
        
        # Get the value we input and assign it to self.Np
        self.Np = int(self.Np.get())

        # We are instantiating taskA as an object of the class TaskA
        # Right now, since the default value for task_A is everything inside globals (eg task_A.Np = 15000)
        task_A = TaskA()

        # We want to override this value and equate it with the value that we assign in the box
        task_A.Np = self.Np

        # Run everything inside the main function of task_A
        task_A.main(self.win)

        # Dont use plt.show() as this will actually plot using matpltotlib's frontend
        # You want to use this library
        """
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
        from matplotlib.figure import Figure
        """
        # as this library will embed our plot into Tkinter's window
        # I only use plt.show() in this case to show you if the button and the command parameter works

        # https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
        # At 4:50 and 10:30, he mentioned about it 

    def quadratic_equation(self,a,b,c):
        
        self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.clear()
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.win)
        self.bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        
        x = np.linspace(0,100,30)
        y_list = []
        for val in x:
            y = a*val**2 + b*val + c
            y_list.append(y)

        self.ax1.plot(x,y_list)
        self.bar1.draw()


test = GraphPlot()