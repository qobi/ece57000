from gui import *
from linear_classifier import *

points = []
labels = []
weights = []
bias = 0

def redisplay():
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i]<0:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        else:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    if len(weights)==2:
        get_axes().plot([0, 1],
                        [-(weights[0]*0+bias)/weights[1],
                         -(weights[0]*1+bias)/weights[1]],
                        "g-")
    redraw()

def clear_command():
    global points, labels, weights, bias
    points = []
    labels = []
    weights = []
    bias = 0
    message("")
    get_axes().clear()
    redraw()

def train_command():
    def internal():
        global weights, bias
        weights, bias = train(points, labels)
        message("{:.3f}".format(cost(points, labels, weights, bias)))
        redisplay()
    if not all_labels(labels):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

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
        if len(weights)==0:
            message("Train first")
        else:
            label = classify([x, y], weights, bias)
            if label<0:
                message("Red")
            else:
                message("Blue")

add_button(0, 0, "Clear", clear_command, nothing)
mode = add_radio_button_group([[0, 1, "Red", 0],
                               [0, 2, "Blue", 1],
                               [0, 3, "Classify", 2]],
                              lambda: False)
add_button(0, 4, "Train", train_command, nothing)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 6)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 6)
