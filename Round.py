from pokerHandDist import *
import pbots_calc
from hand import *
from allHands import *
import itertools
from preflop import getEq

class Round:

    def __init__ (self, initData, myName, oppAName, oppBName):
        # initData contains: 
        # NEWHAND handId seat holeCard1 holeCard2 [stackSizes] [playerNames] numActivePlayers [activePlayers] timeBank
        # generic stuff that doesn't need to be regenerated every hand.

        self.cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
        self.listOfTuples = [tup for tup in itertools.combinations(self.cardList,2)]
        self.allHands = allHands(self.listOfTuples)
        
        # These get initialized at the start of the hand
        self.handId = int(initData[1])
        #self.seat = int(initData[2])
        self.holeCard1 = initData[3].lower()
        self.holeCard2 = initData[4].lower()
        self.stackSizes = initData[5:8]
        self.playerNames = initData[8:11]
        self.numActivePlayers = int(initData[11])
        self.activePlayers = initData[11:14]
        self.timeBank = float(initData[15])
        
        
        # These get defined once we get the first GETACTION packet
        self.potSize = 0
        self.numBoardCards = -1
        self.boardCards = []


        self.numLastActions = 0
        self.lastActions = []
        self.numLegalActions = 0
        self.legalActions = []

        self.preFlop = True
        self.betInto = True
        
        self.oppAAggression = 0
        self.oppBAggression = 0


        for name in self.playerNames:
            if name == myName:
                self.seat = self.playerNames.index(name)
        if self.seat == self.numActivePlayers - 1:
            self.betInto = False

        self.oppAName = oppAName
        self.oppBName = oppBName
        self.oppAPreflopRaiseNum = 0
        self.oppBPreflopRaiseNum = 0
        self.strugglebotPreflopRaiseNum = 0
        self.oppAProbDist = pokerHandDist(self.listOfTuples)
        self.oppAProbDist.removeExistingCards([self.holeCard1,self.holeCard2])
        self.oppBProbDist = pokerHandDist(self.listOfTuples)
        self.oppBProbDist.removeExistingCards([self.holeCard1,self.holeCard2])



        self.equities = {}
        
        self.maxBet = 1000
        self.maxRaise = 1000

        self.preflopStrength = getEq(self.holeCard1+self.holeCard2)
        

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
                    self.oppAProbDist.removeExistingCards(self.boardCards[self.numBoardCards-1:self.numBoardCards])
                if self.oppBProbDist != None:
                    self.oppBProbDist.removeExistingCards(self.boardCards[self.numBoardCards-1:self.numBoardCards])
            
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

        m = self.legalActions[self.numLegalActions-1].split(':')
        if m[0] == 'BET':
            self.maxBet = int(m[2])
        elif m[0] == 'RAISE':
            self.maxRaise = int(m[2])

        self.parseOpponentsActionsandUpdateTheirRange()
        if not self.preFlop:
            self.updateEquities()


    def parseOpponentsActionsandUpdateTheirRange(self):
        actions = self.lastActions
        
        for action in actions:
            a = action.split(':')
            if self.preFlop:
                if a[0] == 'CHECK':
                    if a[1] == self.oppAName:
                        self.oppAProbDist.preflopUpdate(3)
                    elif a[1] == self.oppBName:
                        self.oppBProbDist.preflopUpdate(3)

                elif a[0] == 'FOLD':
                    if a[1] == self.oppAName:
                        self.oppAProbDist = None
                        self.numActivePlayers -= 1
                    elif a[1] == self.oppBName:
                        self.oppBProbDist = None
                        self.numActivePlayers -= 1
                    
                elif a[0] == 'CALL':
                    # remove everything less than .27 and everything greater than .44 (stuff better than aj)
                    if a[2] == self.oppAName:
                        if a[1] < 6:
                            self.oppAProbDist.preflopUpdate(1)
                        else:
                            self.oppAProbDist.preflopUpdate(2)
                    elif a[2] == self.oppBName:
                        if a[1] < 6:
                            self.oppBProbDist.preflopUpdate(1)
                        else:
                            self.oppBProbDist.preflopUpdate(2)
                        # relatively weak move

                elif a[0] == 'RAISE':
                    # remove everything less than .4
                    if a[2] == self.oppAName:
                        if self.oppAPreflopRaiseNum == 0:
                            self.oppAProbDist.preflopUpdate(2) # update level and use preflop table
                        elif self.oppAPreflopRaiseNum == 1:
                            self.oppAProbDist.preflopUpdate(4)
                        elif self.oppAPreflopRaiseNum == 2:
                            self.oppAProbDist.preflopUpdate(5)
                        else:
                            self.oppAProbDist.preflopUpdate(6)

                        self.oppAPreflopRaiseNum += 1
                        self.betInto = True
                    elif a[2] == self.oppBName:
                        if self.oppBPreflopRaiseNum == 0:
                            self.oppBProbDist.preflopUpdate(2) # update level and use preflop table
                        elif self.oppBPreflopRaiseNum == 1:
                            self.oppBProbDist.preflopUpdate(4)
                        elif self.oppBPreflopRaiseNum == 2:
                            self.oppBProbDist.preflopUpdate(5)
                        else:
                            self.oppBProbDist.preflopUpdate(6)

                        self.oppBPreflopRaiseNum += 1
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
                        if self.numBoardCards == 3:
                            self.oppAProbDist.update('split', 3, 11, self.allHands)
                        else:
                            self.oppAProbDist.update('split', 6, 20, self.allHands)

                elif a[0] == 'FOLD':
                    if a[1] == self.oppAName:
                        self.oppAProbDist = None
                        self.numActivePlayers -= 1
                    elif a[1] == self.oppBName:
                        self.oppBProbDist = None
                        self.numActivePlayers -= 1

                elif a[0] == 'CALL':
                    amountCalled = a[1]
                    percentCalled = float(amountCalled)/self.potSize # not the pot size they bet into needs to be fixed
                    if a[2] == self.oppAName:
                        if self.numBoardCards == 3:
                            self.oppAAggression += int(5*percentCalled)
                        else:
                            self.oppAAggression += int(2*percentCalled)
                        self.oppAProbDist.update('normal', self.oppAAggression, 20, self.allHands)
                    elif a[2] == self.oppBName:
                        if self.numBoardCards == 3:
                            self.oppBAggression += int(5*percentCalled)
                        else:
                            self.oppAAggression += int(2*percentCalled)

                        self.oppBProbDist.update('normal', self.oppBAggression, 20, self.allHands)

                elif a[0] == 'RAISE' or a[0] == 'BET':
                    amountRaised = a[1]
                    percentRaised = float(amountRaised) / self.potSize # not the pot size they bet into needs to be fixed
                    if a[2] == self.oppAName:
                        if self.numBoardCards == 3:
                            self.oppAAggression += int(5*percentRaised) 
                        else:
                            self.oppAAggression += int(2*percentRaised) 
                        self.oppAProbDist.update('normal', self.oppAAggression, 20, self.allHands)
                        self.betInto = True
                        
                    elif a[2] == self.oppBName:
                        if self.numBoardCards == 3:
                            self.oppBAggression += int(5*percentRaised) 
                        else:
                            self.oppBAggression += int(2*percentRaised) 

                        self.oppBProbDist.update('normal', self.oppBAggression, 20, self.allHands)
                        self.betInto = True


    def getBestAction(self):
        #print self.handId
        # if self.oppAProbDist != None:
        #     print 'Opp A Range', self.oppAProbDist.distribution.keys()
        # if self.oppBProbDist != None:
        #     print 'Opp B Range', self.oppBProbDist.distribution.keys()




        if self.preFlop:
            if self.betInto:
                self.betInto = False
                numTimesRaisedPreflop = self.oppAPreflopRaiseNum+self.oppBPreflopRaiseNum+self.strugglebotPreflopRaiseNum

                # do I want to call?
                for action in self.legalActions:
                    a = action.split(':')
                    if a[0] == "CALL":
                        amountToCall = int(a[1])
                
                if True: #self.numActivePlayers == 2:
                    if numTimesRaisedPreflop == 0:
                        if self.preflopStrength > .41:
                            self.strugglebotPreflopRaiseNum += 1
                            return 'RAISE:'+ str(min(max(self.potSize/2+amountToCall, 4),self.maxRaise))
                        elif amountToCall == 1:
                            if self.preflopStrength > .19:
                                return 'CALL:' + str(amountToCall)
                            else:
                                return 'FOLD'
                        elif self.preflopStrength > .31:
                            return 'CALL:' + str(amountToCall)
                        else:
                            return 'FOLD'
                    if numTimesRaisedPreflop == 1:
                        if self.preflopStrength > .455:
                            self.strugglebotPreflopRaiseNum += 1
                            return 'RAISE:'+ str(min(max(self.potSize/2+amountToCall, 4),self.maxRaise))
                        elif self.preflopStrength > .405:
                            return 'CALL:' + str(amountToCall)
                        elif self.preflopStrength > .33 and amountToCall < 5:
                            return 'CALL:' + str(amountToCall)
                        else:
                            return 'FOLD'
                    if numTimesRaisedPreflop == 2:
                        if self.preflopStrength > .6:
                            self.strugglebotPreflopRaiseNum += 1
                            return 'RAISE:'+ str(min(max(self.potSize/2+amountToCall, 4),self.maxRaise))
                        elif self.preflopStrength > .468:
                            return 'CALL:' + str(amountToCall)
                        else:
                            return 'FOLD'
                    else:
                        if self.preflopStrength == .64:
                            self.strugglebotPreflopRaiseNum += 1
                            return 'RAISE:'+ str(min(max(self.potSize/2+amountToCall, 4),self.maxRaise))
                        elif self.preflopStrength > .48:
                            return 'CALL:' + str(amountToCall)
                        else:
                            return 'FOLD'

                # elif self.numActivePlayers == 3:
                #     if self.preflopStrength > .6:
                #         return 'RAISE:'+ str(min(max(self.potSize/2+amountToCall, 4),self.maxRaise))
                #     elif self.preflopStrength > .37:
                #         return 'CALL:' + str(amountToCall)
                #     else:
                #         return 'FOLD'

                # calculate expected value to decided to call
                
                
            else:
                
                if self.preflopStrength > .43:
                    return 'RAISE:'+ str(min(max(self.potSize/2,4),self.maxRaise)) # raising off the big blind there is a minimum
                else:
                    return 'CHECK'
                
        else:
            expectedEquity = self.expectedEquity()
            #print 'expected Equity', expectedEquity
            if self.betInto:
                for action in self.legalActions:
                    a = action.split(':')
                    if a[0] == "CALL":
                        amountToCall = int(a[1])
                potOdds = float(amountToCall)/(amountToCall+self.potSize)
            
            if self.numActivePlayers == 2:
                if self.betInto:
                    self.betInto = False
                    if expectedEquity > .8 and self.numBoardCards != 3:
                        return 'CALL:' + str(amountToCall)
                    elif expectedEquity > .55:
                        return 'RAISE:'+ str(min(self.potSize/2+amountToCall,self.maxRaise))
                    elif potOdds < expectedEquity:
                        return 'CALL:' + str(amountToCall)
                    else:
                        return 'FOLD'
                    
                else:
                    if expectedEquity > .8:
                        if self.numBoardCards == 3:
                            return 'CHECK'
                        else:
                            return 'BET:'+ str(min(self.potSize/2,self.maxBet))
                    elif expectedEquity > .5:
                        return 'BET:'+ str(min(self.potSize/2,self.maxBet))
                    else:
                        return 'CHECK'

            elif self.numActivePlayers == 3:
                if self.betInto:
                    self.betInto = False
                    if expectedEquity > .75:
                        return 'CALL:' + str(amountToCall)
                    elif expectedEquity > .43:
                        return 'RAISE:'+ str(min(int(self.potSize/1.5)+amountToCall,self.maxRaise))
                    elif potOdds < expectedEquity:
                        return 'CALL:' + str(amountToCall)
                    else:
                        return 'FOLD'
                    
                else:
                    if expectedEquity > .75:
                        if self.numBoardCards == 3:
                            return 'CHECK'
                        else:
                            return 'BET:'+ str(min(self.potSize/2,self.maxBet))
                    elif expectedEquity > .45:
                        return 'BET:'+ str(min(self.potSize/2,self.maxBet))
                    else:
                        return 'CHECK'

        
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
        if self.oppAProbDist == None:
            combinedList = self.oppBProbDist.distribution.keys()
        elif self.oppBProbDist == None:
            combinedList = self.oppAProbDist.distribution.keys()
        else:
            combinedList = list(set(list(self.oppAProbDist.distribution.keys()) + list(self.oppBProbDist.distribution.keys())))

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
        return totalA*totalB

        # print('A Name', self.oppAName)
        # print('A', self.oppAProbDist.distribution)
        # print('A length', len(self.oppAProbDist.distribution))
        # print('B Name', self.oppBName)
        # print('B', self.oppBProbDist.distribution)
        # print('B length', len(self.oppBProbDist.distribution))
        # print('total', totalA * totalB)
        #return total


# data = ['NEWHAND', '24', '3', 'Jc', 'Ac', '218', '200', '182', 'P32', 'P22', 'struggleBot2', '3', 'true', 'true', 'true', '-1.616462']
# r = Round(data)
# parse = ['GETACTION', '10', '0', '216', '194', '180', '3', 'true', 'true', 'true', '4', 'POST:1:P22', 'POST:2:struggleBot2', 'CALL:2:P32', 'RAISE:6:P22', '3', 'FOLD', 'CALL:6', 'RAISE:10:20', '-1.616461590000002']
# parse2 = ['GETACTION', '18', '3', '7h', '3c', '9c', '212', '194', '176', '3', 'true', 'true', 'true', '4', 'CALL:6:struggleBot2', 'CALL:6:P32', 'DEAL:FLOP', 'CHECK:P22', '2', 'CHECK', 'BET:2:18', '-2.123151129000002']
# # parse3 = ['GETACTION', '4', '4', 'As', 'Ah', '5c', 'Th', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:TURN', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.609433912']
# # parse4 = ['GETACTION', '4', '5', 'As', 'Ah', '5c', 'Th', 'Kc', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:RIVER', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.547964306']
# r.parsePacket(parse)
# #r.parsePacket(parse2)
# print r.getBestAction()
# r.parsePacket(parse2)
# print r.getBestAction()



        


# data = ['NEWHAND', '11', '3', 'Kd', 'Ad', '233', '176', '188', '3', 'true', 'true', 'true', '8.789302']
# r = Round(data, 'P2', 'P3')
# parse = ['GETACTION', '9', '0', '233', '175', '188', '3', 'true', 'true', 'true', '4', 'POST:1:P3', 'POST:2:v1', 'CALL:2:P2', 'RAISE:4:P3', '3', 'CHECK','CALL:2', 'RAISE:4:6', '8.789301610999999']
# parse2 = ['GETACTION', '15', '3', 'As', 'Ah', '5c', '233', '175', '188', '3', 'true', 'true', 'true', '4', 'CALL:2:v1', 'DEAL:FLOP', 'CHECK:P2', 'RAISE:5:P3', '3', 'CHECK','CALL:5', 'BET:2:4', '8.664166238']
# # parse3 = ['GETACTION', '4', '4', 'As', 'Ah', '5c', 'Th', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:TURN', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.609433912']
# # parse4 = ['GETACTION', '4', '5', 'As', 'Ah', '5c', 'Th', 'Kc', '233', '175', '188', '3', 'true', 'true', 'true', '3', 'CHECK:v1', 'DEAL:RIVER', 'CHECK:P3', '2', 'CHECK', 'BET:2:4', '8.547964306']
# r.parsePacket(parse)
# print r.getBestAction()

# r.parsePacket(parse2)
# print r.getBestAction()


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
