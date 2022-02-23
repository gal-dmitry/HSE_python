import numpy as np


class ExtendedMatrix:
    def __init__(self, matrix):
        width = len(matrix[0])
        height = len(matrix)
        for row in matrix:
            if len(row) != width:
                raise ValueError('Incorrect dimensions')
        self.matrix = matrix
        self.shape = (height, width)

    def __getitem__(self, ind):
        if not isinstance(ind, (int, tuple)):
            raise ValueError('Incorrect index format')
        if isinstance(ind, int):
            return self.matrix[ind]
        if len(ind) != 2:
            raise ValueError('Incorrect index format')
        i, j = ind
        return self.matrix[i][j]

    def __str__(self):
        matrix = '\n'.join([str(row) for row in self.matrix])
        return f"[{matrix}]"

    def __eq__(self, other):
        return self.matrix == other.matrix if isinstance(other, self.__class__) else False

    def __add__(self, other):
        if other.shape != self.shape:
            raise ValueError('Incorrect shapes')
        height, width = self.shape
        result_matrix = [[self[i, j] + other[i, j] for j in range(width)] for i in range(height)]
        return self.__class__(result_matrix)

    def __mul__(self, other):
        if other.shape != self.shape:
            raise ValueError('Incorrect shapes')
        height, width = self.shape
        result_matrix = [[self[i, j] * other[i, j] for j in range(width)] for i in range(height)]
        return self.__class__(result_matrix)

    def __matmul__(self, other):
        height_0, width_0 = self.shape
        height_1, width_1 = other.shape
        if width_0 != height_1:
            raise ValueError('Incorrect shapes')
        result_matrix = \
        [[sum(self[i, j] * other[j, k] for j in range(width_0)) for k in range(width_1)] for i in range(height_0)]
        return self.__class__(result_matrix)


if __name__ == "__main__":

    filename = 'artefacts/01_easy/matrix'

    np.random.seed(0)
    A = np.random.randint(0, 10, (10, 10))
    B = np.random.randint(0, 10, (10, 10))

    add_matrix = ExtendedMatrix(A.tolist()) + ExtendedMatrix(B.tolist())
    assert add_matrix.matrix == (A + B).tolist(), "not equal"
    with open(f"{filename}+.txt", 'w') as f:
        f.write(str(add_matrix))

    mul_matrix = ExtendedMatrix(A.tolist()) * ExtendedMatrix(B.tolist())
    assert mul_matrix.matrix == (A * B).tolist(), "not equal"
    with open(f"{filename}*.txt", 'w') as f:
        f.write(str(mul_matrix))

    matmul_matrix = ExtendedMatrix(A.tolist()) @ ExtendedMatrix(B.tolist())
    assert matmul_matrix.matrix == (A @ B).tolist(), "not equal"
    with open(f"{filename}@.txt", 'w') as f:
        f.write(str(matmul_matrix))