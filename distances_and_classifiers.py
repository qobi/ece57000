import numpy as np

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

def unidirectional_hausdorf(distance):
    def internal(points1, points2):
        d = 0
        for point1 in points1:
            d = max(d,
                    distance(point1,
                             nearest_neighbor_classify(point1,
                                                       distance,
                                                       points2,
                                                       points2)))
        return d
    return internal

def bidirectional_hausdorf(distance):
    def internal(points1, points2):
        return max(unidirectional_hausdorf(distance)(points1, points2),
                   unidirectional_hausdorf(distance)(points2, points1))
    return internal

def unidirectional_chamfer(distance):
    def internal(points1, points2):
        d = 0
        for point1 in points1:
            d = d+distance(point1,
                           nearest_neighbor_classify(point1,
                                                     distance,
                                                     points2,
                                                     points2))
        return d
    return internal

def bidirectional_chamfer(distance):
    def internal(points1, points2):
        return (unidirectional_chamfer(distance)(points1, points2)+
                unidirectional_chamfer(distance)(points2, points1))
    return internal

def nearest_neighbor_classify(point, distance, points, labels):
    best_distance = float("inf")
    best_label = -1
    for i in range(0, len(points)):
        d = distance(point, points[i])
        if d<best_distance:
            best_distance = d
            best_label = labels[i]
    return best_label
