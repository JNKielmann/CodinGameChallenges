import sys
import math

w, h = [int(i) for i in input().split()]
maze = []
labels_top = input().split()
for i in range(h-2):
    connections = ' ' + input()[1::3] + ' '
    line = []
    for j in range(len(labels_top)):
        if connections[j] == '-':
            line.append(j-1)
        elif connections[j+1] == '-':
            line.append(j+1)
        else:
            line.append(j)
    maze.append(line)
labels_bot = input().split()

for i in range(len(labels_top)):
    current_index = i
    for j in range(h-2):
        current_index = maze[j][current_index]
    print(labels_top[i] + labels_bot[current_index])
