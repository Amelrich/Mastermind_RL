#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mastermind import Mastermind
from AI_agent import Sarsa
import time
import csv



def update(iteration_number):
    #This function aim to generate a number of 
    
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
    
    
def update_recursive_SARSA(iteration_number):
    #Use a "recursive" update of SARSA as defined in the report
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
        
            #swap observation and action
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
        
    print('Ratio = ', (win_count/iteration_number)*100, '%')
    print('In ', turn_number/win_count, 'turns')
    return(None)
    

def save_table(table):
    #A function to save the Q-table in a csv file
    file = open('learnt_table_SARSA.csv', 'w')    
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
    file = open(file_name, 'r')
    q_temp = dict()
    for row in csv.reader(file, delimiter = ';'):
        q_temp[row[0]] = [float(row[k+1]) for k in range(1296)]
    
    file.close()
    return(q_temp)
    

if __name__ == "__main__":
    env = Mastermind()
    RL = Sarsa()      
    
    for k in range(21):
        t1 = time.time()
        print('After ',k*100000,' epochs')
        test_perf(10000)
        update(100000) #or update_recursive_SARSA(100000)
        print('')
        print(time.time()-t1)
        
    save_table(RL.q_table)