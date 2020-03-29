import sys

sys.path.insert(1, '....//network')

from npc import npc

class cow(npc):
    def __init__(self,server, pid, x, y):
        super().__init__(server, pid, x, y)
            
        self.name="cow"
        self.hpmax=5
        self.hp=self.hpmax
        
        self.respawntime=1
        
        #[name, probability, min stack, max stack]
        self.droptable=[
            ["coins", 1, 5, 10],
            ["sword", .2, 1, 1]
                        ]