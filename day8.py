#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:30:01 2023

@author: simon
"""


test_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

c = test_input
with open('day8_input.txt', 'r') as f:
    c = f.read().strip()



instructions, _, *lines = c.split('\n')

nodes = {line[:3]:(line[7:10], line[12:15]) for line in lines}


steps = 0
curr_node = nodes['AAA']
for instr in instructions*10000:
    next_node = curr_node[instr=='R']
    curr_node = nodes[next_node]
    print(curr_node)
    steps += 1
    if next_node=='ZZZ':
        break

print(f'{steps=}')
# 263 too low
# %%
from tqdm import tqdm
import numpy as np
# c = """LR

# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)"""

# instructions, _, *lines = c.split('\n')

# nodes = {line[:3]:(line[7:10], line[12:15]) for line in lines}

steps = 0

cycles = []

curr_nodes = [nodes[node] for node in nodes if node.endswith('A')]

for instr in tqdm(instructions*1000000):
    next_nodes = [node[instr=='R'] for node in curr_nodes]
    curr_nodes = [nodes[next_node] for next_node in next_nodes]
    # print(curr_node)
    steps += 1
    curr_nodes = []
    for node in next_nodes:
        if node.endswith('Z'):
            cycles.append([steps])
        else:
            curr_nodes.append(nodes[node])
    if len(curr_nodes)==0:
        break


lcm = np.lcm.reduce(cycles)
print(f'part 2 {lcm=}')
# 263 too low
# 8339819458498168537 too high
# %% part2 brute force just to try

steps = 0
curr_nodes = [nodes[node] for node in nodes if node.endswith('A')]

for instr in tqdm(instructions*10000000):
    next_nodes = [node[instr=='R'] for node in curr_nodes]
    curr_nodes = [nodes[next_node] for next_node in next_nodes]
    steps += 1
    if all([node.endswith('Z') for node in next_nodes]):
        break

print(f'{steps=}')
# 263 too low