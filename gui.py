import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk

buttons = []
checkboxes = []
checkbox_variables = []
radio_button_groups = []
radio_button_variables = []
messages = []
message_variables = []
click_command = False

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global window
        window = self
        for button in buttons:
            row, column, text, press, release = button
            b = ttk.Button(self, text=text)
            b.bind("<ButtonPress-1>",
                   (lambda press: (lambda event: press()))(press))
            b.bind("<ButtonRelease-1>",
                   (lambda release: (lambda event: release()))(release))
            b.grid(row=row, column=column)
        for checkbox in checkboxes:
            row, column, text, command = checkbox
            variable = tk.IntVar()
            checkbox_variables.append(variable)
            ttk.Checkbutton(self,
                            text=text,
                            variable=variable,
                            command=command).grid(row=row, column=column)
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
        if use_matplotlib:
            canvas = FigureCanvasTkAgg(figure, self)
            if fixed_size:
                axes.set_xlim(0, 1)
                axes.set_ylim(0, 1)
            canvas.show()
            if click_command:
                canvas.mpl_connect('button_press_event',
                                   lambda event: click_command(event.xdata,
                                                               event.ydata))
            canvas.get_tk_widget().grid(row=button_rows,
                                        columnspan=button_columns)
        else:
            canvas = tk.Canvas(self, width=window_width, height=window_height)
            canvas.grid(row=button_rows, columnspan=button_columns)
        self.bind("<Control-c>", lambda event: done())
        self.bind("<Escape>", lambda event: done())
    def show_image(self, bgr_image):
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(rgb_image))
        canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

def nothing():
    return

def done():
    exit()

def add_button(row, column, text, press, release):
    buttons.append([row, column, text, press, release])

def add_checkbox(row, column, text, command):
    checkboxes.append([row, column, text, command])
    i = len(checkboxes)-1
    def internal():
        return checkbox_variables[i].get()==1
    return internal

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

def get_axes():
    return axes

def redraw():
    if fixed_size:
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
    canvas.show()

def get_window():
    return window

def start_fixed_size_matplotlib(width, height, rows, columns):
    global use_matplotlib
    use_matplotlib = True
    global fixed_size, figure, axes, button_rows, button_columns
    fixed_size = True
    button_rows = rows
    button_columns = columns
    global axes
    figure = Figure(figsize=(width, height), dpi=100)
    axes = figure.add_subplot(111)
    App().mainloop()

def start_variable_size_matplotlib(width, height, rows, columns):
    global use_matplotlib
    use_matplotlib = True
    global fixed_size, figure, axes, button_rows, button_columns
    fixed_size = False
    button_rows = rows
    button_columns = columns
    global axes
    figure = Figure(figsize=(width, height), dpi=100)
    axes = figure.add_subplot(111)
    App().mainloop()

def start_video(width, height, rows, columns):
    global use_matplotlib
    use_matplotlib = False
    global window_width, window_height, button_rows, button_columns
    window_width = width
    window_height = height
    button_rows = rows
    button_columns = columns
    App().mainloop()
