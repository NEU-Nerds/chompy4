import util
from sortedcontainers import SortedSet
import os
from pathlib import Path
import time
import sqlite3
conn = sqlite3.connect('nodes.db')
c = conn.cursor()
#conn.commit()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")

MAX_N = 4
DELTA_N = 1



def main():
    nevens = util.load(DATA_FOLDER / "n&evens.dat")
    n = nevens[0]
    evens = nevens[1]

    # conn = sqlite3.connect('nodes.db')
    # c = conn.cursor()

    firstStartT = time.time()

    while n+DELTA_N <= MAX_N:
        sT = time.time()

        util.genDB(c, n + DELTA_N)
        conn.commit()

        evens = expand(evens, n, DELTA_N)
        n += DELTA_N
        util.store((n, evens), DATA_FOLDER / "n&evens.dat")
        endT = time.time()
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
        print(str(n)+"X"+str(n)+" evens: " + str(evens))

    if n != MAX_N:
        sT = time.time()

        util.genDB(c, n + DELTA_N)
        conn.commit()

        evens = expand(evens, n, MAX_N-n)
        n = MAX_N
        endT = time.time()
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)) + "\t in " + str(endT-sT)+"s")
        print(str(n)+"X"+str(n)+" evens: " + str(evens))
        util.store((n, evens), DATA_FOLDER / "n&evens.dat")


def dbHandler():

    pass

def expand(evens, initN , deltaN):
    finalN = initN + deltaN

    #initialize cords to empty sets for each possible rho
    # cords = {}
    # for i in range(1,(finalN*finalN)+1):
    #     cords[i] = set([])

    #get all the new nods for (initN, finalN]
    newNodes = set([])
    for n in range(initN, finalN+1):
        newNodes.update(util.newNodes(n))
    # print("newNodes: " + str(newNodes))
    #add new nodes to DB
    util.addNodesToDB(newNodes, finalN, c)
    conn.commit()
    # print("evens: " + str(evens))
    util.removeParents(evens, finalN, c)
    conn.commit()

    for sigma in range(finalN*finalN+1):
        nodes = util.getSigmaNodes(sigma, n, c)
        util.removeParents(nodes, n, c)
        conn.commit()
        for node in nodes:
            evens.add(tuple(node))


    #get all parents of all evens and remove try to remove them from the list
    # evenParents = util.getParentsBatch(evens, n)
    # for parent in evenParents:
    #     cords[sum(parent)].discard(parent)

    # for key in cords.keys():
    #     if len(cords[key]) == 0:
    #         continue
    #
    #     parents = util.getParentsBatch(cords[key], n)
    #     for parent in parents:
    #         cords[sum(parent)].discard(parent)
    #
    #     for node in cords[key]:
    #         evens.add(node)
    #
    #     cords[key] = set([])

    return evens



def seed():

    evens = (1,set([(1,)]))
    util.store(evens, DATA_FOLDER / "n&evens.dat")
    # return evens


if __name__ == '__main__':
    seed()
    main()
