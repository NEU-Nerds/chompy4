
class Tree():
    rootNode = None
    sigmaNodes = {}
    sigmaEvens = {}
    def __init__(self, n):
        print("init")
        for s in range(n*n+1):
            self.sigmaNodes[s] = set([])
            self.sigmaEvens[s] = set([])
        print(f"sigmaEvens: {self.sigmaEvens}")
        self.rootNode = Node(n,n, self.sigmaNodes, self.sigmaEvens)
    def getSigmaEvens(self,sigma):
        return self.sigmaEvens[sigma]



class Node():
    parentTree = None
    path = None
    sigma = 0
    sigmaEvens = None
    even = True
    leaves = []
    leaf = False

    def __init__(self, max, depth, sigmaNodes, sigmaEvensIn, inPath = []):
        if depth > 0:
            self.leaves = [Node(x,depth-1, sigmaNodes, sigmaEvensIn, inPath + [x]) for x in range(max+1)]
        else:
            self.leaf = True
        self.path = inPath
        self.sigma = sum(inPath)
        sigmaNodes[self.sigma].add(self)
        print(f"sigEvIn: {sigmaEvensIn}")
        print(f"{self.sigma}")
        print(sigmaEvensIn[self.sigma])
        sigmaEvensIn[self.sigma].add(self)
        self.sigmaEvens = sigmaEvensIn

    def setOdd(self):
        self.even = False
        self.sigmaEvens[self.sigma].remove(self)


        # return self
    def __repr__(self):
        return str(self.path)

    def __str__(self):
        if self.leaf:
            return str(self.even)
        else:
            return str([l.forStr() for l in self.leaves])

    def forStr(self):
        if self.leaf:
            return self.even
        else:
            return [l.forStr() for l in self.leaves]

    def toTuple(self):
        return tuple(self.path)



if __name__ == "__main__":
    t = Tree(3)
    print(t.rootNode)
    print(t.sigmaNodes)
