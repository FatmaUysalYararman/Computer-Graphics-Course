# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 06 2019
import math


class vec3d(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ', ' + str(self.w) + ')'

    def scalarMultiplication(self, value):
        return vec3d(value * self.x,  value * self.y, value * self.z, value * self.w)

    def dotProduct(self, vector3d):
        return self.x * vector3d.x + self.y * vector3d.y + self.z * vector3d.z + self.w * vector3d.w

    def addVectors(self, vector3d):
        return vec3d(self.x + vector3d.x, self.y + vector3d.y, self.z + vector3d.z, self.w + vector3d.w)

    def substractionVectors(self, vector3d):
        return vec3d(self.x - vector3d.x, self.y - vector3d.y, self.z - vector3d.z, self.w - vector3d.w)

    def lengthOfVector(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def angleBetweenVectors(self, vector3d):
        if(self.dotProduct(vector3d) == 0):
            return math.acos(0)
        return math.acos(self.dotProduct(vector3d) / (self.lengthOfVector() * other.lengthOfVector()))

    def projectionForXBasisVector(self):
        x = (1, 0, 0, 0)
        return vec3d(self.x * x[0], self.y * x[1], self.z * x[2], self.w * x[3])

    def projectionForYBasisVector(self):
        y = (0, 1, 0, 0)
        return vec3d(self.x * y[0], self.y * y[1], self.z * y[2], self.w * y[3])

    def projectionForXBasisVector(self):
        z = (0, 0, 1, 0)
        return vec3d(self.x * z[0], self.y * z[1], self.z * z[2], self.w * z[3])

    @staticmethod
    def getBasisXVector():
        return vec3d(1, 0, 0, 0)

    @staticmethod
    def getBasisYVector():
        return vec3d(0, 1, 0, 0)

    @staticmethod
    def getBasisZVector():
        return vec3d(0, 0, 1, 0)

    @staticmethod
    def getBasisWVector():
        return vec3d(0, 0, 0, 1)

    def crossProduct(self, vector3d):
        outputVectorX = self.y * vector3d.z - self.z * vector3d.y
        outputVectorY = self.z * vector3d.x - self.x * vector3d.z
        outputVectorZ = self.x * vector3d.y - self.y * vector3d.x
        return vec3d(outputVectorX, outputVectorY, outputVectorZ, 0)
