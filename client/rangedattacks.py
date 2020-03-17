import pygame
from threading import Thread
import time
class rangedAttack:
    def __init__(self,world,target,x,y):
        self.x=x
        self.y=y
        self.world=world
        self.target=target
        self.running=True
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        if self.target==None:
            self.stop()
        else:
            xvel=((self.target.x+self.target.w/2)-self.x)/45
            yvel=((self.target.y+self.target.h/2)-self.y)/45
            
        while self.running:
            if self.target==None:
                self.stop()
                break
            else:
                self.x+=xvel
                self.y+=yvel
                if time.time()-start_time>45/self.world.FPS:
                    self.stop()

            time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
    def draw(self):
        xx=self.world.viewport[0]
        yy=self.world.viewport[1]
        pygame.draw.circle(self.world.screen, (0,255,255), (int(self.x+xx),int(self.y+yy)), 5)
        
    def stop(self):
        self.running=False
        if self in self.world.attacks:
            self.world.attacks.remove(self)