import braid2rect
import rectDiagMisc
import highLevel

import time

print('time:', time.clock())
for i in range(11, 12):
    for j in range(530, 550):
        if (i, j) in braid2rect.atlas:
            rect = braid2rect.atlas[(i, j)]
            print("KNOT:", i, "n", j)
            print(rect)
            print(rectDiagMisc.toStringNice(rect))
            print(highLevel.AllToString(rect))
print('time:', time.clock())

##i=7#int(raw_input("knot nb of crossings"))
##j=6#int(raw_input("knot nb"))
##if braid2rect.atlas.has_key((i,j)):
##    rect=braid2rect.atlas[(i,j)]
####    rect=rect[6:]+rect[:6]
##    print("KNOT:",i,"n",j)
##    print(rect)
##    print(rectDiagMisc.toStringNice(rect))
##    print(bdMapGeneral.AllToString(rect))
####
##raw_input("w")
