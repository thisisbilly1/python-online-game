from player import Player
import pygame

class player_self(Player):
    def __init__(self, world, name, pid,  x, y):
        super().__init__(world, name, pid, x, y)
        self.world=world
        self.client=self.world.client
        self.namecolor=(255,0,255)
    def update(self):
        xdir=0
        ydir=0
        if self.world.chat.chatting==False:
            for key in self.world.keyspressed:#pygame.event.get():
                if key == pygame.K_w:
                    ydir=-1
                elif key == pygame.K_s:
                    ydir=1
                elif key == pygame.K_a:
                    xdir=-1
                elif key == pygame.K_d:
                    xdir=1   
            self.move(xdir,ydir)   
    def move(self, xdir, ydir):
        if not (ydir==0 and xdir==0):
            if (0<self.x+xdir<self.world.screen.get_width()-self.width
            and 0<self.y+ydir<self.world.screen.get_height()-self.height):
                self.x+=xdir
                self.y+=ydir
                #send packet
                self.client.sendmove(self.x,self.y)
    
    def startPosition(self,position):
        self.x=position[0]
        self.y=position[1]

