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
    
    """
    def calculate_intersection(self, L1, L2):
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        #  find the position of the intersection in respect to the line segments
        p1 = L1[0]
        p2 = L1[1]
        p3 = L2[0]
        p4 = L2[1]
        
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x3 = p3[0]
        y3 = p3[1]
        x4 = p4[0]
        y4 = p4[1]
        
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator != 0: # maybe: if denominator is not close to 0
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
            #Pxy = ((x1 + t * (x2 - x1)), (y1 + t * (y2 - y1)))
            if t >= 0 and t <= 1:
                Pxy = ((x1 + t * (x2 - x1)), (y1 + t * (y2 - y1)))
            elif u >= 0 and u <= 1:
                Pxy = ((x3 + u * (x4 - x3)), (y3 + u * (y4 - y3)))
            else:
                Pxy = None
        else:
            Pxy = None
        
        return Pxy
    """
    
    
    def calculate_intersection(self, L1, L2):
        p1 = L1[0]  # position vector
        p2 = L1[1]  # direction vector
        p3 = L2[0]  # position vector
        p4 = L2[1]  # direction vector
        
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x3 = p3[0]
        y3 = p3[1]
        x4 = p4[0]
        y4 = p4[1]
        
        a = np.array([[x2, -x4], [y2, -y4]])
        b = np.array([x3 - x1, y3 - y1])
        try:
            solved = np.linalg.solve(a, b)
            if solved[0] <= 1 and solved[0] > 0 and solved[1] <= 1 and solved[1] > 0:
                Pxy = np.array([(x1 + (x2 * solved[0])), (y1 + (y2 * solved[0]))])
            else:
                Pxy = None
        except:
            Pxy = None
        return Pxy
    
    def sensor(self, track, tracer_length=200, color=(0,0,0), show=False):   
        self.tracers = [0] * 6
        self.center = np.array((self.xpos, self.ypos))
        self.tracers[0] = tracer_length * ((np.array(self.points[0]) + np.array(self.points[1]))/2 - self.center) / (self.length/2)               # forward
        self.tracers[1] = tracer_length * (np.array(self.points[0]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # forward/left
        self.tracers[2] = tracer_length * (np.array(self.points[1]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # forwards/right
        self.tracers[3] = tracer_length * (np.array(self.points[2]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # backwards/right
        self.tracers[4] = tracer_length * (np.array(self.points[3]) - self.center) / sqrt(self.width*self.width + self.length*self.length) * 2    # backwards/left
        self.tracers[5] = tracer_length * ((np.array(self.points[2]) + np.array(self.points[3]))/2 - self.center) / (self.length/2)               # backwards
      
        contact_tracers = []
        for tracer in self.tracers:
            contacts = []
            for line in track.impassable_lines:
                contact = self.calculate_intersection((self.center, tracer), line)
                if contact is not None:
                    contacts.append(contact)
            try:
                contact_tracers.append(np.array(min(contacts)))
            except:
                contact_tracers.append(None)

        
        if show:
            for tracer in self.tracers:
                pygame.draw.line(self.surface, color, self.center, self.center + tracer)

            if contact_tracers[0] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[0].astype(int), 4)
            if contact_tracers[1] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[1].astype(int), 4)
            if contact_tracers[2] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[2].astype(int), 4)
            if contact_tracers[3] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[3].astype(int), 4)
            if contact_tracers[4] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[4].astype(int), 4)
            if contact_tracers[5] is not None:
                pygame.draw.circle(self.surface, color, contact_tracers[5].astype(int), 4)
        