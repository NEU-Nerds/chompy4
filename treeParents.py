import util
from collections import defaultdict

def getParents(treeNode, tree):
	# print("treeNode: " + str(treeNode))
	leafVal = treeNode.path[-1]

	#all the leaves of a node will be its parents, but we don't have to worry about these
	#b/c the only nodes being passed in here will be even, and they won't have any leaves

	#branchmates with # > than node are parents
	bMates = treeNode.branchNode.leaves
	bNode = treeNode.branchNode
	# print("bMates: " + str(bMates))#IMPT: (2, ) does not seem to be in bMates when this is called!!!!!!
	#the tree's root node however does have (2, ), so root node and bNode are different

	# print("branchNode: " + str(bNode))
	# print("branchNode == rootNode: " + str(bNode == tree.rootNode))
	#confirms that bNode and rootNode are different


	#the numbers we are concerned with are tN.p[-1]+1 to the max of its branchmates,
	#but b/c of 0 indexing and non-inclusive upper-bound, we subtract 1 from i when it's being used
	# for i in range(leafVal, treeNode.path[-2]):
		# bMates[i].setOdd()
	for node in bMates:
		print("node: " + str(node.path))
		if node.path[-1] > leafVal:
			print("Node: " + str(node) + " is odd.")
			node.setOdd()

	traversed = defaultdict(lambda: False)

	stackUnchecked = [treeNode.branchNode] # we can't actually start with treeNode b/c it would get set odd

	traversed[str(treeNode.branchNode)] = True

	layerEquivalence = treeNode.layerEquivalence()
	treeCommonAncestor = treeNode.branchNode

	maxDepth = len(treeNode.path) - 1

	while (not len(stackUnchecked) == 0):
		currNode = stackUnchecked.pop()

		print("curr:\n" + str(currNode))

		currDepth = len(currNode.path)-1

		if not currDepth == maxDepth:
			if currNode.even:
				continue

			print("\nlen: " + str(len(layerEquivalence)))
			nextDepth = currDepth + 1
			print("next: " + str(nextDepth))
			print("max: " + str(maxDepth))
			if not layerEquivalence[nextDepth]:
				stackUnchecked.append(currNode.leaves[leafVal-1])
				traversed[str(currNode.leaves[leafVal-1])] = True
			else:
				print(currNode.even)
				print("leaves: " + str(currNode.leaves))
				print("maxDepth: " + str(maxDepth))
				for i in range(leafVal, currNode.path[-1] + 1):
					print("i: " + str(i))
					stackUnchecked.append(currNode.leaves[i-1])
					traversed[str(currNode.leaves[i-1])] = True
		else:
			if currNode != treeNode:
				print("Node: " + str(currNode) + " is odd.")
				currNode.setOdd()
			# else:
				# print("tree node!!")


			#traverse up the tree
			if len(treeCommonAncestor.path) < 2:
				treeCommonAncestor = None
				# commonAncestor is already at the top
			else:
				print("len path: " + str(len(treeCommonAncestor.path)))
				print("path: " + str(treeCommonAncestor.path))
				print("-1: " + str(treeCommonAncestor.path[-1]))
				print("-2: " + str(treeCommonAncestor.path[-2]))
				while treeCommonAncestor.path[-1] == treeCommonAncestor.path[-2]:
					treeCommonAncestor = treeCommonAncestor.branchNode
					if treeCommonAncestor == None:
						break # TODO: think about if all parents will be added by this point
					if len(treeCommonAncestor.path) < 2:
						# commonAncestor is already at the top
						treeCommonAncestor = None
						break

			if treeCommonAncestor == None:
				break

			bMatesAncestor = treeCommonAncestor.branchNode.leaves
			for nextNode in bMatesAncestor:
				if (not traversed[str(nextNode)]) and nextNode.path[-1] > treeCommonAncestor.path[-1]:
					stackUnchecked.append(nextNode)
					traversed[str(nextNode)] = True # TODO: this might not be necessary


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
	defaults to startNode's branchNode

while 'unchecked' is not empty:
	currNode = pop from 'unchecked'
	(this part is traversing down the graph)
	(currDepth is length of path)
	if currDepth is not maxDepth:
		nextDepth = currDepth + 1
		if layerEquivalence[nextDepth] is false:
			add the leaf of currNode with the save value to 'unchecked'
			(same thing as above) add the node from the next group of branchmates (at nextDepth layer) with the same value to 'unchecked'
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
