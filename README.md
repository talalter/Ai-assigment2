Assigment2 - Artificial Intelligence 202-2-5661 

Cooperating and adversarial agents in the Hurricane Evacuation Problem
In the second exercise you will be using a simplified version of the environment simulator from the first assignment, the Hurricane Evacuation problem, as a platform for implementing intelligent cooperating and adversarial agents. The environment is the same as before, except that now we will assume two evacuation agents (perhaps they are employed at competing companies) who seek to evacuate as many people as possible. We will examine settings ranging from cooperative to adversarial.

Game Environment
As before, the environment consists of an undirected weighted graph, but now we will assume that all edge weights are 1. An agent can apply 2 types of action: traverse and no-op. Semantics of the action are as in assignment 1, repeated below. The traverse action always succeeds if the target vertex is unbroken, and fails otherwise. A failed action behaves like no-op. Although this is a bit unnatural, we will assume for simplicity that the agents take turns at every time unit, rather than moving truly in parallel. The game ends when no more people can be saved or when a previously visited world state is revisited. (By a world state being revisited, this inclused locations of both agents with the same agent to move, same people saved, and same unbroken vertex states.)

Implementation Steps
The simulator should query the user about the parameters, the type of game (see below) as well as other initialization parameters.

After the above initialization, the simulator should run each agent in turn, performing the actions returned by the agents, and update the world accordingly. Additionally, the simulator should be capable of displaying the world status after each step, with the appropriate state of the agents and their score. The agent individual score ISi is the number of people it has saved. The agent total score TSi that it tries to optimize depends on the type of game, below. Each agent program (a function) works as follows. The agent is called by the simulator, together with a set of observations. The agent returns a move to be carried out in the current world state. The agent is allowed to keep an internal state if needed. In this assignment, the agents can observe the entire state of the world. You should support the following types of games:

Adversarial (zero sum game): each agent aims to maximize its own individual score (number of people saved) minus the opposing agent's score. That is, TS1=IS1-IS2 and TS2=IS2-IS1. Here you should implement an "optimal" agent, using mini-max, with alpha-beta pruning.
A semi-cooperative game: each agent tries to maximize its own individual score. The agent disregards the other agent score, except that ties are broken cooperatively. THat is, TS1=IS1, breking ties in favor of greater IS2.
A fully cooperative game: both agents aim to maximize the sum of individual scores, so TS1=TS2=IS1+IS2.
Since the game tree will usually be too big to reach terminal positions in the search, you should also implement a cutoff, and a heuristic static evaluation function for each game. You may use the same heuristic for all games, if you think this is justified.
