from functools import lru_cache


@lru_cache
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
    Parent = [[0] * (len(P) + 1) for _ in range(len(T) + 1)]
    for j in range(len(T) + 1):
        D[j][0] = j
        Parent[j][0] = 'D'
    for i in range(len(P) + 1):
        D[0][i] = i
        Parent[0][i] = 'I'
    print(D)
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
        path.append(Parent[j][i])

    return D[-1][-1], Parent[-1][-1]



def main():
    print(calcCostPD("kot", "pies"))


if __name__ == "__main__":
    main()
