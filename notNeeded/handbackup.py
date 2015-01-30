'''
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

        self.strength = 0
        # 0 means nothing
        # 1 means highcard
        # 2 means low pair
        # 4 means mid pair
        # 6 means high pair
        # 8 means two pair
        # 5 means trip
        # 15 means straight
        # 16 means weak flush
        # 17 means strong flush
        # 18 means fullhouse
        # 19 means 4ofkind
        # 20 means straightflush

    def idUpdate(self):
        temp1 = str(int(self.madePair))+str(self.pairSize)+str(int(self.madeTwoPair))+str(self.twoPairSize)+str(int(self.madeTrips))+str(self.tripSize)
        temp2 = str(int(self.madeStraight))+str(int(self.madeFlush))+str(int(self.madeFullHouse))+str(self.FullHouseSize)+str(int(self.madeFourOfKind))+str(int(self.madeStraightFlush))
        temp3 = str(int(self.OpenEndedStraightDraw))+str(int(self.GutShotStraightDraw))+str(int(self.FlushDraw))
        self.Id = temp1+temp2+temp3

    def PrintEverything(self):
        print('madePair', self.madePair)
        print('pairSize', self.pairSize)

        print('madeTwoPair', self.madeTwoPair)
        print('twoPairSize', self.twoPairSize)

        print('madeTrips', self.madeTrips)
        print('tripSize', self.tripSize)

        print('madeStraight', self.madeStraight)
        print('madeFlush', self.madeFlush)
        print('madeFullHouse', self.madeFullHouse)
        print('FullHouseSize', self.FullHouseSize)
        print('madeFourOfKind', self.madeFourOfKind)
        print('madeStraightFlush', self.madeStraightFlush)

        print('OpenEndedStraightDraw', self.OpenEndedStraightDraw)
        print('GutShotStraightDraw', self.GutShotStraightDraw)
        print('FlushDraw', self.FlushDraw)
        print(self.Id)
        print(self.strength)


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
            self.strength = 20
        elif hasFourOfKind(duplicates): # works!
            self.madeFourOfKind = True
            self.strength = 19
        elif len(duplicates) >= 3 and len(set(duplicates)) != len(duplicates): # works?
            self.madeFullHouse = True
            self.FullHouseSize = duplicates[1] #works for most cases
            self.strength = 18
        elif hasFlush(suits):
            self.madeFlush = True
            self.strength = 17
        elif hasStraight(nums):
            self.madeStraight = True
            self.strength = 15

            if hasFlushDraw(suits):
                self.FlushDraw = True
                self.strength +=1

        elif len(duplicates) == 2 and len(set(duplicates)) == 1: # this works
            self.madeTrips = True
            self.tripSize = duplicates[0]
            self.strength = 11

            if hasFlushDraw(suits):
                self.FlushDraw = True
                self.strength += 1
            straightDrawOuts = countStraightDrawOuts(nums)
            if straightDrawOuts != 0:
                if straightDrawOuts ==1:
                    self.hasGutShotStraightDraw = True
                    self.strength += 1
                else:
                    self.hasOpenEndedStraightDraw = True
                    self.strength += 1
            if hasGoodKicker(self.cards, self.tripSize):
                self.strength += 1

        elif len(duplicates) >= 2: # this works
            self.madeTwoPair = True
            self.twoPairSize = duplicates[1]
            self.strength = 7

            if hasFlushDraw(suits):
                self.FlushDraw = True
                self.strength += 1
            straightDrawOuts = countStraightDrawOuts(nums)
            if straightDrawOuts != 0:
                if straightDrawOuts ==1:
                    self.hasGutShotStraightDraw = True
                    self.strength += 1
                else:
                    self.hasOpenEndedStraightDraw = True
                    self.strength += 1
            if hasGoodKicker(self.cards, self.twoPairSize):
                self.strength += 1

        elif len(duplicates) == 1:
            self.madePair = True
            self.pairSize = duplicates[0]
            if self.pairSize >= 12:
                self.pairSize = 5
            elif self.pairSize >= 7:
                self.strength = 3
            else:
                self.strength = 1

            if hasFlushDraw(suits):
                self.FlushDraw = True
                self.strength += 2
            if hasGoodKicker(self.cards, self.pairSize):
                self.strength += 1

            straightDrawOuts = countStraightDrawOuts(nums)
            if straightDrawOuts != 0:
                if straightDrawOuts ==1:
                    self.hasGutShotStraightDraw = True
                    self.strength += 1
                else:
                    self.hasOpenEndedStraightDraw = True
                    self.strength += 2

        else:
            if hasFlushDraw(suits):
                self.FlushDraw = True
                if hasGoodFlushDraw:
                    self.strength = 6
                else:
                    self.strength = 3
            straightDrawOuts = countStraightDrawOuts(nums)
            if straightDrawOuts != 0:
                if straightDrawOuts ==1:
                    self.hasGutShotStraightDraw = True
                    self.strength = 2
                else:
                    self.hasOpenEndedStraightDraw = True
                    self.strength = 5

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
    # h, d, c, s = 0, 0, 0, 0

    # for x in cards:
    #     if x[1] == 'h':
    #         h += 1
    #     if x[1] == 'd':
    #         d += 1
    #     if x[1] == 'c':
    #         c += 1
    #     if x[1] == 's':
    #         s += 1

    # if h > 4 or d > 4 or c > 4 or s > 4:
    #     for i in range(len(cards)-1):
    #         diff = int(cards[i])-int(cards[i-1])
    #         if diff != 1:
    #             if i > 3:
    #                 cards.pop(i)
    #             else:
    #                 cards.pop(i-1)
        
    # return (len(cards) > 4)

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

def countStraightDrawOuts(nums):
    if len(nums) == 7:
        return 0

    x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    count = 0
    for i in x:
        test = nums[:]
        test.append(i)
        test.sort()
        if hasStraight(test):
            count +=1
    return count


def hasGoodFlushDraw(cards):
    hearts = []
    diamonds = []
    spades = []
    clubs = []
    kickers = []

    for x in cards:
        if x[1]=='h':
            hearts.append(x)
        elif x[1]=='d':
            hearts.append(x)
        elif x[1]=='s':
            spades.append(x)
        elif x[1]=='c':
            clubs.append(x)

    if len(hearts)>3:
        kickers = diamonds + spades+ clubs
    elif len(diamonds)>3:
        kickers = hearts + spades + clubs
    elif len(spades)>3:
        kickers = hearts + diamonds + clubs
    elif len(clubs)>3:
        kickers = hearts + diamonds + spades

    for i in kickers:
        if i[0]=='a':
            return True
        elif i[0]=='k':
            return True
        elif i[0]=='q':
            return True
        elif i[0]=='j':
            return True
        else:
            return False

def hasGoodKicker(cards, relevantCard):
    if cards[0] == relevantCard:
        kicker = cards[1]
    else:
        kicker = cards[0]
    if kicker > 9:
        return True
    else:
        return False

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