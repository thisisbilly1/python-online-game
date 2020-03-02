class player:
    def __init__(self, name):
        self.name=name
        self.x=0
        self.y=0
        self.running=True
    def move(self,position):
        self.x=position[0]
        self.y=position[1]