from six.moves import range

from generators import classifiedGen
from homology import chain2DToHomv2


# boundary map
def isRectPunc(diag, ax, ay, bx, by):
    for i in range(ax, bx):
        if ay <= diag[i][0] < by:
            return True
        if ay <= diag[i][1] < by:
            return True
    return False


def isRectGen(gen, a, b):
    """
    gen is is before the map!
    a < b
    """
    y1 = gen.perm[a]
    y2 = gen.perm[b]
    for i in range(a + 1, b):
        if y1 < gen.perm[i] < y2:
            return True
    return False


def isBndryLargeEll(rect, gen1, gen2):
    """
    rect = [[0, 1], [0, 2], [1, 2]]

    a = gen([-1, 4, 3, 0, 2], [0, -1, -1, 1, -1], [0, 1, 1, 1, -1])
    b = gen([-1, 4, 3, 0, 2], [0, -1, 1, 1, -1], [0, 1, 1, 1, -1])
    print(isBndryLargeEll(rect, a, b))
    """
    n = len(gen1.perm)
    diff = []
    for i in range(n):
        if gen1.perm[i] != gen2.perm[i]:
            diff.append(i)
    l = len(diff)
    if l > 2:
        return False
    elif l == 0:
        diffxs = []
        diffys = []
        for i in range(n):
            if gen1.xShift[i] != gen2.xShift[i]:
                diffxs.append(i)
            if gen1.yShift[i] != gen2.yShift[i]:
                diffys.append(i)
        if len(diffxs) + len(diffys) != 1:
            return False

        if len(diffxs) == 1:
            delta = diffxs[0]
            y = gen1.perm[delta] + (gen1.yShift[delta] + 1) / 2
            return ((y > rect[delta][1] and gen1.xShift[delta] < gen2.xShift[delta]) or
                    (y <= rect[delta][0] and gen1.xShift[delta] > gen2.xShift[delta]))
        else:
            xx = []
            delta = diffys[0]
            for i in range(n):
                if rect[i][0] == gen1.perm[delta] or rect[i][1] == gen1.perm[delta]:
                    xx.append(i)
            x = delta + (gen1.xShift[delta] + 1) / 2
            return ((x <= xx[0] and gen1.yShift[delta] > gen2.yShift[delta]) or
                    (x > xx[1] and gen1.yShift[delta] < gen2.yShift[delta]))

    elif l == 2:
        if gen1.perm[diff[0]] > gen1.perm[diff[1]]:
            return False
        for i in range(n):
            if gen1.xShift[i] != gen2.xShift[i] or gen1.yShift[i] != gen2.yShift[i]:
                if i != diff[0] and i != diff[1]:
                    return False
        a, b = diff
        if (gen1.xShift[a] != gen2.xShift[a] or gen1.xShift[b] != gen2.xShift[b] or
                gen1.yShift[a] != gen2.yShift[b] or gen2.yShift[a] != gen1.yShift[b]):
            return False
        if isRectGen(gen1, a, b) or isRectPunc(rect, a + (gen1.xShift[a] + 1) / 2,
                                               gen1.perm[a] + (gen1.yShift[a] + 1) / 2,
                                               b + (gen1.xShift[b] + 1) / 2,
                                               gen1.perm[b] + (gen1.yShift[b] + 1) / 2):
            return False
        return True
    elif l == 1:
        raise RuntimeError("1 of diff")
    raise RuntimeError("error in boundary")


if __name__ == "__main__":
    rect0 = [[0, 2], [1, 3], [0, 2], [1, 3]]
    rect1 = [[0, 2], [1, 3], [0, 2], [1, 3]]
    rect2 = [[0, 1], [0, 1]]

    rect = [[1, 4], [0, 2], [1, 3], [2, 4], [0, 3]]

    tmp = classifiedGen(rect, 0)[0]
    print("second phase")
    tmp = chain2DToHomv2(tmp, lambda x, y: isBndryLargeEll(rect, x, y))

    def format(s, l):
        if len(s) < l:
            return " " * (l - len(s)) + s
        return s

    for i in tmp:
        s = ""
        for j in i:
            s += format(str(j), 5) + " "
        print(s)
