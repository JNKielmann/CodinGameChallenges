import sys
import math
from collections import namedtuple


def parseFloat(input: str) -> float:
    return float(input.replace(',', '.'))


class Defib:
    def __init__(self, id, name, address, phone, longitude, latitude):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.longitude = parseFloat(longitude)
        self.latitude = parseFloat(latitude)

    def distance_to(self, longitude, latitude) -> float:
        x = (longitude - self.longitude) * \
            math.cos((latitude + self.latitude)*0.5)
        y = (latitude - self.latitude)
        return math.sqrt(x*x + y*y) * 6371


lon = parseFloat(input())
lat = parseFloat(input())
n = int(input())
defibs = []
for i in range(n):
    defib_data = str(input()).split(";")
    defibs.append(Defib(*defib_data))

defib_distances = [defib.distance_to(lon, lat) for defib in defibs]
closest_defib = min(zip(defib_distances, defibs))
print(closest_defib[1].name)