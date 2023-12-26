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
import psutil


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

with open('day17_input.txt', 'r') as f:
    c = f.read().strip()


#%% failed dijkstra apporach
class Node():

    counterdirection = {0:1, 1:0, 2:3, 3:2}
    direction2d = dict(enumerate([[-1, 0], [1, 0], [0, -1], [0, 1]]))
    num2vec = {0:'^', 1:'v', 2:'<', 3:'>', -1:'o'}

    def __eq__(self, other):
        return self.r == other.r and self.c==other.c and \
            self.direction==other.direction and self.streak==other.streak

    def __hash__(self):
        return hash(self.r) + hash(self.c) + hash(self.streak) + hash(self.direction)

    def __repr__(self):
        return f'Node({self.r}, {self.c}; heatloss={self.curr_heatloss})'

    def __lt__(self, other):
        # return self.r>other.r and self.c>other.c
        return self.curr_heatloss<other.curr_heatloss
            # return True
        # elif self.curr_heatloss==other.curr_heatloss:
        #     return self.r>other.r or self.c>other.c
        # return False

    def __init__(self, r, c, grid, direction, streak, heatloss, prev_node=None):
        self.r = r
        self.c = c
        self.grid = grid
        self.direction = direction
        self.streak=streak
        self.curr_heatloss = heatloss+grid[r, c]
        self.prev_node = None
        # if streak>3:
        #     self.curr_heatloss = np.inf

    def get_neighbours(self):
        # assert self.curr_heatloss < np.inf
        neighbours = set()
        for d, rc in enumerate([[-1, 0], [1, 0], [0, -1], [0, 1]]):
            next_r = self.r+rc[0]
            next_c = self.c+rc[1]
            if next_r<0 or next_r>=self.grid.shape[0]:
                continue
            if next_c<0 or next_c>=self.grid.shape[1]:
                continue
            if Node.counterdirection[d]==self.direction:
                continue
            new_streak = 1 if self.direction!=d else self.streak+1
            if new_streak>3:
                continue
            next_node = Node(next_r, next_c, self.grid, direction=d,
                             streak = new_streak,  heatloss=self.curr_heatloss,
                             prev_node=self)
            neighbours.add(next_node)

        return neighbours



class Grid():
    def __init__(self, grid, heuristic=True):
        grid = np.array([[int(x) for x in row] for row in grid.strip().split('\n')])
        self.grid = grid
        self.heuristic = heuristic
        # path_cumulative_heatloss = -grid[0,0]
        self.curr_node = Node(0, 0, grid, -1, -1, -grid[0,0])
        self.visited = set()
        # indices = product(range(grid.shape[0]), range(grid.shape[1]))
        self.not_visited = []
        manhatten_mask = np.eye(grid.shape[0], grid.shape[1], k=0)
        manhatten_mask += np.eye(grid.shape[0], grid.shape[1], k=1)
        if heuristic:
            self.upper_bound = grid[manhatten_mask.astype(bool)].sum()
        else:
            self.upper_bound = np.inf

        heapq.heappush(self.not_visited, self.curr_node)

        # self.not_visited = [self.curr_node]

    def explore_neighbours(self):
        # visit lowest node
        try:
            self.curr_node = heapq.heappop(self.not_visited)
            # if self.curr_node.r == grid.shape[0]-1 and self.curr_node.c==grid.shape[1]-1:
            #     if self.curr_node.curr_heatloss<self.upper_bound:
            #         self.upper_bound = self.curr_node.curr_heatloss
        except IndexError:
            return False

        self.visited.add(self.curr_node)

        neighbours = self.curr_node.get_neighbours()

        for neighbour in neighbours:
            # if neighbour not in self.visited and not neighbour.curr_heatloss==np.inf:
                # heapq.heappush(self.not_visited, neighbour)
            # heuristic to stop early
            if self.heuristic:
                manhattendistance = grid.shape[0]-neighbour.r + grid.shape[1]+neighbour.c
            else:
                manhattendistance = 0
            if neighbour.curr_heatloss + manhattendistance < self.upper_bound and \
               neighbour not in self.visited and not neighbour in self.not_visited:
                # manhattendistance = grid.shape[0]-neighbour.r + grid.shape[1]+neighbour.c
                # if neighbour.curr_heatloss + manhattendistance < self.upper_bound:
                # if not neighbour.curr_heatloss==np.inf:
                heapq.heappush(self.not_visited, neighbour)

        return True


    def plot_heatmap(self):
        plt.cla()
        grid = self.grid
        heatmap= np.zeros(self.grid.shape, dtype=int)
        # for node in self.not_visited:
        #     heatmap[node.r, node.c] = node.curr_heatloss
        ax = plt.gca()

        for node in sorted(self.visited, reverse=True):
            heatmap[node.r, node.c] = node.curr_heatloss

        vmax = max(self.grid[np.eye(*self.grid.shape, dtype=bool)].sum(), heatmap.max())
        ax.imshow(heatmap, vmax=vmax, origin='upper')
        # ax.imshow(grid, alpha=0.2)
        if grid.shape[0]<20:
            plt.xticks(np.arange(grid.shape[1]))
            plt.yticks(np.arange(grid.shape[0]))
            plt.tick_params(labeltop=True, labelright=True)

            for node in sorted(self.visited):
                text = ax.text(node.c, node.r, heatmap[node.r, node.c],
                               fontsize=14, ha="center", va="center",
                               color="green")

            for r, row in enumerate(grid):
                for c, val in enumerate(row):
                    text = ax.text(c, r-0.25, val,
                                   fontsize=14, ha="center", va="center",
                                   color="gray")

        for node in self.not_visited:
            highlight_cell(node.c, node.r, ax=ax, color='red')
            if grid.shape[0]<20:
                text = ax.text(node.c, node.r, node.curr_heatloss,
                               fontsize=14, ha="center", va="center",
                               color="black")

        node = self.curr_node
        for nodex in self.visited:
            if nodex.r==grid.shape[0]-1 and nodex.c==grid.shape[1]-1:
                node = nodex
        highlight_cell(node.c, node.r, ax=ax, color='blue')

        while (node:=node.prev_node) is not None:
            highlight_cell(node.c, node.r, ax=ax)
            text = ax.text(node.c, node.r+0.25, Node.num2vec[node.direction],
                    fontsize=14,
                        ha="center", va="center", color="black")


def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


grid = c

self = Grid(grid)
grid = self.grid

loop = tqdm()
i = 0
while self.explore_neighbours():
    break
    loop.update()
    i+=1
    # if i==50000:
        # break
    # plot_path(self.visited[-1], grid)
    if i%10000==0:
        self.plot_heatmap()
        plt.pause(0.01)
        if psutil.virtual_memory().percent>85:
            raise Exception('outofmemory')
    # print(len(curr_node))
    # input()

heatlosses = [node.curr_heatloss for node in self.visited if node.r==grid.shape[0]-1 and node.c==grid.shape[1]-1]
if len(heatlosses)>0:
    print(f'{min(heatlosses)=}  {heatlosses=}')

# for node in self.visited:
#     if node.r==12 and node.c==12:
#         self.curr_node = node
#         self.plot_heatmap()
#         plt.pause(0.1)
#         plt.waitforbuttonpress(50)

# 882 too high


#%% part 2


def get_neighbours_ultra(self):
    # assert self.curr_heatloss < np.inf
    neighbours = set()

    for d, (r, c) in enumerate([[-1, 0], [1, 0], [0, -1], [0, 1]]):
        # if we are turning, move at least three steps
        # however, also add the heatloss of the path we have taken
        heatloss_path = 0
        if d!=self.direction:
            r, c = [r*4, c*4]
            new_streak = 4
        else:
            new_streak = self.streak+1
        next_r = self.r + r
        next_c = self.c + c

        if next_r<0 or next_r>=self.grid.shape[0]:
            continue
        if next_c<0 or next_c>=self.grid.shape[1]:
            continue
        if Node.counterdirection[d]==self.direction:
            continue

        if d!=self.direction:
            # try:
                heatloss_path += sum([grid[self.r+(r>0)*i, self.c+(c>0)*i] for i in range(1,4)])
            # except Exception:
                # pass
        # no more than 10 moves in one direction
        if new_streak>10:
            continue
        next_node = Node(next_r, next_c, self.grid, direction=d,
                         streak = new_streak,  heatloss=self.curr_heatloss + heatloss_path,
                         prev_node=self)
        neighbours.add(next_node)
    return neighbours

Node.get_neighbours = get_neighbours_ultra
grid = test_input
grid = c
# grid = """111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991"""

self = Grid(grid, heuristic=False)
grid = self.grid

loop = tqdm()
i = 0

while self.explore_neighbours():
    loop.update()
    i+=1
    # if i==50000:
    #     # break
    # # plot_path(self.visited[-1], grid)

    if i%10000==0:
        self.plot_heatmap()
        plt.pause(0.01)
    # plt.waitforbuttonpress(30)

    # print(len(curr_node))
    # input()
self.plot_heatmap()

heatlosses = [node.curr_heatloss for node in self.visited if node.r==grid.shape[0]-1 and node.c==grid.shape[1]-1]
print(f'{min(heatlosses)=}  {heatlosses=}')

# 720 too low
# why is it 734????
# my solution shows 743.... :-/
