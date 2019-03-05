#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:16:37 2019

@author: amaury
"""

from mastermind import Mastermind
from AI_agent import Sarsa
import time


def update(iteration_number):
    for episode in range(iteration_number):
        # initial observation
        observation = env.reset()

        # RL choose action based on observation
        action = RL.choose_action(str(observation))

        for line in range(10):     #may be (1,11)??

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
        
        if episode >= 95000:
            print(won,line)

    # end of game

if __name__ == "__main__":
    t1 = time.time()
    env = Mastermind()
    RL = Sarsa()
    
    update(100000)
    print(time.time()-t1)