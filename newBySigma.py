import util
import chompy
import os
from pathlib import Path
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
#THIS_FOLDER = "D:/Mass Storage/Math/chompy"
THIS_FOLDER = Path(THIS_FOLDER)
DATA_FOLDER = Path(THIS_FOLDER, "./data/epoc1/")

finalN = 12

def main ():
    print("Generating evens.")
    chompy.main(finalN, finalN + 5)
    print("Loading evens.")
    nevens = util.load(DATA_FOLDER / "n&evens.dat")
    n = nevens[0]
    evens = nevens[1]
    print(n)
    evens = list(evens)

    print(f"Removing evens with n not {finalN}.")
    evens = purgeBoards(evens, finalN)

    print("Counting new evens by sigma.")
    evensBySigma = {}
    for s in range(n**2 + 1):
        evensBySigma[s] = 0
    for board in evens:
        evensBySigma[sum(board)] += 1

    print(f"Generating nodes with n {finalN}.")
    newNodes = util.newNodes(finalN)
    newNodes = purgeBoards(newNodes, finalN)
    print(len(newNodes))
    print("Counting new nodes by sigma.")
    allBySigma = {}
    for s in range(n**2 + 1):
        allBySigma[s] = 0
    for board in newNodes:
        allBySigma[sum(board)] += 1

    print("Exporting data.")
    # with open(THIS_FOLDER/"data"/"sigmaNumbers.csv", "w", newline="") as csvfile:
    with open(THIS_FOLDER/"data"/"newSigmaNumbersAll.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow([f"Increasing from: {finalN-1} to {finalN}"])
        writer.writerow(["sigma", "# new nodes", "# new evens"])
        for key in range(n*n + 1):
            writer.writerow([str(key), str(allBySigma[key]), str(evensBySigma[key])])

def purgeBoards(boards, n):
    nBoards = []
    for board in boards:
        if len(board) == n or board[0] == n:
            nBoards.append(board)
    return nBoards

def sortKey(board):
    return sum(board)

if __name__ == "__main__":
    main()
