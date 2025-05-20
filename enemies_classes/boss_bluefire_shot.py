import random, pygame

class Bluefire_Shot():
    def __init__(self, image,position_x, position_y, difficulty, direction):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = 4
        self.image : str = image 
        self.direction = direction
        self.max_health = 5
        self.current_health = self.max_health

    
    
    def move(self, player_x, player_y):
        """Moves the enemy in the direction of the player
            The difficulty solution is NOT Final
        """
            
        #Gets direction to the player
        move_vector = [(player_x - self.position_x),(player_y - self.position_y)]
        #print(move_vector)


        #This loop shrinks the vector to fit our difficulty
        while (move_vector[0]**2 + move_vector[1]**2) > self.difficulty**2:
            move_vector[0] = move_vector[0] / (1.1)
            move_vector[1] = move_vector[1] / (1.1)
         


        #This does the moving of the enemy
        self.position_x += move_vector[0]
        self.position_y += move_vector[1]
       
        #switch image
        if move_vector[0] > 0:
            self.image = self.image
        else:
            self.image = self.image

        pass
       

    def get_enemy_rect(self,camera_x,camera_y):
        enemy_width = self.image.get_width()
        enemy_height = self.image.get_height()
        enemyRect = pygame.Rect(self.position_x-camera_x - enemy_width//2, self.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
        return enemyRect
    
    def get_enemy_attackbox(self,camera_x,camera_y):
        enemyRect = pygame.Rect(self.position_x-camera_x - 1, self.position_y-camera_y - 1, 2, 2)
        return enemyRect
    
    def is_hit(self,player_x, player_y, damage):
        self.current_health -= damage
        