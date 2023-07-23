import cv2
import numpy as np
from tqdm import tqdm
from utils.color_math import color_distance, shortest_index

image = cv2.imread('shouko.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

colors = [
    '#FFFFFF',  # White
    # '#F7E942',  # Lemon Yellow
    '#FFCA00',  # Yellow
    '#F8880B',  # Orange
    # '#F2631F',  # Pale Vermillion
    # '#F4899D',  # Light Pink
    # '#E81684',  # Pink
    # '#EF5134',  # Light Red
    '#E3010D',  # Red
    # '#C23C33',  # Sanguine
    '#CF0541',  # Crimson
    # '#E794C0',  # Heliotrope
    # '#B2204F',  # Purple
    # '#BC9ACC',  # Light Lilac
    '#B2204F',  # Lilac
    '#582280',  # Violet
    # '#201559',  # Night Blue
    # '#A1DAF5',  # Ice Blue
    '#00BAE3',  # Azure
    # '#008FD5',  # Light Blue
    '#103E93',  # Dark Blue
    '#0084CF',  # Ultramarine
    '#24B6A9',  # Ice Green
    '#009bb7',  # Turquoise
    # '#005646',  # Pine Green
    # '#87C795',  # Light Emerald
    '#73B73C',  # Leaf Green
    # '#A3BF08',  # Apple Green
    '#00914C',  # Green
    '#3F5D39',  # Olive Green
    # '#67523F',  # Umber
    '#6A3F2C',  # Brown
    # '#804E37',  # Sienna
    # '#D49955',  # Light Ochre
    '#C65F1A',  # Dark Ochre
    # '#939BA6',  # Med. Cold Gray
    '#697486',  # Dark Gray
    # '#4C535B',  # Deep Cold Gray
    # '#1A416C',  # Payne’s Gray
    '#000000',  # Black
    '#B9CADA',  # Light Gray
    # '#FAAD93',  # Apricot
    # '#FEBA29',  # Fluor. Orange
    # '#FFE900',  # Fluor. Yellow
    '#F16BA8',  # Fluor. Pink
    # '#F8A7B6',  # Fluor. Red
    # '#81BF3A',  # Fluor. Green
    # '#2EC1F5',  # Fluor. Blue
]

colors = [tuple(int(hex_code.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
          for hex_code in colors]



# colors = [
#     [0,0,0],
#     [255,0,0],
#     [0,255,0],
#     [0,0,255],
#     # [255,255,255],
# ]
num_shades = 20
new_colors = []
for color in colors:
    new_colors.append(color)
    shades = np.linspace(color, [255, 255, 255], num_shades, dtype=np.uint8)[:-1].tolist()
    new_colors += shades
# new_colors.append([255, 255, 255])  # White
colors = new_colors

point_image = np.ones(image.shape, np.uint8)
point_image = 255*point_image

color_images = [255*np.ones(image.shape, np.uint8) for _ in range(len(colors)//num_shades)]

bar = tqdm(total=image.shape[0]*image.shape[1])
for j, row in enumerate(image):
    for i, pixel in enumerate(row):
        bar.update()
        index = shortest_index(pixel, colors)

        index = int(index/num_shades)
        point_image[j, i] = colors[index*num_shades]
        color_images[index][j, i] = [0, 0, 0]

for i, color_image in enumerate(color_images):
    cv2.imwrite(f'colors/{i:02d}.png', color_image)

cv2.imwrite('extract_color.png', cv2.cvtColor(point_image, cv2.COLOR_RGB2BGR))
