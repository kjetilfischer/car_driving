import pygame
import numpy as np
import matplotlib.image as mpimg

class Track:
    def __init__(self, surface, window_width, window_height, color1, color2, color3):
        self.surface = surface
        self.width = window_width
        self.height = window_height
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        
        
        s1_x1 = int(15/100 * self.width)
        s1_y1 = int(15/100 * self.height)
        s1_x2 = int(15/100 * self.width)
        s1_y2 = int(85/100 * self.height)
        s1_x3 = int(25/100 * self.width)
        s1_y3 = int(85/100 * self.height)
        s1_x4 = int(25/100 * self.width)
        s1_y4 = int(15/100 * self.height)
        self.s1 = [(s1_x1, s1_y1), (s1_x2, s1_y2), (s1_x3, s1_y3), (s1_x4, s1_y4)]
        
        s2_x1 = int(75/100 * self.width)
        s2_y1 = int(15/100 * self.height)
        s2_x2 = int(75/100 * self.width)
        s2_y2 = int(85/100 * self.height)
        s2_x3 = int(85/100 * self.width)
        s2_y3 = int(85/100 * self.height)
        s2_x4 = int(85/100 * self.width)
        s2_y4 = int(15/100 * self.height)
        self.s2 = [(s2_x1, s2_y1), (s2_x2, s2_y2), (s2_x3, s2_y3), (s2_x4, s2_y4)]
        
        s3_x1 = int(45/100 * self.width)
        s3_y1 = int(0/100 * self.height)
        s3_x2 = int(45/100 * self.width)
        s3_y2 = int(30/100 * self.height)
        s3_x3 = int(55/100 * self.width)
        s3_y3 = int(30/100 * self.height)
        s3_x4 = int(55/100 * self.width)
        s3_y4 = int(0/100 * self.height)
        self.s3 = [(s3_x1, s3_y1), (s3_x2, s3_y2), (s3_x3, s3_y3), (s3_x4, s3_y4)]
        
        s4_x1 = int(45/100 * self.width)
        s4_y1 = int(70/100 * self.height)
        s4_x2 = int(45/100 * self.width)
        s4_y2 = int(100/100 * self.height)
        s4_x3 = int(55/100 * self.width)
        s4_y3 = int(100/100 * self.height)
        s4_x4 = int(55/100 * self.width)
        s4_y4 = int(70/100 * self.height)
        self.s4 = [(s4_x1, s4_y1), (s4_x2, s4_y2), (s4_x3, s4_y3), (s4_x4, s4_y4)]
        
        s5_x1 = int(25/100 * self.width)
        s5_y1 = int(45/100 * self.height)
        s5_x2 = int(25/100 * self.width)
        s5_y2 = int(55/100 * self.height)
        s5_x3 = int(75/100 * self.width)
        s5_y3 = int(55/100 * self.height)
        s5_x4 = int(75/100 * self.width)
        s5_y4 = int(45/100 * self.height)
        self.s5 = [(s5_x1, s5_y1), (s5_x2, s5_y2), (s5_x3, s5_y3), (s5_x4, s5_y4)]
        
        
        # START OF TRACK ANALYSIS

        # read image
        self.img = mpimg.imread("track3.png")

        # check for track size
        if len(self.img) != self.height or len(self.img[0]) != self.width:
            raise ValueError(f"The size of the track is not {self.width}x{self.height}.")

        # find track limits
        self.track_limits = []
        self.start_finish = []
        self.checkpoint = []
        for row in range(len(self.img)):
            for column in range(len(self.img[0])):
                if (self.img[row][column][:3] == [0, 0, 0]).all():
                    self.track_limits.append((column, row))
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
        
        """
        s6_x1 = int(0/100 * self.width)
        s6_y1 = int(49/100 * self.height)
        s6_x2 = int(0/100 * self.width)
        s6_y2 = int(51/100 * self.height)
        s6_x3 = int(15/100 * self.width)
        s6_y3 = int(51/100 * self.height)
        s6_x4 = int(15/100 * self.width)
        s6_y4 = int(49/100 * self.height)
        self.start_finish = [(s6_x1, s6_y1), (s6_x2, s6_y2), (s6_x3, s6_y3), (s6_x4, s6_y4)]
        
        s7_x1 = int(85/100 * self.width)
        s7_y1 = int(49/100 * self.height)
        s7_x2 = int(85/100 * self.width)
        s7_y2 = int(51/100 * self.height)
        s7_x3 = int(100/100 * self.width)
        s7_y3 = int(51/100 * self.height)
        s7_x4 = int(100/100 * self.width)
        s7_y4 = int(49/100 * self.height)
        self.checkpoint = [(s7_x1, s7_y1), (s7_x2, s7_y2), (s7_x3, s7_y3), (s7_x4, s7_y4)]
        """
        
        self.myfont = pygame.font.SysFont("Comic Sans MS", 12)
        self.myfont2 = pygame.font.SysFont("Comic Sans MS", 24)
        self.text = self.myfont.render("START/FINISH", False, self.color3)
        
        
        self.impassable_lines = [[self.s1[0], np.array(self.s1[1]) - np.array(self.s1[0])],
                                [self.s1[1], np.array(self.s1[2]) - np.array(self.s1[1])],
                                [self.s1[2], np.array(self.s1[3]) - np.array(self.s1[2])],
                                [self.s1[3], np.array(self.s1[0]) - np.array(self.s1[3])],
                            
                                [self.s2[0], np.array(self.s2[1]) - np.array(self.s2[0])],
                                [self.s2[1], np.array(self.s2[2]) - np.array(self.s2[1])],
                                [self.s2[2], np.array(self.s2[3]) - np.array(self.s2[2])],
                                [self.s2[3], np.array(self.s2[0]) - np.array(self.s2[3])],
                            
                                [self.s3[0], np.array(self.s3[1]) - np.array(self.s3[0])],
                                [self.s3[1], np.array(self.s3[2]) - np.array(self.s3[1])],
                                [self.s3[2], np.array(self.s3[3]) - np.array(self.s3[2])],
                                [self.s3[3], np.array(self.s3[0]) - np.array(self.s3[3])],
                            
                                [self.s4[0], np.array(self.s4[1]) - np.array(self.s4[0])],
                                [self.s4[1], np.array(self.s4[2]) - np.array(self.s4[1])],
                                [self.s4[2], np.array(self.s4[3]) - np.array(self.s4[2])],
                                [self.s4[3], np.array(self.s4[0]) - np.array(self.s4[3])],
                            
                                [self.s5[0], np.array(self.s5[1]) - np.array(self.s5[0])],
                                [self.s5[1], np.array(self.s5[2]) - np.array(self.s5[1])],
                                [self.s5[2], np.array(self.s5[3]) - np.array(self.s5[2])],
                                [self.s5[3], np.array(self.s5[0]) - np.array(self.s5[3])],
                            
                                [(0,0), (0,self.height)],
                                [(0,self.height), np.array((self.width, self.height))-np.array(((0,self.height)))],
                                [(0,0), (self.width,0)],
                                [(self.width,0), np.array((self.width, self.height))-np.array(((self.width,0)))]]
        
        
        
    def draw(self, current_time1, current_time2, lap_time1, lap_time2):
        """
        pygame.draw.polygon(self.surface, self.color1, self.s1)
        pygame.draw.polygon(self.surface, self.color1, self.s2)
        pygame.draw.polygon(self.surface, self.color1, self.s3)
        pygame.draw.polygon(self.surface, self.color1, self.s4)
        pygame.draw.polygon(self.surface, self.color1, self.s5)
        pygame.draw.polygon(self.surface, self.color2, self.start_finish)
        pygame.draw.polygon(self.surface, self.color3, self.checkpoint)
        self.surface.blit(self.text, (int(2/100 * self.width), int(49/100 * self.height)))
        """
        
        self.surface.blit(self.pyimg, (0,0))
        
        self.current_time1 = self.myfont2.render(current_time1, False, self.color2)
        self.current_time2 = self.myfont2.render(current_time2, False, self.color2)
        self.surface.blit(self.current_time1, (5,5))
        self.surface.blit(self.current_time2, (750,5))
        self.lap_time1 = self.myfont2.render("Red's lap time: " + lap_time1, False, self.color2)
        self.lap_time2 = self.myfont2.render("Blue's lap time: " + lap_time2, False, self.color2)
        self.surface.blit(self.lap_time1, (5, 30))
        self.surface.blit(self.lap_time2, (750, 30))
        
        