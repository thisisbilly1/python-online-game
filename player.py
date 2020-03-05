import time
from threading import Thread
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, world, name, pid, x, y):
        super().__init__()
        self.world=world
        self.width=16
        self.height=16
        
        self.image=pygame.Surface((self.width,self.height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        
        #self.rect = pygame.draw.rect(self.world.screen, (0, 0, 128), (64, 54, 16, 16))
        
        self.name=name
        self.running=True

        self.x=x
        self.y=y
        self.x_previous=0
        self.y_previous=0
        
        self.pid=pid
        self.namecolor=(0,0,0)
        

    def getpid(self):
        return self.pid
    
    def updatePosition(self):
        self.image=pygame.Surface((self.width,self.height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect().move(self.x,self.y)
        
        #self.rect=self.rect.move(self.x, self.y)
        
        #self.rect.move_ip(self.x-self.x_previous,self.y-self.y_previous)

    def draw(self):
        #print(str(self.x)+","+str(self.y))
        #self.rect.move(self.x, self.y)
        self.updatePosition()
        self.world.screen.blit(self.image, self.rect)
        
        fontobject = pygame.font.Font(None,18)
        self.world.screen.blit(fontobject.render(self.name, 1, (0,0,0)),(self.x,self.y-self.height)) 
        
        self.x_previous=self.x
        self.y_previous=self.y
        #pygame.draw.rect(self.world.screen, (0, 0, 128), self.rect) # draw the rect at a variable location
        

        
    def stop(self):
        self.running=False
#name=input("name: ")
#player=Player(name).start()