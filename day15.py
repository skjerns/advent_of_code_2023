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
