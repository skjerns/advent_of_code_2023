#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:19:43 2023

@author: simon
"""
import numpy as np

test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


c = test_input

with open('day7_input.txt', 'r') as f:
    c = f.read().strip()

def card_value(c):
    if c.isdigit():
        return int(c)
    others = 'AKQJT'[::-1]
    return others.index(c)+10


def sort_hands(hand):
    uniques, counts = np.unique([x for x in hand], return_counts=True)
    value = int(''.join([f'{card_value(c):02d}' for c in hand]))
    if len(uniques)==1:
        print(hand, 'five of a kind')
        return 90000000000, value
    elif len(uniques)==2 and (1 in counts):
        ## four of a kind
        print(hand, 'four of a kind')
        return 80000000000, value
    elif len(uniques)==2 and (2 in counts):
        # full house
        print(hand, 'full house')
        return 70000000000, value
    elif len(uniques)==3 and (3 in counts):
        # three of a kind
        print(hand, 'three of a kind')
        return 60000000000, value
    elif len(uniques)==3 and (2 in counts):
        # two pair
        print(hand, 'two pair')
        return 50000000000, value
    elif (2 in counts):
        # one pair
        print(hand, 'one pair')
        return 40000000000, value
    elif len(uniques)==5:
        # high card
        print(hand, 'high card')
        return 30000000000, value
    else:
        raise Exception

def sort_hands_normal(hand):
    basevalue, cardvalue = sort_hands(hand)
    return basevalue + cardvalue

hands = []
bids = []
for line in c.split('\n'):
    hand, bid = line.split(' ')
    hands.append(''.join(hand))
    bids.append(int(bid))

sorted_hands = sorted(zip(hands, bids), key=lambda x:sort_hands_normal(x[0]))

score = 0
for i, (hand, bid) in enumerate(sorted_hands, 1):
    score += i*bid

print(score)


#%% part 2

def card_value(c):
    if c.isdigit():
        return int(c)
    if c=='J':
        return 1
    others = 'AKQJT'[::-1]
    return others.index(c)+10


def sort_hands_joker(hand):
    if not 'J' in hand:
        return sort_hands_normal(hand)
    deck = '23456789AKQJT'
    possible_replacements = [hand.replace('J', card) for card in deck]
    best_hand = sorted(possible_replacements, key=sort_hands, reverse=True)[0]
    _, cardvalue = sort_hands(hand)
    basevalue, _ = sort_hands(best_hand)

    return basevalue+cardvalue

values = [sort_hands_joker(hand) for hand in hands]
sorted_hands = sorted(zip(hands, bids, values), key=lambda x:sort_hands_joker(x[0]))

score = 0
for i, (hand, bid, value) in enumerate(sorted_hands, 1):
    score += i*bid

print(score)

# 253625043 too low
# 253630207 too low
# 254081341 too low