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

class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction/linalg.norm(direction) #vector

    def __repr__(self):
        return "Ray({},{})".format(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + multiply(self.direction,t)

    def reflect(self, vec, other):
        other = other / linalg.norm(other)
        return  vec - multiply(2, multiply(multiply(vec, other),other))


def calcRay(x, y): #S33
    global camera, WIDTH, HEIGHT
    pixelWidth = WIDTH/ (camera.res-1)
    pixelHeight = HEIGHT /(camera.res -1)
    xcomp = multiply(camera.s,(x*pixelWidth - WIDTH/2))
    ycomp = multiply(camera.u,(y*pixelHeight - HEIGHT/2))
    return Ray(camera.e, camera.f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel

################################################

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

###############################################


def rayTracing():
    for x in range(res):
        for y in range(res):
            ray = calcRay(x, y) # cameraParamter in glob camera
            color = tuple(int(f) for f in traceRay(0, ray))
            image.putpixel((x,y), color)


def traceRay(level, ray):
    hitPointData = intersect(level, ray, maxlevel) # maxLevel = maximale Rekursions-Tiefe
    if hitPointData is not None:
        return shade(level, hitPointData)
    return BACKGROUND_COLOR


def shade(level, hitPointData):
    directColor = computeDirectLight(hitPointData)

    reflcetedRay = computeReflectedRay(hitPointData)
    reflcetedColor = traceRay(level+1, reflcetedRay)

    return directColor + reflcetedColor

def computeReflectedRay(hitPointData):
    ray, obj, hitdist, level = hitPointData

    intersectionPt = ray.pointAtParameter(hitdist)

    surfaceNorm = obj.normalAt(intersectionPt)

    # specualr (reflective) light
    reflectedRay = Ray(intersectionPt,
                       ray.reflect(ray.direction, surfaceNorm) / linalg.norm(ray.reflect(ray.direction, surfaceNorm)))

    return reflectedRay

def computeDirectLight(hitPointData):
    ray, obj, hitdist, level = hitPointData

    color = (0,0,0)

    intersectionPt = ray.pointAtParameter(hitdist)
    #intersectionPt = intersectionPt / linalg.norm(intersectionPt) # lieber nicht normalisieren
    #objColor = array(obj.colorAt()) #TODO objColor != surface nrom
    surfaceNorm = obj.normalAt(intersectionPt)

    #ambient light
    color = multiply(obj.material.color ,obj.material.ambient)


    #lambert shading
    for light in lights:
        ptTpLiVec = (light - intersectionPt) / linalg.norm(light - intersectionPt)
        ptToLiRay = Ray(intersectionPt, ptTpLiVec)
        hitPointData = None
        hitPointData = intersect(0, ptToLiRay, maxlevel)
        if hitPointData is None:
            #lambertIntensity = multiply(surfaceNorm, ptTpLiVec) # i do not want lamb..In.. to be a Vector. it should be a single number
            lambertIntensity = surfaceNorm[0] * ptTpLiVec[0] + surfaceNorm[1] * ptTpLiVec[1] + surfaceNorm[2] * ptTpLiVec[2]

            if lambertIntensity > 0:
                color += multiply(multiply(obj.material.color, obj.material.lambert), lambertIntensity)

    return color

def intersect(level, ray, maxlevel):
    if level >= maxlevel:
        return None

    maxdist = float('inf')
    hitPointData = None

    for obj in objectlist:
        hitdist = obj.intersectionParamter(ray)
        if hitdist and hitdist >= 0:
            if .001 < hitdist < maxdist:
                maxdist = hitdist
                hitPointData = ray, obj, hitdist, level

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
            objects.Plane(array([0,0,0]), up, objects.Material((128, 128, 128))),
            objects.Sphere(array([0, top, z]), radius, objects.Material((0, 255, 0))),
            objects.Sphere(array([-side, 0, z]), radius, objects.Material((255, 0, 0))),
            objects.Sphere(array([side, 0, z]), radius, objects.Material((0, 0, 255))),
            objects.Triangle(array([0, top, z]), array([side, 0, z-20]), array([-side, 0, z -20]), objects.Material((255, 255, 0)))

        ]



        lights = [array([40,200,0])]

        camera = Camera(array([0,50,0]), up, array([0,top/2, z]), fov, res) # war e, c, up ist e, up c

        image = Image.new("RGB", (res, res))

        #rayCasting(res, res)
        rayTracing()

        image.save('./result/result_{}.png'.format(datetime.datetime.now()))

        print("... finish.")

    elif int(sys.argv[1]) == 2:
        print("Image with reflection")
    elif int(sys.argv[1]) == 3:
        print("Image with checker floor")
    else:
        print("Which image do you want to see? \n1 == l. \t|\t 2 == m. \t|\t 3 == r")