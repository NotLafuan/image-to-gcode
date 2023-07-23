from utils.myModule import _color_distance, _shortest_index
import numpy as np


def color_distance(colorA: tuple[int, int, int], colorB: tuple[int, int, int]) -> float:
    return _color_distance(colorA, colorB)


def shortest_index(pixel: tuple[int, int, int], colors: list[tuple[int, int, int]]) -> int:
    return _shortest_index(pixel, colors)

# def shortest_index(pixel: tuple[int, int, int], colors: list[tuple[int, int, int]]) -> int:
#     shortest = np.inf
#     for i, color in enumerate(colors):
#         dist = color_distance(pixel, color)
#         if dist < shortest:
#             shortest = dist
#             shortest_index = i
#     return shortest_index
