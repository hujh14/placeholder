class Hand():
    def __init__(self, cardTuple):
        self.holeCardA = cardTuple[0]
        self.holeCardB = cardTuple[1]

        self.madePairA = False
        self.madePairB = False
        self.madePairC = 
        self.madeTrips = False
        self.madeStraight = False
        self.madeFlush = False
        self.madeFullHouse = False
        self.madeFourOfKind = False
        self.madeStraightFlush = False

        self.hasOpenEndedStraightDraw = False
        self.hasGutShotStraightDraw = False
        self.hasFlushDraw = False

        self.ID = 0
        

    def update(self, board, ourCards):
        # Updates boolean profile
        