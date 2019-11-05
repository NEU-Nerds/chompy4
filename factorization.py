import util
import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")


nevens = util.load(DATA_FOLDER / "n&evens.dat")
N = nevens[0]
evens = nevens[1]

evenBySigma = {}
evenXnum = {}
numXeven = {}

factXnodes = {}

evens.remove((1,))

for i in range(1,(N*N)+1):
    evenBySigma[i] = set([])

count = 0
for even in evens:
    evenXnum[count] = even
    numXeven[even] = count
    count += 1
    evenBySigma[sum(even)].add(even)

for n in range(2,6):
    print("n: " +str(n))
    cords = {}
    for i in range(1,(n*n)+1):
        cords[i] = set([])

    #get all the new nods for (initN, finalN]
    newNodes = []
    for x in range(2,n+1):
        newNodes = newNodes + util.newNodes(x)
    #add new nodes to cords
    for node in newNodes:
        cords[sum(node)].add(node)


    for s in range(1,(n*n)+1):
        nodes = cords[s]
        for node in nodes:
            # print("node: " + str(node))
            children = util.getChildren(list(node))
            fact = []
            for child in children:
                if tuple(child) in evens:
                    fact.append(numXeven[tuple(child)])
            fact.sort()
            factS = tuple(fact)
            # for f in fact:
            #     factS += str(f) + "_"
            if factS in factXnodes.keys():
                factXnodes[factS].append(node)
            else:
                factXnodes[factS] = [node]
    # print("factXnodes: " + str(factXnodes))
    for key in factXnodes:
        print("key: " + str(key))
        print(len(factXnodes[key]))

# print("numXeven: " + str(numXeven))
# for key in factXnodes:
#     print("key: " + str(key))
#     maxN = 0
#     for even in factS:
#         maxN = max(len(evenXnum[even]), evenXnum[even][0], maxN)
