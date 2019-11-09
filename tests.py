import util
import time
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/")


nevens = util.load(DATA_FOLDER / "nevens.dat")
n = nevens[0]
evens = nevens[1]


# startT = time.time()
#
# print(len(util.newNodes(15)))
# print("In " + str(time.time()-startT)+"s")
# print(util.getParents((2,1),3) )
# print(util.getParents((3,1,1),3) )
# # print(util.newNodes(4))
# print()
# print(util.getParentsBatch([(2,1), (3,1,1)],3) )
# tree = util.initTree(3,3)
# tree[2][1][0] = False
# tree[3][1][0] = False
# tree[1][1][1] = False
# print(tree)
# print(util.getSigmaEvens(tree, 0, 3))
# print(util.newNodes(3))

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

def getP(node, n):
	parents = []
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
				parents.append(baseParent)
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
					parents.append(newParent)
		#sets the next row to work on to be the row above the top same row
		i = j
	return parents

# parents = getP([3,3],n)
for child in util.getChildren([3,3,3,3,2]):
	if tuple(child) in evens:
		print("even parent: " + str(child))
