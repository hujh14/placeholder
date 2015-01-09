from pokerHandDist import *
class Hand:

	def __init__ (self, initData):
		# initData contains: NEWHAND handId seat holeCard1 holeCard2 [stackSizes] numActivePlayers [activePlayers] timeBank

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

		#self.opponentHandDist = pokerHandDist(uniform)

        def parsePacket(self,inp):
                # inp contains: GETACTION potSize numBoardCards
                # [boardCards] [stackSizes] numActivePlayers
                # [activePlayers] numLastActions [lastActions]
                # numLegalActions [legalActions] timebank

                # I'm so sorry
                # Do parse things
                # Grabs the lists in the packet and puts them in actual lists
                inp = [inp[0], inp[1], inp[3:int(inp[2]) + 3]] + inp[int(inp[2]) + 3:]
                inp = inp[0:3] + [inp[3:6], inp[6], inp[7:10],
                                  inp[10], inp[11:int(inp[10]) + 11]] + inp[int(inp[10]) + 11:]
                inp = inp[0:9] + [inp[9:int(inp[8]) + 9]] + inp[int(inp[8]) + 9:]
        
                self.potSize = int(inp[1])
                self.numBoardCards = len(inp[2])
                self.boardCards = inp[3]
                self.numActivePlayers = int(inp[4])
                self.activePlayers = inp[5]
                for i in range(0, len(inp[5])):
                        self.activePlayers[i] = strToBool(self.activePlayers[i])
                self.numLastActions = int(inp[6])
                self.lastActions = inp[7]
                self.numLegalActions = int(inp[8])
                self.legalActions = inp[9]
                self.timeBank = float(inp[10])

	def getBestAction(self):

                print self.holeCard1
                print self.holeCard2
                v = self.value(self.holeCard1) + self.value(self.holeCard2)
                if v < 15:
                        return 'CHECK'
                else:
                        return 'RAISE:2'
                
        def strToBool(str):
                if str.lower() == 'true':
                        return True
                else:
                        return False
        
        def value(self, card):
                card = card[0]
                if card == 'T':
                        return 10
                elif card == 'J':
                        return 11
                elif card == 'Q':
                        return 12
                elif card == 'K':
                        return 13
                elif card == 'A':
                        return 14
                else:
                        return int(card)
