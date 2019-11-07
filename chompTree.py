
"""
treeTrim changes:
default evens = None
when a node is marked as even, delete all its leaves
(need recursive __del__ function)
Keep a dict of unevaluated nodes
once marked as false, remove from sigmaNodes, pathNodes, del path, del sigma,
   make it "inert"

Parent representation in terms of tree?

"""
class Tree():
    rootNode = None
    sigmaNodes = {}
    sigmaEvens = {}
    pathNodes = {}
    def __init__(self, n):
        # print("init")
        for s in range(n*n+1):
            self.sigmaNodes[s] = set([])
            self.sigmaEvens[s] = set([])

        # print(f"sigmaEvens: {self.sigmaEvens}")
        self.rootNode = Node(n,n, self.sigmaNodes, self.sigmaEvens, self.pathNodes)

    def getSigmaEvens(self,sigma):
        # print("sigmaEvens: " + str(self.sigmaEvens))
        return self.sigmaEvens[sigma]

    def getNode(self, path):
        return self.pathNodes[path]
    def __getitem__(self,index):
        return self.rootNode[index]

    def __repr__(self):
        return self.rootNode.__repr__()

    def __str__(self):
        return self.rootNode.__str__()


class Node():
    parentTree = None
    path = None
    sigma = 0
    sigmaEvens = None
    even = True
    leaves = []
    leaf = False

    def __init__(self, max, depth, sigmaNodes, sigmaEvensIn, pathNodes, inPath = []):
        if depth > 0:
            self.leaves = [Node(x,depth-1, sigmaNodes, sigmaEvensIn, pathNodes, inPath + [x]) for x in range(1,max+1)]
        else:
            self.leaf = True
        self.path = tuple(inPath)
        pathNodes[self.path] = self
        self.sigma = sum(inPath)
        sigmaNodes[self.sigma].add(self)
        sigmaEvensIn[self.sigma].add(self)
        self.sigmaEvens = sigmaEvensIn

    def setOdd(self):
        if self.even:
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

    def __getitem__(self,index):
        #only becuase 0's were being used previously
        if index == 0:
            return self
        # print("index")
        return self.leaves[index-1]

if __name__ == "__main__":
    t = Tree(3)
    print(t.rootNode)
    print(t.sigmaNodes)
