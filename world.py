import cv2
import numpy as np
import time
from threading import Thread
from player_self import player_self
from player_other import player_other
from client import Client

class world:
    def __init__(self):
        name=input("name: ")
        
        #network
        self.client=Client("127.0.0.1",1337, name, self).start()
        
        #scene
        self.size=(300,300)
        self.scene=np.ones((self.size[0],self.size[1],3),np.uint8)*255
        self.FPS=60
        self.running=True

        #players
        self.player=player_self(name, self, self.client).start()
        self.otherplayers=[]
        
    def start(self):
        #Thread(target=self.update,args=()).start()
        
        self.input_thread = Thread(target = self.inputs)
        self.input_thread.setDaemon(True)
        self.input_thread.start()
        
        self.update()
        
        return self
    def update(self):
        while self.running:
            now = time.time()
            
            xdir=0
            ydir=0
            self.draw()
            
            k = cv2.waitKey(1) & 0xFF
            if k == ord('w'):
                ydir=-5
            elif k == ord('s'):
                ydir=5
            if k == ord('a'):
                xdir=-5
            elif k == ord('d'):
                xdir=5
            
            if k == ord("q"):
                self.running=False
                cv2.destroyAllWindows()
                self.player.stop()
                self.client.stop()
                for c in self.otherplayers:
                    c.stop()
            self.player.move(xdir,ydir)

            
            #cap the fps
            timeDiff = time.time() - now
            if (timeDiff < 1.0/(self.FPS)): 
                time.sleep( 1.0/(self.FPS) - timeDiff )
                
                
    def draw(self):
        self.scene=np.ones((self.size[0],self.size[1],3),np.uint8)*255
            
        self.scene=self.player.draw(self.scene)
        for c in self.otherplayers:
            self.scene=c.draw(self.scene)
            
        cv2.imshow("scene", self.scene)

    def inputs(self):
            while self.running:
                x=input(self.player.name+">")
                self.client.sendchat(x)
                
    def findPlayer(self, pid):
        for c in self.otherplayers:
            if c.getpid()==pid:
                return c
        print("cant find player with pid "+str(pid))
        return None

world().start()