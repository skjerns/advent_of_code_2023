#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:44:27 2023

@author: simon
"""
import numpy as np

test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


c = test_input
def fmt_array(arr):
    lines = [''.join(x) for x in arr]
    return '\n'.join(lines)

with open('day13_input.txt', 'r') as f:
    c = f.read().strip()


patterns = c.split('\n\n')
numbersum = 0
for pattern in patterns:
    arr = np.array([[x for x in line] for line in pattern.split('\n')])

    number = None
    for orientation in ['rows', 'columns']:
        if number: break
        if orientation=='columns':
            arr = np.flipud(np.rot90(arr))
            # print(fmt_array(arr))
        for i in range(1, len(arr)):
            # print(i, '\n')
            mirr = arr[i:i+i][::-1]
            orig = arr[i-len(mirr):i]
            # print('——————————'),
            # print(fmt_array(orig))
            # print('——————————')
            # print(fmt_array(mirr[::-1]))
            # print('——————————')
            mirrored = (mirr==orig).all()
            if mirrored:
                number = i*(100 if orientation=='rows' else 1)
                numbersum+=number
            # print(f'same at {orientation} at {i}?', mirrored)
            if mirrored:
                break
    print(number)
    # break

print(numbersum)


#%% part 2

numbersum = 0
for pattern in patterns:
    arr = np.array([[x for x in line] for line in pattern.split('\n')])

    number = None
    for orientation in ['rows', 'columns']:
        if number: break
        if orientation=='columns':
            arr = np.flipud(np.rot90(arr))
            # print(fmt_array(arr))
        for i in range(1, len(arr)):
            # print(i, '\n')
            mirr = arr[i:i+i][::-1]
            orig = arr[i-len(mirr):i]
            # print('——————————'),
            # print(fmt_array(orig))
            # print('——————————')
            # print(fmt_array(mirr[::-1]))
            # print('——————————')
            almost_mirrored = (mirr==orig).sum()==(orig.size-1)

            if almost_mirrored:
                number = i*(100 if orientation=='rows' else 1)
                numbersum+=number
            print(f'almost same at {orientation} at {i}?', almost_mirrored)
            if almost_mirrored:
                break
    print(number)
    # break

print(numbersum)
