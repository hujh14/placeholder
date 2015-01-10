class pokerHandDist:
	def __init__ ():
		#list of possible cards
		card_list_A = ['2s','3s','4s','5s','6s','7s','8s','9s','Ts','Js','Qs','Ks','2c','3c','4c','5c','6c','7c','8c','9c','Tc','Jc','Qc','Kc','2h','3h','4h','5h','6h','7h','8h','9h','Th','Jh','Qh','Kh','2d','3d','4d','5d','6d','7d','8d','9d','Td','Jd','Qd','Kd']
		card_list_B = ['2s','3s','4s','5s','6s','7s','8s','9s','Ts','Js','Qs','Ks','2c','3c','4c','5c','6c','7c','8c','9c','Tc','Jc','Qc','Kc','2h','3h','4h','5h','6h','7h','8h','9h','Th','Jh','Qh','Kh','2d','3d','4d','5d','6d','7d','8d','9d','Td','Jd','Qd','Kd']

		##initialize list of possible hands

		list_of_hands = []

		##create tuples for all possible pairs of cards
		cpair = (0,0)
		for i in range(len(card_list_A)):
	    	for j in range(len(card_list_B)):
	            cpair = (card_list_A[i],card_list_B[j])
	            list_of_hands.append(cpair)

		return list_of_hands

		##create dictionary
		prob_of_hands = {}
		for i in range(len(list_of_hands)):
		    prob_of_hands.update({list_of_hands[i]})
		    
		
		self.oppHandADist = 
		self.oppHandBDist = 

	def removeHoleCards(hc1,hc2):

		