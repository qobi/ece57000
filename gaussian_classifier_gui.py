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

def all_command():
    resolution = 50
    scale = 1.0/resolution
    for y in range(0, resolution+1):
        for x in range(0, resolution+1):
            labels = classify(
                [scale*x, scale*y], mixture_proportions, means, variances)
            if labels[0]>labels[1]:
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
        if len(means)==0:
            message("Train first")
        else:
            label = classify([x, y], mixture_proportions, means, variances)
            message("Red: {:.3f}, Blue: {:.3f}".format(label[0], label[1]))

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
