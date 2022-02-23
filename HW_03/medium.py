import numpy as np

from numbers import Number
from numpy.lib.mixins import NDArrayOperatorsMixin


class MixClass(NDArrayOperatorsMixin):
    def __init__(self, matrix):
        self.matrix = np.asarray(matrix)

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix

    def __str__(self):
        rows = [[str(num) for num in row] for row in self.matrix.tolist()]
        beautiful_rows = '\t'.join('{{:{}}}'.format(x) for x in [max(map(len, col)) for col in zip(*rows)])
        return '\n'.join([beautiful_rows.format(*row) for row in rows])

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == '__call__':
            values = []
            for inp in inputs:
                if isinstance(inp, (Number, np.ndarray)):
                    values.append(inp)
                elif isinstance(inp, self.__class__):
                    values.append(inp.matrix)
                else:
                    raise NotImplementedError()
            return self.__class__(ufunc(*values, **kwargs))
        return NotImplementedError()

    def save(self, save_path):
        with open(save_path, 'w') as f:
            f.write(str(self))


if __name__ == "__main__":

    filename = 'artefacts/02_medium/matrix'

    np.random.seed(0)
    A = np.random.randint(0, 10, (10, 10))
    B = np.random.randint(0, 10, (10, 10))

    add_matrix = MixClass(A) + MixClass(B)
    assert np.array_equal(add_matrix.matrix, A + B), "not equal"
    add_matrix.save(f"{filename}+.txt")

    mul_matrix = MixClass(A) * MixClass(B)
    assert np.array_equal(mul_matrix.matrix, A * B), "not equal"
    mul_matrix.save(f"{filename}*.txt")

    matmul_matrix = MixClass(A) @ MixClass(B)
    assert np.array_equal(matmul_matrix.matrix, A @ B), "not equal"
    matmul_matrix.save(f"{filename}@.txt")