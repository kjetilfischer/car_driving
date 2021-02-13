import pygame
import sys
from pygame.locals import *
from math import sin, cos
import time
import car
import track
import numpy as np
 
# set up pygame
pygame.init()
pygame.font.init()

# set up the window
window_height = 800
window_width = 1000
windowSurface = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption("Car driving")

# set up the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# draw the white background onto the surface
windowSurface.fill(white)

track = track.Track("track1.png", windowSurface, window_width, window_height, green, black, white)


#car_1 = car.Car(windowSurface,
#                track,
#                xpos=track.startp1[0],
#                ypos=track.startp1[1],
#                width=20,
#                length=40,
#                angle=0,
#                vmax=0.25,
#                acc=0.00025,
#                carmodel="redcar.png",
#                color=red,
#                drift_factor=1,
#                left="K_a",
#                right="K_d",
#                up="K_w",
#                down="K_s")

car_2 = car.Car(windowSurface,
                track,
                xpos=track.startp2[0],
                ypos=track.startp2[1],
                width=20,
                length=40,
                angle=0,
                vmax=0.1,
                acc=0.00025,
                carmodel="bluecar.png",
                color=blue,
                drift_factor=1,
                left="K_LEFT",
                right="K_RIGHT",
                up="K_UP",
                down="K_DOWN")

clock = pygame.time.Clock()
time_start1 = time.time()
time_start2 = time_start1
lap_time1 = ""
lap_time2 = ""

# run the game loop
while True:
    pygame.display.update()
    current_time1 = f"{time.time() - time_start1:.2f}"
    current_time2 = f"{time.time() - time_start2:.2f}"
    dt = clock.tick(60)
    windowSurface.fill(white)
    track.draw(current_time1, current_time2, lap_time1, lap_time2)
#    car_1.update(dt)
    car_2.update(dt)
#    car_1.draw()
    car_2.draw()
#    car_1.sensor(track, tracer_length=300, tracer_directions=[0, np.pi/4, -np.pi/4, np.pi/2, -np.pi/2, np.pi], color=black, show=True)
    car_2.sensor(track, tracer_length=300, tracer_directions=[0, np.pi/4, -np.pi/4, np.pi/2, -np.pi/2, np.pi], color=black, show=True)
#    car_1.check_crash(track, dt)
    car_2.check_crash(track, dt)
#    car_1.check_checkpoint()
    car_2.check_checkpoint()
#    if car_1.finish:
#        lap_time1 = current_time1
#        time_start1 = time.time()
#        car_1.finish = False
    if car_2.finish:
        lap_time2 = current_time2
        time_start2 = time.time()
        car_2.finish = False
    
    for event in pygame.event.get():
#        car_1.controls(event)
        car_2.controls(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
#                car_1.reset()
                car_2.reset()
                time_start = time.time()
                lap_time1 = ""
                lap_time2 = ""
                
        if event.type == QUIT:
            print("quit")
            pygame.quit()
            sys.exit()