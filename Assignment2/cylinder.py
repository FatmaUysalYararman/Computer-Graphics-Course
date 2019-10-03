# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 03 2019

from math import *
from vec3d import vec3d


class Cylinder:

    def __init__(self, r, h, s):
        self.radius = r
        self.height = h
        self.subdivision = s
        self.vertices = []

    def increaseSubdivision(self):
        if self.subdivision < 256:
            self.subdivision = self.subdivision + 1

    def decreaseSubdivision(self):
        if self.subdivision > 3:
            self.subdivision = self.subdivision - 1

    def getSubdivision(self):
        return self.subdivision

    def setSubdivision(self, s):
        self.subdivision = s

    def calculateVertices(self):
        self.vertices = []
        n = float(self.subdivision)
        points = []
        for i in range(int(n) + 1):
            angle = 2 * pi * (i / n)
            x = self.radius * cos(angle)
            y = self.radius * sin(angle)
            point = (x, y)
            points.append(point)

        groupCoverFirst = []
        groupCoverFirst.append(vec3d(0, 0, self.height / 2.0, 1))
        for (x, y) in points:
            z = self.height / 2.0
            groupCoverFirst.append(vec3d(x, y, z, 1))
        self.vertices.append(groupCoverFirst)

        groupCoverSecond = []
        groupCoverSecond.append(vec3d(0, 0, self.height / 2.0, 1))
        for (x, y) in points:
            z = -self.height / 2.0
            groupCoverSecond.append(vec3d(x, y, z, 1))
        self.vertices.append(groupCoverSecond)

        groupSide = []
        for (x, y) in points:
            z = self.height / 2.0
            groupSide.append(vec3d(x, y, z, 1))
            groupSide.append(vec3d(x, y, -z, 1))
        self.vertices.append(groupSide)

        return self.vertices
