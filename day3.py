#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:27:33 2023

@author: simon
"""
import numpy as np
from scipy.ndimage import binary_dilation
from itertools import groupby

test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
lines = test_input.split()


with open('day3_input.txt', 'r') as f:
    c = f.read()

lines = c.split('\n')



matrix = np.zeros([len(lines), len(lines[0])])
mask = np.zeros([len(lines), len(lines[0])], dtype='bool')

for i, line in enumerate(lines):
    j = 0
    # first create the digits by removing all nondigit chars
    line_digitis = ''.join([x if x.isdigit() else '.' for x in line ])
    for x in line_digitis.split('.'):
        if x.isdigit():
            for _ in enumerate(x):
                matrix[i, j] = int(x)
                j+=1
        j += 1

    # then create the same for the mask
    line_mask = ''.join(['.' if x.isdigit() else x for x in line])
    j = 0
    for x in line_mask.split('.'):
        if len(x)>0:
            mask[i, j] = True
            j+=1
        j += 1

# now go through each point and look at the surrounding
# this is a stupid way to do it but it is still tractable so lets do it
summed = 0
for i, j in zip(*np.where(mask)):
    # i is the line, j is the position in the line
    for di in [-1, 0, 1]:
        if i+di<0: continue
        line = matrix[i+di]
        neighbours = line[max(j-1, 0):min(j+1, len(line))+1]
        for num, _ in groupby(neighbours):
            summed += num


print('answer' , summed)
# 546728 too high
# 557480 too high

#%% part 2

gears = [1 if x=='*' else 0 for x in c.replace('\n', '')]
gears = np.reshape(gears, [len(matrix), len(matrix)])
summed_ratios = 0
for i, j in zip(*np.where(gears)):
    # i is the line, j is the position in the line
    uniques = []
    for di in [-1, 0, 1]:
        if i+di<0: continue
        line = matrix[i+di]
        neighbours = line[max(j-1, 0):min(j+1, len(line))+1]
        for num, _ in groupby(neighbours):
            if num!=0:
                uniques += [num]
    if len(uniques)==2:
        summed_ratios += np.prod(uniques)

print('answer' , summed_ratios)