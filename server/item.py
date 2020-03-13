import sys
sys.path.insert(1, '..//network')
from NetworkConstants import send_codes
sys.path.insert(1, '..//game')
from items import items, item
class Serveritem():
    def __init__(self, server, iid, data, x, y):
        #print(iid)
        self.iid=iid
        self.x=x
        self.y=y
        self.name=data[0]
        self.server=server
        self.quantity=data[1]
        #items[self.name].__init__()
        self.stackable=items[self.name].stackable
        #create item for all clients
        self.create_all()
        #print(data)
        self.data=data
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