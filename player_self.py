from player import Player

class player_self(Player):
    def __init__(self, world, name, pid,  x, y):
        super().__init__(world, name, pid, x, y)
        self.world=world
        self.client=self.world.client
        self.namecolor=(255,0,255)
        
    def move(self, xdir, ydir):
        if not (ydir==0 and xdir==0):
            self.x+=xdir
            self.y+=ydir
            #send packet
            self.client.sendmove(self.x,self.y)
    
    
    def startPosition(self,position):
        self.x=position[0]
        self.y=position[1]
