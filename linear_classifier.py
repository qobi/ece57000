from forward_mode import *
from random import uniform

def vplus(u, v):
    return [ad_plus(u[i], v[i]) for i in range(0, len(u))]

def ktimesv(k, u):
    return [ad_times(k, u[i]) for i in range(0, len(u))]

def dot(u, v):
    sum = 0
    for i in range(0, len(u)):
        sum = ad_plus(sum, ad_times(u[i], v[i]))
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
    return ad_plus(dot(weights, point), bias)

def cost(points, labels, weights, bias):
    return reduce(ad_plus,
                  [distance([linear_model(points[i], weights, bias)],
                            [labels[i]])
                   for i in range(0, len(points))],
                  0)

def pack(weights, bias):
    parameters = [bias]
    for weight in weights:
        parameters.append(weight)
    return parameters

def unpack(parameters):
    bias = parameters[0]
    weights = parameters[1:]
    return weights, bias

def initialize(points, labels):
    weights = [uniform(-1, 1) for i in range(0, len(points[0]))]
    bias = uniform(-1, 1)
    return weights, bias

def step(points, labels, weights, bias):
    def loss(parameters):
        weights, bias = unpack(parameters)
        return cost(points, labels, weights, bias)
    parameters = pack(weights, bias)
    parameters = vminus(parameters, ktimesv(0.01, gradient(loss)(parameters)))
    weights, bias = unpack(parameters)
    return weights, bias

def train(points, labels):
    def loss(parameters):
        weights, bias = unpack(parameters)
        return cost(points, labels, weights, bias)
    weights = [uniform(-1, 1) for i in range(0, len(points[0]))]
    bias = uniform(-1, 1)
    parameters = pack(weights, bias)
    parameters = naive_gradient_descent(loss, parameters, 0.01, 100)
    weights, bias = unpack(parameters)
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
