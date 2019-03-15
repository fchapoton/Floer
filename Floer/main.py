import six

from highLevel import AllToString
from rectDiagMisc import toStringNice
from braid2rect import atlas
import simplify.diagSimplify


if six.PY2:
    input = raw_input

print("""
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Floer version 0.1   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
""")
s = ""
while s != "y" and s != "n":
    s = input("""Do you want to enter a knot:
(y) by its rectangular diagram ?
(n) by its table location (for knots with at most 12 crossings) ?
Please answer (y/n): """)

if s == "n":
    i = int(input("knot number of crossings: "))
    j = int(input("knot number: "))
    if (i, j) in atlas:
        rect = atlas[(i, j)]
        print("KNOT: ", i, "n", j)
        print(rect)
        print(toStringNice(rect))
        print(AllToString(rect))
    else:
        raise ValueError("not in the knot table")
else:
    print("Please enter the rectangular diagram as a list of pairs of coordinates:")
    print("(example: [[0,0],[0,1],[1,0],[1,1]] is the trivial knot (the 4 corners of a rectangle))")
    s = input("")
    rect = eval(s)
    print("How hard do you want the program to try to simplify your rectangular diagram?(0-100000) 0: no simplification 5000: pretty good compromise")
    print("Warning! The running time of the program is not linear in this number!")
    br = int(input(""))

    if br != 0:
        rect = simplify.diagSimplify.simplifyPoints(rect, br)
    print(toStringNice(rect))
    print(AllToString(rect))
