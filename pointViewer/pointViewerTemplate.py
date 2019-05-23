import tkinter
import sys
import numpy

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
        #4. Transform to [0,0] x [WIDTH, HEIGHT]
        x, y = (1+i[0])*WIDTH/2.0, (1-i[1])*HEIGHT/2.0
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
            input.append(numpy.array([float(line[0]), float(line[1]), float(line[2])]))


    # 1. calculate the BoundaryBox
    bbox = {"top":input[0][1],"bottom":input[0][1],"right":input[0][0],"left":input[0][0], "far":input[0][2], "near":input[0][2]} # max(y), min(y), max(x), min(x), max(z), min(z)

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
    bboxMedian = [numpy.median([bbox["right"], bbox["left"]]), numpy.median([bbox["top"], bbox["bottom"]]), numpy.median([bbox["far"], bbox["near"]])]
    data = input - numpy.array([bboxMedian[0], bboxMedian[1], bboxMedian[2]])

    # 2.2 scale in to[-1, 1] ^ 3 (F.110) scale factor 2/max
    maxVec = max([bbox["right"]-bbox["left"], bbox["top"]-bbox["bottom"], bbox["far"]-bbox["near"]])
    data = data * (2/maxVec)

    # 3. Model to [-1, 1]^2 on x-y with "ortographischer Parallelprojektion
    #F.106 Grundriss -> einfach z weglassen

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
    
