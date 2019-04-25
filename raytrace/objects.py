from numpy import *
from colour import Color
from PIL import Image
import datetime

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

class Sphere(object): #S37
    def __init__(self, center, radius):
        self.center = center #point
        self.radius = radius #scalar

    def __repr__(self):
        return "Sphere(%s,%s)" %(repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v*v - co.dot(co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p-self.center).normalized()

class Plane(object): #S39
    def __init__(self, point, normal):
        self.point = point # point
        self.normal = normal.normalized() #vector

    def __repr__(self):
        return "Plane(%s,%s)" %(repr(self.point), repr(self.normal))

    def intersectionParamter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return (-a)/b
        else:
            return None

    def normalAt(self, p):
        return self.normal

class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a #point
        self.b = b #point
        self.c = c #point
        self.u = self.b - self.a #direction vector
        self.v = self.c - self.a #direction vector

    def __repr__(self):
        return "Triangle(%s,%s,%s)" %(repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return wu.dot(self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()

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

objectlist = []
image = Image.new("RGB", "(wRes, hRes)")
image.save("images/"+str(datetime.datetime.now()) +".jpg")