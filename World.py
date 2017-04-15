class World:
    def __init__(self):
        self.objects = []
        self.lights = []
        self.camera = None
        self.rays = 0

    def addLight(self, light):
        self.lights.append(light)


    def addObject(self, object):
        self.objects.append(object)

    def addRay(self):
        self.rays = self.rays + 1

