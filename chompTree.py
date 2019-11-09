
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

    # sigmaNodes = {}
    # sigmaEvens = {}
    sigmaUnchecked = {}
    maxDepthNodes = None

    pathNodes = {}
    def __init__(self, n):
        # print("init")
        for s in range(n*n+1):
            # self.sigmaNodes[s] = set([])
            # self.sigmaEvens[s] = set([])
            self.sigmaUnchecked[s] = set([])
        self.maxDepthNodes = set([])
        # print(f"sigmaEvens: {self.sigmaEvens}")

        self.rootNode = Node(n,n, self)

    # def getSigmaEvens(self,sigma):
    #     # print("sigmaEvens: " + str(self.sigmaEvens))
    #     return self.sigmaEvens[sigma]

    def getSigmaUnchecked(self,sigma):
        # print("sigmaEvens: " + str(self.sigmaEvens))
        return self.sigmaUnchecked[sigma]

    def getNode(self, path):
        # print("pathNodes: " +str(self.pathNodes))
        # print(f"path: {path}")
        # print(type(path))
        return self.pathNodes[path]

    def __getitem__(self,index):
        return self.rootNode[index]

    def __repr__(self):
        return self.rootNode.__repr__()

    def __str__(self):
        return self.rootNode.__str__()

    def expandTree(self, initN, n):
        # print("initN: " +str(initN))
        # print(f"n={n}")
        #expand and clear(should already be) sigmaUnchecked
        # print("n: " + str(n))
        for s in range(n*n+1):
            # self.sigmaNodes[s] = set([])
            # self.sigmaEvens[s] = set([])
            self.sigmaUnchecked[s] = set([])
        # print("keys: " + str(self.sigmaUnchecked.keys()))

        #expand existing nodes to maxDepth
        # print("maxDepthNodes: " + str(self.maxDepthNodes))
        for node in self.maxDepthNodes.copy():
            if node.even or len(node.path) < initN:
                continue
            # print("Expanding node: "+str(node) )
            # oldMaxNodes.add(node)
            # print(f"Expanding node: {node} in n: {n}")
            node.expand(n-initN, self.sigmaUnchecked)

        #add new subTrees
        # print()
        for x in range(initN + 1, n+1):
            # print(f"x={x}")
            newNode = Node(x, n-1, self, [x])
            # print(f"newNode: {newNode}")
            self.rootNode.leaves.append(newNode)

class Node():
    path = None
    sigma = 0
    # pathNodes = None
    # # sigmaEvens = None
    # sigmaUnchecked = None
    # maxDepthNodes = None
    parentTree = None
    even = None
    leaves = []
    leaf = False


    def __init__(self, max, depth, parentTreeIn, inPath = []):
        # print("initKeys: " + str(sigmaUnchecked.keys()))
        self.parentTree = parentTreeIn
        if depth > 0:
            self.leaves = [Node(x,depth-1, parentTreeIn, inPath + [x]) for x in range(1,max+1)]
        else:
            self.parentTree.maxDepthNodes.add(self)
            self.leaf = True
        # print("inPath: " +str(inPath))
        self.path = tuple(inPath)
        self.sigma = sum(inPath)

        self.parentTree.pathNodes[self.path] = self
        # print("pathNodesInNodeAfter: " + str(self.parentTree.pathNodes))
        # sigmaNodes[self.sigma].add(self)
        self.parentTree.sigmaUnchecked[self.sigma].add(self)


        # self.sigmaUnchecked = sigmaUnchecked
        # self.pathNodes = pathNodes
        # self.maxDepthNodes = maxDepthNodes
    def expand(self, depth, sigmaUnchecked):
        # print("expandKeys: " + str(sigmaUnchecked.keys()))
        self.leaves = [Node(x,depth-1, self.parentTree, list(self.path) + [x]) for x in range(1,self.path[-1]+1)]

        self.leaf = False

    def setOdd(self):
        # print(f"setOddInternal on {self.path} sigma: {self.sigma}")
        if self.even is None:
            # print("Even was None")
            self.even = False
            # self.parentTree.sigmaUnchecked[self.sigma].remove(self)
            self.removeFromSigmaUnchecked()
            # print("If its in unchecked after: " + str(self in self.parentTree.sigmaUnchecked[self.sigma]))
    def removeFromSigmaUnchecked(self):
        self.parentTree.sigmaUnchecked[self.sigma].remove(self)
    def setEven(self):
        if self.even is None:
            self.even = True
            self.parentTree.sigmaUnchecked[self.sigma].remove(self)
            # self.parentTree.maxDepthNodes.pop()
            for leafD in self.leaves:
                # print(leafD.path)
                # print(f"del leaf {leafD}")
                leafD.delManual()
                del leafD
            self.leaves.clear()
            # del self.leaves
            # for leaf in self.leaves:

        else:
            print("Resetting an node to be even when it's already been set as " + str(self.even))
        #sigmaEvens?

        # return self
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
        # del self.sigmaUnchecked
        # del self.even
        self.leaves.clear()
        del self.parentTree
        # del self.leaf


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
        # del self.sigmaUnchecked
        # del self.even
        self.leaves.clear()
        del self.parentTree
        # del self.leaf
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
        # print("index")
        return self.leaves[index-1]

# if __name__ == "__main__":
#     t = Tree(3)
#     print(t.rootNode)
#     print(t.sigmaNodes)
