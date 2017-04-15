class Rectangle():

    kEpsilon = 0.0000001

    def __init__(self, p, w, h, mat, sampler):
        """Initializes plane attributes"""
        self.p = p
        self.h = h
        self.w = w
        self.n = w.cross(h).normalize()
        self.a = w.length() * h.length()
        self.material = mat
        self.position = p
        self.s = sampler
        self.pdf = 1 / self.a
        self.type = "Plane"
        self.shadows = False

    def intersectRay(self, ray, sr):
        """ Determine if a ray intersects the Rectangle
            Returns: the parameter t for the closest intersection point to
                     the ray origin.
                     Returns a value of None for no intersection
        """
        test = ray.d * self.n
        if test == 0:
            return False
        t = ((self.position - ray.o) * self.n) / (ray.d * self.n)
        if (t < kEpsilon):
            return False
        p = ray.o + t * ray.d
        v = p - self.p
        h = v * self.h
        if (h < 0 or h > self.h.length() * self.h.length()):
            return False
        w = v * self.w
        if w < 0 or w > (self.w.length() * self.w.length()):
            return False
        self.t = t
        self.normal = self.n
        self.local_hit = p
        return True

    # Same as intersectRay, but no sr
    def shadowHit(self, ray):
        test = ray.d * self.n
        if test == 0:
            return False
        t = ((self.position - ray.o) * self.n) / (ray.d * self.n)
        if (t < kEpsilon):
            return False
        p = ray.o + t * ray.d
        v = p - self.p
        h = v * self.h
        if (h < 0 or h > self.h.length() * self.h.length()):
            return False
        w = v * self.w
        if w < 0 or w > (self.w.length() * self.w.length()):
            return False
        self.st = t
        return True

    # Return sample point
    def sample(self):
        s = self.s.sampleSquare();
        return (self.p + s.x * self.w + s.y * self.h)

    def getNormal(self, pt):
        """ Returns unit normal of sphere at the point pt """
        return self.n