from gui import *
from distances import *
from nearest_neighbor_classifier import *

points = []
labels = []

distance = L2_vector(L2_scalar)

def clear_command():
    global points, labels
    points = []
    labels = []
    message("")
    get_axes().clear()
    redraw()

def all_command():
    resolution = 50
    scale = 1.0/resolution
    for y in range(0, resolution+1):
        for x in range(0, resolution+1):
            label = classify([scale*x, scale*y], distance, points, labels)
            if label==0:
                get_axes().plot([scale*x], [scale*y], "r.")
            else:
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
        if len(points)==0:
            message("No data")
        else:
            label = classify([x, y], distance, points, labels)
            if label==0:
                message("Red")
            elif label==1:
                message("Blue")

add_button(0, 0, "Clear", clear_command, nothing)
mode = add_radio_button_group([[0, 1, "Red", 0],
                               [0, 2, "Blue", 1],
                               [0, 3, "Classify", 2]],
                              lambda: False)
add_button(0, 4, "All", all_command, nothing)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 6)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 6)
