import random

class Tree():
    def __init__(self, image, position_x, position_y):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.image : str = image


        # treba toto este doladit aby sa to generovalo rovnomerne a neboli hluche miesta ked sa hybem s kamerou

    def get_random_position(self, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        self.position_x = random.randint(-MAXOFFSCREENPOS, WINWIDTH+ MAXOFFSCREENPOS)
        self.position_y = random.randint(-MAXOFFSCREENPOS, WINHEIGHT+MAXOFFSCREENPOS)
        

    def get_random_position_off_screen(self, moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        if moveUp:
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
            y = random.randint(0,WINWIDTH)
        else:
            x = random.randint(-MAXOFFSCREENPOS, -50) if random.choice([True, False]) else random.randint(WINWIDTH+50, WINWIDTH + MAXOFFSCREENPOS)
            y = random.randint(-MAXOFFSCREENPOS, -50) if random.choice([True, False]) else random.randint(WINHEIGHT+50, WINHEIGHT + MAXOFFSCREENPOS)
        self.position_x = x
        self.position_y = y
        
    
    def is_off_screen(self, camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
        pos_X = self.position_x
        pos_Y = self.position_y
        maxoff = MAXOFFSCREENPOS
        return pos_X+ WINWIDTH+maxoff <camera_x  or pos_Y + WINHEIGHT + maxoff < camera_y or pos_X - WINWIDTH - maxoff > camera_x  or pos_Y - WINHEIGHT - maxoff > camera_y 
    
