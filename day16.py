#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:32:08 2023

@author: simon
"""
import numpy as np
from joblib import Memory
import time
import sys
sys.setrecursionlimit(10000)
mem = Memory("/dev/shm/joblib")


test_input = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

grid = test_input

with open('day16_input.txt', 'r') as f:
    grid = f.read().strip()

grid = np.array([[x for x in row] for row in grid.split('\n')])

grid_energized = np.zeros(grid.shape, dtype=int)

visited = set()

# @mem.cache
def beam(r, c, d):
    if (c, r, d) in visited:
        return
    visited.add((c, r, d))
    # print(r, c, d)
    if r<0 or r>(grid.shape[0]-1):
        return
    if c<0 or c>(grid.shape[1]-1):
        return

    grid_energized[r, c] += 1
    tile = grid[r, c]
    # print(grid_energized)
    # time.sleep(0.1)
    # print(r, c, tile, d)
    # if r==7 and c==1:
        # pass
    if d=='>':
        if tile in '.-':
            beam(r, c+1, d)
        elif tile=='\\':
            beam(r+1, c, 'v')
        elif tile=='/':
            beam(r-1, c, '^')
        elif tile=='|':
            beam(r-1, c, '^')
            beam(r+1, c, 'v')

    elif d=='<':
        if tile in '.-':
            beam(r, c-1, d)
        elif tile=='\\':
            beam(r-1, c, '^')
        elif tile=='/':
            beam(r+1, c, 'v')
        elif tile=='|':
            beam(r-1, c, '^')
            beam(r+1, c, 'v')
    elif d=='^':
        if tile in '.|':
            beam(r-1, c, d)
        elif tile=='\\':
            beam(r, c-1, '<')
        elif tile=='/':
            beam(r, c+1, '>')
        elif tile=='-':
            beam(r, c+1, '>')
            beam(r, c-1, '<')
    elif d=='v':
        if tile in '.|':
            beam(r+1, c, d)
        elif tile=='\\':
            beam(r, c+1, '>')
        elif tile=='/':
            beam(r, c-1, '<')
        elif tile=='-':
            beam(r, c+1, '>')
            beam(r, c-1, '<')


beam(0, 0, '>')

print(np.sum(grid_energized>0))


#%% part 2

max_energized = 0

for r in range(grid.shape[0]):
    visited = set()
    grid_energized = np.zeros(grid.shape, dtype=int)
    beam(r, 0, '>')
    if (curr_energy:=np.sum(grid_energized>0))> max_energized:
        max_energized = curr_energy

    visited = set()
    grid_energized = np.zeros(grid.shape, dtype=int)
    beam(r, grid.shape[1]-1, '<')
    if (curr_energy:=np.sum(grid_energized>0))> max_energized:
        max_energized = curr_energy


for c in range(grid.shape[1]):
    visited = set()
    grid_energized = np.zeros(grid.shape, dtype=int)
    beam(0, c, 'v')
    if (curr_energy:=np.sum(grid_energized>0))> max_energized:
        max_energized = curr_energy

    visited = set()
    grid_energized = np.zeros(grid.shape, dtype=int)
    beam(grid.shape[0]-1, c, '^')
    if (curr_energy:=np.sum(grid_energized>0))> max_energized:
        max_energized = curr_energy


print(max_energized)
