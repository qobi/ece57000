from simple_plot import variable_size, add_button, add_click, get_a, redraw, start
import sounddevice as sd
import numpy as np

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

def record(duration):
    waveform = sd.rec(duration*sd.default.samplerate)
    sd.wait()
    waveform = waveform[:,0]
    sd.play(waveform)
    sd.wait()
    spectrum, freqs, t, im = get_a().specgram(waveform,
                                              Fs=sd.default.samplerate)
    redraw()
    return np.transpose(spectrum)

def clear_command():
    points = []
    labels = []

def dog_command():
    points.append(record(2))
    labels.append("dog")

def cat_command():
    points.append(record(3))
    labels.append("cat")

def classify_command():
    print classify(record(4), dtw(L2_vector(L2_scalar)), points, labels)

variable_size()
add_button("Clear", clear_command)
add_button("Dog", dog_command)
add_button("Cat", cat_command)
add_button("Classify", classify_command)
add_button("Exit", exit)
start()
