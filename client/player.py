import time
from threading import Thread
import pygame
import sys
sys.path.insert(1, 'D:/work/python online game/game')
from Obj import Obj

class Player(Obj):
    def __init__(self, world, name, pid, x, y):
        self.world=world
        self.width=16
        self.height=16
        super().__init__(self.world,x,y,self.width,self.height)
        

        
        #self.image=pygame.Surface((self.width,self.height))
        #self.image.fill((255,0,0))
        #self.rect = self.image.get_rect()
        
        self.name=name
        self.running=True

        #self.x=x
        #self.y=y
        self.x_previous=x
        self.y_previous=y
        
        self.pid=pid
        self.namecolor=(0,0,0)

        self.inputs=[0,0,0,0]#left,right,up,down
        self.friction=0.1
         
    def getpid(self):
        return self.pid
    
    def move(self):
        xdir=(self.inputs[1]-self.inputs[0])*.1
        #ydir=(self.inputs[3]-self.inputs[2])*.1

        if self.inputs[2] and self.onground:
            self.yvel=-4.0
            

        #if (0<self.x+xdir<self.world.screen.get_width()-self.width):
        #and 0<self.y+ydir<self.world.screen.get_height()-self.height):
        self.xvel+=xdir
        
        self.collision()
        
        self.x+=self.xvel
        self.y+=self.yvel
            
        self.xvel=self.xvel*(1-self.friction)
        
        #print(self.x,self.y)

    def draw(self):
        xx=self.world.viewport[0]
        yy=self.world.viewport[1]
        box=[self.x+xx,self.y+yy,self.w,self.h]
        pygame.draw.rect(self.world.screen, (255,0,0),
                         (box[0],box[1],
                          box[2],box[3]), 0)
        
        #self.rect.move(self.x, self.y)
        #self.rect = self.image.get_rect().move(int(self.x),int(self.y))
        #self.world.screen.blit(self.image, self.rect)
        

        self.world.screen.blit(self.world.fontobject.render(self.name, 1, (0,0,0)),(box[0],box[1]-box[3])) 
        
        self.x_previous=self.x
        self.y_previous=self.y
        #pygame.draw.rect(self.world.screen, (0, 0, 128), self.rect) # draw the rect at a variable location
        

        
    def stop(self):
        self.running=False
#name=input("name: ")
#player=Player(name).start()