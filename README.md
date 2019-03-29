# Mastermind with Reinforcement Learning
Amaury Sudrie, Mark Sandal, Jefferson Gabriele Collaço

Last update 28 March 2019

### Abstract - 
In this paper we are interested in solving a master- mind game with reinforcement learning. The Mastermind game is a two players code-breaking game. The first player tries to find secret code chosen by the second player. The secret code consists of four colored pegs. With six colors and four pegs Donald E. Knuth elaborated a strategy [1] to find the secret code in at most five guess. Solving the problem using reinforcement learning was already studied in [2] however we provided an other point of view on the problem. We implemented a SARSA method and define a specific space state for this method. Our main goal is to compare our agent’s efficiency with the Knuth’s strategy efficiency and compare our results with the ones of [2]. Finally our trained agent is able to solve the game in an average less than 4.25 turns whereas [2] did it in an average of 4.294 at the best. Moreover our agent learnt to play a twice two same color pegs combination at the beginning of the game; the combination is the one recommended by Knuth’s strategy.



## About the code 
All methods and functions are commented. Here more explanations about how the code is organized. The code is structured in three principal python files:

#### mastermind.py
This module provide a class to build a graphic (or not) mastermind interface.

#### AI_agent.py
This module implement a SARSA method to solve master game by training an agent. 

The agent maintains policy vector which contain every still possible secret code candidates. At each turn it puts away all impossible combination.
About the Q-table: be aware that the state space is not the space of combination. We built a space state by concatenating the combination and the feedback provided by the environement. For the beginning we created an initial state 'init'.

This module contain three principal methods.
- One to init the Q-table
- One to update the policy vector and to choose an action w.r.t Q-table.
- One to update the Q-table i.e. to learn.

#### main.py
This file contains many functions:
- One to play games in order to train the agent
- One to test the current Q-table
- One to save the Q-table
- One to load an already Q-table
At the end of the file you will find some actions. The code is configured to run 100.000 training epochs and to give you every 10.000 epochs the average number of turns it requires to solve the game.

### Other comments
The file Without_past_conception allows to train an agent which only choose the next action based on the Q-table. In fact in this version there is no policy vector. Here the agent does not win systematically. After training it, the agent is able to win 20% to 30% of every games. Beware that here the agent will require a lot of training (2 millions epochs) which could take few hours.

## References:
[1] Donald E. Kunth. The Computer as Master Mind, J. Recreational Mathematics, Vol.9(1), 1976-77.

[2] W. Lu, J. Yang, H. Chu. Playing Mastermind Game by using Reinforcement Learning, 2017 First IEEE International Conference on Robotic Computing

[3] J.Read. Lecture6 - Topics in Reinforcement Learning, INF581 Advanced Topics in Artificial Intelligence, 2019.

[4] A. Oppermann - Self Learning AI-Agents Part II: Deep Q-Learning. Article on towardsdatascience.com

[5] J. Murielle - Mastermind in pygame https://www.dropbox.com/s/l9cooc1y246biii/mastermind.zip?dl=0
