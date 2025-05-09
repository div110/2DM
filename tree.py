import random
import pygame


class Tree():
    def __init__(self, image, position_x, position_y):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.image : str = image
        self.width : int = image.get_width()
        self.height : int = image.get_height()

        # treba toto este doladit aby sa to generovalo rovnomerne a neboli hluche miesta ked sa hybem s kamerou

    def get_random_position(self, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        self.position_x = random.randint(-MAXOFFSCREENPOS, WINWIDTH+ MAXOFFSCREENPOS)
        self.position_y = random.randint(-MAXOFFSCREENPOS, WINHEIGHT+MAXOFFSCREENPOS)
        
    def get_random_position_off_screen(self, camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        cameraRect = pygame.Rect(camera_x, camera_y, WINWIDTH, WINHEIGHT)
        while True:
            x = random.randint(camera_x -MAXOFFSCREENPOS, camera_x+ WINWIDTH + MAXOFFSCREENPOS)
            y = random.randint(camera_y -MAXOFFSCREENPOS, camera_y+ WINHEIGHT +MAXOFFSCREENPOS)
            treeRect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)
            if not cameraRect.colliderect(treeRect):
                self.position_x = x
                self.position_y = y
                break


    def is_off_screen(self, camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        pos_X = self.position_x
        pos_Y = self.position_y
        left = camera_x  - MAXOFFSCREENPOS
        top = camera_y  - MAXOFFSCREENPOS
        active_areaRect = pygame.Rect(left, top, WINWIDTH + 2*MAXOFFSCREENPOS, WINHEIGHT + 2*MAXOFFSCREENPOS)
        treeRect = pygame.Rect(pos_X, pos_Y, self.width, self.height)
        return not active_areaRect.colliderect(treeRect)
    
