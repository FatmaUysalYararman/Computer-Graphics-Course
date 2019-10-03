from math import *
from vec3d import vec3d


class Obj:
    def __init__(self):
        self.vertices = []
        self.polygons = []
        self.biggest = 0
        self.totalPolygonCount = 0

    def load(self, fileName):
        faces = []

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
                if x > self.biggest:
                    self.biggest = x
                if y > self.biggest:
                    self.biggest = y
                if z > self.biggest:
                    self.biggest = z
                vertice = vec3d(x, y, z, 1)
                self.vertices.append(vertice)

            if data[0] == 'f':
                face = []
                for v in data[1:5]:
                    w = v.split('/')
                    face.append(int(w[0])-1)
                faces.append(face)

        self.polygons = []
        for i in range(len(faces)):
            face = faces[i]
            polygon = []
            for j in range(len(face)):
                point = face[j]
                polygon.append(self.vertices[point])
            self.polygons.append(polygon)
        self.totalPolygonCount = len(self.polygons)

    def increaseSubdivision(self):
        if self.totalPolygonCount < 5000:
            tempPolygons = []
            for i in range(len(self.polygons)):
                polygon = self.polygons[i]
                (centerX, centerY, centerZ) = self.getCentroidOfPolygon(polygon)
                for j in range(len(polygon)):
                    tempPolygon = []
                    pointTwo = polygon[0]
                    if j != len(polygon) - 1:
                        pointTwo = polygon[j + 1]
                    pointZer = polygon[len(polygon) - 1]
                    if j != 0:
                        pointZer = polygon[j - 1]
                    pointOne = polygon[j]
                    midPointPrev = self.getCentroidOfTwoPoints(pointOne, pointZer)
                    midPointNext = self.getCentroidOfTwoPoints(pointOne, pointTwo)
                    verticeOne = vec3d(pointOne.x, pointOne.y, pointOne.z, 1)
                    verticeTwo = vec3d(midPointNext.x, midPointNext.y, midPointNext.z, 1)
                    verticeThr = vec3d(centerX, centerY, centerZ, 1)
                    verticeFou = vec3d(midPointPrev.x, midPointPrev.y, midPointPrev.z, 1)
                    tempPolygon.append(verticeOne)
                    tempPolygon.append(verticeTwo)
                    tempPolygon.append(verticeThr)
                    tempPolygon.append(verticeFou)
                    tempPolygons.append(tempPolygon)
            self.polygons = tempPolygons
            self.totalPolygonCount = len(self.polygons)
        print "Total Polygon: ", self.totalPolygonCount

    def getCentroidOfTwoPoints(self, pointOne, pointTwo):
        return vec3d((pointOne.x + pointTwo.x) / 2, (pointOne.y + pointTwo.y) / 2, (pointOne.z + pointTwo.z) / 2, 1)

    def getCentroidOfPolygon(self, polygon):
        sx = sy = sz = slen = 0
        centerX = centerY = centerZ = centerLen = 0
        x1 = polygon[len(polygon) - 1].x
        y1 = polygon[len(polygon) - 1].y
        z1 = polygon[len(polygon) - 1].z
        for i in range(len(polygon)):
            x2 = polygon[i].x
            y2 = polygon[i].y
            z2 = polygon[i].z
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            tempLen = sqrt(dx*dx + dy*dy + dz*dz)
            centerX = centerX + (x1 + x2) / 2 * tempLen
            centerY = centerY + (y1 + y2) / 2 * tempLen
            centerZ = centerZ + (z1 + z2) / 2 * tempLen
            centerLen = centerLen + tempLen
            x1 = x2
            y1 = y2
            z1 = z2
        centerX = centerX / centerLen
        centerY = centerY / centerLen
        centerZ = centerZ / centerLen

        return (centerX, centerY, centerZ)
