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

def dtw(distance):
    def internal(s1, s2):
        m = len(s1)
        n = len(s2)
        c = np.zeros((m, n))
        c[0, 0] = distance(s1[0], s2[0])
        for i in range(1, m):
            c[i, 0] = distance(s1[i], s2[0])+c[i-1, 0]
        for j in range(1, n):
            c[0, j] = distance(s1[0], s2[j])+c[0, j-1]
        for i in range(1, m):
            for j in range(1, n):
                c[i, j] = distance(s1[i], s2[j])+min(c[i-1, j],
                                                     c[i, j-1],
                                                     c[i-1, j-1])
        return c[m-1, n-1]
    return internal

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

def start_recording(ignore):
    message("")
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 15)
    global stop, video
    stop = False
    video = []
    def internal():
        if not stop:
            return_value, image = camera.read()
            get_a().imshow(image)
            redraw()
            video.append(image)
            task().after(10, internal)
    internal()

def stop_recording():
    global stop
    stop = True
    camera.release()
    for image in video:
        get_a().imshow(process(image), cmap="gray")
        redraw()
    return [edge_pixels(process(image)) for image in video]

def clear_command(ignore):
    points = []
    labels = []
    message("")
    get_a().clear()
    redraw()

def pick_up_command(ignore):
    message("")
    points.append(stop_recording())
    labels.append("Pick Up")

def put_down_command(ignore):
    message("")
    points.append(stop_recording())
    labels.append("Put Down")

def classify_command(ignore):
    message("")
    message(classify(stop_recording(),
                     dtw(bidirectional_chamfer_distance(L2_vector(L2_scalar))),
                     points,
                     labels))

variable_size()
add_button(0, 0, "Clear", clear_command, nothing)
add_button(0, 1, "Pick Up", start_recording, pick_up_command)
add_button(0, 2, "Put Down", start_recording, put_down_command)
add_button(0, 3, "Classify", start_recording, classify_command)
add_button(0, 4, "Exit", done, nothing)
message = add_message(1, 0, 2)
start(7, 7, 2, 5)
