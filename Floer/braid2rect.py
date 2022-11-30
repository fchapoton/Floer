"""
The file knotAtlas.pic contains a Python pickle for the knot table,
as a dictionary {(n,i): rectangular diagram}

The same data is available in json format in knotAtlasV1.txt.

This is not convenient for use in sage.
"""
from six.moves import range

import pickle

import simplify.diagSimplify


def spaceRect(rect, y):
    for i in range(len(rect)):
        for b in [0, 1]:
            if rect[i][b] >= y:
                rect[i][b] += 1


def spaceColumn(col, y):
    for i, coli in enumerate(col):
        if coli >= y:
            col[i] += 1


def findMax(rect):
    return max(recti[b] for recti in rect for b in [0, 1])


def braidToRect(br, n):
    """
    >>> print(braidToRect([[0, 0], [1, 0]], 2))
    """
    start = list(range(n))
    end = list(range(n))
    rect = []
    for gen in br:
        if gen[0] == 0:
            height = end[gen[1]]
            height2 = end[gen[1] + 1]
            spaceColumn(start, height)
            spaceRect(rect, height)
            rect.append([height, height2 + 1])
            end[gen[1] + 1] = height + 1
            spaceColumn(end, height + 2)
        else:
            spaceColumn(start, end[gen[1] + 1] + 1)
            spaceRect(rect, end[gen[1] + 1] + 1)
            rect.append([end[gen[1]], end[gen[1] + 1] + 1])
            tmp = end[gen[1] + 1]
            spaceColumn(end, tmp)
            end[gen[1]] = tmp
    mx = findMax(rect)
    for i in range(len(start)):
        rect = [[start[len(start) - i - 1], mx + i + 1]] + rect + [[end[len(start) - i - 1], mx + i + 1]]
    return rect


def elim(tab):
    return [e for e in tab if e]


def rdBraid(s):
    tmp = s[1:-1]
    tmp = tmp.split(", ")
    mx = -1
    res = []
    for kk in tmp:
        k = int(kk)
        if k < 0:
            res.append((0, -k - 1))
            mx = max(mx, -k)
        else:
            res.append((1, k - 1))
            mx = max(mx, k)
    return (res, mx + 1)

# ---------- application ----------


def read_from_braid_file():
    with open("braidList.txt", "r") as br:
        rawList = [elim(kn.split(" ")) for kn in br.read().split("\n")]
    atlas = {}

    for kn in rawList:
        tmp = rdBraid(kn[2])
        atlas[(int(kn[0]), int(kn[1]))] = simplify.diagSimplify.simplify(
            braidToRect(tmp[0], tmp[1]), 5000)
        if len(atlas) % 100 == 0:
            print(len(atlas))
    return atlas

#     # the result is the knot dico called atlas!
#     with open("knotAtlas.pic", "wb") as f:
#         pickle.dump(atlas, f)
#     print("Atlas ready")


with open("knotAtlas.pic", "rb") as f:
    atlas = pickle.load(f)

"""
pour reconstruction du fichier knotAtlasV1.txt
"""
# if __name__ == "__main__":
#     s = "{"
#     for i in range(13):
#         for j in range(1, len(atlas) + 1):
#             if (i, j) in atlas:
#                 s += str((i, j)) + ": " + str(atlas[(i, j)]) + ", \n"
#             else:
#                 break
#     s += "}"
#     with open("knotAtlasV1.txt", "w") as av:
#         av.write(s)
