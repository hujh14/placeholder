from hand import *

class allHands():
	def __init__(self, listOfTuples):
		self.hands = [Hand(tup) for tup in listOfTuples]

	def update(self, board, holeCard1, holeCard2):
		# h.update(board, ourCards) for h in self.hands
		