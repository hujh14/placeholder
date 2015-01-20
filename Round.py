from pokerHandDist import *
from pbots_calc import *
from hand import *
from allHands import *
import itertools


class Round:

    def __init__ (self, initData):
        # initData contains: NEWHAND handId seat holeCard1 holeCard2 [stackSizes] numActivePlayers [activePlayers] timeBank

        # generic stuff that doesn't need to be regenerated every hand.
        self.cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
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

        self.oppAProbDist = pokerHandDist(self.listOfTuples).removeExistingCards(self.allHands,[(self.holeCard1,self.holeCard2),(self.holeCard2,self.holeCard1)])
        self.oppBProbDist = pokerHandDist(self.listOfTuples).removeExistingCards(self.allHands,[(self.holeCard1,self.holeCard2),(self.holeCard2,self.holeCard1)])


        self.equities = {} # get from table
        
        
        

    def parsePacket(self,inp):
        # inp contains: GETACTION potSize numBoardCards
        # [boardCards] [stackSizes] numActivePlayers
        # [activePlayers] numLastActions [lastActions]
        # numLegalActions [legalActions] timebank

        # GETACTION 30 5 As Ks Qh Qd Qc 200 200 200
        # 2 true true false 3 CHECK:two CHECK:one DEAL:RIVER
        # 2 CHECK BET:2:30 19.997999999999998

        # I'm so sorry
        # Do parse things
        # Grabs the lists in the packet and puts them in actual lists


        # self.potSize = int(inp[1])

        # if self.numBoardCards != int(inp[2]):
        #     self.allHands.update(self.boardCards,self.holeCard1,self.holeCard2)
        #     self.updateEquities()
        #     self.numBoardCards = int(inp[2])

        # self.boardCards = inp[3]
        # self.numActivePlayers = int(inp[4])
        # self.activePlayers = inp[5]
        # for i in range(0, len(inp[5])):
        #     self.activePlayers[i] = self.strToBool(self.activePlayers[i])
        # self.numLastActions = int(inp[6])
        # self.lastActions = inp[7]
        # self.numLegalActions = int(inp[8])
        # self.legalActions = inp[9]
        # self.timeBank = float(inp[10])

        # Split to list
        t = str(type(inp))
        if t == "<class 'str'>" or t == "<type 'str'>":
            inp = inp.split()
        # Trim "GETACTION" header
        inp = inp[1:]
        self.boardCards, self.activePlayers, self.lastActions = [], [], []
        self.stackSizes, self.legalActions = [], []
        # Set pot
        self.potSize = int(inp.pop(0))
        # Get board cards
        temp = int(inp.pop(0))
        # trigger update with new board
        if self.numBoardCards != temp:
            self.numBoardCards = temp
            for i in range(self.numBoardCards):
                self.boardCards += [inp.pop(0)]
            self.allHands.update(self.boardCards)
            self.updateEquities()
        else:
            for i in range(self.numBoardCards):
                self.boardCards += [inp.pop(0)]
        for i in range(3):
            self.stackSizes += [inp.pop(0)]
        self.numActivePlayers = int(inp.pop(0))
        for i in range(3):
            self.activePlayers += [self.strToBool(inp.pop(0))]
        self.numLastActions = int(inp.pop(0))
        for i in range(self.numLastActions):
            self.lastActions += [inp.pop(0)]
        self.numLegalActions = int(inp.pop(0))
        for i in range(self.numLegalActions):
            self.legalActions += [inp.pop(0)]
        self.timeBank = float(inp.pop(0))


        
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
        if self.numActivePlayers == 3:
            tempEquityDictionary = {}
            self.equities = {}
            eq = 0
            print len(self.oppAProbDist.distribution)
            for keyA in self.oppAProbDist.distribution:
                for keyB in self.blank:
                    keyAId = self.allHands.getId(keyA)
                    print keyA, keyAId
                    keyBId = self.allHands.getId(keyB)
                    if (keyAId,keyBId) not in tempEquityDictionary and (keyBId,keyAId) not in tempEquityDictionary:
                        #query equity calculator
                        eq += 1
                        tempEquityDictionary[(keyAId, keyBId)] = eq
                        self.equities[(keyA,keyB)] = eq
                    else:
                        if (keyAId,keyBId) in tempEquityDictionary:
                            eq = tempEquityDictionary[(keyAId,keyBId)]
                        else:
                            eq = tempEquityDictionary[(keyBId,keyAId)]
                        self.equities[(keyA,keyB)] = eq



data = ['NEWHAND', '6', '3', '4c', '5s', '180', '223', '194', '3', 'true', 'true', 'true', '9.976153']
r = Round(data)
parse = ['GETACTION', '5', '0', '178', '223', '194', '3', 'true', 'true', 'true', '4', 'POST:1:P3', 'POST:2:v1', 'CALL:2:P2', 'FOLD:P3', '2', 'CHECK', 'RAISE:4:7', '9.976153464000001']
parse2 = ['GETACTION', '5', '3', '7h', '6s', '5h', '178', '223', '194', '3', 'true', 'true', 'true', '2', 'CHECK:v1', 'DEAL:FLOP', '2', 'CHECK', 'BET:2:5', '9.972645038000001']
r.parsePacket(parse)
r.parsePacket(parse2)
print r.holeCard1,r.holeCard2
print r.boardCards
print r.oppAProbDist.distribution
print r.equities
print r.allHands.hands[0].Id

