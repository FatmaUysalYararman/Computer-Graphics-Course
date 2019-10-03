# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 06 2019
import sys
import numpy
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from vector import *
from matrix import *
from shapes import *
from camera import *
from scene import *
from view import *
from wavefront import *

# I was here. ###################
# # create grid
# grid = Grid("grid", 10, 10)
# grid.setDrawStyle(DrawStyle.WIRE)
# grid.setWireWidth(1)
# ###############################

# create camera
camera = Camera()
camera.createView(Point3f(0.0, 0.0, 10.0), Point3f(0.0, 0.0, 0.0), Vector3f(0.0, 1.0, 0.0))
camera.setNear(1)
camera.setFar(1000)

# create View
view = View(camera)
view.camera.zoom(-67)
view.camera.dolly(0, 24.4, 0)

# init scene
scene = Scene()
view.setScene(scene)

# # create objects
# cube1 = Cube("cube", 1, 1, 1, 10, 10, 10)
# cube1.Translate(2, 0.5, 0)
# scene.add(cube1)
# cube2 = Cube("cube", 1.5, 1.5, 1.5, 10, 10, 10)
# cube2.Translate(-2, 0, 0)
# scene.add(cube2)


def main():
    global view
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("CENG487 Assigment Template")

    # define callbacks
    glutDisplayFunc(view.draw)
    glutIdleFunc(view.idleFunction)
    glutReshapeFunc(view.resizeView)
    glutKeyboardFunc(view.keyPressed)
    glutSpecialFunc(view.specialKeyPressed)
    glutMouseFunc(view.mousePressed)
    glutMotionFunc(view.mouseMove)

    # Initialize our window
    width = 640
    height = 480
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LEQUAL)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    # glEnable(GL_LINE_SMOOTH)			# Enable line antialiasing

    # I was here. #######
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    lightFirstPos = [0, 44, 10, 1.0]
    lightIntensity = [0.5, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightFirstPos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightIntensity)
    # ###################

    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix

    # create the perpective projection
    gluPerspective(view.camera.fov, float(width)/float(height), camera.near, camera.far)
    glMatrixMode(GL_MODELVIEW)

    # Start Event Processing Engine
    glutMainLoop()


objFile = Wavefront()
objFile.load("cornell.obj")
colors = [
    ColorRGBA(0.6, 0.8, 1.0, 1.0),  # Kisa Kutu
    ColorRGBA(0.6, 0.8, 1.0, 1.0),  # Uzun Kutu
    ColorRGBA(0.8, 0.6, 0.4, 1.0),  # Taban
    ColorRGBA(0.8, 0.6, 0.4, 1.0),  # Tavan
    ColorRGBA(0.9, 0.2, 0.2, 1.0),  # Sol Duvar
    ColorRGBA(0.3, 0.6, 0.2, 1.0),  # Sag Duvar
    ColorRGBA(0.9, 0.7, 0.5, 1.0),  # Arka Duvar
]
# if len(sys.argv) > 1:
for i in range(len(objFile.objects)):
    obj = objFile.objects[i]
    shape = _Shape(str(obj[0]), obj[1], obj[2], False)
    shape.drawStyle = DrawStyle.SMOOTH
    shape.setColors([colors[i]])
    # shape.colors.append(colors[i])
    scene.add(shape)

LightCube = Cube("Light", 10, 1, 4, 10, 10, 10, True)
LightCube.Translate(0, 44, 10)
scene.add(LightCube)

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
# else:
#     # cube1.load("tori.obj")
#     print("Please type obj file name!")

"""
Grid ozelliginin eklenip eklenilmeyecegi view.py kodu icerisinden belirlendi.
Sahneye eklenen nesnenin boyutu cok buyuk oldugu icin kamera sahneden uzaklastirildi ve view.py kodu icerisinde kamera hareketlerinin hizi yukseltildi.
cornell.obj icerisindeki her parca (Group) icin ayri renk tanimlandi.
Sahneye eklenen bir nesnenin isik kaynagi olup olmayacagini belirlemek icin shapes.py kodu icerisinde degisiklikler yapildi.
"""
