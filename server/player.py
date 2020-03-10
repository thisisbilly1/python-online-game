class player:
    def __init__(self, name, x, y, inventory):
        self.name=name
        self.x=x
        self.y=y
        self.running=True
        self.inventory=[]
        for i in list(inventory):
            if not i==None:
                self.inventory.append(i.split(":"))
            else:
                self.inventory.append(i)
        
    def move(self,position):
        self.x=position[0]
        self.y=position[1]
    
    #def addInv(self, iid):
        