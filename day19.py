#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 07:45:14 2023

@author: simon
"""

test_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


c = test_input

# with open('day19_input.txt', 'r') as f:
    # c = f.read().strip()

rules_raw, parts = c.split('\n\n')

rules_table = {}
for rule in rules_raw.split('\n'):
    name, conditions_raw = rule[:-1].split('{')
    *conditions, fallback_action = conditions_raw.split(',')
    rules = []
    for condition in conditions:
        cond, action = condition.split(':')
        # print(condition)
        rules.append([cond, action])
    rules.append(['True', fallback_action])
    rules_table[name] = rules


parts = [eval(f'dict({part[1:-1]})') for part in  parts.split('\n')]
summed = 0
for part in parts:
    x = part['x']
    m = part['m']
    a = part['a']
    s = part['s']
    next_step = 'in'
    while not next_step in 'RA':
        print(next_step)
        next_rules = rules_table[next_step]
        for rule, next_step in next_rules:
            if eval(rule):
                break
    if next_step=='A':
        summed += x+m+a+s

print('accepted sum', summed)

#%% part 2
x=m=a=s=0
accepted_combinations = 0

i = 0
from tqdm import tqdm

loop = tqdm(total=4000**4)
for x in range(4000):
    for m in range(4000):
        for a in range(4000):
            a += 1
            loop.update()

print('accepted sum', summed)
