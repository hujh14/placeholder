from pokerHandDist import *
from pbots_calc import *
from hand import *
from allHands import *
import itertools


class Round:

    def __init__ (self, initData):
        # initData contains: NEWHAND handId seat holeCard1 holeCard2 [stackSizes] numActivePlayers [activePlayers] timeBank

        # generic stuff that doesn't need to be regenerated every hand.
        self.cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','Ts','Js','Qs','Ks','As','2c','3c','4c','5c','6c','7c','8c','9c','Tc','Jc','Qc','Kc','Ac','2h','3h','4h','5h','6h','7h','8h','9h','Th','Jh','Qh','Kh','Ah','2d','3d','4d','5d','6d','7d','8d','9d','Td','Jd','Qd','Kd','Ad']
        self.listOfTuples = [tup for tup in itertools.combinations(self.cardList,2)]
        self.allHands = allHands(self.listOfTuples)
        
        # These get initialized at the start of the hand
        self.handId = int(initData[1])
        self.seat = int(initData[2])
        self.holeCard1 = initData[3]
        self.holeCard2 = initData[4]
        self.stackSizes = initData[5:8]
        self.numActivePlayers = int(initData[8])
        self.activePlayers = initData[9:12]
        self.timeBank = float(initData[12])
        
            # These get defined once we get the first GETACTION packet
        self.potSize = 0
        self.numBoardCards = 0
        self.boardCards = []
        self.stackSizes = []
        self.numActivePlayers = 0
        self.activePlayers = []
        self.numLastActions = 0
        self.lastActions = []
        self.numLegalActions = 0
        self.legalActions = []

        # this Class needs help!!!!
        #self.oppA = pokerHandDist(self.listOfTuples).removeExistingCards([(self.holeCard1,self.holeCard2)])
        #self.oppB = pokerHandDist(self.listOfTuples).removeExistingCards([(self.holeCard1,self.holeCard2)])
            
        # initialize possible hand objects
        self.oppAProbDist = pokerHandDist(self.listOfTuples)
        self.oppBProbDist = pokerHandDist(self.listOfTuples)

        self.equities = # get from table
        
        

    def parsePacket(self,inp):
        # inp contains: GETACTION potSize numBoardCards
        # [boardCards] [stackSizes] numActivePlayers
        # [activePlayers] numLastActions [lastActions]
        # numLegalActions [legalActions] timebank

        # I'm so sorry
        # Do parse things
        # Grabs the lists in the packet and puts them in actual lists
        inp = [inp[0], inp[1], inp[3:int(inp[2]) + 3]] + inp[int(inp[2]) + 3:]
        inp = inp[0:3] + [inp[3:6], inp[6], inp[7:10], inp[10], inp[11:int(inp[10]) + 11]] + inp[int(inp[10]) + 11:]
        inp = inp[0:9] + [inp[9:int(inp[8]) + 9]] + inp[int(inp[8]) + 9:]

        self.potSize = int(inp[1])

        if self.numBoardCards != int(inp[2]):
            self.allHands.update(self.boardCards,self.holeCard1,self.holeCard2)
            self.updateEquities()
            self.numBoardCards = int(inp[2])

        self.boardCards = inp[3]
        self.numActivePlayers = int(inp[4])
        self.activePlayers = inp[5]
        for i in range(0, len(inp[5])):
            self.activePlayers[i] = self.strToBool(self.activePlayers[i])
        self.numLastActions = int(inp[6])
        self.lastActions = inp[7]
        self.numLegalActions = int(inp[8])
        self.legalActions = inp[9]
        self.timeBank = float(inp[10])

        

    def getBestAction(self):
    
        print self.holeCard1
        print self.holeCard2
        v = 2
        if v < 15:
            return 'CHECK'
        else:
            return 'RAISE:2'
            
    def strToBool(self, s):
        if s.lower() == 'true':
            return True
        else:
            return False
    

    def updateEquities(self):
        # consider num of active players
        # group by boolean profiles
        # find all combinations of boolean profiles
        # query equity calculator
        # generate full list
        pass


        

