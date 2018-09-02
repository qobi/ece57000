from numpy.linalg import inv, det
from numpy import pi, sqrt, exp, dot, sum, product, outer, transpose, array
from random import random

def distance(x, mean, variance):
    return dot((x-mean), dot(inv(variance), (x-mean)))

def gaussian(x, mean, variance):
    coefficient = 1/sqrt((2*pi)**len(x)*det(variance))
    return coefficient*exp(-0.5*distance(x, mean, variance))

def normalize(l):
    return (1.0/sum(l))*array(l)

def random_labels(points, k):
    return [normalize([random() for j in range(0, k)]) for point in points]

def weighted_mean(weights, points):
    return ((1.0/sum(weights))*
            sum([weight*array(point)
                 for weight, point in zip(weights, points)], axis=0))

def weighted_variance(weights, mean, points):
    return ((1.0/sum(weights))*
            sum([weight*outer(point-mean, point-mean)
                 for weight, point in zip(weights, points)], axis=0))

def train(points, labels):
    mixture_proportions = normalize([sum(weights)
                                     for weights in transpose(labels)])
    means = [weighted_mean(weights, points)
             for weights in transpose(labels)]
    variances = [weighted_variance(weights, mean, points)
                 for weights, mean in zip(transpose(labels), means)]
    return mixture_proportions, means, variances

def classify(point, mixture_proportions, means, variances):
    return normalize([mixture_proportion*gaussian(point, mean, variance)
                      for mixture_proportion, mean, variance
                      in zip(mixture_proportions, means, variances)])

def reclassify_all(points, mixture_proportions, means, variances):
    return [classify(point, mixture_proportions, means, variances)
            for point in points]

def likelihood(points, mixture_proportions, means, variances):
    return product([sum([mixture_proportion*gaussian(point, mean, variance)
                         for mixture_proportion, mean, variance
                         in zip(mixture_proportions, means, variances)])
                    for point in points])

def all_labeled(labels):
    for label in labels:
        if sum(label)==0:
            return False
    return True

def all_labels(labels, k):
    if len(labels)==0:
        return False
    for j in range(0, k):
        if sum(array(labels)[:, j])==0:
            return False
    return True
