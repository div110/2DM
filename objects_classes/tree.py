import random
import pygame


class Tree():
    def __init__(self, image, position_x, position_y, treeimgwidth, treeimgheight):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.image : str = image
        self.width = treeimgwidth
        self.height = treeimgheight

        # treba toto este doladit aby sa to generovalo rovnomerne a neboli hluche miesta ked sa hybem s kamerou

    def get_random_position(self, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        self.position_x = random.randint(-MAXOFFSCREENPOS, WINWIDTH+ MAXOFFSCREENPOS)
        self.position_y = random.randint(-MAXOFFSCREENPOS, WINHEIGHT+MAXOFFSCREENPOS)
        
    def get_random_position_off_screen(self, moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        if moveUp and moveRight:
            r_choice = random.choice([True, False])
            if r_choice:
                x = random.randint(0, WINWIDTH + MAXOFFSCREENPOS)
                y = random.randint(-MAXOFFSCREENPOS, -50) 
            else:
                x = random.randint(WINWIDTH, WINWIDTH + MAXOFFSCREENPOS)
                y = random.randint(-MAXOFFSCREENPOS, WINHEIGHT)

        elif moveUp and moveLeft:
            r_choice = random.choice([True, False])
            if r_choice:
                x = random.randint(-MAXOFFSCREENPOS, WINWIDTH)
                y = random.randint(-MAXOFFSCREENPOS, -50)
            else:
                x = random.randint(-MAXOFFSCREENPOS, -50)
                y = random.randint(-MAXOFFSCREENPOS, WINHEIGHT)

        elif moveDown and moveRight:
            r_choice = random.choice([True, False])
            if r_choice:
                x = random.randint(0, WINWIDTH + MAXOFFSCREENPOS)
                y = random.randint(WINHEIGHT + 50, WINHEIGHT + MAXOFFSCREENPOS)
            else:
                x = random.randint(WINWIDTH, WINWIDTH + MAXOFFSCREENPOS)
                y = random.randint(0, WINHEIGHT + MAXOFFSCREENPOS)

        elif moveDown and moveLeft:
            r_choice = random.choice([True, False])
            if r_choice:
                x = random.randint(-MAXOFFSCREENPOS, WINWIDTH)
                y = random.randint(WINHEIGHT + 50, WINHEIGHT + MAXOFFSCREENPOS)
            else:
                x = random.randint(-MAXOFFSCREENPOS, -50)
                y = random.randint(0, WINHEIGHT + MAXOFFSCREENPOS)
        elif moveUp:
            x = random.randint(0,WINWIDTH) 
            y = random.randint(-MAXOFFSCREENPOS, -50)
        elif moveDown:
            x = random.randint(0,WINWIDTH) 
            y = random.randint(WINHEIGHT+50, WINHEIGHT + MAXOFFSCREENPOS)
        elif moveLeft:
            x = random.randint(-MAXOFFSCREENPOS, -50)
            y = random.randint(0,WINHEIGHT) 
        elif moveRight:
            x =random.randint(WINWIDTH+50, WINWIDTH + MAXOFFSCREENPOS)
            y = random.randint(0,WINHEIGHT)
        else:
            x = random.randint(-MAXOFFSCREENPOS, -50) if random.choice([True, False]) else random.randint(WINWIDTH+50, WINWIDTH + MAXOFFSCREENPOS)
            y = random.randint(-MAXOFFSCREENPOS, -50) if random.choice([True, False]) else random.randint(WINHEIGHT+50, WINHEIGHT + MAXOFFSCREENPOS)
        return x, y
        
    
    def is_off_screen(self, camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        pos_X = self.position_x
        pos_Y = self.position_y
        left = camera_x  - MAXOFFSCREENPOS
        top = camera_y  - MAXOFFSCREENPOS
        active_areaRect = pygame.Rect(left, top, WINWIDTH + 2*MAXOFFSCREENPOS, WINHEIGHT + 2*MAXOFFSCREENPOS)
        treeRect = pygame.Rect(pos_X, pos_Y, self.width, self.height)
        return not active_areaRect.colliderect(treeRect)
    
    def get_tree_rect(self,camera_x,camera_y):
        tree_width = self.width
        tree_height = self.height
        treeRect = pygame.Rect(self.position_x-camera_x - tree_width//2, self.position_y-camera_y-tree_height//2, tree_width, tree_height)
        return treeRect
    