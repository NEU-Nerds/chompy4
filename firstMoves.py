import util
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

firstMoves = {}
n_evens = util.load(DATA_FOLDER / "n&evens.dat")
evens = set(n_evens[1])
n = n_evens[0]
for i in range(2,n+1):
	for j in range(i,n+1):
		print("Getting moves for " + str(i)+"X"+str(j))
		fms = []
		emptyB = [j]*i
		children = util.getChildren(emptyB)
		for child in children:
			#or str(util.mirror(child)) in evens

			if tuple(child) in evens:
				fms.append(child)
		firstMoves[str(i)+"X"+str(j)] = fms
		if len(fms) > 1:
			print("Length of "+ str(i)+"X"+str(j)+" fms is " + str(len(fms)))
util.storeJson(firstMoves, DATA_FOLDER / "firstMovesV4_2.json")
