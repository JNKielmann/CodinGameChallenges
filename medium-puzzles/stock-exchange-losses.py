import sys
import math

input()
current_max = 0
highest_loss = 0
for i in input().split():
    value = int(i)
    if value >= current_max:
        current_max = value
    elif current_max - value > highest_loss:
        highest_loss = current_max - value

print(-highest_loss)
