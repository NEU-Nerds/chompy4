import pickle
import json
from math import ceil

def newNodes(n):
	#for x(-1) in range(n)
	#for x(-2) in range(x(-1)+1)

	nodes = newNodesRec(n, [n])

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
		for i in range(0, part[-1] + 1):
			#add all the possiblities for the rest of the rows recursively
			nodes = nodes + newNodesRec(n, part + [i])
		return nodes


# def initTree(depth, max, sigmaDict, path=[]):
# 	if depth == 1:
# 		ret = [True]*(max+1)
# 		for x in range(max+1):
# 			sigmaDict[sum(path)+x].append((ret,x,path+[x]))
# 		return ret
# 	tree = []
# 	for i in range(max+1):
# 		tree.append(initTree(depth-1, i, sigmaDict, path+[i]))
# 	return tree



def fillTree(nodes, tree, n):
	# print("fillTree Nodes: "  +str(nodes))
	for nodeObj in nodes.copy():

		if type(nodeObj) != tuple and type(nodeObj) != list:
			 node = list(nodeObj.path)
		else:
			node = list(nodeObj)
		print(f"filling from {node}")
		#make sure square form
		for i in range(n-len(node)):
			node.append(0)

		# print(f"\nnode: {node}")
		#i is the current row we are lookign at, from bottom to top
		i = len(node) - 1
		while i >= 0:
			#j is index of first row with a different value
			j = i-1
			while j >= 0 and node[j] == node[i]:
				j -= 1
			# print(f"i: {i}\tj: {j}")
			#maxDiff is difference between next non same row and the i row
			maxDiff = 0
			#if j < 0 then same val as the top row so use n for maxDiff
			if j < 0:
				maxDiff = n - node[i]
			else:
				maxDiff = node[j] - node[i]

			#go through each diff
			for d in range(1, maxDiff+1):
				# print(f"d: {d}")
				#make a coppy of the node
				baseParent = node[:]
				#set the top of the same rows equal to its val + diff
				baseParent[j+1] += d

				#if i the only row with that val then baseparent is the only parent for this d
				#(there are no subsequent rows to work through)
				if j == i - 1:
					# print("parent: " + str(baseParent))
					# print("addingB: " +str(baseParent))
					setOdd(baseParent, tree)
				#else go through recursively all the below rows
				else:
					#the max the row can go to, set to n then adjusted if there is an above row
					max = n
					if j >= 0:
						max = baseParent[j+1]
					# print(f"max: {max}")
					#get all the possiblites for the rows under the top row with the same value
					subParents = getParentsRec(baseParent[j+1:i+1] , max)
					for sub in subParents:
						#combining the sub possiblity with the rest of the board
						newParent = baseParent[:j+1] + sub + baseParent[i+1:]
						# print("addingN: " +str(newParent))
						# print("")
						setOdd(newParent, tree)
			#sets the next row to work on to be the row above the top same row
			i = j


def setOdd(path, tree):
	if path[-1] == 0:
		path = cleanPath(path)
	# print(f"setOdd cleaned Path: {path}" )
	try:
		tree.getNode(tuple(path)).setOdd()
	except:
		# print("exception for path: " + str(path))
		pass
# def getSigmaEvens(tree, sigma, n, path=[]):
# 	if len(path) == n-1:
# 		if not (sigma >= len(tree)) and tree[sigma]:
# 			return [path + [sigma]]
# 		return []
#
# 	ret = []
# 	for i in range(min(len(tree), sigma+1)):
# 		ret.extend(getSigmaEvens(tree[i], sigma-i, n, path + [i]))
# 	return cleanParents(ret)

# def getSigmaPaths(sigma, n):
# 	paths = []
# 	for x in range(ceil(sigma/n), min(sigma,n)+1):
# 		paths.append([x]+getSigmaPaths(sigma-x))
# 	pass


# def fillTreeNext(nodes, tree, n):
# 	paths = getPaths(nodes, n)
# 	# print(f"paths: {paths}")
# 	for path in paths:
# 		# print(f"path: {path}")
# 		cBranch = tree
# 		for x in path[0]:
# 			cBranch = cBranch[x]
# 		# print(f"cBranch: {cBranch}")
# 		# cB2 = cBranch
# 		branches = [cBranch]
# 		for xRange in path[1]:
# 			# for branch in branches:
# 			# 	for x in range(xRange[0], min(len(branches),xRange[1]+1)):
#
#
# 			branches = [branch[x] for branch in branches for x in range(xRange[0], min(len(branches),xRange[1]+1)) ]
# 		print(f"branches: {branches}")
# 		for branch in branches:
# 			for x in path[2]:
# 				branch = branch[x]
# 			print(f"addToTree {branch}, {tree}")
# 			addToTree(branch, tree)

# def getPaths(nodes, n):
# 	paths = []
# 	for node in nodes:
# 		# print("node: " + str(node))
# 		node = list(node)
# 		#make sure square form
# 		for i in range(n-len(node)):
# 			node.append(0)
#
#
# 		#i is the current row we are lookign at, from bottom to top
# 		i = len(node) - 1
# 		while i >= 0:
# 			# print("i: " + str(i))
# 			#j is index of first row with a different value
# 			j = i-1
# 			while j >= 0 and node[j] == node[i]:
# 				j -= 1
# 			# print("j: " + str(j))
#
# 			#maxDiff is difference between next non same row and the i row
# 			max = n
# 			#if j < 0 then same val as the top row so use n for maxDiff
# 			if j >= 0:
# 				max = node[j]# - node[i]
# 			# print("max: " + str(max))
#
# 			min = 0
# 			if i+1 < len(node):
# 				min = node[i+1]
#
# 			path1 = []
# 			for x in range(j+1):
# 				path1.append(node[x])
#
#
#
#
# 			path2 = []
# 			#for all eqal rows
# 			for x in range(j+1,i+1):
# 				path2.append((min,max))
#
#
# 			path3 = []
# 			for x in range(i+1, len(node)):
# 				path3.append(node[x])
#
# 			paths.append((path1,path2,path3))
# 			i = j
# 	return paths
#
#
# def getParentsBatch(nodes, n):
# 	parents = set([])
# 	for node in nodes:
# 		node = list(node)
# 		#make sure square form
# 		for i in range(n-len(node)):
# 			node.append(0)
#
#
# 		#i is the current row we are lookign at, from bottom to top
# 		i = len(node) - 1
# 		while i >= 0:
# 			#j is index of first row with a different value
# 			j = i-1
# 			while j >= 0 and node[j] == node[i]:
# 				j -= 1
#
# 			#maxDiff is difference between next non same row and the i row
# 			maxDiff = 0
# 			#if j < 0 then same val as the top row so use n for maxDiff
# 			if j < 0:
# 				maxDiff = n - node[i]
# 			else:
# 				maxDiff = node[j] - node[i]
#
# 			#go through each diff
# 			for d in range(1, maxDiff+1):
# 				#make a coppy of the node
# 				baseParent = node[:]
# 				#set the top of the same rows equal to its val + diff
# 				baseParent[j+1] += d
#
# 				#if i the only row with that val then baseparent is the only parent for this d
# 				#(there are no subsequent rows to work through)
# 				if j == i - 1:
# 					parents.add(tuple(baseParent[:]))
# 				#else go through recursively all the below rows
# 				else:
# 					#the max the row can go to, set to n then adjusted if there is an above row
# 					max = n
# 					if j >= 0:
# 						max = baseParent[j+1]
# 					#get all the possiblites for the rows under the top row with the same value
# 					subParents = getParentsRec(baseParent[j+2:i+1] , max)
# 					for sub in subParents:
# 						#combining the sub possiblity with the rest of the board
# 						newParent = baseParent[:j+2] + sub + baseParent[i+1:]
# 						parents.add(tuple(newParent))
# 			#sets the next row to work on to be the row above the top same row
# 			i = j
#
#
#
# 	return cleanParents(parents)

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
#
# def getParents(node, n):
# 	node = list(node)
# 	#make sure square form
# 	for i in range(n-len(node)):
# 		node.append(0)
#
# 	parents = []
#
# 	#i is the current row we are lookign at, from bottom to top
# 	i = len(node) - 1
# 	while i >= 0:
# 		#j is index of first row with a different value
# 		j = i-1
# 		while j >= 0 and node[j] == node[i]:
# 			j -= 1
#
# 		#maxDiff is difference between next non same row and the i row
# 		maxDiff = 0
# 		#if j < 0 then same val as the top row so use n for maxDiff
# 		if j < 0:
# 			maxDiff = n - node[i]
# 		else:
# 			maxDiff = node[j] - node[i]
#
# 		#go through each diff
# 		for d in range(1, maxDiff+1):
# 			#make a coppy of the node
# 			baseParent = node[:]
# 			#set the top of the same rows equal to its val + diff
# 			baseParent[j+1] += d
#
# 			#if i the only row with that val then baseparent is the only parent for this d
# 			#(there are no subsequent rows to work through)
# 			if j == i - 1:
# 				parents.append(baseParent[:])
# 			#else go through recursively all the below rows
# 			else:
# 				#the max the row can go to, set to n then adjusted if there is an above row
# 				max = n
# 				if j >= 0:
# 					max = baseParent[j+1]
# 				#get all the possiblites for the rows under the top row with the same value
# 				subParents = getParentsRec(baseParent[j+2:i+1] , max)
# 				for sub in subParents:
# 					#combining the sub possiblity with the rest of the board
# 					newParent = baseParent[:j+2] + sub + baseParent[i+1:]
# 					parents.append(newParent)
# 		#sets the next row to work on to be the row above the top same row
# 		i = j
#
#
# 	retParents = []
# 	#clean out any zereos
# 	for parent in parents:
# 		x = len(parent) - 1
# 		while x >= 0 and parent[x] == 0:
# 			del parent[x]
# 			x -= 1
# 		retParents.append(tuple(parent))
#
# 	return retParents

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

# #TODO, right now just returning all parents
# def getExpandParents(even, n):
# 	parents = getParents(even, n)
# 	return parents
# 	#similar to the recursive generation of states.

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
