import cv2
import numpy as np
from collections import deque

class Car():
    nextID = 1
    def __init__(self,x,y,width,height,i=0):
        self.cx = x
        self.cy = y
        self.dx = 1
        self.dy = 1
        self.prex = 0
        self.prey = 0
        self.fx = x
        self.fy = y
        self.exe = 0
        self.width = width
        self.height = height
        self.stat = 0
        self.xs = [0,0,0,0,0]
        self.ys = [0,0,0,0,0]
        self.center = deque(maxlen=64)
        self.id = i
        if self.id == 0:
            self.id = Car.nextID
            Car.nextID += 1

    def printInfo(self):
        print("Car ID: {}, car x: {}, car y: {}, car width: {}, car height: {},car center: {}".format(self.id, self.cx, self.cy, self.width, self.height,Car.nextID,self.center))

    def equal(self,another):
        return self.cx == another.cx and self.cy == another.cy and self.width == another.width and self.height == another.height
