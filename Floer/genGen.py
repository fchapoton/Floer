from six.moves import range


def genPseudogen(ellx, elly):
    """
    # ell is a list of pairs representing
    # width of ellipses,in ellx [a,b] means a<y<b, not a<y<=b!!!
    """
    pool = [[]]
    for i in range(len(ellx)):
        if ellx[i] == -1:
            for g in pool:
                g.append(-1)
            continue
        tmp = []
        for j in range(ellx[i][0], ellx[i][1] + 1):
            if elly[j] != -1 and elly[j][0] <= i and elly[j][1] + 1 > i:
                for g in pool:
                    if g.count(j) == 0:
                        tmp.append(g + [j])
        pool = tmp
    return pool

# second I gen "shifts of permutation


class gen:
    def __init__(self, perm, xShift, yShift, premas):
        self.perm = perm
        self.xShift, self.yShift, self.maslov = xShift, yShift, premas

    def show(self):
        s = ""
        for k in range(len(self.perm)):
            s += str((self.perm[k], self.xShift[k], self.yShift[k]))
        print(s)
        print(self.perm, self.xShift, self.yShift)

    def toString(self):
        return str(self.perm)+","+str(self.xShift)+","+str(self.yShift)


def _genShifts2(g,poss,i,premas,tab,alex):
    nn = 1
    l = 0
    for i in poss:
        for j in i:
            if len(j) == 2:
                l += 1
                nn *= 2
    res = []
    le = len(g)
    for i in range(nn):
        k = 0
        xShift = [0] * le
        yShift = [0] * le
        for v in poss:
            if len(v[0]) == 2:
                xShift[k] = v[0][i & 1]
                i>>=1
            else:
                xShift[k] = v[0][0]
            if len(v[1]) == 2:
                yShift[k] = v[1][i & 1]
                i>>=1
            else:
                yShift[k] = v[1][0]
            k += 1

        val = 0
        # WRONG TO USE i AGAIN!
        for i in range(le):
            if g[i]==-1:
                continue
            val += tab[i+(xShift[i]+1) // 2][g[i]+(yShift[i]+1) // 2]
        if val == alex:
            res.append(gen(g, xShift, yShift, premas))
    return res


def _I(p1, p2):
    res = 0
    for j in range(len(p1)):
        for i in range(j):
            if p1[i]!=-1 and p1[i] < p2[j]:
                res += 1
    return res


def genGen(ellx, elly, counting=0, alex="no", pool="no"):
    """
    tmp=genGen([[2, 8], [0, 3], [6, 10], [5, 7], [6, 9], [1, 8], [2, 9], [1, 4], [5, 10], [3, 7], -1],
    [[1, 10], [5, 7], [0, 6], [1, 9], -1, [3, 8], [2, 4], [3, 9], [0, 5], [4, 6], [2, 8]],0)
    """
    if pool == "no":
        pool = genPseudogen(ellx,elly)
    n = len(ellx)
    if alex == "no":
        alex, tab=0,[[0]*(n+1)]*(n+1)
    else:
        alex, tab=alex[0], alex[1]
    res = []
    count = 0
    for c in range(len(pool)):
        g = pool[c]
        premas=_I(g,g)
        poss = [0]*n
        for i in range(n):
            if g[i] == -1:
                poss[i]=[[0],[0]]
                continue
            (x,y) = (i,g[i])
            boo = 0
            if (y==ellx[x][0] or y==ellx[x][1]):
                if y==ellx[x][0]:
                    poss[i]=[[1]]
                else:
                    poss[i]=[[-1]]
                boo=1
            else:
                poss[i]=[[1,-1]]
            if boo==0 and (x==elly[y][0] or x==elly[y][1]):
                if x==elly[y][0]:
                    poss[i]+=[[1]]
                else:
                    poss[i]+=[[-1]]
            else:
                poss[i]+=[[1,-1]]
            (poss[i][0],poss[i][1])=(poss[i][1],poss[i][0])
        nn = 1
        for i in poss:
            for j in i:
                if len(j) == 2:
                    nn *= 2
        count += nn

        if counting == 0:
            update=_genShifts2(g, poss, n, premas, tab, alex)
            for i in range(len(update)):
                update[i].psNb = c
            res.extend(update)

    if counting == 1:
        return count
    return (res, pool)
