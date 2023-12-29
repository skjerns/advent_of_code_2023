#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:02:05 2023

@author: simon
"""
import numpy as np
from tqdm import tqdm
import networkx
import matplotlib.pyplot as plt

test_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


content = test_input

with open('day23_input.txt', 'r') as f:
    content = f.read().strip()

grid = np.array([[x for x in row] for row in content.split('\n')])
start = [0, np.where(grid[0]=='.')[0][0]]
end = [grid.shape[0]-1, np.where(grid[-1]=='.')[0][0]]


current_paths = [[start]]
finished_paths = []


while len(current_paths):
    new_paths = []
    for path in current_paths:
        r, c = path[-1]
        added_step = False
        for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            steps = [[r+dr, c+dc]]
            if r+dr<0 or r+dr>grid.shape[0]-1:
                continue
            if c+dc<0 or c+dc>grid.shape[1]-1:
                continue
            if grid[r+dr, c+dc]=='#':
                continue
            if grid[r+dr, c+dc]=='>':
                dc+=1
                steps.append([r+dr, c+dc])

            if grid[r+dr, c+dc]=='<':
                dc-=1
                steps.append([r+dr, c+dc])

            if grid[r+dr, c+dc]=='^':
                dr-=1
                steps.append([r+dr, c+dc])

            if grid[r+dr, c+dc]=='v':
                dr+=1
                steps.append([r+dr, c+dc])

            if [r+dr, c+dc] in path:
                continue
            new_paths.append(path + steps)

            # path.append([r+dr, c+dc])
            added_step = True
        if not added_step and not [r+dr, c+dc]==end:
            finished_paths.append(path[:-1])

    current_paths = new_paths


print(max([len(path) for path in finished_paths]))


#%% part 2

# content = test_input

grid = np.array([[x for x in row] for row in content.split('\n')])
start = [0, np.where(grid[0]=='.')[0][0]]
end = [grid.shape[0]-1, np.where(grid[-1]=='.')[0][0]]


current_paths = [[start]]
finished_paths = []

loop = tqdm()

while len(current_paths):
    new_paths = []
    for path in current_paths:
        loop.update()
        r, c = path[-1]
        added_step = False
        for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            steps = [[r+dr, c+dc]]
            if r+dr<0 or r+dr>grid.shape[0]-1:
                continue
            if c+dc<0 or c+dc>grid.shape[1]-1:
                continue
            if grid[r+dr, c+dc]=='#':
                continue
            if [r+dr, c+dc] in path:
                continue
            new_paths.append(path + steps)
            added_step = True

        if [r, c]==end:
            finished_paths.append(len(path))
            print(len(path))
    # print('next')
    current_paths = new_paths


print(max([len(path) for path in finished_paths]))
# 1423 too low
stop
#%%
import networkx
# content = test_input

grid = np.array([[x for x in row] for row in content.split('\n')])

start = tuple([0, np.where(grid[0]=='.')[0][0]])
end = tuple([grid.shape[0]-1, np.where(grid[-1]=='.')[0][0]])

graph = networkx.Graph()
for r in range(grid.shape[0]):
    for c in range(grid.shape[1]):
        if grid[r, c]=='#':
            continue
        for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if r+dr<0 or r+dr>grid.shape[0]-1:
                continue
            if c+dc<0 or c+dc>grid.shape[1]-1:
                continue
            if grid[r+dr, c+dc]=='#':
                continue
            graph.add_edge((r, c), (r+dr, c+dc), weight=1)

for node, degree in list(graph.degree):
    if degree==2:
        n1, n2 = graph.neighbors(node)
        w1 = graph.get_edge_data(node, n1)['weight']
        w2 = graph.get_edge_data(node, n2)['weight']
        graph.add_edge(n1, n2, weight=w1+w2)
        graph.remove_node(node)

loop = tqdm()

ax = plt.gca()
import psutil
# Stack for paths

current_paths = [[(start)]]
finished_paths = []

loop = tqdm()

def prune(graph, paths):
    valid_paths = []
    for path in tqdm(paths, desc='pruning'):
        graph_tmp = graph.copy()
        graph_tmp.remove_nodes_from(path[:-1])
        if networkx.has_path(graph_tmp, path[-1], end):
            valid_paths.append(path)
    try:
        print(f'pruned {100-len(valid_paths)/len(paths)*100:.1f}% of paths')
    except:
        pass
    return valid_paths

def get_length(graph, path):
    length = 0
    for edge in zip(path, path[1:]):
        length += graph.get_edge_data(*edge)['weight']
    return length

def check_reachable(graph, target, visited):
    graph_tmp = graph.copy()
    graph_tmp.remove_nodes_from(visited[:-1])
    return networkx.has_path(graph_tmp, visited[-1], target)


while len(current_paths):
    new_paths = []
    for path in current_paths:
        loop.update()
        current = path[-1]

        added_step = 0
        forks = []
        for neighbor in graph.neighbors(current):
            if neighbor in path[::-1]:
                continue# Check if the neighbor is visited
            # new_paths.append(path + [neighbor])
            forks.append(path + [neighbor])
            added_step += 1

        for fork in forks:
            # if added_step>1 and not check_reachable(graph, end, fork):
            #     continue
            new_paths.append(fork)

        if current==end:
            path_length = get_length(graph, path)
            finished_paths.append(path_length)
            print(path_length)
            if len(finished_paths)%100!=0: continue
            ax.clear()
            networkx.draw(graph, pos={node:node for node in graph.nodes}, node_size=200,
                          nodelist=path + [neighbor], ax=ax)
            plt.pause(0.01)

            if psutil.virtual_memory().percent>90:
                raise Exception('outofmemory')
        # if loop.n%500000==0:
        #     new_paths = prune(graph, new_paths)

    current_paths = new_paths



print("Longest Path:", max(finished_paths))
