def calcCost(P, T, i=None, j=None):
    if i is None:
        i = len(P) - 1
    if j is None:
        j = len(T) - 1
    if i == -1:
        return j + 1
    if j == -1:
        return i + 1

    r1 = 1 + calcCost(P, T, i, j - 1)
    r2 = 1 + calcCost(P, T, i - 1, j)
    r3 = (1 if P[i] != T[j] else 0) + calcCost(P, T, i - 1, j - 1)
    return min(r1, r2, r3)


def calcCostPD(P, T):
    D = [[0] * (len(P) + 1) for _ in range(len(T) + 1)]
    Parent = [['X'] * (len(P) + 1) for _ in range(len(T) + 1)]
    for j in range(len(T) + 1):
        D[j][0] = j
        Parent[j][0] = 'D'
    for i in range(len(P) + 1):
        D[0][i] = i
        Parent[0][i] = 'I'
    Parent[0][0] = 'X'

    for i in range(1, len(P) + 1):
        for j in range(1, len(T) + 1):
            k1 = (D[j - 1][i] + 1, 'I')
            k2 = (D[j][i - 1] + 1, 'D')
            k3 = (D[j - 1][i - 1] + (1 if P[i - 1] != T[j - 1] else 0), 'S' if P[i - 1] != T[j - 1] else 'M')
            D[j][i] = min(k1, k2, k3, key=lambda a: a[0])[0]
            Parent[j][i] = min(k1, k2, k3, key=lambda a: a[0])[1]
    i = len(P)
    j = len(T)
    path = []
    while Parent[j][i] != 'X':
        p = Parent[j][i]
        path.append(p)

        if p == 'M' or p == 'S':
            i -= 1
            j -= 1
        elif p == 'D':
            i -= 1
        elif p == 'I':
            j -= 1

    return D[-1][-1], ''.join(reversed(path))


def findSequence(P, T):
    D = [[0] * (len(P) + 1) for _ in range(len(T) + 1)]
    Parent = [['X'] * (len(P) + 1) for _ in range(len(T) + 1)]

    for j in range(len(T) + 1):
        D[j][0] = 0
        Parent[j][0] = 'X'

    for i in range(1, len(P) + 1):
        for j in range(1, len(T) + 1):
            k1 = (D[j - 1][i] + 1, 'I')
            k2 = (D[j][i - 1] + 1, 'D')
            k3 = (D[j - 1][i - 1] + (1 if P[i - 1] != T[j - 1] else 0), 'S' if P[i - 1] != T[j - 1] else 'M')
            D[j][i] = min(k1, k2, k3, key=lambda a: a[0])[0]
            Parent[j][i] = min(k1, k2, k3, key=lambda a: a[0])[1]

    row = [D[a][len(P)] for a in range(1, len(T) + 1)]
    min_cost = min(row)
    i = len(P)
    j = row.index(min_cost)

    path = []
    while Parent[j][i] != 'X':
        p = Parent[j][i]
        path.append(p)

        if p == 'M' or p == 'S':
            i -= 1
            j -= 1
        elif p == 'D':
            i -= 1
        elif p == 'I':
            j -= 1

    return j


def longestSequence(P, T):
    D = [[0] * (len(P) + 1) for _ in range(len(T) + 1)]
    Parent = [['X'] * (len(P) + 1) for _ in range(len(T) + 1)]
    for j in range(len(T) + 1):
        D[j][0] = j
        Parent[j][0] = 'D'
    for i in range(len(P) + 1):
        D[0][i] = i
        Parent[0][i] = 'I'
    Parent[0][0] = 'X'

    for i in range(1, len(P) + 1):
        for j in range(1, len(T) + 1):
            k1 = (D[j - 1][i] + 1, 'I')
            k2 = (D[j][i - 1] + 1, 'D')
            k3 = (D[j - 1][i - 1] + (1e11 if P[i - 1] != T[j - 1] else 0), 'S' if P[i - 1] != T[j - 1] else 'M')
            D[j][i] = min(k1, k2, k3, key=lambda a: a[0])[0]
            Parent[j][i] = min(k1, k2, k3, key=lambda a: a[0])[1]
    i = len(P)
    j = len(T)
    path = []
    while i >= 0 and j >= 0 and Parent[j][i] != 'X':
        p = Parent[j][i]

        if p == 'M' or p == 'S':
            path.append(P[i-1])
            i -= 1
            j -= 1
        elif p == 'D':
            i -= 1
        elif p == 'I':
            j -= 1

    return ''.join(reversed(path))

def main():
    print(calcCost("kot","pies"))
    print(calcCostPD("biały autobus","czarny autokar")[0])
    print(calcCostPD('thou shalt not', 'you should not')[1])
    print(findSequence("ban","mokeyssbanana"))
    print(longestSequence("democrat","republican"))
    T = '243517698'
    P = sorted(T)
    print(longestSequence(P,T))


if __name__ == "__main__":
    main()
