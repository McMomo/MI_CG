from numpy import *


class Material:
    def __init__(self, color, reflective=False, texture=None, specular=0.5, lambert=1, ambient=0.9):
        self.color = color
        self.reflective = reflective
        self.texture = texture
        self.specular = specular
        self.lambert = lambert
        self.ambient = ambient

class CheckerboardMaterial:
    def __init__(self, baseColor = (255, 255, 255), otherColor = (0, 0, 0), checkSize = 5):
        self.baseColor = baseColor
        self.otherColor = otherColor
        self.checkSize = checkSize

    def baseColorAt(self, p):
        v = p
        v = multiply(v, (0.1/self.checkSize))
        if (int(abs(v[0])+0.5) + int(abs(v[1])+0.5) + int(abs(v[2])+0.5)) %2:
            return self.otherColor
        return self.baseColor

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center #point
        self.radius = radius #scalar

        self.material = material

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

    def colorAt(self):
        return self.material.color


class Plane(object):
    def __init__(self, point, normal, material):
        self.point = point # point
        self.normal = normal /linalg.norm(normal)

        self.material = material

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

    def colorAt(self):

        return self.material.color




class Triangle(object):
    def __init__(self, a, b, c, material):
        self.a = a #point
        self.b = b #point
        self.c = c #point
        self.u = self.b - self.a #direction vector
        self.v = self.c - self.a #direction vector
        self.material = material

    def __repr__(self):
        return "Triangle({},{},{})".format(repr(self.a), repr(self.b), repr(self.c))

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

    def colorAt(self):
        return self.material.color