import util
"""
#O(evens*deltaW*depth)
def sideExpansion (evens, uncheckedNodes):
	endNodes = []

	for unknown in uncheckedNodes:
		evenChild = False
		for even in evens:
			#if even is a child of unknown
			if util.isChild(even, unknown):
				evenChild = True
				break
		if not evenChild:
			unknown.setEven()
			evens.add(unknown)
		else:
			unknown.setOdd()
			endNodes.append(unknown)

	return endNodes

"""
"""
marking the new nodes of the added side bar as odd/even by depth
given: evens@depth, newNodes(unchecked nodes, in the side bar), maybe depth
for mvp, check between each even and each unchecked if even is child of unchecked
"""

# evens at depth, new nodes at depth, previous width, change in width
def sideExpansion (evens, uncheckedNodes, pN, dN):
	# print("\n\nIn parents")
	# print(f"evens: {evens}")
	evenParents = []
	for even in evens:
		evenParents += getParents(pN, dN, even)
	# print(f"\nPARENTS OF EVENS:\t\t{evenParents}")
	evenParents = set(evenParents)

	endNodes = []
	for unknown in uncheckedNodes:
		# print(f"parents of evens: {evenParents}")
		if tuple(unknown.path) in evenParents:
			unknown.setOdd()
			endNodes.append(unknown)
		else:
			unknown.setEven()
			evens.add(unknown)
			evenParents = evenParents.union(getParents(pN, dN, unknown))

	# print("DONE WITH PARENTS\n\n")
	return endNodes



# returns the parents of a node at depth (don't add the tails)
# pass in previous width, change in width, and the node
def getParents (pN, dN, evenNode):
	parents = []

	# maybe use layerEquivalence to do this?
	layerEq = evenNode.layerEquivalence()

	lastAdded = []

	for d in range(len(evenNode.path)):
		start = max(pN + 1, evenNode.path[0] + 1)
		stop = pN + dN + 1
		if d != 0:
			start = max(evenNode.path[d] + 1, pN + 1)
			stop = max(evenNode.path[d-1] + 1, start + 1)
		if layerEq[d]:
			toAdd = []
			for parent in lastAdded:
				for i in range(parent[d], parent[d-1] + 1):
					p = list(parent[:])
					p[d] = i
					toAdd.append(tuple(p))
			lastAdded.extend(toAdd)
		else:
			parents.extend(lastAdded)
			lastAdded = []
		for i in range(start, stop):
			p = list(evenNode.path[:])
			p[d] = i
			# parents[-1][d] = i
			lastAdded.append(tuple(p))
	parents.extend(lastAdded)
	# for d in range(1, len(evenNode.path)):

	# print(f"pN: {pN}\ndN: {dN}")
	# print(f"parents of {evenNode}: {parents}")
	return tuple(parents)
