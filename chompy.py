import util
from sortedcontainers import SortedSet
import os
from pathlib import Path
import time
import chompTree
import treeParents
import depthParents

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
# THIS_FOLDER = "/Users/tymarking/Documents/chomp/chompy4"
# print(THIS_FOLDER)
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

MAX_M = 10
MAX_N = 10

DELTA_N = 1
DELTA_M = 1

def main(MAX_N, DELTA_N):
	#seed here for testing
	tree = chompTree.Tree(1)
	util.fillTree([tree.getNode((1,))], tree, 1)
	tree.getNode((1,)).setEven()

	mn_evens = ((1,1), [ [], set([tree.getNode((1,))]) ] )
	mnevens = mn_evens



	# nevens = util.load(DATA_FOLDER / "mn&evens.dat")
	# tree = util.load(DATA_FOLDER / "tree.dat")
	m = mnevens[0][0]
	n = mnevens[0][1]
	#evens is list by depth of sets of evens
	evens = mnevens[1]
	firstStartT = time.time()

	while m < MAX_M or n < MAX_N:
		dM = min(DELTA_M, MAX_M - m)
		dN = min(DELTA_N, MAX_N - n)

		sT = time.time()
		evens, tree = expand(evens, tree, m, dM, n, dN)
		endT = time.time()
		m += dM
		n += dN
		s = 0
		for depth in evens:
			s += len(depth)
		print(str(m)+"X"+str(n)+" #evens: " + str(s) + "\t in " + str(endT-sT)+"s")
		# print(str(n)+"X"+str(n)+" evens: " + str(evens))

	util.store(((m,n), evens), DATA_FOLDER / "mn&evens.dat")

def expand(evens, tree, m, dM, n, dN):
	"""
	Side Expand
		For depth
	"""
	#side expand
	#up to prev n
	workingNodes = []
	for x in range(dM):
		# print("Adding leaf sideExpansion")
		leaf = tree.rootNode.addLeaf()
		leaf.setOdd()
		workingNodes.append(leaf)


	#expand sideways, modify evens
	for depth in range(2, n+1):
		leaves = []
		for node in workingNodes:
			leaves += node.expandNode()
		workingNodes = depthParents.sideExpansion(evens[depth], leaves, m, dM)

	for node in workingNodes:
		tree.maxDepthNodes.add(node)

	#bottom expand
	for depth in range(n+1, n+dN + 1):
		#expand down, modify evens
		util.expandDown(tree, evens, m+dM, depth)
		pass
	return evens, tree

def seed():
	tree = chompTree.Tree(1)
	util.fillTree([tree.getNode((1,))], tree, 1)
	tree.getNode((1,)).setEven()

	n_evens = (1, [ [], set([tree.getNode((1,))]) ] )

	# util.store(n_evens, DATA_FOLDER / "mn&evens.dat")
	# util.store(tree, DATA_FOLDER / "tree.dat")
	# return evens


if __name__ == '__main__':
	seed()
	main(MAX_N, DELTA_N)
