# -*- coding: utf-8 -*-
import socket
import struct
import sys
import threading
from player import player
from item import Serveritem

sys.path.insert(1, 'D:/work/python online game/network')
import Network
from NetworkConstants import receive_codes, send_codes, inventory_codes

class Client(threading.Thread):
    def __init__(self, connection, address, server, pid):
        threading.Thread.__init__(self)
        
        self.connection = connection
        self.address = address
        self.server = server
        self.connected = True
        
        self.pid=pid
        self.id = -1 #used for database
        
        self.buffer = Network.Buff()
        self.player = None
        self.name = None
        
        self.ping=0
    def getpid(self):
        return self.pid
    def sendmessage_distance(self):
        for c in self.server.clients:
            if not c == self:
                if not c.player==None:
                    if (self.player.x-self.server.sendsize[0]<c.player.x<self.player.x+self.server.sendsize[0]
                        and self.player.y-self.server.sendsize[1]<c.player.y<self.player.y+self.server.sendsize[1]):
                        c.sendmessage(self.buffer)
                    
    def sendmessage(self, buff=None, debuf=False):
        if buff == None:
            buff=self.buffer
        types = ''.join(buff.BufferWriteT)
        length=struct.calcsize("="+types)
        buff.BufferWrite[0]=length #set header length
        
        self.connection.send(struct.pack("="+types, *buff.BufferWrite))
        
    def sendmessage_all(self,sendToSelf=True):
        for c in self.server.clients:
            if not c.player==None:
                if sendToSelf:
                    c.sendmessage(self.buffer)
                else:
                    if not c == self:
                        c.sendmessage(self.buffer)  
    def sendmessage_other(self,pid):
        for c in self.server.clients:
            if not c.player==None:
                if pid==c.pid:
                    c.sendmessage(self.buffer)   
                
    def run(self):
        #print(self.pid)
        #send the terrain

        
        while self.connected:
            if self.ping>1000:
                self.running=False
                self.disconnect_user()
                return
            try:
                self.buffer.Buffer = self.connection.recv(1024)
                #self.buffer.Buffer0 = self.buffer.Buffer
                
                while(len(self.buffer.Buffer))>0:
                    packet_size = len(self.buffer.Buffer)
                    
                    msg_size = self.readushort() #read the header
                    
                    #if we have not gotten enough data, keep receiving
                    while(len(self.buffer.Buffer)+2<msg_size):
                        self.buffer.Buffer+=self.connection.recv(1024)
                        packet_size=len(self.buffer.Buffer)+2
                    self.handlepacket()
                    
                    #pop the remaining data in the packet
                    while((packet_size-len(self.buffer.Buffer))<msg_size):
                        self.readbyte()
                        
            except Exception as e:#ConnectionResetError:
                #print(e)
                #self.connected=False
                #self.disconnect_user()
                self.ping+=1

    def handlepacket(self):
        event_id=self.readbyte()
        
        if event_id == receive_codes["ping"]:
            self.case_message_ping()
        if event_id == receive_codes["leave"]:
            self.case_message_disconnect()
        if event_id == receive_codes["join"]:
            self.case_message_join()
        if event_id == receive_codes["chat"]:
            self.case_message_chat()
        if event_id == receive_codes["move"]:
            self.case_message_move()
        if event_id == receive_codes["login"]:
            self.case_message_login()
        if event_id == receive_codes["register"]:
            self.case_message_register()
        if event_id == receive_codes["inventory"]:
            #request to update inventory
            self.case_message_inventory()
        if event_id == receive_codes["terrain"]:
            self.case_message_send_terrain()
    
    def case_message_send_terrain(self):
        self.server.terrain.send(self)
        
    def case_message_inventory(self):
        #print("1")
        t=self.readbyte()
        if t==inventory_codes["swap"]:#swapping items
            clickID=self.readbyte()
            hoverID=self.readbyte()
            self.player.inventory[clickID], self.player.inventory[hoverID] = self.player.inventory[hoverID], self.player.inventory[clickID]
        elif t==inventory_codes["drop"]:#drop item
            clickID=self.readbyte()
            i=Serveritem(self.server,len(self.server.items)+1,self.player.inventory[clickID],self.player.x,self.player.y)
            self.server.items.append(i)
            self.player.inventory[clickID]=None
        elif t==inventory_codes["pickup"]:
            #add check for player distance to item
            iid=self.readdouble()
            itm=None
            for i in self.server.items:
                    if i.iid==iid:
                       itm=i 
            if not itm==None:
                emptyinvslot=-1
                #check for stackable
                for i in range(len(self.player.inventory)): 
                    if not self.player.inventory[i]==None:
                        if (self.player.inventory[i][0]==itm.name and itm.stackable==True):
                            newValue=int(self.player.inventory[i][1])+int(itm.quantity)
                            self.player.inventory[i][1]=newValue
                            emptyinvslot=i
                            #print("stacked")
                            break
                #check for open spot if not stackable
                if emptyinvslot==-1:
                    for i in range(len(self.player.inventory)):
                        if self.player.inventory[i]==None:
                            self.player.inventory[i]=itm.data#str(itm.name)+":"+str(itm.quantity)
                            emptyinvslot=i
                            #print("new item")
                            break
                    
                if not emptyinvslot==-1:
                    itm.delete()
                    if self in self.server.clients:
                        self.server.items.remove(itm)
                else:
                    self.clearbuffer()
                    self.writebyte(send_codes["chat"])
                    self.writestring("Inventory full")
                    self.sendmessage()
            else:
                print("no item found...")
                       
                            
        self.send_inventory()
    def send_inventory(self):
        #print(self.player.inventory)
        self.clearbuffer()
        self.writebyte(send_codes["inventory"])
        self.writebyte(len(self.player.inventory))#number of inv slots
        for i in self.player.inventory:#write all of them
            #print(i)
            if not str(i)=="None":
                self.writestring(str(i[0]))
                self.writedouble(float(i[1]))
            else:
                self.writestring(str(i))
        self.sendmessage()
        
    def case_message_register(self):
        username=self.readstring()
        password=self.readstring()
        result = self.server.sql("SELECT * FROM Players WHERE username=?",(username,))
        st=""
        success=True
        if result == None:
            self.server.sql("INSERT INTO Players(Username, Password) VALUES(?,?)",(username,password))
            
            result = self.server.sql("SELECT * FROM Players WHERE username=?",(username,))
            print(result)
            self.server.sql("INSERT INTO Inventory(PlayerID) VALUES(?)",(result[0]))
            
            st="Succesfully registered account!"
            success=True
            print(username+" registered")
        else:
            st="Name already taken."
            success=False
        self.clearbuffer()
        self.writebyte(send_codes["register"])
        self.writestring(st)
        self.writebit(success)
        self.sendmessage()
    def case_message_login(self):
        username=self.readstring()
        password=self.readstring()
        login=True
        login_msg=""
        #check username+pass 
        result = self.server.sql("SELECT * FROM Players WHERE username=?",(username,))
        self.id=result[0]
        invresult = self.server.sql("SELECT * FROM Inventory WHERE PlayerID=?",(self.id,))
        #print(result)
        #print(invresult)
        if result == None:
            login=False
            login_msg="Invalid username or password"
        if login:
            pwd=result[2]#password
            if not password==pwd:
                login=False
                login_msg="Invalid username or password"
        #check if they are already logged in
        for c in self.server.clients:
            if c.name==username:
                login=False
                login_msg="you are already logged in"
        
        x=0
        y=0
        #log in or send message to client
        self.clearbuffer()
        self.writebyte(send_codes["login"])
        self.writebit(login)
        if login:
            x=result[3]#x
            y=result[4]#y

            self.writebyte(self.pid)
            self.writedouble(x)
            self.writedouble(y)
            print(username+" logged in")
            self.name=username
        else:
            self.writestring(login_msg)
        self.sendmessage()
        
        #send location to other players
        if login:
            #create player and send inventory
            self.player=player(self.name,x,y,invresult[2:]).start()
            self.send_inventory()
            
            #send join command to everyone else
            self.clearbuffer()
            self.writebyte(send_codes["join"])
            self.writestring(self.name)
            self.writebyte(self.pid)
            self.writedouble(x)
            self.writedouble(y)
            self.sendmessage_all(False)
            
            #get the other players
            for players in self.server.clients:
                if (not players.getpid() == self.pid) and (not players.player==None):
                    self.clearbuffer()
                    self.writebyte(send_codes["join"])
                    self.writestring(players.name)
                    self.writebyte(players.getpid())
                    self.writedouble(players.player.x)
                    self.writedouble(players.player.y)
                    self.sendmessage()
            #get all the items
            for i in self.server.items:
                i.create(self)
                    
    def case_message_move(self):
        self.player.inputs=[self.readbit(),self.readbit(),self.readbit(),self.readbit()]
		
        self.player.x=self.readdouble()
        self.player.y=self.readdouble()

        self.clearbuffer()
        self.writebyte(send_codes["move"])
        self.writebyte(self.pid)
        self.writebit(self.player.inputs[0])
        self.writebit(self.player.inputs[1])
        self.writebit(self.player.inputs[2])
        self.writebit(self.player.inputs[3])
        self.writedouble(self.player.x)
        self.writedouble(self.player.y)
        
        #self.sendmessage_all(False)
        self.sendmessage_distance()
        
    def case_message_chat(self):
        text=self.readstring()
        text=self.name+": "+text
        print(text)
        self.clearbuffer()
        self.writebyte(send_codes["chat"])
        self.writestring(text)
        self.sendmessage_all()
    
    def case_message_ping(self):
        self.clearbuffer()
        self.writebyte(send_codes["ping"])
        self.sendmessage()
    def case_message_disconnect(self):
        self.disconnect_user()
        
        
        
        
        
    def disconnect_user(self):
        #print("Disconnected from ", self.address)
        print(self.name+ " disconnected")
        
        #save into db
        if not self.player==None:
            self.server.sql("UPDATE Players SET x=?, y=? WHERE username=?", 
                            (self.player.x, self.player.y, self.name))
            
            #save the player's inventory
            invsqlcommand="UPDATE Inventory SET "
            for i in range(len(self.player.inventory)):
                if not i == len(self.player.inventory)-1:
                    invsqlcommand+="item"+str(i)+"=?, "
                else:
                    invsqlcommand+="item"+str(i)+"=? "
            invsqlcommand+="WHERE PlayerID=?"
            #print(invsqlcommand)
            sqlvalues=[]
            for a in self.player.inventory:
                if not a==None:
                    sqlvalues.append(a[0]+":"+str(a[1])) 
                else:
                    sqlvalues.append(a) 
            #sqlvalues=[a[0]+":"+str(a[1]) for a in self.player.inventory]#self.player.inventory
            sqlvalues.append(self.id)
            self.server.sql(invsqlcommand,tuple(sqlvalues))#(self.id,)
            
            #commit to database
            self.server.sql("COMMIT")
        
            self.clearbuffer()
            self.writebyte(send_codes["leave"])
            self.writestring(self.name)
            self.writebyte(self.pid)
            self.sendmessage_all(False)

            self.player.running=False
            
        self.connected = False  
        if self in self.server.clients:
            self.server.clients.remove(self)
        
        
        
        
        
        
        
        
    def clearbuffer(self):
        self.buffer.clearbuffer()
    def writebit(self,b):
        self.buffer.writebit(b)
    def writebyte(self,b):
        self.buffer.writebyte(b)
    def writestring(self,b):
        self.buffer.writestring(b)
    def writeint(self,b):
        self.buffer.writeint(b)
    def writedouble(self,b):
        self.buffer.writedouble(b)
    def writefloat(self,b):
        self.buffer.writefloat(b)
    def writeshort(self,b):
        self.buffer.writeshort(b)
    def writeushort(self,b):
        self.buffer.writeushort(b)
    def readstring(self):
        return self.buffer.readstring()
    def readbyte(self):
        return self.buffer.readbyte()
    def readbit(self):
        return self.buffer.readbit()
    def readint(self):
        return self.buffer.readint()
    def readdouble(self):
        return self.buffer.readdouble()
    def readfloat(self):
        return self.buffer.readfloat()
    def readshort(self):
        return self.buffer.readshort()
    def readushort(self):
        return self.buffer.readushort()