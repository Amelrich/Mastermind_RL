#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from random import randint
from mastermind import Mastermind

def random_policy():
    combi = [randint(0,5), randint(0,5), randint(0,5), randint(0,5)]
    return(combi)
    

class Sarsa(object):
    
    def __init__(self, learning_rate = 0.01, gamma = 0.9, q_table = dict(), is_qtable = False):
        #gamma and learning rate as seen in the 6th and 7th lecture
        self.lr = learning_rate
        self.gamma = gamma
        self.policy = []
        self.action_representation = self.create_list_action()
        
        #We now build the Q-table
        #Q-table is a 19440*1296 table (state, action) computed as (combination+feedback, combination)
        
        #The results possibilities represents the feedback giving by the environment 
        #They are presented as a string of couple numbers: (placed,misplaced)
        #   Placed are the pegs which have the right color AND the right placement
        #   Misplaced are the pegs which have the right color but are not currently at the right place.
        if is_qtable:
            self.q_table = q_table
        else:
            results_poss = ['00','01','10','11','02','20','11','30','03','21','12','04','40','31','13','22']
            q_temp = dict()
            for i in range(1296):
                for s in results_poss:
                    q_temp[str(i)+s] = np.array([0. for j in range(1296)])
                    
            q_temp['init'] = np.array([0. for j in range(1296)])
            
            self.q_table = q_temp
        
        
    def choose_action(self, observation):
        
        state_action = self.q_table[observation]
        
        if observation == 'init':
            self.policy = [i for i in range(1296)]
            
        else:
            pseudo_code = self.action_representation[ int(observation[:-2]) ]
            new_policy = []
            placed, misplaced = int(observation[-2]), int(observation[-1])
            for s in self.policy:
                possible_code = self.action_representation[s]
                if self.feedback(pseudo_code, possible_code) == (placed,misplaced):
                    new_policy.append(s)
            self.policy = new_policy
        
        #Compute the argmax space
        val_qmax = state_action[ self.policy[0] ]
        qmax = [ self.policy[0] ]
        
        for s in self.policy:
            if state_action[s] > val_qmax:
                val_qmax = state_action[s]
                qmax = [s]
                
            elif state_action[s] == val_qmax:
                qmax.append(s)
        
        action = np.random.choice(qmax)
        return (action)
        
    
    def learn(self, s, a, r, s_, a_, terminal):
        
        q_predict = self.q_table[s][a]
        if terminal:
            q_target = r  # next state is terminal
        else:
            q_target = r + self.gamma * self.q_table[s_][a_] # next state is not terminal
            
        self.q_table[s][a] += self.lr * (q_target - q_predict)  # update
        
        
    def feedback(self, combi1, combi2):
        
        #print(self.combi, prediction)
        try:
            a,b = zip(*[(a,b) for a,b in zip(combi1, combi2) if a!=b])
            a   = list(a)
        except: return 4,0
        
        for i in b:
            try: a.remove(i)
            except: continue
        
        return 4-len(b),len(b)-len(a)
    
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