from numpy import *


class Ray(object): #S30
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction/ linalg.norm(direction) #vector

    def __repr__(self):
        return "Ray({},{})".format(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + multiply(self.direction,t)



class Sphere(object): #S37
    def __init__(self, center, radius, color):
        self.center = center #point
        self.radius = radius #scalar

        self.color = color

    def __repr__(self):
        return "Sphere({},{})".format(repr(self.center), self.radius)

    def intersectionParamter(self, ray):
        co = self.center - ray.origin
        v = dot(co,ray.direction)
        discriminant = v*v - dot(co,co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - sqrt(discriminant)

    def normalAt(self, p):
        tmp = (p-self.center)
        return tmp/linalg.norm(tmp)

    def colorAt(self, ray):



        return self.color



class Plane(object): #S39
    def __init__(self, point, normal, color):
        self.point = point # point
        self.normal = normal/linalg.norm(normal) #normal.normalized() #vector # removed np

        self.color = color

    def __repr__(self):
        return "Plane(%s,%s)" %(repr(self.point), repr(self.normal))

    def intersectionParamter(self, ray):
        op = ray.origin - self.point
        a = dot(op, self.normal)
        b = dot(ray.direction, self.normal)
        if b:
            return (-a)/b
        else:
            return None

    def normalAt(self, p):
        return self.normal

    def colorAt(self, ray):

        return self.color




class Triangle(object):
    def __init__(self, a, b, c, color):
        self.a = a #point
        self.b = b #point
        self.c = c #point
        self.u = self.b - self.a #direction vector
        self.v = self.c - self.a #direction vector
        self.color = color

    def __repr__(self):
        return "Triangle(%s,%s,%s)" %(repr(self.a), repr(self.b), repr(self.c))

    def intersectionParamter(self, ray):
        w = ray.origin - self.a
        dv = cross(ray.direction, self.v)
        dvu = dot(dv, self.u)

        if dvu == 0.0:
            return None

        wu = cross(w, self.u)
        r = dot(dv, w) / dvu
        s = dot(wu, ray.direction) / dvu

        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return dot(wu, self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        tmp = cross(self.u,self.v)
        return tmp/linalg.norm(tmp)

    def colorAt(self, ray):
        return self.color