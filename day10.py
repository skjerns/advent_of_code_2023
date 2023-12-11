#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 18:03:54 2023

@author: simon
"""

import networkx
import numpy as np
import matplotlib.pyplot as plt
import scipy
from skimage.segmentation import flood, flood_fill


test_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

# test_input = """.....
# .S-7.
# .|.|.
# .L-J.
# ....."""

c = test_input

with open('day10_input.txt', 'r') as f:
    c = f.read().strip()





def construct_graph(inputstring):
    graph = networkx.Graph()
    lines = inputstring.split('\n')

    nodes = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            curr_node = (y, x)
            node_up   = (y-1, x)
            node_down = (y+1, x)
            node_right  = (y, x+1)
            node_left = (y, x-1)
            if c=='|':
                nodes.append(sorted((curr_node, node_up)))
                nodes.append(sorted((curr_node, node_down)))
            elif c=='-':
                nodes.append(sorted((curr_node, node_right)))
                nodes.append(sorted((curr_node, node_left)))
            elif c=='L':
                nodes.append(sorted((curr_node, node_right)))
                nodes.append(sorted((curr_node, node_up)))
            elif c=='J':
                nodes.append(sorted((curr_node, node_up)))
                nodes.append(sorted((curr_node, node_left)))
            elif c=='7':
                nodes.append(sorted((curr_node, node_down)))
                nodes.append(sorted((curr_node, node_left)))
            elif c=='F':
                nodes.append(sorted((curr_node, node_right)))
                nodes.append(sorted((curr_node, node_down)))
            elif c=='S':
                start = curr_node
                for neighbour in [node_up, node_down, node_right, node_left]:
                    nodes.append(sorted((curr_node, neighbour)))


    nodes, counts = np.unique(nodes, axis=0, return_counts=True)

    for nodex, count in zip(nodes, counts):
        if count>1:
            node1, node2 = nodex
            graph.add_edge(tuple(node1), tuple(node2))
    return start, graph

start, graph = construct_graph(c)
print(max(dict(networkx.single_source_shortest_path_length(graph, start)).values()))

# 600 too low

#%% part 2
def connect2(ends):
    d0, d1 = np.diff(ends, axis=0)[0]
    if np.abs(d0) > np.abs(d1):
        return np.c_[np.arange(ends[0, 0], ends[1,0] + np.sign(d0), np.sign(d0), dtype=np.int32),
                     np.arange(ends[0, 1] * np.abs(d0) + np.abs(d0)//2,
                               ends[0, 1] * np.abs(d0) + np.abs(d0)//2 + (np.abs(d0)+1) * d1, d1, dtype=np.int32) // np.abs(d0)]
    else:
        return np.c_[np.arange(ends[0, 0] * np.abs(d1) + np.abs(d1)//2,
                               ends[0, 0] * np.abs(d1) + np.abs(d1)//2 + (np.abs(d1)+1) * d0, d0, dtype=np.int32) // np.abs(d1),
                     np.arange(ends[0, 1], ends[1,1] + np.sign(d1), np.sign(d1), dtype=np.int32)]

test_input1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""" # 4

test_input2 = """OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO""" # 8

test_input3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""" # 10


c = test_input1

# with open('day10_input.txt', 'r') as f:
#     c = f.read().strip()

# we can actually take the graph from above and convert the main loop
# into a numpy array
lines = c.split()
start, graph = construct_graph(c)

mainloop = set(networkx.single_source_shortest_path_length(graph, start))

for i in range(len(lines)):
    for j in range(len(lines[0])):
        graph.add_node((i, j))

networkx.draw(graph, pos={(node): [node[0], node[1]] for node in graph.nodes})

matrix = np.zeros([len(lines)*2+2, len(lines[0])*2+2], dtype=np.uint(8))

for node in mainloop:
    # offset by 1 to have edge of canvas empty
    matrix[node[0]*2+1, node[1]*2+1] = 1
plt.figure()
plt.imshow(matrix)



edges = [[tuple(x) for x in np.array(sorted(e))*2+1] for e in sorted(graph.edges)]

for edge in sorted(graph.edges):
    edge = np.array(edge)
    # print(edge)
    if any([tuple(node) in mainloop for node in edge]):
        edge = edge*2+1
        edge_sorted_x = np.array(sorted(edge, key=lambda x:x[0]))
        for dx in range(np.diff(edge.T)[0][0]):
            x = edge_sorted_x[0][0]+dx
            y = edge_sorted_x[0][1]
            if matrix[x, y]: continue
            matrix[x, y] = True
        edge_sorted_y = np.array(sorted(edge, key=lambda x:x[1]))
        for dy in range(np.diff(edge_sorted_y.T)[1][0]):
            x = edge_sorted_y[0][0]
            y = edge_sorted_y[0][1]+dy
            if matrix[x, y]: continue
            matrix[x, y] = True
            # print(x, y)
            plt.imshow(matrix, alpha=0.2)
            plt.pause(0.1)



plt.imshow(matrix, alpha=0.2)


# x = scipy.ndimage.binary_dilation(matrix)
# plt.imshow(x, alpha=0.2)
from skimage import data, filters, color, morphology
from skimage.segmentation import flood, flood_fill


checkers = data.checkerboard()
filled_checkers = flood_fill(matrix, (0, 0), 2)
plt.imshow(filled_checkers)

pixelcount = 0
for x, y in zip(*np.where(filled_checkers==0)):
    if not ((x-1)//2, (y-1)//2) in mainloop:
        pixelcount += 1

# plt.imshow(components>1)


print(f'n components not connected to outside: {pixelcount//4}')

# 391 too highe