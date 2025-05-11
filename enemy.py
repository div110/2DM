class Enemy():
    def __init__(self, left_image, right_image,position_x, position_y, difficulty, max_health):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = difficulty 
        self.current_health : int = max_health
        self.max_health : int = max_health
        self.image : str = left_image 
        self.left_image = left_image
        self.right_image = right_image
    
    
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



