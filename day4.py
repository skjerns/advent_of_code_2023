# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

c =  test_input

with open('day4_input.txt', 'r') as f:
    c = f.read().strip()


lines = c.split('\n')

points = 0

for line in lines:
    winning, owning = line.split(': ')[1].split('|')
    
    winning = [int(x) for x in winning.strip().split(' ') if x.isdigit()]
    owning = [int(x) for x in owning.strip().split(' ') if x.isdigit()]
    winning_cards = 0
    for card in winning:
        if card in owning:
            winning_cards += 1
    points += 2**(winning_cards-1) * (winning_cards>0)
print('total of points:', points)

#%% part 2

lines = c.split('\n')

points = 0

cards = []

for line in lines:
    winning, owning = line.split(': ')[1].split('|')
    
    winning = [int(x) for x in winning.strip().split(' ') if x.isdigit()]
    owning = [int(x) for x in owning.strip().split(' ') if x.isdigit()]
    # store cards as winning, owning, n_copies
    cards.append([winning, owning, 1])

for i, card in enumerate(cards):
    winning, owning, n_copies = card
    winning_cards = 0
    for card in winning:
        if card in owning:
            winning_cards += 1
            
    for j in range(1, winning_cards+1):
        cards[i+j][2] += n_copies
    
n_cards = sum(n_copies for _,_, n_copies in cards)
print('total of points:', [n_cards])
