from hand import *

class allHands():
	def __init__(self, listOfTuples):
		self.hands = [Hand(tup) for tup in listOfTuples]

	def update(self, board):
		h.update(board) for h in self.hands
