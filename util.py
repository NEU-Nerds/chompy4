def newNodes(n):
	#for x(-1) in range(n)
	#for x(-2) in range(x(-1)+1)
	nodes = []
	for i in range(1,n+1):
		nodes = nodes + newNodesRec(n, [i])
	nodes = nodes + newNodesRecReversed(n-1, [n])
	return nodes

def newNodesRec(n, part):
	if len(part) == n:
		return [tuple(part)]
	else:
		nodes = []
		for i in range(part[0], n+1):
			nodes = nodes + newNodesRec(n, [i] + part)
		return nodes

def newNodesRecReversed(n, part):
	if len(part) == n:
		return [tuple(part)]
	else:
		nodes = []
		for i in range(1, part[-1]+1):
			nodes = nodes + newNodesRec(n, part + [i])
		return nodes


def getParents(node, n):
	pass

def getExpandParents(even, n):
	pass
