from gui import *
from distances import *
from mean_classifier import *

points = []
labels = []
means = []

def redisplay():
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i]==0:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        elif labels[i]==1:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    if len(means)==2:
        get_axes().plot([means[0][0]], [means[0][1]], "ro")
        get_axes().plot([means[1][0]], [means[1][1]], "bo")
    redraw()

def clear_command():
    global points, labels, means
    points = []
    labels = []
    means = []
    message("")
    get_axes().clear()
    redraw()

def train_command():
    def internal():
        global means
        means = train(points, labels)
        message("{:.3f}".format(cost(points, labels, means)))
        redisplay()
    if not all_labels(labels, 2):
        message("Missing class")
    elif not all_labeled(labels):
        message("Random labels first")
    else:
        message("Training")
        get_window().after(10, internal)

def all_command():
    resolution = 50
    scale = 1.0/resolution
    for y in range(0, resolution+1):
        for x in range(0, resolution+1):
            label = classify([scale*x, scale*y], means)
            if label==0:
                get_axes().plot([scale*x], [scale*y], "r.")
            elif label==1:
                get_axes().plot([scale*x], [scale*y], "b.")
    redraw()

def click(x, y):
    message("")
    if mode()==0:
        points.append([x, y])
        labels.append(mode())
        get_axes().plot([x], [y], "r+")
        redraw()
    elif mode()==1:
        points.append([x, y])
        labels.append(mode())
        get_axes().plot([x], [y], "b+")
        redraw()
    else:
        if len(means)==0:
            message("Train first")
        else:
            label = classify([x, y], means)
            if label==0:
                message("Red")
            elif label==1:
                message("Blue")

add_button(0, 0, "Clear", clear_command, nothing)
mode = add_radio_button_group([[0, 1, "Red", 0],
                               [0, 2, "Blue", 1],
                               [0, 3, "Classify", 2]],
                              lambda: False)
add_button(0, 4, "Train", train_command, nothing)
add_button(0, 5, "All", all_command, nothing)
add_button(0, 6, "Exit", done, nothing)
message = add_message(1, 0, 7)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 7)
