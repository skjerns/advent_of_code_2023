#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:39:07 2023

@author: simon
"""
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from itertools import product, combinations_with_replacement
import networkx
import heapq


test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

c = test_input

# with open('day17_input.txt', 'r') as f:
#     c = f.read().strip()



#%% failed dijkstra apporach

class Node():


    def __eq__(self, other):
        if other is None: return False
        return self.r == other.r  and self.c==other.c and \
            self.prev_directions==other.prev_directions

    def __hash__(self):
        return hash(f'{self.r}, {self.c}, {self.prev_directions}')

    def __repr__(self):
        return f'Node({self.r}, {self.c}; heatloss={self.curr_heatloss} {self.prev_directions})'

    @profile
    def __lt__(self, other):
        # return self.r>other.r and self.c>other.c
        if self.curr_heatloss<other.curr_heatloss:
            return True
        elif self.curr_heatloss==other.curr_heatloss:
            return self.r>other.r or self.c>other.c
        return False

    @profile
    def __init__(self, r, c, grid, prev_node, path_cumulative_heatloss, direction=None):
        self.r = r
        self.c = c
        self.curr_heatloss = np.inf
        self.prev_directions = []
        self.grid = grid
        self.prev_node = prev_node
        self.curr_heatloss = path_cumulative_heatloss+grid[r, c]
        self.direction = direction
        self.neighbours = []

        if prev_node is None:
            self.prev_directions = []
            return

        if prev_node.prev_node is None:
            self.prev_directions = [prev_node.direction]
            return

        if prev_node.prev_node.prev_node is None:
            self.prev_directions =  [prev_node.prev_node.direction, prev_node.direction]
            return

        self.prev_directions =  [prev_node.prev_node.prev_node.direction,
                                 prev_node.prev_node.direction,
                                 prev_node.direction,
                                 direction]

        for x in self.prev_directions[:-1]:
            if direction!=x:
                return

        self.curr_heatloss = np.inf


    @profile
    def get_neighbours(self):
        assert self.curr_heatloss < np.inf
        neighbours = set()
        for r, d in zip([-1, 1], ['^', 'v']):
            next_r = self.r+r
            if next_r<0 or next_r>=self.grid.shape[0]:
                continue
            if self.prev_node and next_r==self.prev_node.r:
                continue
            next_node = Node(next_r, self.c, self.grid, self,
                             self.curr_heatloss, direction=d)
            neighbours.add(next_node)

        for c, d in zip([-1, 1], ['<', '>']):
            next_c = self.c+c
            if next_c<0 or next_c>=self.grid.shape[1]:
                continue
            if self.prev_node and next_c==self.prev_node.c:
                continue
            next_node = Node(self.r, next_c, self.grid, self,
                             self.curr_heatloss, direction=d)
            # print(next_node)
            neighbours.add(next_node)
        # if len(self.neighbours)==4:
        #     pass
        # print(len(self.neighbours))
        return neighbours



class Grid():

    def __init__(self, grid):
        grid = np.array([[int(x) for x in row] for row in grid.strip().split('\n')])
        self.grid = grid
        prev_node = None
        path_cumulative_heatloss = -grid[0,0]
        self.curr_node = Node(0, 0, grid, prev_node, path_cumulative_heatloss)
        self.visited = set()
        # indices = product(range(grid.shape[0]), range(grid.shape[1]))
        self.not_visited = []
        manhatten_mask = np.eye(grid.shape[0], grid.shape[1], k=0)
        manhatten_mask += np.eye(grid.shape[0], grid.shape[1], k=1)
        self.upper_bound = grid[manhatten_mask.astype(bool)].sum()
        heapq.heappush(self.not_visited, self.curr_node)
        # self.not_visited = [self.curr_node]

    @profile
    def explore_neighbours(self):
        # visit lowest node
        try:
            self.curr_node = heapq.heappop(self.not_visited)
            if self.curr_node.r == grid.shape[0]-1 and self.curr_node.c==grid.shape[1]-1:
                if self.curr_node.curr_heatloss<self.upper_bound:
                    self.upper_bound = self.curr_node.curr_heatloss
        except IndexError:
            return False

        self.visited.add(self.curr_node)

        neighbours = self.curr_node.get_neighbours()

        for neighbour in neighbours:
            # if neighbour not in self.visited and not neighbour.curr_heatloss==np.inf:
                # heapq.heappush(self.not_visited, neighbour)
            if neighbour not in self.visited:
                manhattendistance = grid.shape[0]-neighbour.r + grid.shape[1]+neighbour.c
                if neighbour.curr_heatloss + manhattendistance < self.upper_bound:
                # if not neighbour.curr_heatloss==np.inf:
                    heapq.heappush(self.not_visited, neighbour)

                # self.not_visited.append(neighbour)
                # idx = self.not_visited.index(neighbour)

        # self.not_visited = sorted(self.not_visited)
        return True

    def __repr__(self):
        plot_path(self.path[0], self.grid)

    def plot_heatmap(self):
        plt.cla()
        heatmap= np.zeros(self.grid.shape)
        # for node in self.not_visited:
        #     heatmap[node.r, node.c] = node.curr_heatloss
        for node in self.visited:
            heatmap[node.r, node.c] = node.curr_heatloss
        vmax = self.grid[np.eye(*self.grid.shape, dtype=bool)].sum()
        ax = plt.gca()
        ax.imshow(heatmap.T, vmax=vmax, origin='upper')

        node = self.curr_node
        highlight_cell(node.r, node.c, ax=plt.gca())
        text = ax.text(node.c, node.r, node.direction,
                    fontsize=14,
                       ha="center", va="center", color="black")
        while (node:=node.prev_node) is not None:
            highlight_cell(node.c, node.r, ax=ax)
            text = ax.text(node.c, node.r, node.direction,
                    fontsize=14,
                       ha="center", va="center", color="black")


def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect

def plot_path(node, grid):
    grid_str = grid.copy().astype(str)

    grid_str[node.r, node.c] = node.direction

    while (node:=node.prev_node)not in (BaseNode(0, 0), None):
        if node is not None and node.direction is not None:
            grid_str[node.r, node.c] = node.direction
    print('\n'.join([''.join([x for x in row]) for row in grid_str]))


grid = c

self = Grid(grid)
grid = self.grid

loop = tqdm()
i = 0
while self.explore_neighbours():
    loop.update()
    i+=1
    # if i==5000:
        # break
    # # plot_path(self.visited[-1], grid)
    # if i%1000000==0:
        # self.plot_heatmap()
        # plt.pause(0.01)
    # print(len(curr_node))
    # input()

heatlosses = [node.curr_heatloss for node in self.visited if node.r==12 and node.c==12]
print(f'{min(heatlosses)=}  {heatlosses=}')

# for node in self.visited:
#     if node.r==12 and node.c==12:
#         self.curr_node = node
#         self.plot_heatmap()
#         plt.pause(0.1)
#         plt.waitforbuttonpress(50)

# 882 too high
