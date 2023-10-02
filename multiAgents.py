# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        estimatedScore = successorGameState.getScore()
        """
            New evaluation function estimates score based on 2 aspects:
                We add the score based on the distance between food and Pacman
                    -> Each food add 10 points -> 10/min_manhattanDistance
                If this action makes Pacman too vulnerable to ghost nit in Scared time
                    -> We decrease the score very seriously, as it leads to instant loss
        """

        remainingFood = newFood.asList()

        if remainingFood:
            minManhattanDistance = min([util.manhattanDistance(newPos, food) for food in remainingFood])
            if minManhattanDistance == 0: 
                estimatedScore += 10
            else:
                estimatedScore += 10/minManhattanDistance

        for ghostStates, scaredTimes in zip(newGhostStates, newScaredTimes):
            ghostPosition = ghostStates.getPosition()
            if scaredTimes == 0 and util.manhattanDistance(ghostPosition, newPos) < 1.8:
                estimatedScore -= 1000
        return estimatedScore


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0) #generate Pacman legal action
        bestValue = -float("inf")
        bestAction = None
        for action in legalActions:
            childState = gameState.generateSuccessor(0,action)
            actionEvaluation = self.miniMax(childState, self.depth, 1)
            if actionEvaluation > bestValue:
                bestValue = actionEvaluation
                bestAction = action

        return bestAction


    def miniMax(self, gameState, depth, agentIndex):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
        
        numOfAgents = gameState.getNumAgents()
        agentIndex = agentIndex% numOfAgents # avoid overflow value 
        if agentIndex == 0: #max agent -> the pacman-kun
            maxEval = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                childState = gameState.generateSuccessor(agentIndex, action)
                newEval = self.miniMax(childState, depth, agentIndex + 1)
                maxEval = max(newEval, maxEval)
            return maxEval
        else:
            minEval = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                childState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numOfAgents - 1: #last agent, move to the next depth
                    newEval = self.miniMax(childState, depth-1, 0) 
                else:
                    newEval = self.miniMax(childState, depth, agentIndex + 1)
                minEval = min(minEval, newEval)
            return minEval    



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0) #generate Pacman legal action
        bestValue = -float("inf")
        bestAction = None
        alpha = -float("inf")
        beta = float("inf")
        for action in legalActions:
            childState = gameState.generateSuccessor(0,action)
            actionEvaluation = self.miniMax(childState, self.depth, alpha, beta, 1)
            if actionEvaluation > bestValue:
                bestValue = actionEvaluation
                bestAction = action
            alpha = max(alpha, bestValue)
            if bestValue > beta:
                break

        return bestAction


    def miniMax(self, gameState, depth, alpha, beta, agentIndex):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        
        numOfAgents = gameState.getNumAgents()
        agentIndex = agentIndex% numOfAgents # avoid overflow value 

        if agentIndex == 0: #max agent -> the pacman-kun
            maxEval = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                childState = gameState.generateSuccessor(agentIndex, action)
                newEval = self.miniMax(childState, depth, alpha, beta, agentIndex + 1)
                maxEval = max(newEval, maxEval)
                if maxEval > beta:
                    return maxEval

                alpha = max(maxEval, alpha)
            return maxEval
        else:
            minEval = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                childState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numOfAgents - 1: #last agent, move to the next depth
                    newEval = self.miniMax(childState, depth-1, alpha, beta, 0) 
                else:
                    newEval = self.miniMax(childState, depth, alpha, beta, agentIndex + 1)
                minEval = min(minEval, newEval)
                if minEval < alpha:
                    return minEval
                beta = min(minEval,beta)

            return minEval   


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0) #generate Pacman legal action
        bestValue = -float("inf")
        bestAction = None
        for action in legalActions:
            childState = gameState.generateSuccessor(0,action)
            actionEvaluation = self.expectiMax(childState, self.depth, 1)
            if actionEvaluation > bestValue:
                bestValue = actionEvaluation
                bestAction = action

        return bestAction

    def expectiMax(self, gameState, depth, agentIndex):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
        
        numOfAgents = gameState.getNumAgents()
        agentIndex = agentIndex% numOfAgents # avoid overflow value 
        if agentIndex == 0: #max agent -> the pacman-kun
            maxEval = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                childState = gameState.generateSuccessor(agentIndex, action)
                newEval = self.expectiMax(childState, depth, agentIndex + 1)
                maxEval = max(newEval, maxEval)
            return maxEval
        else: # Ghost suboptimal  
            expectedValue = 0.0
            legalActions = gameState.getLegalActions(agentIndex)
            numOfActions = len(legalActions)
            for action in legalActions:
                childState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numOfAgents - 1: #last agent, move to the next depth
                    newEval = self.expectiMax(childState, depth-1, 0) 
                else:
                    newEval = self.expectiMax(childState, depth, agentIndex + 1)

                expectedValue += newEval
            return expectedValue / numOfAgents

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()
    estimatedScore = currentGameState.getScore()

    # Weighted features
    foodWeight = 10.0  # Lower weight to encourage moving towards food earlier
    ghostAvoidanceWeight = -1000.0  # Stronger penalty to avoid non-scared ghosts
    capsuleWeight = 100.0  # Adjusted weight to encourage moving towards capsules

    # Calculate remaining food and its distance
    foodDistances = [manhattanDistance(pacmanPos, food) for food in food.asList()]
    foodScore = 1
    if len(foodDistances) > 0:
        foodScore = foodWeight / min(foodDistances)

    # Avoid non-scared ghost
    for ghostState, scaredTime in zip(ghostStates, scaredTimes):
        ghostPosition = ghostState.getPosition()
        ghostDistance = util.manhattanDistance(ghostPosition, pacmanPos)
        if scaredTime == 0:
            if ghostDistance < 4:
                estimatedScore += ghostAvoidanceWeight
            else:
                estimatedScore += foodScore
        else: 
            estimatedScore += 100/ghostDistance

    # Accumulate score from capsules
    for capsule in capsules:
        if capsule == pacmanPos:
            estimatedScore += capsuleWeight


    return estimatedScore


better = betterEvaluationFunction
