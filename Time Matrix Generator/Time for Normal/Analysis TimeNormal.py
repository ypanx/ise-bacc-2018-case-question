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
    
def read_csv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    return list(lines)

data = read_csv("TimeNormal3.csv")

values = []

for i in range(101):
    for j in range(101):
        if i == j: continue
        n = data[i][j]
        n = convert_time(n)
        values.append(n)




##ofile = open("TimeDefault.csv", "w")
##for row in new_data:
##    ofile.write(",".join(row) + "\n")
##ofile.close()
