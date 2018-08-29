from gui import *
from distances import *
from nearest_neighbor_classifier import *
import sounddevice as sd
import numpy as np
import time

sd.default.samplerate = 8000
sd.default.channels = 1
points1 = []
points2 = []

def start_recording(maximum_duration, for_classify):
    def internal():
        if (not for_classify) or len(points)>0:
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
    get_axes().clear()
    spectrum, freqs, t, im = get_axes().specgram(waveform,
                                                 Fs=sd.default.samplerate)
    redraw()
    sd.play(waveform)
    time.sleep(float(len(waveform))/sd.default.samplerate)
    return np.transpose(spectrum)

def dog_command():
    message("")
    global points1
    points1 = stop_recording()

def cat_command():
    message("")
    global points2
    points2 = stop_recording()

def distance_command():
    message("")
    if len(points1)==0 or len(points2)==0:
        message("No data")
    else:
        d, image = dtw_with_image(L2_vector(L2_scalar))(points1, points2)
        message("{:.6f}".format(d))
        get_axes().imshow(image, cmap="gray")
    redraw()

add_button(0, 0, "Dog", start_recording(10, False), dog_command)
add_button(0, 1, "Cat", start_recording(10, False), cat_command)
add_button(0, 2, "Distance", distance_command, nothing)
add_button(0, 3, "Exit", done, nothing)
message = add_message(1, 0, 4)
start_variable_size_matplotlib(7, 7, 2, 4)
