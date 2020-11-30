import pygame
from math import sin, cos, sqrt
import matplotlib.path as pltPath
import numpy as np

class Car():
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
                carmodel=None,
                #fric=5, # friction is interpreted as maximum centripetal acceleration (not yet)
                #r_turn=2, # radius of the driven circle when turning
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
        self.vmax_static = vmax
        self.acc = acc
        self.color = color
        self.surface = surface
        if drift_factor < 1:
            raise ValueError("drift_factor should not be smaller than one")
        self.drift_factor = drift_factor
        self.xpos_start = xpos
        self.ypos_start = ypos
        self.angle_start = angle
        self.track = track
        # control keys
        self.kleft = getattr(pygame, left)
        self.kright = getattr(pygame, right)
        self.kup = getattr(pygame, up)
        self.kdown = getattr(pygame, down)
        self.kbrake = getattr(pygame, brake)
        
        # variable properties
        self.vmax = self.vmax_static
        self.angle = self.angle_start
        self.old_angles = [0]
        self.drift_counter = 0
        self.xpos = self.xpos_start
        self.ypos = self.ypos_start
        self.velo = 0.
        
        # load car model
        #if carmodel is not None:                                                                   # not working yet
        #    self.carmodel = pygame.image.load(carmodel)
        #    self.carmodel = pygame.transform.scale(self.carmodel, (self.width, self.length))
        #    self.carmodel = pygame.transform.rotate(self.carmodel, self.angle)
        
        # states of the car
        self.turn_left = False
        self.turn_right = False
        self.accelerate = False
        self.decelerate = False
        self.brake = False
        
        self.checkpoint = False
        self.finish = False
    
    def reset(self):
        self.vmax = self.vmax_static
        self.angle = self.angle_start
        self.old_angles = [0]
        self.drift_counter = 0
        self.xpos = self.xpos_start
        self.ypos = self.ypos_start
        self.velo = 0.
        self.checkpoint = False
    
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
            #if event.key == self.kbrake:
            #    self.brake = True
        
        if event.type == pygame.KEYUP:
            if event.key == self.kleft:
                self.turn_left = False
            if event.key == self.kright:
                self.turn_right = False
            if event.key == self.kup:
                self.accelerate = False
            if event.key == self.kdown:
                self.decelerate = False
            #if event.key == self.kbrake:
            #    self.brake = False

    
    def draw(self):
        # Drehmatrix
        x1 = int(self.xpos - self.width/2*cos(self.angle) + self.length/2*sin(self.angle))
        y1 = int(self.ypos - self.width/2*sin(self.angle) - self.length/2*cos(self.angle))
        
        x2 = int(self.xpos + self.width/2*cos(self.angle) + self.length/2*sin(self.angle))
        y2 = int(self.ypos + self.width/2*sin(self.angle) - self.length/2*cos(self.angle))
        
        x3 = int(self.xpos + self.width/2*cos(self.angle) - self.length/2*sin(self.angle))
        y3 = int(self.ypos + self.width/2*sin(self.angle) + self.length/2*cos(self.angle))
        
        x4 = int(self.xpos - self.width/2*cos(self.angle) - self.length/2*sin(self.angle))
        y4 = int(self.ypos - self.width/2*sin(self.angle) + self.length/2*cos(self.angle))
        
        self.points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        pygame.draw.polygon(self.surface, self.color, self.points)
        #self.carmodel = pygame.transform.rotate(self.carmodel, self.angle)     # not working yet
        #self.surface.blit(self.carmodel, (x1, y1))

    
    def update(self, dt):
        # driving physics; update variable properties
        if self.velo > self.vmax and self.velo > 0:
            self.velo = self.vmax
        if self.velo < -self.vmax/2 and self.velo < 0:
            self.velo = -self.vmax/2
        if self.turn_left:
            self.angle -= (0.015 * self.velo * dt) # - (0.01 * (self.velo*self.velo/self.vmax) * dt)
        if self.turn_right:
            self.angle += (0.015 * self.velo * dt) # - (0.01 * (self.velo*self.velo/self.vmax) * dt)
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
        
        # drift physics
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
                if point in self.track.checkpoint:
                    self.checkpoint = True
                if self.checkpoint:
                    break
        # finish
        if self.checkpoint and not self.finish:
            for point in self.points:
                if point in self.track.start_finish:
                    self.finish = True
                    self.checkpoint = False
                if self.finish:
                    break
    
    
    def check_crash(self, track, dt):
        for point in self.points:
            # check for window boundaries first
            if point[0] < 0 or point[0] > track.width:
                crash = True
                crash_bounds = True
            elif point[1] < 0 or point[1] > track.height:
                crash = True
                crash_bounds = True
            elif track.track_limits[point[1]][point[0]]:
                crash = True
                crash_bounds = True
            else:
                crash = False
                crash_bounds = False
            if crash:
                break
        if crash:
            self.velo = self.velo * (-1)
            #self.vmax = self.vmax_static/10 * 0
            #self.xpos -= dt * 1.2 *(self.velo) * sin(self.angle) #not working yet
            #self.ypos -= dt * 1.2 *(self.velo) * cos(self.angle)
        else:
            self.vmax = self.vmax_static
        if crash_bounds:
            out_of_bounds_x_left = []
            out_of_bounds_x_right = []
            out_of_bounds_y_top = []
            out_of_bounds_y_bot = []
            for point in self.points:
                if point[0] < 0:
                    out_of_bounds_x_left.append(True)
                else:
                    out_of_bounds_x_left.append(False)
                if point[0] > track.width:
                    out_of_bounds_x_right.append(True)
                else:
                    out_of_bounds_x_right.append(False)
                if point[1] < 0:
                    out_of_bounds_y_top.append(True)
                else:
                    out_of_bounds_y_top.append(False)
                if point[1] > track.height:
                    out_of_bounds_y_bot.append(True)
                else:
                    out_of_bounds_y_bot.append(False)
            if all(out_of_bounds_x_left) or all(out_of_bounds_x_right) or all(out_of_bounds_y_top) or all(out_of_bounds_y_bot):
                self.reset()

    
    def calculate_intersection(self, L1, L2):    # not necessary for the code right now
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
            if all(0 < item <= 1 for item in solved):       # if solved[0] <= 1 and solved[0] > 0 and solved[1] <= 1 and solved[1] > 0:
                Pxy = np.array([(x1 + (x2 * solved[0])), (y1 + (y2 * solved[0]))])
            else:
                Pxy = None
        except np.linalg.LinAlgError:
            Pxy = None
        return Pxy
    
    def multidim_intersect(self, arr1, arr2):     # https://stackoverflow.com/questions/9269681/intersection-of-2d-numpy-ndarrays       # not necessary for the code right now
        arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
        arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
        intersected = np.intersect1d(arr1_view, arr2_view)
        return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])
    
    def list_intersections(self, lst_1, lst_2):   # not necessary for the code right now
        intersections = [point for point in lst_1 if point in lst_2]
        return intersections
    
    
    def sensor(self, track, tracer_length=200, tracer_directions=[0], color=(0,0,0), show=False):   
        
        self.tracers = np.array([(tracer_length * sin(self.angle + direction), tracer_length * (-cos(self.angle + direction))) for direction in tracer_directions])
        self.center = np.array((self.xpos, self.ypos))
        
        self.tracer_points = []
        self.intersections = []
        
        # calculate intersections
        for tracer in self.tracers:
            self.tracer_points = [self.center + (length/tracer_length * tracer) for length in range(tracer_length)]
            for point in self.tracer_points:
                if track.track_limits[int(point[1])][int(point[0])]:
                    self.intersections.append(point)
                    break
        
        if show:
            for tracer in self.tracers:
                pygame.draw.line(self.surface, color, self.center, self.center + tracer)
            for intersection in self.intersections:
                if intersection is not None:
                    pygame.draw.circle(self.surface, color, intersection.astype(int), 4)
    
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
