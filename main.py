#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mastermind import Mastermind
from AI_agent import Sarsa
import time
import csv



def update(iteration_number):
    for episode in range(iteration_number):
        # initial observation
        observation = env.reset()
        # RL choose action based on observation
        action = RL.choose_action(observation)

        for line in range(10):
            # RL take action and get next observation and reward
            observation_, reward, won = env.step(action, line)
            # RL choose action based on next observation
            action_ = RL.choose_action(str(observation_))
            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            RL.learn(str(observation), action, reward, str(observation_), action_, won)
            # swap observation and action
            observation = observation_
            action = action_
            # break while loop when end of this episode
            if won:
                break

            
    return(None)
            
def test_perf(iteration_number):
    win_count = 0
    turn_number = 0
    
    for episode in range(iteration_number):
        # initial observation
        observation = env.reset()
        
        # RL choose action based on observation
        action = RL.choose_action(observation)

        for line in range(10):
            # RL take action and get next observation and reward
            observation_, reward, won = env.step(action, line)
            
            # RL choose action based on next observation
            action_ = RL.choose_action(observation_)
            # swap observation and action
            observation = observation_
            action = action_
            # break while loop when end of this episode
            if won:
                win_count += 1
                turn_number += (line+1)
                break
            
        #print(won, line)
        
    print('Ratio = ', (win_count/iteration_number)*100, '%')
    print('In ', turn_number/win_count, 'turns')
    return(None)
    

def save_table(table):
    #A function to save the Q-table in a csv file
    file = open('learnt_table_SARSA_passed.csv', 'w')    
    line = ";".join(str(v) for v in table['init'])
    line = "init;" + line + "\n"
    file.write(line)
    
    results_poss = ['00','01','10','11','02','20','11','30','03','21','12','04','40','31','13','22']
    for i in range(1296):
        for s in results_poss:
            line = ";".join(str(v) for v in table[str(i)+s])
            line = str(i)+s + ";" + line + "\n"
            file.write(line)

    file.close()
            
def open_table(file_name, newline = ''):
    #A function to open a Q-table stored in a csv file
    file = open(file_name, 'r')
    q_temp = dict()
    for row in csv.reader(file, delimiter = ';'):
        q_temp[row[0]] = [float(row[k+1]) for k in range(1296)]
    
    file.close()
    return(q_temp)
    

if __name__ == "__main__":
    env = Mastermind()
    #RL = Sarsa(q_table = open_table(file_name="learnt_table_SARSA_passed.csv"), is_qtable=True) 
    #Remove the comment mode if you want to use an already saved Q-table.
    RL = Sarsa()
    
    n_epochs = 100000
    #update(n_epochs) #Remove the comment mode to directly train the agent
    #save_table(RL.q_table) #Remove the comment mode to save the table 
    
    perf_episode = n_epochs//10000
    
    for k in range(perf_episode + 1):
        t1 = time.time()
        print('After ',k*10000,' epochs')
        test_perf(10000)
        update(10000)
        print(time.time()-t1)
        print('')
    
    save_table(RL.q_table)
    