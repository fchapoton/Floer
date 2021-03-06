from __future__ import absolute_import

from six.moves import range

from .RectDia import RectDia

import copy


def sign(x):
    return -1 if x < 0 else 1


class FastRectDiag:
    def __init__(self, tab):
        if isinstance(tab, RectDia):
            tab = [(p.x, p.y) for p in tab.points]
        self.predecessor = 0
        self.complexity = len(tab) // 2
        self.xSorted = []
        self.ySorted = []
        for i in range(self.complexity):
            self.xSorted += [-1, -1]
            self.ySorted += [-1, -1]
        for p in tab:
            if self.xSorted[p[0] * 2 + 0] == -1:
                self.xSorted[p[0] * 2 + 0] = p[1]
            else:
                if p[1] > self.xSorted[p[0] * 2 + 0]:
                    self.xSorted[p[0] * 2 + 1] = p[1]
                else:
                    (self.xSorted[p[0] * 2 + 0], self.xSorted[p[0] * 2 + 1]) = (p[1], self.xSorted[p[0] * 2 + 0])
            if self.ySorted[p[1] * 2 + 0] == -1:
                self.ySorted[p[1] * 2 + 0] = p[0]
            else:
                if p[0] > self.ySorted[p[1] * 2 + 0]:
                    self.ySorted[p[1] * 2 + 1] = p[0]
                else:
                    (self.ySorted[p[1] * 2 + 0], self.ySorted[p[1] * 2 + 1]) = (p[0], self.ySorted[p[1] * 2 + 0])

    def copy(self):
        h = copy.copy(self)
        h.xSorted = h.xSorted[:]
        h.ySorted = h.ySorted[:]
        return h

    def __repr__(self):
        return repr(self.toRectDia())

    def order(self):
        for i in range(self.complexity):
            if self.xSorted[2 * i] > self.xSorted[2 * i + 1]:
                (self.xSorted[2 * i], self.xSorted[2 * i + 1]) = (self.xSorted[2 * i + 1], self.xSorted[2 * i])
            if self.ySorted[2 * i] > self.ySorted[2 * i + 1]:
                (self.ySorted[2 * i], self.ySorted[2 * i + 1]) = (self.ySorted[2 * i + 1], self.ySorted[2 * i])

    def xySorted(self, tab):
        a = [-1] * (2 * self.complexity)
        for i in range(2 * self.complexity):
            o = tab[i]
            if a[2 * o] == -1:
                a[2 * o] = i // 2
            else:
                a[2 * o + 1] = i // 2
        return a

    def size(self):
        return self.complexity

    def _areUnlinked2(self, i, j, k, l):
        """
        pas bien efficace sans doute
        """
        return sign(k - i) * sign(j - k) * sign(l - i) * sign(j - l) > 0

    def castleX(self, nb):
        N = self.complexity
        tmp11 = self.xSorted[nb * 2]
        tmp12 = self.xSorted[nb * 2 + 1]
        tmp21 = self.xSorted[(nb + 1) % N * 2]
        tmp22 = self.xSorted[(nb + 1) % N * 2 + 1]
        if self.ySorted[tmp11 * 2] == nb:
            self.ySorted[tmp11 * 2] = (nb + 1) % N
        else:
            self.ySorted[tmp11 * 2 + 1] = (nb + 1) % N
        if self.ySorted[tmp12 * 2] == nb:
            self.ySorted[tmp12 * 2] = (nb + 1) % N
        else:
            self.ySorted[tmp12 * 2 + 1] = (nb + 1) % N
        if self.ySorted[tmp21 * 2] == (nb + 1) % N:
            self.ySorted[tmp21 * 2] = nb
        else:
            self.ySorted[tmp21 * 2 + 1] = nb
        if self.ySorted[tmp22 * 2] == (nb + 1) % N:
            self.ySorted[tmp22 * 2] = nb
        else:
            self.ySorted[tmp22 * 2 + 1] = nb
        (self.xSorted[nb * 2], self.xSorted[(nb + 1) % N * 2]) = (self.xSorted[(nb + 1) % N * 2], self.xSorted[nb * 2])
        (self.xSorted[nb * 2 + 1], self.xSorted[(nb + 1) % N * 2 + 1]) = (self.xSorted[(nb + 1) % N * 2 + 1], self.xSorted[nb * 2 + 1])
        return self

    def castleY(self, nb):
        N = self.complexity
        tmp11 = self.ySorted[nb * 2]
        tmp12 = self.ySorted[nb * 2 + 1]
        tmp21 = self.ySorted[(nb + 1) % N * 2]
        tmp22 = self.ySorted[(nb + 1) % N * 2 + 1]
        if self.xSorted[tmp11 * 2] == nb:
            self.xSorted[tmp11 * 2] = (nb + 1) % N
        else:
            self.xSorted[tmp11 * 2 + 1] = (nb + 1) % N
        if self.xSorted[tmp12 * 2] == nb:
            self.xSorted[tmp12 * 2] = (nb + 1) % N
        else:
            self.xSorted[tmp12 * 2 + 1] = (nb + 1) % N

        if self.xSorted[tmp21 * 2] == (nb + 1) % N:
            self.xSorted[tmp21 * 2] = nb
        else:
            self.xSorted[tmp21 * 2 + 1] = nb
        if self.xSorted[tmp22 * 2] == (nb + 1) % N:
            self.xSorted[tmp22 * 2] = nb
        else:
            self.xSorted[tmp22 * 2 + 1] = nb
        (self.ySorted[nb * 2], self.ySorted[(nb + 1) % N * 2]) = (self.ySorted[(nb + 1) % N * 2], self.ySorted[nb * 2])
        (self.ySorted[nb * 2 + 1], self.ySorted[(nb + 1) % N * 2 + 1]) = (self.ySorted[(nb + 1) % N * 2 + 1], self.ySorted[nb * 2 + 1])
        return self

    def castle(self, nb, direction):
        N = self.complexity
        if direction:
            if self._areUnlinked2(self.ySorted[(nb + 1) % N * 2],
                                  self.ySorted[(nb + 1) % N * 2 + 1],
                                  self.ySorted[nb * 2], self.ySorted[nb * 2 + 1]):
                return self.castleY(nb)

        else:
            if self._areUnlinked2(self.xSorted[(nb + 1) % N * 2],
                                  self.xSorted[(nb + 1) % N * 2 + 1],
                                  self.xSorted[nb * 2], self.xSorted[nb * 2 + 1]):
                return self.castleX(nb)
        return 0

    def isCastle(self, nb, direction):
        N = self.complexity
        if direction:
            return self._areUnlinked2(self.ySorted[(nb + 1) % N * 2],
                                      self.ySorted[(nb + 1) % N * 2 + 1],
                                      self.ySorted[nb * 2], self.ySorted[nb * 2 + 1])
        else:
            return self._areUnlinked2(self.xSorted[(nb + 1) % N * 2],
                                      self.xSorted[(nb + 1) % N * 2 + 1],
                                      self.xSorted[nb * 2], self.xSorted[nb * 2 + 1])

    def __has(self, x, y):
        return self.xSorted[x * 2] == y or self.xSorted[x * 2 + 1] == y

    def isdestabilisation(self, x, y):
        nn = self.__has(x, y)
        mn = self.__has((x - 1) % self.complexity, y)
        nm = self.__has(x, (y - 1) % self.complexity)
        mm = self.__has((x - 1) % self.complexity, (y - 1) % self.complexity)
        if mn and nm and nn and (not mm):
            return 0
        if mm and mn and nn and (not nm):
            return 1
        if mm and nm and nn and (not mn):
            return 2
        if mm and mn and nm and (not nn):
            return 3
        return -1

    def isdestabilisable(self):
        self.order()
        for x in range(self.complexity):
            if self.ySorted[x * 2 + 1] - self.ySorted[x * 2] == 1:
                return (1, x)
            if self.xSorted[x * 2 + 1] - self.xSorted[x * 2] == 1:
                return (0, x)
        return 0

    def _areUnlinked3(self, a, b, d):
        if d == 0:
            return self._areUnlinked2(self.xSorted[a * 2],
                                      self.xSorted[a * 2 + 1],
                                      self.xSorted[b * 2],
                                      self.xSorted[b * 2 + 1])
        else:
            return self._areUnlinked2(self.ySorted[a * 2],
                                      self.ySorted[a * 2 + 1],
                                      self.ySorted[b * 2],
                                      self.ySorted[b * 2 + 1])

    def chainCastle(self, a, b, d):
        tmp = self
        if a > b:
            b += self.complexity
        interval = b - a - 1
        for i in range(interval):
            tmp, tmp.predecessor = tmp.copy(), tmp
            if tmp._areUnlinked3(a % self.complexity,
                                 (a + 1) % self.complexity, d):
                tmp.castle(a % self.complexity, d)
                a = (a + 1) % self.complexity
            else:
                tmp.castle((b - 1) % self.complexity, d)
                b = (b - 1) % self.complexity
        if a == self.complexity - 1:
            tmp, tmp.predecessor = tmp.copy(), tmp
            tmp.cycle(d)
        return tmp

    def isdestabilisableAdvanced(self):
        if self.isdestabilisable():
            return 0
        self.order()
        fw = [0] * self.complexity
        bw = [0] * self.complexity
        for d in (0, 1):
            for i in range(self.complexity):
                n = 1
                while self._areUnlinked3(i, (i + n) % self.complexity, d):
                    n += 1
                fw[i] = n - 1
                n = 1
                while self._areUnlinked3(i, (i - n) % self.complexity, d):
                    n += 1
                bw[i] = n - 1
            for i in range(self.complexity):
                if d == 0:
                    x1 = self.ySorted[2 * i]
                    x2 = self.ySorted[2 * i + 1]
                else:
                    x1 = self.xSorted[2 * i]
                    x2 = self.xSorted[2 * i + 1]
                if fw[x1] + bw[x2] + 1 >= x2 - x1:
                    return self.chainCastle(x1, x2, d)
                if fw[x2] + bw[x1] + 1 >= x1 + self.complexity - x2:
                    return self.chainCastle(x2, x1, d)
        return 0

    def cycle(self, d):
        """
        change self inplace

        d is a direction (0 or 1)
        """
        if d == 0:
            self.xSorted = self.xSorted[-2:] + self.xSorted[:-2]
            self.ySorted = self.xySorted(self.xSorted)
        else:
            self.ySorted = self.ySorted[-2:] + self.ySorted[:-2]
            self.xSorted = self.xySorted(self.ySorted)

    def m_destabilisation(self, direction, row):
        self.complexity -= 1
        xS = []
        yS = []
        if direction == 0:
            for i in range(self.complexity + 1):
                if i != row:
                    a = self.xSorted[2 * i]
                    b = self.xSorted[2 * i + 1]
                    if a > self.xSorted[2 * row]:
                        a -= 1
                    if b > self.xSorted[2 * row]:
                        b -= 1
                    xS += [a, b]
            self.xSorted = xS
            self.ySorted = self.xySorted(xS)
        else:
            for i in range(self.complexity + 1):
                if i != row:
                    a = self.ySorted[2 * i]
                    b = self.ySorted[2 * i + 1]
                    if a > self.ySorted[2 * row]:
                        a -= 1
                    if b > self.ySorted[2 * row]:
                        b -= 1
                    yS += [a, b]
            self.ySorted = yS
            self.xSorted = self.xySorted(yS)

    def succCa(self):
        acc = []
        for i in range(self.complexity):
            if self.isCastle(i, 0):
                acc.append(self.copy().castle(i, 0))
            if self.isCastle(i, 1):
                acc.append(self.copy().castle(i, 1))
        return acc

    def fastsuccCa(self, dico):
        acc = []
        for i in range(self.complexity):
            if self.isCastle(i, 0):
                if self.hashCastle(i, 0) not in dico:
                    acc.append(self.copy().castle(i, 0))
            if self.isCastle(i, 1):
                if self.hashCastle(i, 1) not in dico:
                    acc.append(self.copy().castle(i, 1))
        return acc

    def hashCastle(self, i, d):
        self.castle(i, d)
        h1 = self.hashInt()
        self.castle(i, d)
        return h1

    def hashInt(self):
        n = self.complexity
        res = 0
        for i in range(n):
            res *= n
            res += self.xSorted[i * 2 + 0]
            res *= n
            res += self.xSorted[i * 2 + 1]
        return res

    def toRectDia(self):
        """
        d = FastRectDiag([(0,0),(0,4),(1,2),(1,8),(2,7),
        (2,9),(3,6),(3,8),(4,1),
        (4,3),(5,2),(5,7),(6,0),(6,3),(7,1),(7,5),(8,4),(8,6),
        (9,5),(9,9)])
        In [16]: d.toRectDia()
        Out[16]:
        o-----o
        |   o-+o
        |o--+o||
        ||  o+o|
        o+---+-+o
         |   | o+o
         | o-+--o|
         |o+-o   |
         o+o     |
          o------o
        """
        return RectDia([(i, self.xSorted[2 * i])
                        for i in range(len(self.xSorted) // 2)] +
                       [(i, self.xSorted[2 * i + 1])
                        for i in range(len(self.xSorted) // 2)])


if __name__ == "__main__":
    dd = FastRectDiag([(0, 0), (0, 4), (1, 2), (1, 8), (2, 7), (2, 9),
                       (3, 6), (3, 8), (4, 1), (4, 3), (5, 2), (5, 7),
                       (6, 0), (6, 3), (7, 1), (7, 5), (8, 4), (8, 6),
                       (9, 5), (9, 9)])
    dd.complexity = 7
    dd.xSorted = [2, 6, 1, 5, 4, 6, 3, 5, 0, 3, 1, 4, 0, 2]
    dd.ySorted = [4, 6, 1, 5, 0, 6, 3, 4, 2, 5, 1, 3, 0, 2]
    print(dd.toRectDia().toStringNice())
    des = dd.isdestabilisable()
    tmp = dd.copy()
    tmp.m_destabilisation(des[0], des[1])
    print(tmp.toRectDia().toStringNice())
