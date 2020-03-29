from player import Player
import time
from threading import Thread


def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False


class player_other(Player):
    def __init__(self, world, name, pid, x, y, hpmax, manamax, staminamax):
        super().__init__(world, name, pid, x, y)
        self.namecolor=(0,0,0)
        self.isPlayer=True
        self.world=world
        
        self.hp=hpmax
        self.hpmax=hpmax
        
        self.mana=manamax
        self.manamax=manamax
        
        self.stamina=staminamax
        self.staminamax=staminamax
        self.isPlayer=1
        
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
                time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
            except:
                time.sleep(.5)
                #time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
                pass
    
    '''
    def move(self, position):
        self.x=position[0]
        self.y=position[1]
       
    '''
    