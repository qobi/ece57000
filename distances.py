import numpy as np

def L2_scalar(p1, p2):
    return (p1-p2)*(p1-p2)

def plus(x, y):
    return x+y

def L2_vector(distance):
    def internal(p1, p2):
        return reduce(plus,
                      [distance(p1[i], p2[i]) for i in range(0, len(p1))],
                      0)
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

def dtw_with_image(distance):
    def internal(s1, s2):
        m = len(s1)
        n = len(s2)
        c = np.zeros((m, n))
        b = [[False for j in range(0, n)] for i in range(0, m)]
        image = np.ones((m, n))
        c[0, 0] = distance(s1[0], s2[0])
        for i in range(1, m):
            c[i, 0] = distance(s1[i], s2[0])+c[i-1, 0]
            b[i][0] = [i-1, 0]
        for j in range(1, n):
            c[0, j] = distance(s1[0], s2[j])+c[0, j-1]
            b[0][j] = [0, j-1]
        for i in range(1, m):
            for j in range(1, n):
                l = min(c[i-1, j], c[i, j-1], c[i-1, j-1])
                c[i, j] = distance(s1[i], s2[j])+l
                if l==c[i-1, j-1]:
                    b[i][j] = [i-1, j-1]
                elif l==c[i, j-1]:
                    b[i][j] = [i, j-1]
                elif l==c[i-1, j]:
                    b[i][j] = [i-1, j]
        i = m-1
        j = n-1
        while i>0 or j>0:
            image[i, j] = 0
            i, j = b[i][j]
        image[i, j] = 0
        return c[m-1, n-1], image
    return internal

infinity = float("inf")

def hausdorf(distance):
    def internal(points1, points2):
        return reduce(max,
                      [reduce(min,
                              [distance(point1, point2)
                                        for point2 in points2],
                              infinity)
                       for point1 in points1],
                      -infinity)
    return internal

def chamfer(distance):
    def internal(points1, points2):
        return reduce(plus,
                      [reduce(min,
                              [distance(point1, point2)
                                        for point2 in points2],
                              infinity)
                       for point1 in points1],
                      0)
    return internal

def complete_linkage(distance):
    def internal(points1, points2):
        return reduce(max,
                      [reduce(max,
                              [distance(point1, point2)
                                        for point2 in points2],
                              -infinity)
                       for point1 in points1],
                      -infinity)
    return internal

def average_linkage(distance):
    def internal(points1, points2):
        return reduce(plus,
                      [reduce(plus,
                              [distance(point1, point2)
                                        for point2 in points2],
                              0)
                       for point1 in points1],
                      0)/(len(points2)*len(points2))
    return internal

def minimum_average(distance):
    def internal(points1, points2):
        return reduce(min,
                      [reduce(plus,
                              [distance(point1, point2)
                                        for point2 in points2],
                              0)
                       for point1 in points1],
                      infinity)
    return internal

def point_with_minimum_average_distance(distance):
    def internal(points1, points2):
        best = points1[0]
        best_distance = reduce(plus,
                               [distance(points1[0], point2)
                                for point2 in points2],
                               0)
        for point1 in points1[1:]:
            this_distance = reduce(plus,
                                   [distance(point1, point2)
                                    for point2 in points2],
                                   0)
            if this_distance<best_distance:
                best = point1
                best_distance = this_distance
        return best
    return internal

def invert(distance):
    def internal(point1, point2):
        return distance(point1, point1)
    return internal

def bidirectional(distance, aggregate):
    def internal(point1, point2):
        return aggregate(distance(point1, point2),
                         invert(distance)(point1, point2))
    return internal
