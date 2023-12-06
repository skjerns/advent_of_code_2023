# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:31:10 2023

@author: Simon.Kern
"""
import numpy as np
test_input = """Time:      7  15   30
Distance:  9  40  200"""

c = test_input

with open('day6_input.txt', 'r') as f:
    c=f.read()


times = [int(x) for x in c.split('\n')[0].strip().split(' ') if x.isdigit()]
dists = [int(x) for x in c.split('\n')[1].strip().split(' ') if x.isdigit()]



record_counter = []
for t, record in zip(times, dists):
    record_counter_i = 0
    for speed_per_ms in range(t):
        remaining_time = t - speed_per_ms
        est_dist = speed_per_ms*remaining_time
        if est_dist>record:
            record_counter_i +=1
    record_counter.append(record_counter_i)
        
print('sum is', np.prod(record_counter))


#%% part 2
from tqdm import tqdm
c = test_input
with open('day6_input.txt', 'r') as f:
    c=f.read()


rtime = int(c.split('\n')[0][5:].replace(' ', ''))
record = int(c.split('\n')[1][9:].replace(' ', ''))


record_counter_i = 0
for speed_per_ms in tqdm(range(rtime), total=rtime):
    remaining_time = rtime - speed_per_ms
    est_dist = speed_per_ms*remaining_time
    if est_dist>record:
        record_counter_i +=1

print('sum is' , record_counter_i)
