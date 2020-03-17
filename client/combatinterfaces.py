import pygame
import time

def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False

class abilitybar:
    def __init__(self,world):
        self.world=world
        self.num_abilities=5
        self.abilitycooldowns=[0]*self.num_abilities
        self.cooldowns=[2,3,4,5,6]
        self.GCD=0
        
        self.x=0
        self.y=100
        self.abilitysize=20
        
        self.keybinds=[ord("1"),ord("2"),ord("3"),ord("4"),ord("5")]
        self.abilitydescriptions=[("Poop", "deal 1 damage"),
                                  ("Poop2", "deal 2 damage"),
                                  ("Poop3", "deal 3 damage"),
                                  ("Poop4", "deal 4 damage"),
                                  ("Poop5", "deal 5 damage")]
    def triggerCD(self,x):
        self.abilitycooldowns[x]=time.time()+self.cooldowns[x]
    def triggerGCD(self):
        self.GCD=time.time()+1.3
        
    def draw(self):
        mouse=(self.world.mouse_x,self.world.mouse_y)
        for x in range(self.num_abilities):
            xx=self.x+x*self.abilitysize
            yy=self.y
            box=[xx,yy,self.abilitysize,self.abilitysize]
            
            pygame.draw.rect(self.world.screen, (150,150,150),
                         (box[0]+1,box[1]+1,
                          box[2]-1,box[3]-1), 0)
            pygame.draw.rect(self.world.screen, (0,0,0),
                         (box[0],box[1],
                          box[2],box[3]), 1)
            if self.GCD-time.time()>0 or self.abilitycooldowns[x]-time.time()>0:
                if self.abilitycooldowns[x]-time.time()>0:
                    progress=(1-(self.abilitycooldowns[x]-time.time())/self.cooldowns[x])
                    #print(progress)
                else:
                    progress=(1-(self.GCD-time.time())/1.3)
                points=[]
                #if progress<1/8:
                points = [(xx+self.abilitysize/2,yy+self.abilitysize/2),(xx+self.abilitysize/2,yy),
                          (xx+self.abilitysize/2+min(self.abilitysize/2,(8)*progress*self.abilitysize/2),yy)]
                if progress>1/8:
                    points.append((xx+self.abilitysize,yy+min(self.abilitysize,max((8*(progress-1/8))*self.abilitysize/2,0))))
                if progress>3/8:
                    points.append((xx+self.abilitysize-min(self.abilitysize,max((8*(progress-3/8))*self.abilitysize/2,0)),yy+self.abilitysize))
                if progress>5/8:
                    points.append((xx,yy+self.abilitysize-min(self.abilitysize,max((8*(progress-5/8))*self.abilitysize/2,0))))
                if progress>7/8:
                    points.append((xx+min(self.abilitysize/2,max((8*(progress-7/8))*self.abilitysize/2,0)),yy))
                
                
                pygame.draw.polygon(self.world.surface, (0,0,0,100), points)
            self.world.screen.blit(self.world.fontobject.render(chr(self.keybinds[x]), 1, (0,0,0)),(box[0]+4,box[1]+2)) 
            
        #ability description  
        for x in range(self.num_abilities):
            xx=self.x+x*self.abilitysize
            yy=self.y
            box=[xx,yy,self.abilitysize,self.abilitysize]
            if checkmousebox(box,mouse):
                descriptionbox=[mouse[0],mouse[1]-55,150,55]
                pygame.draw.rect(self.world.screen, (150,150,150),
                             (descriptionbox[0]+1,descriptionbox[1]+1,
                              descriptionbox[2]-1,descriptionbox[3]-1), 0)
                pygame.draw.rect(self.world.screen, (0,0,0),
                             (descriptionbox[0],descriptionbox[1],
                              descriptionbox[2],descriptionbox[3]), 1)
                self.world.screen.blit(self.world.fontobject.render(self.abilitydescriptions[x][0]+":", 1, (0,0,0)),(descriptionbox[0]+5,descriptionbox[1]+5)) 
                self.world.screen.blit(self.world.fontobject.render(self.abilitydescriptions[x][1], 1, (0,0,0)),(descriptionbox[0]+5,descriptionbox[1]+20)) 
                self.world.screen.blit(self.world.fontobject.render("cooldown: "+str(self.cooldowns[x])+" seconds", 1, (255,255,255)),(descriptionbox[0]+5,descriptionbox[1]+descriptionbox[3]-15)) 
            
            

class statusbars:
    def __init__(self,world):
        self.world=world
        self.hpmax=1
        self.hp=0
        self.manamax=1
        self.mana=0
        self.staminamax=1
        self.stamina=0
        
        #displaying enemy info
        self.target=None
    def startbars(self, hpmax, hp, manamax, mana, staminamax, stamina):
        self.hpmax=int(hpmax)
        self.hp=int(hp)
        self.manamax=int(manamax)
        self.mana=int(mana)
        self.staminamax=int(staminamax)
        self.stamina=int(stamina)
        
    def draw(self):
        if not self.target==None:
            box=[100, 45, 150, 50]
            pygame.draw.rect(self.world.screen, (200,200,200),(box[0],box[1],
                                                             box[2],box[3]), 0)
            self.world.screen.blit(self.world.fontobject.render(str(self.target.name), 1, (0,0,0)),(box[0]+box[2]/2-(len(self.target.name))*4,box[1]+5))
            
            hpmaxbox=[110,70,130,12]
            pygame.draw.rect(self.world.screen, (255,50,50),(hpmaxbox[0],hpmaxbox[1],
                                                     hpmaxbox[2],hpmaxbox[3]), 1)
            pygame.draw.rect(self.world.screen, (255,0,0),(hpmaxbox[0]+1,hpmaxbox[1]+1,
                                                     (self.target.hp/self.target.hpmax)*(hpmaxbox[2]-1),hpmaxbox[3]-1), 0)
            hpstring=str(self.target.hp)+"/"+str(self.target.hpmax)
            self.world.screen.blit(self.world.fontobject.render(hpstring, 1, (0,0,0)),(hpmaxbox[0]+hpmaxbox[2]/2-(len(hpstring))*3,hpmaxbox[1]))
        
        hpmaxbox=[125,1,150,12]
        pygame.draw.rect(self.world.screen, (255,50,50),(hpmaxbox[0],hpmaxbox[1],
                                                     hpmaxbox[2],hpmaxbox[3]), 1)
        pygame.draw.rect(self.world.screen, (255,0,0),(hpmaxbox[0]+1,hpmaxbox[1]+1,
                                                     (self.hp/self.hpmax)*(hpmaxbox[2]-1),hpmaxbox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render(str(self.hp)+"/"+str(self.hpmax), 1, (0,0,0)),(hpmaxbox[0]+hpmaxbox[2]/3,hpmaxbox[1]))
                
        manamaxbox=[125,15,150,12]
        pygame.draw.rect(self.world.screen, (50,50,255),(manamaxbox[0],manamaxbox[1],
                                                     manamaxbox[2],manamaxbox[3]), 1)
        pygame.draw.rect(self.world.screen, (0,0,255),(manamaxbox[0]+1,manamaxbox[1]+1,
                                                     (self.mana/self.manamax)*(manamaxbox[2]-1),manamaxbox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render(str(self.mana)+"/"+str(self.manamax), 1, (0,0,0)),(manamaxbox[0]+manamaxbox[2]/3,manamaxbox[1]))
        
        staminamaxbox=[125,29,150,12]
        pygame.draw.rect(self.world.screen, (50,255,50),(staminamaxbox[0],staminamaxbox[1],
                                                     staminamaxbox[2],staminamaxbox[3]), 1)
        pygame.draw.rect(self.world.screen, (0,255,0),(staminamaxbox[0]+1,staminamaxbox[1]+1,
                                                     (self.stamina/self.staminamax)*(staminamaxbox[2]-1),staminamaxbox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render(str(self.stamina)+"/"+str(self.staminamax), 1, (0,0,0)),(staminamaxbox[0]+staminamaxbox[2]/3,staminamaxbox[1]))
        