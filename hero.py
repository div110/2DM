class hero():
    def __init__(self,position_x, position_y, health_points):
        self.position_x : int = position_x
        self.position_y : int = position_y
        self.health_points : int = health_points
        self.image : str = image
        self.level : int = level
        self.max_health : int = max_health
    
    def is_alive(self):
        if self.health_points <= 0:
            return False
        else:
            return True

    
