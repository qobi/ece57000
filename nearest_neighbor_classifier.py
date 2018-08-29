infinity = float("inf")

def classify(point, distance, points, labels):
    best_distance = infinity
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label
