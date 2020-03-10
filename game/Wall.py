import sys
sys.path.insert(1, 'D:/work/python online game/game')
from Obj import Obj
import pygame
class Wall(Obj):
    def __init__(self,world,x,y,w,h):
        self.world=world
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.color=(128, 255, 0)
        self.solid=True

        self.image=pygame.Surface((self.w,self.h))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        
    def draw(self):
        self.rect = self.image.get_rect().move(int(self.x),int(self.y))
        self.world.screen.blit(self.image, self.rect)