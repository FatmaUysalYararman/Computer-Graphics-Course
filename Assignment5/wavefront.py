# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 06 2019

from vec3d import vec3d


class Wavefront:
    def __init__(self):
        self.objects = []
        self.vertices = []
        self.polygons = []

    def load(self, fileName):
        name = ""
        faces = []

        for line in open(fileName, 'r'):
            if line.startswith('#'):
                continue
            data = line.split()

            if not data:
                continue

            if (data[0] == "g" and data[1] == "default"):
                # print("Group")
                self.createObject(name, faces)
                # self.vertices = []
                self.polygons = []
                faces = []
                continue
            elif (data[0] == "g"):
                name = data[1]
                continue

            if data[0] == 'v':
                x = float(data[1])
                y = float(data[2])
                z = float(data[3])
                vertice = vec3d(x, y, z, 1)
                self.vertices.append(vertice)

            if data[0] == 'f':
                face = []
                for v in data[1:5]:
                    w = v.split('/')
                    face.append(int(w[0]) - 1)
                faces.append(face)
        
        self.createObject(name, faces)

    def createObject(self, name, faces):
        if(len(self.vertices) > 0):
            self.polygons = []
            for i in range(len(faces)):
                face = faces[i]
                polygon = []
                for j in range(len(face)):
                    point = face[j]
                    polygon.append(self.vertices[point])
                self.polygons.append(polygon)
            self.objects.append([name, self.vertices, faces, self.polygons])
