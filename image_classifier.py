from gui import *
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

def classify(point, distance, points, labels):
    best_distance = float("inf")
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label

def process(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0-sigma)*v))
    upper_thresh = int(min(255, (1.0+sigma)*v))
    edge = cv2.Canny(gray, lower_thresh, upper_thresh)
    return edge

def edge_pixels(image):
    m, n = image.shape
    pixels = []
    for i in range(0, m, 10):
        for j in range(0, n, 10):
            if image[i, j]>0:
                pixels.append([i,j])
    return pixels

def capture():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    camera.release()
    edge = process(image)
    if show_edges():
        get_window().show_image(cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
    else:
        get_window().show_image(image)
    return edge_pixels(edge)

def clear_command():
    points = []
    labels = []
    message("")

def cup_command():
    message("")
    points.append(capture())
    labels.append("Cup")

def box_command():
    message("")
    points.append(capture())
    labels.append("Box")

def classify_command():
    message("")
    message (classify(capture(),
                      bidirectional_chamfer_distance(L2_vector(L2_scalar)),
                      points,
                      labels))

add_button(0, 0, "Clear", clear_command, nothing)
show_edges = add_checkbox(0, 1, "Edges?", nothing)
add_button(0, 2, "Cup", cup_command, nothing)
add_button(0, 3, "Box", box_command, nothing)
add_button(0, 4, "Classify", classify_command, nothing)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 2)
message = add_message(1, 0, 2)
camera = cv2.VideoCapture(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)
camera.release()
start_video(width, height, 2, 6)
