from numpy import *

class Ray(object): #S30
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction.normalized() #vector

    def __repr__(self):
        return "Ray(%s,%s)" %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


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

def rayPerPixel(): #S33
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