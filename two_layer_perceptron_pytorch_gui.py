from gui import *
import torch.nn as nn
from two_layer_perceptron_pytorch import *

points = []
labels = []
network = []

batch_size = 10
learning_rate = 0.1
criterion = nn.MSELoss()

def redisplay():
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i][0]>labels[i][1]:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        else:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    redraw()

def clear_command():
    global points, labels, network
    points = []
    labels = []
    network = []
    message("")
    get_axes().clear()
    redraw()

def initialize_command():
    def internal():
        global network
        network = initialize(2, 10, 2)
        message("{:.3f}".format(cost(points, labels, network, criterion)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def step_command():
    def internal():
        step(points, labels, network, criterion, batch_size, learning_rate)
        message("{:.3f}".format(cost(points, labels, network, criterion)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def train_command():
    def internal():
        train(points, labels, network, criterion, batch_size, learning_rate)
        message("{:.3f}".format(cost(points, labels, network, criterion)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def all_command():
    resolution = 50
    scale = 1.0/resolution
    for y in range(0, resolution+1):
        for x in range(0, resolution+1):
            label = classify([scale*x, scale*y], network)
            if label==0:
                get_axes().plot([scale*x], [scale*y], "r.")
            else:
                get_axes().plot([scale*x], [scale*y], "b.")
    redraw()

def click(x, y):
    message("")
    if mode()==0:
        points.append([x, y])
        labels.append([1, 0])
        get_axes().plot([x], [y], "r+")
        redraw()
    elif mode()==1:
        points.append([x, y])
        labels.append([0, 1])
        get_axes().plot([x], [y], "b+")
        redraw()
    else:
        if network==[]:
            message("Train first")
        else:
            label = classify([x, y], network)
            if label==0:
                message("Red")
            else:
                message("Blue")

add_button(0, 0, "Clear", clear_command, nothing)
mode = add_radio_button_group([[0, 1, "Red", 0],
                               [0, 2, "Blue", 1],
                               [0, 3, "Classify", 2]],
                              lambda: False)
add_button(0, 4, "Initialize", initialize_command, nothing)
add_button(0, 5, "Step", step_command, nothing)
add_button(0, 6, "Train", train_command, nothing)
add_button(0, 7, "All", all_command, nothing)
add_button(0, 8, "Exit", done, nothing)
message = add_message(1, 0, 9)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 9)
