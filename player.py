import time
from threading import Thread
import cv2

class Player:
    def __init__(self, name, pid):
        self.name=name
        self.running=True
        self.width=16
        self.height=16
        self.x=0
        self.y=0
        self.pid=pid

    def start(self):
        #self.update()
        Thread(target=self.update,args=()).start()
        return self
        
    def update(self):
        while self.running:
            time.sleep(1)
            
    def getpid(self):
        return self.pid
    
    def draw(self,scene):
        font=cv2.FONT_HERSHEY_SIMPLEX
        scene = cv2.rectangle(scene, (int(self.x-self.width/2),int(self.y-self.height/2)),
                             (int(self.x+self.width/2),int(self.y+self.height/2)),
                             (0,0,0),cv2.FILLED)
        scene = cv2.putText(scene, str(self.name),(int(self.x),int(self.y-self.width)),font, .5, (255,0,255), 1, cv2.LINE_AA)
        return scene
    def stop(self):
        self.running=False
#name=input("name: ")
#player=Player(name).start()