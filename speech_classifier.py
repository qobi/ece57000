from gui import *
import sounddevice as sd
import numpy as np
import time

sd.default.samplerate = 8000
sd.default.channels = 1
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

def classify(point, distance, points, labels):
    best_distance = float("inf")
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label

def start_recording(maximum_duration):
    def internal():
        global waveform, start_time
        message("")
        waveform = sd.rec(maximum_duration*sd.default.samplerate)
        start_time = time.time()
    return internal

def stop_recording():
    global waveform
    actual_time = time.time()-start_time
    sd.stop()
    samples = min(int(actual_time*sd.default.samplerate), len(waveform))
    waveform = waveform[0:samples, 0]
    sd.play(waveform)
    sd.wait()
    get_axes().clear()
    spectrum, freqs, t, im = get_axes().specgram(waveform,
                                                 Fs=sd.default.samplerate)
    redraw()
    return np.transpose(spectrum)

def clear_command():
    points = []
    labels = []
    message("")
    get_axes().clear()
    redraw()

def dog_command():
    message("")
    points.append(stop_recording())
    labels.append("Dog")

def cat_command():
    message("")
    points.append(stop_recording())
    labels.append("Cat")

def classify_command():
    message("")
    message(classify(stop_recording(),
                     dtw(L2_vector(L2_scalar)),
                     points,
                     labels))

add_button(0, 0, "Clear", clear_command, nothing)
add_button(0, 1, "Dog", start_recording(10), dog_command)
add_button(0, 2, "Cat", start_recording(10), cat_command)
add_button(0, 3, "Classify", start_recording(10), classify_command)
add_button(0, 4, "Exit", done, nothing)
message = add_message(1, 0, 2)
start_variable_size_matplotlib(7, 7, 2, 5)
