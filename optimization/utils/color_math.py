from utils.myModule import _color_distance, _shortest_index


def color_distance(colorA: tuple[int, int, int], colorB: tuple[int, int, int]) -> float:
    return _color_distance(colorA, colorB)


def shortest_index(pixel: tuple[int, int, int], colors: list[tuple[int, int, int]]) -> int:
    return _shortest_index(pixel, colors)
