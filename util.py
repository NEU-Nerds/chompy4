def newNodes(n):
	#for x(-1) in range(n)
	#for x(-2) in range(x(-1)+1)

	nodes = []
	#calling the rec function with all the first rows
	for i in range(0,n+1):
		nodes = nodes + newNodesRec(n, [i])

	#this was here but I forgot why and commenting out didn't seem to change anything?
	# nodes = nodes + newNodesRecReversed(n-1, [n])

	retNodes = []
	#just cleaning up any 0's or empty boards, and converting to tuple
	for node in nodes:
		node = list(node)
		x = len(node) - 1
		#removing 0 entries
		while x >= 0 and node[x] == 0:
			del node[x]
			x -= 1
		#making sure not empty
		if len(node) == 0:
			continue
		retNodes.append(tuple(node))

	return retNodes

def newNodesRec(n, part):
	#break case, means part has grown to be n long (square board shape)
	if len(part) == n:
		return [tuple(part)]
	else:
		nodes = []
		#go through all the possiblities for this row
		for i in range(part[0], n+1):
			#add all the possiblities for the rest of the rows recursively
			nodes = nodes + newNodesRec(n, [i] + part)
		return nodes

#I thought this was necessary, now I forget why...
"""
def newNodesRecReversed(n, part):
	if len(part) == n:
		return [tuple(part)]
	else:
		nodes = []
		for i in range(0, part[-1]+1):
			nodes = nodes + newNodesRec(n, part + [i])
		return nodes
"""
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
	#make sure square form
	for i in range(n-len(node)):
		node.append(0)

	parents = []

	#i is the current row we are lookign at, from bottom to top
	i = len(node) - 1
	while i >= 0:
		#j is index of first row with a different value
		j = i-1
		while j >= 0 and node[j] == node[i]:
			j -= 1

		#maxDiff is difference between next non same row and the i row
		maxDiff = 0
		#if j < 0 then same val as the top row so use n for maxDiff
		if j < 0:
			maxDiff = n - node[i]
		else:
			maxDiff = node[j] - node[i]

		#go through each diff
		for d in range(1, maxDiff+1):
			#make a coppy of the node
			baseParent = node[:]
			#set the top of the same rows equal to its val + diff
			baseParent[j+1] += d

			#if i the only row with that val then baseparent is the only parent for this d
			#(there are no subsequent rows to work through)
			if j == i - 1:
				parents.append(baseParent[:])
			#else go through recursively all the below rows
			else:
				#the max the row can go to, set to n then adjusted if there is an above row
				max = n
				if j >= 0:
					max = baseParent[j+1]
				#get all the possiblites for the rows under the top row with the same value
				subParents = getParentsRec(baseParent[j+2:i+1] , max)
				for sub in subParents:
					#combining the sub possiblity with the rest of the board
					newParent = baseParent[:j+2] + sub + baseParent[i+1:]
					parents.append(newParent)
		#sets the next row to work on to be the row above the top same row
		i = j


	retParents = []
	#clean out any zereos
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

	subNode = list(subNode)
	parents = []

	#all the options for the first row
	for i in range(subNode[0], max+1):
		#coppy the subNode
		baseParent = subNode[:]
		#set the first row
		baseParent[0] = i
		#if that's the only row then that's that
		if len(subNode) == 1:
			parents.append(baseParent)
		#else add the modified first row to all the possible permutations of the other rows
		else:
			newSecondParents = getParentsRec(subNode[1:], i)
			for secondParent in newSecondParents:
				parents.append([i] + secondParent)

	return parents

#TODO, right now just returning all parents
def getExpandParents(even, n):
	parents = getParents(even, n)
	return parents
	#similar to the recursive generation of states.

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
