import pygame
from math import sin, cos
import matplotlib.path as pltPath

class Car:
    def __init__(self, surface, track, xpos, ypos, width=50, length=100, angle=0, vmax=100, acc=10, color=(255, 0, 0)):
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
        
        # path for intersection check`s
        self.path1 = pltPath.Path(track.s1)
        self.path2 = pltPath.Path(track.s2)
        self.path3 = pltPath.Path(track.s3)
        self.path4 = pltPath.Path(track.s4)
        self.path5 = pltPath.Path(track.s5)
        
        self.pathsf = pltPath.Path(track.start_finish)
        self.pathcp = pltPath.Path(track.checkpoint)
        
        self.turn_left = False
        self.turn_right = False
        self.accelerate = False
        self.decelerate = False
        self.brake = False
        
        self.checkpoint = False
        self.finish = False
    
    
    def controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.turn_left = True
            if event.key == pygame.K_RIGHT:
                self.turn_right = True
            if event.key == pygame.K_UP:
                self.accelerate = True
            if event.key == pygame.K_DOWN:
                self.decelerate = True
            if event.key == pygame.K_SPACE:
                self.brake = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.turn_left = False
            if event.key == pygame.K_RIGHT:
                self.turn_right = False
            if event.key == pygame.K_UP:
                self.accelerate = False
            if event.key == pygame.K_DOWN:
                self.decelerate = False
            if event.key == pygame.K_SPACE:
                self.brake = False

    
    def draw(self):
        x1 = self.xpos - self.width/2*cos(self.angle) + self.length/2*sin(self.angle)
        y1 = self.ypos - self.width/2*sin(self.angle) - self.length/2*cos(self.angle)
        
        x2 = self.xpos + self.width/2*cos(self.angle) + self.length/2*sin(self.angle)
        y2 = self.ypos + self.width/2*sin(self.angle) - self.length/2*cos(self.angle)
        
        x3 = self.xpos + self.width/2*cos(self.angle) - self.length/2*sin(self.angle)
        y3 = self.ypos + self.width/2*sin(self.angle) + self.length/2*cos(self.angle)
        
        x4 = self.xpos - self.width/2*cos(self.angle) - self.length/2*sin(self.angle)
        y4 = self.ypos - self.width/2*sin(self.angle) + self.length/2*cos(self.angle)
        
        self.points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        pygame.draw.polygon(self.surface, self.color, self.points)
        #pygame.draw.polygon(self.surface, self.color, [(10, 10), (20, 80), (10, 300), (400, 50)])

    
    def update(self, dt):
        # driving physics; update variable properties
        if self.turn_left:
            self.angle -= 0.01 * self.velo * dt
        if self.turn_right:
            self.angle += 0.01 * self.velo * dt
        if self.accelerate:
            if self.velo < self.vmax:
                self.velo += self.acc * dt
        if self.decelerate:
            if self.velo > -self.vmax/2:
                self.velo -= self.acc * dt
        if self.brake:
            if self.velo > 0:
                self.velo -= self.acc * dt
            if self.velo < 0:
                self.velo += self.acc * dt
            if self.velo > -0.01 and self.velo < 0.01:
                self.velo = 0
        if not self.accelerate and not self.decelerate:
            if self.velo > 0:
                self.velo -= self.acc/3 * dt
            if self.velo < 0:
                self.velo += self.acc/3 * dt
            if self.velo > -0.01 and self.velo < 0.01:
                self.velo = 0
        if self.velo != 0:
            self.xpos = self.xpos + (dt* self.velo * sin(self.angle))
            self.ypos = self.ypos - (dt* self.velo * cos(self.angle))
    
    
    def check_checkpoint(self):
        # checkpoint
        if not self.checkpoint:
            for point in self.points:
                if self.pathcp.contains_point(point):
                    self.checkpoint = True
                if self.checkpoint:
                    break
        # finish
        if self.checkpoint and not self.finish:
            for point in self.points:
                if self.pathsf.contains_point(point):
                    self.finish = True
                    self.checkpoint = False
                if self.finish:
                    break
    
    
    def check_crash(self, track):
        for point in self.points:
            if point[0] < 0 or point[0] > track.width:
                crash = True
            elif point[1] < 0 or point[1] > track.height:
                crash = True
            elif self.path1.contains_point(point):
                crash = True
            elif self.path2.contains_point(point):
                crash = True
            elif self.path3.contains_point(point):
                crash = True
            elif self.path4.contains_point(point):
                crash = True
            elif self.path5.contains_point(point):
                crash = True
            else:
                crash = False
            if crash:
                break
        if crash:
            self.velo = 0
    
    
    def sensor(self):
        pass