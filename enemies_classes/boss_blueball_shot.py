import random, pygame

class Blueball_Shot():
    def __init__(self, image,position_x, position_y, difficulty, direction, destroyed_image):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = 4
        self.image : str = image 
        self.direction = direction
        self.max_health = 5
        self.current_health = self.max_health
        self.destroyed_image = destroyed_image
        self.remove_destroyed_time = 4000
        self.destroyed_time = None
        self.time_to_remove = False

    
    
    def move(self, player_x, player_y):
        """Moves the enemy in the direction of the player
            The difficulty solution is NOT Final
        """
        if self.image == self.destroyed_image:
            return
            
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

    def get_destroyed(self):
        self.image = self.destroyed_image
        self.destroyed_time = pygame.time.get_ticks()
        self.current_health = 10000

    def update(self): # matches time with main and check if its time for spawn
        current_time = pygame.time.get_ticks()
        if not self.destroyed_time == None:
            if current_time - self.destroyed_time > self.remove_destroyed_time:
                self.time_to_remove = True
            pass
        if self.current_health == 0:
            self.get_destroyed()
            
        
        