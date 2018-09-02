from gui import *
from distances import *
from nearest_neighbor_classifier import *
import cv2
import numpy as np

points = []
labels = []

distance = bidirectional(chamfer(L2_vector(L2_scalar)), plus)

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
    global points, labels
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
    if len(points)==0:
        message("No data")
    else:
        message(classify(capture(), distance, points, labels))

add_button(0, 0, "Clear", clear_command, nothing)
show_edges = add_checkbox(0, 1, "Edges?", nothing)
add_button(0, 2, "Cup", cup_command, nothing)
add_button(0, 3, "Box", box_command, nothing)
add_button(0, 4, "Classify", classify_command, nothing)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 6)
camera = cv2.VideoCapture(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)
camera.release()
start_video(width, height, 2, 6)
