import sys
from numpy import *
from colour import Color
from PIL import Image
import datetime
from raytrace import objects

BACKGROUND_COLOR = Color(rgb=(0,0,0))
wRes = 400
hRes = 400

class Ray(object): #S30
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction.normalized() #vector

    def __repr__(self):
        return "Ray(%s,%s)" %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


def calcRay(width, height): #S33
    pixelWidth = width / (wRes-1)
    pixelHeight = height /(hRes-1)
    for y in range(hRes):
        for x in range(wRes):
            xcomp = s.scale(x*pixelWidth - width/2)
            ycomp = u.scale(y*pixelHeight - height/2)
            ray = Ray(e, f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel


def rayCasting(imageWidth, imageHeight): #S31

    for x in range(imageWidth):
        for y in range(imageHeight):
            ray = calcRay(x,y)
            maxdist = float('inf')
            color = BACKGROUND_COLOR
            for object in objectlist:
                hitdist = object.intersectionParameter(ray)
                if hitdist:
                    if hitdist < maxdist:
                        maxdist = hitdist
                        color = object.colorAt(ray)
            image.putpixel((x,y), color)


if __name__ == "__main__":
    if len(sys.argv) <= 1 :
        sys.exit(1) #TODO error msg.
    if int(sys.argv[1]) == 1:
        print("Default Picture")

        objectlist = [
            objects.Plane(array([0, -1, 0, 1]), array([0,1,0,0]), (128, 128,128,)),
            objects.Sphere(array([-2, 1.5, -2, 1]), 1.5, (0, 255, 0)),
            objects.Sphere(array([2, 1.5, -2, 1], 1.5, (255, 0, 0))),
            objects.Sphere(array([0, 4.5, -2, 1], 1.5, (0, 0, 255))),
            objects.Triangle(array([-2, 1.5, -2, 1]), array([ 2, 1.5, -2, 1]), array([ 0, 4.5, -2, 1], (255, 255, 0)))
        ]

        lights = array([0,3,10,1])

        #TODO Scene aus Beispiel 1 == camera aus Beispiel 2



    elif int(sys.argv[1]) == 2:
        print("Image with reflection")
    elif int(sys.argv[1]) == 3:
        print("Image with checker floor")
    else:
        print("Which image do you want to see? \n1 == l. \t|\t 2 == m. \t|\t 3 == r")