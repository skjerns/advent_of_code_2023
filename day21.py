#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:28:20 2023

@author: simon
"""
import numpy as np
from tqdm import tqdm

test_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


content = test_input

# with open('day21_input.txt', 'r') as f:
#     c = f.read().strip()

grid = np.array([[x for x in row] for row in content.split('\n')])

curr_plots = [[int(x) for x in np.where(grid=='S')]]
grid[*curr_plots[0]] = '.'

for steps in tqdm(list(range(64))):
    next_plots = set()
    while len(curr_plots):
        r, c = curr_plots.pop()
        for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if r+dr<0 or r+dr>grid.shape[0]-1:
                continue
            if c+dc<0 or c+dc>grid.shape[1]-1:
                continue
            neighbour = grid[r+dr, c+dc]
            if neighbour=='#':
                continue
            next_plots.add((r+dr, c+dc))
    curr_plots = next_plots

print(len(set(next_plots)))


#%% part 2

# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.

grid = np.array([[x for x in row] for row in content.split('\n')])

curr_plots = [[int(x) for x in np.where(grid=='S')]]
grid[*curr_plots[0]] = '.'


seen_sets = set()
# steps = 26501365
steps = 50 # 1594 plots reachable

for steps in tqdm(list(range(steps))):
    next_plots = set()
    while len(curr_plots):
        r, c = curr_plots.pop()
        for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            # if r+dr<0 or r+dr>grid.shape[0]-1:
            #     pass
            # if c+dc<0 or c+dc>grid.shape[1]-1:
            #     pass
            next_r = (r+dr) % grid.shape[0]
            next_c = (c+dc) % grid.shape[1]

            neighbour = grid[next_r, next_c]
            if neighbour=='#':
                continue
            next_plots.add((next_r, next_c))
    curr_plots = next_plots
    sethash = hash(frozenset(curr_plots))
    # if sethash in seen_sets:
    #     raise Exception
    seen_sets.add(sethash)

print(len(set(next_plots)))


#%%
