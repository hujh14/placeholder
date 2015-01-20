from pokerHandDist import *
import pbots_calc
from hand import *
from allHands import *
import itertools
import equityCalc

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

<<<<<<< HEAD
        self.oppAProbDist = pokerHandDist(self.listOfTuples).removeExistingCards(self.holeCard1,self.holeCard2)
        self.oppBProbDist = pokerHandDist(self.listOfTuples).removeExistingCards(self.holeCard1,self.holeCard2)
=======
        self.oppAProbDist = pokerHandDist(self.listOfTuples)#.removeExistingCards([self.holeCard1,self.holeCard2])
        self.oppBProbDist = pokerHandDist(self.listOfTuples)#.removeExistingCards([self.holeCard1,self.holeCard2])
        
        self.blank = {'3c':2}
>>>>>>> FETCH_HEAD


        self.equities = {} # get from table
        #self.calculator = Results()
        
        
        

    def parsePacket(self,inp):
        # inp contains: GETACTION potSize numBoardCards
        # [boardCards] [stackSizes] numActivePlayers
        # [activePlayers] numLastActions [lastActions]
        # numLegalActions [legalActions] timebank

        # GETACTION 30 5 As Ks Qh Qd Qc 200 200 200
        # 2 true true false 3 CHECK:two CHECK:one DEAL:RIVER
        # 2 CHECK BET:2:30 19.997999999999998

        # Split to list
        t = str(type(inp))
        if t == "<class 'str'>" or t == "<type 'str'>":
            inp = inp.split()
            
        # Trim "GETACTION" header
        inp = inp[1:]
        self.activePlayers, self.lastActions = [], []
        self.stackSizes, self.legalActions = [], []
        # Set pot
        self.potSize = int(inp.pop(0))
        # Get board cards
        temp = int(inp.pop(0))
        # trigger update with new board
        if self.numBoardCards != temp:
            self.numBoardCards = temp
            self.boardCards = []
            for i in range(self.numBoardCards):
                self.boardCards += [inp.pop(0).lower()]
            self.allHands.update(self.boardCards)
            if temp == 3:
                self.oppAProbDist.removeExistingCards(self.boardCards)
                self.oppBProbDist.removeExistingCards(self.boardCards)
            else:
                self.oppAProbDist.removeExistingCards(self.boardCards[-1:])
                self.oppBProbDist.removeExistingCards(self.boardCards[-1:])
            self.updateEquities()
        else:
            for i in range(self.numBoardCards):
                inp.pop(0)
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

    def parseActions(self):
        a = self.lastActions[:]
        

        
    def getBestAction(self):
    
        
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
            for keyA in self.oppAProbDist.distribution.keys():
                keyAId = self.allHands.getId(keyA)
                if keyAId not in tempEquityDictionary:
                    # print [(self.holeCard1,self.holeCard2),keyA]
                    # print self.boardCards
                    # eq = pbots_calc.calc([(self.holeCard1,self.holeCard2),keyA], self.boardCards, '', 10).ev[0]
                    eq = equityCalc.getEquity([self.holeCard1,self.holeCard2], keyA, self.boardCards, 100)
                    self.equities[keyA] = eq
                    tempEquityDictionary[keyAId] = eq
                else:
                    self.equities[keyA] = tempEquityDictionary[keyAId]

            
            # for keyA in self.oppAProbDist.keys():
            #     for keyB in self.oppBProbDist.keys():
            #         keyAId = self.allHands.getId(keyA)
            #         #print keyA,keyB, keyAId
            #         keyBId = self.allHands.getId(keyB)
            #         if (keyAId,keyBId) not in tempEquityDictionary and (keyBId,keyAId) not in tempEquityDictionary:
            #             #query equity calculator
            #             eq = self.calculator.calc([self.holeCard1+self.holeCard2, keyA, keyB])
            #             tempEquityDictionary[(keyAId, keyBId)] = eq
            #             self.equities[(keyA,keyB)] = eq
            #         else:
            #             if (keyAId,keyBId) in tempEquityDictionary:
            #                 eq = tempEquityDictionary[(keyAId,keyBId)]
            #             else:
            #                 eq = tempEquityDictionary[(keyBId,keyAId)]
            #             self.equities[(keyA,keyB)] = eq
            #     print len(self.equities)



# data = ['NEWHAND', '6', '3', '4c', '5s', '180', '223', '194', '3', 'true', 'true', 'true', '9.976153']
# r = Round(data)
# parse = ['GETACTION', '5', '0', '178', '223', '194', '3', 'true', 'true', 'true', '4', 'POST:1:P3', 'POST:2:v1', 'CALL:2:P2', 'FOLD:P3', '2', 'CHECK', 'RAISE:4:7', '9.976153464000001']
# parse2 = ['GETACTION', '5', '3', '7h', '6s', '5h', '178', '223', '194', '3', 'true', 'true', 'true', '2', 'CHECK:v1', 'DEAL:FLOP', '2', 'CHECK', 'BET:2:5', '9.972645038000001']
# r.parsePacket(parse)
# r.parsePacket(parse2)
# #for h in r.allHands.hands:
# #    print h.cards, h.Id
# print r.holeCard1,r.holeCard2
# print r.boardCards
# #print r.oppAProbDist
# for key in r.equities:
#     print key, r.equities[key]
# print len(r.equities)

# #print equityCalc.getEquity(['ah','ad'], ['as','5h'], [], 1000)
# print pbots_calc.calc([('4c', '5s'), ('5h', 'jh')],['7h', '6s', '5d'],'', 1000).ev[0]




