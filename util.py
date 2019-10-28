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

<<<<<<< HEAD
def getParents(node):
=======
def getParents(node, n):
	pass

def getExpandParents(even, n):
	pass
>>>>>>> a490f3fda68bb84c9bb65551086c0f7e17d3f1ce
