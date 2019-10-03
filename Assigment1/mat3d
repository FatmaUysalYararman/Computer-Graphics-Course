# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 03 2019
from vec3d import vec3d
import math


class mat3d(object):
    def __init__(self, matrix):
        self.matrix = matrix
        self.row = len(matrix)
        self.col = len(matrix[0])
        self.newMatrix = []
        self.line = ''

    def __str__(self):
        for i in range(self.row):
            self.line += '\n'
            for j in range(self.col):
                self.line += '%g\t' % (self.matrix[i][j])
        return self.line
    def multiplication(self, vertex):
        vec = vec3d(vertex.x, vertex.y, vertex.z, vertex.w)
        vecRow01 = vec3d(self.matrix[0][0], self.matrix[0][1], self.matrix[0][2], self.matrix[0][3])
        vecRow02 = vec3d(self.matrix[1][0], self.matrix[1][1], self.matrix[1][2], self.matrix[1][3])
        vecRow03 = vec3d(self.matrix[2][0], self.matrix[2][1], self.matrix[2][2], self.matrix[2][3])
        vecRow04 = vec3d(self.matrix[3][0], self.matrix[3][1], self.matrix[3][2], self.matrix[3][3])

        return vec3d(vecRow01.dotProduct(vec), vecRow02.dotProduct(vec), vecRow03.dotProduct(vec), vecRow04.dotProduct(vec))

    def transpose(self):
        self.row, self.col = self.col, self.row
        self.matrix = [list(item) for item in zip(*self.matrix)]
        return mat3d(self.matrix)

    @staticmethod
    def translationMatrix(dx, dy, dz):
        matrix = [
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ]
        return mat3d(matrix)

    @staticmethod
    def rotationX(angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        rotationX = [
            [1, 0, 0, 0],
            [0, cos, -sin, 0],
            [0, sin, cos, 0],
            [0, 0, 0, 1]
        ]
        return (mat3d(rotationX))

    @staticmethod
    def rotationY(angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        rotationY = [
            [cos, 0, sin, 0],
            [0, 1, 0, 0],
            [-sin, 0, cos, 0],
            [0, 0, 0, 1]
        ]
        return (mat3d(rotationY))

    @staticmethod
    def rotationZ(angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        rotationZ = [
            [cos, -sin, 0, 0],
            [sin, cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        return (mat3d(rotationZ))

    @staticmethod
    def scalingMatrix(sx, sy, sz):
        matrix = [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ]
        return mat3d(matrix)
