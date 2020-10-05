import pygame
from math import sin, cos, sqrt
import matplotlib.path as pltPath
import numpy as np

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
    
    
    def sensor(self, track, tracer_length=200, color=(0,0,0) , show=False):
        self.center = np.array((self.xpos, self.ypos))
        self.tracer0 = tracer_length * ((np.array(self.points[0]) + np.array(self.points[1]))/2 - self.center) / (self.length/2)               # forward
        self.tracer1 = tracer_length * (np.array(self.points[0]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # forward/left
        self.tracer2 = tracer_length * (np.array(self.points[1]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # forwards/right
        self.tracer3 = tracer_length * (np.array(self.points[2]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # backwards/right
        self.tracer4 = tracer_length * (np.array(self.points[3]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # backwards/left
        self.tracer5 = tracer_length * ((np.array(self.points[2]) + np.array(self.points[3]))/2 - self.center) / (self.length/2)               # backwards
        
        
        
        # measure distance to impassables; NEEDS TO BE REVISED: TOO SLOW!!! + include outer edges
        # contact_tracers are the intersections of tracers with impassables / distance from the center of the vehicle to impassables
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer0 + self.center).astype(int)):
                contact_tracer0 = i/tracer_length * self.tracer0 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer0 + self.center).astype(int)):
                contact_tracer0 = i/tracer_length * self.tracer0 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer0 + self.center).astype(int)):
                contact_tracer0 = i/tracer_length * self.tracer0 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer0 + self.center).astype(int)):
                contact_tracer0 = i/tracer_length * self.tracer0 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer0 + self.center).astype(int)):
                contact_tracer0 = i/tracer_length * self.tracer0 + self.center
                break
            else:
                contact_tracer0 = None
            i += 1
        
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer1 + self.center).astype(int)):
                contact_tracer1 = i/tracer_length * self.tracer1 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer1 + self.center).astype(int)):
                contact_tracer1 = i/tracer_length * self.tracer1 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer1 + self.center).astype(int)):
                contact_tracer1 = i/tracer_length * self.tracer1 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer1 + self.center).astype(int)):
                contact_tracer1 = i/tracer_length * self.tracer1 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer1 + self.center).astype(int)):
                contact_tracer1 = i/tracer_length * self.tracer1 + self.center
                break
            else:
                contact_tracer1 = None
            i += 1
        
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer2 + self.center).astype(int)):
                contact_tracer2 = i/tracer_length * self.tracer2 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer2 + self.center).astype(int)):
                contact_tracer2 = i/tracer_length * self.tracer2 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer2 + self.center).astype(int)):
                contact_tracer2 = i/tracer_length * self.tracer2 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer2 + self.center).astype(int)):
                contact_tracer2 = i/tracer_length * self.tracer2 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer2 + self.center).astype(int)):
                contact_tracer2 = i/tracer_length * self.tracer2 + self.center
                break
            else:
                contact_tracer2 = None
            i += 1
        
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer3 + self.center).astype(int)):
                contact_tracer3 = i/tracer_length * self.tracer3 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer3 + self.center).astype(int)):
                contact_tracer3 = i/tracer_length * self.tracer3 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer3 + self.center).astype(int)):
                contact_tracer3 = i/tracer_length * self.tracer3 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer3 + self.center).astype(int)):
                contact_tracer3 = i/tracer_length * self.tracer3 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer3 + self.center).astype(int)):
                contact_tracer3 = i/tracer_length * self.tracer3 + self.center
                break
            else:
                contact_tracer3 = None
            i += 1
        
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer4 + self.center).astype(int)):
                contact_tracer4 = i/tracer_length * self.tracer4 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer4 + self.center).astype(int)):
                contact_tracer4 = i/tracer_length * self.tracer4 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer4 + self.center).astype(int)):
                contact_tracer4 = i/tracer_length * self.tracer4 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer4 + self.center).astype(int)):
                contact_tracer4 = i/tracer_length * self.tracer4 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer4 + self.center).astype(int)):
                contact_tracer4 = i/tracer_length * self.tracer4 + self.center
                break
            else:
                contact_tracer4 = None
            i += 1
        
        i = 1
        while i <= tracer_length:
            if self.path1.contains_point((i/tracer_length * self.tracer5 + self.center).astype(int)):
                contact_tracer5 = i/tracer_length * self.tracer5 + self.center
                break
            elif self.path2.contains_point((i/tracer_length * self.tracer5 + self.center).astype(int)):
                contact_tracer5 = i/tracer_length * self.tracer5 + self.center
                break
            elif self.path3.contains_point((i/tracer_length * self.tracer5 + self.center).astype(int)):
                contact_tracer5 = i/tracer_length * self.tracer5 + self.center
                break
            elif self.path4.contains_point((i/tracer_length * self.tracer5 + self.center).astype(int)):
                contact_tracer5 = i/tracer_length * self.tracer5 + self.center
                break
            elif self.path5.contains_point((i/tracer_length * self.tracer5 + self.center).astype(int)):
                contact_tracer5 = i/tracer_length * self.tracer5 + self.center
                break
            else:
                contact_tracer5 = None
            i += 1
        
        if show:
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer0)
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer1)                                  # why is np.array(self.points[0])*4 as last argument is not possible???
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer2)
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer3)
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer4)
            pygame.draw.line(self.surface, color, self.center, self.center + self.tracer5)
            if contact_tracer0 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer0).astype(int), 4)
            if contact_tracer1 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer1).astype(int), 4)
            if contact_tracer2 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer2).astype(int), 4)
            if contact_tracer3 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer3).astype(int), 4)
            if contact_tracer4 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer4).astype(int), 4)
            if contact_tracer5 is not None:
                pygame.draw.circle(self.surface, color, (contact_tracer5).astype(int), 4)
        