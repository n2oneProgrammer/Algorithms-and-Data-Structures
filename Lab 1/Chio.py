import copy
from typing import List, Tuple


class Matrix:
    def __init__(self, arg: Tuple | List, val=0):
        if isinstance(arg, tuple):
            self.__matrix = [[val for _ in range(arg[1])] for __ in range(arg[0])]
            self.__size = arg
        elif (isinstance(arg, list)
              and len(arg) > 0
              and len(arg[0]) > 0
              and any(isinstance(el, list) for el in arg)):
            self.__matrix = copy.deepcopy(arg)
            self.__size = (len(arg), len(arg[0]))

    def __getitem__(self, id: int) -> List:
        if id >= self.__size[0] or id < 0:
            raise IndexError()
        return self.__matrix[id]

    def __add__(self, other: any):
        if self.size()[0] != other.size()[0] or self.size()[1] != other.size()[1]:
            raise ArithmeticError()
        mat = [[self.__matrix[i][j] + other[i][j] for j in range(self.size()[1])] for i in range(self.size()[0])]
        return Matrix(mat)

    def __mul__(self, other):
        if self.size()[1] != other.size()[0]:
            raise ArithmeticError()
        mat = [[sum([self.__matrix[i][k] * other[k][j] for k in range(self.size()[1])]) for j in range(other.size()[1])]
               for i in range(self.size()[0])]
        return Matrix(mat)

    def __str__(self):
        res = ""
        for row in self.__matrix:
            res += "|"
            for id, el in enumerate(row):
                res += str(el)
                if id + 1 != len(row):
                    res += " "
            res += "|\n"
        return res

    def size(self):
        return self.__size

    def swap_row(self, x, y):
        if x < 0 or y < 0 or x >= self.__size[0] or y >= self.__size[1]:
            raise ArithmeticError()

        temp = self.__matrix[x]
        self.__matrix[x] = self.__matrix[y]
        self.__matrix[y] = temp


def transpose(mat: Matrix) -> Matrix:
    mat = [[mat[i][j] for i in range(mat.size()[0])] for j in range(mat.size()[1])]
    return Matrix(mat)


def chio(mat: Matrix) -> float:
    if mat.size()[0] != mat.size()[1]:
        raise ArithmeticError()
    n = mat.size()[0]
    if n == 1:
        return mat[0][0]
    if n == 2:
        return mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]
    if mat[0][0] == 0:
        for i in range(1, n):
            if mat[i][0] != 0:
                mat.swap_row(i, 0)
                break
        else:
            return 0
        return -chio(mat)
    temp_mat = Matrix((n - 1, n - 1))
    for x in range(n - 1):
        for y in range(n - 1):
            temp_mat[x][y] = chio(
                Matrix([
                    [mat[0][0], mat[0][y + 1]],
                    [mat[x + 1][0], mat[x + 1][y + 1]]
                ])
            )
    return 1 / (mat[0][0] ** (n - 2)) * chio(temp_mat)


if __name__ == "__main__":
    m = Matrix([
        [5, 1, 1, 2, 3],
        [4, 2, 1, 7, 3],
        [2, 1, 2, 4, 7],
        [9, 1, 0, 7, 0],
        [1, 4, 7, 2, 2]
    ])
    print(chio(m))

    m = Matrix([
        [0, 1, 1, 2, 3],
        [4, 2, 1, 7, 3],
        [2, 1, 2, 4, 7],
        [9, 1, 0, 7, 0],
        [1, 4, 7, 2, 2]
    ])
    print(chio(m))
    m = Matrix([
        [0, 0, 1, 2, 3],
        [4, 2, 1, 7, 3],
        [2, 1, 2, 4, 7],
        [10, 5, 0, 7, 0],
        [8, 4, 7, 2, 2]
    ])
    print(chio(m))
