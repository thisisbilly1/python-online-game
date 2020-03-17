#used for collisions. Anything that has to collide can inherit from this obj

class Obj():
    def __init__(self,world,x,y):
        self.world=world
        self.x=x
        self.y=y
        
        self.color=(0,0,0)
        
        self.xvel=0
        self.yvel=0
        
        self.maxvel=6
        
        self.onground=False
        self.w=16
        self.h=16
        
        self.solid=False
        self.friction=0
        
        self.gravity=.1
        
    def collision(self):
        #print(self.onground,self.yvel)
        
        self.onground=False
        if self.solid==False:           
            self.yvel+=self.gravity
        checkrange=[int(2+abs(self.xvel*1)+self.w/16),int(2+abs(self.yvel*1)+self.h/16)]#5x5 16 blocks
        for x in range(max(int(self.x/16)-checkrange[0],0),min(len(self.world.walls),int((self.x)/16)+checkrange[0])):
            for y in range(max(int(self.y/16)-checkrange[1],0),min(len(self.world.walls[x]),int((self.y)/16)+checkrange[1])):
                if not self.world.walls[x][y]==None:
                    i=self.world.walls[x][y]
                    if i.solid:
                        if (i.y<self.y+self.h-1 and i.y+i.h>self.y
                            and self.x+self.xvel+self.w>i.x
                            and self.x+self.xvel+self.w<i.x+i.w):
                            self.xvel=min(0,self.xvel)
                        				
                        if (i.y<self.y+self.h-1 and i.y+i.h>self.y
                            and self.x+self.xvel<i.x+i.w
                            and self.x+self.xvel>i.x):
                            self.xvel=max(0,self.xvel)   
                        
                        #y collision
                        if (self.y+self.h+self.yvel>i.y):
                            if (self.x<i.x+i.w and self.x+self.w>i.x
                            or self.x+self.w>i.x and self.x<i.x+i.w):
                                #print(self.yvel)
                                #if (i.y>self.y):
                                self.yvel=min(0,self.yvel)
                                self.onground=True
                                    #self.y=i.y-self.h
                                    #self.y=i.y-self.h
                        '''
                        if (self.y+self.yvel+self.h>i.y
                        and self.y+self.yvel<i.y+i.h
                        and i.x+i.w>self.x
                        and i.x<self.x+self.w-1):
                            self.yvel=0
                            if (i.y>self.y):
                                self.onground=True
                                #self.y=i.y-self.h
                        '''
        if self.y>self.world.worldsize[1]-self.h:
            #self.y=self.world.worldsize[1]-self.h
            self.onground=True
    
        if not 0<self.x+self.xvel<self.world.worldsize[0]+self.w:
            self.xvel=0

        

               
        #self.xvel=min(max(self.xvel,-self.maxvel),self.maxvel)
        self.yvel=min(max(self.yvel,-self.maxvel),self.maxvel)
        self.x+=self.xvel
        self.y+=self.yvel
