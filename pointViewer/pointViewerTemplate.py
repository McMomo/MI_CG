from tkinter import *
#from Canvas import *
import sys
import random

from OpenGL.raw.GL.VERSION.GL_1_0 import glOrtho, glFrustum
from OpenGL.raw.GLU import gluLookAt
from numpy import *
from OpenGL import *

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))

data = []

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    for i in data:
        x, y, z = i[0], i[1], i[2]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE, fill=COLOR, outline=COLOR)
        pointList.append(p)

    can.update()

def rotYp():
    """ rotate counterclockwise around y axis """
    global NOPOINTS
    NOPOINTS += 100
    print("In rotYp: ", NOPOINTS)
    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global NOPOINTS
    NOPOINTS -= 100
    print("In rotYn: ", NOPOINTS )
    can.delete(*pointList)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 2:
       print("pointViewerTemplate.py")
       sys.exit(-1)

    input = list()

    with open(sys.argv[1], "r") as file:
        for line in file.readlines():
            line = line.split()
            input.append(array([float(line[0]), float(line[1]), float(line[2])]))


    # 1. calculate the BoundaryBox
    bbox = {"top":input[0][1],"bottom":input[0][1],"right":input[0][0],"left":input[0][0], "far":input[0][0], "near":input[0][0]} # max(y), min(y), max(x), min(x), max(z), min(z)

    for vec in input:
        if vec[0] > bbox["right"]:
            bbox["right"] = vec[0]
        elif vec[0] < bbox["left"]:
            bbox["left"] = vec[0]

        if vec[1] > bbox["top"]:
            bbox["top"] = vec[1]
        elif vec[1] < bbox["bottom"]:
            bbox["bottom"] = vec[1]

        if vec[2] > bbox["far"]:
            bbox["far"] = vec[2]
        elif vec[2] < bbox["near"]:
            bbox["near"] = vec[2]


    # 2.
    # 2.1Put the middle of the Boundingbox in the origin (F.65?) &&
    '''
    bboxMedian = [median([bbox["right"], bbox["left"]]), median([bbox["top"], bbox["bottom"]])]
    for vec in input:
        data.append(matrix(vec) + matrix([[1, 0, 0], [0, 1, 0], [-bboxMedian[0], -bboxMedian[1], 1]]))

    print(data[0])
    '''

    glOrtho(bbox["left"],bbox["right"],bbox["bottom"],bbox["top"],bbox["near"],bbox["far"])

    # 2.2scale in to[-1, 1] ^ 3 (F.111)
    glFrustum(bbox["left"], bbox["right"],bbox["bottom"],bbox["top"],bbox["near"],bbox["far"])


    # 3.
    gluLookAt(2,2,2,0,0,0,0,1,0) # Einfach aus VL F.107

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
    
