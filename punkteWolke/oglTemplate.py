from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math, os
import numpy as np

EXIT = -1
FIRST = 0

points = list()


def init(width, height):
   """ Initialize an OpenGL window """
   glClearColor(1.0, 1.0, 1.0, 0.0)         #background color
   glMatrixMode(GL_PROJECTION)              #switch to projection matrix
   glLoadIdentity()                         #set to 1
   glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0) #multiply with new p-matrix
   glMatrixMode(GL_MODELVIEW)               #switch to modelview matrix

   #Camera
   gluPerspective(30, 1, 1, 50)
   gluLookAt(0, 0, 4, 0, 0, 0, 0, 1, 0)



def display():
   global points
   """ Render all objects"""
   glClear(GL_COLOR_BUFFER_BIT) #clear screen
   glColor(0.0, 0.0, 1.0)       #render stuff

   #draw
   glBegin(GL_POINTS)
   for xyz in points:
      x, y, z = xyz
      glVertex3f(x, y, z)
   glEnd()

   glutSwapBuffers()            #swap buffer


def reshape(width, height):
   """ adjust projection matrix to window size"""
   glViewport(0, 0, width, height)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if width <= height:
       glOrtho(-1.5, 1.5,
               -1.5*height/width, 1.5*height/width,
               -1.0, 1.0)
   else:
       glOrtho(-1.5*width/height, 1.5*width/height,
               -1.5, 1.5,
               -1.0, 1.0)
   glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
   key = str(key)
   key = key.split('\'')[1]
   """ handle keypress events """
   if key == chr(27) or key == chr(113): # chr(27) = ESCAPE chr(113) = q
       sys.exit(0)
   elif key == chr(120): # x
      glRotatef(2, 1, 0, 0)
   elif key == chr(121): # y
      glRotatef(2, 0, 1, 0)
   elif key == chr(122): # z
      glRotatef(2, 0, 0, 1)
   display()


def mouse(button, state, x, y):
   """ handle mouse events """
   if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       print("left mouse button pressed at ", x, y)


def mouseMotion(x,y):
   """ handle mouse motion """
   print("mouse motion at ", x, y)


def menu_func(value):
   """ handle menue selection """
   print("menue entry ", value, "choosen...")
   if value == EXIT:
       sys.exit()
   glutPostRedisplay()


def process_input(filepath):
   global points
   with open(filepath, "r") as file:
      for line in file.readlines():
         line = line.split()
         points.append(np.array([float(line[0]), float(line[1]), float(line[2])]))

   # Bounding Box
   vecX = [vec[0] for vec in points]
   vecY = [vec[1] for vec in points]
   vecZ = [vec[2] for vec in points]

   bbox = {"right": max(vecX), "left": min(vecX),
            "top": max(vecY), "bottom": min(vecY),
            "far": max(vecZ), "near": min(vecZ)}

   #Put the middle of the Boundingbox in the origin
   points = points - np.array([np.median([bbox["right"], bbox["left"]]),
                               np.median([bbox["top"], bbox["bottom"]]),
                               np.median([bbox["far"], bbox["near"]])])

   #scale in to[-1, 1]^3 | scale factor is 2/maxDiagonal
   maxVec = max([bbox["right"] - bbox["left"], bbox["top"] - bbox["bottom"], bbox["far"] - bbox["near"]])
   points = points * (2.0 / maxVec)


def main():
   # Hack for Mac OS X
   cwd = os.getcwd()
   glutInit(sys.argv)
   os.chdir(cwd)

   process_input(sys.argv[1])

   glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
   glutInitWindowSize(500, 500)
   glutCreateWindow("simple openGL/GLUT template")

   glutDisplayFunc(display)     #register display function
   glutReshapeFunc(reshape)     #register reshape function
   glutKeyboardFunc(keyPressed) #register keyboard function 
   glutMouseFunc(mouse)         #register mouse function
   glutMotionFunc(mouseMotion)  #register motion function
   glutCreateMenu(menu_func)    #register menue function

   glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
   glutAddMenuEntry("EXIT",EXIT)         #Add another menu entry
   glutAttachMenu(GLUT_RIGHT_BUTTON)     #Attach mouse button to menue

   init(500,500) #initialize OpenGL state

   glutMainLoop() #start even processing


if __name__ == "__main__":
   main()
