from gui import *

points = []
labels = []
means = []

def distance(p1, p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])

def vplus(p1, p2):
    return [p1[0]+p2[0], p1[1]+p2[1]]

def ktimesv(k, p):
    return [k*p[0], k*p[1]]

def train(points, labels):
    k = 0
    for i in range(0, len(points)):
        if labels[i]>k:
            k = labels[i]+1
    means = []
    for j in range(0, k):
        mean = [0, 0]
        count = 0
        for i in range(0, len(points)):
            if labels[i]==j:
                mean = vplus(mean, points[i])
                count = count+1
        mean = ktimesv(1.0/count, mean)
        means.append(mean)
    return means

def classify(point, means):
    best_distance = float("inf")
    best_label = -1
    for j in range(0, len(means)):
        d = distance(point, means[j])
        if d<best_distance:
            best_distance = d
            best_label = j
    return best_label

def clear_command(ignore):
    global points, labels
    points = []
    labels = []
    message("")
    get_a().clear()
    redraw()

def train_command(ignore):
    global means
    means = train(points, labels)
    get_a().clear()
    for i in range(0, len(points)):
        if labels[i]==0:
            get_a().plot([points[i][0]], [points[i][1]], "r+")
        elif labels[i]==1:
            get_a().plot([points[i][0]], [points[i][1]], "b+")
    get_a().plot([means[0][0]], [means[0][1]], "ro")
    get_a().plot([means[1][0]], [means[1][1]], "bo")
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
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 2)
add_click(click)
start(7, 7, 2, 6)
