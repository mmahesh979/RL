# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

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
        helper_vector = util.Counter() # Copy of vectors to be used for batch updating 
        
        for i in range(self.iterations):
            for state in mdp.getStates():
                if mdp.isTerminal(state):
                    continue
                if mdp.getPossibleActions(state):
                    helper_vector[state] = sum([transition[1]*(mdp.getReward(state,mdp.getPossibleActions(state)[0],transition[0])+self.discount*self.values[transition[0]])
                        for transition in mdp.getTransitionStatesAndProbs(state, mdp.getPossibleActions(state)[0])] )
                for action in mdp.getPossibleActions(state):
                    helper_vector[state] = max(helper_vector[state],sum([ transition[1]*(mdp.getReward(state, action, transition[0])+self.discount*self.values[transition[0]])
                        for transition in mdp.getTransitionStatesAndProbs(state, action)] ))
            for state in helper_vector:
                self.values[state] = helper_vector[state]
 
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
        out_value = sum( [ transition[1] * ( self.mdp.getReward(state, action, transition[0]) + self.discount*self.getValue(transition[0]) )
            for transition in self.mdp.getTransitionStatesAndProbs(state, action) ] )
        return out_value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions_from_here = self.mdp.getPossibleActions(state)
        transitions_from_here = list()

        if not actions_from_here:
            return None

        for action in actions_from_here:
            transitions_from_here.append(self.mdp.getTransitionStatesAndProbs(state, action))

        best_action = actions_from_here[0]
        best_value = sum( [self.getValue(trans[0])*trans[1] for trans in transitions_from_here[0]] )
        for action_index, transition in enumerate(transitions_from_here):
            current_value = sum( [self.getValue(trans[0])*trans[1] for trans in transition ] )
            if current_value > best_value:
                best_value = current_value
                best_action = actions_from_here[action_index]
        return best_action  
                      
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
