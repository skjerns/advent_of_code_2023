#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 10:29:21 2023

@author: simon
"""
import numpy as np

test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


c = test_input

with open('day9_input.txt', 'r') as f:
    c= f.read().strip()

def printarr(arr):
    for i, row in enumerate(arr):
        print(' '*i + ' '.join([str(x) for x in row]))

hists_finalval = []
for line in c.split('\n'):
    df = [int(x) for x in line.split(' ')]
    dfs = [df]
    while (df:=np.diff(dfs[-1])).any():
        dfs.append([x for x in df])
    dfs.append(df)
    # printarr(dfs)
    for i in range(len(dfs)-1):
        prev_df = dfs.pop(-1)
        dfs[-1].append(dfs[-1][-1] + prev_df[-1])
        # print(i, dfs)
    hists_finalval.append(dfs[-1][-1])
    #print(dfs)


print(np.sum(hists_finalval))


#%% part2

hists_finalval = []
for line in c.split('\n'):
    df = [int(x) for x in line.split(' ')]
    dfs = [df]
    while (df:=np.diff(dfs[-1])).any():
        dfs.append([x for x in df])
    dfs.append(df)
    printarr(dfs)
    for i in range(len(dfs)-1):
        prev_df = dfs.pop(-1)
        dfs[-1].insert(0, dfs[-1][0] - prev_df[0])
        print(i, dfs)
    hists_finalval.append(dfs[-1][0])
    print(dfs)


print(np.sum(hists_finalval))