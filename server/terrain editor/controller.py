import pygame
import math
from wall import wall
import pickle

def roundup(x):
    return int(math.ceil(x / 16.0)) * 16

def clamp(x,minn,maxx):
    if x<minn:
        x=minn
    if x>maxx:
        x=maxx
    return x

class controller:
    def __init__(self,world):
        self.world=world
        self.selected=0
        
        #self.size=1
        self.xsize=1
        self.ysize=1
        
        self.load()
        
    def load(self):
        #try loading
        try:
            walls=[]
            with open('terrain.pkl','rb') as f:
                saveWalls=pickle.load(f)
            #print(saveWalls)
            for x in range(len(saveWalls)):
                #walls.append([])
                for y in range(len(saveWalls[x])):
                    if saveWalls[x][y]=="01":
                        self.world.walls[x][y]=wall(self.world,x*16,y*16,16,16)  
                    else:
                        self.world.walls[x][y]=None  
                        
            print("loaded")
        except Exception as e:
            print(e)
            
    def save(self):
        #convert the walls into non objects
            saveWalls=[]
            for x in range(0,self.world.size[0],self.world.blocksize):
                saveWalls.append([])
                for y in range(0,self.world.size[1],self.world.blocksize):
                    if not self.world.walls[int(x/16)][int(y/16)]==None:
                        saveWalls[len(saveWalls)-1].append("01")#(y.__class__.__name__)
                    else:
                        saveWalls[len(saveWalls)-1].append("00")
            print(saveWalls)
            with open('terrain.pkl','wb') as f:
                pickle.dump(saveWalls, f)
            print("saved")
    
    def update(self):
        worldx=self.world.xx
        worldy=self.world.yy
        
        #saving/loading
        if ord("s") in self.world.keyspress:
            self.save()
        if ord("l") in self.world.keyspress:
            self.load()
            
        #scaling
        if self.world.mouse_scroll_up:
            #print(self.world.keyspress)
            if not ord("x") in self.world.keyspressed:
                self.ysize=min(5,self.ysize+1)
            if not ord("y") in self.world.keyspressed:
                self.xsize=min(5,self.xsize+1)
            #self.size=min(5,self.size+1)
        if self.world.mouse_scroll_down:
            if not ord("x") in self.world.keyspressed:
                self.ysize=max(1,self.ysize-1)
            if not ord("y") in self.world.keyspressed:
                self.xsize=max(1,self.xsize-1)
        if self.world.mouse_left:
            xx=roundup(self.world.mouse_x-16-worldx)
            yy=roundup(self.world.mouse_y-16-worldy)
            
            for xt in range(-self.xsize+1,self.xsize):
                x=int((xx+xt*16)/16)#clamp(int((xx+xt*16)/16),0,int(self.world.size[0]/16))
                if 0<x<int(self.world.size[0]/16):
                    for yt in range(-self.ysize+1, self.ysize):
                        y=int((yy+yt*16)/16)#clamp(int((yy+yt*16)/16),0,int(self.world.size[1]/16))
                        if 0<y<int(self.world.size[1]/16):
                            if self.world.walls[x][y]==None:
                                self.world.walls[x][y]=wall(self.world,x*16,y*16,16,16)
        
        if self.world.mouse_right:
            
            xx=roundup(self.world.mouse_x-16-worldx)
            yy=roundup(self.world.mouse_y-16-worldy)
            
            x=int(xx/16)
            y=int(yy/16)
            
            for xt in range(-self.xsize+1,self.xsize):
                x=int((xx+xt*16)/16)#clamp(int((xx+xt*16)/16),0,int(self.world.size[0]/16))
                if 0<x<int(self.world.size[0]/16):
                    for yt in range(-self.ysize+1, self.ysize):
                        y=int((yy+yt*16)/16)#clamp(int((yy+yt*16)/16),0,int(self.world.size[1]/16))
                        if 0<y<int(self.world.size[1]/16):
                            if not self.world.walls[x][y]==None:
                                del self.world.walls[x][y]
                                self.world.walls[x].insert(y,None)
            '''
            if not self.world.walls[x][y]==None:
                del self.world.walls[x][y]
                self.world.walls[x].insert(y,None)
                #print("deleted")
            '''
    def draw(self):
        worldx=self.world.xx
        worldy=self.world.yy
        xx=roundup(self.world.mouse_x-20)+worldx%16
        yy=roundup(self.world.mouse_y-20)+worldy%16
        
        pygame.draw.rect(self.world.screen, (100,100,100),(xx,yy,16,16), 0)
        
        for x in range(-self.xsize,self.xsize):
            pygame.draw.line(self.world.screen, (0,0,0), (xx+(x+1)*16,yy-(16*(self.ysize-1))),(xx+(x+1)*16,yy+16*self.ysize),1)
            for y in range(-self.ysize,self.ysize):
                pygame.draw.line(self.world.screen, (0,0,0), (xx-(16*(self.xsize-1)),yy+(y+1)*16),(xx+16*self.xsize,yy+(y+1)*16),1)
        '''
        for x in range(3):
            pygame.draw.line(self.world.screen, (0,0,0), (xx+x*16,yy),(xx+x*16,yy+64),1)
            for y in range(3):
                pygame.draw.line(self.world.screen, (0,0,0), (xx,yy+y*16),(xx+64,yy+y*16),1)
        '''