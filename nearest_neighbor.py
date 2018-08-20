from simple_plot import add_button, add_click, get_a, redraw, start

mode = 0
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

def clear_command():
    global points, labels
    points = []
    labels = []
    get_a().clear()
    redraw()

def red_command():
    global mode
    mode = 0

def blue_command():
    global mode
    mode = 1

def classify_command():
    global mode
    mode = 2

def click(x, y):
    if mode==0:
        points.append([x, y])
        labels.append(mode)
        get_a().plot([x], [y], "r+")
        redraw()
    elif mode==1:
        points.append([x, y])
        labels.append(mode)
        get_a().plot([x], [y], "b+")
        redraw()
    else:
        label = classify([x, y], points, labels)
        if label==0:
            print "Red"
        elif label==1:
            print "Blue"

add_button("Clear", clear_command)
add_button("Red", red_command)
add_button("Blue", blue_command)
add_button("Classify", classify_command)
add_button("Exit", exit)
add_click(click)
start()
