from six.moves import range


def connComp(ellx, elly):
    """
    something about connected components

    >>> tst1 = [-1, (6, 1, 9, 10), (11, 5, 14, 14), (16, 9, 19, 18), (21, 1, 24, 14)]
    >>> tst2 = [(5, 0, 25, 3), -1, (5, 8, 20, 11), (10, 12, 25, 15), (2, 16, 20, 19)]
    >>> print(connComp(tst1, tst2))
    """
    n = len(ellx)
    mx = 5 * n + 10
    my = 4 * n + 10
    tab = [[0] * (2 * my) for _ in range(mx * 2)]
    for e in ellx + elly:
        if e == -1:
            continue
        for i in range(e[0] * 2, e[2] * 2 + 1):
            tab[i][e[1] * 2] = -1
            tab[i][e[3] * 2] = -1
        for i in range(e[1] * 2, e[3] * 2 + 1):
            tab[e[0] * 2][i] = -1
            tab[e[2] * 2][i] = -1
    col = 0
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            cc = tab[i][j]
            if cc == 0:
                col += 1
                contaminate(i, j, tab, col, mx, my)  # 1..n for col
    res = []
    for c in range(col):
        boo = False
        for i in range(len(tab) // 2):
            for j in range(len(tab[0]) // 2):
                if tab[i * 2 + 1][j * 2 + 1] == c + 1:
                    res.append((i, j))
                    boo = True
                    break
            if boo:
                break
    return res


def contaminate(x, y, tab, col, mx, my):
    s = [(x, y)]
    while s:
        x, y = s.pop()
        if tab[x][y] == 0:
            tab[x][y] = col
            if x > 0:
                s.append((x - 1, y))
            if x < mx * 2 - 1:
                s.append((x + 1, y))
            if y < my * 2 - 1:
                s.append((x, y + 1))
            if y > 0:
                s.append((x, y - 1))
