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

MAX_N = 10

def main():
    evens = seed()

    for n in range(2, MAX_N+1):
        #list of new nodes sorted by rho
        cords = SortedSet(util.newNodes(n), key=lambda x: sum(x))

        #Handle extended constraints from previous nodes very poorly
        #DO THIS WITH SET FUNCTIONALITY?
        for even in evens:
            #get all parents of all evens and remove try to remove them from the list
            cords -= util.getExpandParents(even, n)
            # for parent in util.getExpandParents(even, n):
            #     try:
            #         cords.remove(parent)
            #     except:
            #         pass

        #Go through each node left (they will be even)
        while len(cords) > 0:
            node = cords.pop(0)
            #remove all parents from cords
            cords -= util.getParents(node, n)
            # parents = util.getParents(node, n)
            # for parent in parents:
            #     try:
            #         cords.remove(parent)
            #     except:
            #         pass
            evens.add(node)

        # print(str(n)+"X"+str(n)+" evens: " + str(evens))
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)))

def main2():
    evens = seed()

    #list of new nodes sorted by rho
    newNodes = []
    for n in range(2,MAX_N+1):
        newNodes = newNodes + util.newNodes(n)

    cords = SortedSet(newNodes, key=lambda x: sum(x))

    #Handle extended constraints from previous nodes very poorly
    #DO THIS WITH SET FUNCTIONALITY?
    for even in evens:
        #get all parents of all evens and remove try to remove them from the list
        cords -= util.getExpandParents(even, n)
        # for parent in util.getExpandParents(even, n):
        #     try:
        #         cords.remove(parent)
        #     except:
        #         pass

    #Go through each node left (they will be even)
    while len(cords) > 0:
        node = cords.pop(0)
        #remove all parents from cords
        cords -= util.getParents(node, n)
        # parents = util.getParents(node, n)
        # for parent in parents:
        #     try:
        #         cords.remove(parent)
        #     except:
        #         pass
        evens.add(node)

    # print(str(n)+"X"+str(n)+" evens: " + str(evens))
    print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)))


def seed():

    evens = set([(1,)])
    return evens


if __name__ == '__main__':

    main2()
