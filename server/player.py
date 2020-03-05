class player:
    def __init__(self, name, x, y, inventory):
        self.name=name
        self.x=x
        self.y=y
        self.running=True
        self.inventory=inventory
    def move(self,position):
        self.x=position[0]
        self.y=position[1]