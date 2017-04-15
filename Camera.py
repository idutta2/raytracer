import numpy as np
from numpy import linalg as LA
from PIL import Image
from ViewPort import ViewPort
from Material import *
from Ray import *
from WhittedTracer import *
import RayTracer
from Sphere import Sphere
from World import *

radius = 1.0
radius1 = 0.5
center = np.array([0, 0, -2.5])
s = Sphere(radius, center, np.array([255, 0, 0]))

objects = [RayTracer.add_sphere(s)]

def ray_direction(self, p):
    print("calculating new direction")
    ray = (p[0] * self.u) + (p[1] * self.v) - (self.d * self.w)
    ray = ray / LA.norm(ray)
    return ray

class PerspectiveCamera:
    """Simple perspective camera"""

    def __init__(self, eye, lookat, up, ra):
        self.up = up
        self.eye = eye
        self.lookat = lookat
        self.ra = ra
        self.compute_uvw()

    def compute_uvw(self):
        self.w = self.eye - self.lookat
        self.w = self.w / LA.norm(self.w)
        self.u = np.cross(self.up, self.w)
        self.u = self.u / LA.norm(self.u)
        self.v = np.cross(self.w, self.u)

    def rayDirection(self, p, d):
        dir = self.u*p[0] + self.v*p[1] - self.w*d
        return LA.norm(dir)

    def render_scene(self, w, res):
        # create a viewport and image
        v = ViewPort(res[0], res[1])
        im = Image.new("RGB", (v.w, v.h))
        pix = im.load()
        depth = 0
        ray = Ray(self.eye, self.lookat)
        d = 1
        n = 4
        # define a ray
        # FIX BUG -- STILL ORTHO
        #ray = Ray(np.array([0, 0, 0]), ray_direction(v))

        # Perform perspective ray-tracing
        print("...generating " + str(v) + " image")
        for col in range(v.w):
            for row in range(v.h):
                color = np.zeros(3)
                #print(color)
                #ray.o = v.getPixelCenter(col, row)

                for p in range(n):
                    for q in range(n):
                        ray.o = Point(v.s * (col - 0.5 * v.w + (q + 0.5) / n) + self.eye.x,
                                      v.s * (row - 0.5 * v.h + (p + 0.5) / n) + self.eye.y, self.eye.z)
                        color += w.tracer.trace(ray, depth)

                        # Divide by number of rays per pixel
                color /= n * n
                pix[col, v.h - 1 - row] = (int(color.r * 255), int(color.g * 255), int(color.b * 255))

        im.show()
