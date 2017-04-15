from Ray import *
import math
from RayTracer import *

class Material():
    def shade(self, sr):
        pass

class BRDF:
    def f(self):
        pass

class PerfectSpecular(BRDF):
    def __init__(self, kr, surf):
        self.kr = kr
        self.surface = surf

    def f(self):
        return Color(0, 0, 0)

    def sample_f(self, sr, w_o):
        dot_prod = sr.normal*w_o
        self.wi = (-1.0*w_o) + (2*sr.normal*dot_prod)
        pdf = math.fabs(sr.normal *w_o)
        retVal = (self.kr * self.surface.getColor(sr)/pdf)

        return retVal


class Lambertian(BRDF):
    def __init__(self, kd, surface, sampler = None):

        self.kd = kd
        self.surface = surface
        if sampler != None:
            self.sampler = sampler
            self.sampler.mapHemisphere(1)

    def rho(self, sr):
        return self.kd * self.surface.getColor(sr)

    def f(self, sr):
        return (self.kd * self.surface.getColor(sr))/math.pi

    def sample_f(self, sr):
        w = sr.normal
        v = Vector(0.003, 1, 0.006).cross(w)
        v.normalize()
        u = v.cross(w)

        sp = self.sampler.sampleHemisphere()
        wi = sp.x * u + sp.y * v + sp.z * w
        wi.normalize()
        pdf = sr.normal * wi / math.pi

        return pdf, wi, (self.kd * self.surface.getColor(sr) / math.pi)


class GlossySpecular(BRDF):
    def __init__(self, ks, surface, exp, sampler):

        self.ks = ks
        self.surface = surface
        self.exp = exp
        if(sampler != None):
            self.sampler = Regular(25, 83)

    def setSamples(self, exp):
        self.sampler.mapHemisphere(exp)


    def sample_f(self, sr, wo):
        ndotwo = sr.normal * wo
        r = -1.0 * wo + 2 * sr.normal * ndotwo
        w = r
        u = Vector(0.005, 1, 0.008).cross(w)
        u.normalize()
        v = u.cross(w)
        sp = self.sampler.sampleHemisphere()

        self.wi = sp.x * u + sp.y * v + sp.z * w
        if sr.normal * self.wi < 0.0:
            self.wi = -1.0 * sp.x * u - sp.y * v - sp.z * w

        phong_lobe = pow(r * self.wi, self.exp)

        self.pdf = phong_lobe * (sr.normal * self.wi)
        return (self.ks * self.surface.getColor(sr) * phong_lobe)

class Emissive(Material):
    def __init__(self, ls, ce):
        self.ls = ls
        self.ce = ce

    def areaLightShade(self, sr):
        wo = -1.0 * sr.ray.d
        wo = wo.normalize()
        if sr.normal * wo > 0.0:
            return self.ls * self.ce
        else:
            return Color(0, 0, 0)


    def getLe(self):
        return self.ls * self.ce

    def getColor(self, sr):
        return self.ce

class Matte(Material):
    def __init__(self, ka, kd, cd, sampler=None):
        self.ambient = Lambertian(ka, cd, sampler)
        self.diffuse = Lambertian(kd, cd, sampler)
        self.cd = cd

    def shade(self,sr):
        L = self.ambient.rho(sr)*sr.w.ambient.L(s)
        for light in sr.w.lights:
            w_i = light.getDirection(sr)*-1.0
            w_i = w_i.normalize()
            dot_prod = sr.normal * w_i
            if dot_prod > 0.0:
                shadow = False
                shadowRay = Ray(sr.hit_point, w_i)
                shadow = light.inShadow(shadowRay, sr)

                if not shadow:
                    L = L + self.diffuse.f(sr)*w_i*light.L(sr)
        return L

    def areaLightShade(self, sr):
        L = self.ambient.rho(sr) * sr.w.ambient.L(sr)

        for light in sr.w.lights:
            wi = -1.0 * light.getDirection(sr)
            wi = wi.normalize()
            dot_prod = sr.normal * wi
            if dot_prod > 0.0:
                shadow = False
                # Check if object is in the way
                shadowRay = Ray(sr.hit_point, wi)
                shadow = light.inShadow(shadowRay, sr)
                # No object in the way, so add color
                if not shadow:
                    L += self.diffuse.f(sr) * light.L(sr) * dot_prod * light.G(sr) / light.pdf(sr)

        return L


class Phong(Material):
    def __init__(self, ka, kd, ks, cd, exp):
        self.ambient = Lambertian(ka, cd)
        self.diffuse = Lambertian(kd, cd)
        self.specular = GlossySpecular(ks, cd, exp, None)
        self.cd = cd

    def shade(self, sr):
        w_o = -1.0*sr.ray.d
        w_o = w_o.normalize()

        L = self.ambient.rho(sr) * sr.w.ambient.L(sr)
        for l in sr.w.lights:
            w_i = -1.0*l.getDirection(sr)
            w_i = w_i.normalize()
            dot_prod = sr.normal * w_i

            if dot_prod > 0:
                shadow = False
                shadowRay = Ray(sr.hit_point, w_i)
                shadow = l.inShadow(shadowRay, sr)
                if not shadow:
                    L = L + (dot_prod * l.L(sr) *( self.diffuse.f(sr) + self.specular.f(sr, w_o, w_i)))

        return L

    def areaLightShade(self, sr):
        w_o = -1.0 * sr.ray.d
        w_o = w_o.normalize()
        L = self.ambient.rho(sr) * sr.w.ambient.L(sr)
        for light in sr.w.lights:
            w_i = -1.0 * light.getDirection(sr)
            w_i = w_i.normalize()
            dot_prod = sr.normal * w_i
            if dot_prod > 0:
                shadow = False
                shadowRay = Ray(sr.hit_point, w_i)
                shadow = light.inShadow(shadowRay, sr)
                if not shadow:
                    L += (self.diffuse.f(sr) + self.specular.f(sr, w_o, w_i)) * light.L(sr) * dot_prod * light.G(
                        sr) / light.pdf(sr)

        return L

class Reflective(Phong):
    def __init__(self, ka, kd, ks, cd, exp, kr, cr):
        Phong.__init__(self, ka, kd, ks, cd, exp)
        self.reflective = PerfectSpecular(kr, cr)

    def shade(self, sr):
        L = Phong.shade(self, sr)
        w_o = sr.ray.d * -1.0
        fr = self.reflective.sample_f(sr, w_o)
        w_i = self.reflective.wi
        reflectedR = Ray(sr.hit_point, w_i)
        dot_prod = sr.normal * w_i
        L = L + (dot_prod * fr * sr.w.tracer.trace(reflectedR, 1+sr.depth))

        return L

    def areaLightShade(self, sr):
        L = Phong.areaLightShade(self, sr)
        w_o = sr.ray.d * -1.0
        fr = self.reflective.sample_f(sr, w_o)
        w_i = self.reflective.wi
        reflectedR = Ray(sr.hit_point, w_i)
        dot_prod = sr.normal * w_i
        L = L+(dot_prod * fr * sr.w.tracer.trace(reflectedR, 1+sr.depth))

        return L




