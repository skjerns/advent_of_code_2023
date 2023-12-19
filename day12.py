#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 05:54:19 2023

@author: simon
"""
from itertools import groupby, product
from tqdm import tqdm
import numpy as np
from numba import njit, jit
from functools import cache

test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


c = test_input

with open('day12_input.txt', 'r') as f:
    c = f.read().strip()


def get_n_arangements(row, groups, indent=0):
    if not '?' in row:
        # print('  '*indent, row)
        springs = [len(list(group)) for x, group in groupby(row) if x=='#']
        if springs==groups:
            # print(f'yes! valid config {row} {springs=} {groups}')
            return 1 # configuration found
        return 0
    if row.count('#')>sum(groups):
        return 0

    counts = 0
    for opt in '.#':
        rowx = row.replace('?', opt, 1)
        counts += get_n_arangements(rowx, groups, indent+1)
    return counts

arrangements = []
for line in tqdm(c.strip().split('\n')):
    row, groups = line.split(' ')
    groups = [int(x) for x in groups.split(',')]
    counts = get_n_arangements(row, groups)
    arrangements.append(counts)


print(sum(arrangements), arrangements)


#%% part 2
import stimer

def formatrow(row):
    mapping = {'.': 0, '#':1, '?':9}
    mapping = {v:k for k,v in mapping.items()}
    return ''.join([mapping[x] for x in row])

import numpy as np

def numpy_groupby(arr):
    # Find the indices where the value changes

    return groups
@profile
def get_groups(row):
    groups = []
    group = []
    for x in row:
        if x:
            group+=[x]
        else:
            groups.append(group)
            group = []
    else:
        groups.append(group)
    return [np.array(g) for g in groups]

@profile
def get_arangements(group, expected):
    if len(group)==0:
        return [0]

    group.sum()
    # is this group already complete?
    if group.sum()<=len(group):
        streak = 0
        springs = []
        for x in group:
            if x:
                streak+=1
            elif streak:
                springs += [streak]
                streak = 0
        else:
            springs += [streak]
        return [springs] # configuration found

    groups = []
    first_idx = np.argmax(group==9)
    # first the case that it is a dot and divides the row
    group = group.copy()
    group[first_idx] = 0
    groups = get_groups(group)
    for groupx in groups:
        arrangements = get_arangements(groupx, expected)
        # print(arrangements)

    # second case that it is a sharp and connects
    group[first_idx] = 1
    groups = get_groups(group)
    for groupx in groups:
        arrangements = get_arangements(groupx, expected)
        # print(arrangements)

    return None

@profile
def match_groups(group_options, expected):
    n_arrangements = 0
    for arrangement in product(*group_options):
        groups = [x for xs in arrangement for x in xs if x]
        if groups==expected:
            n_arrangements += 1
    return n_arrangements

mapping = {'.': 0, '#':1, '?':9}

arrangements = []
for line in tqdm(c.strip().split('\n')):
    row, expected = line.split(' ')
    expected = [int(x) for x in expected.split(',')]
    row = (row+'?')*5
    expected *= 5
    row = np.array([mapping[x] for x in row], dtype=np.int8)
    get_arangements(row, expected)

    arrangements.append(counts)

print(sum(arrangements))
