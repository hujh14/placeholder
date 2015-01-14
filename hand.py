class Hand():
    def __init__(self, cardTuple):
        self.holeCardA = cardTuple[0]
        self.holeCardB = cardTuple[1]
        self.equity = #calls table for preflop
        self.prob = 1.0/(52*51) #should be largely uniform

    def updateEquity(self, board, ourCards):
        # calls equity calculator
        '''
        self.madePair = False
        self.madeTrips = False
        self.madeStraight = False
        self.madeFlush = False
        self.madeFullHouse = False
        self.madeFourOfKind = False
        self.madeStraightFlush = False

        self.hasOpenEndedStraightDraw = False
        self.hasGutShotStraightDraw = False
        self.hasFlushDraw = False'''