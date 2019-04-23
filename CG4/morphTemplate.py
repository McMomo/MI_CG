from Tkinter import *
from Canvas import *
import sys

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

polygon = [[50,50],[350,50],[350,350],[50,350],[50,50]]

polygonA = []
polygonZ = []

#TODO: Olgon A und Z liste anlegen
#Vektor (lineare Interpolation) berechnen und auf forward/backward Verctor entlangwandern = morph


time = 0
dt = 0.01

def drawObjekts():
    """ draw polygon and points """
    # TODO: inpterpolate between polygons and render
    for (p,q) in zip(polygon,polygon[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1],fill=CCOLOR))
        elementList.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE, p[0]+HPSIZE, p[1]+HPSIZE, fill=CCOLOR, outline=CCOLOR))
            


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    del elementList[:]
    drawObjekts()
    can.update()


def forward(): # from A to Z
    global time, polygonZ, polygonA, polygon

    # I(t) = (1-t)p+tq


    while(time<1):
        time += dt
        # TODO: interpolate
        polygon[:] = []

        for a,z in zip(polygonA, polygonZ):
            polygon.append([(1-time)*a[0]+time*z[0], (1-time)*a[1]+time*z[1]])

        #print(time)
        draw()


def backward(): # from Z to A
    global time, polygonA, polygonZ, polygon



    while(time>0):
        time -= dt
        # TODO: interpolate
        polygon[:] = []

        for a,z in zip(polygonA, polygonZ):
            polygon.append([(1-time)*a[0]+time*z[0], (1-time)*a[1]+time*z[1]])

        if time < 0.1: # to fix the missing foot, because len(PolA) > len(PolZ)
            polygon.append(polygonA[-1])

        #print(time)
        draw()
    

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 3:
       print ("morph.py firstPolygon secondPolygon")
       sys.exit(-1)

    # TODOS:
    # - read in polygons
    # - transform from local into global coordinate system 
    # - make both polygons contain same number of points

    # create main window
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    draw()


    fileZ = open("polygonZ.dat")
    for line in fileZ.readlines():
        polygonZ.insert(0, [float(line.split()[0]) * WIDTH, float(line.split()[1]) * HEIGHT])

    fileA = open("polygonA.dat")
    for line in fileA.readlines():
        polygonA.insert(0, [float(line.split()[0]) * WIDTH, float(line.split()[1]) * HEIGHT])

    # start
    mw.mainloop()
    
