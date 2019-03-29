#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygame import *
import numpy.random as rd

"""For now the human parameter which will permit someone to test the AI agent 
    in the graphical environment is not configured yet.
    Please let the human parameter remain to False""" 

class Mastermind(object):

    def __init__(self, human = False):
        self.human = human
        if human:
            self._build_mastermind()
            
        self.list_action = self.create_list_action()
        self.combi = []

    def _build_mastermind(self):

        self.screen = display.set_mode((280,550))
        display.set_caption('MasterMind')

        self.mmbg    = image.load('MMbg2.jpg')
        self.palette = image.load('palette2.png')
        self.myst    = image.load('myst.png')

        self.palet_rect = Rect(20,440,240,30)
        self.go_rect    = Rect(20,475,240,30)
        self.reset_rect = Rect(20,510,240,30)

        self.palet_mask = mask.from_surface(self.palette)

        self.combi = []
        self.ready = False

        self.screen.blit(self.mmbg,(0,0))
        self.screen.blit(self.palette,self.palet_rect)
        display.flip()
        

    def reset(self):
        if self.human:
            self.screen.blit(self.mmbg,(0,0))
            self.screen.blit(self.palette, self.palet_rect)
            self.ready = False
            display.flip()
        
        self.combi = []
        return('init')
    
    def create_list_action(self):
        #For a tissue to wipe your bleeding eyes, please come to Fayolle building 11.30.31
        res = dict()
        num = 0
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    for l in range(6):
                        res[num] = [i,j,k,l]
                        num = num + 1
        return res
        
    def human_agent(self):
        
        while (len(self.combi) < 4):
            ev = event.wait()
            
            if ev.type == MOUSEBUTTONUP:
                
                if self.palet_rect.collidepoint(ev.pos):
                    x,y = ev.pos
                    x -= self.palet_rect.x
                    y -= self.palet_rect.y
                    if self.palet_mask.get_at((x,y)):
                        self.combi.append(x//30)
                        self.scr.blit(self.palette,(80+(len(self.combi)-1)*30,20),(x//30*30,0,30,30))
                        display.flip()
                        
                if self.reset_rect.collidepoint(ev.pos):
                    self.reset()      


    def step(self, action, line):
        
        if self.human:
            if len(self.combi == 0):
                self.human_agent()
                
            while (self.ready != True):
                ev = event.wait()
                if ev.type == MOUSEBUTTONUP:
                    if self.go_rect.collidepoint(ev.pos):
                        self.ready=True
                    
        elif len(self.combi) == 0:
            self.combi = [rd.randint(0,5), rd.randint(0,5), rd.randint(0,5), rd.randint(0,5)]
        
        if self.human:
            r = self.screen.blit(self.myst,(50,line*35+70))
            display.update(r)
            
        prediction = self.list_action[action]
        
        if self.human:
            for i in range(4):
                r = self.screen.blit(self.palette, ((i+1)*30+20, line*35+70),(prediction[i]*30,0,30,30))
                display.update(r)
            
        placed,misplaced = self.feedback(prediction)
        
        if self.human:
            for e,c in enumerate([(255,0,0)]*placed+[(255,255,255)]*misplaced):
                r = draw.circle(self.screen, c, (190+e*10,line*35+85), 2, 0)
                display.update(r)
        
        s_ = str(action) + str(placed) + str(misplaced)
            
        return (s_, self.reward2(placed,misplaced,line), self.if_won(placed))

    def if_won(self, placed):
        return(placed==4)
        
    def reward1(self, placed):
        if placed == 4:
            return 0
        else:
            return -1
        
    def reward2(self, placed,misplaced,line):
        reward = -1
        
        if(placed==4):
            reward = (10-line)*(10-line)
            return reward
        
        if (placed == 0 and misplaced == 0):
            return reward
        else: 
            reward += placed*0.1
            reward += misplaced*0.05
            return reward
        
        
    def feedback(self, prediction):
        
        #print(self.combi, prediction)
        try:
            a,b = zip(*[(a,b) for a,b in zip(self.combi, prediction) if a!=b])
            a   = list(a)
        except: return 4,0
        
        for i in b:
            try: a.remove(i)
            except: continue
        
        return 4-len(b),len(b)-len(a)
    

