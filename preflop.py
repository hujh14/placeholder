#import pbots_calc
import itertools

def getEq(hand):
    
    if str(type(hand)) == "<type 'str'>":
        hand = [hand[:2], hand[2:]]
    
    hand[0] = hand[0][0].upper() + hand[0][1]
    hand[1] = hand[1][0].upper() + hand[1][1]

    if hand[0][1] == hand[1][1]:
        # Same suit
        hand = hand[0][0] + hand[1][0] + "s"
    elif hand[0][0] == hand[1][0]:
        # Same number
        hand = hand[0][0] + hand[1][0]
    else:
        # Different suit and number
        hand = hand[0][0] + hand[1][0] + "o"
    with open("preflop.csv") as data:
        s = data.read()
        if s.find(hand) == -1:
            # Flip card oder if necessary
            hand = hand[1] + hand[0] + hand[2:]
        # Find hand in file
        eq = s[s.find(hand):s.find("\n", s.find(hand) + 1)]
        eq = '.' + eq[eq.find(',') + 1:].replace('.', '')
        return float(eq)

