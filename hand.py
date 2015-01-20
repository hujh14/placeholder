class Hand():
    def __init__(self, cardTuple):
        self.cards = cardTuple

        self.madePair = False
        self.pairSize = 0

        self.madeTwoPair = False
        self.twoPairSize = 0

        self.madeTrips = False
        self.tripSize = 0

        self.madeStraight = False
        self.madeFlush = False
        self.madeFullHouse = False
        self.FullHouseSize = 0
        self.madeFourOfKind = False
        self.madeStraightFlush = False

        self.OpenEndedStraightDraw = False
        self.GutShotStraightDraw = False
        self.FlushDraw = False

        self.Id = 0

    def idUpdate(self):
        temp1 = str(int(self.madePair))+str(self.pairSize)+str(int(self.madeTwoPair))+str(self.twoPairSize)+str(int(self.madeTrips))+str(self.tripSize)
        temp2 = str(int(self.madeStraight))+str(int(self.madeFlush))+str(int(self.madeFullHouse))+str(self.FullHouseSize)+str(int(self.madeFourOfKind))+str(int(self.madeStraightFlush))
        temp3 = str(int(self.OpenEndedStraightDraw))+str(int(self.GutShotStraightDraw))+str(int(self.FlushDraw))
        self.Id = temp1+temp2+temp3

    def PrintEverything(self):
        print 'madePair', self.madePair
        print 'pairSize', self.pairSize

        print 'madeTwoPair', self.madeTwoPair
        print 'twoPairSize', self.twoPairSize

        print 'madeTrips', self.madeTrips
        print 'tripSize', self.tripSize

        print 'madeStraight', self.madeStraight
        print 'madeFlush', self.madeFlush
        print 'madeFullHouse', self.madeFullHouse
        print 'FullHouseSize', self.FullHouseSize
        print 'madeFourOfKind', self.madeFourOfKind
        print 'madeStraightFlush', self.madeStraightFlush

        print 'OpenEndedStraightDraw', self.OpenEndedStraightDraw
        print 'GutShotStraightDraw', self.GutShotStraightDraw
        print 'FlushDraw', self.FlushDraw
        print self.Id


    def update(self, board):
        # Updates boolean profile
        cards = [self.cards[0], self.cards[1]] + board
        cards = sorted(cards, key = lambda x: int(numValue(x[0])))
        suits = [i[1] for i in cards]
        nums = [numValue(i[0]) for i in cards]
        duplicates = nums[:]
        
        uniqueNums = set(nums)
        for x in uniqueNums:
            duplicates.remove(x)
        
        if hasStraightFlush(cards): # not going to happen
            self.madeStraightFlush = True
        elif hasFourOfKind(duplicates): # works!
            self.madeFourOfKind = True
        elif len(duplicates) >= 3 and len(set(duplicates)) != len(duplicates): # works?
            self.madeFullHouse = True
            self.FullHouseSize = duplicates[1] #works for most cases
        elif hasFlush(suits):
            self.madeFlush = True
        elif hasStraight(nums):
            self.madeStraight = True
            if hasFlushDraw(suits):
                self.FlushDraw = True
        elif len(duplicates) == 2 and len(set(duplicates)) == 1: # this works
            self.madeTrips = True
            self.tripSize = duplicates[0]
            if hasFlushDraw(suits):
                self.FlushDraw = True
            self.hasOpenEndedStraightDraw,self.hasGutShotStraightDraw = straightDrawType(cards)
        elif len(duplicates) >= 2: # this works
            self.madeTwoPair = True
            self.twoPairSize = duplicates[1]
            if hasFlushDraw(suits):
                self.FlushDraw = True
            self.hasOpenEndedStraightDraw,self.hasGutShotStraightDraw = straightDrawType(cards)
        elif len(duplicates) == 1:
            self.madePair = True
            self.pairSize = duplicates[0]
            if hasFlushDraw(suits):
                self.FlushDraw = True
            self.hasOpenEndedStraightDraw,self.hasGutShotStraightDraw = straightDrawType(cards)
        else:
            if hasFlushDraw(suits):
                self.FlushDraw = True
            self.hasOpenEndedStraightDraw,self.hasGutShotStraightDraw = straightDrawType(cards)

        self.idUpdate()
        #self.PrintEverything()
        

def hasFourOfKind(duplicates):
    num = 0
    counter = 0
    for i in xrange(len(duplicates)):
        if duplicates[i] == num:
            counter += 1
        else:
            num = duplicates[i]
            counter = 1
        if counter == 3:
            return True
    return False

def hasStraightFlush(cards):
    return False

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

def hasFlushDraw(suits):
    h, d, c, s = 0, 0, 0, 0
    if len(suits) == 7:
        return False
    for card in suits:
        if card == 'h':
            h += 1
        elif card == 's':
            s += 1
        elif card == 'd':
            d += 1
        elif card == 'c':
            c += 1
    return h > 3 or c > 3 or s > 3 or d > 3

def hasStraight(cards):
    
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

def straightDrawType(cards):
    return (False,False)




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

#h = Hand(('as','s'))
#h.update(['as','8h','8d','tc','9h'])
#h.PrintEverything()

# Three pairs down register
# Straights dont register

        