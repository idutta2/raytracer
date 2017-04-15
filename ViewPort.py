import numpy as np

class ViewPort:
    """ Simple viewport class center on z-axis """

    def __init__(self, width, height, gamma=1.0):
        self.w = width
        self.h = height
        self.g = gamma
        self.inv_g = 1 / gamma
        self.setCorners(np.array([-1.0, -1.0, 0.0]), np.array([1.0, 1.0, 0.0]))

    def setCorners(self, minC, maxC):
        """Sets the lower left and upper right corners"""
        self.minCorner = minC
        self.maxCorner = maxC
        self.s = (self.maxCorner[0] - self.minCorner[0]) / self.w

    def getPixelCenter(self, r, c):
        return np.array([self.s * (c - self.w / 2.0 + 0.5), self.s * (r - self.h / 2.0 + 0.5), self.minCorner[2]])