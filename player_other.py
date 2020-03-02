from player import Player
import time

class player_other(Player):
    def __init__(self, name, pid):
        Player.__init__(self,name,pid)

    def update(self):
        while self.running:
            time.sleep(1)
            
    def move(self, position):
        self.x=position[0]
        self.y=position[1]
        

    