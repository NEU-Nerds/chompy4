
"""
treeTrim changes:
default evens = None
when a node is marked as even, delete all its leaves
(need recursive __del__ function)
Keep a dict of unevaluated nodes
once marked as false, remove from sigmaNodes, pathNodes, del path, del sigma,
   make it "inert"

Parent representation in terms of tree?

"""
class Tree():
	rootNode = None
	# sigmaUnchecked = {}
	maxDepthNodes = None


	pathNodes = {}
	def __init__(self, n):
		# for s in range(n*n+1):
		# 	self.sigmaUnchecked[s] = set([])
		self.maxDepthNodes = set([])
		self.rootNode = Node(n,n, self, None)

	# def getSigmaUnchecked(self,sigma):
	# 	return self.sigmaUnchecked[sigma]

	def getNode(self, path):
		return self.pathNodes[path]

	def __getitem__(self,index):
		return self.rootNode[index]

	def __repr__(self):
		return self.rootNode.__repr__()

	def __str__(self):
		return self.rootNode.__str__()

	#depricated
	# def expandTree(self, initN, n):
	# 	#expand and clear(should already be) sigmaUnchecked
	# 	for s in range(n*n+1):
	# 		self.sigmaUnchecked[s] = set([])
	#
	# 	#expand existing nodes to maxDepth
	# 	for node in self.maxDepthNodes.copy():
	# 		if node.even or len(node.path) < initN:
	# 			continue
	# 		node.expand(n-initN, self.sigmaUnchecked)
	#
	# 	#add new subTrees
	# 	for x in range(initN + 1, n+1):
	# 		newNode = Node(x, n-1, self, self.rootNode, [x])
	# 		self.rootNode.leaves.append(newNode)

class Node():
	path = None#tuple of the numbers chosen as the path to get to this point
	sigma = 0#the sum of this node's path
	parentTree = None#the pointer to the whole tree
	even = None
	branchNode = None#the parent node of this node
	leaves = []#list of pointers to the treeChildren of this node
	leaf = False#is this node at max depth

	evenLeaf = False #if the node has a leaf that is even
	combinedLeaf = False #if node has a leaf that is a combined node
	nodeDepth = 1 #the depth of this node (1 if not combined)
	# fullyChecked = False
	uncheckedLeaves = None#the number of unchecked leaves (inc. indirect leaves) remaining for this node
	# traversed = None

	def __init__(self, max, depth, parentTreeIn, branchNode, inPath = []):
		self.parentTree = parentTreeIn
		if depth > 0:
			self.leaves = [Node(x,depth-1, parentTreeIn, self, inPath + [x]) for x in range(1,max+1)]
			self.uncheckedLeaves = max
		else:
			self.parentTree.maxDepthNodes.add(self)
			self.leaf = True
			self.uncheckedLeaves = 0

		self.path = tuple(inPath)
		self.sigma = sum(inPath)
		self.branchNode = branchNode

		self.parentTree.pathNodes[self.path] = self
		# self.parentTree.sigmaUnchecked[self.sigma].add(self)
		self.traversed = False

	def expand(self, depth, sigmaUnchecked):
		self.leaves = [Node(x,depth-1, self.parentTree, self, list(self.path) + [x]) for x in range(1,self.path[-1]+1)]
		self.uncheckedLeaves = len(self.leaves)
		self.leaf = False
		# return self.leaves
	def expandNode(self):
		self.leaves = [Node(x,0, self.parentTree, self, list(self.path) + [x]) for x in range(1,self.path[-1]+1)]
		self.uncheckedLeaves = len(self.leaves)
		self.leaf = False
		return self.leaves

	def addLeaf(self):
		if len(self.path) > 0 and len(self.leaves) >= self.path[-1]:
			print("WTF YA DOING ADDING A LEAF TO A FULL NODE")
			return 1/0
		self.leaves.append(Node(len(self.leaves)+1, 0, self.parentTree, self, list(self.path) + [len(self.leaves)+1]))
		print("added leaf: " + str(self.leaves[-1]))
		return self.leaves[-1]

	def setOdd(self):
		# print("setOdd")
		if self.even is None:
			self.even = False
			# self.removeFromSigmaUnchecked()

			if self.leaf or self.uncheckedLeaves == 0:
				self.branchNode.decreaseChecked()
				# self.combine()
			#
			# if self.uncheckedLeaves == 0:
			# 	self.branchNode.decreaseChecked()
			#	self.combine()

	def decreaseChecked(self):
		self.uncheckedLeaves -= 1
		if self.uncheckedLeaves == 0 and self.even is not None:
			self.branchNode.decreaseChecked()
			# self.combine()

	def combine(self):
		#combining nodes
		if not self.evenLeaf and not self.combinedLeaf:
			#combine
			self.branchNode.combinedLeaf = True
			self.combineBranch(self.leaves)
			self.nodeDepth += 1

	def combineBranch(self, branch):
		if isinstance(branch, list):
			for leaf in branch:
				self.combineBranch(leaf)
		else:
			newBranch = []
			for leaf in branch:
				newBranch.append(leaf.leaves)
				self.evenLeaf = self.evenLeaf or leaf.evenLeaf
				self.increaseChecked(leaf.uncheckedLeaves)

			branch = newBranch

	def increaseChecked(self, x=1):
		self.uncheckedLeaves += x
		if self.uncheckedLeaves == x:
			self.branchNode.increaseChecked(x)

	# def removeFromSigmaUnchecked(self):
	# 	self.parentTree.sigmaUnchecked[self.sigma].remove(self)

	def setEven(self):
		print("setting even: " + str(self))
		if self.even is None:
			self.even = True
			# self.parentTree.sigmaUnchecked[self.sigma].remove(self)
			# self.removeFromSigmaUnchecked()

			for leafD in self.leaves:
				print("leafD: " + str(leafD))
				leafD.delManual()
				del leafD
			self.leaves.clear()

			self.branchNode.evenLeaf = True
			self.uncheckedLeaves = 0
			self.branchNode.decreaseChecked()

		else:
			print("Resetting an node to be even when it's already been set as " + str(self.even))

	def __repr__(self):
		return str(self.path)
		# return "HIII"
		if self.path == None:
			return "PATH IS NONE"
		else:
			return str(self.path)

	def __str__(self):
		return str(self.path)
		#
		# if self.leaf:
		# 	return str(self.even)
		# else:
		# 	return str([l.forStr() for l in self.leaves])

		if len(self.path) == 0:
			return "Root Node"
		else:
			return str(self.path)

	def delManual(self):
		return
		# print("delManual: " + str(self))
		# return
		#fucking nuke this thing to the astral sea
		for leaf in self.leaves:
			try:
				leaf.delManual()
				del leaf
			except:
				# print("except1")
				pass
		try:
			del self.parentTree.pathNodes[self.path]

		except:
			# print("except2")
			pass
		try:
			self.removeFromSigmaUnchecked()
			# self.parentTree.sigmaUnchecked[self.sigma].remove(self)
		except:
			# print("except3")
			pass
		if self.leaf:
			self.parentTree.maxDepthNodes.remove(self)

		del self.path
		del self.sigma
		self.leaves.clear()#maybe the problem is with this?
		del self.parentTree

	def __delete__(self):
		print("del: " + str(self))
		return
		#fucking nuke this thing to the astral sea
		for leaf in self.leaves:
			try:
				del leaf
			except:
				# print("except1")
				pass
		try:
			del self.parentTree.pathNodes[self.path]

		except:
			# print("except2")
			pass
		try:
			self.removeFromSigmaUnchecked()
			# del self.parentTree.sigmaUnchecked[self]
		except:
			# print("except3")
			pass
		if self.leaf:
			self.parentTree.maxDepthNodes.remove(self)

		del self.path
		del self.sigma
		self.leaves.clear()
		del self.parentTree
		pass

	def forStr(self):
		if self.leaf:
			return self.even
		else:
			return [l.forStr() for l in self.leaves]

	def toTuple(self):
		return tuple(self.path)

	def __getitem__(self,index):
		#only becuase 0's were being used previously
		if index == 0:
			return self
		return self.leaves[index-1]

	def layerEquivalence(self):
		layerEq = [False] * len(self.path)
		for i in range(1, len(self.path)):
			layerEq[i] = self.path[i] == self.path[i-1]
		return layerEq

class OddNode(Node):
	 def __init__(self):
		 pass
