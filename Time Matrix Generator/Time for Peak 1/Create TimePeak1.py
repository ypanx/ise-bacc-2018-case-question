import csv
from numpy import *
import matplotlib.pyplot as plt

def convert_time(string):
    hour, minute = string.split(":")
    return int(hour) * 60 + int(minute)

def convert_time_back(integer):
    hour = integer//60
    hour = ("00" + str(hour))[-2:]
    minutes = integer % 60
    minutes = ("00" + str(minutes))[-2:]
    return hour + ":" + minutes

PeakOneTimeData = []
for k in range(10):
    Data = []
    for i in range(101):
        row = []
        for j in range(101):
            row.append(convert_time_back(0))
        Data.append(row)
    PeakOneTimeData.append(Data)
    
def read_csv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    return list(lines)

data = read_csv("TimeDefault.csv")

for i in range(101):
    for j in range(101):
        n = data[i][j]
        if (i == j):
            nlist = [n] * 10
        else:
            n = convert_time(n)
            low, mode, high = n-1, n+7, n+12
            nlist = list(random.triangular(low, mode, high, 10))
            nlist = list(map(lambda x: convert_time_back(int(round(x))), nlist))
        for k in range(10):
           PeakOneTimeData[k][i][j] = nlist[k]
                     
for k in range(10):
    Data = PeakOneTimeData[k]
    ofile = open("S{} - Time Peak One.csv".format(k+1), "w")
    for row in Data:
        ofile.write(",".join(row) + "\n")
    ofile.close()
