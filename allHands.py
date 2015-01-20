from hand import *
# import itertools

class allHands():
	def __init__(self, listOfTuples):
		self.hands = [Hand(tup) for tup in listOfTuples]

	def update(self, board):
		for h in self.hands:
			h.update(board)

	def getId(self, tup):
		for h in self.hands:
			if h.cards == tup:
				return h.Id

# cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
# listOfTuples = [tup for tup in itertools.combinations(cardList,2)]
# #print listOfTuples
# ah = allHands(listOfTuples)
# ah.update(['ah','8h','8d','th'])
# ids = []
# for h in ah.hands:
# 	if h.Id not in ids:
# 		ids+=[h.Id]
# 		print h.cards, h.Id

# print len(set(ids))