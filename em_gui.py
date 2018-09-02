from gui import *
from em import *
from numpy.linalg import eigh
from numpy import sqrt, sin, cos, arctan2, radians

points = []
labels = []
mixture_proportions = []
means = []
variances = []

def redisplay():
    get_axes().clear()
    get_axes().clear()
    for i in range(0, len(points)):
        if labels[i][0]>labels[i][1]:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        elif labels[i][0]<=labels[i][1]:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
    if len(means)==2:
        for j in range(0, 2):
            ellipse_x = []
            ellipse_y = []
            w, v = eigh(variances[j])
            x0 = means[j][0]
            y0 = means[j][1]
            t0 = arctan2(variances[j][1, 0], w[0]-variances[j][1, 1])
            a = sqrt(2*w[0])
            b = sqrt(2*w[1])
            rxx = cos(t0)
            rxy = -sin(t0)
            ryx = -rxy
            ryy = rxx
            for l in range(0, 37):
                x = a*sin(radians(10*l))
                y = b*cos(radians(10*l))
                ellipse_x.append(rxx*x+rxy*y+x0)
                ellipse_y.append(ryx*x+ryy*y+y0)
            if j==0:
                color = "r"
            else:
                color = "b"
            get_axes().plot(ellipse_x, ellipse_y, color)
    redraw()

def clear_command():
    global points, labels, mixture_proportions, means, variances
    points = []
    labels = []
    mixture_proportions = []
    means = []
    variances = []
    message("")
    get_axes().clear()
    redraw()

def random_labels_command():
    global labels, mixture_proportions, means, variances
    labels = random_labels(points, 2)
    mixture_proportions = []
    means = []
    variances = []
    message("")
    redisplay()

def train_command():
    def internal():
        global mixture_proportions, means, variances
        mixture_proportions, means, variances = train(points, labels)
        message("{:.3e}".format(
            likelihood(points, mixture_proportions, means, variances)))
        redisplay()
    if not all_labeled(labels):
        message("Random labels first")
    elif not all_labels(labels, 2):
        message("Missing class")
    else:
        message("Training")
        get_window().after(10, internal)

def reclassify_all_command():
    def internal():
        global labels
        labels = reclassify_all(points, mixture_proportions, means, variances)
        message("{:.3e}".format(
            likelihood(points, mixture_proportions, means, variances)))
        redisplay()
    if len(means)==0:
        message("Train first")
    else:
        message("Reclassifying all")
        get_window().after(10, internal)

def loop_command():
    infinity = float("inf")
    def internal(last_likelihood):
        global labels, mixture_proportions, means, variances
        mixture_proportions, means, variances = train(points, labels)
        labels = reclassify_all(points, mixture_proportions, means, variances)
        this_likelihood = likelihood(
            points, mixture_proportions, means, variances)
        message("{:.3e}".format(this_likelihood))
        redisplay()
        if (last_likelihood==-infinity or
            (this_likelihood-last_likelihood)/last_likelihood>1e-3):
            get_window().after(500, lambda: internal(this_likelihood))
        else:
            message("Done")
    if not all_labeled(labels):
        message("Random labels first")
    elif not all_labels(labels, 2):
        message("Missing class")
    else:
        internal(-infinity)

def click(x, y):
    message("")
    points.append([x, y])
    labels.append([0, 0])
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
