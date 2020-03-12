import pygame

def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False


class wall:
    def __init__(self, world, x, y, w, h):
        self.world=world
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.name="wall"
        #self.image=pygame.Surface((self.w,self.h))
        #self.image.fill((0,0,0))
        #self.rect = self.image.get_rect()
    
    def draw(self):
        xx=self.world.xx
        yy=self.world.yy
        box=[self.x+xx,self.y+yy,self.w,self.h]
        '''
        if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
            color=(100,100,100)
        else:
            color=(0,0,0)
        '''
        pygame.draw.rect(self.world.screen, (0,0,0),
                         (box[0]+1,box[1]+1,
                          box[2]-1,box[3]-1), 0)
        #self.rect = self.image.get_rect().move(int(self.x),int(self.y))
        #self.world.screen.blit(self.image, self.rect)