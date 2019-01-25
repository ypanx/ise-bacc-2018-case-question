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
##
##ofile = open("Origin_Destination.csv", "w")
##ofile.write("Request,Origin,Destination,Distance\n")
##n = 1
##for row in result:
##    ofile.write(str(n) + "," + ",".join(map(str, row)) + "\n")
##    n += 1
##ofile.close()
##
##print(sum(x[2] for x in result)/1000)
