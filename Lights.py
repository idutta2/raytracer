from Ray import *

class Light:
    def getDirection(self, sr):
        pass

    def L(self):
        pass

class AreaLights(Light):

    def __init__(self, o):
        self.o = o

    def getDirection(self, sr):
        self.sp = self.o.sample()
        self.n = self.o.getNormal(self.p)
        self.wi = self.sp - sr.hit_point
        self.wi = self.wi.normalize()
        return self.wi*(-1.0)

    def inShadow(self, ray, sr):

        ts = (self.p - ray.o)*ray.d
        for object in sr.w.objects:
            sr.w.addRay()
            if object.shadowHit(ray) and object.st < ts:
                return True

        return False

    def L(self):
        n = (-1.0*self.n *self.wi)

        if(n>0):
            return self.o.material.getLe()
        else:
            return Color(0,0,0)

    def G(self, sr):
        nd = (-1.0*self.n*self.wi)
        d = self.p - sr.hit_point
        ddot = d*d
        return nd/ddot

    def pdf(self):
        return self.o.pdf

class DirectionLight(Light):
    def __init__(self, d, color, ls):
        self.d = d
        self.color = color
        self.ls = ls

    def getDirection(self, sr):
        return self.d

    def L(self):
        light_col = self.ls * self.color
        return light_col

    def inShadow(self, ray, sr):
        for obj in sr.w.objects:
            sr.w.addRay()
            if obj.shadowHit(ray):
                return True
            else:
                return False

class PointLight(Light):
    def __init__(self, color, ls, p):
        self.p = p
        self.ls = ls
        self.color = color

    def getDirection(self, sr):
        self.distance = sr.hit_point - self.p
        return self.distance

    def L(self):
        retVal = (self.color * self.ls)/(self.distance* self.distance)
        return retVal

    def inShadow(self, ray, sr):
        for obj in sr.w.objects:
            sr.w.addRay()
            t = (self.p - ray.o).length()
            if obj.shadowHit(ray, t):
                if(obj.st >= t):
                    return False
                else:
                    return True

class AmbientLight(Light):
    def __init__(self, color, ls):
        self.color = color
        self.ls = ls

    def getDirection(self, sr):
        return Vector(0, 0, 0)

    def L(self):
        amb_col = self.ls * self.color
        return amb_col