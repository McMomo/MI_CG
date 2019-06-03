from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

from numpy import array
import sys, math

points = [[math.cos(i*math.pi/3), math.sin(i*math.pi/3)] for i in range(6)]

vbo = vbo.VBO(array(points, 'f'))

def initGL(width, height):
    glClearColor(0.0, 0.0, 0.1, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(.75, .75, .75)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    vbo.bind()
    glVertexPointerf(vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_LINES, 0, 14)  # GL_TRIANGLES, GL_TRIANGLE_STRIP
    vbo.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glFlush()


def main():
    height, width = 500, 500
    #calcPoints()

    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow("GL_TRIANGLES")

    glutDisplayFunc(display)

    initGL(width, height)

    glutMainLoop()


def calcPoints():
    h = math.sqrt(0.75) / 7
    j = 0
    for i in range(5):
        i = i / 7
        if i == 2 / 7:
            # Tri look up
            points.append([(-1 / 7 + i, -1 / 7 + j), 0.0])
            points.append([(0.0 + i, -1 / 7 + j), 0.0])
            points.append([(-0.5 / 7 + i, h - 1 / 7 + j), 0.0])
            # Tri look down
            points.append([(0.0 + i, -1 / 7 + j), 0.0])
            points.append([(-0.5 / 7 + i, h - 1 / 7 + j), 0.0])
            points.append([(0.5 / 7 + i, h - 1 / 7 + j), 0.0])
            j = h
            i += 1 / 7
        # Tri look up
        points.append([(-1 / 7 + i, -1 / 7 + j), 0.0])
        points.append([(0.0 + i, -1 / 7 + j), 0.0])
        points.append([(-0.5 / 7 + i, h - 1 / 7 + j), 0.0])
        # Tri look down
        points.append([(0.0 + i, -1 / 7 + j), 0.0])
        points.append([(-0.5 / 7 + i, h - 1 / 7 + j), 0.0])
        points.append([(0.5 / 7 + i, h - 1 / 7 + j), 0.0])


if __name__ == "__main__":
    main()