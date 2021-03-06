from __future__ import absolute_import

from . import fastUnknot2


def toPoints(rDiag):
    res = []
    for dd in range(len(rDiag)):
        res.append((dd, rDiag[dd][0]))
        res.append((dd, rDiag[dd][1]))
    return res


def makePairs(r):
    return [[r[2 * i], r[2 * i + 1]] for i in range(len(r) // 2)]


def simplify(rect, bd):
    return makePairs(fastUnknot2.unknot(toPoints(rect), bd)[1].xSorted)


def simplifyPoints(rect, bd):
    return makePairs(fastUnknot2.unknot(rect, bd)[1].xSorted)
