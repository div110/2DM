import random, pygame

class Fire_Shot():
    def __init__(self, image,position_x, position_y, difficulty, direction):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = difficulty 
        self.image : str = image 
        self.direction = direction

    
    
    def move(self):
        if self.direction == "right":
            self.position_x += 1
        elif self.direction == "left":
            self.position_x -=1
       

    def get_enemy_rect(self,camera_x,camera_y):
        enemy_width = self.image.get_width()
        enemy_height = self.image.get_height()
        enemyRect = pygame.Rect(self.position_x-camera_x - enemy_width//2, self.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
        return enemyRect
    
    def get_enemy_attackbox(self,camera_x,camera_y):
        enemyRect = pygame.Rect(self.position_x-camera_x - 1, self.position_y-camera_y - 1, 2, 2)
        return enemyRect
        