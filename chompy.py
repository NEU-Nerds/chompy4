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

MAX_N = 5

def main():
    evens = seed()

    for n in range(n, MAX_N+1):

        cords = SortedSet(util.newNodes(n), key=lambda x: sum(x))

        for even in evens:
            # expandParents = util.getExpandParents(even, n)
            for parent in util.getExpandParents(even, n):
                try:
                    cords.remove(parent)
                except:
                    pass

        while len(cords) > 0:
            node = cords.pop(0)
            #remove all parents from cords
            for parent in util.getParents(node, n):
                try:
                    cords.remove(parent)
                except:
                    pass

            evens.add(node)
        print(str(n)+"X"+str(N)+" evens: " + str(evens))



def seed():

    evens = set([(1,)])
    return evens


if __name__ == '__main__':

    main()
