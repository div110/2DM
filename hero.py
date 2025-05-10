import pygame

class Hero():
    def __init__(self,image, position_x, position_y, level, max_health, heart_image,bheart_r_image,bheart_l_image):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.current_health : int = max_health
        self.image : str = image
        self.level : int = level
        self.max_health : int = max_health
        self.heart_image : str = heart_image
        self.bheart_r_image : str = bheart_r_image
        self.bheart_l_image : str = bheart_l_image
    
    def is_alive(self):
        if self.health_points <= 0:
            return False
        else:
            return True

    
    def draw_health_bar(self,DISPLAYSURF):
        for i in range(self.max_health):
            if i%2 == 0 and self.current_health>i:
                DISPLAYSURF.blit(self.heart_image,(10 + i*10, 10))
            elif self.current_health<=i and  i%2==0:
                DISPLAYSURF.blit(self.bheart_r_image,(9 + i*10, 10))
            elif self.current_health<=i and  i%2==1:
                DISPLAYSURF.blit(self.bheart_l_image,(0 + i*10, 10))
        return

