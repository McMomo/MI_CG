#!usr/bin/env python3

import numpy as np

'''read Wavefont Object files (.obj)'''
class ObjParser:
    def __init__(self, filepath):
        self.vertices = []
        self.texture = []
        self.normals = []
        self.faces = []

        objFile = open(filepath)

        for line in objFile:

            if(line.startswith("v ")):
                vLine = line.split()
                v = np.array([float(i) for i in vLine[1:]])
                self.vertices.append(v)

            elif (line.startswith("vt ")):
                vtLine = line.split()
                vt  = np.array([float(i) for i in vtLine[1:]])
                self.texture.append(vt)
            elif (line.startswith("vn ")):
                vnLine = line.split()
                vn = np.array([float(i) for i in vnLine[1:]])
                self.normals.append(vn)
            elif (line.startswith("f ")):
                fLine = line.split()
                #f v/vt/vn or f v//vn or f v
                #f is a index
                if '/' in line:
                    face = []
                    for i in fLine[1:]:
                        i = i.split('/')
                        i = [int(x) if x != '' else None for x in i]
                        face.append(i)
                    self.faces.append(face)
                else:
                    face = [int(i)-1 for i in fLine[1:]] # i -1 because a list starts with i = 0
                    self.faces.append(face)

                    n = np.cross(self.vertices[face[2]]-self.vertices[face[0]],
                                 self.vertices[face[2]]-self.vertices[face[1]])

                    if (len(self.normals) == 0):
                        self.normals = [0.0] * len(self.vertices)

                    self.normals[face[0]] += n
                    self.normals[face[1]] += n
                    self.normals[face[2]] += n


