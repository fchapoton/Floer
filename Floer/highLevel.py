# psyco is obsolete (try cython?)
# import psyco
# psyco.log()
# psyco.full()

import time

import generators
from braid2rect import atlas
import homology
import getOptiEllipses
from homology import transpose
import rectDiagMisc
from bdMapGeneral import (hdEllipsesGen, hdCond, hdCond2, preparePath,
                          deepBdMap2, bdMapPsgenCache, fillFValue, bdMap, categ)


def getKnotFloerHomology(rect):
    """
    INPUT:

    a grid diagram ?
    """
    ellCandidate = getOptiEllipses.simple(rect, 1)
    print(ellCandidate)
    tmp = ellCandidate.pop()
    rect = tmp[3]
    print(rect)
    ell = (tmp[1], tmp[2])
    print("ellipses:")
    print(ell)
    print("score:", tmp[0])
    print("new Diagram:")
    print(rectDiagMisc.toStringNice(rect))
    tmp, b, pool, index = generators.classifiedGen(rect, ell, 1)
    print("index", index)
    print("Scale:A and M: ",b)
    print("Generators, tabulated by Maslov and Alexander grading:")

    transposed = transpose(tmp)

    def format(s, l):
        if len(s) < l:
            return " " * (l - len(s)) + s
        return s

    for i in transposed:
        s = ""
        for j in i:
            s += format(str(len(j)),6)+" "
        print(s)
    # the bdMap stuff
    HDEll=hdEllipsesGen(ell[0],ell[1])
    (to0,toPlus,chEll)=hdCond(rect,HDEll)
    delta=hdCond2(rect,HDEll,to0,toPlus)
    path=preparePath(rect,ell)
    print("path", path)
    # the deepBd stuff
    init=deepBdMap2.initWith(rect,ell)


    #     def eulerP(tab):
    #         k=[0]*(len(tab[0]))
    #         for i in range(len(tab[0])):
    #             tot=0
    #             for j in range(len(tab)):
    #                 tot=len(tab[j][i])-tot
    #             k[i]=tot
    #         return k
    #     print(eulerP(tmp))
    cache = bdMapPsgenCache(rect, ell, pool)
    fillFValue(tmp,cache,ell,to0,toPlus,chEll,delta)
    # new# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #         cache2=bdMapGolay.bdMapPsgenCache(rect,ell,pool)
    #     a=raw_input("w")
    tmp2 = homology.chain2DToHomv3(tmp,lambda x,y:bdMap(rect,x,y,cache,ell,to0,toPlus,chEll,delta,path,init),len(rect)-1,index)

    return transpose(tmp2)


def AllToString(rect):
    #     import profile
    #     profile.run("tmp2=getKnotFloerHomology(rect)")
    #     from trace import Trace
    #     tracer=Trace(count=1, trace=0, countfuncs=1, countcallers=1)
    #     tracer.run("tmp2=getKnotFloerHomology(rect)")
    #     r = tracer.results()
    #     r.write_results()
    tmp2 = getKnotFloerHomology(rect)
    print("HFK:")

    def format(s, l):
        if len(s) < l:
            return " " * (l - len(s)) + s
        return s
    st = ''
    for i in tmp2:
        s = ""
        for j in i:
            s += format(str(j), 5) + " "
        st += s + "\n"
    return st

# # # # # # # # # # # # # # # # # # # #  debug # # # # # # # # # # # #


if __name__ == "__main__":
    rect0 = [[1,4],[0,2],[1,3],[2,4],[0,3]]  # treefoil
    rect1 = [[3,6],[4,8],[0,2],[1,7],[0,5],[3,8],[2,6],[1,5],[4,7]]#16 crossings
    rect2 = [[1,3],[2,5],[0,4],[0,3],[2,4],[1,5]]
    rect3 = [[2,4],[3,6],[0,6],[0,5],[1,4],[1,5],[2,3]]  # big unknot
    rect4 = [[1,5],[0,2],[1,4],[3,5],[2,4],[0,3]]
    rect5 = [[0,1],[0,1]]
    rect6 = [[5,7],[3,6],[2,5],[1,4],[0,3],[2,6],[1,7],[0,4]]  # 8_19
    rect7 = [[0,4],[3,6],[2,5],[1,3],[4,7],[2,6],[0,5],[1,7]]  # 8_20
    rect8 = [[0,3],[1,14],[0,2],[1,9],[3,11],[2,10],[4,7],[6,9],
             [5,8],[7,12],[11,14],[10,13],[6,12],[4,8],[5,13]]
    rect9 = [[0,3],[1,13],[0,2],[1,6],[3,10],[2,9],
             [5,8],[7,11],[10,13],[9,12],[6,11],[4,8],[5,12],[4,7]]

    rect_a = [[0,2],[1,3],[2,5],[1,4],[3,5],[0,4]]
    rect_b = [[1,6],[0,2],[1,4],[0,3],[2,5],[4,7],[6,8],[5,7],[3,8]]
    rect_c = [[0,1],[0,1]]
    rect_d = [[0,13],[9,11],[5,7],[6,10],[9,12],[11,13],[5,8],
              [7,10],[1,3],[2,6],[1,4],[3,8],[4,12],[0,2]]

    rect_e = atlas[(12,1291)]
    rect_f = atlas[(11,370)]  # 90s about
    rect_g = atlas[(9,15)]
    rect = atlas[(11,418)]  # has a multi domain!

    print(rectDiagMisc.toStringNice(rect))
    print(rect)

    startTime = time.clock()
    print(AllToString(rect))
    print("categ:", categ)
    print("dpM2:", deepBdMap2.debug)
    print("Duration:", time.clock() - startTime)
