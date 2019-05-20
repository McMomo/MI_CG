from Tkinter import *
from Canvas import *
import sys
import random
from numpy import *

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

    data = list()

    with open(sys.argv[1], "r") as file:
        for line in file.readlines():
            line = line.split()
            data.append(array([float(line[0]), float(line[1]), float(line[2])]))


    bbox = {"top":data[0][1],"bottom":data[0][1],"right":data[0][0],"left":data[0][0]} # max(y), min(y), max(x), min(x)

    for vec in data:
        if vec[0] > bbox["right"]:
            bbox["right"] = vec[0]
        elif vec[0] < bbox["left"]:
            bbox["left"] = vec[0]

        if vec[1] > bbox["top"]:
            bbox["top"] = vec[1]
        elif vec[1] < bbox["bottom"]:
            bbox["bottom"] = vec[1]

    dataOrigin = array([bbox["left"], bbox["bottom"], 0])
    origin = array([0, 0, 0])

    dif = origin - dataOrigin

    print("Dif: ",dif)

    print("bbox: ",bbox)

    print("data: ", data[0])

    for vec in data: #FIXME Wie auf Folie Seite 65 -> so ist die transformation/verscheibung falsch
        vec += dif

    print("data + dif : ", data[0])

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
    
