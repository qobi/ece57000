from gui import *
import cv2
import numpy as np
import random

images = []
points = []
labels = []
medoids = []

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
    return image, edge_pixels(edge)

def clear_command():
    global images, points, labels, medoids
    images = []
    points = []
    labels = []
    medoids = []
    message("")

def capture_command():
    message("")
    image, edge_pixels = capture()
    images.append(image)
    points.append(edge_pixels)
    labels.append(-1)

def random_labels_command():
    global labels, means
    means = []
    for i in range(0, len(points)):
        labels[i] = random.randint(0, 1)

def train_command():
    return

def reclassify_all_command():
    return

def show(i):
    if i<len(images):
        if labels[i]==0:
            message("Cup")
        else:
            message("Box")
        if show_edges():
            edge = process(images[i])
            get_window().show_image(cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
        else:
            get_window().show_image(images[i])
        get_window().after(1000, lambda: show(i+1))

def show_command():
    show(0)

add_button(0, 0, "Clear", clear_command, nothing)
show_edges = add_checkbox(0, 1, "Edges?", nothing)
add_button(0, 2, "Capture", capture_command, nothing)
add_button(0, 3, "Random labels", random_labels_command, nothing)
add_button(1, 0, "Train", train_command, nothing)
add_button(1, 1, "Reclassify all", reclassify_all_command, nothing)
add_button(1, 2, "Show", show_command, nothing)
add_button(1, 3, "Exit", done, nothing)
message = add_message(2, 0, 2)
camera = cv2.VideoCapture(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)
camera.release()
start_video(width, height, 3, 4)
