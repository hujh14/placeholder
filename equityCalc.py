#10 - Royal Flush
# 9 - Straight Flush
# 8 - Four of a kind    
# 7 - Full House
# 6 - Flush
# 5 - Straight
# 4 - Three of a kind
# 3 - Two Pair
# 2 - Pair
# 1 - High Card

import itertools
import random
import time

def getEquity(hand, opponent = [], board = [], iters = 100):
    t = time.time()
    if str(type(hand)) == "<type: 'str'>":
        hand = [hand[:2].lower(), hand[2:].lower()]
    if str(type(board)) == "<type: 'str'>":
        b = []
        for i in range(len(board) / 2):
            b += [board[i:i+2].lower()]
        board = b
    if str(type(opponent)) == "<type: 'str'>":
        b = []
        for i in range(len(opponent) / 2):
            o += [opponent[i:i+2].lower()]
        opponent = o
    card_list = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as',
                 '2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac',
                 '2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah',
                 '2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']

    # Remove hole and board cards
    for card in hand + board + opponent:
        card_list.remove(card)
    
    a = 0
    for i in range(iters):
        number_of_cards = 7 - len(board)
        cards = random.sample(card_list, number_of_cards)
        hand_1 = hand + cards[len(hand):] + board
        hand_2 = opponent + cards[len(opponent):] + board
        w = winner(hand_1, hand_2)
        if w == 1:
            a += 1
    eq = (1.0 * a) / (iters)
    print("Time Elapsed: " + str(time.time() - t) + " seconds")
    return eq

def winner(hand_1, hand_2):
    ev_1 = evalHand(hand_1)
    ev_2 = evalHand(hand_2)
    if ev_1 > ev_2:
        return 1
    if ev_2 > ev_1:
        return 2
    return breakTie(ev_1, hand_1, hand_2)

def breakTie(case, hand_1, hand_2):
    if case == 1:
        while len(hand_1) > 2:
            h_1 = numValue(hand_1.pop()[0])
            h_2 = numValue(hand_2.pop()[0])
            if h_1 > h_2:
                return 1
            if h_2 > h_1:
                return 2
        return 0
    if case == 2:
        hand_1 = [numValue(x[0]) for x in hand_1]
        hand_2 = [numValue(x[0]) for x in hand_2]
        r_1 = sorted([x for x in hand_1 if hand_1.count(x) > 1]).pop()
        r_2 = sorted([x for x in hand_2 if hand_2.count(x) > 1]).pop()
        if r_1 > r_2:
            return 1
        if r_2 > r_1:
            return 2
        hand_1 = sorted([x for x in hand_1 if x != r_1])
        hand_2 = sorted([x for x in hand_2 if x != r_2])
        while len(hand_1) > 2:
            h_1 = hand_1.pop()
            h_2 = hand_2.pop()
            if h_1 > h_2:
                return 1
            if h_2 > h_1:
                return 2
        return 0
    if case == 3:
        hand_1 = sorted([numValue(x[0]) for x in hand_1])
        hand_2 = sorted([numValue(x[0]) for x in hand_2])
        s_1 = sorted(set([x for x in hand_1 if hand_1.count(x) == 2]))
        s_2 = sorted(set([x for x in hand_2 if hand_2.count(x) == 2]))
        if s_1[1] > s_2[1]:
            return 1
        if s_2[1] > s_1[1]:
            return 2
        if s_1[0] > s_2[0]:
            return 1
        if s_2[0] > s_1[0]:
            return 2
        h_1 = numValue([x for x in hand_1 if x not in s_1].pop())
        h_2 = numValue([x for x in hand_2 if x not in s_2].pop())
        if h_1 > h_2:
            return 1
        if h_2 > h_1:
            return 2
        return 0
    if case == 4:
        hand_1 = [numValue(x[0]) for x in hand_1]
        hand_2 = [numValue(x[0]) for x in hand_2]
        s_1 = sorted([x for x in hand_1 if hand_1.count(x) == 3]).pop()
        s_2 = sorted([x for x in hand_2 if hand_2.count(x) == 3]).pop()
        if s_1 > s_2:
            return 1
        if s_2 > s_1:
            return 2
        hand_1 = sorted([x for x in hand_1 if x != s_1])
        hand_2 = sorted([x for x in hand_2 if x != s_2])
        while len(hand_1) > 2:
            h_1 = hand_1.pop()
            h_2 = hand_2.pop()
            if h_1 > h_2:
                return 1
            if h_2 > h_1:
                return 2        
        return 0
    if case == 5:
        cards_1 = [numValue(x[0]) for x in hand_1]
        cards_2 = [numValue(x[0]) for x in hand_2]
        n = 6
        while n > 0:
            diff_1 = cards_1[n] - cards_1[n - 1]
            diff_2 = cards_2[n] - cards_2[n - 1]
            if diff_1 != 1:
                if n > 3:
                    cards_1.pop(n)
                else:
                    cards_1.pop(n - 1)
            if diff_2 != 1:
                if n > 3:
                    cards_2.pop(n)
                else:
                    cards_2.pop(n - 1)
            n -= 1
        c_1 = cards_1.pop()
        c_2 = cards_2.pop()
        if c_1 > c_2:
            return 1
        if c_2 > c_1:
            return 2
        return 0
    if case == 6:
        suits = [i[1] for i in hand_1]
        for i in set(suits):
            suits.remove(i)
        for i in set(suits):
            suits.remove(i)
        s = str(suits[0])
        hand_1 = [x for x in hand_1 if x[1] == s]
        hand_2 = [x for x in hand_2 if x[1] == s]
        hand_1 = sorted([numValue(x[0]) for x in hand_1])
        hand_2 = sorted([numValue(x[0]) for x in hand_2])
        while len(hand_1) > 0 and len(hand_2) > 0:
            h_1 = hand_1.pop()
            h_2 = hand_2.pop()
            if h_1 > h_2:
                return 1
            if h_2 > h_1:
                return 2
        return 0
    if case == 7:
        hand_1 = sorted([numValue(x[0]) for x in hand_1])
        hand_2 = sorted([numValue(x[0]) for x in hand_2])
        t_1 = sorted([x for x in hand_1 if hand_1.count(x) == 3]).pop()
        t_2 = sorted([x for x in hand_2 if hand_2.count(x) == 3]).pop()
        if t_1 > t_2:
            return 1
        if t_2 > t_1:
            return 2
        hand_1 = [x for x in hand_1 if x != t_1]
        hand_2 = [x for x in hand_2 if x != t_2]
        d_1 = sorted([x for x in hand_1 if hand_1.count(x) > 1]).pop()
        d_2 = sorted([x for x in hand_2 if hand_2.count(x) > 1]).pop()
        if d_1 > d_2:
            return 1
        if d_2 > d_1:
            return 2
        return 0
    if case == 8:
        hand_1 = [numValue(x[0]) for x in hand_1]
        hand_2 = [numValue(x[0]) for x in hand_2]
        c_1 = sorted([x for x in hand_1 if hand_1.count(x) == 4]).pop()
        c_2 = sorted([x for x in hand_2 if hand_2.count(x) == 4]).pop()
        if c_1 > c_2:
            return 1
        if c_2 > c_1:
            return 2
        k_1 = sorted([x for x in hand_1 if x != c_1]).pop()
        k_2 = sorted([x for x in hand_2 if x != c_2]).pop()
        if k_1 > k_2:
            return 1
        if k_2 > k_1:
            return 2
        return 0
    if case == 9:
        suits = [i[1] for i in hand_1]
        for i in set(suits):
            suits.remove(i)
        for i in set(suits):
            suits.remove(i)
        s = suits[0]
        hand_1 = sorted([x for x in hand_1 if x[1] == s])
        hand_2 = sorted([x for x in hand_2 if x[1] == s])
        while len(hand_1) > 0 and len(hand_2) > 0:            
            h_1 = numValue(hand_1.pop()[0])
            h_2 = numValue(hand_2.pop()[0])
            if h_1 > h_2:
                return 1
            if h_2 > h_1:
                return 2
        return 0
    if case == 10:
        return 0
    
def evalHand(hand):
    # hand is a list of 7 cards
    
    # sort hand from lowest face value to highest
    hand = sorted(hand, key = lambda x: int(numValue(x[0])))

    suits = [i[1] for i in hand]
    cards = [numValue(i[0]) for i in hand]

    uniqueCards = len(set(cards))
    if uniqueCards == 7:
        # No pairs
        flush = hasFlush(suits)
        if hasStraight(cards):
            if flush:
                return 9
            return 5
        if flush:
            return 6
        return 1
    if uniqueCards == 6:
        # One pair
        flush = hasFlush(suits)
        if hasStraight(cards):
            if flush:
                return 9
            return 5
        if flush:
            return 6
        return 2
    if uniqueCards == 5:
        # Two pair or three of a kind
        flush = hasFlush(suits)
        if hasStraight(cards):
            if flush:
                return 9
            return 5
        if flush:
            return 6
        for i in set(cards):
            cards.remove(i)
        if len(set(cards)) == 1:
            return 4
        return 3
    if uniqueCards == 4:
        # Full house, four of a kind, or three pair
        for i in set(cards):
            cards.remove(i)
        if len(set(cards)) == 1:
            return 8
        if len(set(cards)) == 2:
            return 7
        if len(set(cards)) > len(cards):
            return 7
        return 3

def hasStraight(c):
    cards = [x for x in c]
    n = len(cards) - 1
    while n > 0:
        diff = cards[n] - cards[n - 1]
        if diff != 1:
            if n > 3:
                cards.pop(n)
            else:
                cards.pop(n - 1)
        n -= 1
    return (len(cards) > 4)

def hasFlush(suits):
    h, d, c, s = 0, 0, 0, 0
    for card in suits:
        if card == 'h':
            h += 1
        elif card == 's':
            s += 1
        elif card == 'd':
            d += 1
        elif card == 'c':
            c += 1
    return h > 4 or c > 4 or s > 4 or d > 4

def numValue(card):
    if card == 't':
        return 10
    elif card == 'j':
        return 11
    elif card == 'q':
        return 12
    elif card == 'k':
        return 13
    elif card == 'a':
        return 14
    else:
        return int(card)
    
