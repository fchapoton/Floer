from .RectDia import RectDia


def unknot(diag):
    counter = 0
    stack = [(diag, 0)]
    hmap = {diag.hashInt(): 0}
    while True:
        if not stack:
            print(diag.toStringNice())
            return "not an unknot"
        else:
            diag, depth = stack.pop()

        if diag.size() < 3:
            return "not knotted"
        succDe = diag.succTrDe()
        if succDe:
            print("reduction!")
            print(len(stack))
            print(depth)

            diag = succDe[0]

            stack = [(diag, 0)]
            depth = 0

            hmap = {diag.hashInt(): 0}
        succ = diag.succCa()
        print(len(succ))
        for k in succ:
            if k.hashInt() not in hmap:
                stack = [(k, depth + 1)] + stack
                hmap[k.hashInt()] = 0
        if len(hmap) >= 500 + counter or len(hmap) <= -500 + counter:
            counter = len(hmap)
            print("Please wait!")
            print(len(hmap))
            print(depth)


def unknotByFlipe(diag):
    while True:
        n = diag.size()
        succ = diag.succfl()
        for k in succ:
            if k.size() < n:
                print("reduction")
                diag = k
                break
        if n == diag.size():
            break
    print("finished")
    diag.draw()


if __name__ == "__main__":
    dd0 = RectDia([(0, 0), (0, 3), (1, 1), (1, 2), (2, 2),
                   (2, 3), (3, 0), (3, 1)])  # c
    dd1 = RectDia([(0, 0), (2, 0), (0, 2), (2, 2), (1, 1), (1, 3),
                   (3, 1), (3, 3)])  # bracelet
    dd2 = RectDia([(2, 0), (1, 1), (0, 2), (0, 4), (1, 3), (2, 2),
                   (3, 1), (4, 0), (4, 3), (3, 4)])  # threefoil
    dd3 = RectDia([(2, 0), (1, 1), (0, 2), (0, 4), (1, 3), (2, 2), (3, 1),
                   (4, 0), (4, 3), (3, 5), (5, 4), (5, 5)])  # threefoil
    dd4 = RectDia([(0, 0), (0, 4), (1, 2), (1, 8), (2, 7), (2, 9), (3, 6),
                   (3, 8), (4, 1), (4, 3), (5, 2), (5, 7), (6, 0), (6, 3),
                   (7, 1), (7, 5), (8, 4), (8, 6), (9, 5), (9, 9)])
    dd5 = RectDia([(0, 0), (0, 4), (1, 2), (1, 8), (2, 7), (2, 9), (3, 6),
                   (3, 8), (4, 1), (4, 3), (5, 2), (5, 7), (6, 0), (6, 3),
                   (7, 1), (7, 5), (8, 4), (8, 6), (9, 5), (9, 9)])
    dd6 = RectDia([(0, 23), (0, 6), (1, 21), (1, 7), (2, 19), (2, 11),
                   (3, 0), (3, 4), (4, 5), (4, 18), (5, 3), (5, 1),
                   (6, 7), (6, 2), (7, 16), (7, 8), (8, 11), (8, 6),
                   (9, 13), (9, 5), (10, 12), (10, 4), (11, 9), (11,
                   3), (12, 15), (12, 8), (13, 21), (13, 13), (14,
                   10), (14, 1), (15, 15), (15, 9), (16, 17), (16,
                   14), (17, 16), (17, 12), (18, 18), (18, 10), (19,
                   14), (19, 0), (20, 20), (20, 17), (21, 22), (21,
                   19), (22, 23), (22, 20), (23, 22), (23, 2)])
    dd7 = RectDia([(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2)])

    dd = dd0
    dd.draw()
    print(unknot(dd))
