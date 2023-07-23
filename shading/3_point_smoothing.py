import numpy as np
from tqdm import tqdm
from scipy.signal import savgol_filter

points: list[list[int]] = np.load(
    'sorted_points.npy', allow_pickle=True).tolist()

new_points = []
for group in tqdm(points):
    ys = [y for y, _, s in group if s > 1]
    xs = [x for _, x, s in group if s > 1]
    ss = [s for _, _, s in group if s > 1]

    if len(xs) < 10:
        new_points.append(group)
        continue

    new_xs = savgol_filter(xs, 10, 3)
    new_ys = savgol_filter(ys, 10, 3)
    new_group = [[y, x, s] for y, x, s in zip(new_ys, new_xs, ss)]
    new_points.append(new_group)

np.save('smooth_points.npy', new_points)