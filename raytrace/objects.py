from numpy import *

class Sphere(object): #S37
    def __init__(self, center, radius, color):
        self.center = center #point
        self.radius = radius #scalar

        self.color = color

    def __repr__(self):
        return "Sphere(%s,%s)" %(repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = np.dot(co,ray.direction)
        discriminant = v*v - np.dot(co,co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - np.sqrt(discriminant)

    def normalAt(self, p):
        tmp = (p-self.center)
        return tmp/np.linalg.norm(tmp)



class Plane(object): #S39
    def __init__(self, point, normal, color):
        self.point = point # point
        self.normal = normal/linalg.norm(normal) #normal.normalized() #vector # removed np

        self.color = color

    def __repr__(self):
        return "Plane(%s,%s)" %(repr(self.point), repr(self.normal))

    def intersectionParamter(self, ray):
        op = ray.origin - self.point
        a = np.dot(op, self.normal)
        b = np.dot(ray.direction, self.normal)
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
        dv = np.cross(ray.direction, self.v)
        dvu = np.dot(dv, self.u)
        if dvu == 0.0:
            return None
        wu = np.cross(w, self.u)
        r = np.dot(dv, w) / dvu
        s = np.dot(wu, ray.direction) / dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return np.dot(wu, self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        tmp = np.cross(self.u,self.v)
        return tmp/np.linalg.norm(tmp)
