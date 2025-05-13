import random, pygame

class Goblin_Mage():
    def __init__(self, left_image, right_image,position_x, position_y, difficulty, max_health, Small_Goblin, lsmall_goblin_img, rsmall_goblin_img):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = difficulty 
        self.current_health : int = max_health
        self.max_health : int = max_health
        self.image : str = left_image 
        self.left_image = left_image
        self.right_image = right_image
        #small goblin stats
        self.spawn_time = pygame.time.get_ticks()
        self.spawn_small_goblin_time = 7000
        self.small_goblin_objs = []
        self.small_goblin_Class = Small_Goblin
        self.lsmall_goblin_img = lsmall_goblin_img
        self.rsmall_goblin_img = rsmall_goblin_img

    
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
            self.image = self.right_image
        else:
            self.image = self.left_image

        pass

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
        self.position_x = x
        self.position_y = y

    def get_enemy_rect(self,camera_x,camera_y):
        enemy_width = self.image.get_width()
        enemy_height = self.image.get_height()
        enemyRect = pygame.Rect(self.position_x-camera_x - enemy_width//2, self.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
        return enemyRect
    
    def get_enemy_attackbox(self,camera_x,camera_y):
        enemyRect = pygame.Rect(self.position_x-camera_x - 1, self.position_y-camera_y - 1, 2, 2)
        return enemyRect
        
    def spawn_small_goblins(self, Small_Goblin, left_image, right_image): # maked new smallgoblins around goblinamge
        small_goblin_objs = []
        position_x = [self.position_x - 20, self.position_x, self.position_x +20, self.position_x]
        position_y = [self.position_y, self.position_y+20, self.position_y, self.position_y -20]
        max_health = 8
        difficulty = 10
        for i in range(4):
            small_goblin = Small_Goblin( left_image, right_image,position_x[i], position_y[i], difficulty, max_health)
            self.small_goblin_objs.append(small_goblin)
        pass

    def is_hit(self, player_x, player_y):
        self.current_health -= 1
        pass

    def update(self): # matches time with main and check if its time for spawn
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.spawn_small_goblin_time:
            self.spawn_small_goblins(self.small_goblin_Class,self.lsmall_goblin_img,self.rsmall_goblin_img)
            self.spawn_time = current_time
        pass
        
