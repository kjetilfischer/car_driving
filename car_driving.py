import pygame
import sys
from pygame.locals import *
import car

# set up pygame
pygame.init()

# set up the window
window_height = 800
window_width = 1000
windowSurface = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption("Car driving")

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# draw the white background onto the surface
windowSurface.fill(WHITE)

#pygame.draw.rect(windowSurface,BLUE,(100, 100, 100, 50)) # {display, color, (left, top, width, height)}
car_1 = car.Car(windowSurface, xpos=window_width/2, ypos=window_height/2, width=50, length=100, angle=2, vmax=100, acc=10, color=RED)





# run the game loop
while True:
    windowSurface.fill(WHITE)
    car_1.draw()
    
    # draw thge window onto the screen
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_1.angle += -0.1
                print("anlge1")
            #car_1.draw()
            #pygame.display.update()
            if event.key == pygame.K_RIGHT:
                car_1.angle += +0.1
                print("anlge2")
            #car_1.draw()
            #pygame.display.update()
        if event.type == QUIT:
            print("quit")
            pygame.quit()
            sys.exit()


"""
# set up the fonts
basicFont = pygame.font.SysFont(None, 48)

# set up the text
text = basicFont.render("Hello world!", True, WHITE, BLUE)
textRect = text.get_rect()
textRect.centerx = windowSurface.get_rect().centerx
textRect.centery = windowSurface.get_rect().centery

# draw the white background onto the surface
windowSurface.fill(WHITE)

# draw a green polygon onto the surface
pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106),  (236, 277), (56, 277), (0, 106)))

# draw some blue lines onto the surface
pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120), 4)
pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)

# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = BLACK
del pixArray

# draw the text onto the surface
#windowSurface.blit(text, textRect)
"""