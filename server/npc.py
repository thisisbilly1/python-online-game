import time
from threading import Thread
import sys
sys.path.insert(1, '..//network')
from NetworkConstants import send_codes
class npc:
    def __init__(self,server, name, pid, x, y):
        self.pid=pid
        self.x=x
        self.y=y

        self.server=server
        
        self.name="npc"
        self.hpmax=1000
        self.hp=self.hpmax
    
        self.hp_previous=self.hp
        self.x_previous=x
        self.y_previous=y
        
        self.running=True
        
        self.respawntimer=0
        self.damagedelays=[]
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            try:
                for d in self.damagedelays:
                    if d[0]-time.time()<=0:
                        self.hp-=d[1]
                        self.damagedelays.remove(d)
                if self.hp<=0:
                    if self.respawntimer==0:
                        self.respawntimer=time.time()
                    else:
                        if time.time()-self.respawntimer>=10:
                            self.hp=self.hpmax
                            self.respawntimer=0
                    
                #self.move() 
                if (not self.x==self.x_previous or
                not self.y==self.y_previous or
                not self.hp==self.hp_previous):
                    for c in self.server.clients:
                        if not c.player==None:
                            c.clearbuffer()
                            c.writebyte(send_codes["npc_move"])
                            c.writedouble(self.pid)
                            c.writedouble(self.x)
                            c.writedouble(self.y)
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