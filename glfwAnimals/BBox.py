import numpy as np

class BBox():
    def __init__(self, points):
        if type(points) is list or type(points) is np.ndarray:
            self.points = points

        else:
            self.faces = points.faces
            self.vertices = points.vertices
            self.normals = points.normals

            self.points = []

            for face in self.faces:
                for f in face:
                    self.points.append(self.vertices[f])

            for face in self.faces:
                n = face[0]
                self.points.append(self.normals[n])


        # Bounding Box
        vecX = [vec[0] for vec in self.points]
        vecY = [vec[1] for vec in self.points]
        vecZ = [vec[2] for vec in self.points]

        self.right = max(vecX)
        self.left = min(vecX)
        self.top = max(vecY)
        self.bottom = min(vecY)
        self.far = max(vecZ)
        self.near = min(vecZ)



    def move_to_origin(self):
        self.points = self.points - np.array([np.median([self.right, self.left]),
                                    np.median([self.top, self.bottom]),
                                    np.median([self.far, self.near])])

    def scale_to_kanonisches_Sichtvolumen(self): # scale to [-1, 1]^3
        self.points = self.points * (2.0 /max([self.right - self.left, self.top - self.bottom, self.far - self.near]))