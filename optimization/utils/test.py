import itertools
import myModule
import numpy as np
import random
import math

new_coord = [2, 3]
coords = [
    [1, 4],
    [6, 5],
    [2, 5],
]

print(myModule._shortest_index(new_coord, coords))
dist_list = list(map(lambda x: math.dist(new_coord, x),
                     coords))
shortest_index = np.argmin(dist_list)
print(shortest_index)

print(myModule._neighbour_index(new_coord, coords))
offsets = [[0, 1],
           [1, 0],
           [0, -1],
           [-1, 0],
           [1, 1],
           [1, -1],
           [-1, 1],
           [-1, -1]]
index = -1
for offset in offsets:
    new_offsetted = np.add(new_coord, offset).tolist()
    if new_offsetted in coords:
        index = coords.index(new_offsetted)
        break
print(index)

table = list(itertools.product([-3, -2, -1, 0, 1, 2, 3], repeat=2))
for item in table:
    if 3 in item or -3 in item:
        print(f'{{{item[0]}, {item[1]}}},')
