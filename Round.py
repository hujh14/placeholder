from pokerHandDist import *
import pbots_calc
from hand import *
from allHands import *
import itertools
import equityCalc

class Round:

    def __init__ (self, initData, oppA, oppB):
        # initData contains: NEWHAND handId seat holeCard1 holeCard2 [stackSizes] numActivePlayers [activePlayers] timeBank

        # generic stuff that doesn't need to be regenerated every hand.
        self.cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
        self.listOfTuples = [tup for tup in itertools.combinations(self.cardList,2)]
        self.allHands = allHands(self.listOfTuples)
        
        # These get initialized at the start of the hand
        self.handId = int(initData[1])
        self.seat = int(initData[2])
        self.holeCard1 = initData[3].lower()
        self.holeCard2 = initData[4].lower()
        self.stackSizes = initData[5:8]
        self.numActivePlayers = int(initData[8])
        self.activePlayers = initData[9:12]
        self.timeBank = float(initData[12])
        
        # These get defined once we get the first GETACTION packet
        self.potSize = 0
        self.numBoardCards = -1
        self.boardCards = []
        self.stackSizes = []
        self.numActivePlayers = 0
        self.activePlayers = []
        self.numLastActions = 0
        self.lastActions = []
        self.numLegalActions = 0
        self.legalActions = []

        self.preFlop = True
        self.betInto = False
        self.oppAAggression = 0
        self.oppBAggression = 0




        # this Class needs help!!!!
        #self.oppA = pokerHandDist(self.listOfTuples).removeExistingCards([(self.holeCard1,self.holeCard2)])
        #self.oppB = pokerHandDist(self.listOfTuples).removeExistingCards([(self.holeCard1,self.holeCard2)])
            
        # initialize possible hand objects

        self.oppAName = oppA
        self.oppBName = oppB
        self.oppAProbDist = pokerHandDist(self.listOfTuples)
        self.oppAProbDist.removeExistingCards([self.holeCard1,self.holeCard2])
        self.oppBProbDist = pokerHandDist(self.listOfTuples)
        self.oppBProbDist.removeExistingCards([self.holeCard1,self.holeCard2])

        



        self.equities = {} # get from table
        
        self.startingHandStrengths = {} # get from table
        
        

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

            #self.allHands.update(self.boardCards)

            if temp == 3:
                if self.oppAProbDist != None:
                    self.oppAProbDist.removeExistingCards(self.boardCards)
                if self.oppBProbDist != None:
                    self.oppBProbDist.removeExistingCards(self.boardCards)
            else:
                if self.oppAProbDist != None:
                    self.oppAProbDist.removeExistingCards(self.boardCards[:len(self.boardCards)-1])
                if self.oppBProbDist != None:
                    self.oppBProbDist.removeExistingCards(self.boardCards[:len(self.boardCards)-1])



            
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


        self.parseOpponentsActionsandUpdateTheirRange()
        self.updateEquities()


        

    def parseOpponentsActionsandUpdateTheirRange(self):
        print self.holeCard1,self.holeCard2
        print self.boardCards
        actions = self.lastActions
        print 'actions', actions
        
        for action in actions:
            a = action.split(':')
            if self.preFlop:
                if a[0] == 'CHECK':
                    pass
                elif a[0] == 'FOLD':
                    if a[1] == self.oppAName:
                        self.oppAProbDist = None
                        self.numActivePlayers -= 1
                    elif a[1] == self.oppBName:
                        self.oppBProbDist = None
                        self.numActivePlayers -= 1
                    # delete opp distribution
                    # change num of active players
                elif a[0] == 'CALL':
                    if a[2] == self.oppAName:
                        self.oppAProbDist.preflopUpdate(1, self.startingHandStrengths)
                    elif a[2] == self.oppBName:
                        self.oppBProbDist.preflopUpdate(1, self.startingHandStrengths)
                    # relatively weak move

                elif a[0] == 'RAISE':
                    if a[2] == self.oppAName:
                        self.oppAProbDist.preflopUpdate(2, self.startingHandStrengths) # update level and use preflop table
                    elif a[2] == self.oppBName:
                        self.oppBProbDist.preflopUpdate(2, self.startingHandStrengths)
                    self.betInto = True

                elif a[0] == 'POST':
                    pass
                elif a[0] == 'DEAL':
                    self.allHands.update(self.boardCards)
                    self.preFlop = False

            else: 
                if a[0] == 'DEAL':
                    self.allHands.update(self.boardCards)

                elif a[0] == 'CHECK':
                    if a[1] == self.oppAName:
                        pass
                        # should show weakness

                elif a[0] == 'FOLD':
                    if a[1] == self.oppAName:
                        self.oppAProbDist = None
                        self.numActivePlayers -= 1
                    elif a[1] == self.oppBName:
                        self.oppBProbDist = None
                        self.numActivePlayers -= 1

                elif a[0] == 'CALL':
                    amountCalled = a[1]
                    if a[2] == self.oppAName:
                        self.oppAAggression += int(3*(float(amountCalled) / self.potSize))
                        self.oppAProbDist.update(self.oppAAggression, self.allHands)
                    elif a[2] == self.oppBName:
                        self.oppBAggression += int(6*(float(amountCalled) / self.potSize)) # not the pot size they bet into needs to be fixed
                        self.oppBProbDist.update(self.oppBAggression, self.allHands)

                elif a[0] == 'RAISE':
                    amountRaised = a[1]
                    if a[2] == self.oppAName:
                        self.oppAAggression += int(6*(float(amountRaised) / self.potSize)) # not the pot size they bet into needs to be fixed
                        self.oppAProbDist.update(self.oppAAggression, self.allHands)
                        
                    elif a[2] == self.oppBName:
                        self.oppBAggression += int(6*(float(amountRaised) / self.potSize)) # not the pot size they bet into needs to be fixed
                        self.oppBProbDist.update(self.oppBAggression, self.allHands)

                        #self.oppAProbDist.update(3,self.allHands)
            


    def getBestAction(self):
        self.expectedEquity()
        if self.preFlop:
            if self.betInto:
                # calculate expected value to decided to call
                self.expectedEquity()
                self.betInto = False
            else:
                pass
        else:
            pass
        
        # v = 2
        # if v < 15:
        #     return 'CHECK'
        # else:
        #     return 'RAISE:2'
            
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
        if self.numActivePlayers == 2:
            if self.oppAProbDist != None:
                combinedList = self.oppAProbDist.distribution.keys()
            else:
                combinedList = self.oppBProbDist.distribution.keys()
        elif self.numActivePlayers == 3:
            combinedList = list(set(self.oppAProbDist.distribution.keys() + self.oppBProbDist.distribution.keys()))

        # without boolean check
        self.equities = {}
        for keyA in combinedList: # should be combined distribution
            eq = pbots_calc.calc([(self.holeCard1,self.holeCard2),keyA], self.boardCards, '', 1000).ev[0]
            self.equities[keyA] = eq

        # # With boolean check
        # if self.numActivePlayers == 3:
        #     tempEquityDictionary = {}
        #     self.equities = {}
        #     eq = 0
        #     for keyA in self.oppAProbDist.distribution.keys():
        #         keyAId = self.allHands.getId(keyA)
        #         if keyAId not in tempEquityDictionary:
        #             # print [(self.holeCard1,self.holeCard2),keyA]
        #             # print self.boardCards
        #             eq = pbots_calc.calc([(self.holeCard1,self.holeCard2),keyA], self.boardCards, '', 1000).ev[0]
        #             # eq = equityCalc.getEquity([self.holeCard1,self.holeCard2], keyA, self.boardCards, 100)
        #             self.equities[keyA] = eq
        #             tempEquityDictionary[keyAId] = eq
        #         else:
        #             self.equities[keyA] = tempEquityDictionary[keyAId]

        # # for three players at the same time
        # # doesn't work since opponents might have the same cards
        # if self.numActivePlayers == 3:
        #     tempEquityDictionary = {}
        #     self.equities = {}
        #     eq = 0
        #     for keyA in self.oppAProbDist.distribution.keys():
        #         for keyB in self.oppBProbDist.distribution.keys():
        #             keyAId = self.allHands.getId(keyA)
        #             #print keyA,keyB, keyAId
        #             keyBId = self.allHands.getId(keyB)
        #             if (keyAId,keyBId) not in tempEquityDictionary and (keyBId,keyAId) not in tempEquityDictionary:
        #                 #query equity calculator
        #                 print [(self.holeCard1,self.holeCard2),keyA,keyB], self.boardCards
        #                 eq = pbots_calc.calc([(self.holeCard1,self.holeCard2),keyA,keyB], self.boardCards, '', 10000).ev[0]
        #                 tempEquityDictionary[(keyAId, keyBId)] = eq
        #                 self.equities[(keyA,keyB)] = eq
        #             else:
        #                 if (keyAId,keyBId) in tempEquityDictionary:
        #                     eq = tempEquityDictionary[(keyAId,keyBId)]
        #                 else:
        #                     eq = tempEquityDictionary[(keyBId,keyAId)]
        #                 self.equities[(keyA,keyB)] = eq
        #         print len(self.equities)

    def expectedEquity(self):
        totalA = 0
        totalB = 0
        if self.oppAProbDist != None:
            for key in self.oppAProbDist.distribution:
                totalA += self.oppAProbDist.distribution[key] * self.equities[key]
        else:
            totalA = 1
        if self.oppBProbDist != None:
            for key in self.oppBProbDist.distribution:
                totalB += self.oppBProbDist.distribution[key] * self.equities[key]
        else:
            totalB = 1
        print 'A', self.oppAProbDist
        print 'B Name', self.oppBName
        print 'B', self.oppBProbDist.distribution
        print 'B length', len(self.oppBProbDist.distribution)
        print 'total', totalA*totalB
        #return total


data = ['NEWHAND', '11', '3', 'Jd', '3d', '233', '176', '188', '3', 'true', 'true', 'true', '8.789302']
r = Round(data, 'P2', 'P3')
parse = ['GETACTION', '4', '0', '233', '175', '188', '3', 'true', 'true', 'true', '4', 'POST:1:P3', 'POST:2:v1', 'FOLD:P2', 'CALL:2:P3', '2', 'CHECK', 'RAISE:4:6', '8.789301610999999']
parse2 = ['GETACTION', '4', '3', 'As', 'Ah', '5c', '233', '175', '188', '2', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:FLOP', 'RAISE:5:P3', '2', 'CHECK', 'BET:2:4', '8.664166238']
# parse3 = ['GETACTION', '4', '4', 'As', 'Ah', '5c', 'Th', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:TURN', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.609433912']
# parse4 = ['GETACTION', '4', '5', 'As', 'Ah', '5c', 'Th', 'Kc', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:RIVER', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.547964306']
r.parsePacket(parse)
r.parsePacket(parse2)
r.getBestAction()

# # These get initialized at the start of the hand
# print r.handId
# print r.seat
# print r.holeCard1
# print r.holeCard2
# print r.stackSizes
# print r.numActivePlayers
# print r.activePlayers
# print r.timeBank

# # These get defined once we get the first GETACTION packet
# print r.potSize
# print r.numBoardCards
# print r.boardCards
# print r.stackSizes
# print r.numActivePlayers
# print r.activePlayers
# print r.numLastActions
# print r.lastActions
# print r.numLegalActions
# print r.legalActions






#for h in r.allHands.hands:
#    print h.cards, h.Id

#print r.oppAProbDist
#r.oppAProbDist.update(3,r.allHands)


# for key in r.equities:
#     print key, r.equities[key], r.allHands.getStrength(key)
# print len(r.equities)



#print equityCalc.getEquity(['ah','ad'], ['as','5h'], [], 1000)
#print pbots_calc.calc([('4c', '5s'), ('5h', 'jh')],['7h', '6s', '5d'],'', 1000).ev[0]