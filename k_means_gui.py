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

def random_labels_command():
    global labels, means
    labels = random_labels(points, 2)
    means = []
    message("")
    redisplay()

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

def reclassify_all_command():
    def internal():
        global labels
        labels = reclassify_all(points, means)
        message("{:.3f}".format(cost(points, labels, means)))
        redisplay()
    if len(means)==0:
        message("Train first")
    else:
        message("Reclassifying all")
        get_window().after(10, internal)

def loop_command():
    def internal(last_cost):
        global labels, means
        means = train(points, labels)
        labels = reclassify_all(points, means)
        this_cost = cost(points, labels, means)
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
