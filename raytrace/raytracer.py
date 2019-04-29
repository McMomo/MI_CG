import sys
from numpy import *
from colour import Color
from PIL import Image
import datetime
from raytrace import objects

BACKGROUND_COLOR = Color(rgb=(0,0,0))
WIDTH = 400
HEIGHT = 400

image = None
camera = []
lights = []

class Ray(object): #S30
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction/ np.linalg.norm(direction) #vector

    def __repr__(self):
        return "Ray(%s,%s)" %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


def calcRay(width, height): #S33
    pixelWidth = width / (WIDTH-1)
    pixelHeight = height /(HEIGHT-1)
    for y in range(HEIGHT):
        for x in range(WIDTH):

            f = camera[1]-camera[0]
            f = f / np.linalg.norm(f)
            s = np.cross(f, camera[2])
            s = s / np.linalg.norm(s)
            u = np.cross(s, f)

            xcomp = np.multiply(s,(x*pixelWidth - width/2))
            ycomp = np.multiply(u,(y*pixelHeight - height/2))
            ray = Ray(e, f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel

            yield ray



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
            objects.Plane(array([0, -1, 0, 1]), array([0,1,0,0]),  Color(rgb=(1/128, 1/128, 1/128,))),
            objects.Sphere(array([-2, 1.5, -2, 1]), 1.5,  Color(rgb=(0, 1/255, 0))),
            objects.Sphere(array([2, 1.5, -2, 1]), 1.5,  Color(rgb=(1/255, 0, 0))),
            objects.Sphere(array([0, 4.5, -2, 1]), 1.5,  Color(rgb=(0, 0, 1/255))),
            objects.Triangle(array([-2, 1.5, -2, 1]), array([ 2, 1.5, -2, 1]), array([ 0, 4.5, -2, 1]),  Color(rgb=(1/255, 1/255, 0)))
        ]

        lights = [array([30,30,10]), Color(rgb=(1/255,1/255,1/255))]

        camera = [array([0,1.8,10]),array([0,3,0]), array([0,1,0]), 45] #e, c, up, fov

        if len(sys.argv >= 3):
            HEIGHT = sys.argv[2]
            WIDTH = sys.argv[3]


        image = Image.new("RGB", (HEIGHT, WIDTH), BACKGROUND_COLOR)
        rayCasting(WIDTH, HEIGHT)



    elif int(sys.argv[1]) == 2:
        print("Image with reflection")
    elif int(sys.argv[1]) == 3:
        print("Image with checker floor")
    else:
        print("Which image do you want to see? \n1 == l. \t|\t 2 == m. \t|\t 3 == r")