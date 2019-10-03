# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 05 2019

import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import pi, sin, cos, sqrt, acos
from vector import *
from matrix import *
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']


class _Shape:
    def __init__(self, name, vertices, faces):
        self.vertices = vertices
        self.edges = []
        self.faces = faces
        self.colors = []
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.bboxWorld = BoundingBox()
        self.calcBboxObj()

        self.bagVertices = []
        self.bagFaces = []

        vs = []
        for v in self.vertices:
            vs.append(v)

        fs = []
        for f in self.faces:
            fs.append(f)

        self.bagVertices.append(vs)
        self.bagFaces.append(fs)

        self.totalVertexCount = len(vertices)
        self.totalPolygonCount = len(faces)

    def load(self, fileName):
        self.faces = []
        self.vertices = []
        self.bagVertices = []
        self.bagFaces = []

        for line in open(fileName, 'r'):
            if line.startswith('#'):
                continue
            data = line.split()

            if not data:
                continue

            if data[0] == 'v':
                x = float(data[1])
                y = float(data[2])
                z = float(data[3])
                vertice = Point3f(x, y, z)
                self.vertices.append(vertice)

            if data[0] == 'f':
                face = []
                for v in data[1:5]:
                    w = v.split('/')
                    face.append(int(w[0])-1)
                self.faces.append(face)

        vs = []
        for v in self.vertices:
            vs.append(v)
        self.bagVertices.append(vs)

        fs = []
        for f in self.faces:
            fs.append(f)
        self.bagFaces.append(fs)

    def calcBboxObj(self):
        for vertex in self.vertices:
            self.bboxObj.expand(vertex)

    def setDrawStyle(self, style):
        self.drawStyle = style

    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)

    def setWireWidth(self, width):
        self.wireWidth = width

    def draw(self):
        index = 0
        for face in self.faces:
            if self.drawStyle == DrawStyle.FACETED or self.drawStyle == DrawStyle.SMOOTH:
                glBegin(GL_POLYGON)

                if len(self.colors) > 0:
                    glColor3f(
                        self.colors[index].r, self.colors[index].g, self.colors[index].b)
                else:
                    glColor3f(1.0, 0.6, 0.0)

                for vertex in face:
                    glVertex3f(
                        self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
                glEnd()

            if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded == True:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glLineWidth(self.wireWidth)
                # glDisable(GL_LIGHTING)

                glBegin(GL_POLYGON)

                if self.wireOnShaded == True:
                    if self.fixedDrawStyle == True:
                        glColor3f(self.wireColor.r,
                                  self.wireColor.g, self.wireColor.b)
                    else:
                        glColor3f(self.wireOnShadedColor.r,
                                  self.wireOnShadedColor.g, self.wireOnShadedColor.b)
                else:
                    glColor3f(self.wireColor.r,
                              self.wireColor.g, self.wireColor.b)

                for vertex in face:
                    glVertex3f(
                        self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
                glEnd()

                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                # glEnable(GL_LIGHTING)

            index += 1
            if len(self.colors) == index:
                index = 0

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = self.obj2World.product(translate)

    def increaseSubdivision(self):
        newFaces = []
        edgePoints = {}
        faceCentroidList = []

        self.vertices = []
        vs = self.bagVertices[len(self.bagVertices) - 1]
        for v in vs:
            self.vertices.append(v)

        self.faces = []
        fs = self.bagFaces[len(self.bagFaces) - 1]
        for f in fs:
            self.faces.append(f)

        oldVertexCount = len(self.vertices)

        self.totalPolygonCount = len(self.faces)
        self.totalVertexCount = len(self.vertices)

        # Creating Generate face points
        for faceVertices in self.faces:
            centroid = Point3f(0, 0, 0)
            for idx in faceVertices:
                centroid.x += self.vertices[idx].x
                centroid.y += self.vertices[idx].y
                centroid.z += self.vertices[idx].z
            vertexCount = len(faceVertices)
            centroid.x /= vertexCount
            centroid.y /= vertexCount
            centroid.z /= vertexCount
            indexCenter = self.addVertice(centroid)
            faceCentroidList.append(indexCenter)

        # Creating edge points
        for face, faceVertices in enumerate(self.faces, 0):
            vertexCount = len(faceVertices)
            for faceIndex in range(vertexCount):
                index01 = faceVertices[faceIndex]
                index02 = faceVertices[(faceIndex + 1) % vertexCount]
                if index01 > index02:
                    indexTemp = index01
                    index01 = index02
                    index02 = indexTemp
                if not index01 in edgePoints.keys():
                    edgePoints[index01] = {}
                if not index02 in edgePoints[index01]:
                    connectedFaces = self.getConnectedFaces(index01, index02)
                    assert len(connectedFaces) == 2
                    avg = self.getCentroidOfPolygon(
                        index01, index02, faceCentroidList[connectedFaces[0]], faceCentroidList[connectedFaces[1]])
                    edgePoints[index01][index02] = self.addVertice(avg)

        # Modifing the existing vertices
        for index in range(oldVertexCount):
            connectedFaces = self.getConnectedFaces(index)
            n = float(len(connectedFaces))

            vertex01 = self.vertices[index]
            vertex02 = self.getCentroidOfPolygon(
                *[faceCentroidList[faceIndex] for faceIndex in connectedFaces])

            connectedVertexIndices = self.getConnectedVertexIndices(index)
            connectedEdgeMidPoints = []
            for connectedVertexIndex in connectedVertexIndices:
                if index < connectedVertexIndex:
                    connectedIndex01 = index
                    connectedIndex02 = connectedVertexIndex
                else:
                    connectedIndex01 = connectedVertexIndex
                    connectedIndex02 = index
                connectedEdgeMidPoints.append(
                    edgePoints[connectedIndex01][connectedIndex02])
            vertex03 = self.getCentroidOfPolygon(*connectedEdgeMidPoints)

            # Technique 1
            # w1 = (n - 3.0) / n
            # w2 = 1.0 / n
            # w3 = 2.0 / n
            # Technique 2
            w1 = (n - 2.5) / n
            w2 = 1.0 / n
            w3 = 1.5 / n
            # Technique 3
            # w1 = ((4.0 * n) - 7.0) / (4.0 * n)
            # w2 = 1.0 / (4.0 * (n * n))
            # w3 = 1.0 / (2.0 * (n * n))

            vertex01.x *= w1
            vertex01.y *= w1
            vertex01.z *= w1
            vertex02.x *= w2
            vertex02.y *= w2
            vertex02.z *= w2
            vertex03.x *= w3
            vertex03.y *= w3
            vertex03.z *= w3
            vertex03.x += vertex01.x + vertex02.x
            vertex03.y += vertex01.y + vertex02.y
            vertex03.z += vertex01.z + vertex02.z
            self.vertices[index] = vertex03

        # Creating new faces
        for face, faceVertices in enumerate(self.faces, 0):
            vertexCount = len(faceVertices)
            for faceIndex in range(len(faceVertices)):
                index01 = faceVertices[(faceIndex-1) % vertexCount]
                index02 = faceVertices[faceIndex]
                index03 = faceVertices[(faceIndex+1) % vertexCount]
                if index01 < index02:
                    midPoint01 = edgePoints[index01][index02]
                else:
                    midPoint01 = edgePoints[index02][index01]
                if index02 < index03:
                    midPoint02 = edgePoints[index02][index03]
                else:
                    midPoint02 = edgePoints[index03][index02]
                indexCenter = faceCentroidList[face]
                newFaces.append([indexCenter, midPoint01, index02, midPoint02])

        # Binding new faces
        self.faces = []
        for face in newFaces:
            self.faces.append(face)
        fs = []
        for f in self.faces:
            fs.append(f)
        self.bagFaces.append(fs)

        # Binding new vertices
        vertices = []
        for vertex in self.vertices:
            vertices.append(vertex)
        self.bagVertices.append(vertices)

        for vrt in self.bagVertices:
            print("VRT: ", len(vrt))
        for fc in self.bagFaces:
            print("FC: ", len(fc))

        self.totalVertexCount = len(self.vertices)
        self.totalPolygonCount = len(self.faces)
        print("")

    def decreaseSubdivision(self):
        if len(self.bagVertices) > 1:
            self.vertices = []
            vs = self.bagVertices[len(self.bagVertices) - 2]
            for v in vs:
                self.vertices.append(v)
            self.totalVertexCount = len(self.vertices)
            self.bagVertices.pop()

        if len(self.bagFaces) > 1:
            self.faces = []
            fs = self.bagFaces[len(self.bagFaces) - 2]
            for f in fs:
                self.faces.append(f)
            self.totalPolygonCount = len(self.faces)
            self.bagFaces.pop()

        for vrt in self.bagVertices:
            print("VRT: ", len(vrt))
        for fc in self.bagFaces:
            print("FC: ", len(fc))
        print ""

    def addVertice(self, vertex):
        self.vertices.append(vertex)
        return len(self.vertices) - 1

    def getCentroidOfPolygon(self, *points):
        centroid = Point3f(0.0, 0.0, 0.0)
        for idx in points:
            centroid.x += self.vertices[idx].x
            centroid.y += self.vertices[idx].y
            centroid.z += self.vertices[idx].z
        point_count = float(len(points))
        centroid.x /= point_count
        centroid.y /= point_count
        centroid.z /= point_count
        return centroid

    def getConnectedFaces(self, *indices):
        faces = []
        for face, faceVertices in enumerate(self.faces, 0):
            for index in indices:
                if not index in faceVertices:
                    break
            else:
                faces.append(face)
        return faces

    def getConnectedVertexIndices(self, vertexIndex):
        connectedVertexIndices = []
        for faceVertices in self.faces:
            polySize = len(faceVertices)
            if vertexIndex in faceVertices:
                faceIndex = faceVertices.index(vertexIndex)
                connectedVertexIndices.append(
                    faceVertices[(faceIndex-1) % polySize])
                connectedVertexIndices.append(
                    faceVertices[(faceIndex+1) % polySize])
        return list(set(connectedVertexIndices))


class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize, xDiv, yDiv, zDiv):
        vertices = []
        xStep = xSize / (xDiv + 1.0)
        yStep = ySize / (yDiv + 1.0)
        zStep = zSize / (zDiv + 1.0)
        # for i in range(0, xDiv):
        # 	for j in range(0, yDiv):
        # 		for k in range(0, zDiv):
        # 			x = -xSize / 2.0 + i * xStep
        # 			y = -ySize / 2.0 + j * yStep
        # 			z = -zSize / 2.0 + k * zStep
        # 			vertices.append( Point3f(x, y, z) )
        # add corners
        vertices.append(Point3f(-xSize / 2.0, -ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, -ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, ySize / 2.0, zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, -ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, -ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(-xSize / 2.0, ySize / 2.0, -zSize / 2.0))
        vertices.append(Point3f(xSize / 2.0, ySize / 2.0, -zSize / 2.0))

        faces = []
        faces.append([0, 2, 3, 1])
        faces.append([4, 6, 7, 5])
        faces.append([4, 6, 2, 0])
        faces.append([1, 3, 7, 5])
        faces.append([2, 6, 7, 3])
        faces.append([4, 0, 1, 5])

        _Shape.__init__(self, name, vertices, faces)
        self.drawStyle = DrawStyle.SMOOTH

        for i in range(0, len(faces) + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            self.colors.append(ColorRGBA(r, g, b, 1.0))
