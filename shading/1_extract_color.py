import cv2
import numpy as np
from tqdm import tqdm
from utils.color_math import color_distance, shortest_index

image = cv2.imread('Makima.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

colors = [
    '#000000',  # Black
    # '#00914C',  # Green
]

colors = [tuple(int(hex_code.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
          for hex_code in colors]

point_image = np.ones(image.shape, np.uint8)
point_image = 255*point_image


new_colors = []
for color in colors:
    new_colors.append(color)
    shades = np.linspace(color, [255,255,255], 10, dtype=np.uint8)[:-1].tolist()
    new_colors += shades
new_colors.append([255, 255, 255])  # White
colors = new_colors

color_images = [255*np.ones(image.shape, np.uint8) for _ in range(len(colors))]

bar = tqdm(total=image.shape[0]*image.shape[1])
for j, row in enumerate(image):
    for i, pixel in enumerate(row):
        bar.update()
        index = shortest_index(pixel, colors)
        point_image[j, i] = colors[index]
        color_images[index][j, i] = [0, 0, 0]

for i, color_image in enumerate(color_images):
    cv2.imwrite(f'colors/{i:02d}.png', color_image)

cv2.imwrite('extract_color.png', cv2.cvtColor(point_image, cv2.COLOR_RGB2BGR))
