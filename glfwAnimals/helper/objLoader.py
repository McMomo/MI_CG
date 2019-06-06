#!usr/bin/env python3

import numpy as np

'''read Wavefont Object files (.obj)'''
class ObjLoader:
    def __init__(self, filepath):
        self.vertices = []
        self.texture = []
        self.normals = []
        self.faces = []

        objFile = open(filepath)

        for line in objFile:

            if(line.startswith("v ")):
                vLine = line.split()
                v = [float(i) for i in vLine[1:]]
                self.vertices.append(v)

            elif (line.startswith("vt ")):
                vtLine = line.split()
                vt  = [float(i) for i in vtLine[1:]]
                self.texture.append(vt)
            elif (line.startswith("vn ")):
                vnLine = line.split()
                vn = [float(i) for i in vnLine[1:]]
                self.normals.append(vn)
            elif (line.startswith("f ")):
                fLine = line.split()
                #f v/vt/vn oder f v//vn oder f v
                #f ist ein index
                if '/' in line:
                    face = []
                    for i in fLine[1:]:
                        i = i.split('/')
                        i = [float(x) if x != '' else None for x in i]
                        face.append(i)
                    self.faces.append(face)
                else:
                    face = [[float(i)] for i in fLine[1:]]
                    self.faces.append(face)

                    n = np.cross(self.vertices[face[2]]-self.vertices[face[0]],
                                 self.vertices[face[2]]-self.vertices[face[1]])

                    self.normals[face[0]] += n
                    self.normals[face[1]] += n
                    self.normals[face[2]] += n


