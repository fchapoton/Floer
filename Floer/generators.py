from __future__ import print_function
from six.moves import range

from genGen import genGen
from combinatoric import putInTable2d
import rectDiagMisc


def getShortEllipses(rect):
    ellx = rect[:]
    ellx[0] = -1
    elly = rectDiagMisc.transpose(rect)
    elly[rect[0][0]] = -1
    return (ellx, elly)


def getLargeEllipses(rect):
    n = len(rect)
    ellx = [[0,n-1]]*n
    elly = [[0,n-1]]*n
    ellx[0] = -1
    elly[rect[0][0]]=-1
    return (ellx, elly)


def alexIndexRaw(gen,tab):
    res = 0
    for i in range(len(gen.perm)):
        if gen.perm[i] == -1:
            continue
        res += tab[i+(gen.xShift[i]+1)/2][gen.perm[i]+(gen.yShift[i]+1)/2]
    return res


def alexIndexShift(rect, tab, ell):
    # first the corners
    res = 0
    for x in range(len(rect)):
        for h in rect[x]:
            for d in [[0,0],[0,1],[1,0],[1,1]]:
                res+=tab[x+d[0]][h+d[1]]
    res = res/8.0
    res += (len(rect)-1)/2.0
    return -res + len(rect)-1


def _I(p1, p2):
    res=0
    for j in range(len(p1)):
        for i in range(j):
            if p1[i]!=-1 and p1[i]<p2[j]:
                res+=1
    return res


def maslovIndex(gen,p):  # to check!
    res=0
    for i in range(len(p)):
        for j in range(len(p)):
            if p[j]==-1 or gen.perm[i]==-1:
                continue
            (x,y)=(2*i+gen.xShift[i],2*gen.perm[i]+gen.yShift[i])  # new
            if x<j*2 and y<p[j]*2:
                res+=1
            if x>j*2 and y>p[j]*2:
                res+=1
    return -(_I(gen.perm,gen.perm)-res+_I(p,p))


def maslovTab(p):
    def _M(p,x,y):
        res=0
        for i in range(len(p)):
            if (i<x)==(p[i]<y):
                res+=1
        return res
    return [[_M(p,i,j) for j in range(len(p)+1)] for i in range(len(p)+1)]


def maslovIndex2(gen, tab, ipp):
    res = 0
    for i in range(len(gen.perm)):
        if gen.perm[i] != -1:
            res += tab[i+(gen.xShift[i]+1)//2][gen.perm[i]+(gen.yShift[i]+1)//2]
    return -(gen.maslov + ipp - res)


def classifiedGen(rect, ell, strat=0):
    p1,p2 = rectDiagMisc.recToPermAndComp(rect)[0]
    tabAl = rectDiagMisc.getWindingNbTable(p1, p2)
    print("alexander table:", tabAl)
    AShift = alexIndexShift(rect, tabAl, ell)
    print("alexander Index Shift", AShift)

    tabMas=maslovTab(p1)
    ipp=_I(p1,p1)

    if strat==0:
        (gen,pool)=genGen(ell[0],ell[1])
        print("nb of gens:")
        print(len(gen))
        (gen, bounds) = putInTable2d(gen,lambda x:(alexIndexRaw(x,tabAl)+AShift,maslovIndex2(x,tabMas,ipp)))

    else:
        import gc
        n=len(rect)
        aiml,aimr=0,0
        for i in range(len(tabAl)):
            aiml+=min(tabAl[i])
            aimr+=max(tabAl[i])
        minimum=aiml
        right,left=0,0
        line=[0]*(aimr-aiml+1)
        d=-1
        pool = "no"
        while True:
            gc.collect()
            if d == -1:
                aim = aiml
                aimForIndex = aiml + 1
            else:
                aim = aimr
            (gen,pool)=genGen(ell[0],ell[1],0,(aim,tabAl),pool)
            line[aim-minimum]=gen
            print("raw generators:", aim, len(gen))
            if d==-1:
                aiml+=1
                left=len(gen)
            else:
                aimr-=1
                right=len(gen)
            if aimr-aiml==n-2:
                break
            if left <= right:
                d = -1
            else:
                d = 1
        miniA,maxiA=100000,-100000
        miniM,maxiM=100000,-100000
        for i in range(len(line)):
            if line[i]==0:
                continue
            tmp = len(line[i])
            if tmp:
                miniA = min(minimum+i,miniA)
                maxiA = max(minimum+i,maxiA)
                d = {}
                for e in line[i]:
                    mas = maslovIndex2(e, tabMas, ipp)
                    if mas in d:
                        d[mas].append(e)
                    else:
                        d[mas]=[e]

                keys = list(d)
                if keys:
                    miniM = min(min(keys), miniM)
                    maxiM = max(max(keys), maxiM)
                line[i] = d

        bounds = (miniA + AShift, maxiA + AShift, miniM, maxiM)
        gen = [[[] for j in range(miniM, maxiM + 1)]
               for i in range(miniA, maxiA + 1)]
        for i, a in enumerate(line):
            if a:
                for b in a:
                    gen[i + minimum - miniA][b - miniM] = a[b]
        index = aimForIndex - miniA
    return (gen, bounds, pool, index)


if __name__ == "__main__":
    # rect = [[0,2],[1,3],[0,2],[1,3]]
    rect_trefoil = [[1, 4], [0, 2], [1, 3], [2, 4], [0, 3]]
    classifiedGen(rect_trefoil, 1)
