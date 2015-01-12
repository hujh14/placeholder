
class pokerHandDist:
	def uniformDist(self,elts):
		p = 1.0/len(elts)
		return dict([(e,p) for e in elts])

	def __init__ (self, list_of_hands):
		
		self.pokerDist = self.uniformDist(list_of_hands)

	def removeExistingCards(self,rlist):
		p0 = 1.0/len(list_of_hands)

		for x in range(len(list_of_hands)):
			for y in range(len(rlist)):
				if rlist[y] == list_of_hands[x]:
					del list_of_hands[x]

		new_p = 1.0/(p0*len(list_of_hands))
		self.oppHandADist = dict([(h,p) for h in list_of_hands])
		self.oppHandBDist = dict([(h,p) for h in list_of_hands])	

				

		