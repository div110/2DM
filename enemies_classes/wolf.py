import random, pygame

class Wolf():
    def __init__(self, left_image, right_image, running_left_image, running_right_image, position_x, position_y, speed, max_health, air_image):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.speed : int = 20 * speed 
        self.current_health : int = max_health
        self.max_health : int = max_health
        self.image : str = left_image 
        self.left_image = left_image
        self.right_image = right_image
        self.running_left_image = running_left_image
        self.running_right_image = running_right_image
        self.air_image = air_image
        self.knockback = 25
        self.counter = 0
        self.vector = [0,0] 
    
    def move(self, player_x, player_y):
        """Moves the enemy in the direction of the player
            The speed solution is NOT Final
        """
            

        if self.counter % 50 == 0:
            self.counter += 1
            #Gets direction to the player
            self.vector = [(player_x - self.position_x),(player_y - self.position_y)]
            #print(self.vector)
            #This loop shrinks the vector to fit our speed
            while (self.vector[0]**2 + self.vector[1]**2) > self.speed**2:
                self.vector[0] = self.vector[0] / (1.1)
                self.vector[1] = self.vector[1] / (1.1)
        
        elif self.counter % 23 == 0:
            self.counter += 1
            self.vector = [0,0]
        else:
            self.counter += 1
            if self.counter % 49 == 0:
                self.counter = 0
            #This does the moving of the enemy
            self.position_x += self.vector[0]
            self.position_y += self.vector[1]
       
        #switch image
        if self.vector[0] > 0:
            self.image = self.running_right_image
        elif self.vector[0] < 0:
            self.image = self.running_left_image
        else:
            if self.image == self.running_right_image:
                self.image = self.right_image
            elif self.image == self.running_left_image:
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
        enemyRect = pygame.Rect(self.position_x-camera_x - 20, self.position_y-camera_y - 20, 40, 40)
        return enemyRect
        
    def is_hit(self, player_x, player_y, damage):
        self.current_health -= damage
        enemy_player_vector = [(self.position_x - player_x),(self.position_y - player_y)]
        if enemy_player_vector[0] < 0:
            enemy_player_vector[0] = -self.knockback
        else:
            enemy_player_vector[0] = self.knockback

        if enemy_player_vector[1] < 0:
            enemy_player_vector[1] = -self.knockback
        else:
            enemy_player_vector[1] = self.knockback    
        self.position_x += enemy_player_vector[0]
        self.position_y += enemy_player_vector[1]
