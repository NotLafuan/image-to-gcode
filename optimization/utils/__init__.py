import utils.myModule

def shortest_index(new_coord:list[int], coords:list[list[int]]) -> int:
    return myModule._shortest_index(new_coord, coords)

def neighbour_index(new_coord:list[int], coords:list[list[int]]) -> int:
    return myModule._neighbour_index(new_coord, coords)
