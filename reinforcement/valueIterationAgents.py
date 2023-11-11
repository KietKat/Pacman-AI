# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations):
            newValues = util.Counter()

            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    qValues = [self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)]
                    newValues[state] = max(qValues) if qValues else 0

            self.values = newValues        


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0

        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action): # Max sum
            qValue += prob * (self.discount*self.getValue(nextState) + self.mdp.getReward(state, action, nextState))

        return qValue    

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if not self.mdp.isTerminal(state):
            possibleAction = self.mdp.getPossibleActions(state)
            bestAction = max(possibleAction, key = lambda action: self.computeQValueFromValues(state, action))

            return bestAction
        
        return None


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        self.priorityQueue = util.PriorityQueue()
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {state : set() for state in self.mdp.getStates()}

        # Set up predecessors of all states
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                for action in self.mdp.getPossibleActions(s):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                        if prob != 0:
                            predecessors[nextState].add(s)
        
        pq = util.PriorityQueue()

        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                maxQDiff = abs(self.values[s] - max([self.computeQValueFromValues(s,action)
                                 for action in self.mdp.getPossibleActions(s)]))
                pq.update(s, -maxQDiff)

        for _ in range(self.iterations):
            if pq.isEmpty(): 
                break

            currentState = pq.pop()
            if not self.mdp.isTerminal(currentState):
                self.values[currentState] = max([self.computeQValueFromValues(currentState,action)
                                                 for action in self.mdp.getPossibleActions(currentState)])
            
            for p in predecessors[currentState]:
                diff = abs(self.values[p] - max([self.computeQValueFromValues(p,action)
                             for action in self.mdp.getPossibleActions(p)]))
                if diff > self.theta:
                    pq.update(p, -diff)




        
                        


