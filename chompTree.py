
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
	# maxDepth = None


	pathNodes = {}
	def __init__(self, n):
		# for s in range(n*n+1):
		# 	self.sigmaUnchecked[s] = set([])
		maxDepth = n
		self.maxDepthNodes = set([])
		self.rootNode = nodeWrapper(n,n, self, None)

	# def getSigmaUnchecked(self,sigma):
	# 	return self.sigmaUnchecked[sigma]

	def getNode(self, path):
		return self.pathNodes[path]

	def __getitem__(self,index):
		return self.rootNode[index]

	def __repr__(self):
		return self.rootNode.__repr__()

	def __str__(self):
		return "TREE"
		return self.rootNode.__str__()



class Node():
	path = None#tuple of the numbers chosen as the path to get to this point
	sigma = 0#the sum of this node's path
	parentTree = None#the pointer to the whole tree
	even = None
	branchNodeW = None#the parent node of this node
	leaves = None#list of pointers to the treeChildren of this node
	leaf = False#is this node at max depth

	evenLeaf = False #if the node has a leaf that is even
	combinedLeaf = False #if node has a leaf that is a combined node
	developedLeaves = 0 #number of leaves which themselves have full leaves
	maxLeaves = 0 # number of leaves at max depth
	nodeDepth = 1 #the depth of this node (1 if not combined)
	# fullyChecked = False
	uncheckedLeaves = None#the number of unchecked leaves (inc. indirect leaves) remaining for this node
	# traversed = None
	wrapper = None

	def __init__(self, max, depth, parentTreeIn, branchNodeW, wrap, inPath = []):
		self.parentTree = parentTreeIn
		self.uncheckedLeaves = 0
		# self.internalLeaves = 0
		# print("")
		# print(f"max: {max}")
		# print(f"depth: {depth}")
		# print(f"parentTreeIn: {parentTreeIn}")
		# print(f"branchNode: {branchNodeW}")
		# print(f"wrap: {wrap}")
		# print(f"inPath: {inPath}")
		self.maxLeaves = max
		self.wrapper = wrap

		# self.uncheckedLeaves = 0
		# print("created " + str(inPath))
		self.path = tuple(inPath)
		self.sigma = sum(inPath)
		self.branchNodeW = branchNodeW

		self.parentTree.pathNodes[self.path] = self.wrapper
		# self.parentTree.sigmaUnchecked[self.sigma].add(self)
		# self.traversed = False
		if len(self.path) > 1:
			self.branchNodeW.increaseUnchecked()

		self.initPt2(max, depth, inPath)

	def initPt2(self, max, depth, inPath):
		if depth > 0:
			# self.uncheckedLeaves = 0
			self.leaves = [nodeWrapper(x,depth-1, self.parentTree, self.wrapper, inPath + [x]) for x in range(1,max+1)]
			# self.uncheckedLeaves = max
			if len(self.path) > 0:
				self.branchNodeW.increaseInternalLeaves()
		else:
			# print(f"self.wrapper: {self.wrapper}")
			self.parentTree.maxDepthNodes.add(self.wrapper)
			# self.branchNode.
			self.leaf = True
			# self.uncheckedLeaves = 0
			self.leaves = []

	def expandNode(self):
		if self.even:
			return
		self.leaves = [nodeWrapper(x,0, self.parentTree, self.wrapper, list(self.path) + [x]) for x in range(1,self.path[-1]+1)]
		self.uncheckedLeaves = len(self.leaves)
		self.setNotLeaf()
		return self.leaves

	def addLeaf(self):
		w = self.wrapper
		if self.even:
			return
		# print("Adding leaf to " + str(self))
		self.setNotLeaf()
		if self.nodeDepth > 1:
			print("WTF YA DOING ADDING A LEAF TO A COMBINED NODE")
			return 1/0
		if len(self.path) > 0 and len(self.leaves) >= self.path[-1]:
			print("WTF YA DOING ADDING A LEAF TO A FULL NODE")
			return 1/0
		# print(f"pre leaves: {self.leaves}")
		node = nodeWrapper(len(self.leaves)+1, 0, self.parentTree, self.wrapper, list(self.path) + [len(self.leaves)+1])
		# self.increaseUnchecked()
		self.leaves.append(node)
		# print(f"post leaves: {self.leaves}")
		# print("added leaf: " + str(node))
		# print(f"w.node.leaves {w.node.leaves}")
		if len(w.node.path) > 0 and len(w.node.leaves) == w.node.path[-1]:
			# print("Incearsing developedLeaves from addLeaf")
			w.node.branchNodeW.increaseDevelopedLeaves()
		# print(f"w.node.leaves {w.node.leaves}")
		return node

	def setNotLeaf(self):
		if self.leaf:
			self.leaf = False
			# print("removing from MDN: " + str(self))
			self.parentTree.maxDepthNodes.remove(self.wrapper)

	def setOdd(self):
		# print("setOdd")
		if self.even is None:
			self.even = False
			# self.removeFromSigmaUnchecked()
			#self.leaf or
			if self.uncheckedLeaves == 0:
				self.branchNodeW.decreaseUnchecked()
				# if len(self.leaves) > 0:
				#
				# 	self.combine()

	def combine(self):
		# return
		# print("attempting combining: " + str(self))
		#combining nodes
		# print("combine node leaves: " + str(self.leaves))
		if not self.evenLeaf and not self.combinedLeaf and self.developedLeaves == self.maxLeaves and self.even == False:
			# print("combining: " + str(self) + " to depth: " + str(self.nodeDepth + 1))
			# print(f"original evenLeaf: {self.evenLeaf}")
			# print(f"original combinedLeaf: {self.combinedLeaf}")
			# print(f"original developedLeaves: {self.developedLeaves}")
			# print(f"original maxLeaves: {self.maxLeaves}")
			# print("original leaves: " + str(self.leaves))
			#combine

			self.branchNodeW.node.combinedLeaf = True
			self.developedLeaves = 0
			self.maxLeaves = 0
			self.combineBranch1(self.leaves)
			self.leaves = self.combineBranch(self.leaves)
			self.nodeDepth += 1
			# print(f"combined evenLeaf: {self.evenLeaf}")
			# print(f"combined combinedLeaf: {self.combinedLeaf}")
			# print(f"combined developedLeaves: {self.developedLeaves}")
			# print(f"combined maxLeaves: {self.maxLeaves}")
			# print("combined leaves: " + str(self.leaves))
			# print("")

	def combineBranch1(self, branch):
		if isinstance(branch[0], list):
			for leaf in branch:
				self.combineBranch1(leaf)
		else:
			for leaf in branch:
				if len(leaf.node.path) > 0:
					self.maxLeaves += leaf.node.path[-1]


	def combineBranch(self, branch):
		if isinstance(branch[0], list):
			newBranch = []
			for leaf in branch:
				newBranch.append(self.combineBranch(leaf))
			return newBranch
		else:
			newBranch = []
			for leaf in branch:
				# print("internal leaf: " + str(leaf))

				# print(f"leaf.node.leaves: {leaf.node.leaves}")
				newBranch.append(leaf.node.leaves)
				self.evenLeaf = self.evenLeaf or leaf.node.evenLeaf

				for l in leaf.node.leaves:
					if len(l.node.leaves) == l.node.path[-1]:
						self.increaseDevelopedLeaves()

				self.increaseUnchecked(leaf.node.uncheckedLeaves)

				try:
					leaf.delManual()
				except:
					pass

				leaf.node = self
			# print("newBranch: " + str(newBranch))
			# branch = newBranch
			return newBranch

	def decreaseUnchecked(self):
		self.uncheckedLeaves -= 1
		if self.uncheckedLeaves == 0 and self.even is not None:
			self.branchNodeW.decreaseUnchecked()
			if len(self.leaves) > 0:
				# print("!")
				self.combine()

	def increaseUnchecked(self, x=1):
		self.uncheckedLeaves += x
		if self.uncheckedLeaves == x:
			if len(self.path) > 0:
				self.branchNodeW.increaseUnchecked(x)

	def decreaseDevelopedLeaves(self):
		self.developedLeaves -=1

	def increaseDevelopedLeaves(self, x=1):
		self.developedLeaves += x
		if self.developedLeaves == self.maxLeaves:
			self.combine()

	def setEven(self):
		# print("setting even: " + str(self))
		if self.even is None:
			# print("setting even: " + str(self))
			self.even = True
			# self.parentTree.sigmaUnchecked[self.sigma].remove(self)
			# self.removeFromSigmaUnchecked()

			# WHY DOES THIS NEED TO BE COMMENTED?
			for leafD in self.leaves:
				# print("leafD: " + str(leafD))
				leafD.delManual()
				del leafD
			self.leaves.clear()

			self.branchNodeW.node.evenLeaf = True
			self.uncheckedLeaves = 0
			self.branchNodeW.decreaseUnchecked()
			# print("removing from maxDepthNodes")
			# print(f"maxDepthNodes: {self.parentTree.maxDepthNodes}")
			self.parentTree.maxDepthNodes.remove(self.wrapper)
			# print(f"maxDepthNodes: {self.parentTree.maxDepthNodes}")

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

		# return
		# print("delManual: " + str(self))
		# return
		#fucking nuke this thing to the astral sea
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
		del self.leaves
		del self.path
		del self.sigma
		del self.uncheckedLeaves

		del self.wrapper
		del self.even
		del self.branchNodeW
		del self.evenLeaf
		del self.combinedLeaf
		del self.developedLeaves
		del self.maxLeaves
		del self.nodeDepth


		# self.leaves.clear()#maybe the problem is with this?
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

class nodeWrapper():
	node = None

	def __init__(self, a, b, c, d, e = []):
		# print("NEW nodeWrapper")
		# print(f"a: {a}")
		# print(f"b: {b}")
		# print(f"c: {c}")
		# print(f"d: {d}")
		# print(f"self: {self}")
		# print(f"e: {e}")
		self.node = Node(a,b,c,d, self ,e)


	def initPt2(self, max, depth, inPath):
		return self.node.initPt2(max, depth, inPath)

	def expandNode(self):
		return self.node.expandNode()

	def addLeaf(self):
		return self.node.addLeaf()

	def setNotLeaf(self):
		return self.node.setNotLeaf()

	def setOdd(self):
		return self.node.setOdd()

	def combine(self):
		return self.node.combine()

	def combineBranch(self, branch):
		return self.node.combineBranch(branch)

	def decreaseUnchecked(self):
		return self.node.decreaseUnchecked()

	def increaseUnchecked(self, x=1):
		return self.node.increaseUnchecked(x)

	def decreaseDevelopedLeaves(self):
		return self.node.decreaseDevelopedLeaves()

	def increaseDevelopedLeaves(self, x=1):
		return self.node.increaseDevelopedLeaves(x)

	def setEven(self):
		return self.node.setEven()

	def __repr__(self):
		return self.node.__repr__()

	def __str__(self):
		return 'wraped \"' + self.node.__str__() +'\"'

	def delManual(self):
		return self.node.delManual()

	def __delete__(self):
		return self.node.__delete__()

	def forStr(self):
		return self.node.forStr()

	def toTuple(self):
		return self.node.toTuple()

	def __getitem__(self,index):
		return self.node.__getitem__(index)

	def layerEquivalence(self):
		return self.node.layerEquivalence()
