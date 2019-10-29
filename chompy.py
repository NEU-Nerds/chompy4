import util
from sortedcontainers import SortedSet
"""
seed 1x1

for n

add new nodes
extend constraints
add new constraints

for all cords sorted by rho
work constraints
add expandable constraints to list
add this node to evens
del this node

"""
"""
store: evens, expandable contraints?
sess data: cord list

"""

MAX_N = 11

def main():
    evens = seed()

    evens = expand(evens, 2, MAX_N - 2)
    print(str(MAX_N)+"X"+str(MAX_N)+" #evens: " + str(len(evens)))

def expand(evens, initN , deltaN):
    finalN = initN + deltaN

    #initialize cords to empty sets for each possible rho
    cords = {}
    for i in range(1,(finalN*finalN)+1):
        cords[i] = set([])

    #get all the new nods for (initN, finalN]
    newNodes = []
    for n in range(initN, finalN+1):
        newNodes = newNodes + util.newNodes(n)
    #add new nodes to cords
    for node in newNodes:
        cords[sum(node)].add(node)

    #get all parents of all evens and remove try to remove them from the list
    evenParents = util.getParentsBatch(evens, n)
    for parent in evenParents:
        cords[sum(parent)].discard(parent)

    for key in cords.keys():
        if len(cords[key]) == 0:
            continue

        parents = util.getParentsBatch(cords[key], n)
        for parent in parents:
            cords[sum(parent)].discard(parent)

        for node in cords[key]:
            evens.add(node)

        cords[key] = set([])
    return evens



def seed():

    evens = set([(1,)])
    return evens


if __name__ == '__main__':

    main()
