from Ray import *

class ShadeRec():
    def __init__(self, world):
        self.w = world
        self.hit_point = Point(0.0, 0.0, 0.0)
        self.local_hit = Point(0.0, 0.0, 0.0)
        self.normal = Vector(0.0, 0.0, 0.0)
        self.ray = Ray(Point(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0))
        self.color = Color(0.0, 0.0, 0.0)
        self.hit = False
        self.mat = None
        self.t = 0.0
        self.depth = 0
