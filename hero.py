import pygame

class Hero():
    def __init__(self,image, position_x, position_y, level, max_health):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.current_health : int = max_health
        self.image : str = image
        self.level : int = level
        self.max_health : int = max_health
    
    def is_alive(self):
        if self.health_points <= 0:
            return False
        else:
            return True

    
    def draw_health_bar(self,DISPLAYSURF):
        pygame.draw.rect(DISPLAYSURF,(150,150,150),(0,0,150,30))
        pygame.draw.rect(DISPLAYSURF,(255,0,0),(5,5,140*(self.current_health//self.max_health),20))
        return
