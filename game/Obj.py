#used for collisions. Anything that has to collide can inherit from this obj

class Obj():
    def __init__(self,world,x,y,w,h):
        self.world=world
        self.x=x
        self.y=y
        
        self.color=(0,0,0)
        
        self.xvel=0
        self.yvel=0
        
        self.maxvel=3
        
        self.onground=False
        self.w=w
        self.h=h
        
        self.solid=False
        self.friction=0
        
        self.gravity=.1
        
    def collision(self):
        self.onground=False

        checkrange=[int(2+abs(self.xvel*1)),int(2+abs(self.yvel*1))]#5x5 16 blocks
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
                        if (self.y+self.yvel+self.h>i.y
                        and self.y+self.yvel<i.y+i.h
                        and i.x+i.w>self.x
                        and i.x<self.x+self.w-1):
                            self.yvel=0
                            if (i.y>self.y):
                                self.onground=True
                                #self.y=i.y-self.h
                            #else:
                                #self.y=i.y+i.h
        
        if self.y>self.world.worldsize[1]-self.height:
            self.y=self.world.worldsize[1]-self.height
            self.onground=True
            #self.
            #self.yvel=0
       
        if self.solid==False:
            if self.onground==False:            
                self.yvel+=self.gravity
        if not 0<self.x+self.xvel<self.world.worldsize[0]+self.width:
            #self.x=self.world.worldsize[0]*16-self.width
            self.xvel=0

        '''
        if self.x<0:
            #self.x=0
            self.xvel=0
        '''

        #if self.y<0:
            #self.y=0
            #self.yvel=0
        self.x+=min(self.xvel,self.maxvel)
        self.y+=min(self.yvel,self.maxvel)