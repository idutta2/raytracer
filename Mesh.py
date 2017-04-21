from ShadeRec import *
import pymesh
class Mesh:
    def __init__(self, vertices, indices, normals, vertex_faces, u, v, num_vertices, num_triangles):
        self.vertices = vertices
        self.indices = indices
        self.normals = normals
        self.vertex_faces = vertex_faces
        self.u = u
        self.v = v
        self.num_vertices = num_vertices
        self.num_triangles = num_triangles

    def hit_FlatMeshTriangle(self, ray, tmin, sr):

        v1 = self.vertices[0]
        v2 = self.vertices[1]
        v3 = self.vertices[2]

        a = v1[0] - v2[0]
        b = v1[0] - v3[0]
        c = ray.d[0]
        d = v1[0] - ray.o[0]

        e = v1[1] - v2[1]
        f = v1[1] - v3[1]
        g = ray.d[1]
        h = v1[1] - ray.o[1]

        i = v1[2] - v2[2]
        j = v1[2] - v3[2]
        k = ray.d[2]
        l = v1[2] - ray.o[2]

        m = f*k - g*j
        n = h*k - g*l
        p = f*l - h*j
        q = g*i - e*k
        r = e*l - h*i
        s = e*j - f*i

        inv_denom = 1.0/(a*m + b*q + c*s)

        e1 = d*m - b*n - c*p
        beta = e1 *inv_denom

        if beta < 0.0 or beta >1.0:
            return False

        e2 = a*n + d*q + c*r
        gamma = e2 * inv_denom

        if gamma < 0.0 or gamma > 1.0:
            return False

        if beta+gamma > 1.0:
            return False

        e3 = a*p - b*r + d*r
        t = e3 * inv_denom

        #tmin = t
        sr.normal = self.normal
        sr.local_hit = ray.o + t*ray.d

    def hit_SmoothMeshTriangle(self, ray, tmin, sr):

        v1 = self.vertices[0]
        v2 = self.vertices[1]
        v3 = self.vertices[2]

        a = v1[0] - v2[0]
        b = v1[0] - v3[0]
        c = ray.d[0]
        d = v1[0] - ray.o[0]

        e = v1[1] - v2[1]
        f = v1[1] - v3[1]
        g = ray.d[1]
        h = v1[1] - ray.o[1]

        i = v1[2] - v2[2]
        j = v1[2] - v3[2]
        k = ray.d[2]
        l = v1[2] - ray.o[2]

        m = f*k - g*j
        n = h*k - g*l
        p = f*l - h*j
        q = g*i - e*k
        r = e*l - h*i
        s = e*j - f*i

        inv_denom = 1.0/(a*m + b*q + c*s)

        e1 = d*m - b*n - c*p
        beta = e1 *inv_denom

        if beta < 0.0 or beta >1.0:
            return False

        e2 = a*n + d*q + c*r
        gamma = e2 * inv_denom

        if gamma < 0.0 or gamma > 1.0:
            return False

        if beta+gamma > 1.0:
            return False

        e3 = a*p - b*r + d*r
        t = e3 * inv_denom

        #tmin = t
        sr.normal = interpolate_normal(beta, gamma)
        sr.local_hit = ray.o + t*ray.d

    def interpolate_normal(self, beta, gamma):

        normal((1-beta-gamma)*self.normals[0] + (beta * self.normals[1]) + (gamma * self.normals[2]))
        normal.normalize()

        return normal
