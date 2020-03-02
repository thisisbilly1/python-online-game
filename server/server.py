# -*- coding: utf-8 -*-
import socket
import sys
from threading import Thread, Lock
from serverclient import Client
import time

sys.path.insert(1, 'D:/work/network base/network')
from NetworkConstants import receive_codes, send_codes


class Server:
    def __init__(self, max_clients, ip, port):
        
        self.max_clients = max_clients
        self.clients = []
        self.port = port
        self.ip = ip
        self.socket = None
        self.running = False
        
    def inputs(self):
        while self.running:
            x=input("Server>")
            
            if "/help" in x:
                print("help coming soon LOL")
            
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
    def start(self):
        #create new socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.bind((self.ip,self.port))
            self.running = True
        except self.socket.error as err:
            print("Failed to bind socket")
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