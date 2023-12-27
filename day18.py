#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 06:25:20 2023

@author: simon
"""
import numpy as np
from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.segmentation import flood_fill

test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""



c = test_input

with open('day18_input.txt', 'r') as f:
    c = f.read().strip()

lines = [line.split(' ') for line in c.split('\n')]


maxdist = sum([int(x) for _,x, _ in lines]) + 10

r, c = maxdist//2, maxdist//2

dir_rc = {'R': [0, 1],
          'L': [0, -1],
          'D': [1, 0],
          'U': [-1, 0]}

canvas = np.zeros([maxdist, maxdist, 3], dtype=float)

for d, steps, color in lines:
    color = to_rgb(color[1:-1])
    dr, dc = dir_rc[d]
    for step in range(int(steps)):
        r += dr
        c += dc
        canvas[r, c, :] = color

binary_canvas = (canvas.sum(-1)>0)
filled_canvas = flood_fill(binary_canvas, (maxdist//2+1, maxdist//2+1), 2)

# plt.imshow(canvas)
# plt.waitforbuttonpress()
# plt.imshow(binary_canvas)
# plt.waitforbuttonpress()
plt.imshow(filled_canvas)

print(filled_canvas.sum())


#%% part 1 shoelace
def shoelace_area(coords):
    n = len(coords)  # Number of vertices
    area = 0

    # Sum over each vertex
    for i in range(n):
        j = (i + 1) % n  # Next vertex index (with wraparound)
        area += coords[i][0] * coords[j][1]  # x[i] * y[j]
        area -= coords[j][0] * coords[i][1]  # y[i] * x[j]
        area -= coords[i][2]
        # area += coords[j][0] + coords[i][0]
        # area += coords[j][1] + coords[i][1]
    return abs(area) / 2

r, c = 0, 0
coords = []
for d, steps, color in lines:
    dr, dc = dir_rc[d]
    r += dr*int(steps)
    c += dc*int(steps)
    length = abs(dr*int(steps) + dc*int(steps))
    coords.append([r, c, length])
area = shoelace_area(coords)+1
print('part 1 shoelace:', area)

#%% part 2

dir_hex = {'0': 'R',
           '1': 'D',
           '2': 'L',
           '3': 'U'}

r, c = 0, 0
coords = []
for _, _, hexcode in lines:
    steps = int(hexcode[2:-2], 16)
    d = dir_hex[hexcode[-2]]
    dr, dc  = dir_rc[d]
    r += dr*(steps)
    c += dc*(steps)
    length = abs(dr*int(steps) + dc*int(steps))
    coords.append([r, c, length])


area = shoelace_area(coords)+1

print(area)
# 122109751411028 too low
