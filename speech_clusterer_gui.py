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
    global labels, means
    means = []
    for i in range(0, len(points)):
        labels[i] = random.randint(0, 1)
    message("")

def train_command():
    def internal():
        global medoids
        medoids = train(dtw(L2_vector(L2_scalar)), points, labels)
        message("{:.6f}".format(cost(dtw(L2_vector(L2_scalar)),
                                     points,
                                     labels,
                                     medoids)))
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
        labels = reclassify_all(dtw(L2_vector(L2_scalar)), points, medoids)
        message("{:.6f}".format(cost(dtw(L2_vector(L2_scalar)),
                                     points,
                                     labels,
                                     medoids)))
    if len(medoids)==0:
        message("Train first")
    else:
        message("Reclassifying all")
        get_window().after(10, internal)

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
add_button(0, 4, "Reclassify all", reclassify_all_command, nothing)
add_button(0, 5, "Play", play_command, nothing)
add_button(0, 6, "Exit", done, nothing)
message = add_message(1, 0, 7)
start_variable_size_matplotlib(7, 7, 2, 7)
