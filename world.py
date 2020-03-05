import pygame
import time
from threading import Thread
from player_self import player_self
from player_other import player_other
from client import Client
from loginscreen import LoginScreen
import sys
from interface import Inventory, Chat
sys.path.insert(1, 'D:/work/python online game/network')
from NetworkConstants import login_status

class world:
    def __init__(self):
        self.otherplayers=[]
        self.inventory=Inventory(self)
        self.chat=Chat(self)
        #keyboard inputs
        self.keyspressed=[] #for key HOLD DOWN
        self.keyspress=[] #for key DOWN 
        
        #network
        self.client=Client("127.0.0.1",1337, self).start()
        
        #log in screen
        self.loggedin=False
        self.loginscreen=LoginScreen()
        while self.loggedin==False:
            self.loginscreen.start()
            
            #if the window is exitted, stop the connection to the server
            if self.loginscreen.running==False:
                self.client.stop()
                return
                sys.exit()
            #get the name, pass, and which button was pressed
            name=str.join("",self.loginscreen.name_string)
            password=str.join("",self.loginscreen.password_string)
            login=self.loginscreen.login
        
            #try to log in
            t=time.time()
            self.client.log(name, password, login)
            while self.client.loginStatus==login_status["wait"]:
                if time.time()-t>10:
                    time.sleep(1)
                    print("connection to server timed out")
                    return
            print(self.client.loginStatus)
            if self.client.loginStatus==login_status["success"]:
                self.loggedin=True
                self.loginscreen.stop()
            else:
                self.client.loginStatus=login_status["wait"]
                

                
                
            
            
        #scene
        pygame.init()
        self.size=(300,300)
        #self.scene=np.ones((self.size[0],self.size[1],3),np.uint8)*255
        self.screen = pygame.display.set_mode((720, 480))
        self.clock=pygame.time.Clock()
        self.FPS=60
        self.running=True
        
        #players
        self.player=player_self(self, name, self.client.pid, 0, 0)
        self.client.updatePlayerStart()
         
    def start(self):
        if self.loggedin==True:
            self.update()
        return self
    
    def update(self):
        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    #print("a")
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                        return
                    else:
                        self.keyspressed.append(event.key)
                        self.keyspress.append(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key in self.keyspressed:
                        self.keyspressed.remove(event.key)
                        
            self.player.update()
            self.chat.update()
            self.inventory.update()
    
            self.keyspress=[]#reset the tapped keys
            
    def draw(self):
        self.screen.fill((255,255,255))
        
        self.player.draw()
        for c in self.otherplayers:
            c.draw()
        
        self.inventory.draw()
        self.chat.draw()
        
        pygame.display.update()
        
        
    def stop(self):
        self.running=False
        self.player.stop()
        self.client.stop()
        for c in self.otherplayers:
            c.stop()
        pygame.quit() 
         
    def findPlayer(self, pid):
        for c in self.otherplayers:
            if c.getpid()==pid:
                return c
        print("cant find player with pid "+str(pid))
        return None

world().start()