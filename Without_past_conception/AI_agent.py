import numpy as np
from random import randint

def random_policy():
    combi = [randint(0,5), randint(0,5), randint(0,5), randint(0,5)]
    return(combi)
    
class Sarsa(object):

    def __init__(self, learning_rate = 0.01, gamma = 0.9):
        #gamma and learning rate as seen in the 6th and 7th lecture
        self.lr = learning_rate
        self.gamma = gamma

        #We now build the Q-table
        #Q-table is a 19440*1296 table (state, action) computed as (combination+feedback, combination)

        #The results possibilities represents the feedback giving by the environment 
        #They are presented as a string of couple numbers: (placed,misplaced)
        #   Placed are the pegs which have the right color AND the right placement
        #   Misplaced are the pegs which have the right color but are not currently at the right place.
        results_poss = ['00','01','10','11','02','20','11','30','03','21','12','04','40','31','13','22']
        q_temp = dict()
        for i in range(1296):
          for s in results_poss:
              q_temp[str(i)+s] = np.array([0. for j in range(1296)])

        q_temp['init'] = np.array([0. for j in range(1296)])

        self.q_table = q_temp
        
        
    def choose_action(self, observation):
	
        state_action = self.q_table[observation]

        #Compute the argmax space
        val_qmax = state_action[0]
        qmax = []
        for i in range(1296):
          if state_action[i] > val_qmax:
              val_qmax = state_action[i]
              qmax = [i]

          elif state_action[i] == val_qmax:
              qmax.append(i)

        action = np.random.choice(qmax)
        return (action)
    
    
    def learn(self, s, a, r, s_, a_, terminal):
        
        q_predict = self.q_table[s][a]
        if terminal:
            q_target = r  # next state is terminal
        else:
            q_target = r + self.gamma * self.q_table[s_][a_] # next state is not terminal
            
        self.q_table[s][a] += self.lr * (q_target - q_predict)  # update