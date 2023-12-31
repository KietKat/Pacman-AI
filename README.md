# Pacman- AI (Fall 2023)
======================================

## Intro
[The Pacman Projects](http://ai.berkeley.edu/project_overview.html) by the [University of California, Berkeley](http://berkeley.edu/).

![Animated gif pacman game](http://ai.berkeley.edu/images/pacman_game.gif)

> In this project, the Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. Try to build general search algorithms and apply them to Pacman scenarios.

Start a game with the command:
```
$ python pacman.py
```
You can see the list of all options and their default values via:
```
$ python pacman.py -h
```

## PHASE 1: Search
- DFS, BFS, UCS, ASTAR, ASTAR heuristic 
```
States are wrapped in a `SearchNode` that stores: 

- the cost to reach the node,
- the previous node, 
- the action that led to the node. 

All the search algorithm variants were implemented using a single 
generic search function and various `Fringe` implementations, one for each
search variant: 
- For DFS, it is stack 
$ python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs
- For BSF, it is queue 
$ python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
- For UCS, it is a priority queue 
$ python pacman.py -l bigMaze -p SearchAgent -a fn=ucs
- For A*, it is a priority queue whose keys are computed by summing 
the backward cost (as in UCS) to the estimated forward cost computed
by the provided heuristic.
$ python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```
- Corner problem, Corner heuristic
```
In corner mazes, there are four dots, one in each corner. Our new search problem 
is to find the shortest path through the maze that touches all four corners (whether 
the maze has food there or not).

$ python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
$ python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```
- Eating all the dots
```
For this, we’ll need a new search problem definition that formalizes the food-clearing 
problem: FoodSearchProblem in searchAgents.py (implemented for you). A solution is 
defined to be a path that collects all of the food in the Pacman world. For the present 
project, solutions do not take into account any ghosts or power pellets; solutions only 
depend on the placement of walls, regular food, and Pacman.

$ python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

## PHASE 2: Multi-Agent Pacman (Adversarial Search)
- Minimax Algorithm
![Pacman Minimax](https://inst.eecs.berkeley.edu/~cs188/fa23/assets/projects/minimax_depth.png)
- Alpha-beta pruning
```
The AlphaBetaAgent minimax values should be identical to the MinimaxAgent minimax values,
although the actions it selects can vary because of different tie-breaking behavior.
```
- Expectimax Algorithm
```
Minimax and alpha-beta are great, but they both assume that you are playing against an adversary
who makes optimal decisions. As anyone who has ever won tic-tac-toe can tell you, this is not
always the case. In this question, you will implement the ExpectimaxAgent, which is useful for
 modeling the probabilistic behavior of agents who may make suboptimal choices.
```
## Credits
- This is the homework project for the course Intro to Artificial Intelligence, UC Berkeley (2023 Fall)
- Author: Kyle Nguyen
