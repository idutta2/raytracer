from Ray import *
import math
from RayTracer import *


class Material():
    def shade(self, sr):
        pass

class BRDF:
    def f(self):
        pass

class Lambertian(BRDF):
    def __init__(self, kd, surface):

        self.kd = kd
        self.surface = surface

    def rho(self, sr):
        return self.kd * self.surface.getColor(sr)

    def diffuse(self):
        return (self.kd * self.surface) / math.pi

    def ambient(self):
        return self.kd * self.cd

class GlossySpecular(BRDF):
    def __init__(self, ks, surface, exp):
        self.ks = ks
        self.surface = surface
        self.exp = exp

    def specular_function(self, sr, wo, wi):
        ndotwi = sr.normal * wi
        r = (-wi + (2.0 * sr.normal * ndotwi))
        rdotwo = r * wo

        if (rdotwo > 0.0):
            L = self.ks * (rdotwo ** self.exp)

class Phong(Material):
    def __init__(self, ka, kd, ks, cd, exp):
        self.ambient = Lambertian(ka, cd)
        self.diffuse = Lambertian(kd, cd)
        self.specular = GlossySpecular(ks, cd, exp)
        self.cd = cd

    def shade(self, sr):
        w_o = -1.0*sr.ray.d
        L = self.ambient.rho(sr) * sr.w.ambient.L(sr)

        for light in sr.w.lights:
            w_i = -1.0*light.getDirection(sr)
            ndotwi = sr.normal * w_i

            if ndotwi > 0:
                in_shadow = False
                if light.casts_shadows():
                    shadowRay = Ray(sr.hit_point, w_i)
                    in_shadow = light.inShadow(shadowRay, sr)
                if not in_shadow:
                    L = L + (ndotwi * light.L(sr) *( Lambertian.diffuse(self.diffuse) + GlossySpecular.specular_function(self.specular,sr, w_o, w_i)))

        return L