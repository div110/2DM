class Hero():
    def __init__(self,position_x, position_y, max_health):
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

    
