# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 03 2019

'''
Use number keys to change shape:
Key 1: Sphere Shape
Key 2: Cylinder Shape

Use NUM+ and NUM- keys to change subdivision count:
Key NUM+: Increases subdivision count
Key NUM-: Decreases subdivision count

Use Alt Key + Mouse Left Button to rotate:
To shift to left : Rotates clockwise
To shift to right: Rotates counterclockwise 

Use Alt Key + Mouse Right Button to zoom:
To shift to left : Zoom out
To shift to right: Zoom in

Use F key for resetting the view to fully enclose the primitive on screen.
'''

import sys
import sphere
import cylinder
from vec3d import vec3d
from math import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *

pressedSpecialKey = '\001'

# ESCAPE Key = 27
ESCAPE = '\033'
# NUM+ Key = 43
NUMPLUS = '\053'
# NUM- Key = 45
NUMMINUS = '\055'
# NUM1 Key = 49
NUM1 = '\061'
# NUM2 Key = 50
NUM2 = '\062'
# W Key = 87
KEYW = '\127'
# w Key = 119
KEYWW = '\167'
# S Key = 83
KEYS = '\123'
# s Key = 115
KEYSS = '\163'
# F Key = 70
KEYF = '\106'
# f Key = 102
KEYFF = '\146'

# Number of the glut window.
window = 0
windowSizeX = 640
windowSizeY = 480

# Type of current drawn shape.
# 1 = Sphere
# 2 = Cylinder
shapeType = 1

# gluLookAt 'eye' coordinates
eyeX = 3.0
eyeY = 0.0
eyeZ = 0.0
# gluLookAt 'up' coordinates
upX = 0.0
upY = 0.0
upZ = 1.0

mousePosX = 0
mousePosY = 0
isPressedMouseLeft = 0
isPressedMouseRight = 0

rotation = 0

Sph = sphere.Sphere(1.0)
Cyl = cylinder.Cylinder(0.75, 1.25, 16)


def InitGL(Width, Height):
    # We call this right after our OpenGL window is created.
    global eyeX, eyeY, eyeZ, upX, upY, upZ

    # This Will Clear The Background Color To Black
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    # glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    glShadeModel(GL_FLAT)				# Enables Flat Color Shading

    lightFirstPos = [-9.0, 9.0, -2.0, 1.0]
    lightSecondPos = [9.0, -9.0, -2.0, 1.0]
    lightIntensity = [0.9, 0.9, 0.9, 1.0]
    lightAmbientIntensity = [0.75, 0.75, 0.75, 1.0]

    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lightAmbientIntensity)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightFirstPos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightIntensity)

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, lightSecondPos)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightIntensity)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()


def ReSizeGLScene(Width, Height):
    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    if Height == 0:
        Height = 1

    # Reset The Current Viewport And Perspective Transformation
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    # The main drawing function.
    global rotation

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, 0.0)
    gluLookAt(eyeX, eyeY, eyeZ, 0.0, 0.0, 0.0, upX, upY, upZ)

    if shapeType == 1:
        glRotate(rotation, 0, 0, 1)
        glColor3f(0.6, 0.6, 0.6)
        vertices = Sph.calculateVertices()
        for i in range(len(vertices)):
            longitudeGroup = vertices[i]
            glBegin(GL_QUAD_STRIP)
            for j in range(len(longitudeGroup)):
                verticeGroup = longitudeGroup[j]
                glNormal3f(verticeGroup[0].x,
                           verticeGroup[0].y, verticeGroup[0].z)
                glVertex3f(verticeGroup[1].x,
                           verticeGroup[1].y, verticeGroup[1].z)
                glNormal3f(verticeGroup[2].x,
                           verticeGroup[2].y, verticeGroup[2].z)
                glVertex3f(verticeGroup[3].x,
                           verticeGroup[3].y, verticeGroup[3].z)
            glEnd()
    elif shapeType == 2:
        glRotate(45, 0, 1, 0)
        glRotate(rotation, 0, 0, 1)
        vertices = Cyl.calculateVertices()
        glColor3f(1.0, 0.4, 0.2)
        glBegin(GL_TRIANGLE_FAN)    # Draw Cover First
        for i in range(len(vertices[0])):
            glVertex(vertices[0][i].x, vertices[0][i].y, vertices[0][i].z)
        glEnd()
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_TRIANGLE_FAN)    # Draw Cover Second
        for i in range(len(vertices[1])):
            glVertex(vertices[1][i].x, vertices[1][i].y, vertices[1][i].z)
        glEnd()
        glColor3f(0.4, 1.0, 0.2)
        glBegin(GL_TRIANGLE_STRIP)  # Draw Sides
        for i in range(len(vertices[2])):
            glVertex(vertices[2][i].x, vertices[2][i].y, vertices[2][i].z)
        glEnd()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


def keyPressed(*args):
    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
    global shapeType, eyeX
    step = 0.1
    if args[0] == ESCAPE:
        sys.exit()
    elif args[0] == NUMPLUS:
        if shapeType == 1:
            Sph.increaseSubdivision()
        elif shapeType == 2:
            Cyl.increaseSubdivision()
    elif args[0] == NUMMINUS:
        if shapeType == 1:
            Sph.decreaseSubdivision()
        elif shapeType == 2:
            Cyl.decreaseSubdivision()
    elif args[0] == KEYW or args[0] == KEYWW:
        eyeX -= step
    elif args[0] == KEYS or args[0] == KEYSS:
        eyeX += step
    elif args[0] == NUM1:
        shapeType = 1
    elif args[0] == NUM2:
        shapeType = 2
    elif args[0] == KEYF or args[0] == KEYFF:
        eyeX = 3.0


def mouse(button, state, x, y):
    global isPressedMouseLeft, isPressedMouseRight
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        isPressedMouseLeft = 1
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        isPressedMouseLeft = 0
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        isPressedMouseRight = 1
    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        isPressedMouseRight = 0
    glutPostRedisplay()


def mouseMove(posX, posY):
    global mousePosX, mousePosY, eyeX, rotation
    # SHIFT=1  CTRL=2  ALT=4
    mod = glutGetModifiers()
    step = 0.1
    stepRotation = 1.0
    if mousePosX > posX:
        if isPressedMouseLeft == 1 and mod == 4:
            rotation -= stepRotation
        if isPressedMouseRight == 1 and mod == 4:
            eyeX += step
    else:
        if isPressedMouseLeft == 1 and mod == 4:
            rotation += stepRotation
        if isPressedMouseRight == 1 and mod == 4:
            eyeX -= step
    mousePosX = posX
    mousePosY = posY
    glutPostRedisplay()


def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(windowSizeX, windowSizeY)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(300, 200)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("CENG487 Assignment 2")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Register the function called when the mouse is pressed.
    glutMouseFunc(mouse)
    # Register the function called when the mouse is moved.
    glutMotionFunc(mouseMove)

    # Initialize our window.
    InitGL(windowSizeX, windowSizeY)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
