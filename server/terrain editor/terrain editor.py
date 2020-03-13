import pygame
from wall import wall
from controller import controller

class world:
    def __init__(self):
        #self.size=(920,680)
        self.displaysize=(980,620)
        self.size=(1000,1000)
        self.blocksize=16
        self.walls=[]
        for x in range(0,self.size[0],self.blocksize):
            self.walls.append([])
            #print("x: "+str(x))
            for y in range(0,self.size[1],self.blocksize):
                #print("y: "+str(x))
                self.walls[len(self.walls)-1].append(None)
        
        
        self.controller=controller(self)
        
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
        
        self.mouse_scroll_down=False
        self.mouse_scroll_up=False
        
        pygame.init()
        pygame.font.init()
        self.fontobject = pygame.font.Font(None,18)
        
        #self.scene=np.ones((self.size[0],self.size[1],3),np.uint8)*255
        self.screen = pygame.display.set_mode(self.displaysize)
        self.clock=pygame.time.Clock()
        self.FPS=200#60
        self.running=True
        
        self.viewport=[0,0]
        self.mouse_drag_pos=(0,0)
        
    def update(self):
        while self.running:
            self.keyspress=[]
            self.draw()
            #reset the mouse vars
            self.mouse_left_up=False
            self.mouse_left_down=False
            self.mouse_right_up=False
            self.mouse_right_down=False
            self.mouse_middle_up=False
            self.mouse_middle_down=False
            
            self.mouse_scroll_down=False
            self.mouse_scroll_up=False
            
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
            if self.mouse_middle and self.mouse_middle_previous==False:
                self.mouse_middle_down=True
            if self.mouse_left==False and self.mouse_left_previous:
                self.mouse_left_up=True
            if self.mouse_right==False and self.mouse_right_previous:
                self.mouse_right_up=True
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
                #scroll wheel
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==5:
                        self.mouse_scroll_down=True
                    if event.button==4:
                        self.mouse_scroll_up=True
                
            self.controller.update()
                        
            
            #dragging around
            if ord("g") in self.keyspress or self.mouse_middle_down:
                self.mouse_drag_pos=(self.mouse_x,self.mouse_y)
            if ord("g") in self.keyspressed or self.mouse_middle:
                self.viewport[0]+=self.mouse_x-self.mouse_drag_pos[0]
                self.viewport[1]+=self.mouse_y-self.mouse_drag_pos[1]
                self.mouse_drag_pos=(self.mouse_x,self.mouse_y)
            #print(self.xx,self.yy)
    def draw(self):
        self.screen.fill((255,255,255))
        self.controller.draw()
        #wallsrendered=0
        for x in range(max(int(-self.viewport[0]/16),0),min(len(self.walls),int((self.displaysize[0]-self.viewport[0]+16)/16))):
            #for y in range(len(x)):
            for y in range(max(int(-self.viewport[1]/16),0),min(len(self.walls[x]),int((self.displaysize[1]-self.viewport[1]+16)/16))):
                if not self.walls[x][y]==None:
                    self.walls[x][y].draw(editing=True)
                    #wallsrendered+=1
        #print(wallsrendered) 

        pygame.draw.line(self.screen, (0,0,0), (0+self.viewport[0],0+self.viewport[1]),(0+self.viewport[0],self.size[1]+self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (0+self.viewport[0],0+self.viewport[1]),(self.size[0]+self.viewport[0],0+self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (0+self.viewport[0],self.size[1]+self.viewport[1]),(self.size[0]+self.viewport[0],self.size[1]+self.viewport[1]),1)
        pygame.draw.line(self.screen, (0,0,0), (self.size[0]+self.viewport[0],0+self.viewport[1]),(self.size[0]+self.viewport[0],self.size[1]+self.viewport[1]),1)
        pygame.display.update()
        self.clock.tick(self.FPS)
    def stop(self):
        self.running=False
        pygame.quit() 
w=world()
w.update()