import time
import random
from threading import Thread
import sys
from item import Serveritem
sys.path.insert(1, '....//network')
from NetworkConstants import send_codes
class npc:
    def __init__(self,server, pid, x, y):
        self.pid=pid
        self.x=x
        self.y=y

        self.server=server
        
        self.name="npc"
        self.hpmax=25
        self.hp=self.hpmax
    
        self.hp_previous=self.hp
        self.x_previous=x
        self.y_previous=y
        
        self.running=True
        
        self.respawntimer=0
        self.respawntime=15
        self.damagedelays=[]#[time,damage,pid]
        self.playerdamages=[]#[name,damage]
        
        self.isPlayer=False
        
        self.droptable=[]
        
        self.target=None
        self.globalcooldown=time.time()
        
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def death(self):
        player=None
        m=0
        for d in self.playerdamages:
            if d[1]>m:
                m=d[1]
                player=d[0]

        #[name, probability, min stack, max stack]
        for i in self.droptable:
            if i[1]>=random.random():
                if i[2]==i[3]:
                    itm=[i[0],i[2]]
                else:
                    itm=[i[0],random.randrange(i[2],i[3])]
                self.server.items.append(Serveritem(self.server,len(self.server.items)+1,itm,self.x,self.y,pid=player))
                
    def attack(self):
        damage=1
        target=self.server.findPlayer(self.target)#self.target
        target.damagedelays.append([time.time()+(45/self.client.server.FPS),damage,self.pid])
        #TODO: add the difference between ranged and melee attacks based on weapons/abilities
        self.client.clearbuffer()
        self.client.writebyte(send_codes["attack"])
        self.client.writebit(target.isPlayer)
        self.client.writedouble(self.target)
        self.client.writedouble(self.pid)
        self.client.writebyte(0)#attack number
        #self.client.sendmessage_distance()
        #self.client.sendmessage()
        self.client.sendmessage_all()
    

        
    def update(self):
        start_time=time.time()
        while self.running:
            try:
                #damaging the npc
                for d in self.damagedelays:
                    if d[0]-time.time()<=0:
                        self.hp-=d[1]
                        self.damagedelays.remove(d)
                        #track damage for player drops
                        newPlayer=True
                        for damages in self.playerdamages:
                            if damages[0]==d[2]:
                                damages[1]+=d[1]
                                newPlayer=False
                        if newPlayer:
                            self.playerdamages.append([d[2],d[1]]) #[name,damage]
                            #attack back, add a target
                            self.target=d[2]
                            
                #death and respawn
                if self.hp<=0:
                    if self.respawntimer==0:
                        self.respawntimer=time.time()
                        self.death()
                        self.target=None
                    else:
                        if time.time()-self.respawntimer>=self.respawntime:
                            self.hp=self.hpmax
                            self.respawntimer=0
                #attacking
                if not self.target==None:
                    if time.time()-self.globalcooldown>=1.3:
                        print(self.target)
                        self.attack()
                        
                #updating
                if (not self.x==self.x_previous or
                not self.y==self.y_previous):
                    for c in self.server.clients:
                        if not c.player==None:
                            c.clearbuffer()
                            c.writebyte(send_codes["npc_move"])
                            c.writedouble(self.pid)
                            c.writedouble(self.x)
                            c.writedouble(self.y)
                            c.sendmessage()
                
                #update status
                if (not self.hp==self.hp_previous):
                    for c in self.server.clients:
                        if not c.player==None:
                            c.clearbuffer()
                            c.writebyte(send_codes["update_stats"])
                            c.writebit(self.isPlayer)
                            c.writedouble(self.pid)
                            c.writedouble(self.hp)
                            c.sendmessage()
                            
                self.hp_previous=self.hp
                self.x_previous=self.x
                self.y_previous=self.y
                
                time.sleep(1.0/self.server.FPS - ((time.time() - start_time) % (1.0/self.server.FPS)))
            except Exception as e:
                print(e)
    #def move(self):
        
    def create(self,client):
        if not client.player==None:
            client.clearbuffer()
            client.writebyte(send_codes["npc_create"])
            client.writedouble(self.pid)
            client.writestring(self.name)
            client.writedouble(self.x)
            client.writedouble(self.y)
            client.writedouble(self.hpmax)
            client.writedouble(self.hp)
            client.sendmessage()
            
            
    def stop(self):
        self.running=False