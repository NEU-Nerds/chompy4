import util

#O(evens*deltaW*depth)
def sideExpansion (evens, uncheckedNodes):
	for even in evens:
		for unknown in uncheckedNodes:
			#if even is a child of unknown
			if util.isChild(even, unknown):
				unknown.setOdd()



"""
marking the new nodes of the added side bar as odd/even by depth

given: evens@depth, newNodes(unchecked nodes, in the side bar), maybe depth

for mvp, check between each even and each unchecked if even is child of unchecked
"""
