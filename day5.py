#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:20:56 2023

@author: simon
"""
import numpy as np

test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


c = test_input

with open('day5_input.txt', 'r') as f:
    c=f.read()

class Mapping():
    def __init__(self, block):
        name, *lines = block.strip().split('\n')
        self.name = name.split(' ')[0].split('-')[-1]
        self.mappings = []
        for line in lines:
            dest, source, r = [int(x) for x in line.split(' ')]
            self.mappings += [[dest, source, r]]
        self.mappings = sorted(self.mappings, key=lambda x:x[1])
        

    def __repr__(self):
        return f'mapping({self.name})'

    def process(self, number):
        new_number = number
        for dest, source, r in self.mappings:
            if number<source:
                continue
            if number<(source+r):
                new_number = number + (dest-source)
                break
        # print(f'{self.name} {new_number} ', end='')
        return new_number

def compute(seedrange):
    from tqdm import tqdm
    locations = []
    for number in tqdm(seedrange, total=len(seedrange), miniters=200000):
        # print('\nseed', number, end=' ')
        for mapping in mappings:
            number = mapping.process(number)
        locations.append(number)    
    return min(locations)


blocks = c.split('\n\n')
seeds = [int(x) for x in blocks[0].split(' ')[1:]]
mappings = [Mapping(block) for block in blocks[1:]]

locations = []

for number in seeds:
    print('\nseed', number, end=' ')
    for mapping in mappings:
        number = mapping.process(number)
    locations.append(number)
    
    
    

print(min(locations), 'minimum location')
#%% part 2 in stupid

from joblib import Parallel, delayed
import pickle
blocks = c.split('\n\n')
seeds = [int(x) for x in blocks[0].split(' ')[1:]]
seeds_ranges = list(zip(seeds[::2], seeds[1::2]))

ranges = [range(start, start+r) for start, r in seeds_ranges]

res = Parallel(-1)(delayed(compute)(seedrange) for seedrange in ranges)

with open('day5.pkl', 'wb') as f:
    pickle.dump(res, f)

print(np.min(res))

stop

#%% part 1 but better

locations = []


class Mapping():
    def __init__(self, minseed, maxseed):
        #  in the beginning the mapping maps everything to its own number
        self.minseed = minseed
        self.maxseed = maxseed
        self.ranges = [(range(minseed, maxseed+1), 0)]

    def add_block(self, block):
        name, *lines = block.strip().split('\n')
        self.name = name
        lines = sorted(lines, key=lambda x:x.split(' ')[1])
        lines = [[int(l) for l in line.split(' ')] for line in lines]
        rangepile = [(range(max(l[1], self.minseed), min(l[1]+l[2], self.maxseed+1)),
                      l[0]-l[1]) for l in lines]

        while len(rangepile)>0:
            range_c, delta = rangepile.pop()
            if len(range_c)==0:
                continue

            self.ranges = sorted(self.ranges, key=lambda x:x[0].start)

            for i, (range_i, delta_i) in  enumerate(self.ranges):

                # case 1: source is completely smaller
                if (range_c.start>=range_i.stop):
                    continue

                # case 2: source is completely larger
                if (range_c.start>=range_i.stop):
                    continue

                assert range_c.start>=range_i.start

                # create the four possible ranges
                range_left = range(min(range_i.start, range_c.start), range_c.start)
                range_overlap = range(range_c.start, min(range_i.stop, range_c.stop))
                range_right = range(min(range_i.stop, range_c.stop), range_i.stop)
                range_larger = range(range_i.stop, range_c.stop)

                assert (len(range_left) + len(range_overlap) + len(range_right))==len(range_i)

                if len(range_left)>0:
                    self.ranges += [(range_left, delta_i)]
                if len(range_overlap)>0:
                    self.ranges += [(range_overlap, delta+delta_i)]
                if len(range_right)>0:
                    self.ranges += [(range_right, delta_i)]
                if len(range_larger)>0:
                        lines += [(range_larger, delta)]
                self.ranges.pop(i)

                self.ranges = sorted(self.ranges, key=lambda x:x[0].start)



                break


    def __repr__(self):
        return str(self.ranges)

    def process(self, number):
        for mapping, delta in self.ranges:
            if number in mapping:
                return number+delta
        return number

blocks = c.split('\n\n')
seeds = [int(x) for x in blocks[0].split(' ')[1:]]

minseed = min(seeds)
maxseed = max(seeds)

mapping = Mapping(minseed, maxseed)
print('###########')
print(seeds[2])
for block in blocks[1:]:
    mapping.add_block(block)
    print(mapping.name, mapping.process(seeds[2]))

asd

#%% real part 2
asd
seeds = list(zip(seeds[::2], seeds[1::2]))

block = blocks[1]


minseed = min([s[0] for s in seeds])
maxseed = max(s[0]+s[1] for s in seeds)

print(min(locations), 'minimum location')