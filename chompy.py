import util
from sortedcontainers import SortedSet
import os
from pathlib import Path
import time
import chompTree

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc2/")

MAX_N = 11
DELTA_N = 1

def main(MAX_N, DELTA_N):
    nevens = util.load(DATA_FOLDER / "n&evens.dat")
    tree = util.load(DATA_FOLDER / "tree.dat")
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
        # print(str(n)+"X"+str(n)+" evens: " + str(evens))
    if n != MAX_N:
        sT = time.time()
        evens, tree = expand(evens, tree, n, MAX_N-n)
        n = MAX_N
        util.store((n, evens), DATA_FOLDER / "n&evens.dat")
        endT = time.time()
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
        # print(str(n)+"X"+str(n)+" evens: " + str(evens))
    util.store((n, evens), DATA_FOLDER / "n&evens.dat")


def expand(evens, tree, initN , deltaN):
    """
    Build tree from condition generations!

    """

    n = initN + deltaN

    tree.expandTree(initN, n)
    util.fillTree(evens, tree, n)

    for sigma in range(1, n*n+1):
        newEvens = tree.getSigmaUnchecked(sigma)

        util.fillTree(newEvens, tree, n)

        for even in newEvens.copy():
            even.setEven()
            evens.add(even)

    return evens, tree

def seed():

    tree = chompTree.Tree(1)
    evens = (1,set([tree.getNode((1,))]))
    util.store(evens, DATA_FOLDER / "n&evens.dat")
    util.fillTree([tree.getNode((1,))], tree, 1)
    tree.getNode((1,)).setEven()

    util.store(tree, DATA_FOLDER / "tree.dat")



if __name__ == '__main__':
    seed()
    main(MAX_N, DELTA_N)
