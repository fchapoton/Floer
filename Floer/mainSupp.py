from __future__ import absolute_import

from .braid2rect import atlas
from .rectDiagMisc import toStringNice
from .highLevel import AllToString

import time

"""
This is not imported by anything. Maybe just a test file?
"""

print('time:', time.clock())
for i in range(11, 12):
    for j in range(530, 550):
        if (i, j) in atlas:
            rect = atlas[(i, j)]
            print("KNOT:", i, "n", j)
            print(rect)
            print(toStringNice(rect))
            print(AllToString(rect))
print('time:', time.clock())

# i=7  # int(input("knot nb of crossings"))
# j=6  # int(input("knot nb"))
# if (i, j) in atlas:
#     rect = atlas[(i,j)]
#       rect = rect[6:] + rect[:6]
#     print("KNOT:", i, "n", j)
#     print(rect)
#     print(rectDiagMisc.toStringNice(rect))
#     print(bdMapGeneral.AllToString(rect))
