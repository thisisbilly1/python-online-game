from threading import Thread
import time
import sys
sys.path.insert(1, '..//network')
from NetworkConstants import send_codes
sys.path.insert(1, '../game')
from items import items, item


class Serveritem():
    def __init__(self, server, iid, data, x, y, pid=None):
        #print(iid)
        self.iid=iid
        self.x=x
        self.y=y
        self.name=data[0]
        self.server=server
        self.quantity=data[1]
        #items[self.name].__init__()
        self.stackable=items[self.name].stackable
        
        #print(data)
        self.data=data
        
        #if this variable!=None, then the player with that pid will only see the items until a certain amount of time
        self.pid=pid
        self.create_time=time.time()+30
        self.created_pid=False
        self.created_world=False
        
        self.running=True
        self.start()
    def start(self):
        Thread(target=self.update,args=()).start()
    def update(self):
        while self.running:
            if not self.created_world:
                if not self.pid==None:
                    #self
                    if not self.created_pid:
                        for c in self.server.clients:
                            if not c.player==None:
                                if self.pid==c.pid:
                                    self.create(c)
                                    break
                        self.created_pid=True
                    #world
                    if self.create_time-time.time()<=0:
                        #self.create_all()
                        for c in self.server.clients:
                            if not c.player==None:
                                if not self.pid==c.pid:
                                    self.create(c)
                        self.created_world=True
                        self.pid=None
                else:
                    self.create_all()
                    self.created_world=True
            
            
    def create_all(self):
        for c in self.server.clients:
            self.create(c)
    def create(self,client):
        if not client.player==None:
            client.clearbuffer()
            client.writebyte(send_codes["item_drop"])
            client.writedouble(self.iid)
            client.writestring(self.name)
            client.writedouble(self.x)
            client.writedouble(self.y)
            client.writedouble(self.quantity)
            client.sendmessage()
        
    def delete(self):
        for client in self.server.clients:
            if not client.player==None:
                client.clearbuffer()
                client.writebyte(send_codes["item_pickup"])
                client.writedouble(self.iid)
                client.sendmessage()
        self.running=False