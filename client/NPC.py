import time
from threading import Thread
import pygame
from player import Player


def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False

class NPC(Player):
    def __init__(self, world, name, NPCID, x, y, hpmax):
        super().__init__(world, name, NPCID, x, y)
        self.namecolor=(0,0,0)
        self.w=32
        self.h=32
        
        self.hpmax=hpmax
        self.hp=hpmax
        self.isPlayer=0
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            try:
                if self.hp>0:
                    self.move()
                    xx=self.world.viewport[0]
                    yy=self.world.viewport[1]
                    if self.world.mouse_left_down:
                        if checkmousebox([self.x+xx,self.y+yy,self.w,self.h],(self.world.mouse_x,self.world.mouse_y)):
                            self.world.combatstatusbars.target=self
                            #print("al;sdjfl")
                     
                time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
            except Exception as e:
                print(e)
                pass