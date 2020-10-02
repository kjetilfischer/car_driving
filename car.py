import pygame
from math import sin, cos

class Car:
    def __init__(self, surface, xpos, ypos, width=50, length=100, angle=0, vmax=100, acc=10, color=(255, 0, 0)):
        # static properties
        self.width = width
        self.length = length
        self.vmax = vmax
        self.acc = acc
        self.color = color
        self.surface = surface
        
        # variable properties
        self.angle = angle
        self.xpos = xpos
        self.ypos = ypos
        self.velo = 0.
              
        
    def velocity(self, t):
        self.velo = self.acc * t + self.velo
    
        
    def draw(self):
        x1 = self.xpos - self.width/2*cos(self.angle) + self.length/2*sin(self.angle)
        y1 = self.ypos - self.width/2*sin(self.angle) - self.length/2*cos(self.angle)
        
        x2 = self.xpos + self.width/2*cos(self.angle) + self.length/2*sin(self.angle)
        y2 = self.ypos + self.width/2*sin(self.angle) - self.length/2*cos(self.angle)
        
        x3 = self.xpos + self.width/2*cos(self.angle) - self.length/2*sin(self.angle)
        y3 = self.ypos + self.width/2*sin(self.angle) + self.length/2*cos(self.angle)
        
        x4 = self.xpos - self.width/2*cos(self.angle) - self.length/2*sin(self.angle)
        y4 = self.ypos - self.width/2*sin(self.angle) + self.length/2*cos(self.angle)
        
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        pygame.draw.polygon(self.surface, self.color, points)
        #pygame.draw.polygon(self.surface, self.color, [(10, 10), (20, 80), (10, 300), (400, 50)])