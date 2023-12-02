# main file

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from lian.Lian import LIAN
from lian.Point import Point

# from line_profiler import LineProfiler

RES_DIR = "res/"

image = cv.imread('resources/map.png')
Y, X = np.loadtxt('resources/points.txt', unpack=True)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray[gray > 200] = 255
gray[gray != 255] = 0

start = Point(int(X[0]), int(Y[0]))
end = Point(int(X[1]), int(Y[1]))
end = Point(400, 430)
image = np.array(gray)
image = np.ones_like(image)


# change end point for test
# end = Point(460, 450)
# end = Point(260, 460)

demo = image.copy()
demo = cv.circle(demo, (start.x, start.y), 7, (30,240,240), -1)
demo = cv.circle(demo, (end.x, end.y), 7, (30,240,240), -1)
plt.imshow(demo)
plt.show()

# k = 10

# start = Point(40//k, 500//k)
# end = Point(800//k, 500//k)

# image = np.ndarray((1000//k, 1000//k, 1), 'uint8')
# image = np.array(image)

# image[:,:] = 255
# # image[350//k:650//k, 450//k:550//k] = 0
# image[0//k:700//k, 200//k:250//k] = 0
# image[600//k:1000//k, 600//k:1000//k] = 0

# demo = image.copy()
# demo = cv.circle(demo, (start.x, start.y), 1, (30,240,240), -1)
# demo = cv.circle(demo, (end.x, end.y), 1, (30,240,240), -1)
# plt.imshow(demo)
# plt.show()

# ---- main code ----

# params -> start, end, delta, angle, map

path = LIAN(start, end, 18, 25, image, RES_DIR) # for map (big image)

# for profiler

# lp = LineProfiler()
# lp_wrapper = lp(LIAN)
# lp_wrapper(start, end, 10, 70, image, RES_DIR)
# lp.print_stats()

# path = LIAN(start, end, 10, 70, image, RES_DIR)   # for small image

pathImg = image.copy()
for point in path:
    pathImg = cv.circle(pathImg, (point.x, point.y), 1, (30,240,240), -1)

plt.imshow(pathImg)
plt.show()