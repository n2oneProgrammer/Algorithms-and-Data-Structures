import math
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


def distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def triangular_cost(p1: Point, p2: Point, p3: Point):
    return distance(p1, p2) + distance(p1, p3) + distance(p2, p3)


def min_cost_triangular_recursive(shape: list[Point]):
    n = len(shape)
    if n < 3:
        return 0

    min_cost = float("inf")
    for k in range(1, n - 1):
        cost = min_cost_triangular_recursive(shape[k:]) + min_cost_triangular_recursive(
            shape[:(k + 1)]) + triangular_cost(
            shape[0], shape[k], shape[n - 1])
        if cost < min_cost:
            min_cost = cost
    return min_cost


def min_cost_triangular_iterative(shape: list[Point]):
    n = len(shape)
    if n < 3:
        return 0

    dp = [[0 if j <= i + 1 else float('inf') for j in range(n)] for i in range(n)]
    for gap in range(2, n):
        for i in range(n - gap):
            j = i + gap
            for k in range(i + 1, j):
                cost = dp[i][k] + dp[k][j] + triangular_cost(shape[i], shape[j], shape[k])
                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[0][n - 1]


if __name__ == "__main__":
    shape1 = [Point(p[0], p[1]) for p in [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]]
    time11 = time.time()
    result11 = min_cost_triangular_recursive(shape1)
    delay11 = time.time() - time11
    time12 = time.time()
    result12 = min_cost_triangular_iterative(shape1)
    delay12 = time.time() - time12
    print("Wynik rekurencja: ", round(result11, 4), " czas: ", delay11)
    print("Wynik interacja: ", round(result12, 4), " czas: ", delay12)
    shape2 = [Point(p[0], p[1]) for p in [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]]
    time21 = time.time()
    result21 = min_cost_triangular_recursive(shape2)
    delay21 = time.time() - time21
    time22 = time.time()
    result22 = min_cost_triangular_iterative(shape2)
    delay22 = time.time() - time22
    print("Wynik rekurencja: ", round(result21, 4), " czas: ", delay21)
    print("Wynik interacja: ", round(result22, 4), " czas: ", delay22)
