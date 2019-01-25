import csv
from random import *
from numpy import *
import matplotlib.pyplot as plt

def read_csv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    return list(lines)

header = read_csv("Distance.csv")[0]
DistanceTable = read_csv("Distance.csv")
DistanceTable = list(map(lambda x: x[1:], DistanceTable[1:]))
for i in range(101): DistanceTable[i] = list(map(float, DistanceTable[i]))

def get_NewDistanceTable():
    NewDistanceTable = []
    for i in range(101):
        row = []
        for j in range(101):
            if i == j:
                n = 0
                row.append(n)
            elif DistanceTable[i][j] < 2:
                n = DistanceTable[i][j]
                row.append(n)
            else:
                n = DistanceTable[i][j]
                low, mode, high = n-0.8, n, n+0.8
                n = random.triangular(low, mode, high, 1)[0]
                n = round(n, 1)
                row.append(n)
        NewDistanceTable.append(row)
    return NewDistanceTable

for k in range(10):
    ofile = open("S{} - Distance.csv".format(k+1), "w")
    result = get_NewDistanceTable()
    for row in result:
        ofile.write(",".join(map(str, row)) + "\n")
    ofile.close()
