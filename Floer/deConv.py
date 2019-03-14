from .homology import getBin

# both function below are unused: duplicate of homology.deconv ?


def deConv(tab, n, s):
    ex = getBin(n)
    ex[0] = 0
    print(ex)
    x, y = len(tab), len(tab[0])
    for k in range(s):
        for i in range(y):
            mul = tab[k][i]
            if mul != 0:
                for j in range(n+1):
                    a = k + j
                    b = i + j
                    if a>=0 and b>=0 and a<x and b<y:
                        tab[a][b]-=ex[j]*mul
    return tab


def deConvSimp(tab, n):
    """
    >>> print(deConvSimp([[0,1,0,0,0],[0,0,3,0,0],[0,0,0,3,0],[0,0,0,0,1]],3))
    >>> print(deConv([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],3,3))
    """
    ex = getBin(n)
    ex[0] = 0
    x, y = len(tab), len(tab[0])
    for k in range(len(tab)):
        for i in range(y):
            mul = tab[k][i]
            if mul != 0:
                for j in range(n + 1):
                    a = k + j
                    b = i + j
                    if a>=0 and b>=0 and a<x and b<y:
                        tab[a][b] -= ex[j] * mul
    return tab
