#used for collisions. Anything that has to collide can inherit from this obj

class Obj():
    def __init__(self,world):
        self.world=world
        self.x=0
        self.y=0
        self.color=(0,0,0)
        
        self.xvel=0
        self.yvel=0
        
        self.onground=False
        self.w=16
        self.h=16
        
        self.solid=False
        self.friction=0
        

    def collision(self):
        self.onground=False
        for i in self.world.objects:
            if i.solid:
                if (i.y<self.y+self.h-1 and i.y+i.h>self.y
                    and self.x+self.xvel+self.w-1>i.x
                    and self.x+self.xvel+self.w<i.x+i.w):
                    self.xvel=0
                				
                if (i.y<self.y+self.h-1 and i.y+i.h>self.y
                    and self.x+self.xvel<i.x+i.w
                    and self.x+self.xvel>i.x):
                    self.xvel=0    
                    
                if (self.y+self.yvel+self.h>i.y
                and self.y+self.yvel<i.y+i.h
                and i.x+i.w>self.x
                and i.x<self.x+self.w-1):
                    self.yvel=0
                    if (i.y>self.y):
                        self.onground=True
                        self.y=i.y-self.h
                    else:
                        self.y=i.y+i.h
        
        if self.solid==False:
            if self.onground==False:            
                self.yvel-=-.2
        if self.x>self.world.screen.get_width()-self.width:
            self.x=self.world.screen.get_width()-self.width
            self.xvel=0
        if self.x<0:
            self.x=0
            self.xvel=0
        
        