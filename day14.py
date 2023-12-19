#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 10:46:20 2023

@author: simon
"""
import numpy as np
from tqdm import tqdm
from joblib import Memory

mem = Memory("/dev/shm/joblib", verbose=0)
mem.clear()

test_input = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""



board_orig = test_input
with open('day14_input.txt', 'r') as f:
    board_orig = f.read().strip()

def int2board(board_int):

    board_str = np.zeros(board_int.shape, dtype='<U1')
    for r, row in enumerate(board_int):
        for c, num in enumerate(row):
            if str(num).endswith('99'):
                x = '.'
            elif str(num).endswith('1'):
                x = 'O'
            else:
                x = '#'
            board_str[r, c] = x
    return board_str

def board_count(board_str):

    res = [np.unique(row, return_counts=True, axis=0) for i, row in enumerate(board_str)]
    load = 0
    for i, (uniques, counts) in enumerate(res[::-1], 1):
        if not 'O' in uniques: continue
        rocks = counts[uniques=='O'][0]
        load += rocks*i
    return load

@mem.cache
def tilt(board, direction='north'):
    # rotate board by x to have specific direction to the left
    # i.e. we need to move all rocks to the left   #

    rot = {'north': 1,
           'west': 0,
           'east': 2,
           'south': 3}[direction]

    board_rot = np.rot90(board, rot)

    board_int = np.zeros(board_rot.shape, dtype=int)
    for r, row in enumerate(board_rot):
        stoppers = 0
        for c, pos in enumerate(row):
            if pos=='.':
                board_int[r, c] = (99 + stoppers*1000)
            elif pos=='O':
                board_int[r, c] = (1 + stoppers*1000)
            elif pos=='#':
                stoppers += 1
                board_int[r, c] = (stoppers*1000)

    board_int.sort()
    board_int = np.rot90(board_int, -rot)

    return int2board(board_int)
#%% part1
board = np.array([[y for y in x] for x in board_orig.strip().split('\n')])
board = tilt(board, direction='north')
print(board)
print(board_count(board))


#%% part 2
mem.clear()

board = np.array([[y for y in x] for x in board_orig.strip().split('\n')])

foundloop = False
directions = ['north', 'west', 'south', 'east']
i = 0
n_cycles = 1000000000
while i <= n_cycles:
    i+=1
    # print(i)
    for rot, direction in enumerate(directions):
        already_computed = tilt.check_call_in_cache(board, direction)
        if not foundloop and already_computed and direction=='north':
            foundloop = True
            i-=4
            new_i  = i * (n_cycles//i)
            print(f'loop found after {i} cycles')
            print(f'setting {i=} to {new_i}')
            i = new_i
        board = tilt(board, direction)
    # print(board)

    # input()


print(board)
print(board_count(board))

# 102507 too low
