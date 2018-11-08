import torch
from torch.autograd import Variable
import torch.nn as nn
import numpy as np

def two_layer_perceptron(
        number_of_features, number_of_hidden, number_of_classes):
    network = nn.Sequential(
	nn.Linear(number_of_features, number_of_hidden),
	nn.ReLU(),
	nn.Linear(number_of_hidden, number_of_classes),
	nn.Softmax(dim=1))
    return network.cuda()

def cost(points, labels, network, criterion):
    points = torch.FloatTensor(points).cuda()
    labels = torch.FloatTensor(labels).cuda()
    predictions = network.forward(points)
    loss = criterion(predictions, labels)
    return loss.cpu().detach().numpy()

def initialize(number_of_features, number_of_hidden, number_of_classes):
    return two_layer_perceptron(
        number_of_features, number_of_hidden, number_of_classes)

def step(points, labels, network, criterion, batch_size, learning_rate):
    number_of_samples = len(points)
    start = 0
    while start<number_of_samples:
	end = min(start+batch_size, number_of_samples)
	points1 = Variable(torch.FloatTensor(points[start:end]).cuda())
	labels1 = Variable(torch.FloatTensor(labels[start:end]).cuda())
	predictions = network.forward(points1)
	loss = criterion(predictions, labels1)
	loss.backward()
	for W in network.parameters():
	    W.data = W.data-learning_rate*W.grad.data
	start += batch_size

def train(points, labels, network, criterion, batch_size, learning_rate):
    for i in range(1000):
        step(points, labels, network, criterion, batch_size, learning_rate)

def classify(point, network):
    points = torch.FloatTensor(point).unsqueeze(0).cuda()
    predictions = network.forward(points)
    if predictions[0][0]>predictions[0][1]:
        return 0
    else:
        return 1

def all_labels(labels):
    red = False
    blue = False
    for label in labels:
        if label[0]>label[1]:
            red = True
        else:
            blue = True
    return red and blue
