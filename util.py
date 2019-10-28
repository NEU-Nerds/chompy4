def newNodes(n):
	#for x(-1) in range(n)
	#for x(-2) in range(x(-1)+1)
	nodes = []
	for i in range(0,n+1):
		nodes = nodes + newNodesRec(n, [i])
	nodes = nodes + newNodesRecReversed(n-1, [n])

	retNodes = []
	for node in nodes:
		node = list(node)
		x = len(node) - 1
		while x >= 0 and node[x] == 0:
			del node[x]
			x -= 1
		if len(node) == 0:
			continue
		retNodes.append(tuple(node))

	return retNodes

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
		for i in range(0, part[-1]+1):
			nodes = nodes + newNodesRec(n, part + [i])
		return nodes

# def getParents(node, n):
# 	parents = []
# 	node = list(node)
# 	for r in range(1, len(node)):
# 		max = n
# 		if r != 0:
# 			max = node[r-1]
# 		numConsecutive = 0
# 		for i in range(len(node)):
# 			if not r == len(node)-i:
# 				if node[r] == node[r+i]:
# 					numConsecutive = i
# 			else:
# 				break
# 		for i in range(node[r] - max + 1):
# 			#add the parents only increasing 1 row
# 			n1 = node[:]
# 			n1[r] = n1[r] + i
# 			parents.append(n1)
# 		for j in range(numConsecutive + 1):
# 			#j is the number rows being added to
# 			n2 = node[:]
# 			for k in range(max):
# 				#k is the number to be added
# 				n2[r+j] = n2[r+j] + k
# 			parents.append(n2)
# 	#if any consecutive rows are the same, both of them can be increased by the same amount
# 	return parents

def getParents(node, n):
	node = list(node)
	for i in range(n-len(node)):
		node.append(0)
	# print("Node: " + str(node))
	parents = []
	i = len(node) - 1
	while i >= 0:
		# print("i: " + str(i))
		#j is index of first row with a different value
		j = i-1
		while j >= 0 and node[j] == node[i]:
			j -= 1
		# print("j: " + str(j))

		#maxDiff is difference between next non same row and the i row
		maxDiff = 0
		#if j < 0 then same val as the top row so use n for maxDiff
		if j < 0:
			maxDiff = n - node[i]
		else:
			maxDiff = node[j] - node[i]

		# print("maxDiff: " + str(maxDiff))

		#go through each diff
		for d in range(1, maxDiff+1):
			# print("d: " + str(d))

			#make a coppy of the node
			baseParent = node[:]
			#set the top of the same rows equal to its val + diff
			baseParent[j+1] += d
			# print("baseParent: " + str(baseParent))

			#if i the only row with that val (baseparent is the only parent for this d)
			if j == i - 1:
				# print("j == i-1")
				parents.append(baseParent[:])
			#else go through recursively all the below rows
			else:
				# print("baseParent[j+2:i+1]: "  +str(baseParent[j+2:i+1]))
				max = n
				if j >= 0:
					max = baseParent[j+1]
				subParents = getParentsRec(baseParent[j+2:i+1] , max)
				# print("subParents: " + str(subParents))
				for sub in subParents:
					newParent = baseParent[:j+2] + sub + baseParent[i+1:]
					# print("newParent: " + str(newParent))
					parents.append(newParent)

			# for k in range(j+1, i+1):
			# 	parent = node[:]
			# 	print("k: " + str(k))
			# 	for l in range(j+1, k+1):
			# 		print("l: " + str(l))
			# 		parent[l] += d
			#
			#
			# 	print("parent: " + str(parent))
			# 	parents.append(tuple(parent))
			# print("final parent: " + str(parent))

		i  = j
	retParents = []
	for parent in parents:
		x = len(parent) - 1
		while x >= 0 and parent[x] == 0:
			del parent[x]
			x -= 1
		retParents.append(tuple(parent))

	return retParents




	#then do up till n for node[0]


def getParentsRec(subNode, max):
	#subnode is a list of rows with equal vals,
	#max is the maximum the rows can go to
	# print("\nsubNode: " + str(subNode) + "\tmax: " + str(max))
	subNode = list(subNode)
	parents = []

	for i in range(subNode[0], max+1):
		# print("i: " + str(i))
		baseParent = subNode[:]
		baseParent[0] = i
		if len(subNode) == 1:
			# print("len == 1")
			parents.append(baseParent)

		else:
			newSecondParents = getParentsRec(subNode[1:], i)
			for secondParent in newSecondParents:
				parents.append([i] + secondParent)
	return parents


def getExpandParents(even, n):
	parents = getParents(even, n)
	return parents
	#similar to the recursive generation of states. Ty, do this later

"""
def mirror(board):
	# [ for i in range(len(board))]
	mirrored = [0] * board[0] #initialize the mirrored rectangular board
	for i in range(board[0]):
		for j in range(len(board)):
			if board[j] > i:
				mirrored[i] += 1
	return mirrored
"""
