from gui import *

points = []
labels = []

def distance(p1, p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])

def classify(point, points, labels):
    best_distance = float("inf")
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label

def clear_command(ignore):
    global points, labels
    points = []
    labels = []
    message("")
    get_a().clear()
    redraw()

def click(x, y):
    if mode()==0:
        points.append([x, y])
        labels.append(mode())
        get_a().plot([x], [y], "r+")
        redraw()
    elif mode()==1:
        points.append([x, y])
        labels.append(mode())
        get_a().plot([x], [y], "b+")
        redraw()
    else:
        label = classify([x, y], points, labels)
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
start(7, 7, 2, 5)
