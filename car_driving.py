import pygame
import sys
from pygame.locals import *
from math import sin, cos
import time
import car
import track
 
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

track = track.Track(windowSurface, window_width, window_height, green, black, white)

car_1 = car.Car(windowSurface,
                track,
                xpos=int(7.5/100 * window_width),
                ypos=int(55/100 * window_height),
                width=20,
                length=40,
                angle=0,
                vmax=0.25,
                acc=0.00025,
                color=red)

clock = pygame.time.Clock()
time_start = time.time()
lap_time = ""

# run the game loop
while True:
    pygame.display.update()
    current_time = str(time.time() - time_start)[:4]
    dt = clock.tick(60)
    windowSurface.fill(white)
    track.draw(current_time, lap_time)
    car_1.update(dt)
    car_1.draw()
    car_1.check_crash(track)
    car_1.check_checkpoint()
    if car_1.finish:
        lap_time = current_time
        time_start = time.time()
        car_1.finish = False
    
    for event in pygame.event.get():
        car_1.controls(event)
        
        if event.type == QUIT:
            print("quit")
            pygame.quit()
            sys.exit()