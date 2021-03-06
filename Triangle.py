import numpy as np
import math
from numpy import linalg as LA


def length(v):
    return math.sqrt(np.dot(v, v))

class Triangle:
    """Simple geometric sphere
    Attributes:
        kEpsilon: floating value used for allowable error in equality tests
        p: point
        v1: vertex 1
        v2: vertex 2
        v3: vertex 3
        material: tuple representing an RGB color with values in [0,255]
    """
    kEpsilon = 0.0000001


    def __init__(self, v1, v2, v3, mat):
        """Initializes triangle attributes"""
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.material = mat

    # #419begin #type=3 #src=Ray Tracing from the Ground Up


    def intersectRay(self, ray):
        """ Determine if a ray intersects the sphere
            Returns: the parameter t for the closest intersection point to
                     the ray origin.
                     Returns a value of None for no intersection
        """
        #print ("intersecting triangle")
        v1v3 = self.v3 - self.v1
        v1v2 = self.v2 - self.v1

        n = np.cross(v1v3, v1v2)
        area_tot = length(n)/2

        edge1 = self.v3 - self.v2
        vp1 = ray.o - self.v2

        C1 = np.cross(edge1, vp1)
        u = (length(C1)/2)/area_tot

        if u < 0:
            #print("this condition broke me")
            return None
        if u > 1:
            #print("this is annoying")
            return None

        edge2 = self.v1 - self.v3
        vp2 = ray.o - self.v3

        C = np.cross(edge2, vp2)
        v = (length(C)/2)/area_tot

        if v < 0:
            #print("this condition broke me")
            return None
        if v > 1:
            #print("this is annoying")
            return None

        w = 1-u-v

        if w < 0:
            #print("this condition broke me")
            return None
        if w > 1:
            #print("this is annoying")
            return None

       # print("hit triangle")
        t = w*self.v1 + u*self.v2 + v*self.v3
        return t

    def shadowHit(self, ray):
        """ Determine if a ray intersects the sphere
            Returns: the parameter t for the closest intersection point to
                     the ray origin.
                     Returns a value of None for no intersection
        """
        #print ("intersecting triangle")
        v1v3 = self.v3 - self.v1
        v1v2 = self.v2 - self.v1

        n = np.cross(v1v3, v1v2)
        area_tot = length(n)/2

        edge1 = self.v3 - self.v2
        vp1 = ray.o - self.v2

        C1 = np.cross(edge1, vp1)
        u = (length(C1)/2)/area_tot

        if u < 0:
            #print("this condition broke me")
            return None
        if u > 1:
            #print("this is annoying")
            return None

        edge2 = self.v1 - self.v3
        vp2 = ray.o - self.v3

        C = np.cross(edge2, vp2)
        v = (length(C)/2)/area_tot

        if v < 0:
            #print("this condition broke me")
            return None
        if v > 1:
            #print("this is annoying")
            return None

        w = 1-u-v

        if w < 0:
            #print("this condition broke me")
            return None
        if w > 1:
            #print("this is annoying")
            return None

       # print("hit triangle")
        t = w*self.v1 + u*self.v2 + v*self.v3

        if(t<self.kEpsilon):
            return False

        else:
            self.st = t
            return True


    def getNormal(self, pt):
        v1v3 = self.v3 - self.v1
        v1v2 = self.v1 - self.v2

        n = np.cross(v1v3, v1v2)
        return n

    def getBbox(self):
        delta = 0.000001

        min_x = min(min(self.v1[0], self.v2[0]), self.v3[0]) - delta
        max_x = max(max(self.v1[0], self.v2[0]), self.v3[0]) + delta
        min_y = min(min(self.v1[1], self.v2[1]), self.v3[1]) - delta
        max_y = max(max(self.v1[1], self.v2[1]), self.v3[1]) + delta
        min_z = min(min(self.v1[2], self.v2[2]), self.v3[2]) - delta
        max_z = max(max(self.v1[2], self.v2[2]), self.v3[2]) + delta

        return min_x, max_x, min_y, max_y, min_z, max_z


v1 = np.array([3.0, 0.0, 0.0])
v2 = np.array([0.0, 1.5, 0.0])
v3 = np.array([1.0, 0.0, 1.5])

tr = Triangle(v1, v2, v3, np.array([255, 215, 0]))
Triangle.getBbox(tr)
