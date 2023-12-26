#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:31:48 2023

@author: simon
"""

string = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


with open('day15_input.txt', 'r') as f:
    string = f.read().strip()

def ascii_hash(string):
    curr_val = 0
    for c in string:
        curr_val += ord(c)
        curr_val *= 17
        curr_val %= 256
    return curr_val


hashes = [ascii_hash(x.replace('\n', '')) for x in string.split(',')]

print(f'{sum(hashes)=}')


#%% part 2

boxes = [{} for _ in range(256)]

for instr in string.split(','):
    if '=' in instr:
        label, focal = instr.split('=')
    else:
        label = instr[:-1]
        focal = None

    idx = ascii_hash(label)
    box = boxes[idx]

    if focal:
        box[label] = focal
    else:
        try:
            del box[label]
        except Exception:
            pass


focusing_power = 0
for box_i, box in enumerate(boxes, 1):
    for slot_i ,(label, focal) in enumerate(box.items(), 1):
        focusing_power += box_i * int(focal) * slot_i

print(focusing_power)
