# -*- coding: utf-8 -*-
try:
    import Tkinter as tkinter
except ImportError:
    import tkinter

from .visu2 import _line


class RectDia(object):
    def __init__(self, tab):
        self.points = []
        for x in tab:
            self.points.append(self.point(x[0], x[1], 0, 0))
        self.isOriented = False
        self._size = len(self.points) // 2

    class point:  # NOT immutable
        def __init__(self, x, y, isO, ori):
            self.x = x
            self.y = y
            if isO:
                self.ori = ori

        def castle(self, i, d, n):
            if d==0:
                if self.x==i:
                    self.x+=1
                else:
                    self.x-=1
            if d==1:
                if self.y==i:
                    self.y+=1
                else:
                    self.y-=1
            self.x %= n
            self.y %= n

        def __inv(self, b):
            if b:
                (self.x, self.y) = (self.y, self.x)

    def copy(self):
        r = RectDia([])
        for p in self.points:
            r.points.append(self.point(p.x, p.y, 0, 0))
        return r

    def size(self):
        """
        half the number of points
        """
        return self._size

    def __iter__(self):
        return ((pt.x, pt.y) for pt in self.points)

    def isCorrectNonOri(self):
        n = self._size
        if len(self.points) % 2:
            return False
        x = [0] * n
        y = [0] * n
        for p in self.points:
            if p.x < 0 or p.y < 0:
                return False
            x[p.x] += 1
            y[p.y] += 1
        return all(x[i] == 2 and y[i] == 2 for i in range(n))

    def orderPoints(self, direction):
        if direction:
            def f(p):
                return p.y
        else:
            def f(p):
                return p.x
        self.points.sort(key=f)

    def ____compact(self, l, d):
        """
        d is a direction

        l is a bound in this direction
        """
        for p in self.points:
            if d == 0 and p.x > l:
                p.x -= 1
            if d == 1 and p.y > l:
                p.y -= 1

    def __compact(self):
        n=100
        x=[0]*n
        y=[0]*n
        for p in self.points:
            x[p.x]+=1
            y[p.y]+=1
        for i in range(n):
            if x[n-1-i]==0:
                self.____compact(n-1-i,0)
            if y[n-1-i]==0:
                self.____compact(n-1-i,1)

    def _contains_(self, xy):
        x, y = xy
        return any(p.x == x and p.y == y for p in self.points)

    def __del(self,x,y):
        for p in self.points:
            if p.x == x and p.y == y:
                self.points.remove(p)
                if self.isOriented:
                    return p.ori

############################# The moves #############################3

    def _unlinked(self, i, j, k, l):
        if i==j or i==k or i==l or j==k or j==l or k==l:
            return 0
        if j<i:
            (i,j)=(j,i)
        if l<k:
            (k,l)=(l,k)
        if (i<k<j and j<l) or (i<l<j and k<i):
            return 0
        return 1

    def m_cycle(self, dx, dy):
        n = self._size
        for p in self.points:
            p.x += dx
            p.y += dy
            if p.x >= n:
                p.x -= n
            if p.y >= n:
                p.y -= n

    def is_castling(self,i,direction):
        n=self._size
        self.orderPoints(direction)
        p1=self.points[2*i]
        p2=self.points[2*i+1]
        if i!=n-1:
            q1=self.points[2*i+2]
            q2=self.points[2*i+3]
        else:
            q1=self.points[0]
            q2=self.points[1]
        d=1-direction
        if direction and self._unlinked(p1.x,p2.x,q1.x,q2.x):
            return True
        if d and self._unlinked(p1.y,p2.y,q1.y,q2.y):
            return True
        return False

    def m_castling(self, i, direction):  # if impossible throws exception
        n = self._size
        self.orderPoints(direction)
        p1=self.points[2*i]
        p2=self.points[2*i+1]
        if i!=n-1:
            q1=self.points[2*i+2]
            q2=self.points[2*i+3]
        else:
            q1=self.points[0]
            q2=self.points[1]
        d=1-direction
        if direction and not self._unlinked(p1.x,p2.x,q1.x,q2.x):
            raise RuntimeError
        if d and not self._unlinked(p1.y,p2.y,q1.y,q2.y):
            raise RuntimeError
        p1.castle(i, direction, n)
        p2.castle(i, direction, n)
        q1.castle(i, direction, n)
        q2.castle(i, direction, n)

    def is_stabilisation(self):
        n = self._size
        for p in self.points:
            if p.x == p.y and n == 1 + p.x:
                return True
        return False

    def m_stabilisation(self,kind):
        if not self.is_stabilisation(kind):
            raise ValueError
        n=self._size-1
        ori = 0
        if kind==0:
            for p in self.points:
                if p.x==p.y and p.x==n:
                    if self.isOriented:
                        ori=p.ori
                    self.points.remove(p)
                    break
            self.points+=[self.point(n,n+1,self.isOriented,ori),self.point(n+1,n,self.isOriented,ori),self.point(n+1,n+1,self.isOriented,1-ori)]
        if kind==1 or kind==2:
            i=-1
            for p in self.points:
                if kind==2 and p.x==n and p.y!=n or kind==1 and p.y==n and p.x!=n:
                    if kind==2:
                        i=p.y
                    else:
                        i=p.x
                    if self.isOriented:
                        ori=p.ori
                    self.points.remove(p)
                    break
            self.points+=[self.point(i,n+1,self.isOriented,ori).__inv(kind-1)]
            self.points+=[self.point(n+1,n+1,self.isOriented,ori).__inv(kind-1)]
            self.points+=[self.point(n+1,n,self.isOriented,1-ori).__inv(kind-1)]
        if kind==3:
            i=-1
            j=-1
            for p in self.points:
                if self.isOriented and p.x==n and p.y!=n:
                    p.ori=1-p.ori
                if p.x==n and p.y!=n:
                    i=p.y
                    if self.isOriented:
                        ori=p.ori
                    self.points.remove(p)
                if p.y==n and p.x!=n:
                    j=p.x
                    self.points.remove(p)
            self.points+=[self.point(i,n+1,self.isOriented,ori)]
            self.points+=[self.point(n+1,j,self.isOriented,ori)]
            self.points+=[self.point(n,n+1,self.isOriented,1-ori)]
            self.points+=[self.point(n+1,n,self.isOriented,1-ori)]

    def is_destabilisation(self):
        n = self._size - 1
        nn = (n, n) in self
        mn = (n - 1, n) in self
        nm = (n, n - 1) in self
        mm = (n - 1, n - 1) in self
        if mn and nm and nn and (not mm):
            return 0
        if mm and mn and nn and (not nm):
            return 1
        if mm and nm and nn and (not mn):
            return 2
        if mm and mn and nm and (not nn):
            return 3
        return -1

    def m_destabilisation(self, kind):  # use following is_desta
        n = self._size - 1
        if kind==0:
            self.__del(n,n)
            self.__del(n-1,n)
            ori=self.__del(n,n-1)
            self.points+=[self.point(n-1,n-1,self.isOriented,ori)]
        if kind==1:
            self.__del(n,n)
            self.__del(n-1,n)
        if kind==2:
            self.__del(n,n)
            self.__del(n,n-1)
        if kind==3:
            self.__del(n,n-1)
            self.__del(n-1,n)
            if self.isOriented:
                for p in self.points:
                    if p.x==n and p.y==n:
                        p.ori=1-p.ori
        for p in self.points:
            if p.x==n:
                p.x-=1
            if p.y==n:
                p.y-=1

    def __hash__(self):
        """
        a "perfect" hash function
        """
        n = self._size
        res = 0
        self.orderPoints(1)
        self.orderPoints(0)
        for i in range(2 * n):
            res *= n
            res += self.points[i].y
        return (res * 2 + 1) * pow(2, n)

#######################building lists of successors by the moves

    def succCy(self):
        succ = []
        for i in range(self._size):
            for j in range(self._size):
                tmp=self.copy()
                tmp.m_cycle(i,j)
                succ.append(tmp)
        return succ

    def succCa(self):
        succ = []
        for d in range(2):
            for i in range(self._size):
                tmp = self.copy()
                if tmp.is_castling(i, d):
                    tmp.m_castling(i, d)
                    succ.append(tmp)
        return succ

    def succDe(self):
        succ = []
        tmpp = self.is_destabilisation()
        if tmpp != -1:
            tmp = self.copy()
            tmp.m_destabilisation(tmpp)
            succ.append(tmp)
        return succ

    def succTrDe(self):
        succ = []
        n=self._size
        for k in self.points:
            tmp=self.copy()
            tmp.m_cycle(n-1-k.x,n-1-k.y)
            s=tmp.is_destabilisation()
            if s!=-1:
                tmp.m_destabilisation(s)
                succ.append(tmp)
        return succ

    def succSt(self):
        succ=[]
        if self.is_stabilisation():
            for d in range(4):
                tmp=self.copy()
                tmp.m_stabilisation(d)
                succ.append(tmp)
        return succ

    def successors(self):
        return self.succCy() + self.succCa() + self.succDe() + self.succSt()
##Flipe-move part##################################

    def _fetch(self, x, y, dx, dy):
        return [p for p in self.points
                if x <= p.x < x + dx and y <= p.y < y + dy]

    def __hasNoneDiag(self, x, y, s):
        return not any(x <= p.x < x + s and y <= p.y < y + s and
                       p.x - x != p.y - y
                       for p in self.points)

    def __hasFullDiag(self,x,y,s):
        n=self._size
        d=[-1]*min(min(n-x,n-y),s)
        for p in self.points:
            if p.x>=x and p.y>=y and p.x<x+s and p.y<y+s:
                if p.x-x==p.y-y:
                    d[p.x-x]=1
                else:
                    return 0
        if d.count(-1)==0:
            return 1
        else:
            return 0

##    def __count(self,l,x,d)
##        tot=0
##        for p in l:
##            if (p.x==x and d==0) or (p.y==y and d==1):tot+=1
##        return tot

    def is_flipe(self, a, b):
        if self.__hasFullDiag(0,b,a) and self.__hasFullDiag(0,a,b):
            if len(self._fetch(a,b,b,a))==0:
                return 1
        return 0

    def m_flipe(self,a,b):
        flipped=self._fetch(0,0,a,b)
        dx=[0]*self._size
        dy=[0]*self._size
        for p in flipped:
            dx[p.x]+=1
            dy[p.y]+=1
        aList=self._fetch(0,b,a,a)
        bList=self._fetch(a,0,b,b)
        aListX=[p.x for p in aList]
        bListY=[p.y for p in bList]
        for p in flipped:
            if dx[p.x]!=2 and aListX.count(p.x)==0:
                self.points.append(self.point(p.x,b+p.x,0,0))
            else:
                self.__del(p.x,b+p.x)
            if dy[p.y]!=2 and bListY.count(p.y)==0:
                self.points.append(self.point(a+p.y,p.y,0,0))
            else:
                self.__del(a+p.y,p.y)

            (p.x,p.y)=(a+p.y,b+p.x)
        self.__compact()

    def _rotate(self):
        n = self._size
        for p in self.points:
            p.x, p.y = n - 1 - p.y, p.x

    def succfl(self):
        succ = []
        n = self._size
        for r in range(4):
            for i in range(n):
                for j in range(n):
                    for a in range(1, n + 1):  # 3too small!!
                        for b in range(1,n+1):
                            tmp=self.copy()
                            tmp.m_cycle(i,j)
                            if tmp.is_flipe(a,b):
                                tmp.m_flipe(a,b)
                                succ.append(tmp)
            self._rotate()
        return succ

    def draw(self):
        """
        Depict the link in a graphical style.

        In [5]: d = RectDia([(0,0),(2,0),(0,2),(2,2),(1,1),(1,3),(3,1),(3,3)])
        In [6]: d.draw()
        """
        root = tkinter.Tk()
        fig = tkinter.Canvas(root, width=800, height=800)
        fig.pack()

        n = self.size()
        dist = 500 / n

        self.orderPoints(1)
        self.orderPoints(0)  # the sort is order preserving for equals!!
        for x in range(n):
            _line(self.points[2*x].x, self.points[2*x].y,
                  self.points[2*x+1].x, self.points[2*x+1].y, dist, fig)

        self.orderPoints(0)
        self.orderPoints(1)  # the sort is order preserving for equals!!
        for x in range(n):
            _line(self.points[2*x].x, self.points[2*x].y,
                  self.points[2*x+1].x, self.points[2*x+1].y, dist, fig)

        root.mainloop()

    def fromOlink(self, link):
        """
        construction from an oriented link ?
        """
        tangle = link.word
        print(tangle)
        points = []
        section = [-1,1]
        forbidden = [-1,1]

        def findFree(s,e):
            x=(s+e)/2.0
            while True:
                x=(s+x)/2.0
                if forbidden.count(x)==0:
                    return x
        levelCounter=0
        for level in tangle:
            if level[0]==3:
                points.append((section[level[1]+1],levelCounter))
                points.append((section[level[1]+2],levelCounter))
                section[level[1]+1:level[1]+3]=[]
            if level[0]==2:
                tmp1=findFree(section[level[1]],section[level[1]+1])
                tmp2=findFree(tmp1,section[level[1]+1])
                points.append((tmp1,levelCounter))
                points.append((tmp2,levelCounter))
                forbidden+=[tmp1,tmp2]
                section[level[1]+1:level[1]+1]=[tmp1,tmp2]
            if level[0]==0:
                tmp1=findFree(section[level[1]+2],section[level[1]+3])
                points.append((tmp1,levelCounter))
                points.append((section[level[1]+1],levelCounter))
                forbidden+=[tmp1]
                section[level[1]+3:level[1]+3]=[tmp1]
                section[level[1]+1:level[1]+2]=[]
            if level[0]==1:
                tmp1=findFree(section[level[1]],section[level[1]+1])
                points.append((tmp1,levelCounter))
                points.append((section[level[1]+2],levelCounter))
                forbidden+=[tmp1]
                section[level[1]+2:level[1]+3]=[]
                section[level[1]+1:level[1]+1]=[tmp1]
            levelCounter+=1
        forbidden.sort()
        print(points)
        self.points=[]
        for x in range(len(forbidden)):
            for p in points:
                if(p[0]==forbidden[x]):
                    self.points.append(self.point(x-1,p[1],0,0))

    def toStringNice(self):
        """
        dd0 = RectDia([(0,0),(0,3),(1,1),(1,2),(2,2),(2,3),(3,0),(3,1)])
        dd1 = RectDia([(0,0),(0,1),(1,0),(1,2),(2,2),(2,1)])
        dd2 = RectDia([(1,0),(0,1),(2,0),(0,2),(1,2),(2,1)])
        dd = RectDia([(2,0),(1,1),(0,2),(0,4),(1,3),(2,2),(3,1),(4,0),(4,3),(3,4)])

        In [8]: d = RectDia([(0,0),(2,0),(0,2),(2,2),(1,1),(1,3),(3,1),(3,3)])
        In [9]: print(d.toStringNice())
        o-o 
        |o+o
        o+o|
         o-o
        """
        self.orderPoints(1)
        n = self._size
        tab = [[" "] * n for _ in range(n)]
        for x, y in self:
            tab[y][x] = "o"
        for i in range(n):
            for j in range(self.points[2*i].x + 1, self.points[2*i+1].x):
                tab[i][j] = u"─"
        self.orderPoints(0)
        for i in range(n):
            for j in range(self.points[2*i].y + 1, self.points[2*i+1].y):
                if tab[j][i] == u"─":
                    tab[j][i] = u"┼"
                else:
                    tab[j][i] = u"│"

        s = ''
        for i in range(n):
            s += ''.join(tab[i])
            s += "\n"
        return s

    __repr__ = toStringNice
