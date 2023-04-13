import Core
import random


class Matrix:
    __slots__ = ("rows", "cols", "data")

    def __init__(self, rows, cols, create_data=True):
        self.rows = rows
        self.cols = cols

        if create_data:
            self.data = [([0] * cols) for _ in range(rows)]
        else:
            self.data = None

    def __repr__(self):
        return "{}".format(self.data)

    @staticmethod
    def from_array(arr):
        r = len(arr)
        c = len(arr[0])
        m = Matrix(r, c, False)
        m.data = Core.copy_2D_list(arr)
        return m

    @staticmethod
    def from_array_light(arr):
        """ Faster method than from_array but doesn't copy the array arr """
        r = len(arr)
        c = len(arr[0])
        m = Matrix(r, c, False)
        m.data = arr
        return m

    @staticmethod
    def random(rows, cols):
        res = Matrix(rows, cols)
        res.mapImpl(lambda i, j, el: random.uniform(-1, 1))
        return res

    def copy(self):
        m = Matrix(self.rows, self.cols, False)
        m.data = Core.copy_2D_list(self.data)
        return m

    def toDict(self):
        return self.data

    def map(self, fn):
        m = self.copy()
        for i, cols in enumerate(m.data):
            for j, el in enumerate(cols):
                m.data[i][j] = fn(i, j, el)
        return m

    def mapImpl(self, fn):
        for i, cols in enumerate(self.data):
            for j, el in enumerate(cols):
                self.data[i][j] = fn(i, j, el)

    def __sub__(self, other):
        assert self.rows == other.rows and self.cols == other.cols
        return self.map(lambda i, j, el: el - other.data[i][j])

    def __add__(self, other):
        assert self.rows == other.rows and self.cols == other.cols
        return self.map(lambda i, j, el: el + other.data[i][j])

    def __mul__(self, other):
        assert self.cols == other.rows
        res = Matrix(self.rows, other.cols)
        res.mapImpl(lambda i, j, el: sum(
            [(self.data[i][k] * other.data[k][j]) for k in range(self.cols)]
        ))
        return res
