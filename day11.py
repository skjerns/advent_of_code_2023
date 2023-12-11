#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 19:29:41 2023

@author: simon
"""

import numpy as np
from scipy.spatial.distance import cdist

test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

c = test_input

with open('day11_input.txt', 'r') as f:
    c = f.read().strip()

universe = np.array([[x=='#' for x in line] for line in c.strip().split('\n')])



empty_rows = []
for i, row in enumerate(universe):
    if not row.any():
        empty_rows.append(i)

empty_cols = []
for i, col in enumerate(universe.T):
    if not col.any():
        empty_cols.append(i)

galaxies = [list(x) for x in list(zip(*np.where(universe)))]
for galaxy in galaxies:
    galaxy[0] += sum([galaxy[0]>x for x in empty_rows] )
    galaxy[1] += sum([galaxy[1]>y for y in empty_cols] )

# inserted = 0
# for i, col in enumerate(universe.T):
#     if not col.any():
#         # duplicate
#         expanded_universe = np.insert(expanded_universe, i+inserted, col,  axis=1)
#         inserted += 1

# np.testing.assert_array_equal(expanded_universe, universe_expanded_correct)
mindists = 0

while len(galaxies)>1:
    galaxy1 = galaxies.pop(0)
    dists = cdist([galaxy1], galaxies, metric='cityblock')[0]
    mindists += dists.sum()

print(mindists)


#%% part 2
mindists = 0
galaxies = [list(x) for x in list(zip(*np.where(universe)))]
for galaxy in galaxies:
    galaxy[0] += sum([galaxy[0]>x for x in empty_rows])*999999
    galaxy[1] += sum([galaxy[1]>y for y in empty_cols])*999999

while len(galaxies)>1:
    galaxy1 = galaxies.pop(0)
    dists = cdist([galaxy1], galaxies, metric='cityblock')[0]
    mindists += dists.sum()

print(mindists)

# 678729486878 too high
# 678728808158
# 82000292 too low