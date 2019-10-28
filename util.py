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


def newRow(prevRow):
	if prevRow
	return [i for i in range(prevRow+1)]

def getParents(node):
