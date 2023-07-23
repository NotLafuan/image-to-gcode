import cv2
import numpy as np
from tqdm import tqdm

image = cv2.imread('black.png')
image: cv2.Mat = cv2.flip(image, 0)


point_image = np.ones(image.shape, np.uint8)
point_image = 255*point_image

points = []
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
                point_image[j, i] = [0, 0, 0]
                points.append((j, i, surround))
np.save('points.npy', points)

cv2.imwrite('out2.png', point_image)
