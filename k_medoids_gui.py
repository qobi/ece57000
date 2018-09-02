from gui import *
from distances import *
from medoid_classifier import *

points = []
labels = []
medoids = []

distance = L2_vector(L2_scalar)

def redisplay():
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i]==0:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        elif labels[i]==1:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    if len(medoids)==2:
        get_axes().plot([medoids[0][0]], [medoids[0][1]], "ro")
        get_axes().plot([medoids[1][0]], [medoids[1][1]], "bo")
    redraw()

def clear_command():
    global points, labels, medoids
    points = []
    labels = []
    medoids = []
    message("")
    get_axes().clear()
    redraw()

def random_labels_command():
    global labels, medoids
    labels = random_labels(points, 2)
    medoids = []
    message("")
    redisplay()

def train_command():
    def internal():
        global medoids
        medoids = train(distance, points, labels)
        message("{:.3f}".format(cost(distance, points, labels, medoids)))
        redisplay()
    if not all_labels(labels, 2):
        message("Missing class")
    elif not all_labeled(labels):
        message("Random labels first")
    else:
        message("Training")
        get_window().after(10, internal)

def reclassify_all_command():
    def internal():
        global labels
        labels = reclassify_all(distance, points, medoids)
        message("{:.3f}".format(cost(distance, points, labels, medoids)))
        redisplay()

    if len(medoids)==0:
        message("Train first")
    else:
        message("Reclassifying all")
        get_window().after(10, internal)

def loop_command():
    def internal(last_cost):
        global labels, medoids
        medoids = train(distance, points, labels)
        labels = reclassify_all(distance, points, medoids)
        this_cost = cost(distance, points, labels, medoids)
        message("{:.3f}".format(this_cost))
        redisplay()
        if this_cost<last_cost:
            get_window().after(500, lambda: internal(this_cost))
        else:
            message("Done")
    if not all_labeled(labels):
        message("Random labels first")
    elif not all_labels(labels, 2):
        message("Missing class")
    else:
        infinity = float("inf")
        internal(infinity)

def click(x, y):
    message("")
    points.append([x, y])
    labels.append(-1)
    get_axes().plot([x], [y], "g+")
    redraw()

add_button(0, 0, "Clear", clear_command, nothing)
add_button(0, 1, "Random labels", random_labels_command, nothing)
add_button(0, 2, "Train", train_command, nothing)
add_button(0, 3, "Reclassify all", reclassify_all_command, nothing)
add_button(0, 4, "Loop", loop_command, nothing)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 6)
add_click(click)
start_fixed_size_matplotlib(7, 7, 2, 6)
