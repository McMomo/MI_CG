import sys
from numpy import *
from PIL import Image
import datetime
from raytrace import objects

BACKGROUND_COLOR = (0,0,0)

image = None
camera = None
lights = []

maxlevel = 3


class Camera(object):
    def __init__(self, e, up, c, fov, res):

        self.e = e
        self.up = up
        self.c = c
        self.fov = fov
        self.res = res

        self.f = (c - e) / linalg.norm(c - e)
        self.s = cross(self.f , up) / linalg.norm(cross(self.f , up))
        self.u = cross(self.s, self.f)

        self.aspectratio = res/res
        self.alpha = fov/2
        self.height = 2 * tan(self.alpha)
        self.width = self.aspectratio * self.height


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction/linalg.norm(direction) #vector

    def __repr__(self):
        return "Ray({},{})".format(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + multiply(self.direction,t)

    def reflect(self, other): #TODO compare with others
        other = other / linalg.norm(other)
        return  self.direction - multiply(2, multiply(multiply(self.direction, other),other))


def render():
    for x in range(res):
        for y in range(res):
            ray = calcRay(x, y)
            color = tuple(int(f) for f in traceRay(0, ray))
            image.putpixel((x, y), color)


def calcRay(x, y):
    global camera
    pixelWidth = camera.width / (camera.res - 1)
    pixelHeight = camera.height / (camera.res - 1)
    xcomp = multiply(camera.s, (x * pixelWidth - camera.width / 2))
    ycomp = multiply(camera.u, (y * pixelHeight - camera.height / 2))
    return Ray(camera.e, camera.f + xcomp + ycomp) # evtl. mehrere Strahlen pro Pixel


def traceRay(level, ray):
    hitPointData = intersect(level, ray, maxlevel) # maxLevel = maximale Rekursions-Tiefe
    if hitPointData is not None:
        return shade(level, hitPointData)
    return BACKGROUND_COLOR


def shade(level, hitPointData):
    ray, obj, hitdist, level = hitPointData
    directColor = computeDirectLight(hitPointData)

    # if not reflective return black
    if obj.material.reflective == True:
        reflcetedRay = computeReflectedRay(hitPointData)
        reflcetedColor = multiply(traceRay(level+1, reflcetedRay), obj.material.ambient)
    else:
        reflcetedColor = array([0,0,0])

    return directColor + reflcetedColor


def computeReflectedRay(hitPointData):
    ray, obj, hitdist, level = hitPointData
    intersectionPt = ray.pointAtParameter(hitdist)
    surfaceNorm = obj.normalAt(intersectionPt)

    # specualr (reflective) light
    reflectedRay = Ray(intersectionPt,
                       ray.reflect(surfaceNorm) / linalg.norm(ray.reflect(surfaceNorm)))
    return reflectedRay


def computeDirectLight(hitPointData):
    ray, obj, hitdist, level = hitPointData
    color = (0,0,0)
    intersectionPt = ray.pointAtParameter(hitdist)
    surfaceNorm = obj.normalAt(intersectionPt)

    # get texture
    if obj.material.texture is None:
        surfaceColor = obj.material.color
    else:
        surfaceColor = obj.material.texture.baseColorAt(intersectionPt)

    #ambient light
    color = multiply(surfaceColor ,obj.material.ambient)

    #lambert shading
    for light in lights:
        ptTpLiVec = (light - intersectionPt) / linalg.norm(light - intersectionPt)
        ptToLiRay = Ray(intersectionPt, ptTpLiVec)
        hitPointData = None
        hitPointData = intersect(0, ptToLiRay, maxlevel)
        if hitPointData is None:
            #lambertIntensity should be a single number
            lambertIntensity = surfaceNorm[0]*ptTpLiVec[0] + surfaceNorm[1]*ptTpLiVec[1] + surfaceNorm[2]*ptTpLiVec[2]

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
            if .0001 < hitdist < maxdist:
                maxdist = hitdist
                hitPointData = ray, obj, hitdist, level

    return hitPointData


if __name__ == "__main__":
    if len(sys.argv) <= 1 :
        sys.exit(1) #TODO error msg.

    res = 800

    up = array([0, 1, 0])
    radius = 60
    side = 80
    top = 1.75 * side
    z = 500
    fov = -45

    camera = Camera(array([0, 50, 0]), up, array([0, top / 2, z]), fov, res)  # e, up, c, fov, res
    image = Image.new("RGB", (res, res))

    if sys.argv[1] == "light":
        print("Image with light ...")
        objectlist = [
            objects.Plane(array([0, -top ,0]), up, objects.Material((128, 128, 128))),
            objects.Sphere(array([0, top, z-radius]), radius, objects.Material((0, 0, 255))),
            objects.Sphere(array([-side, 0, z-radius]), radius, objects.Material((0, 255, 0) )),
            objects.Sphere(array([side, 0, z-radius]), radius, objects.Material((255, 0, 0) )),
            objects.Triangle(array([0, top, z]), array([side, 0, z]), array([-side, 0, z]),
                             objects.Material((255, 255, 0)))
        ]
        lights = [array([300,300,100])]

    elif sys.argv[1] == "reflection":
        print("Image with reflection ...")
        objectlist = [
            objects.Plane(array([0, -top, 0]), up, objects.Material((128, 128, 128), reflective=True)),
            objects.Sphere(array([0, top, z - radius]), radius, objects.Material((0, 0, 255), reflective=True)),
            objects.Sphere(array([-side, 0, z - radius]), radius, objects.Material((0, 255, 0), reflective=True)),
            objects.Sphere(array([side, 0, z - radius]), radius, objects.Material((255, 0, 0), reflective=True)),
            objects.Triangle(array([0, top, z]), array([side, 0, z]), array([-side, 0, z]),
                             objects.Material((255, 255, 0)))
        ]
        lights = [array([300, 300, 100])]

    elif sys.argv[1] == "texture":
        print("Image with texture ...")
        objectlist = [
            objects.Plane(array([0, -top, 0]), up, objects.Material((128, 128, 128), reflective=True, texture=objects.CheckerboardMaterial(checkSize=10))),
            objects.Sphere(array([0, top, z - radius]), radius, objects.Material((0, 0, 255), reflective=True)),
            objects.Sphere(array([-side, 0, z - radius]), radius, objects.Material((0, 255, 0), reflective=True)),
            objects.Sphere(array([side, 0, z - radius]), radius, objects.Material((255, 0, 0), reflective=True,)),
            objects.Triangle(array([0, top, z]), array([side, 0, z]), array([-side, 0, z]),objects.Material((255, 255, 0)))
        ]
        lights = [array([300, 300, 100]), array([0, -top, top])]

    else:
        print("Please add to the arguments \nlight \tOR\treflection \tOR\ttexture")
        sys.exit(1)

    # start raytracing
    render()

    image.save('./result/result_{}_{}.png'.format(sys.argv[1], datetime.datetime.now()))
    print("... finish.")