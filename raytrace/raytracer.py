import sys
from numpy import *
from PIL import Image
import datetime
from raytrace import objects

BACKGROUND_COLOR = (0,0,0)
WIDTH = 400
HEIGHT = 400

image = None
camera = []
lights = []

class Ray(object): #S30
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction/ linalg.norm(direction) #vector

    def __repr__(self):
        return "Ray(%s,%s)" %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + multiply(self.direction,t)


def calcRay(width, height): #S33
    global camera

    f = camera[1] - camera[0]
    f = f / linalg.norm(f)

    s = cross(f, camera[2])
    s = s / linalg.norm(s)

    u = cross(s, f)

    pixelWidth = width / (WIDTH-1)
    pixelHeight = height /(HEIGHT-1)

    for y in range(HEIGHT):
        for x in range(WIDTH):

            xcomp = multiply(s,(x*pixelWidth - width/2))
            ycomp = multiply(u,(y*pixelHeight - height/2))
            ray = Ray(camera[0], f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel

            return ray



def rayCasting(imageWidth, imageHeight): #S31


    for x in range(imageWidth):
        for y in range(imageHeight):
            ray = calcRay(x,y)
            maxdist = 5 #float('inf')
            color = BACKGROUND_COLOR
            for object in objectlist:

                hitdist = object.intersectionParamter(ray)
                if hitdist:
                    if hitdist < maxdist:
                        maxdist = hitdist
                        color = object.colorAt(ray)

            image.putpixel((x,y), color)


def rayTracing():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            ray = calcRay(x, y) # cameraParamter in glob camera
            #TODO implement raytracing from S.47


if __name__ == "__main__":
    if len(sys.argv) <= 1 :
        sys.exit(1) #TODO error msg.
    elif len(sys.argv) >= 3:
         HEIGHT = sys.argv[2]
         WIDTH = sys.argv[3]

    if int(sys.argv[1]) == 1:
        print("Default Picture, start process ...")


        #TODO Vektor punkte von Hennock einsetzten
        objectlist = [
            objects.Plane(array([0, HEIGHT/-1, 0]), array([0, HEIGHT/1, 0]), (128, 128, 128,)),
            objects.Sphere(array([HEIGHT/-2, HEIGHT/1.5, HEIGHT/-2]), HEIGHT/1.5,  (0, 255, 0)),
            objects.Sphere(array([HEIGHT/2, HEIGHT/1.5, HEIGHT/-2]), HEIGHT/1.5,  (255, 0, 0)),
            objects.Sphere(array([0, HEIGHT/4.5, HEIGHT/-2]), HEIGHT/1.5,  (0, 0, 255)),
            objects.Triangle(array([HEIGHT/-2, HEIGHT/1.5, HEIGHT/-2]), array([ HEIGHT/2, HEIGHT/1.5, HEIGHT/-2]), array([ 0, HEIGHT/4.5, HEIGHT/-2]),  (255, 255, 0))
        ]

        lights = [array([30,30,10]), (255,255,255)]

        camera = [array([0,1.8,10]),array([0,3,0]), array([0,1,0]), 45] #e, c, up, fov


        image = Image.new("RGB", (HEIGHT, WIDTH))
        rayCasting(WIDTH, HEIGHT)
        image.save('./out.png')

        print("... finish.")

    elif int(sys.argv[1]) == 2:
        print("Image with reflection")
    elif int(sys.argv[1]) == 3:
        print("Image with checker floor")
    else:
        print("Which image do you want to see? \n1 == l. \t|\t 2 == m. \t|\t 3 == r")