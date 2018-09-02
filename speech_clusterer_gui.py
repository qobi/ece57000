from gui import *
from distances import *
from medoid_classifier import *
import sounddevice as sd
import numpy as np
import time

sd.default.samplerate = 8000
sd.default.channels = 1
waveforms = []
points = []
labels = []
medoids = []

distance = dtw(L2_vector(L2_scalar))

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
    get_axes().clear()
    spectrum, freqs, t, im = get_axes().specgram(waveform,
                                                 Fs=sd.default.samplerate)
    redraw()
    sd.play(waveform)
    time.sleep(float(len(waveform))/sd.default.samplerate)
    return waveform, np.transpose(spectrum)

def clear_command():
    global waveforms, points, labels, medoids
    waveforms = []
    points = []
    labels = []
    medoids = []
    message("")
    get_axes().clear()
    redraw()

def record_command():
    message("")
    waveform, spectrogram = stop_recording()
    waveforms.append(waveform)
    points.append(spectrogram)
    labels.append(-1)

def random_labels_command():
    global labels, medoids
    labels = random_labels(points, 2)
    medoids = []
    message("")

def train_command():
    def internal():
        global medoids
        medoids = train(distance, points, labels)
        message("{:.6f}".format(cost(distance, points, labels, medoids)))
    if not all_labels(labels, 2):
        message("Missing class")
    elif not all_labeled(labels):
        message("Random labels first")
    else:
        message("Training")
        get_window().after(10, internal)

def reclassify_all_command():
    def internal():
        global labels
        labels = reclassify_all(distance, points, medoids)
        message("{:.6f}".format(cost(distance, points, labels, medoids)))
    if len(medoids)==0:
        message("Train first")
    else:
        message("Reclassifying all")
        get_window().after(10, internal)

def loop_command():
    def internal(last_cost):
        global labels, medoids
        medoids = train(distance, points, labels)
        labels = reclassify_all(distance, points, medoids)
        this_cost = cost(distance, points, labels, medoids)
        message("{:.6f}".format(this_cost))
        if this_cost<last_cost:
            get_window().after(500, lambda: internal(this_cost))
        else:
            message("Done")
    if not all_labeled(labels):
        message("Random labels first")
    elif not all_labels(labels, 2):
        message("Missing class")
    else:
        infinity = float("inf")
        internal(infinity)

def play_command():
    for i in range(0, len(waveforms)):
        if labels[i]==0:
            message("Dog")
        elif labels[i]==1:
            message("Cat")
        else:
            message("Unlabeled")
        get_axes().clear()
        spectrum, freqs, t, im = get_axes().specgram(
            waveforms[i], Fs=sd.default.samplerate)
        redraw()
        sd.play(waveforms[i])
        time.sleep(float(len(waveforms[i]))/sd.default.samplerate+1)

add_button(0, 0, "Clear", clear_command, nothing)
add_button(0, 1, "Record", start_recording(10), record_command)
add_button(0, 2, "Random labels", random_labels_command, nothing)
add_button(0, 3, "Train", train_command, nothing)
add_button(1, 0, "Reclassify all", reclassify_all_command, nothing)
add_button(1, 1, "Loop", loop_command, nothing)
add_button(1, 2, "Play", play_command, nothing)
add_button(1, 3, "Exit", done, nothing)
message = add_message(2, 0, 4)
start_variable_size_matplotlib(7, 7, 3, 4)
