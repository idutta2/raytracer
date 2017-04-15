import numpy as np
from numpy import linalg as LA


class Sphere:
    """Simple geometric sphere
    Attributes:
        kEpsilon: floating value used for allowable error in equality tests
        r: radius
        c: center implemented as a numpy array
        material: tuple representing an RGB color with values in [0,255]
    """
    kEpsilon = 0.0000001

    def __init__(self, r, cntr, mat):
        """Initializes sphere attributes"""
        self.r = r
        self.c = cntr
        self.material = mat

    # #419begin #type=3 #src=Ray Tracing from the Ground Up

    def intersectRay(self, ray):
        """ Determine if a ray intersects the sphere
            Returns: the parameter t for the closest intersection point to
                     the ray origin.
                     Returns a value of None for no intersection
        """
        #print("in intersectRay")
        temp = ray.o - self.c
        a = np.dot(ray.d, ray.d)
        b = 2.0 * np.dot(temp, ray.d)
        cq = np.dot(temp, temp) - np.dot(self.r, self.r)
        disc = b * b - 4.0 * a * cq
        if (disc < 0.0):
            return None
        else:
            e = np.sqrt(disc)
            denom = 2.0 * a
            t = (-b - e) / denom
            if (t > self.kEpsilon):
                return t
            t = (-1.0 * b + e) / denom
            if (t > self.kEpsilon):
                return t
        return None

    # #419end

    def getNormal(self, pt):
        """ Returns unit normal of sphere at the point pt """
        n = pt - self.c
        return n / LA.norm(n)
