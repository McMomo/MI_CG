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
        v = co.dot(ray.direction)
        discriminant = v*v - co.dot(co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p-self.center).normalized()



class Plane(object): #S39
    def __init__(self, point, normal, color):
        self.point = point # point
        self.normal = normal/np.linalg.norm(normal) #normal.normalized() #vector

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
