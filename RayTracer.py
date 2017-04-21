import numpy as np
import matplotlib.pyplot as pt
import random

from PIL import Image
from Sphere import Sphere
from Ray import Ray
from Plane import Plane
from Triangle import Triangle
from ViewPort import ViewPort

# create a viewport and image
v = ViewPort(500, 500)
im = Image.new("RGB", (v.w, v.h))
pix = im.load()

# define a sphere
radius = 1.0
radius1 = 0.5
center = np.array([0, 0, -2.5])
s = Sphere(radius, center, np.array([255, 0, 0]))
s1 = Sphere(radius1, center, np.array([0, 0, 255]))

point = np.array([0.0, -0.5, 0.0])
normal = np.array([0.0, 1.0, 0.0])

p = Plane(point, normal, np.array([0, 0, 255]))

v1 = np.array([3.0, 0.0, 0.0])
v2 = np.array([0.0, 1.5, 0.0])
v3 = np.array([1.0, 0.0, 1.5])

tr = Triangle(v1, v2, v3, np.array([255, 215, 0]))

# define a ray
ray = Ray(np.array([0, 0, 0]), np.array([0, 0, -1]))

# define a light direction
ldir = np.array([0, 0, 1])  # light direction
kd = 0.75  # reflectivity
illum = 1.0  # light luminosity
dc = 1.0    #diffusion coefficient
ambient = 0.05

color_light = np.ones(3)

def add_sphere(s):
    return dict(type='sphere', Sphere=s)

def add_plane(p):
    return dict(type='plane', Plane=p)

def add_triangle(tr):
    return dict(type='triangle', Triangle=tr)

scene = [tr, s, s1]

def normalize(x):
    x /= np.linalg.norm(x)
    return x

def intersect(obj, ray):
    #print(ray.o, " and ", ray.d)
    return obj.intersectRay(ray)

def shadowCheck(Ocheck, Dcheck, obj):
    ray1 = Ray(Ocheck, Dcheck)
    if (type(obj) is Sphere):
        return Sphere.intersectRay(ray1)
    if (type(obj) is Plane):
        return Plane.intersectRay(ray1)
    if (type(obj) is Triangle):
        return Triangle.intersectRay(ray1)

def getNormal(obj):
    if (type(obj) is Sphere):
        return Sphere.getNormal(obj, pt)
    if (type(obj) is Plane):
        return Plane.getNormal(obj, pt)
    if (type(obj) is Triangle):
        return Triangle.getNormal(obj, pt)

def getColor(obj):
    if (type(obj) is Sphere):
        return Sphere.obj.mat
    if (type(obj) is Plane):
        return Plane.obj.mat
    if (type(obj) is Triangle):
        return Triangle.obj.mat


def phongDiffuse(x, n, mat):
    """Implements a Phong-style diffuse shading function
    Args:
         x: is a point on a surface
         n: is the unit normal at that point
         mat: is an RGB tuple of the surface color
    Returns: A tuple representing an RGB color with values in [0,255]

    """
    factor = kd * illum * max(0, n.dot(ldir))
    color = np.rint(factor * mat).astype(int)
    return color[0], color[1], color[2]


def ray_trace(ray, scene):

 # Perform orthographic ray-tracing of the sphere

        for col in range(v.w):
             for row in range(v.h):
             # print("pixel ", col, " ", row)
                ray.o = v.getPixelCenter(col, row)
                for x in scene:
                    t = x.intersectRay(ray)
                    if (t != None):
                        xp = ray.getPoint(t)
                        # print("xp has been set")
                        pix[col, (v.h - 1) - row] = phongDiffuse(xp, x.getNormal(xp), x.material)
                        # print ("pixel coordinates: ", pix[col,(v.h-1)-row])




# Show the image in a window
ray_trace(ray, scene)
im.show()
