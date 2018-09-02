from gui import *
from distances import *
from nearest_neighbor_classifier import *
import cv2
import numpy as np

points = []
labels = []

distance = dtw(bidirectional(chamfer(L2_vector(L2_scalar)), plus))

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

def start_recording(for_classify):
    def internal():
        if (not for_classify) or len(points)>0:
            message("")
            global camera
            camera = cv2.VideoCapture(0)
            global stop, video
            stop = False
            video = []
            def internal():
                if not stop:
                    return_value, image = camera.read()
                    edge = process(image)
                    if show_edges():
                        get_window().show_image(
                            cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
                    else:
                        get_window().show_image(image)
                    video.append(edge)
                    get_window().after(10, internal)
            internal()
    return internal

def stop_recording():
    global stop
    stop = True
    camera.release()
    return [edge_pixels(video[i]) for i in range(0, len(video), 5)]

def clear_command():
    global points, labels
    points = []
    labels = []
    message("")

def pick_up_command():
    message("")
    points.append(stop_recording())
    labels.append("Pick Up")

def put_down_command():
    message("")
    points.append(stop_recording())
    labels.append("Put Down")

def classify_command():
    message("")
    if len(points)==0:
        message("No data")
    else:
        message(classify(stop_recording(), distance, points, labels))

add_button(0, 0, "Clear", clear_command, nothing)
show_edges = add_checkbox(0, 1, "Edges?", nothing)
add_button(0, 2, "Pick Up", start_recording(False), pick_up_command)
add_button(0, 3, "Put Down", start_recording(False), put_down_command)
add_button(0, 4, "Classify", start_recording(True), classify_command)
add_button(0, 5, "Exit", done, nothing)
message = add_message(1, 0, 6)
camera = cv2.VideoCapture(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv2.CAP_PROP_FPS)
camera.release()
start_video(width, height, 2, 6)
