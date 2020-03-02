# -*- coding: utf-8 -*-
import socket
import struct
import sys
import threading
from player import player

sys.path.insert(1, 'D:/work/python online game/network')
import Network
from NetworkConstants import receive_codes, send_codes

class Client(threading.Thread):
    def __init__(self, connection, address, server, pid):
        threading.Thread.__init__(self)
        
        self.connection = connection
        self.address = address
        self.server = server
        self.connected = True
        
        self.pid=pid
        self.id = -1
        
        self.buffer = Network.Buff()
        self.player = None
        self.name = None
    def getpid(self):
        return self.pid
    def sendmessage(self, buff=None, debuf=False):
        if buff == None:
            buff=self.buffer
        types = ''.join(buff.BufferWriteT)
        length=struct.calcsize("="+types)
        buff.BufferWrite[0]=length #set header length
        
        self.connection.send(struct.pack("="+types, *buff.BufferWrite))
        
    def sendmessage_all(self,sendToSelf=True):
        for c in self.server.clients:
            if not sendToSelf:
                if c == self:
                    continue
            c.sendmessage(self.buffer)
    def sendmessage_other(self,pid):
        for c in self.server.clients:
            if pid==c.getpid():
                c.sendmessage(self.buffer)   
            
    def run(self):
        self.clearbuffer()
        self.writebyte(send_codes["self_join"])
        self.writebyte(self.pid)
        self.sendmessage()
        #get the other players
        for players in self.server.clients:
            if (not players.getpid() == self.pid) and (not players.getpid()==-1):
                players.clearbuffer()
                players.writebyte(send_codes["join"])
                players.writestring(players.name)
                players.writebyte(players.getpid())
                players.sendmessage_other(self.pid)
        #start the player obj
        self.player=player(self.name)
        #print(self.pid)
        while self.connected:
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
                        
            except ConnectionResetError:
                self.disconnect_user()

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
    def case_message_move(self):
        x=self.readdouble()
        y=self.readdouble()
        self.player.move((x,y))
        
        self.clearbuffer()
        self.writebyte(send_codes["move"])
        self.writebyte(self.pid)
        self.writedouble(x)
        self.writedouble(y)
        self.sendmessage_all(False)
        
    def case_message_chat(self):
        text=self.readstring()
        text=self.name+": "+text
        print(text)
        self.clearbuffer()
        self.writebyte(send_codes["chat"])
        self.writestring(text)
        self.sendmessage_all()
    
    def case_message_join(self):
        #self.disconnect_user()
        self.name=self.readstring()
        print(self.name+ " joined")
        self.clearbuffer()
        self.writebyte(send_codes["join"])
        self.writestring(self.name)
        self.writebyte(self.pid)
        self.sendmessage_all(False)
        
    def case_message_ping(self):
        self.clearbuffer()
        self.writebyte(send_codes["ping"])
        self.sendmessage()
    def case_message_disconnect(self):
        self.disconnect_user()
        
        
        
        
        
    def disconnect_user(self):
        #print("Disconnected from ", self.address)
        print(self.name+ " disconnected")
        self.clearbuffer()
        self.writebyte(send_codes["leave"])
        self.writestring(self.name)
        self.writebyte(self.pid)
        self.sendmessage_all(False)
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