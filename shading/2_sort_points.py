import numpy as np
from tqdm import tqdm
import math


def get_coords() -> list[list[int]]:
    arr = np.array(points)
    return np.delete(arr, 2, 1).tolist()


points: list[list[int]] = np.load('points.npy').tolist()
bar = tqdm(total=len(points))
new_points: list[list[int]] = [[points.pop(0)]]
bar.update()
while len(points):
    offsets = [[0, 1],
               [1, 0],
               [0, -1],
               [-1, 0],
               [1, 1],
               [1, -1],
               [-1, 1],
               [-1, -1]]

    new_coord = new_points[-1][-1][:2]
    coords = get_coords()
    found = False
    for offset in offsets:
        new_offsetted = np.add(new_coord, offset).tolist()
        if new_offsetted in coords:
            found = True
            index = coords.index(new_offsetted)
            new_points[-1].append(points.pop(index))
            bar.update()
            break
    # no surrounding pixel
    if not found:
        dist_list = list(map(lambda x: math.dist(new_coord, x),
                             coords))
        shortest_index = np.argmin(dist_list)

        new_points.append([points.pop(shortest_index)])
        bar.update()

np.save('sorted_points.npy', new_points)
