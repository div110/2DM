import pygame

class Hero():
    def __init__(self,image, position_x, position_y, level, max_health, heart_image,bheart_r_image,bheart_l_image, image_mage, limage_mage, l_image, fire_shot_class,
                  rfire_shot_img, lfire_shot_img):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.current_health : int = max_health
        self.image : str = image
        self.rimage_mage : str = image_mage
        self.rimage_sword : str = image
        self.limage_mage : str = limage_mage
        self.limage_sword : str = l_image
        self.level : int = level
        self.max_health : int = max_health
        self.heart_image : str = heart_image
        self.bheart_r_image : str = bheart_r_image
        self.bheart_l_image : str = bheart_l_image
        self.weapon_mode = "sword"
        self.direction = "right"
        self.fire_shots_objs = None
        self.fire_shot_class = fire_shot_class
        self.rfire_shotimg = rfire_shot_img
        self.lfire_shotimg = lfire_shot_img
        self.fire_shot_charge_time = 1500
        self.fire_shot_charged = True
        self.spawn_time = pygame.time.get_ticks()
        
    
    def is_alive(self):
        if self.current_health <= 0:
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

    def get_hero_rect(self,camera_x,camera_y):
        hero_width = self.image.get_width()
        hero_height = self.image.get_height()
        heroRect = pygame.Rect(self.position_x-camera_x - hero_width//2, self.position_y-camera_y-hero_height//2, hero_width, hero_height)
        return heroRect
    
    def get_hero_hitbox(self, camera_x, camera_y):
        heroRect = pygame.Rect(self.position_x-camera_x-2 , self.position_y-camera_y-2, 4, 4)
        return heroRect
    
    def change_equipment(self):
        if self.weapon_mode == "sword":
            if self.direction == "right":
                self.image = self.rimage_mage
                self.weapon_mode = "mage"
            elif self.direction == "left":
                self.image = self.limage_mage
                self.weapon_mode = "mage"
        elif self.weapon_mode == "mage":
            if self.direction == "right":
                self.image = self.rimage_sword
                self.weapon_mode = "sword"
            elif self.direction == "left":
                self.image = self.limage_sword
                self.weapon_mode = "sword"
        pass

    def generate_fire_shot(self):
        if self.fire_shot_charged == True:
            if self.direction == "right":
                fsimage = self.rfire_shotimg
                xpos = self.position_x +60
            elif self.direction == "left":
                xpos = self.position_x -60
                fsimage = self.lfire_shotimg
            ypos = self.position_y
            self.fire_shot_charged = False
            return self.fire_shot_class(fsimage, xpos, ypos, 12, self.direction)
         

        pass

    def update(self): # matches time with main and check if its time for spawn
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.fire_shot_charge_time:
            self.fire_shot_charged = True
            self.spawn_time = current_time
        pass