import itertools

class pokerHandDist:
	def uniformDist(elts):
		p = 1.0/len(elts)
		return dict([(e,p) for e in elts])

	def __init__ ():
		#list of possible cards
		card_list = ['2s','3s','4s','5s','6s','7s','8s','9s','Ts','Js','Qs','Ks','As','2c','3c','4c','5c','6c','7c','8c','9c','Tc','Jc','Qc','Kc','Ac','2h','3h','4h','5h','6h','7h','8h','9h','Th','Jh','Qh','Kh','Ah','2d','3d','4d','5d','6d','7d','8d','9d','Td','Jd','Qd','Kd','Ad']

		##create tuples for all possible pairs of cards

		# cpair = (0,0)
		# for i in range(len(card_list)):
		# 	new_card_list = card_list.pop(i)
		# 	for j in range(len(new_card_list)):
		# 		cpair = (card_list[i],new_card_list[j])
		# 		card_list = new_card_list
		# 		list_of_hands.append(cpair)

		# return list_of_hands
		
		hi = itertools.combinations(card_list,2)
		list_of_hands = [tup for tup in hi]

		##create uniform distributions for opponents A and B
		self.oppHandADist = uniformDist(list_of_hands)
		self.oppHandBDist = uniformDIst(list_of_hands)

	def removeExistingCards(rlist):
		for x in range(len(list_of_hands)):
			for y in range(len(rlist)):
				if rlist[y] == list_of_hands[x]:
					del list_of_hands[x]

		self.oppHandADist = uniformDist(list_of_hands)
		self.oppHandBDist = uniformDist(list_of_hands)
		

		