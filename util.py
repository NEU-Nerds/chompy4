def newNodes(n):
	N = []
	r1 = newRow(n)
	for r in r1:
		r2 = newRow(r)
	return N

def newBoardRecurse(b, n, boards):
	if len(b) == n:
		return (b, n, boards)
	r1 = newRow(b[-1])
	for r in r1:

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
			n2 = node[:]
			for k in range(k):
				n2[r+j] = n2[r+j] + k
			parents.append(n2)
	#if any consecutive rows are the same, both of them can be increased by the same amount
	return parents


def getExpandParents(node, n):
