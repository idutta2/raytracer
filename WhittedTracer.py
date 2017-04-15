from Ray import *
from ShadeRec import *
class Tracer:
    def __init__(self, world):
        self.world = world

    def trace(self, ray, depth):
        pass

class Whitted(Tracer):
    def trace(self, ray, depth):
        sr = self.world.hitObjects(ray)
        if sr.hit:
            sr.ray = ray
            sr.depth = depth
            return sr.mat.shade(sr)
        else:
            return self.world.background

class AreaLighting(Tracer):
    def trace(self, ray, depth):

        if(depth > 5):
            return Color(0.0, 0.0, 0.0)
        else:
            sr = self.world.hitObjects(ray)
            if sr.hit:
                sr.ray = ray
                sr.depth = depth
                return sr.mat.areaLightShade(sr)
            else:
                return self.world.background
