import itertools

class pokerHandDist:
        def uniformDist(self,elts):
                p = 1.0/len(elts)
                return dict([(e,p) for e in elts])

        def __init__ (self, hlist):
                self.distribution = self.uniformDist(hlist)

        def removeExistingCards(self,rlist):
                p0 = 1.0/len(self.distribution)

                for x in range(len(rlist)):
                        if rlist[x] in self.distribution:
                                del self.distribution[rlist[x]]

                new_p = 1.0/(len(self.distribution))
                return dict([(h,new_p) for h in self.distribution])