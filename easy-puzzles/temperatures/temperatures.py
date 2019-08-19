import sys
import math

input() # skip as n is not needed
temps = [int(temp) for temp in input().split()]
closest_to_zero = min(temps, key=lambda x: (abs(x), -x), default = 0)
print(closest_to_zero)