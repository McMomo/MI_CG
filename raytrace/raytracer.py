import sys
from numpy import *
from PIL import Image
import datetime
from raytrace import objects

BACKGROUND_COLOR = (0,0,0)
WIDTH = 0
HEIGHT = 0

image = None
camera = None
lights = []

maxlevel = 3

class Camera(object):
    def __init__(self, e, up, c, fov, res):
        global HEIGHT, WIDTH

        self.e = e
        self.up = up
        self.c = c
        self.fov = fov
        self.res = res

        self.f = c - e / linalg.norm(c - e)
        self.s = cross(self.f , up) / linalg.norm(cross(self.f , up))
        self.u = cross(self.s, self.f)


        self.aspectratio = res/res
        self.alpha = fov/2
        HEIGHT = 2*tan(self.alpha)
        WIDTH = self.aspectratio * HEIGHT


def calcRay(x, y): #S33
    global camera, WIDTH, HEIGHT
    pixelWidth = WIDTH/ (camera.res-1)
    pixelHeight = HEIGHT /(camera.res -1)
    xcomp = multiply(camera.s,(x*pixelWidth - WIDTH/2))
    ycomp = multiply(camera.u,(y*pixelHeight - HEIGHT/2))
    return objects.Ray(camera.e, camera.f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel


def rayCasting(imageWidth, imageHeight):
    for x in range(imageWidth):
        for y in range(imageHeight):
            ray = calcRay(x,y)
            maxdist =  float('inf')
            color = BACKGROUND_COLOR
            for object in objectlist:
                hitdist = object.intersectionParamter(ray)
                if hitdist:
                    if .001 < hitdist < maxdist:
                        maxdist = hitdist
                        color = object.colorAt(ray)
            image.putpixel((x,y), color)




def rayTracing():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            ray = calcRay(x, y) # cameraParamter in glob camera
            color = traceRay(0, ray)
            image.putpixel((x,y), color)


def traceRay(level, ray):
    hitPointData = intersect(level, ray, maxlevel) # maxLevel = maximale Rekursions-Tiefe
    if hitPointData:
        return shade(level, hitPointData)
    return BACKGROUND_COLOR


def shade(level, hitPointData):
    directColor = computeDirectLight(hitPointData)

    reflcetedRay = computeReflectedRay(hitPointData)
    reflcetedColor = traceRay(level+1, reflcetedRay)

    return directColor + reflection*reflcetedColor

def intersect(level, ray, maxlevel):
    if level >= maxlevel:
        return None

    maxdist = float('inf')
    hitPointData = None

    for o in objects:
        hitdist = o.intersectParameter
        if hitdist and hitdist >= 0:
            if hitdist < maxdist:
                maxdist = hitdist
                hitPointData = o.colorAt(ray)

    return hitPointData


if __name__ == "__main__":
    if len(sys.argv) <= 1 :
        sys.exit(1) #TODO error msg.

    if int(sys.argv[1]) == 1:
        print("Default Picture, start process ...")

        up = array([0,1,0])
        radius = 30
        side = 40
        top = 1.75 * side
        z = 500

        res = 200
        fov = 45

        objectlist = [
            objects.Plane(array([0,0,0]), up, (128, 128, 128)),
            objects.Sphere(array([0, top, z]), radius, (0, 255, 0)),
            objects.Sphere(array([-side, 0, z]), radius, (255, 0, 0)),
            objects.Sphere(array([side, 0, z]), radius, (0, 0, 255)),
            objects.Triangle(array([0, top, z]), array([side, 0, z-20]), array([-side, 0, z -20]), (255, 255, 0))

        ]



        lights = [array([40,200,0]), (255,255,255)]

        camera = Camera(array([0,50,0]), up, array([0,top/2, z]), fov, res) # war e, c, up ist e, up c

        image = Image.new("RGB", (res, res))
        rayCasting(res, res)
        image.save('./out.png')

        print("... finish.")

    elif int(sys.argv[1]) == 2:
        print("Image with reflection")
    elif int(sys.argv[1]) == 3:
        print("Image with checker floor")
    else:
        print("Which image do you want to see? \n1 == l. \t|\t 2 == m. \t|\t 3 == r")