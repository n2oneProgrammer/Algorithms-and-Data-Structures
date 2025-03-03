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
        mat = [[sum([self.__matrix[i][k]*other[k][j] for k in range(self.size()[1])]) for j in range(other.size()[1])] for i in range(self.size()[0])]
        return Matrix(mat)

    def __str__(self):
        res = ""
        for row in self.__matrix:
            res += "|"
            for id, el in enumerate(row):
                res += str(el)
                if id +1 != len(row):
                    res += " "
            res += "|\n"
        return res

    def size(self):
        return self.__size

def transpose(mat:Matrix)->Matrix:
    mat = [[mat[i][j] for i in range(mat.size()[0])] for j in range(mat.size()[1])]
    return Matrix(mat)

if __name__ == "__main__":
    m = Matrix([
        [1,0,2],
        [-1,3,1]
    ])
    print(transpose(m))
    print(m + Matrix((2,3),1))
    print(m * Matrix([
        [3,1],
        [2,1],
        [1,0]
    ]))