from gui import *
from distances_and_classifiers import *
import sounddevice as sd
import numpy as np
import time

sd.default.samplerate = 8000
sd.default.channels = 1
points = []
labels = []

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
    global points, labels
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
    message(nearest_neighbor_classify(stop_recording(),
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
