import util
import time

# startT = time.time()
#
# print(len(util.newNodes(15)))
# print("In " + str(time.time()-startT)+"s")
print(util.getParents((2,1),3) )
print(util.getParents((3,1,1),3) )
# print(util.newNodes(4))
print()
print(util.getParentsBatch([(2,1), (3,1,1)],3) )
