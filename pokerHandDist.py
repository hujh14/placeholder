import itertools

class pokerHandDist:
        def uniformDist(self,elts):
                p = 1.0/len(elts)
                return dict([(e,p) for e in elts])


        def __init__ (self, hlist):
                self.distribution = self.uniformDist(hlist)

        def removeExistingCards(self,rlist):
                rRemove = []
                for x in rlist:
                        rRemove += [(x,y) for y in cardList if x != y] + [(y,x) for y in cardList if x != y]

                #print self.prob
                #print self.prob*len(self.distribution.keys())

                for r in rRemove:
                        if r in self.distribution.keys():
                                del self.distribution[r]

                s = 0
                for key in self.distribution.keys():
                        s += self.distribution[key]
                #print s

                for key in self.distribution.keys():
                        self.distribution[key] = self.distribution[key]/s

                
                #print self.prob
                #print self.prob*len(self.distribution.keys())

                
# cardList = ['2s','3s','4s','5s','6s','7s','8s','9s','ts','js','qs','ks','as','2c','3c','4c','5c','6c','7c','8c','9c','tc','jc','qc','kc','ac','2h','3h','4h','5h','6h','7h','8h','9h','th','jh','qh','kh','ah','2d','3d','4d','5d','6d','7d','8d','9d','td','jd','qd','kd','ad']
# listOfTuples = [tup for tup in itertools.combinations(cardList,2)]

# # huh = [('ah','kc'),('4s','5s'),('6s','7s'),('8s','qs')]
# oppAProbDist = pokerHandDist(listOfTuples)
# print oppAProbDist.distribution

# oppAProbDist.removeExistingCards(['ah','5s'])
# print oppAProbDist.distribution

# s= 0
# for key in oppAProbDist.distribution:
#         s += oppAProbDist.distribution[key]
# print s

