import pygame
from NetworkConstants import send_codes, inventory_codes

def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False
def addcommas(value):
    return str(format(int(value), ',d'))
def displayStack(value):
    if value<100000:
        st=addcommas(value)
        color=(0,0,0)
    elif 10000000>value>99999:
        st=addcommas(value)
        st=st[:-3]+"k"
        #str=str(format(int(st), ',d'))+"k"
        color=(255,255,255)
    else:
        st=addcommas(value)
        st=st[:-8]+"m"
        color=(0,255,0)
    
    return st,color
class item:
    def __init__(self):
        self.name=""
        self.description = ""
        self.stackable=False
        self.tradeable=False
        self.value=1
        self.weildable=False
        
        self.options={
            "use": self.use,
            "drop": self.drop,
            "examine": self.examine
            }
    def use(self,args=()):
        print("poop poop used")
    def drop(self,args=()):
        world=args[0]
        clickID=args[1]
        world.client.clearbuffer()
        world.client.writebyte(send_codes["inventory"])
        world.client.writebyte(inventory_codes["drop"])
        world.client.writebyte(clickID)
        world.client.sendmessage()
    def examine(self,args=()):
        world=args[0]
        clickID=args[1]
        st=""
        if self.stackable:
            st+=addcommas(int(world.inventory.inventory[clickID][1]))+" "
        st+=self.description
        world.chat.addchat(st)
        

class coins(item):
    def __init__(self):
        super().__init__()
        self.name="coins"
        self.description = "coins!"
        self.stackable=True
class armor(item):
    def __init__(self): 
        super().__init__()
        self.name="armor"
        self.description = "protective armor"
class sword(item):
    def __init__(self):
        super().__init__()
        self.name="sword"
        self.description = "pointy and sharp"

items = {
    "coins":coins(),
    "armor":armor(),
    "sword":sword()
        }

class groundItem:
    def __init__(self, world, iid, name, x, y, quantity):
        self.iid=iid
        self.x=x
        self.y=y
        self.quantity=quantity
        self.name=name
        self.world=world
        self.w=8
        self.h=8
        #self.box=[self.x,self.y,self.width,self.height]
        #self.image=pygame.Surface((self.width,self.height))
        #self.image.fill((0,0,255))
        #self.rect = self.image.get_rect()
        #self.rect = self.image.get_rect().move(self.x,self.y)
        self.options={
            "take": self.take,
            "examine": self.examine
            }
        
    def take(self,args=()):
        self.world.client.clearbuffer()
        self.world.client.writebyte(send_codes["inventory"])
        self.world.client.writebyte(inventory_codes["pickup"])
        self.world.client.writedouble(self.iid)
        self.world.client.sendmessage()

    def examine(self,args=()):
        #items[self.name].examine([self.world])
        world=args[0]
        #clickID=args[1]
        st=""
        if items[self.name].stackable:#self.stackable:
            st+=addcommas(int(self.quantity))+" "
        st+=items[self.name].description
        world.chat.addchat(st)
    def draw(self):
        xx=self.world.viewport[0]
        yy=self.world.viewport[1]
        box=[self.x+xx,self.y+yy,self.w,self.h]
        
        #check if the person is clicking on it
        if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
            if self.world.mouse_left_down:
                self.take()
            if self.world.mouse_right_down:
                options=list(self.options.keys())
                self.world.rightclick.click(self.world.mouse_x, self.world.mouse_y, options, self)
        
        #self.world.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.world.screen, (0,0,255),
                         (box[0],box[1],
                          box[2],box[3]), 0)
        
        self.world.screen.blit(self.world.fontobject.render(str(self.name), 1, (0,0,0)),(box[0],box[1])) 
        if self.quantity>1:
            q,color=displayStack(self.quantity)
            self.world.screen.blit(self.world.fontobject.render(q, 1, color),(box[0],box[1]-10)) 
#print(list(items["coins"].options.keys()))
#st="coins"
#print(items[st].examine())
