import pygame
import time
from threading import Thread
from player_self import player_self
from player_other import player_other
from client import Client
from loginscreen import LoginScreen
import sys
from interface import Inventory, Chat, rightClick
sys.path.insert(1, 'D:/work/python online game/network')
from NetworkConstants import login_status
sys.path.insert(1, 'D:/work/python online game/game')
from items import groundItem



class world:
    def __init__(self):
        self.otherplayers=[]
        self.grounditems=[]
        self.inventory=Inventory(self)
        self.chat=Chat(self)
        self.rightclick=rightClick(self)
        
        #inputs
        self.keyspressed=[] #for key HOLD DOWN
        self.keyspress=[] #for key DOWN 
        self.mouse_x=0
        self.mouse_y=0
        self.mouse_left=False
        self.mouse_left_up=False
        self.mouse_left_down=False
        self.mouse_right=False
        self.mouse_right_up=False
        self.mouse_right_down=False
        self.mouse_left_previous=False
        self.mouse_right_previous=False
        
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
        pygame.font.init()
        self.fontobject = pygame.font.Font(None,18)
        self.size=(300,300)
        #self.scene=np.ones((self.size[0],self.size[1],3),np.uint8)*255
        self.screen = pygame.display.set_mode(self.size)
        self.clock=pygame.time.Clock()
        self.FPS=200#60
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
            
            #reset the mouse vars
            self.mouse_left_up=False
            self.mouse_left_down=False
            self.mouse_right_up=False
            self.mouse_right_down=False

            self.mouse_left_previous=self.mouse_left
            self.mouse_right_previous=self.mouse_right
            #mouse inputs
            mouse = pygame.mouse.get_pos() 
            self.mouse_x=mouse[0]
            self.mouse_y=mouse[1]
            clicks = pygame.mouse.get_pressed()
            self.mouse_left=clicks[0]
            self.mouse_right=clicks[2]
            
            if self.mouse_left and self.mouse_left_previous==False:
                self.mouse_left_down=True
            if self.mouse_right and self.mouse_right_previous==False:
                self.mouse_right_down=True
            if self.mouse_left==False and self.mouse_left_previous:
                self.mouse_left_up=True
            if self.mouse_right==False and self.mouse_right_previous:
                self.mouse_right_up=True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                #keyboard
                elif event.type == pygame.KEYDOWN:
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
        
        for i in self.grounditems:
            i.draw()
         
        
        self.inventory.draw()
        self.chat.draw()
        self.rightclick.draw()
        
        pygame.display.update()
        self.clock.tick(self.FPS)
        
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
    
    def findItem(self, iid):
        for i in self.grounditems:
            if i.getiid()==iid:
                return i
        print("cant find item with iid "+str(iid))
        return None

world().start()