import pygame
import sys
sys.path.insert(1, 'D:/work/python online game/network')
from NetworkConstants import inventory_codes
sys.path.insert(1, 'D:\work\python online game\game')
from items import items, displayStack

def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False
class rightClick:
    def __init__(self,world):
        self.world=world
        self.x=0
        self.y=0
        self.display=False
        self.options=[]
        self.optionwidth=0
        self.box=[]
        self.optionboxes=[]
        self.obj=None #what object is being right clicked
        self.boxheight=15
        self.boxwidth=12
    def click(self, x, y, options, obj):
        self.obj=obj
        self.x=x
        self.y=y
        self.options=options
        self.display=True
        self.optionwidth=len(max(self.options)+str(self.obj.name))*12
        self.box=[self.x,self.y,self.optionwidth,len(self.options)*self.boxheight]
        self.optionboxes=[]
        for i in range(len(self.options)):
            self.optionboxes.append([self.x,self.y+i*self.boxheight,self.optionwidth,self.boxheight])
    def draw(self):
        if self.display:
            
            #check if mouse is outside the options box
            if not checkmousebox([self.box[0]-15,self.box[1]-15,self.box[2]+15,self.box[3]+15],(self.world.mouse_x,self.world.mouse_y)):
                self.display=False

            #draw
            color=(200,200,200)
            pygame.draw.rect(self.world.screen, color,
                         (self.box[0]+1,self.box[1]+1,
                          self.box[2]-1,self.box[3]-1), 0)
            pygame.draw.rect(self.world.screen, (0,0,0),
                         (self.box[0],self.box[1],
                          self.box[2],self.box[3]), 1)
            for i in range(len(self.options)):
                box=self.optionboxes[i]#[self.x,self.y+i*12,self.optionwidth,12]#self.optionboxes[i]#
                if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
                    pygame.draw.rect(self.world.screen, (150,150,150),
                         (box[0],box[1],
                          box[2],box[3]), 0)
                    if self.world.mouse_left:
                        self.display=False
                        #print(self.options[i])------------------------------
                        self.obj.options[self.options[i]]((self.world,self.world.inventory.invclickID))
                            
                self.world.screen.blit(self.world.fontobject.render(str(self.options[i])+" "+str(self.obj.name), 1, (0,0,0)),(box[0],box[1]))
            
class Inventory:
    def __init__(self,world):
        self.world=world
        self.inventory=[]
        self.x=0
        self.y=0
        self.width=3
        self.height=3
        self.invslotwidth=32
        self.invslotheight=32
        
        #inventory dragging
        self.inventoryClicked=False
        self.invclickID=None
        self.hoverID=None
    def update(self):
        pass
    def draw(self):
        self.hoverID=None
        for i in range(len(self.inventory)):
            #find the x and y of inv slots
            xx = divmod(i,self.width)[1]*self.invslotwidth
            yy = divmod(i,self.width)[0]*self.invslotheight
            #bounding box
            box=[xx,yy,self.invslotwidth,self.invslotheight]
            #mouse interactions
            if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
                color=(200,200,200)
                self.hoverID=i
                if self.world.mouse_left_down and self.world.rightclick.display==False:
                    if not self.inventory[i]==None:
                        if self.inventoryClicked==False:
                            self.invclickID=i
                            self.inventoryClicked=True
                if self.world.mouse_right_down:
                    if not self.inventory[i]==None:
                        options=list(items[str(self.inventory[i][0])].options.keys())
                        self.world.rightclick.click(self.world.mouse_x, self.world.mouse_y, options,items[str(self.inventory[i][0])])#str(self.inventory[i])
                        self.invclickID=i
            else:
                color=(150,150,150)
            #draw
            pygame.draw.rect(self.world.screen, color,
                         (box[0]+1,box[1]+1,
                          box[2]-1,box[3]-1), 0)
            pygame.draw.rect(self.world.screen, (0,0,0),
                         (box[0],box[1],
                          box[2],box[3]), 1)
            if not self.inventory[i]==None:
                self.world.screen.blit(self.world.fontobject.render(str(self.inventory[i][0]), 1, (0,0,0)),(box[0]+3,box[1]))
                if items[self.inventory[i][0]].stackable:
                    stackquantity,stackcolor=displayStack(int(self.inventory[i][1]))
                    self.world.screen.blit(self.world.fontobject.render(stackquantity, 1, stackcolor),(box[0]+3,box[1]+int(box[3]/1.5)))
                   
            
        if self.inventoryClicked:
            if self.world.mouse_left:
                box=[int(self.world.mouse_x-self.invslotwidth/2),int(self.world.mouse_y-self.invslotheight/2),self.invslotwidth,self.invslotheight]
                pygame.draw.rect(self.world.screen, color,
                             (box[0]+1,box[1]+1,
                              box[2]-1,box[3]-1), 0)
                pygame.draw.rect(self.world.screen, (0,0,0),
                             (box[0],box[1],
                              box[2],box[3]), 1)
                self.world.screen.blit(self.world.fontobject.render(str(self.inventory[self.invclickID][0]), 1, (0,0,0)),(box[0],box[1]))
                if items[self.inventory[self.invclickID][0]].stackable:
                    stackquantity,stackcolor=displayStack(int(self.inventory[self.invclickID][1]))
                    self.world.screen.blit(self.world.fontobject.render(stackquantity, 1, stackcolor),(box[0]+3,box[1]+int(box[3]/1.5)))
                
            else:
                #swap the inventory slots
                if not self.hoverID==None and not self.hoverID==self.invclickID:
                    self.world.client.updateInventory(inventory_codes["swap"],[self.hoverID, self.invclickID])
                self.invclickID=None
                self.inventoryClicked=False
        
        

class Chat():
    def __init__(self,world):
        self.chathistory=[]
        self.world=world
        self.chatting=False
        self.chatstring=[]
        #self.chatbox=[0,self.world.screen.get_height()-80]
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
        if self.chatting:
            self.world.screen.blit(self.world.fontobject.render(str.join("",self.chatstring), 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-15))
        else:
            self.world.screen.blit(self.world.fontobject.render("Press [Enter] to chat.", 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-15))
        y=0
        for i in range(len(self.chathistory)):
            y=i*10
            self.world.screen.blit(self.world.fontobject.render(str(self.chathistory[i]), 
                                                     1, (0,0,0)),(5,self.world.screen.get_height()-25-y))
