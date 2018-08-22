from simple_plot import variable_size, add_button, add_click, get_a, redraw, start
import cv2
import numpy as np

points = []
labels = []

def L2_scalar(p1, p2):
    return (p1-p2)*(p1-p2)

def L2_vector(distance):
    def internal(p1, p2):
        d = 0
        for i in range(0, len(p1)):
            d = d+distance(p1[i], p2[i])
        return d
    return internal

def classify(point, distance, points, labels):
    best_distance = float("inf")
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label

def unidirectional_hausdorf_distance(distance):
    def internal(points1, points2):
        d = 0
        for point1 in points1:
            d = max(d,
                    distance(point1,
                             classify(point1, distance, points2, points2)))
        return d
    return internal

def bidirectional_hausdorf_distance(distance):
    def internal(points1, points2):
        return max(unidirectional_hausdorf_distance(distance)(points1, points2),
                   unidirectional_hausdorf_distance(distance)(points2, points1))
    return internal

def unidirectional_chamfer_distance(distance):
    def internal(points1, points2):
        d = 0
        for point1 in points1:
            d = d+distance(point1,
                           classify(point1, distance, points2, points2))
        return d
    return internal

def bidirectional_chamfer_distance(distance):
    def internal(points1, points2):
        return (unidirectional_chamfer_distance(distance)(points1, points2)+
                unidirectional_chamfer_distance(distance)(points2, points1))
    return internal

def edge_pixels(a):
    m, n = a.shape
    pixels = []
    for i in range(0, m, 10):
        for j in range(0, n, 10):
            if a[i, j]>0:
                pixels.append([i,j])
    return pixels

def capture():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    camera.release()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0-sigma)*v))
    upper_thresh = int(min(255, (1.0+sigma)*v))
    edge = cv2.Canny(gray, lower_thresh, upper_thresh)
    get_a().imshow(edge, cmap="gray")
    redraw()
    return edge_pixels(edge)

def clear_command():
    points = []
    labels = []

def cup_command():
    points.append(capture())
    labels.append("cup")

def box_command():
    points.append(capture())
    labels.append("box")

def classify_command():
    print classify(capture(),
                   bidirectional_chamfer_distance(L2_vector(L2_scalar)),
                   points,
                   labels)

variable_size()
add_button("Clear", clear_command)
add_button("Cup", cup_command)
add_button("Box", box_command)
add_button("Classify", classify_command)
add_button("Exit", exit)
start()
