from player import Player
import time
from threading import Thread

class player_other(Player):
    def __init__(self, world, name, pid, x, y):
        super().__init__(world, name, pid, x, y)
        self.namecolor=(0,0,0)
        self.isPlayer=True
        
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            try:
                self.move()
                time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
            except:
                pass
    '''
    def move(self, position):
        self.x=position[0]
        self.y=position[1]
       
    '''
    