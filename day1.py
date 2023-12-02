#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:01:21 2023

@author: simon
"""
with open('day1_input.txt', 'r') as f:
    c = f.read()


#%% part 1


lines = c.split('\n')

def find_first_digit(string):
    for s in string:
        if s.isdigit(): return s

digits = []
for line in lines:
    digit = int(''.join([find_first_digit(line), find_first_digit(line[::-1])]))
    digits.extend([digit])

print(sum(digits), 'is the answer part 1')
#%% part 2
with open('day1_input.txt', 'r') as f:
    c = f.read()

test_input2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
# c = test_input2
numbers = {'teen':'t','zero':0, 'one':1, 'two':2, 'three':3,'four': 4, 'five':5, 'six':6,
           'seven':7, 'eight':8, 'nine':9, 'ten': 10, 'eleven': 11, 'twelve':12,
           }

for word, num in numbers.items():
    c = c.replace(word, word + str(num)+ word)
lines = c.split('\n')

digits = []
for line in lines:
    digit = int(''.join([find_first_digit(line), find_first_digit(line[::-1])]))
    digits.extend([digit])

print(sum(digits), 'is the answer part 2')