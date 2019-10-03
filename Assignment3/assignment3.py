# CENG 487 Assignment# by
# Fatma UYSAL
# StudentId: 220201051
# 04 2019

'''
Use NUM+ and NUM- keys to change subdivision count:
Key NUM+: Increases subdivision count
Key NUM-: Decreases subdivision count

Use Arrow Keys to rotate:
Arrow left key : Rotates clockwise
Arrow right key: Rotates counterclockwise 

Use Alt Key + Mouse Right Button to zoom:
To shift to left : Zoom out
To shift to right: Zoom in

Use F key for resetting the view to fully enclose the primitive on screen.
'''

import sys
import obj
from math import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *

# ESCAPE Key = 27
ESCAPE = '\033'
# NUM+ Key = 43
NUMPLUS = '\053'
# NUM- Key = 45
NUMMINUS = '\055'
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

mousePosX = 0
mousePosY = 0
isPressedMouseLeft = 0
isPressedMouseRight = 0

zoom = 6.0
rotation = 0


def InitGL(Width, Height):
    # We call this right after our OpenGL window is created.

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

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    z = -(objFile.biggest * zoom)
    glTranslatef(0.0, 0.0, z)
    glRotate(35, 1, 0, 0)
    glRotate(rotation, 0, 1, 0)

    c = 0.0
    for i in range(len(objFile.polygons)):
        polygon = objFile.polygons[i]
        c = (c + 0.1) % 1
        if c < 0.2:
            c = 0.6
        elif c > 0.6:
            c = 0.2
        # Draw a polygon
        glBegin(GL_POLYGON)
        for j in range(len(polygon)):
            glColor3f(c, c + 0.05, c + 0.10)
            glVertex3f(polygon[j].x, polygon[j].y, polygon[j].z)
        glEnd()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


def keyPressed(*args):
    # The function called whenever a key is pressed.
    global zoom
    step = 0.1
    if args[0] == ESCAPE:
        sys.exit()
    elif args[0] == NUMPLUS:
        objFile.increaseSubdivision()
    elif args[0] == NUMMINUS:
        objFile.increaseSubdivision()
    elif args[0] == KEYW or args[0] == KEYWW:
        zoom -= step
    elif args[0] == KEYS or args[0] == KEYSS:
        zoom += step
    elif args[0] == KEYF or args[0] == KEYFF:
        zoom = 6.0


def specialKeyPressed(key, x, y):
    # The function called whenever a special key is pressed.
    global rotation
    stepRotation = 1.0
    if key == GLUT_KEY_RIGHT:
        rotation += stepRotation
    if key == GLUT_KEY_LEFT:
        rotation -= stepRotation
    glutPostRedisplay()


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
    global mousePosX, mousePosY, zoom, rotation
    # SHIFT=1  CTRL=2  ALT=4
    mod = glutGetModifiers()
    step = 0.1
    stepRotation = 1.0
    if mousePosX > posX:
        if isPressedMouseLeft == 1 and mod == 4:
            rotation -= stepRotation
        if isPressedMouseRight == 1 and mod == 4:
            zoom += step
    else:
        if isPressedMouseLeft == 1 and mod == 4:
            rotation += stepRotation
        if isPressedMouseRight == 1 and mod == 4:
            zoom -= step
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
    window = glutCreateWindow("CENG487 Assignment 3")

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

    # The callback function for keyboard controls
    glutSpecialFunc(specialKeyPressed)

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
print "To increase subdivision count press Shift and + buttons"
print "To rotate object clockwise press Shift and left arrow keys or Alt key and left mouse click"
print "To rotate object counterclockwise press Shift and right arrow keys or Alt key and left mouse click"
print "To make zoom press Alt key and right mouse click"
print "To resetting the view press F key "
objFile = obj.Obj()
if len(sys.argv) > 1:
    objFile.load(sys.argv[1])
else:
    objFile.load("ecube.obj")
# objFile.load("tori.obj")

# python assignment3.py tori.obj
main()
