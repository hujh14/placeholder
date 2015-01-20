import itertools

class pokerHandDist:
        def uniformDist(self,elts):
                p = 1.0/len(elts)
                return dict([(e,p) for e in elts])


        def __init__ (self, hlist):
                self.distribution = self.uniformDist(hlist)

        def removeExistingCards(self,rlist):
                for x in range(len(rlist)):
                        
                        if (rlist[x],) in self.distribution:
                                del self.distribution[rlist[x]]
                                #print 'hi'

                new_p = 1.0/(len(self.distribution))
                newDict = dict([(h,new_p) for h in self.distribution])
                #print newDict
                self.distribution = newDict

# cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
# listOfTuples = [tup for tup in itertools.combinations(cardList,2)]
# test = pokerHandDist(listOfTuples)
# print test.removeExistingCards(['ah'])