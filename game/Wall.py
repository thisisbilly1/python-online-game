import sys
from Obj import Obj

import pygame
class wall(Obj):
    def __init__(self,world,x,y,w,h):
        self.world=world
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.color=(128, 255, 0)
        self.solid=True

        #self.image=pygame.Surface((self.w,self.h))
        #self.image.fill((0,0,0))
        #self.rect = self.image.get_rect()
        
    def draw(self):
        xx=self.world.viewport[0]
        yy=self.world.viewport[1]
        box=[self.x+xx,self.y+yy,self.w,self.h]
        
        pygame.draw.rect(self.world.screen, (0,0,0),
                         (box[0],box[1],
                          box[2],box[3]), 0)
        
        #self.rect = self.image.get_rect().move(int(self.x),int(self.y))
        #self.world.screen.blit(self.image, self.rect)