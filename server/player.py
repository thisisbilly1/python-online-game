import time
from threading import Thread

import sys
sys.path.insert(1, '..//network')
from NetworkConstants import  send_codes

class player:
    def __init__(self,client, x, y, inventory, stats):
        self.client=client
        self.name=self.client.name
        self.pid=self.client.pid
        self.x=x
        self.y=y
        self.running=True
        self.inventory=[]
        self.inputs=[0,0,0,0] #left,right,up,down
        
        
        
        self.target=None
        
        for i in list(inventory):
            if not i==None:
                self.inventory.append(i.split(":"))
            else:
                self.inventory.append(i)
        
        self.hpmax=stats[0]
        self.hp=stats[1]
        self.manamax=stats[2]
        self.mana=stats[3]
        self.staminamax=stats[4]
        self.stamina=stats[5]
        
        self.hp_previous=self.hp
        self.mana_previous=self.mana
        self.stamina_previous=self.stamina
        
        
        self.num_abilities=5
        self.globalcooldown=0
        self.attackinputs=[0]*self.num_abilities
        self.abilitycooldowns=[0]*self.num_abilities
        self.cooldowns=[2,3,4,5,6]
        self.ability_damage=[1,2,3,4,5]
        self.prev_attackinputs=self.attackinputs
        self.damagedelays=[]
        self.isPlayer=True
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            #attacking
            self.prev_attackinputs=self.attackinputs
            
            self.hp_previous=self.hp
            self.mana_previous=self.mana
            self.stamina_previous=self.stamina
            
            for d in self.damagedelays:
                if d[0]-time.time()<=0:
                    self.hp-=d[1]
                    self.damagedelays.remove(d)
            
            
            #lose target if target hp <0
            if not self.target==None:
                if self.target.hp<=0:
                    self.target=None
            if not self.target==None:
                if time.time()-self.globalcooldown>=1.3:
                    for k in range(self.num_abilities):
                        if (self.attackinputs[k]):
                            if time.time()-self.abilitycooldowns[k]>=self.cooldowns[k]:
                                self.attackinputs[k]=0
                                self.attack(k,damage=self.ability_damage[k])

            

                    
            #TODO: add simulation of movement on the server for clients
            #self.move()
            
            #check if your stats changed at all, update
            if (not self.hp==self.hp_previous or not self.mana==self.mana_previous or not self.stamina==self.stamina_previous):
                self.client.clearbuffer()
                self.client.writebyte(send_codes["update_stats"])
                self.client.writebit(self.isPlayer)
                self.client.writedouble(self.pid)
                self.client.writedouble(self.hp)
                self.client.writedouble(self.mana)
                self.client.writedouble(self.stamina)
                #self.sendmessage_distance()
                self.client.sendmessage_all()
            time.sleep(1.0/self.client.server.FPS - ((time.time() - start_time) % (1.0/self.client.server.FPS)))
            
            #time.sleep(1.0/self.FPS - ((time.time() - start_time) % (1.0/self.FPS)))
    def attack(self,att,damage=1):
        self.target.damagedelays.append([time.time()+(45/self.client.server.FPS),damage,self.pid])
        
        #TODO: add the difference between ranged and melee attacks based on weapons/abilities
        self.client.clearbuffer()
        self.client.writebyte(send_codes["attack"])
        self.client.writebit(self.target.isPlayer)
        self.client.writedouble(self.target.pid)
        self.client.writedouble(self.pid)
        self.client.writebyte(att)#attack number
        #self.client.sendmessage_distance()
        #self.client.sendmessage()
        self.client.sendmessage_all()
    
        self.abilitycooldowns[att]=time.time()
        self.globalcooldown=time.time()
    
    '''
    def move(self):
        if self.inputs[0]==1:
            self.x-=5
        if self.inputs[1]==1:
            self.x+=5
        if self.inputs[2]==1:
            self.y-=5
        if self.inputs[3]==1:
            self.y+=5
    '''
    #def addInv(self, iid):
        