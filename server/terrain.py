import pickle
import sys
sys.path.insert(1, 'D:/work/python online game/network')
from NetworkConstants import send_codes

class terrain:
    def __init__(self,server):
        self.walls=""
        self.wallsdim=(0,0)
        self.load()
        self.server=server
        
    def send(self,client):
        client.clearbuffer()
        client.writebyte(send_codes["terrain"])
        client.writeint(self.wallsdim[0])#x dimension
        client.writeint(self.wallsdim[1])#y dimension
        client.writestring(self.walls)
        client.sendmessage()
    def load(self):
        #try loading
        try:
            wallList=[]
            with open('./terrain editor/terrain.pkl','rb') as f:
                wallList=pickle.load(f)
            self.wallsdim=(len(wallList),len(wallList[0]))
            print(self.wallsdim)
            #print(self.wallsdim)
            #convert into a string
            for x in range(len(wallList)):
                for y in range(len(wallList[x])):
                    self.walls+=wallList[x][y]
            
            #print(self.walls)
            print("loaded terrain successfully")
        except Exception as e:
                print(e)
#t=terrain(None)