import numpy as np
from BBox import BBox

'''read Wavefont Object files (.obj)'''
class ObjParser():
    def __init__(self, filepath):
        self.vertices = []
        self.texture = []
        self.normals = []
        self.faces = []
        self.filepath = filepath
        self.bbox = None
        self.parseObj()


    def parseObj(self):
        objFile = open(self.filepath)

        objFile = self.sortFile(objFile) #damit die Reihenfolge v - vt - vn - f gewährleistet werden kann

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


                if len(self.faces) == 0:
                    self.initBBox()


                fLine = line.split()

                index_vertices = []
                index_normals = []

                for index in fLine[1:]: #f is a index
                    if '/' in line: # v/vt/vn & v//vn
                        index = index.split('/')

                        index_vertices.append(int(index[0]) - 1)
                        # ignore value[1] we dont use textures
                        index_normals.append(int(index[2]) - 1)

                    else: # v
                        index_vertices.append(int(index) - 1)

                face = []
                points = []
                norms = []

                points.append(self.vertices[index_vertices[0]])
                points.append(self.vertices[index_vertices[1]])
                points.append(self.vertices[index_vertices[2]])

                if (len(index_normals) == 0):
                    n = np.cross(points[2] - points[0],
                                     points[2] - points[1])

                    norms.append(n)
                    norms.append(n)
                    norms.append(n)

                else:
                    norms.append(self.normals[index_normals[0]])
                    norms.append(self.normals[index_normals[1]])
                    norms.append(self.normals[index_normals[2]])

                face.append(points)
                face.append(norms)
                self.faces.append(face)


    def getVboList(self):
        myVBO = []
        for face in self.faces:
            vertices = face[0]
            norms = face[1]
            for i in range(len(vertices)):
                myVBO.append(np.concatenate((vertices[i], norms[i]), axis=None))  # .flatten() wants np.array()
        return myVBO


    def initBBox(self):
        self.bbox = BBox(self.vertices)
        self.bbox.move_to_origin()
        self.bbox.scale_to_kanonisches_Sichtvolumen()
        self.vertices =  self.bbox.points

    def sortFile(self, file):
        v = []
        vt = []
        vn = []
        f = []
        for line in file:
            if(line.startswith("v ")):
                v.append(line)
            elif(line.startswith("vt ")):
                vt.append(line)
            elif(line.startswith("vn ")):
                vn.append(line)
            elif(line.startswith("f ")):
                f.append(line)

        sortedFile = []
        sortedFile.extend(v)
        sortedFile.extend(vt)
        sortedFile.extend(vn)
        sortedFile.extend(f)

        return sortedFile