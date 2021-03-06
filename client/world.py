import pygame
import time
from threading import Thread
from player_self import player_self
from player_other import player_other
from client import Client
from loginscreen import LoginScreen

from interface import Inventory, Chat, rightClick
from combatinterfaces import statusbars, abilitybar

import sys
sys.path.insert(1, '..//network')
from NetworkConstants import login_status
sys.path.insert(1, '..//game')
from items import groundItem
from wall import wall




class world:
    def __init__(self):
        self.displaysize=(300,300)#(920,680)#
        self.worldsize=(0,0)
        #view port
        self.viewport=[0,0]#[int(self.player.x+self.displaysize[0]/2),int(self.player.y+self.displaysize[1]/2)]
        self.viewboxdim=[50,50] #w, h
        self.FPS=200#600#60
        #objects
        self.walls=[]
        self.npcs=[]
        self.attacks=[]
        self.otherplayers=[]
        self.grounditems=[]
        
        #interfaces
        self.inventory=Inventory(self)
        self.chat=Chat(self)
        self.rightclick=rightClick(self)
        self.combatstatusbars=statusbars(self)
        self.abilitybar=abilitybar(self)
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
        
        self.mouse_middle=False
        self.mouse_middle_up=False
        self.mouse_middle_down=False
        
        self.mouse_left_previous=False
        self.mouse_right_previous=False
        self.mouse_middle_previous=False
        
        #network
        self.client=Client("127.0.0.1",1337, self).start()
        #wait for terrain to load from server
        
        
        
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
        self.screen = pygame.display.set_mode(self.displaysize, pygame.HWSURFACE)
        #self.surface = pygame.Surface(self.displaysize, pygame.HWSURFACE | pygame.SRCALPHA)
        self.surface = pygame.Surface((150,150), pygame.HWSURFACE | pygame.SRCALPHA)
        self.clock=pygame.time.Clock()

        self.running=True
        

        
        #players
        self.player=player_self(self, name, self.client.pid, 100, 10).start()
        self.client.updatePlayerStart()
        


    def start(self):
        if self.loggedin==True:
            self.update()
        return self
    
    def update(self):
        while self.running:
            self.keyspress=[]#reset the tapped keys
            
            self.draw()
            
            #reset the mouse vars
            self.mouse_left_up=False
            self.mouse_left_down=False
            self.mouse_right_up=False
            self.mouse_right_down=False
            self.mouse_middle_up=False
            self.mouse_middle_down=False
            
            self.mouse_left_previous=self.mouse_left
            self.mouse_right_previous=self.mouse_right
            self.mouse_middle_previous=self.mouse_middle
            
            #mouse inputs
            mouse = pygame.mouse.get_pos() 
            self.mouse_x=mouse[0]
            self.mouse_y=mouse[1]
            clicks = pygame.mouse.get_pressed()
            self.mouse_left=clicks[0]
            self.mouse_middle=clicks[1]
            self.mouse_right=clicks[2]
            
            if self.mouse_left and self.mouse_left_previous==False:
                self.mouse_left_down=True
            if self.mouse_right and self.mouse_right_previous==False:
                self.mouse_right_down=True
            if self.mouse_left==False and self.mouse_left_previous:
                self.mouse_left_up=True
            if self.mouse_right==False and self.mouse_right_previous:
                self.mouse_right_up=True
            if self.mouse_middle and self.mouse_middle_previous==False:
                self.mouse_middle_down=True
            if self.mouse_middle==False and self.mouse_middle_previous:
                self.mouse_middle_up=True
                
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

                        
            #self.player.update()
            self.chat.update()
            self.inventory.update()
            
            #update the view port
            
            centerx=-(self.player.x-self.displaysize[0]/2)
            centery=-(self.player.y-self.displaysize[1]/2)
            if self.viewport[0]<centerx-self.viewboxdim[0]:
                self.viewport[0]=centerx-self.viewboxdim[0]
            if self.viewport[0]>centerx+self.viewboxdim[0]:
                self.viewport[0]=centerx+self.viewboxdim[0]
            if self.viewport[1]<centery-self.viewboxdim[1]:
                self.viewport[1]=centery-self.viewboxdim[1]
            if self.viewport[1]>centery+self.viewboxdim[1]:
                self.viewport[1]=centery+self.viewboxdim[1]
            #self.viewport[0]=-(self.player.x-self.displaysize[0]/2)
            #self.viewport[1]=-(self.player.y-self.displaysize[1]/2)
            
            '''
            if self.chat.chatting==False:
                if ord("g") in self.keyspress or self.mouse_middle_down:
                        self.mouse_drag_pos=(self.mouse_x,self.mouse_y)
                if ord("g") in self.keyspressed or self.mouse_middle:
                    self.viewport[0]+=self.mouse_x-self.mouse_drag_pos[0]
                    self.viewport[1]+=self.mouse_y-self.mouse_drag_pos[1]
                    self.mouse_drag_pos=(self.mouse_x,self.mouse_y)
            '''
            #print(self.viewport)
            
            
           
    def draw(self):
        self.screen.fill((255,255,255))
        self.surface.fill((0,0,0,0))
        
        #draw bounding box of world
        pygame.draw.line(self.screen, (0,0,0), (self.viewport[0],self.viewport[1]),(self.viewport[0],self.worldsize[1]+self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (self.viewport[0],self.viewport[1]),(self.worldsize[0]+self.viewport[0],self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (self.viewport[0],self.worldsize[1]+self.viewport[1]),(self.worldsize[0]+self.viewport[0],self.worldsize[1]+self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (self.worldsize[0]+self.viewport[0],self.viewport[1]),(self.worldsize[0]+self.viewport[0],self.worldsize[1]+self.viewport[1]),1)
        
        self.player.draw()
        
        for c in self.npcs:
             if (self.player.x-self.displaysize[0]<c.x<self.player.x+self.displaysize[0]
                and self.player.y-self.displaysize[1]<c.y<self.player.y+self.displaysize[1]):
                 if c.hp>0:
                     c.draw()
                

        for c in self.otherplayers:
             if (self.player.x-self.displaysize[0]<c.x<self.player.x+self.displaysize[0]
                and self.player.y-self.displaysize[1]<c.y<self.player.y+self.displaysize[1]):
                 c.draw()
                 
        
        for i in self.grounditems:
            if (self.player.x-self.displaysize[0]<i.x<self.player.x+self.displaysize[0]
                and self.player.y-self.displaysize[1]<i.y<self.player.y+self.displaysize[1]):
                    i.draw()
                   
        
        for x in range(max(int(-self.viewport[0]/16),0),min(len(self.walls),int((self.displaysize[0]-self.viewport[0]+16)/16))):
            #for y in range(len(x)):
            for y in range(max(int(-self.viewport[1]/16),0),min(len(self.walls[x]),int((self.displaysize[1]-self.viewport[1]+16)/16))):
                if not self.walls[x][y]==None:
                    self.walls[x][y].draw()
        
        for c in self.attacks:
             if (self.player.x-self.displaysize[0]<c.x<self.player.x+self.displaysize[0]
                and self.player.y-self.displaysize[1]<c.y<self.player.y+self.displaysize[1]):
                 c.draw()
        #interfaces
        self.inventory.draw()
        self.chat.draw()
        self.combatstatusbars.draw()
        self.abilitybar.draw()
        
        self.rightclick.draw()
        
        self.screen.blit(self.fontobject.render(str(int(self.clock.get_fps())), 1, (0,0,0)),(self.displaysize[0]-25,5)) 

        
        self.screen.blit(self.surface, (0,0))
        
        
        
        pygame.display.update()
        self.clock.tick(self.FPS)
        
    def stop(self):
        self.running=False
        self.player.stop()
        self.client.stop()
        for c in self.otherplayers:
            c.stop()
        for c in self.npcs:
            c.stop()
        pygame.quit() 
         
    def findPlayer(self, pid):
        for c in self.otherplayers:
            if c.getpid()==pid:
                return c
        print("cant find player with pid "+str(pid))
        return None
    
    def findNPC(self, pid):
        for c in self.npcs:
            if c.pid==pid:
                return c
        print("cant find NPC with pid "+str(pid))
        return None
    def findItem(self, iid):
        for i in self.grounditems:
            if i.getiid()==iid:
                return i
        print("cant find item with iid "+str(iid))
        return None

world().start()
