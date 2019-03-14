# some combinatorics first
from six.moves import range


def matrixProduct(a, b):
    return [[sum([a[j][i] * column[j] for j in range(len(a))])
             for i in range(len(a[0]))] for column in b]
#     res=[]
#     a1=len(a[0])
#     a2=len(a)
#     for column in b:
#         cc=[]
#         for i in range(a1):
#             ss=0
#             for j in range(a2):
#                 if column[j]:
#                     ss+=a[j][i]
#             cc.append(ss)
#         res.append(cc)
#     return res
#     import numpy
#     a=numpy.matrix(numpy.array(a))
#     b=numpy.matrix(numpy.array(b))
#     return b*a
# print(matrixProduct([[1,2]],[[0],[1]]))


def putInTable2d(l, func):
    """
    >>> print(putInTable2d(range(40),lambda x:(x%6,x%5)))
    """
    tmp = [func(i) for i in l]

    bounds = []
    for d in range(2):
        mx = -1000
        mn = 1000
        for r in tmp:
            mx = max(r[d], mx)
            mn = min(r[d], mn)
        bounds.append((mn, mx))

    res = [[[] for j in range(bounds[1][1] - bounds[1][0] + 1)]
           for i in range(bounds[0][1] - bounds[0][0] + 1)]
    for i, li in enumerate(l):
        idx0 = tmp[i][0] - bounds[0][0]
        idx1 = tmp[i][1] - bounds[1][0]
        res[idx0][idx1].append(li)

    return (res, bounds)


def golayCode(n):
    """
    print(golayCode(5))
    """
    if n == 0:
        return []
    return golayCode(n - 1) + [n] + golayCode(n - 1)


def golaySign(l):
    rot = [1] * 40
    for e in range(len(l)):
        tmp = l[e] - 1
        l[e] *= rot[tmp]
        rot[tmp] *= -1


golayCache = [golayCode(i) for i in range(2)] + [-1] * 30


for l in golayCache:
    if l != -1:
        golaySign(l)


# print(golayCache[4])
# def multiDim(dim):# incorrect not zero but []!!
#     if len(dim)==1: return [0]*dim[0]
#     tmp=dim[1:]
#     return [multiDim(tmp) for i in range(dim[0])]
# def putInTable(l,func):# incorrect not zero but []!!
#     if len(l)==0: return ([],[])
#     tmp=[func(i) for i in l]
#     dim=len(tmp[0])
#     bounds=[]
#     for d in range(dim):
#         mx=-1000
#         mn=1000
#         for r in tmp:
#             mx=max(r[d],mx)
#             mn=min(r[d],mn)
#         bounds.append((mn,mx))
#     res=multiDim([i[1]-i[0]+1 for i in bounds])
#     for i in range(len(l)):
#         nn=res
#         for d in range(dim-1):
#             nn=nn[tmp[i][d]]
#         nn[tmp[i][dim-1]]=l[i]
#     return (res,bounds)
