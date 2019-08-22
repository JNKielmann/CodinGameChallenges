import sys
import math


# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]

leftBound = 0
rightBound = w - 1
topBound = 0
bottomBound = h - 1
x, y = x0, y0

# game loop
while True:
    # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    bomb_dir = input()

    # update bounds
    if bomb_dir == "U":
        leftBound = rightBound = x
        bottomBound = y - 1
    elif bomb_dir == "UR":
        leftBound = x + 1
        bottomBound = y - 1
    elif bomb_dir == "R":
        topBound = bottomBound = y
        leftBound = x + 1
    elif bomb_dir == "DR":
        topBound = y + 1
        leftBound = x + 1
    elif bomb_dir == "D":
        leftBound = rightBound = x
        topBound = y + 1
    elif bomb_dir == "DL":
        topBound = y + 1
        rightBound = x - 1
    elif bomb_dir == "L":
        topBound = bottomBound = y
        rightBound = x - 1
    elif bomb_dir == "UL":
        rightBound = x - 1
        bottomBound = y - 1
    
    print("New bounds: ", leftBound, rightBound, topBound, bottomBound, file=sys.stderr)
    
    # update position
    x = leftBound + math.ceil((rightBound - leftBound) / 2.0)
    y = topBound + math.ceil((bottomBound - topBound) / 2.0)
    print("{} {}".format(x, y))
