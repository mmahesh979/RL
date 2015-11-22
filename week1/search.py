# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def genericSearch(problem, mode, heuristic=lambda x,y: 0):
    """
    Implements a generic tree searching algorithm whose queueing 
    behavior can be adjusted by changing the value of parameter 'mode'
        
    Valid modes: 'DFS', 'BFS', 'UCS', 'ASTAR'
        
    If an unsupported 'mode' is passed, raise util.raiseNotDefined()
    """
    from game import Directions
    WEST = Directions.WEST
    EAST = Directions.EAST
    SOUTH = Directions.SOUTH
    NORTH = Directions.NORTH
    
    """
    This determines the queueing strategy used by the searcher. 
        DFS: Uses a LIFO stack
        BFS: Uses a FIFO queue
    """
    if mode == "DFS":
        state_stack = util.Stack()
    elif mode == "BFS":
        state_stack = util.Queue()
    elif mode == "UCS" or mode == "ASTAR":
        state_stack = util.PriorityQueue()
    else:
        util.raiseNotDefined()

    move_list = list()
    history = set()
    start_state = (problem.getStartState(), None, None, 0)
    
    def helper( state ):
        """
        Helper function for the search implementation. Takes a state
        object which is a triple of the form: ( (x,y), DIRECTION, PREV_STATE, TOTAL_COST )
        """
        if mode == "DFS" or mode == "BFS":
            state_stack.push( state )
        else:
            state_stack.push( state, 0)

        while not state_stack.isEmpty():
            current_state = state_stack.pop()
            if problem.isGoalState( current_state[0] ):
                return current_state
            if not current_state[0] in history:
                for successor in problem.getSuccessors(current_state[0]):
                    if mode == "DFS" or mode == "BFS":
                        state_stack.push( (successor[0], successor[1], current_state, 0) )
                    else:
                        state_stack.push( (successor[0], successor[1], current_state, successor[2]+current_state[3] ), 
                            successor[2]+current_state[3] + heuristic(successor[0], problem))
                history.add( current_state[0] )

    goal_triple = helper( start_state )
   
    " Populate the move list with backtracking history from goal "
    while not goal_triple == None:
        move_list.append(goal_triple[1])
        goal_triple = goal_triple[2]

    " The move_list must be normalized on its way out "
    return move_list[::-1][1::]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:",problem.getSuccessors(problem.getStartState())
    """
    
    return genericSearch(problem, "DFS")

    "util.raiseNotDefined()"

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    
    return genericSearch(problem, "BFS")
    
    "util.raiseNotDefined()"

def uniformCostSearch(problem):
    "Search the node of least total cost first. "

    return genericSearch(problem, "UCS")
    
    "util.raiseNotDefined()"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    
    return genericSearch(problem, "ASTAR", heuristic)
    
    "util.raiseNotDefined()"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
