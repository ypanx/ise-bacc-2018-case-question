import csv
from random import *
from numpy import *
import matplotlib.pyplot as plt

def read_csv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    return list(lines)

DistanceTable = read_csv("Distance 1.csv")
DistanceTable = list(map(lambda x: x[1:], DistanceTable[1:]))
for i in range(101): DistanceTable[i] = list(map(float, DistanceTable[i]))

values = []
for i in range(101):
    for j in range(101):
        if i != j:
            values.append(DistanceTable[i][j])
