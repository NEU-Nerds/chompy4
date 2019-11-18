import util

def getParents(treeNode):
	#all the leaves of a node will be its parents, but we don't have to worry about these
	#b/c the only nodes being passed in here will be even, and they won't have any leaves

	#branchmates with # > than node are parents
	treeNode

"""
no need to return parents!!, just set them odd

1. all of the leaves of the node will be its parents (all the way to max depth)
2. all other parents of the node will be on the same depth as the node

Getting the other parents:
(add the greater # branchmates to parents first)
nodes should have a boolean 'traversed' if it has been visited before
have a list (stack) of unchecked nodes: 'unchecked'
have a list of parents: 'parents'
have a list of booleans: 'layerEquivalence' - whether the layer of the start node corresponding to the index
    has an equal value to the layer above it (row 0 is false)

add the start node to 'unchecked'
have 'commonAncestor': a pointer to the most recent common ancestor of startNode and currentNode
    defaults to startNode

while 'unchecked' is not empty:
    currNode = pop from 'unchecked'
    (this part is traversing down the graph)
    (currDepth is lenght of path)
    if currDepth is not maxDepth:
        nextDepth = currDepth + 1
        if layerEquivalence[nextDepth] is false:
            add the node from the next group of branchmates (at nextDepth layer) with the same value to 'unchecked'
            set that node's traversed to true
        else:
            for i starting from the val of startNode at layer nextDepth ending at
                the value of currNode at layer currDepth (inclusive):

                add the leaf of currNode with value i to 'unchecked'
                set the leaf's traversed to true
    else:
        (currDepth is maxDepth --> currNode is a parent of startNode)
        add currNode to 'parents'

        (now it's time to traverse up the tree)
        while commonAncestor is the max of its branchmates:
            commonAncestor = commonAncestor's treeParent
            if commonAncestor is null:
                (we have reaced the top of the tree and added all parents)
                break

        for i starting at 1 + value of commonAncestor, ending at max of its branchmates (inclusive):
            nextNode = commonAncestor's branchmate with value i
            if nextNode is not traversed:
                add nextNode to 'unchecked'
                set nextNode's traversed to true
many of the parents will be easy
the hard ones are when the node has consecutive rows that have the same value

the other nodes are just the "nth" cousins of that node that share the same last row
    you go up the tree to the lowest node that is not yet at max value (max value can be set dynamically)
    then increase the value by 1, and go down the tree taking the path that shares the same values as the first node
    keep going down until you reach the depth of the first node, then take the node that has the same value

"""
