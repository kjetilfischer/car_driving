import pygame
from math import sin, cos, sqrt
import matplotlib.path as pltPath
import numpy as np

class Car:
    def __init__(self,
                surface,
                track,
                xpos,
                ypos,
                width=50,
                length=100,
                angle=0,
                vmax=100,
                acc=10,
                color=(255, 0, 0),
                drift_factor=30, # minimum is 1
                left="K_LEFT",
                right="K_RIGHT",
                up="K_UP",
                down="K_DOWN",
                brake="K_SPACE"):
        
        # static properties
        self.width = width
        self.length = length
        self.vmax = vmax
        self.acc = acc
        self.color = color
        self.surface = surface
        self.drift_factor = drift_factor
        # control keys
        self.kleft = getattr(pygame, left)
        self.kright = getattr(pygame, right)
        self.kup = getattr(pygame, up)
        self.kdown = getattr(pygame, down)
        self.kbrake = getattr(pygame, brake)
        
        # variable properties
        self.angle = angle
        self.old_angles = [0]
        self.drift_counter = 0
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
            if event.key == self.kleft:
                self.turn_left = True
            if event.key == self.kright:
                self.turn_right = True
            if event.key == self.kup:
                self.accelerate = True
            if event.key == self.kdown:
                self.decelerate = True
            if event.key == self.kbrake:
                self.brake = True
        
        if event.type == pygame.KEYUP:
            if event.key == self.kleft:
                self.turn_left = False
            if event.key == self.kright:
                self.turn_right = False
            if event.key == self.kup:
                self.accelerate = False
            if event.key == self.kdown:
                self.decelerate = False
            if event.key == self.kbrake:
                self.brake = False

    
    def draw(self):
        # Drehmatrix
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
        
        self.old_angles.append(self.angle)
        if len(self.old_angles) > self.drift_factor:
            self.old_angles = self.old_angles[-self.drift_factor:]
        
        if self.velo != 0:
            sumx = 0
            sumy = 0
            for angle in self.old_angles:
                sumx += dt* self.velo * sin(angle)
                sumy += dt* self.velo * cos(angle)
            self.xpos = self.xpos + (sumx/self.drift_factor)
            self.ypos = self.ypos - (sumy/self.drift_factor)
            #self.xpos = self.xpos + (dt* self.velo * sin(self.angle))
            #self.ypos = self.ypos - (dt* self.velo * cos(self.angle))
    
    
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

    
    def calculate_intersection(self, L1, L2):
        # calculates the intersection of two given lines in respect to the position vector and the length of the direction vector
        # returns point of intersection in respect to L1
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
        
        # calculate intersections and determine the closest intersection per tracer
        self.contact_tracers = []
        self.tracer_distances = []
        for tracer in self.tracers:
            #contacts = []
            closest_distance = None
            closest_intersection = None
            for line in track.impassable_lines:
                intersection = self.calculate_intersection((self.center, tracer), line)
                if intersection is not None:
                    distance = np.linalg.norm(intersection - self.center)               # intersections - self.center, since we are interested in the distance between the car and the intersection and not the origin and the intersection
                    if closest_distance:
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_intersection = intersection
                    else:
                        closest_distance = distance
                        closest_intersection = intersection 
                #contacts.append(closest_intersection) 
            if closest_intersection is None:
                self.contact_tracers.append(None)
                self.tracer_distances.append(None)                                      # important for autonomous_driving(), since the distance to impassable_lines is important not the location
            else:
                self.contact_tracers.append(np.array(closest_intersection))
                self.tracer_distances.append(closest_distance)

        if show:
            for tracer in self.tracers:
                pygame.draw.line(self.surface, color, self.center, self.center + tracer)
            if self.contact_tracers[0] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[0].astype(int), 4)
            if self.contact_tracers[1] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[1].astype(int), 4)
            if self.contact_tracers[2] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[2].astype(int), 4)
            if self.contact_tracers[3] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[3].astype(int), 4)
            if self.contact_tracers[4] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[4].astype(int), 4)
            if self.contact_tracers[5] is not None:
                pygame.draw.circle(self.surface, color, self.contact_tracers[5].astype(int), 4)
    
    
    def autonomous_driving(self, parameter_sets):
        # include after sensor()
        # decision criteria:
        #   self.tracer_distances
        #   self.velo
        #   track.impassable_lines ?
        # possibilities of action:
        #   press keys: up, left, down, right, space
        # fitness model criteria:
        #   lap_time
        #   checkpoints (maybe)
        
        self.car_states = [self.turn_left, self.turn_right, self.accelerate, self.decelerate, self.brake] # add no_turn for both other turns to be false
        threshold = 1
        for state in car_states:
            for parameter_set in parameter_sets:
                evaluation = parameters[0] * self.tracer_distances[0] + parameters[1] * self.tracer_distances[1] + parameters[2] * self.tracer_distances[2] + parameters[3] * self.tracer_distances[3] + parameters[4] * self.tracer_distances[4] + parameters[5] * self.tracer_distances[5] + parameters[6] * self.velo
                if evaluation < threshold:
                    state = True
                else:
                    state = False
        # [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]]
