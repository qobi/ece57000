import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

button_rows = 0
button_columns = 0
buttons = []
radio_button_groups = []
radio_button_variables = []
messages = []
message_variables = []
click_command = False
fixed_size = True

def variable_size():
    global fixed_size
    fixed_size = False

def on_click(event):
    click_command(event.xdata, event.ydata)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        global frame
        frame = Window(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        self.bind("<Control-c>", done)
        self.bind("<Escape>", done)

class Window(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        for button in buttons:
            row, column, text, press, release = button
            b = ttk.Button(self, text=text)
            b.bind("<ButtonPress-1>", press)
            b.bind("<ButtonRelease-1>", release)
            b.grid(row=row, column=column)
        for radio_button_group in radio_button_groups:
            radio_buttons, command = radio_button_group
            variable = tk.IntVar()
            radio_button_variables.append(variable)
            for radio_button in radio_buttons:
                row, column, text, value = radio_button
                ttk.Radiobutton(self,
                                text=text,
                                variable=variable,
                                value=value,
                                command=command).grid(row=row, column=column)
        for message in messages:
            row, column, columnspan = message
            variable = tk.StringVar()
            message_variables.append(variable)
            m = tk.Label(self)
            m.config(font=("Verdana", 14), textvariable=variable)
            m.grid(row=row, column=column, columnspan=columnspan)
        global canvas
        canvas = FigureCanvasTkAgg(f, self)
        if fixed_size:
            a.set_xlim(0, 1)
            a.set_ylim(0, 1)
        canvas.show()
        if click_command:
            canvas.mpl_connect('button_press_event', on_click)
        canvas.get_tk_widget().grid(row=button_rows, columnspan=button_columns)

def nothing(event):
    return

def done(event):
    exit()

def add_button(row, column, text, press, release):
    buttons.append([row, column, text, press, release])

def add_radio_button_group(buttons, command):
    radio_button_groups.append([buttons, command])
    i = len(radio_button_groups)-1
    def internal():
        return radio_button_variables[i].get()
    return internal

def add_message(row, column, columnspan):
    messages.append([row, column, columnspan])
    i = len(messages)-1
    def internal(text):
        message_variables[i].set(text)
    return internal

def add_click(command):
    global click_command
    click_command = command

def get_a():
    return a

def redraw():
    if fixed_size:
        a.set_xlim(0, 1)
        a.set_ylim(0, 1)
    canvas.show()

def task():
    return frame

def start(width, height, rows, columns):
    global f, a, button_rows, button_columns
    button_rows = rows
    button_columns = columns
    f = Figure(figsize=(width, height), dpi=100)
    a = f.add_subplot(111)
    App().mainloop()
