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
	parents = []
	for r in range(1, len(node)):
		max = n
		if r != 0:
			max = node[r-1]
		numConsecutive = 0
		for i in range(len(node)):
			if not r == len(node)-i:
				if node[r] == node[r+i]:
					numConsecutive = i
			else:
				break
		for i in range(node[r] - max + 1):
			#add the parents only increasing 1 row
			n1 = node[:]
			n1[r] = n1[r] + i
			parents.append(n1)
		for j in range(numConsecutive + 1):
			#j is the number rows being added to
			n2 = node[:]
			for k in range(max):
				#k is the number to be added
				n2[r+j] = n2[r+j] + k
			parents.append(n2)
	#if any consecutive rows are the same, both of them can be increased by the same amount
	return parents


def getExpandParents(even, n):
	parents = getParents(even, n)
	#similar to the recursive generation of states. Ty, do this later
