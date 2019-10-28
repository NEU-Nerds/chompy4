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

    for n in range(2, MAX_N+1):
        #list of new nodes sorted by rho
        cords = SortedSet(util.newNodes(n), key=lambda x: sum(x))

        # print("Pre-1  cords: " + str(cords))
        #Handle extended constraints from previous nodes very poorly
        for even in evens:
            # expandParents = util.getExpandParents(even, n)
            for parent in util.getExpandParents(even, n):
                try:
                    # print("removing1: " + str(parent))
                    if tuple(parent) == (4,2,2):
                        print("CASE 1 from even: " + str(even))
                    cords.remove(parent)
                except:
                    pass
        # print("Pre0  cords: " + str(cords))
        #Go through each node left (will be an even one)
        while len(cords) > 0:
            node = cords.pop(0)
            # print("node: " + str(node))
            #remove all parents from cords
            parents = util.getParents(node, n)
            # print("Parents: " + str(parents))
            for parent in parents:
                # print("parent: " + str(parent))
                # print("Pre  cords: " + str(cords))
                try:
                    # print("removing2: " + str(parent))
                    if tuple(parent) == (4,2,2):
                        print("CASE 2 from node: " + str(node))
                    cords.remove(parent)

                except:
                    pass
                # print("Post cords: " + str(cords))

            evens.add(node)

        print(str(n)+"X"+str(n)+" evens: " + str(evens))
        print(str(n)+"X"+str(n)+" #evens: " + str(len(evens)))



def seed():

    evens = set([(1,)])
    return evens


if __name__ == '__main__':

    main()
