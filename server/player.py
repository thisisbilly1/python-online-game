import time
from threading import Thread

class player:
    def __init__(self, name, x, y, inventory):
        self.FPS=60
        self.name=name
        self.x=x
        self.y=y
        self.running=True
        self.inventory=[]
        self.inputs=[0,0,0,0] #left,right,up,down
        
        for i in list(inventory):
            if not i==None:
                self.inventory.append(i.split(":"))
            else:
                self.inventory.append(i)
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        start_time=time.time()
        while self.running:
            #self.move()
            time.sleep(1.0/self.FPS - ((time.time() - start_time) % (1.0/self.FPS)))
    
    
    '''
    def move(self):
        if self.inputs[0]==1:
            self.x-=5
        if self.inputs[1]==1:
            self.x+=5
        if self.inputs[2]==1:
            self.y-=5
        if self.inputs[3]==1:
            self.y+=5
    '''
    #def addInv(self, iid):
        