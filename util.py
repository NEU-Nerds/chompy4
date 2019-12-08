import pickle
import json
from math import ceil

def newNodes(n):
	nodes = newNodesRec(n, [n])

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
		for i in range(0, part[-1] + 1):
			#add all the possiblities for the rest of the rows recursively
			nodes = nodes + newNodesRec(n, part + [i])
		return nodes

def expandDown(tree, evens, m, n):
	evens.append(set())
	rootsBySigma = []
	for i in range(m*n + 1):
		rootsBySigma.append(set())
	#fill rootsBySigma
	roots = tree.maxDepthNodes
	# print("roots: " + str(roots))
	for root in roots:
		#if the root is even
		if root.node.even:
			continue
		# print(f"root: {root}")
		# print(f"root.depth: {root.nodeDepth}")
		# print(f"root.path: {root.node.path}")
		for t in range(1, (root.node.path[-1] * root.node.nodeDepth) + 1):
			# print("t: " +str(t))
			rootsBySigma[root.node.sigma + t].add(root)
			# print(f"root: {root}")
	# print(f"rootsBySigma: {rootsBySigma}")
	# print("\n\n")
	for sigma in range(len(rootsBySigma)):
		# print(f"sigma: {sigma}")
		for root in rootsBySigma[sigma]:
			# print(f"root: {root}")
			# print(f"root leaves: {root.leaves}")
			#gen leaf of root at right sigma
			#add leaf to evens
			#get parents
			#gen parents
			# for parent in parents:
			# 	rootsBySigma[parent.sigma].remove(parent.rootNode)

			#OR
			# print("Adding leaf 2")
			leaf = root.addLeaf()
			# print("leaf1: " + str(leaf))
			# print(f"leaf: {leaf}")
			evenChild = False
			for even in evens[-1]:
				if isChild(even, leaf):
					evenChild = True
					break
			# print("leaf2: " + str(leaf))
			if evenChild:
				leaf.setOdd()
			else:
				leaf.setEven()
				evens[-1].add(leaf)


def fillTree(nodes, tree, n):

	for nodeObj in nodes.copy():

		# if type(nodeObj) != tuple and type(nodeObj) != list:
		node = list(nodeObj.node.path)
		# else:
		# 	node = list(nodeObj)

		#make sure square form
		for i in range(n-len(node)):
			node.append(0)

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
					setOdd(baseParent, tree)
				#else go through recursively all the below rows
				else:
					#the max the row can go to, set to n then adjusted if there is an above row
					max = n
					if j >= 0:
						max = baseParent[j+1]
					#get all the possiblites for the rows under the top row with the same value
					subParents = getParentsRec(baseParent[j+1:i+1] , max)
					for sub in subParents:
						#combining the sub possiblity with the rest of the board
						newParent = baseParent[:j+1] + sub + baseParent[i+1:]
						setOdd(newParent, tree)
			#sets the next row to work on to be the row above the top same row
			i = j

#returns whether possibleC is a child of possibleP
#O(2m) --> O(m) (m is length of path)
def isChild(possibleC, possibleP):
	pathC = list(possibleC.node.path) #.copy()
	pathP = possibleP
	if not isinstance(pathP, list):
		pathP = possibleP.node.path

	hasDelta = False;
	changedVal = 0;# if there hasDelta is true, the value of the new c

	if len(pathC) > len(pathP):
		return False

	while len(pathP) != len(pathC):
		pathC.append(0)

	for i in range(len(pathP)):
		if pathP[i] - pathC[i] < 0:
			return False
		elif pathP[i] != pathC[i]:
			if hasDelta and pathC[i] != changedVal:
				return False
			else:
				hasDelta = True
				changedVal = pathC[i]
	return True


"""
THIS WAS ACTUALLY CHILDREN
def transverseParents(nodes, tree):
	#set left branchMates
	#reccursively go up?

	#nodes.copy()?

	for node in nodes.copy():
		print(f"transversing {node}")
		#node is object

		#all left sibs
		for sib in node.branchNode.leaves[:node.path[-1]]:
			sib.setOdd()
		recNode = node.branchNode
		while len(recNode.path) >= 1: #is not None:
			#direct branchParents
			print(f"settingRecNode odd {recNode}")
			setNodeOdd(recNode, tree)
			#the rest
			for i in range(1, node.path[len(recNode.path)-1]):
				subRecNode = recNode[i]
				encounteredLeaf = False
				while len(subRecNode.path) < len(node.path):
					if subRecNode.leaf:
						encounteredLeaf = True
						break
					print("index: " + str(min(node.path[len(subRecNode.path)],i)) )
					print(f"path: {subRecNode.path}")
					subRecNode = subRecNode[min(node.path[len(subRecNode.path)],i)]
				if encounteredLeaf:
					print("continueing")
					continue
				print(f"settingSubRecNode odd {subRecNode}")
				setNodeOdd(subRecNode, tree)

			recNode = recNode.branchNode
"""

def setOdd(path, tree):
	if path[-1] == 0:
		path = cleanPath(path)

	try:
		tree.getNode(tuple(path)).setOdd()
	except:
		pass
		# print("exception for path: " + str(path))

def setNodeOdd(node, tree):
	try:
		tree.getNode(tuple(path)).setOdd()
	except:
		pass

def cleanPath(path):
	path = list(path)
	x = len(path) - 1
	while x >= 0 and path[x] == 0:
		# print("necessary?")
		del path[x]
		x -= 1
	return path

def cleanParents(parents):
	retParents = set([])
	#clean out any zereos
	for parent in parents:
		parent = list(parent)
		x = len(parent) - 1
		while x >= 0 and parent[x] == 0:
			# print("necessary?")
			del parent[x]
			x -= 1
		retParents.add(tuple(parent))

	return retParents

subParents = {}
def getParentsRec(subNode, max):
	#subnode is a list of rows with equal vals,
	#max is the maximum the rows can go to
	if (tuple(subNode), max) in subParents.keys():
		return subParents[(tuple(subNode), max)]

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

	subParents[(tuple(subNode), max)] = parents

	return parents


def getChoices(board):
	choices = [(i, j) for i in range(len(board)) for j in range(board[i])]
	choices = choices[1:]
	return choices

def bite(b, pos):
	if pos[1] == 0:
		return b[:pos[0]]

	board = b[:]

	for row in range(pos[0], len(board)):
		if board[row] > pos[1]:
			board[row] = pos[1];
		else:
			break

	# board = [r if r > pos[1] else r for r in b]
	return board

def getChildren(state):
	children = []
	#print("State: " +str(state))
	bites = getChoices(state)
	#print("Choices: " + str(bites))
	for b in bites:
		child = bite(state, b)
		#if util.getN(child) >= util.getM(child):
		children.append(child)
	return children

def storeJson(data, fileName):
	with open(fileName, "w") as file:
		jData = json.dumps(data)
		file.write(jData)
		# file.write(str(data))
		return 1

def load(fileName):
	with open (fileName, 'rb') as f:
		return pickle.load(f)

def store(data, fileName):
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)

def sigma(board):
    return sum(board)

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
