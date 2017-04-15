import numpy as np
from numpy import linalg as LA


class Plane:
    """Simple geometric plane
    Attributes:
        kEpsilon: floating value used for allowable error in equality tests
        n: normal
        p: point
        material: tuple representing an RGB color with values in [0,255]
    """
    kEpsilon = 0.0000001

    def __init__(self, p, n, mat):
        """Initializes sphere attributes"""
        self.p = p
        self.n = n
        self.material = mat

    # #419begin #type=3 #src=Ray Tracing from the Ground Up

    def intersectRay(self, ray):
        """ Determine if a ray intersects the plane
            Returns: the parameter t for the closest intersection point to
                     the ray origin.
                     Returns a value of None for no intersection
        """
        #if(np.dot(ray.d, self.n) == 0)
        t = np.dot((self.p - ray.o), self.n)/np.dot(ray.d, self.n)
        if (t > self.kEpsilon):
            return t
        return None

    def getNormal(self, pt):
        return self.n


    # #419end