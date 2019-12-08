import util

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
marking the new nodes of the added side bar as odd/even by depth
given: evens@depth, newNodes(unchecked nodes, in the side bar), maybe depth
for mvp, check between each even and each unchecked if even is child of unchecked

pass in previousN, deltaN

"""
