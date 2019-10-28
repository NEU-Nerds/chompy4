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

MAX_N = 2

def main():
    evens = seed()

    for n in range(2, MAX_N+1):

        cords = SortedSet(util.newNodes(n), key=lambda x: sum(x))

        for even in evens:
            # expandParents = util.getExpandParents(even, n)
            for parent in util.getExpandParents(even, n):
                try:
                    print("removing1")
                    cords.remove(parent)
                except:
                    pass
        print("Pre0  cords: " + str(cords))
        while len(cords) > 0:
            node = cords.pop(0)
            print("node: " + str(node))
            #remove all parents from cords
            parents = util.getParents(node, n)
            print("Parents: " + str(parents))
            for parent in parents:
                print("parent: " + str(parent))
                print("Pre  cords: " + str(cords))
                try:
                    print("removing2")
                    cords.remove(parent)

                except:
                    pass
                print("Post cords: " + str(cords))

            evens.add(node)
        print(str(n)+"X"+str(n)+" evens: " + str(evens))



def seed():

    evens = set([(1,)])
    return evens


if __name__ == '__main__':

    main()
