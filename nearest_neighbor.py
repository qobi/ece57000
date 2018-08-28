from gui import *
from distances_and_classifiers import *

points = []
labels = []

def clear_command():
    global points, labels
    points = []
    labels = []
    message("")
    get_axes().clear()
    redraw()

def click(x, y):
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
        label = nearest_neighbor_classify([x, y],
                                          L2_vector(L2_scalar),
                                          points,
                                          labels)
        if label==0:
            message("Red")
        elif label==1:
            message("Blue")

add_button(0, 0, "Clear", clear_command, nothing)
mode = add_radio_button_group([[0, 1, "Red", 0],
                               [0, 2, "Blue", 1],
                               [0, 3, "Classify", 2]],
                              lambda: False)
add_button(0, 4, "Exit", done, nothing)
message = add_message(1, 0, 2)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 5)
