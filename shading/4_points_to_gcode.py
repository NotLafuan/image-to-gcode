import numpy as np
from tqdm import tqdm
import cv2
from collections import namedtuple

points: list[list[int]] = np.load(
    'sorted_points.npy', allow_pickle=True).tolist()

scale = 0.08

image = cv2.imread('black.png')

########## OFFSETS ##########
Offset = namedtuple('Offset', ['x', 'y'])

height, width, channel = image.shape
image_offset = Offset((width*scale)/2, (height*scale)/2)

bed_size = (310, 310)
center_offset = Offset(bed_size[0]/2, bed_size[1]/2)

pen_offset = Offset(32.0, -27.0)
########## OFFSETS ##########

start_gcode = '''M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration
M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate
M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration
M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate

;G28 ;Home

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

gcode = ''
point_image = np.ones(image.shape, np.uint8)
point_image = 255*point_image
for group in tqdm(points):
    if len(group) <= 5:
        continue
    first_point = True
    for y, x, s in group:
        point_image[int(y), int(x)] = [0, 0, 0]
        if s > 1:
            x_coord = (x*scale)+center_offset.x-image_offset.x-pen_offset.x
            y_coord = (y*scale)+center_offset.y-image_offset.y-pen_offset.y
            gcode += f'G0 X{round(x_coord, 4)} Y{round(y_coord, 4)}\n'
            if first_point:
                first_point = False
                gcode += f'G0 Z0\n'  # bring the pen down
    gcode += f'G0 Z2\n'  # bring the pen up
cv2.imwrite('point.png', point_image)
# save the gcode
with open('out.gcode', 'w+') as f:
    f.write(f'{start_gcode}\n{gcode}\n{end_gcode}')
