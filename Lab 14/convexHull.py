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


class ConvexHull:
    def __init__(self, points):
        self.points = points
        self.hull = []

    @staticmethod
    def isRight(p: Point, q: Point, r: Point):
        return (q.y - p.y) * (r.x - q.x) - (r.y - q.y) * (q.x - p.x)

    @staticmethod
    def distance(p: Point, q: Point):
        return (p.x - q.x) ** 2 + (p.y - q.y) ** 2

    def jarvis(self):
        first_point = min(self.points, key=lambda p: (p.x, p.y))
        p = first_point
        while True:
            self.hull.append(p)
            q = self.points[0] if self.points[0] != p else self.points[1]

            i = 0
            while i < len(points):
                r = points[i]
                if r == p and r == q:
                    i += 1
                    continue
                o = ConvexHull.isRight(p, q, r)
                if o < 0 or (o == 0 and ConvexHull.distance(p, r) > ConvexHull.distance(p, q)):
                    q = r
                    i = 0
                    continue
                i += 1

            p = q
            if p == first_point:
                break


if __name__ == "__main__":
    points = [Point(p[0], p[1]) for p in [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]]
    hull = ConvexHull(points)
    hull.jarvis()
    print(hull.hull)

    points = [Point(p[0], p[1]) for p in [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]]
    hull = ConvexHull(points)
    hull.jarvis()
    print(hull.hull)

    points = [Point(p[0], p[1]) for p in [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]]
    hull = ConvexHull(points)
    hull.jarvis()
    print(hull.hull)
