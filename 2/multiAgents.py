# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        ghostPositions = [ghost.getPosition() for ghost in newGhostStates]
        scaredTimesSum = sum([num for num in newScaredTimes])
        currentPos = currentGameState.getPacmanPosition()
        oldNearestGhost = min([ manhattanDistance(ghost.getPosition(), currentPos) for ghost in newGhostStates ])
        newNearestGhost = min([ manhattanDistance(ghost.getPosition(), newPos) for ghost in newGhostStates ])
        outScore = 1
        
        def ghostNearMe():
            for r in range(-1,2):
                for c in range(-1,2):
                    if( (newPos[0]-r, newPos[1]-c) in ghostPositions ):
                        return True
            return False
        
        if newFood.asList():
            newNearestFoodPellet = min([manhattanDistance(newPos, dot) for dot in newFood.asList() ] )
            oldNearestFoodPellet = min([manhattanDistance(currentPos, dot) for dot in newFood.asList() ] )
        else:
            newNearestFoodPellet = 0
            oldNearestFoodPellet = 0

        if (newPos in currentGameState.getFood().asList()):
            outScore = 2*outScore
        elif newNearestFoodPellet < oldNearestFoodPellet:
            outScore = 1.55*outScore
           
        if (newPos in ghostPositions):
            outScore = -1
        elif ghostNearMe():
            outScore = .25*outScore

        return outScore

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        def value(state, depth, who):
            if who == 0:
                depth = depth + 1
            if depth == self.depth:
                return self.evaluationFunction(state)
            if who == 0:
                return max_value(state, depth)                    
            return min_value(state, depth, who) 

        def min_value(state, depth, agent_index):
            v = float("inf")
            valid_ghost_actions = state.getLegalActions(agent_index);
            ghost_successors = [ state.generateSuccessor(agent_index, action) for action in valid_ghost_actions]
            if not ghost_successors:
                return self.evaluationFunction(state)
            for successor in ghost_successors:
                v = min(v, value(successor, depth, (agent_index+1) % state.getNumAgents()))
            return v

        def max_value(state, depth):
            v = float("-inf")
            valid_pacman_actions = state.getLegalActions(0)
            pacman_successors = [state.generateSuccessor(0, action) for action in valid_pacman_actions]
            if not pacman_successors:
                return self.evaluationFunction(state)
            for successor in pacman_successors:
                v = max(v, value(successor, depth, 1))
            return v
      
        best_move = gameState.getLegalActions(0)[0]
        best_utility = float("-inf")
        for i, successor in enumerate([gameState.generateSuccessor(0, a) for a in gameState.getLegalActions(0)]): 
            utility_of_successor = value(successor,0,1)
            if utility_of_successor > best_utility:
                best_move = gameState.getLegalActions(0)[i]
                best_utility = utility_of_successor

        return best_move 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def value(state, depth, who, alpha, beta):
            if who == 0:
                depth = depth + 1
            if depth == self.depth:
                return self.evaluationFunction(state)
            if who == 0:
                return max_value(state, depth, who, alpha, beta)[0]
            return min_value(state, depth, who, alpha, beta)

        def min_value(state, depth, agent_index, alpha, beta):
            v = float("inf")

            if not state.getLegalActions(agent_index):
                return self.evaluationFunction(state)

            for action in state.getLegalActions(agent_index):
                successor = state.generateSuccessor(agent_index, action)
                v = min(v, value(successor, depth, (agent_index+1) % state.getNumAgents(), alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(state, depth, who, alpha, beta):
            v = float("-inf")
            current_v = v
            max_index = None

            if not state.getLegalActions(0):
                return (self.evaluationFunction(state),)

            for action_index, action in enumerate(state.getLegalActions(0)):
                successor = state.generateSuccessor(0,action)
                current_v = value(successor, depth, (who+1) % state.getNumAgents(), alpha, beta)
                if current_v > v: 
                    v = current_v
                    max_index = action_index
                if v > beta: 
                    return v, max_index 
                alpha = max(alpha, v)
            return v, max_index
  
        return gameState.getLegalActions(0)[max_value(gameState,0,0,float("-inf"),float("inf"))[1]]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def value(state, depth, who):
            if who == 0:
                depth = depth + 1
            if depth == self.depth:
                return self.evaluationFunction(state)
            if who == 0:
                return max_value(state, depth, who)[0]
            return exp_value(state, depth, who)

        def exp_value(state, depth, who):
            v = 0.0
            valid_ghost_actions = state.getLegalActions(who)

            if not valid_ghost_actions:
                return self.evaluationFunction(state)

            for action in valid_ghost_actions: 
                successor = state.generateSuccessor(who, action)
                v = v + ( value(successor, depth, (who+1) % state.getNumAgents()) / float(len(valid_ghost_actions)) )
            return v

        def max_value(state, depth, who):
            v = float("-inf")
            current_v = v
            max_index = None

            if not state.getLegalActions(0):
                return (self.evaluationFunction(state),)

            for action_index, action in enumerate(state.getLegalActions(0)):
                successor = state.generateSuccessor(0,action)
                current_v = value(successor, depth, (who+1) % state.getNumAgents())
                if current_v > v: 
                    v = current_v
                    max_index = action_index
            return v, max_index
  
        return gameState.getLegalActions(0)[max_value(gameState,0,0)[1]]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The general design of this strategy was to use the game's
        own built-in getScore() method to 'guide' Pacman into behaving properly
        in general. From there, it was mostly a matter of fine-tuning his behavior.
        This was done by using a linearly combination of certain game parameters
        that I felt were important to track (i.e., subtracting distance to the
        nearest pellet to encourage Pacman to move toward pellets even if they were
        out of range of direct evaluation by getScore()). Logic was also added to 
        make Pacman especially apprehensive about getting too close to ghosts.
        Finally, to compensate for certain game conditions that leaves Pacman stuck
        in place due to the limited depth of the search in the event of similar 
        outcomes based on board characteristics alone, I added a parameter that tracks
        the distance to the nearest ghost. This extra randomness helps to seed the 
        evaluator while maintaining good behavior (i.e., keeping Pacman away from ghosts).  
    """
    foodList = currentGameState.getFood().asList(); 
    newPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    ghostPositions = [ghost.getPosition() for ghost in ghostStates]
    currentScore = currentGameState.getScore()
    outScore = 1
    foodCountRemaining = currentGameState.getNumFood()
    nearestFoodPellet = 0
    nearestGhost = 0;
   
    if foodList: 
        nearestFoodPellet = min( [manhattanDistance(newPos, dot) for dot in foodList ])
    if ghostPositions:
        nearestGhost = min([manhattanDistance(newPos, ghost) for ghost in ghostPositions])
    

    "Return true if there are no pellets near me"
    def pelletCheck():
        if foodList:
            if min([manhattanDistance(newPos, dot) for dot in foodList]) > 4:
                return True
        return False

    "Return true if there is a ghost in my viscinity"
    def ghostNearMe():
        for r in range(-2,4):
            for c in range(-2,4):
                if( (newPos[0]-r, newPos[1]-c) in ghostPositions ):
                    return True
        return False

    outScore = outScore - .6*nearestFoodPellet + 1.3*currentScore + .2*nearestGhost - .9*foodCountRemaining
 
    if ghostNearMe():
        outScore = .4*outScore
    if newPos in ghostPositions:
        outScore = -1
    
    return outScore

# Abbreviation
better = betterEvaluationFunction
