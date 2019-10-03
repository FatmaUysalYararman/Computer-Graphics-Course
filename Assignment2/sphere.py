# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 03 2019

from math import *
from vec3d import vec3d


class Sphere:

    def __init__(self, radius):
        self.radius = radius
        self.theta = 0
        self.longitudeCount = 32
        self.latitudeCount = 32
        self.vertices = []

    def increaseSubdivision(self):
        if self.longitudeCount < 256:
            self.longitudeCount = self.longitudeCount + 2
            self.latitudeCount = self.latitudeCount + 2

    def decreaseSubdivision(self):
        if self.longitudeCount > 4:
            self.longitudeCount = self.longitudeCount - 2
            self.latitudeCount = self.latitudeCount - 2

    def getLongitude(self):
        return self.longitudeCount

    def setLongitude(self, longitude):
        self.longitudeCount = longitude

    def getLatitude(self):
        return self.latitudeCount

    def setLatitude(self, latitude):
        self.latitudeCount = latitude

    def calculateVertices(self):
        self.vertices = []
        for i in range(0, self.latitudeCount + 1):
            latitudeOne = pi * (-0.5 + float(float(i - 1) /
                                      float(self.latitudeCount)))
            z0 = sin(latitudeOne)
            zr0 = cos(latitudeOne)

            latitudeTwo = pi * (-0.5 + float(float(i) / float(self.latitudeCount)))
            z1 = sin(latitudeTwo)
            zr1 = cos(latitudeTwo)

            longitudeGroup = []
            for j in range(0, self.longitudeCount + 1):
                longitude = 2 * pi * float(float(j - 1) / float(self.longitudeCount))
                x = cos(longitude)
                y = sin(longitude)
                vecZ0 = vec3d(x * zr0, y * zr0, z0, 1)
                vecZ1 = vec3d(x * zr1, y * zr1, z1, 1)
                verticeGroup = []
                verticeGroup.append(vecZ0)
                verticeGroup.append(vecZ0)
                verticeGroup.append(vecZ1)
                verticeGroup.append(vecZ1)
                longitudeGroup.append(verticeGroup)

            self.vertices.append(longitudeGroup)

        return self.vertices
