class Enemy():
    def __init__(self, position_x, position_y, difficulty, max_health):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.difficulty : int = difficulty 
        self.current_health : int = max_health
        self.max_health : int = max_health
    
    
    def move(self, player_x, player_y):
        """Moves the enemy in the direction of the player"""

        #Gets direction to the player
        correct_vector = [(player_x - self.position_x)/abs(player_y - self.position_y), (player_y - self.position_y)/abs(player_y - self.position_y)]

        self.position_x += correct_vector[0]
        self.position_y += correct_vector[1]
        pass




