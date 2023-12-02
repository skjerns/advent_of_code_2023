#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:29:15 2023

@author: simon
"""
import numpy as np


test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

with open('day2_input.txt') as f:
    c = f.read().strip()

def get_max_cubes(record):
    """gets a line of a game record and returns max red, green blue"""
    draws = record.split(':')[1].split(';')
    game_id = int(record.split(':')[0].split(' ')[-1])

    red = 0
    green = 0
    blue = 0
    for draw in draws:
        for cube in draw.split(','):
            match cube.strip().split(' '):
                case [number, 'red']:
                    if int(number)>red:
                        red = int(number)
                case [number, 'green']:
                    if int(number)>green:
                        green = int(number)
                case [number, 'blue']:
                    if int(number)>blue:
                        blue = int(number)
    return game_id, red, green, blue

maxcubes = np.array([12, 13, 14])
id_sum = 0

for record in c.split('\n'):
    game_id, *cubes = get_max_cubes(record)
    if (np.array(cubes)<=maxcubes).all():
        id_sum +=game_id

print(f'sum of game ids = {id_sum}')
cubes = np.array(cubes)

#%% part 2

id_prod = 0

for record in c.split('\n'):
    game_id, *cubes = get_max_cubes(record)

    id_prod += np.prod(cubes)

print(f'sum of game ids = {id_prod}')