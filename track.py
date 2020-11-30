import pygame
import numpy as np
import matplotlib.image as mpimg

class Track:
    def __init__(self, track_name, surface, window_width, window_height, color1, color2, color3):
        self.surface = surface
        self.width = window_width
        self.height = window_height
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        
        # START OF TRACK ANALYSIS

        # read image
        self.img = mpimg.imread(track_name)

        # check for track size
        if len(self.img) != self.height or len(self.img[0]) != self.width:
            raise ValueError(f"The size of the track is not {self.width}x{self.height}.")

        # find track limits
        self.track_limits = [[0 for x in range(self.width)] for y in range(self.height)]
        self.start_finish = []
        self.checkpoint = []
        for row in range(len(self.img)):
            for column in range(len(self.img[0])):
                if (self.img[row][column][:3] == [0, 0, 0]).all():
                    self.track_limits[row][column] = 1
                if (self.img[row][column][:3] == [1, 0, 0]).all():      # find markers
                    self.startp1 = (column, row)
                    self.img[row][column][0] = 1                        # hide markers
                    self.img[row][column][1] = 1
                    self.img[row][column][2] = 1
                if (self.img[row][column][:3] == [0, 0, 1]).all():
                    self.startp2 = (column, row)
                    self.img[row][column][0] = 1
                    self.img[row][column][1] = 1
                    self.img[row][column][2] = 1
                if (self.img[row][column][:3] == [0, 1, 0]).all():
                    self.start_finish.append((column, row))
                    self.img[row][column][0] = 1
                    self.img[row][column][1] = 1
                    self.img[row][column][2] = 1
                if (self.img[row][column][:3] == [1, 1, 0]).all():
                    self.checkpoint.append((column, row))
                    self.img[row][column][0] = 1
                    self.img[row][column][1] = 1
                    self.img[row][column][2] = 1
        mpimg.imsave("tmp_track.png", self.img)
        
        # END OF TRACK ANALYSIS
        
        # read image for pygame
        self.pyimg = pygame.image.load("tmp_track.png")

        
        self.myfont = pygame.font.SysFont("Comic Sans MS", 24)

        
    def draw(self, current_time1, current_time2, lap_time1, lap_time2):
        self.surface.blit(self.pyimg, (0,0))
        
        self.current_time1 = self.myfont.render(current_time1, False, self.color2)
        self.current_time2 = self.myfont.render(current_time2, False, self.color2)
        self.surface.blit(self.current_time1, (5,5))
        self.surface.blit(self.current_time2, (750,5))
        self.lap_time1 = self.myfont.render("Red's lap time: " + lap_time1, False, self.color2)
        self.lap_time2 = self.myfont.render("Blue's lap time: " + lap_time2, False, self.color2)
        self.surface.blit(self.lap_time1, (5, 30))
        self.surface.blit(self.lap_time2, (750, 30))
        
        