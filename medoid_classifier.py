from distances import *
import random

def random_labels(points, k):
    return [random.randint(0, k-1) for point in points]

def points_with_label(label, points, labels):
    result = []
    for i in range(0, len(points)):
        if labels[i]==label:
            result.append(points[i])
    return result

def medoid(distance):
    def internal(points):
        return point_with_minimum_average_distance(distance)(points, points)
    return internal

def train(distance, points, labels):
    k = 0
    for i in range(0, len(points)):
        if labels[i]>k:
            k = labels[i]+1
    return [medoid(distance)(points_with_label(j, points, labels))
            for j in range(0, k)]

infinity = float("inf")

def classify(point, distance, medoids):
    best_distance = infinity
    best_label = -1
    for j in range(0, len(medoids)):
        d = distance(point, medoids[j])
        if d<best_distance:
            best_distance = d
            best_label = j
    return best_label

def reclassify_all(distance, points, medoids):
    return [classify(point, distance, medoids) for point in points]

def cost(distance, points, labels, medoids):
    return reduce(plus,
                  [reduce(plus,
                          [distance(point, medoids[j])
                           for point in points_with_label(j, points, labels)],
                          0)
                   for j in range(0, len(medoids))],
                  0)

def all_labeled(labels):
    for label in labels:
        if label==-1:
            return False
    return True

def all_labels(labels, k):
    for j in range(0, k):
        if len(points_with_label(j, labels, labels))==0:
            return False
    return True
