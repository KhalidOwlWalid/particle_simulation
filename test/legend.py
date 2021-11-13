# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:41:24 2021

@author: sidha
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt



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
        self.Np = 15000

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

    def __init__(self, window):
        super().__init__()

        self.window = window
        # Stores the substance into a dictionary 
        self.substance = {"sub_1": [], "sub_2": []}
        self.substance_list = ["sub_1", "sub_2"]

        self.figure, self.axes = plt.subplots()

    def plot_solution(self, plot_2D=True):

        if plot_2D:
        
            color = None 

            # for j, coordinate in enumerate(self.substance[sub_type]):


            print((self.yMin, self.yMax))

            fig = Figure(figsize = (5, 5),
                            dpi = 100)
            initial_plot = fig.add_subplot(111)
            
            
            initial_plot.scatter(*zip(*self.substance["sub_2"]), s=self.size, c="blue")
            initial_plot.scatter(*zip(*self.substance["sub_1"]), s=self.size, c="red")

            canvas = FigureCanvasTkAgg(fig,
                            master = self.window)

            canvas.draw()
            # self.axes.set_xbound(lower=self.xMin, upper=self.xMax)
            # self.axes.set_xlim(xmin=self.xMin, xmax=self.xMax)
            # self.axes.set_ybound(lower=self.yMin, upper=self.yMax)
            # self.axes.set_ylim(ymin=self.yMin, ymax=self.yMax)
            # self.axes.scatter(*zip(*self.substance[sub_type]), s=self.size, c=color)
        

    def main(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskA_initial_state()
        self.plot_solution()

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

                fig = Figure(figsize = (5, 5),
                                dpi = 100)
                initial_plot = fig.add_subplot(111)
                
                initial_plot.scatter(*zip(*self.substance[sub_type]), s=self.size, c=color)

                canvas = FigureCanvasTkAgg(fig,
                               master = master)

                # self.axes1.set_xbound(lower=self.xMin, upper=self.xMax)
                # self.axes1.set_xlim(xmin=self.xMin, xmax=self.xMax)
                # self.axes1.set_ybound(lower=self.yMin, upper=self.yMax)
                # self.axes1.set_ylim(ymin=self.yMin, ymax=self.yMax)
                # self.axes1.scatter(*zip(*self.substance[sub_type]), s=self.size, c=color)
        
    def main(self):
        self.substance["sub_1"], self.substance["sub_2"] = self.taskB_initial_state()
        self.plot_solution()



class UI(TaskA):
    def __init__(self,master):
        master.title('Modelling of Diffusion and Advection of a substance')
        master.configure(background = 'white')
    
        self.style = ttk.Style()
        self.style.configure('TLabel',font = ('Arial',10))
        
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
    
        ttk.Label(self.frame_header , text = 'Diffusion and Advection Modelling',style='TLabel').grid(row= 0, column = 2 )
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        
        #ttk.Label(self.frame_content,text='Plot:').grid(row = 2, column = 1,pady=5)
        ttk.Label(self.frame_content,text='Diffusivity:').grid(row = 2, column = 2,pady=5)
        ttk.Label(self.frame_content,text='Timestep:').grid(row = 4, column = 2,pady=5)
        ttk.Label(self.frame_content,text='Time:').grid(row = 4, column = 4,pady=5)
        ttk.Label(self.frame_content,text='Number of points:').grid(row = 3, column = 2,pady=5)
        ttk.Label(self.frame_content,text='Xmin:').grid(row = 5, column = 2,pady=5)
        ttk.Label(self.frame_content,text='Xmax:').grid(row = 6, column = 2,pady=5)
        ttk.Label(self.frame_content,text='Ymin:').grid(row = 5, column = 4,pady=5)
        ttk.Label(self.frame_content,text='Ymax:').grid(row = 6, column = 4,pady=5)
        #ttk.Label(self.frame_content,text='Intial condition:').grid(row = 7, column = 2,pady=5)
        #ttk.Label(self.frame_content,text='Velocity profile:').grid(row = 8, column = 2,pady=5)
        
        self.graph_canvas=tk.Canvas(self.frame_content,width= 640,height = 480, background= 'white')
        self.diffusion=ttk.Entry(self.frame_content,width= 30)
        self.time_step=ttk.Entry(self.frame_content,width= 5)
        self.timeMax=ttk.Entry(self.frame_content,width= 5)
        self.n_particles = ttk.Entry(self.frame_content,width= 30)
        self.x_min=ttk.Entry(self.frame_content,width= 5)
        self.x_max=ttk.Entry(self.frame_content,width= 5)
        self.y_min=ttk.Entry(self.frame_content,width= 5)
        self.y_max=ttk.Entry(self.frame_content,width= 5)
        #self.combobox_Intial_condition=ttk.Combobox(self.frame_content,width= 27)
        #self.combobox_Velocity_profile=ttk.Combobox(self.frame_content,width= 27)
        
        self.graph_canvas.grid(row = 2, rowspan= 8, column= 1)
        self.n_particles.grid(row=3,column=3 , columnspan=5,pady=5,padx=5)
        self.diffusion.grid(row=2,column=3 , columnspan=5,pady=5,padx=5)
        self.time_step.grid(row=4,column=3 ,pady=5,padx=5)
        self.timeMax.grid(row=4,column=5 ,pady=5,padx=5)
        self.x_min.grid(row = 5, column = 3,pady=5,padx=5)
        self.x_max.grid(row = 6, column = 3,pady=5,padx=5)
        self.y_min.grid(row = 5, column = 5,pady=5,padx=5)
        self.y_max.grid(row = 6, column = 5,pady=5,padx=5)
        #self.combobox_Intial_condition.grid(row = 7, column=3 , columnspan=5 ,pady=5,padx=5)
        #self.combobox_Velocity_profile.grid(row = 8,column=3 , columnspan=5,pady=5,padx=5)
        
        #self.combobox_Intial_condition.config(value=('1D','2D','Oil Spill'))
        #self.combobox_Velocity_profile.config(value=('None','Standard'))
        
        ttk.Button(self.frame_content,text = 'Run', command= self.get_coefficient_value).grid(row=9,column=3,stick='sw')
        ttk.Button(self.frame_content,text = 'Cancel').grid(row=9,column=4,stick='se')
        ttk.Button(self.frame_content,text = 'Clear').grid(row=9,column=5,stick='sw')
        
    def ok(self):
        pass

    
    def get_coefficient_value(self):
        # Get the value we input and assign it to self.Np
        # self.Np = int(self.n_particles.get())
        # self.xMax = float(self.x_max.get())
        # self.xMin = float(self.x_min.get())
        # self.yMax = float(self.y_min.get())
        # self.yMin = float(self.y_min.get())
        # self.D = float(self.diffusion.get())
        # self.h = float(self.time_step.get())
        # self.tEnd = float(self.timeMax.get())

        # We are instantiating taskA as an object of the class TaskA
        # Right now, since the default value for task_A is everything inside globals (eg task_A.Np = 15000)
        task_A = TaskA()

        # We want to override this value and equate it with the value that we assign in the box
        # task_A.Np = self.Np
        # task_A.xMax = self.xMax
        # task_A.xMin = self.xMin
        # task_A.yMin = self.yMin
        # task_A.yMax = self.yMax
        # task_A.D = self.D
        # task_A.h = self.h
        # task_A.tEnd = self.tEnd

        # Run everything inside the main function of task_A
        task_A.main()

        plt.show()
        
        
        
        
def main():
    root=Tk()
    ui= UI(root)
    root.mainloop()
    
if __name__=="__main__":
    main()