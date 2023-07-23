import cv2
import numpy as np
import math
from collections import namedtuple
import os
from tqdm import tqdm


def post_process(image: cv2.Mat, threshold: float = 0.5) -> cv2.Mat:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(gray, 255 * threshold, 255, cv2.THRESH_BINARY)[1]
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image = cv2.flip(image, 0)
    return image


def get_points(image: cv2.Mat) -> list[list[int]]:
    points: list[list[int]] = []
    bar = tqdm(total=image.shape[0]*image.shape[1])
    for j, row in enumerate(image):
        for i, pixel in enumerate(row):
            bar.update()
            if np.all(pixel == [0, 0, 0]):
                offsets = [[-1, 0],
                           [+1, 0],
                           [0, -1],
                           [0, +1]]
                surround = 0
                for y, x in offsets:
                    try:
                        value = np.all(image[j+y, i+x] == [255, 255, 255])
                        surround += int(value)
                    except:
                        pass
                if np.mean(surround) != 0:
                    points.append((j, i, surround))
    return points


def get_coords(points: list[list[int]]) -> list[list[int]]:
    arr = np.array(points)
    return np.delete(arr, 2, 1).tolist()


def sort_points(points: list[list[int]]) -> list[list[int]]:
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
        coords = get_coords(points)
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
    return new_points


def create_gcode(points: list[list[int]], image: cv2.Mat, scale: float, min_points: int = 0) -> str:
    start_gcode = '''M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration
M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate
M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration
M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate

G28 ;Home
G29 ;Auto-bed leveling

G90 ;Absolute positioning
G0 X0 Y150 Z0.1
M0 Insert pen and click

G92 E0 ;Reset Extruder
G1 Z2.0 F3000 ;Move Z Axis up
M75
'''

    end_gcode = '''G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positioning

G1 X0 Y300 ;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z
'''

    ########## OFFSETS ##########
    Offset = namedtuple('Offset', ['x', 'y'])

    height, width, _ = image.shape
    image_offset = Offset((width*scale)/2, (height*scale)/2)

    bed_size = (310, 310)
    center_offset = Offset(bed_size[0]/2, bed_size[1]/2)

    pen_offset = Offset(32.0, -27.0)
    ########## OFFSETS ##########

    gcode = ''
    for group in points:
        # skip making short lines/dots
        if len(group) < min_points:
            continue
        first_point = True
        for y, x, s in group:
            if s > 1:
                x_coord = (x*scale)+center_offset.x-image_offset.x-pen_offset.x
                y_coord = (y*scale)+center_offset.y-image_offset.y-pen_offset.y
                gcode += f'G0 X{x_coord} Y{y_coord}\n'
                if first_point:
                    first_point = False
                    gcode += f'G0 Z0\n'  # bring the pen down
        gcode += f'G0 Z2\n'  # bring the pen up
    return f'{start_gcode}\n{gcode}\n{end_gcode}'


if __name__ == '__main__':
    input_file = 'gear1.png'
    output_file = os.path.splitext(input_file)[0] + '.gcode'

    image = cv2.imread(input_file)
    image = post_process(image)
    print('Extracting points . . .')
    points = get_points(image)
    print()
    print('Sorting points . . .')
    points = sort_points(points)
    print()
    print('Generating GCode . . .')
    gcode = create_gcode(points=points, image=image, scale=0.08)

    with open(output_file, 'w+') as f:
        f.write(gcode)
