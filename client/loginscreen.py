# import inputbox
# answer = inputbox.ask(screen, "Your name")

import pygame, pygame.font, pygame.event, pygame.draw
from pygame.locals import *
import re
from threading import Thread

class LoginScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode((320,240))
        self.loginclicked=False
        self.login=True
        
        #username and password box
        self.UsernameBoxSelected=True
        self.usernamebox=[(self.screen.get_width() / 2) - 100,(self.screen.get_height() / 2) - 60,200,20]
        self.passwordbox=[(self.screen.get_width() / 2) - 100,(self.screen.get_height() / 2) - 10,200,20]
        self.usernamecolor=(50,50,50)
        self.passwordcolor=(0,0,0)
        
        #login and register buttons
        self.loginbox=[(self.screen.get_width() / 2) - 100,(self.screen.get_height() / 2) + 25, 75,50]
        self.registerbox=[(self.screen.get_width() / 2) +25,(self.screen.get_height() / 2) + 25, 75,50]
        self.logincolor=(0,0,0)
        self.registercolor=(0,0,0)
        
        pygame.font.init()
        self.name_string = []
        self.password_string = []
        
        self.clock=pygame.time.Clock()
        self.FPS=20
        
        self.running=True
        
        self.servermessage="Server is online!"
        self.servermessagecolor=(0,255,0)
    def start(self):
        #Thread(target=self.display,args=()).start()
        self.display()
        return self
    def checkvalid(self):
        if len(self.name_string)<=0:
            self.servermessage="Please enter Username"
            self.servermessagecolor=(255,0,0)
            return False
        if len(self.password_string)<=0:
            self.servermessage="Please enter Password"
            self.servermessagecolor=(255,0,0)
            return False
        return True
        
    def display(self):
        while self.running:
            self.screen.fill((0,0,0))
            self.clock.tick(self.FPS)
            #select the boxes
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running=False
                    pygame.quit() 
                    return
                
                
                mouse = pygame.mouse.get_pos() 
                
                if self.checkclick(self.loginbox,mouse):
                    self.logincolor=(50,50,50)
                    if event.type == MOUSEBUTTONDOWN:
                        if self.checkvalid():
                            self.login=True
                            self.loginclicked=True
                            return
                    
                else:
                    self.logincolor=(0,0,0)
                if self.checkclick(self.registerbox,mouse):
                    self.registercolor=(50,50,50)
                    if event.type == MOUSEBUTTONDOWN:
                        if self.checkvalid():
                            self.login=False
                            self.loginclicked=True
                            return
                else:
                    self.registercolor=(0,0,0)
                        
                if event.type == MOUSEBUTTONDOWN:
                    if self.checkclick(self.usernamebox,mouse):
                        self.UsernameBoxSelected=True
                        
                    
                    if self.checkclick(self.passwordbox,mouse):
                        self.UsernameBoxSelected=False


                elif event.type == KEYDOWN:
                    inkey = event.key
                    if inkey == K_BACKSPACE:
                        if self.UsernameBoxSelected:
                            self.name_string = self.name_string[0:-1]
                        else:
                            self.password_string = self.password_string[0:-1]
                    elif inkey == K_MINUS:
                        if self.UsernameBoxSelected:
                            self.name_string.append("_")
                        else:
                            self.password_string.append("_")
                    elif inkey == K_TAB:
                        self.UsernameBoxSelected = not self.UsernameBoxSelected
                    elif inkey == K_ESCAPE:
                        self.running=False
                        pygame.quit() 
                        return
                    elif inkey == K_RETURN:#log in
                        if self.UsernameBoxSelected:
                            self.UsernameBoxSelected=False
                        else:
                            if self.checkvalid():
                                self.login=True
                                self.loginclicked=True
                                return
                    elif inkey <= 127:
                        if self.UsernameBoxSelected:
                            self.name_string.append(chr(inkey))
                        else:
                            self.password_string.append(chr(inkey))
                            
            if self.UsernameBoxSelected:
                self.usernamecolor=(50,50,50)
                self.passwordcolor=(0,0,0)
            else:
                self.usernamecolor=(0,0,0)
                self.passwordcolor=(50,50,50)
            fontobject = pygame.font.Font(None,18)
            self.screen.blit(fontobject.render(self.servermessage, 1, self.servermessagecolor),(5,self.screen.get_height()-15)) 
                
            self.display_box("Username: " + str.join("",self.name_string),self.usernamebox,self.usernamecolor)
            self.display_box("Password: " + str.join("",["*"]*len(self.password_string)),self.passwordbox,self.passwordcolor)
            
            self.display_box("Log in",self.loginbox,self.logincolor)
            self.display_box("Register",self.registerbox,self.registercolor)
            
            pygame.display.flip()
            
    def checkclick(self,box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False
    def display_box(self, message, box, color):
        fontobject = pygame.font.Font(None,18)
        pygame.draw.rect(self.screen, color,
                         (box[0],box[1],
                          box[2],box[3]), 0)
        pygame.draw.rect(self.screen, (255,255,255),
                         (box[0]-2,box[1]-2,
                          box[2]+4,box[3]+4), 1)
        self.screen.blit(fontobject.render(message, 1, (255,255,255)),(box[0],box[1]+int(box[3]/2)-5)) 
        #pygame.display.flip()

    def stop(self):
        self.running=False
        pygame.quit() 
        return


#l=LoginScreen().start()
