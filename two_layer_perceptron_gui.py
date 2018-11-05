from gui import *
from two_layer_perceptron import *

points = []
labels = []
weights1 = []
biases1 = []
weights2 = []
biases2 = []

def redisplay():
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i]<0:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        else:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    if len(weights1)==2:
        for j in range(0, len(weights1)):
            get_axes().plot([0, 1],
                            [-(weights1[j][0]*0+biases1[j])/weights1[j][1],
                             -(weights1[j][0]*1+biases1[j])/weights1[j][1]],
                            "y-")
        hidden = [sigmoid_layer(fc_layer(points[i], weights1, biases1))
                  for i in range(0, len(points))]
        for i in range(0, len(points)):
            get_axes().plot(
                [points[i][0], hidden[i][0]],
                [points[i][1], hidden[i][1]],
                "m-")
        get_axes().plot([0, 1],
                        [-(weights2[0][0]*0+biases2[0])/weights2[0][1],
                         -(weights2[0][0]*1+biases2[0])/weights2[0][1]],
                        "g-")
    redraw()

def clear_command():
    global points, labels, weights1, biases1, weights2, biases2
    points = []
    labels = []
    weights1 = []
    biases1 = []
    weights2 = []
    biases2 = []
    message("")
    get_axes().clear()
    redraw()

def initialize_command():
    def internal():
        global weights1, biases1, weights2, biases2
        weights1, biases1, weights2, biases2 = initialize(points, labels, 2)
        message("{:.3f}".format(cost(
            points, labels, weights1, biases1, weights2, biases2)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def step_command():
    def internal():
        global weights1, biases1, weights2, biases2
        weights1, biases1, weights2, biases2 = step(
            points, labels, weights1, biases1, weights2, biases2)
        message("{:.3f}".format(cost(
            points, labels, weights1, biases1, weights2, biases2)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def train_command():
    def internal():
        global weights1, biases1, weights2, biases2
        weights1, biases1, weights2, biases2 = train(points, labels, 2)
        message("{:.3f}".format(cost(
            points, labels, weights1, biases1, weights2, biases2)))
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
            label = classify(
                [scale*x, scale*y], weights1, biases1, weights2, biases2)
            if label<0:
                get_axes().plot([scale*x], [scale*y], "r.")
            else:
                get_axes().plot([scale*x], [scale*y], "b.")
    redraw()

def click(x, y):
    message("")
    if mode()==0:
        points.append([x, y])
        labels.append(-1)
        get_axes().plot([x], [y], "r+")
        redraw()
    elif mode()==1:
        points.append([x, y])
        labels.append(+1)
        get_axes().plot([x], [y], "b+")
        redraw()
    else:
        if len(weights1)==0:
            message("Train first")
        else:
            label = classify([x, y], weights1, biases1, weights2, biases2)
            if label<0:
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
