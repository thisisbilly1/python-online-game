from player import Player
import pygame
from threading import Thread
import time
import sys
sys.path.insert(1, '..//network')
from NetworkConstants import send_codes

class player_self(Player):
    def __init__(self, world, name, pid,  x, y):
        super().__init__(world, name, pid, x, y)
        self.world=world
        self.client=self.world.client
        self.namecolor=(255,0,255)
        self.prev_inputs=self.inputs
        self.prev_attackinputs=self.attackinputs
        
        #update to the server every once in a while 
        self.min_update_max=30
        self.min_update_time=self.min_update_max
        
        self.isPlayer=True
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            self.prev_inputs=self.inputs
            self.prev_attackinputs=self.attackinputs
            self.inputs=[0,0,0,0]
            self.attackinputs=[0,0,0,0,0]
            if self.world.chat.chatting==False:
                for key in self.world.keyspressed:#pygame.event.get():
                    #movement
                    if key == pygame.K_w:
                        self.inputs[2]=1
                    elif key == pygame.K_s:
                        self.inputs[3]=1
                    elif key == pygame.K_a:
                        self.inputs[0]=1
                    elif key == pygame.K_d:
                        self.inputs[1]=1 
                    #attacks
                    if not self.world.combatstatusbars.target==None:
                        for k in range(len(self.world.abilitybar.keybinds)):
                            if key == (self.world.abilitybar.keybinds[k]):
                                self.attackinputs[k]=1 
                        
            #send attack inputs packet
            if (not self.attackinputs==self.prev_attackinputs):
                #if self.attackinputs[0]:
                self.world.client.clearbuffer()
                self.world.client.writebyte(send_codes["attack"])
                self.world.client.writebit(self.world.combatstatusbars.target.isPlayer)
                self.world.client.writedouble(self.world.combatstatusbars.target.pid)
                self.world.client.writebit(self.attackinputs[0])
                self.world.client.writebit(self.attackinputs[1])
                self.world.client.writebit(self.attackinputs[2])
                self.world.client.writebit(self.attackinputs[3])
                self.world.client.writebit(self.attackinputs[4])
                self.world.client.sendmessage()
                #print("a")
                
            #send move input packet
            if (not self.inputs==self.prev_inputs) or self.min_update_time<=0:
                #print("send move")
                self.world.client.clearbuffer()
                self.world.client.writebyte(send_codes["move"])
                self.world.client.writebit(self.inputs[0])
                self.world.client.writebit(self.inputs[1])
                self.world.client.writebit(self.inputs[2])
                self.world.client.writebit(self.inputs[3])
                self.world.client.writedouble(self.x)
                self.world.client.writedouble(self.y)
                self.world.client.sendmessage()
                self.min_update_time=self.min_update_max
                
            self.move()
            self.min_update_time-=1
            #cap fps
            time.sleep(1.0/self.world.FPS - ((time.time() - start_time) % (1.0/self.world.FPS)))
    
           
    
    def startPosition(self,position):
        self.x=position[0]
        self.y=position[1]-10
        

