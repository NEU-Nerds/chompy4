
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
    sigmaUnchecked = {}
    maxDepthNodes = None

    pathNodes = {}
    def __init__(self, n):
        for s in range(n*n+1):
            self.sigmaUnchecked[s] = set([])
        self.maxDepthNodes = set([])
        self.rootNode = Node(n,n, self)

    def getSigmaUnchecked(self,sigma):
        return self.sigmaUnchecked[sigma]

    def getNode(self, path):
        return self.pathNodes[path]

    def __getitem__(self,index):
        return self.rootNode[index]

    def __repr__(self):
        return self.rootNode.__repr__()

    def __str__(self):
        return self.rootNode.__str__()

    def expandTree(self, initN, n):
        #expand and clear(should already be) sigmaUnchecked
        for s in range(n*n+1):
            self.sigmaUnchecked[s] = set([])

        #expand existing nodes to maxDepth
        for node in self.maxDepthNodes.copy():
            if node.even or len(node.path) < initN:
                continue
            node.expand(n-initN, self.sigmaUnchecked)

        #add new subTrees
        for x in range(initN + 1, n+1):
            newNode = Node(x, n-1, self, [x])
            self.rootNode.leaves.append(newNode)

class Node():
    path = None
    sigma = 0
    parentTree = None
    even = None
    leaves = []
    leaf = False


    def __init__(self, max, depth, parentTreeIn, inPath = []):
        self.parentTree = parentTreeIn
        if depth > 0:
            self.leaves = [Node(x,depth-1, parentTreeIn, inPath + [x]) for x in range(1,max+1)]
        else:
            self.parentTree.maxDepthNodes.add(self)
            self.leaf = True

        self.path = tuple(inPath)
        self.sigma = sum(inPath)

        self.parentTree.pathNodes[self.path] = self
        self.parentTree.sigmaUnchecked[self.sigma].add(self)

    def expand(self, depth, sigmaUnchecked):
        self.leaves = [Node(x,depth-1, self.parentTree, list(self.path) + [x]) for x in range(1,self.path[-1]+1)]
        self.leaf = False

    def setOdd(self):
        if self.even is None:
            self.even = False
            self.removeFromSigmaUnchecked()

    def removeFromSigmaUnchecked(self):
        self.parentTree.sigmaUnchecked[self.sigma].remove(self)

    def setEven(self):
        if self.even is None:
            self.even = True
            self.parentTree.sigmaUnchecked[self.sigma].remove(self)
            for leafD in self.leaves:
                leafD.delManual()
                del leafD
            self.leaves.clear()

        else:
            print("Resetting an node to be even when it's already been set as " + str(self.even))

    def __repr__(self):
        return str(self.path)

    def __str__(self):
        return str(self.path)

        if self.leaf:
            return str(self.even)
        else:
            return str([l.forStr() for l in self.leaves])

    def delManual(self):
        #fucking nuke this thing to the astral sea
        for leaf in self.leaves:
            try:
                leaf.delManual()
                del leaf
            except:
                # print("except1")
                pass
        try:
            del self.parentTree.pathNodes[self.path]

        except:
            # print("except2")
            pass
        try:
            del self.parentTree.sigmaUnchecked[self]
        except:
            # print("except3")
            pass
        if self.leaf:
            self.parentTree.maxDepthNodes.remove(self)

        del self.path
        del self.sigma
        self.leaves.clear()
        del self.parentTree


    def __delete__(self):
        #fucking nuke this thing to the astral sea
        for leaf in self.leaves:
            try:
                del leaf
            except:
                # print("except1")
                pass
        try:
            del self.parentTree.pathNodes[self.path]

        except:
            # print("except2")
            pass
        try:
            del self.parentTree.sigmaUnchecked[self]
        except:
            # print("except3")
            pass
        if self.leaf:
            self.parentTree.maxDepthNodes.remove(self)

        del self.path
        del self.sigma
        self.leaves.clear()
        del self.parentTree
        pass


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

        return self.leaves[index-1]
