from forward_mode import *
from random import random

def vplus(u, v):
    return [dual_plus(u[i], v[i]) for i in range(0, len(u))]

def ktimesv(k, u):
    return [dual_times(k, u[i]) for i in range(0, len(u))]

def dot(u, v):
    sum = 0
    for i in range(0, len(u)):
        sum = dual_plus(sum, dual_times(u[i], v[i]))
    return sum

def vminus(u, v):
    return vplus(u, ktimesv(-1, v))

def distance(u, v):
    return dot(vminus(u, v), vminus(u, v))

def naive_gradient_descent(f, x0, learning_rate, n):
    x = x0
    for i in range(0, n):
        x = vminus(x, ktimesv(learning_rate, gradient(f)(x)))
    return x

def linear_model(point, weights, bias):
    return dual_plus(dot(point, weights), bias)

def cost(points, labels, weights, bias):
    return reduce(dual_plus,
                  [distance([linear_model(points[i], weights, bias)],
                            [labels[i]])
                   for i in range(0, len(points))],
                  0)

def train(points, labels):
    def loss(parameters):
        bias = parameters[0]
        weights = parameters[1:]
        return cost(points, labels, weights, bias)
    parameters = naive_gradient_descent(
        loss, [random() for i in range(0, len(points[0])+1)], 0.01, 100)
    bias = parameters[0]
    weights = parameters[1:]
    return weights, bias

def classify(point, weights, bias):
    if linear_model(point, weights, bias)<0:
        return -1
    else:
        return +1

def all_labels(labels):
    red = False
    blue = False
    for label in labels:
        if label<0:
            red = True
        else:
            blue = True
    return red and blue
