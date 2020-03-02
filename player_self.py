from player import Player

class player_self(Player):
    def __init__(self, name, pid, client):
        Player.__init__(self,name,pid)
        self.client=client

    def move(self, xdir, ydir):
        if not (ydir==0 and xdir==0):
            self.x+=xdir
            self.y+=ydir
            #send packet
            self.client.sendmove(self.x,self.y)
        