import tkinter
import sys
import numpy as np

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))

points = []

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    global points
    for i in points:
        x, y = i[0], i[1]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE, fill=COLOR, outline=COLOR)
        pointList.append(p)

    can.update()

def rotYp():
    """ rotate counterclockwise around y axis """
    global points
    can.delete(*pointList)

    #FIXME rotation like on a vinyl with [0, 1, 0]
    theta = np.pi / 6
    c, s = np.cos(theta), np.sin(theta)

    rotMat = np.array([[c, 0, -s], rotationAxis, [s, 0, c]])

    #v = theta * rotationAxis

    #r = np.array([[0, 0, v], [-v, 0, 0], [0, 0, 0]])

    #points = [p + np.dot(p, r) for p in points]

    points = np.dot(points, rotMat)

    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global points
    can.delete(*pointList)

    # FIXME rotation like on a vinyl with [0, 1, 0]
    theta = -(np.pi / 6)
    c, s = np.cos(theta), np.sin(theta)

    rotMat = np.array([[c, 0, -s], rotationAxis, [s, 0, c]])

    points = [np.dot(p, rotMat) for p in points]

    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 2:
       print("pointViewerTemplate.py")
       sys.exit(-1)

    points = list()

    with open(sys.argv[1], "r") as file:
        for line in file.readlines():
            line = line.split()
            points.append(np.array([float(line[0]), float(line[1]), float(line[2])]))


    # 1. calculate the BoundaryBox
    vecX = [vec[0] for vec in points]
    vecY = [vec[1] for vec in points]
    vecZ = [vec[2] for vec in points]

    bbox = {"right": max(vecX), "left": min(vecX),
            "top": max(vecY), "bottom": min(vecY),
            "far":max(vecZ), "near":min(vecZ)}

    # 2.
    # 2.1Put the middle of the Boundingbox in the origin
    bboxMedian = [np.median([bbox["right"], bbox["left"]]), np.median([bbox["top"], bbox["bottom"]]), np.median([bbox["far"], bbox["near"]])]
    points = points - np.array([bboxMedian[0], bboxMedian[1], bboxMedian[2]])

    # 2.2 scale in to[-1, 1]^3 | scale factor is 2/maxDiagonal
    maxVec = max([bbox["right"]-bbox["left"], bbox["top"]-bbox["bottom"], bbox["far"]-bbox["near"]])
    points = points * (2.0 / maxVec)

    # 4. Transform to [0,0] x [WIDTH, HEIGHT]
    for vec in points:
        vec[0] = (1 + vec[0]) * WIDTH / 2.0
        vec[1] = (1 - vec[1]) * HEIGHT / 2.0
        vec[2] = (1 + vec[2]) * HEIGHT / 2.0 #FIXME Height or Width? Step 3. said otherwise


    #Get rotaion axis FIXME i need to get the middle of x and z not the y-axis
    max = np.amax(points, 0)
    min = np.amin(points, 0)

    rotationAxis = np.array([min[0] + (max[0] - min[0]) / 2,
                             1,
                             min[2] + (max[2] - min[2]) / 2])

    # create main window
    mw = tkinter.Tk()

    # create and position canvas and buttons
    cFr = tkinter.Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = tkinter.Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = tkinter.Frame(mw)
    bFr.pack(side="left")
    bRotYn = tkinter.Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = tkinter.Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = tkinter.Frame(mw)
    eFr.pack(side="right")
    bExit = tkinter.Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
    
