# -*- coding: utf-8 -*-
import socket
import sys
from threading import Thread, Lock
from serverclient import Client
from terrain import terrain
import time



sys.path.insert(1, '..//network')
from NetworkConstants import receive_codes, send_codes

sys.path.insert(2, '/sqlite')
import sqlite3

sys.path.insert(3, './npcs')
from cow import cow


class Server:
    def __init__(self, max_clients, ip, port):
        self.FPS=200
        self.max_clients = max_clients
        self.clients = []#players
        self.items = []#items on the ground
        self.npcs = [cow(self, 0,300,100).start()]
        self.terrain=terrain(self)
        self.sendsize=(300,300)#sending box size for player updating things
        
        self.port = port
        self.ip = ip
        self.socket = None
        self.running = False
        
        self.db = sqlite3.connect('./sqlite/playerdata.db',check_same_thread=False)
        self.dbc= self.db.cursor()
        #self.db.row_factory = dict_factory
        
        with open('help.txt', 'r') as myfile:
            self.input_help=myfile.read()
    def __del__(self):
        self.db.commit()
        self.db.close()
        
    def findPlayer(self,pid):
        for p in self.clients:
            if p.pid==pid:
                return pid
        print("unable to find player with pid" +str(pid))
        return None
    
    def sql(self,sql,args=()):
        try:
            if sql=="COMMIT":
                self.db.commit()
            else:
                res = self.dbc.execute(sql,args)
                if "SELECT" in sql:
                    result=res.fetchall()
                    if len(result)==1:
                        return result[0]
                    elif len(result)==0:
                        return None
                    else:
                        return result
                    
                elif "INSERT INTO" in sql:
                    self.db.commit()
        except Exception as e:
            print(e)
    def inputs(self):
        while self.running:
            x=input("Server>")
            if "/help" in x:
                print(self.input_help)
            if "/say" in x:
                text=x.replace("/say ", "")
                for players in self.clients:
                    players.clearbuffer()
                    players.writebyte(send_codes["chat"])
                    players.writestring("SERVER: "+text)
                    players.sendmessage()
            if "/kickall" in x:
                for players in self.clients:
                    players.disconnect_user()
                print("kicked all clients")
            if "/clients" in x:
                for players in self.clients:
                    print(str(players.pid)+". "+str(players.name) + ": " + str(players.address))
            if "/save" in x:
                self.db.commit()
                print("committed to database")
            if "/terrain" in x:
                self.terrain.load()
                for players in self.clients:
                    self.terrain.send(players)
    def start(self):
        #create new socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.bind((self.ip,self.port))
            self.running = True
        except Exception as e:
            print(e)
            print("failed to bind socket")
            sys.exit()
            
        #main loop
        self.input_thread = Thread(target = self.inputs)
        self.input_thread.setDaemon(True)
        self.input_thread.start()
        print("ready")
        while self.running:
            time.sleep(1/1000)
            self.socket.listen(self.max_clients)
            
            connection, address = self.socket.accept()
            print('Connected by', address)
            client = Client(connection, address, self, len(self.clients)+1)
            client.start()
            self.clients.append(client)
                
                
s = Server(32, "127.0.0.1", 1337)
s.start()