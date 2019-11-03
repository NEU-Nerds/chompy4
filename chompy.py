import util
from sortedcontainers import SortedSet
import os
from pathlib import Path
import time

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")

MAX_N = 13
DELTA_N = 100

def main():
    nevens = util.load(DATA_FOLDER / "n&evens.dat")
    n = nevens[0]
    evens = nevens[1]
    firstStartT = time.time()

    while n+DELTA_N <= MAX_N:
        sT = time.time()
        evens = expand(evens, n, DELTA_N)
        n += DELTA_N
        util.store((n, evens), DATA_FOLDER / "n&evens.dat")
        endT = time.time()
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
        # print(str(n)+"X"+str(n)+" evens: " + str(evens))
    if n != MAX_N:
        sT = time.time()
        evens = expand(evens, n, MAX_N-n)
        n = MAX_N
        endT = time.time()
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
        # print(str(n)+"X"+str(n)+" evens: " + str(evens))
    util.store((n, evens), DATA_FOLDER / "n&evens.dat")


def expand(evens, initN , deltaN):
    """
    Build tree from condition generations!

    """

    n = initN + deltaN

    sigmaDict = {}
    for s in range(n*n+1):
        sigmaDict[s] = []

    tree = util.initTree(n, n, sigmaDict)
    # print(f"sigmaDict: {sigmaDict}")
    # print(f"initEvens: {evens}")
    # print(f"tree: {tree}")
    util.fillTree(evens, tree, n)
    # print(f"filled tree: {tree}")


    #iterate through tree starting with lowest sigma and fillTree with that node
    #at some point change tree to deal with sigma
    for sigma in range(1, n*n+1):
        # newEvens = util.getSigmaEvens(tree, sigma, n)
        newEvens = []
        for evenT in sigmaDict[sigma]:
            # print(f"evenT: {evenT}")
            if evenT[0][evenT[1]]:
                newEvens.append(evenT[2])
        newEvens = util.cleanParents(newEvens)
        # print(f"sigma {sigma} newEvens: {newEvens}")
        # print(f"newEvens: {newEvens}")
        util.fillTree(newEvens, tree, n)
        for even in newEvens:
            evens.add(tuple(even))
    # print(f"sigmaDict: {sigmaDict}")
    return evens



def seed():

    evens = (1,set([(1,)]))
    util.store(evens, DATA_FOLDER / "n&evens.dat")
    # return evens


if __name__ == '__main__':
    seed()
    main()
