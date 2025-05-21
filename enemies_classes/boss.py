import random, pygame

class Boss():
    def __init__(self, image, image_barrier, image_no_barrier,position_x, position_y, max_health, Projectile_Class, Projectile_image):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.current_health : int = max_health
        self.max_health : int = max_health
        self.image : str = image
        self.image_barrier : str = image_barrier  
        self.image_no_barrier : str = image_no_barrier
        self.spawn_time = pygame.time.get_ticks()
        self.barrier = True
        self.attack_time = 3000
        self.barier_break_time = None
        self.barier_recharge = 4000
        self.Projectile_Class = Projectile_Class
        self.Projectile_image = Projectile_image
        self.projectile_objs = []

    def change_barrier_state(self):
        if self.image == self.image_barrier:
            self.spawn_time = pygame.time.get_ticks()
            self.image = self.image_no_barrier
            self.barrier = False
        elif self.image == self.image_no_barrier:
            self.image = self.image_barrier
            self.barrier = True
        pass


    def get_enemy_rect(self,camera_x,camera_y):
        enemy_width = self.image.get_width()
        enemy_height = self.image.get_height()
        enemyRect = pygame.Rect(self.position_x-camera_x - enemy_width//2, self.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
        return enemyRect
    
    def get_enemy_attackbox(self,camera_x,camera_y):
        enemyRect = pygame.Rect(self.position_x-camera_x - 1, self.position_y-camera_y - 1, 2, 2)
        return enemyRect
        
    def is_hit(self, player_x, player_y, damage):
        if not self.barrier:
            self.current_health -= damage
        pass

    def attack(self):
        projectile_position_y = random.randint(self.position_y-250,self.position_y+250)
        projectile = self.Projectile_Class(self.Projectile_image,self.position_x,projectile_position_y,10,"right")
        self.projectile_objs.append(projectile)
        pass

    def update(self): # matches time with main and check if its time for spawn
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.attack_time:
            self.attack()
            self.spawn_time = current_time
            pass
        if not self.barier_break_time == None:
            if current_time - self.barier_break_time > self.barier_recharge:
                self.change_barrier_state()
                self.barier_break_time = None
            pass
        if self.barrier == False:
            if self.barier_break_time == None:
                self.barier_break_time = current_time
        pass
        
