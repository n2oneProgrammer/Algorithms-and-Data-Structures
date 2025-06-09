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
    def isLeft(p1: Point, p2: Point, p3: Point):
        return (p3.y - p2.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p3.x - p2.x)

    def jarvis(self):
        first_point = min(self.points, key=lambda p: (p.x, p.y))
        p = first_point
        while True:
            self.hull.append(p)
            q = self.points[0] if self.points[0] != p else self.points[1]

            i=0
            while i < len(self.points):
                r = self.points[i]
                if r == p or r == q:
                    i+=1
                    continue
                if self.isLeft(p, q, r) >= 0:
                    q = r
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
