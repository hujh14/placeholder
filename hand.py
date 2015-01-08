from pokerHandDist import *
class Hand:

	def __init__ (self, initData):
		# initData contains: NEWHAND handId seat holeCard1 holeCard2 [stackSizes] numActivePlayers [activePlayers] timeBank
		self.handId = initData[1]
		self.seat = initData[2]
		self.holeCard1 = initData[3]
		self.holeCard2 = initData[4]
		self.stackSizes = initData[5]
		self.numActivePlayers = initData[6]
		self.activePlayers = initData[7]
		self.timeBank = initData[8]

		self.opponentHandDist = pokerHandDist(uniform)

	def getBestAction(self,inp):

		return 'FOLD'
		