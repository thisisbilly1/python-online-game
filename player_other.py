from player import Player
import time

class player_other(Player):
    def __init__(self, world, name, pid, x, y):
        super().__init__(world, name, pid, x, y)
        self.namecolor=(0,0,0)

        
    def move(self, position):
        self.x=position[0]
        self.y=position[1]
       

    