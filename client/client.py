# -*- coding: utf-8 -*-
import socket
import time
import sys
import struct
from threading import Thread
from player_other import player_other

sys.path.insert(1, 'D:/work/python online game/network')
import Network
from NetworkConstants import receive_codes, send_codes, login_status

sys.path.insert(1, 'D:/work/python online game/game')
from items import groundItem
from terrain_codes import terrain_codes

class Client:
    def __init__(self, ip, port, world):
        self.socket=None
        self.ip=ip
        self.port=port
        self.running = False
        
        self.buffer = Network.Buff()
        self.pid=-1
        self.username=None
        
        self.world=world
        
        self.playerstartx=0
        self.playerstarty=0
        

        self.loginStatus=login_status["wait"]
        self.loginmessage=""
    def sendmessage(self, buff=None, debuf=False):
        if buff == None:
            buff=self.buffer
        types = ''.join(buff.BufferWriteT)
        length=struct.calcsize("="+types)
        buff.BufferWrite[0]=length #set header length
        
        self.socket.send(struct.pack("="+types, *buff.BufferWrite))
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.ip,self.port))
        except Exception as e:
            print(e)
            sys.exit()
        self.running = True
        print("connected")
        Thread(target=self.update,args=()).start()
        
        #send the request for the terrain
        self.clearbuffer()
        self.writebyte(send_codes["terrain"])
        self.sendmessage()
        print("loading terrain from server...")
        
        return self
    def log(self, username, password, login):
        #login : False=Register   True=Log in
        self.username=username
 
        if login:
            self.clearbuffer()
            self.writebyte(send_codes["login"])
            self.writestring(self.username)
            self.writestring(password)
            self.sendmessage()
        else:
            self.clearbuffer()
            self.writebyte(send_codes["register"])
            self.writestring(self.username)
            self.writestring(password)
            self.sendmessage()
    def update(self):
        while self.running:
            #time.sleep(1/1000)    
            try:
                self.buffer.Buffer = self.socket.recv(1024)
                #self.buffer.Buffer0 = self.buffer.Buffer
                while(len(self.buffer.Buffer))>0:
                    packet_size = len(self.buffer.Buffer)
                    
                    msg_size = self.readushort() #read the header
                    
                    #if we have not gotten enough data, keep receiving
                    while(len(self.buffer.Buffer)+2<msg_size):
                        self.buffer.Buffer+=self.socket.recv(1024)
                        packet_size=len(self.buffer.Buffer)+2
                    
                    self.handlepacket()
                    
                    #pop the remaining data in the packet
                    while((packet_size-len(self.buffer.Buffer))<msg_size):
                        self.readbyte()
                        
            except ConnectionResetError:
                self.disconnect_user()
   
    def sendping(self):
        self.clearbuffer()
        self.writebyte(send_codes["ping"])
        self.sendmessage()
        
    def sendchat(self, chat):
        self.clearbuffer()
        self.writebyte(send_codes["chat"])
        self.writestring(chat)
        self.sendmessage()
        
    
        
    def handlepacket(self):
        event_id=self.readbyte()
        if event_id == receive_codes["login"]:#login
            self.case_message_login()
        if event_id == receive_codes["register"]:#register
            self.case_message_register()
        if event_id == receive_codes["ping"]:#ping from server
            self.case_message_ping()
        if event_id == receive_codes["chat"]:#chatting
            self.case_message_chat()
        if event_id == receive_codes["join"]:#other player joins
            self.case_message_join()
        if event_id == receive_codes["leave"]:#other player leaves
            self.case_message_leave()
        if event_id == receive_codes["move"]:#other player moves
            self.case_message_move()
        if event_id == receive_codes["inventory"]:#self inventory is updated
            self.case_message_inventory()
        if event_id == receive_codes["item_drop"]:#dropped item
            self.case_message_item_drop()
        if event_id == receive_codes["item_pickup"]:#dropped item
            self.case_message_item_pickup()
        if event_id == receive_codes["terrain"]:#load terrain
            self.case_message_terrain()
            
    def case_message_terrain(self):
        w=self.readint()
        h=self.readint()
        self.world.walls=[]
        self.world.worldsize=(w*16,h*16)
        print(self.world.worldsize)
        wallstring=self.readstring()
        count=0
        for x in range(w):
            self.world.walls.append([])
            for y in range(h):
                if not terrain_codes[wallstring[count:count+2]]==None:
                    obj=terrain_codes[wallstring[count:count+2]](self.world,x*16,y*16,16,16)
                else:
                    obj=None
                self.world.walls[len(self.world.walls)-1].append(obj)
                count+=2
        #print(wallstring)
        #print(count)
        #print(self.world.walls)
        print("loaded terrain")
    def case_message_item_pickup(self):
        iid=self.readdouble()
        for i in self.world.grounditems:
            if i.iid==iid:
                self.world.grounditems.remove(i)
    def case_message_item_drop(self):
        iid=self.readdouble()
        name=self.readstring()
        x=self.readdouble()
        y=self.readdouble()
        quantity=self.readdouble()
        item=groundItem(self.world,iid,name,x,y,quantity)
        self.world.grounditems.append(item)
    def case_message_inventory(self):
        #inventory
        invslots=self.readbyte()
        self.world.inventory.inventory=[]
        for i in range(invslots):
            item=self.readstring()
            if item=="None":
                self.world.inventory.inventory.append(None)
            else:
                quantity=self.readdouble()
                self.world.inventory.inventory.append([item,quantity])
        #print(self.world.inventory.inventory)
    def case_message_move(self):
        pid=self.readbyte()
        c=self.world.findPlayer(pid)
        if not c == None:
            c.inputs=[self.readbit(),self.readbit(),self.readbit(),self.readbit()]
            c.x=self.readdouble()
            c.y=self.readdouble()

    def case_message_register(self):
        self.loginmessage=self.readstring()
        print(self.loginmessage)
        self.world.loginscreen.servermessage=self.loginmessage#set the login message
        self.loginStatus=login_status["fail"]
        success=self.readbit()
        if success:
            self.world.loginscreen.servermessagecolor=(0,255,0)#set the message color
        else:
            self.world.loginscreen.servermessagecolor=(255,0,0)#set the message color
            
        
    def case_message_login(self):
        login=self.readbit()
        if login:
            self.pid = self.readbyte()
            self.playerstartx=self.readdouble()
            self.playerstarty=self.readdouble()
            print("sucessfully logged in")
            self.loginStatus=login_status["success"]
        else:
            self.loginmessage=self.readstring()
            print(self.loginmessage)
            self.world.loginscreen.servermessage=self.loginmessage#set the login message
            self.world.loginscreen.servermessagecolor=(255,0,0)#set the message color
            self.loginStatus=login_status["fail"]
        
        #send the first ping
        self.sendping()
        
    def case_message_leave(self):
        print(self.readstring() + " disconnected")
        pid=self.readbyte()
        self.world.otherplayers.remove(self.world.findPlayer(pid))
        
    def case_message_join(self):
        name = self.readstring()
        pid = self.readbyte()
        x = self.readdouble()
        y = self.readdouble()
        #print(str((x,y)))
        p=player_other(self.world, name, pid, x, y).start()
        self.world.otherplayers.append(p)
        print(name + " joined")
    def case_message_ping(self):
        #print("pinged")
        self.sendping()

    
    def case_message_chat(self):
        chat=self.readstring()
        self.world.chat.addchat(chat)
        print(chat)
    

    def stop(self):
        self.running=False
        self.disconnect_user()
    
    def disconnect_user(self):
        self.clearbuffer()
        self.writebyte(send_codes["leave"])
        self.sendmessage()
        self.running=False
        self.socket.close()
    def updatePlayerStart(self):
        self.world.player.startPosition((self.playerstartx,self.playerstarty))
    def updateInventory(self,t,sendList):
        self.clearbuffer()
        self.writebyte(send_codes["inventory"])
        self.writebyte(t)
        for i in sendList:
            self.writebyte(i)
        self.sendmessage()
        
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