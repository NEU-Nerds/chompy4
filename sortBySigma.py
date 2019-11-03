import util
import os
from pathlib import Path
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")

finalN = 12

def main ():
    # nevens = util.load(DATA_FOLDER / "n&evens.dat")
    # n = nevens[0]
    # evens = nevens[1]
    # print(n)
    # evens = list(evens)
    # evens.sort(key=sortKey)
    # # print(evens)
    # newNodes = evens

    newNodes = []
    for n in range(1, finalN):
        newNodes = newNodes + util.newNodes(n)
    print(len(newNodes))
    newNodes.sort(key=sortKey)
    newNodes = util.cleanParents(newNodes)
    newNodes = list(newNodes)

    bySigma = {}
    for s in range(n**2 + 1):
        bySigma[s] = 0
    for board in newNodes:
        bySigma[sum(board)] += 1

    # with open(THIS_FOLDER/"data"/"sigmaNumbers.csv", "w", newline="") as csvfile:
    with open(THIS_FOLDER/"data"/"sigmaNumbersAll.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow(["sigma", "# of nodes"])
        for key in bySigma.keys():
            writer.writerow([str(key), str(bySigma[key])])


def sortKey(board):
    return sum(board)

if __name__ == "__main__":
    main()
