import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
buttons = []
click_command = False

def on_click(event):
    click_command(event.xdata, event.ydata)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        frame = Window(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class Window(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for button in buttons:
            ttk.Button(self, text=button[0], command=button[1]).pack()
        global canvas
        canvas = FigureCanvasTkAgg(f, self)
        a.set_xlim(0, 1)
        a.set_ylim(0, 1)
        canvas.show()
        canvas.mpl_connect('button_press_event', on_click)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

def add_button(text, command):
    buttons.append([text,command])

def add_click(command):
    global click_command
    click_command = command

def get_a():
    return a

def redraw():
    a.set_xlim(0, 1)
    a.set_ylim(0, 1)
    canvas.show()

def start():
    App().mainloop()
