import util
from sortedcontainers import SortedSet
import os
from pathlib import Path
import time
import chompTree
import treeParents

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

MAX_N = 4
DELTA_N = 1

def main(MAX_N, DELTA_N):
	#seed here for testing
	tree = chompTree.Tree(1)
	util.fillTree([tree.getNode((1,))], tree, 1)
	tree.getNode((1,)).setEven()

	n_evens = (1,set([tree.getNode((1,))]))
	nevens = n_evens


	# nevens = util.load(DATA_FOLDER / "n&evens.dat")
	# tree = util.load(DATA_FOLDER / "tree.dat")

	n = nevens[0]
	evens = nevens[1]
	firstStartT = time.time()
	while n+DELTA_N <= MAX_N:
		sT = time.time()
		evens, tree = expand(evens, tree, n, DELTA_N)
		n += DELTA_N
		util.store((n, evens), DATA_FOLDER / "n&evens.dat")
		endT = time.time()
		print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
		print(str(n)+"X"+str(n)+" evens: " + str(evens))
	#if the difference between starting n and MAX_N is not a multiple of DELTA_N, we have to do this:
	if n != MAX_N:
		sT = time.time()
		evens, tree = expand(evens, tree, n, MAX_N-n)
		n = MAX_N
		util.store((n, evens), DATA_FOLDER / "n&evens.dat")
		endT = time.time()
		print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
		print(str(n)+"X"+str(n)+" evens: " + str(evens))
	# print(len(evens))
	# print("4, 1, 1, 1: " + str(tree.pathNodes))
	util.store((n, evens), DATA_FOLDER / "n&evens.dat")

def expand(evens, tree, initN , deltaN):
	"""
	Build tree from condition generations!
	"""
	# print("inEvens: " + str(evens))

	n = initN + deltaN
	# tree = chompTree.Tree(n)
	# util.expandTree(initN, n)
	# print("\nExpanding")
	# print("Pre Expansion PathNodes: " + str(tree.pathNodes))
	tree.expandTree(initN, n)
	# util.transverseParents(evens, tree)
	# util.fillTree(evens, tree, n)
	# print("root node leaves: " + str(tree.rootNode.leaves))
	# print("Tree: \n" + str(tree.pathNodes) + "\n")
	for even in evens:
		# print("even: " + str(even))
		# print("bNode: " + str(even.branchNode))
		# print("bMates: " + str(even.branchNode.leaves))
		# print("branchNode == rootNode: " + str(even.branchNode == tree.rootNode))

		treeParents.getParents(even, tree)
		# print("\n\n")
	# print("Expanded")
	# print("Expanded PathNodes: " + str(tree.pathNodes))
	#iterate through tree starting with lowest sigma and fillTree with that node
	#at some point change tree to deal with sigma

	for sigma in range(1, n*n+1):
		# print(f"\nsigma {sigma}")
		newEvens = tree.getSigmaUnchecked(sigma)
		# if n >= 5:
		#	 if tree.getNode((3,3,3,3,2)) in newEvens:
		#		 print(f"IT'S FUCKING THERE :{sigma}")
		# util.fillTree(newEvens, tree, n)

		# print("root node leaves: " + str(tree.rootNode.leaves))
		# print("Tree: \n" + str(tree.pathNodes) + "\n")
		# for even in newEvens.copy():
		for even in newEvens.copy():
			# print("even: " + str(even))
			# print("bNode: " + str(even.branchNode))
			# print("bMates: " + str(even.branchNode.leaves))
			# print("\n\n\n")
			treeParents.getParents(even, tree)

		# print("setting new evens.")

		# util.transverseParents(newEvens, tree)
		# newEvens = tree.getSigmaUnchecked(sigma)
		for even in newEvens.copy():
			# treeParents.getParents(even, tree)
			# print("even: " + str(even.__repr__()))
			# try:
			even.setEven()
			# print("setEven")
			# except:
				# print(f"\n\texcepted while trying to set even for {even}\n")
			evens.add(even)
			# print("added to evens")

	return evens, tree

def seed():
	tree = chompTree.Tree(1)
	util.fillTree([tree.getNode((1,))], tree, 1)
	tree.getNode((1,)).setEven()

	n_evens = (1,set([tree.getNode((1,))]))

	# util.store(n_evens, DATA_FOLDER / "n&evens.dat")
	# util.store(tree, DATA_FOLDER / "tree.dat")
	# return evens


if __name__ == '__main__':
	seed()
	main(MAX_N, DELTA_N)
