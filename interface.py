import pygame
class Inventory:
    def __init__(self,world):
        self.world=world
        self.inventory=[]
    def update(self):
        pass
    def draw(self):
        pass
        fontobject = pygame.font.Font(None,18)
        self.world.screen.blit(fontobject.render("inv: "+str(self.inventory), 1, (0,0,0)),(5,15))

class Chat():
    def __init__(self,world):
        self.chathistory=[]
        self.world=world
        self.chatting=False
        self.chatstring=[]
    def addchat(self,c):
        if len(self.chathistory)>7:
            self.chathistory.pop()
        self.chathistory.insert(0,c)
    def update(self):
        for key in self.world.keyspress:
            if key == pygame.K_RETURN:
                if self.chatting:
                     self.world.client.sendchat(str.join("",self.chatstring))
                self.chatting = not self.chatting
                self.chatstring=[]
            elif key == pygame.K_BACKSPACE:
                if self.chatting:
                    self.chatstring = self.chatstring[0:-1]
            elif key <= 127:
                    if self.chatting:
                        self.chatstring.append(chr(key))

    def draw(self):
        fontobject = pygame.font.Font(None,18)
        if self.chatting:
            self.world.screen.blit(fontobject.render(str.join("",self.chatstring), 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-15))
        else:
            self.world.screen.blit(fontobject.render("Press [Enter] to chat.", 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-15))
        y=0
        for i in range(len(self.chathistory)):
            y=i*10
            self.world.screen.blit(fontobject.render(str(self.chathistory[i]), 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-25-y))
