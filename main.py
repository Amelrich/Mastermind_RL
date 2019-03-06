#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mastermind import Mastermind
from AI_agent import Sarsa
import time


def update(iteration_number):
    for episode in range(iteration_number):
        # initial observation
        observation = env.reset()
        path_sarsa = []

        # RL choose action based on observation
        action = RL.choose_action(observation)

        for line in range(10):

            # RL take action and get next observation and reward
            observation_, reward, won = env.step(action, line)

            # RL choose action based on next observation
            action_ = RL.choose_action(observation_)
            
            path_sarsa.append( [observation, action, reward, observation_, action_, won] )

            # swap observation and action
            observation = observation_
            action = action_

            # break while loop when end of this episode
            if won:
                break
        
        if line == 9:
            path_sarsa[9][5] = True
        
        nb_turns = len(path_sarsa)
        for i in range(nb_turns):
            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            s = path_sarsa[nb_turns - i - 1][0]
            a = path_sarsa[nb_turns - i - 1][1]
            r = path_sarsa[nb_turns - i - 1][2]
            s_ = path_sarsa[nb_turns - i - 1][3]
            a_ = path_sarsa[nb_turns - i - 1][4]
            terminal = path_sarsa[nb_turns - i - 1][5]
            
            RL.learn(s, a, r, s_, a_, terminal)
            
        
        if episode >= 990000: 
            
            print(won, line)

    # end of game

def save_table(table):
    #A function to save the Q-table in a csv file
    file = open('learnt_table.csv', 'w')    
    line = ";".join(str(v) for v in table['init'])
    line = "init;" + line + "\n"
    file.write(line)
    
    results_poss = ['00','01','10','11','02','20','11','30','03','21','12','04','40','31','13','22']
    for i in range(1296):
        for s in results_poss:
            line = ";".join(str(v) for v in table[str(i)+s])
            line = str(i)+s + ";" + line + "\n"
            file.write(line)

if __name__ == "__main__":
    t1 = time.time()
    env = Mastermind()
    RL = Sarsa()
    
    update(1000000)
    
    print(time.time()-t1)