# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    "*** YOUR CODE HERE ***"
    from util import Stack

    #Did we already win?  :o
    if problem.isGoalState(problem.getStartState()):
        return []
    
    pila = Stack()
    visitado = []
    pathFromStart = []

    pila.push((problem.getStartState(), []))
    while(True):
        #Exit condition: Fail D:
        if pila.isEmpty():
            return []

        position, pathFromStart = pila.pop()
        visitado.append(position)

        #Exit condition: Goal! :D
        if problem.isGoalState(position):
            return pathFromStart

        succesor = problem.getSuccessors(position)
        if succesor:
            for item in succesor:
                if item[0] not in visitado:
                    pathFromState = pathFromStart + [item[1]]
                    pila.push((item[0], pathFromState))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    "*** YOUR CODE HERE ***"
    from util import Queue
    
    #Did we already win?  :o
    if problem.isGoalState(problem.getStartState()):
        return []

    cola = Queue()
    visitado = []
    pathFromStart = []

    cola.push((problem.getStartState(), []))
    while(True):
        #Exit condition: Fail D:
        if cola.isEmpty():
            return []

        position, pathFromStart = cola.pop()
        visitado.append(position)
        
        #Exit condition: Goal! :D
        if problem.isGoalState(position):
            return pathFromStart

        succesor = problem.getSuccessors(position)
        if succesor:
            for item in succesor:
                if item[0] not in visitado and item[0] not in (state[0] for state in cola.list):
                    pathFromState = pathFromStart + [item[1]]
                    cola.push((item[0], pathFromState))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    
    #Did we already win?  :o
    if problem.isGoalState(problem.getStartState()):
        return []

    hpq = PriorityQueue()

    visitado = []
    pathFromStart = []

    hpq.push((problem.getStartState(), []), 0) #Lowest priority.
    while(True):
        #Exit condition: Fail D:
        if hpq.isEmpty():
            return []

        position, pathFromStart = hpq.pop()
        visitado.append(position)
        
        #Exit condition: Goal! :D
        if problem.isGoalState(position):
            return pathFromStart

        succesor = problem.getSuccessors(position)
        if succesor:
            for item in succesor:
                if item[0] not in visitado and (item[0] not in (state[2][0] for state in hpq.heap)):
                    pathFromState = pathFromStart + [item[1]]
                    cost = problem.getCostOfActions(pathFromState)
                    hpq.push((item[0], pathFromState), cost)

                elif item[0] not in visitado and (item[0] in (state[2][0] for state in hpq.heap)):
                    for state in hpq.heap:
                        if state[2][0] == item[0]:
                            costPast = problem.getCostOfActions(state[2][1])

                    costNext = problem.getCostOfActions(pathFromStart + [item[1]])

                    if costPast > costNext:
                        pathFromState = pathFromStart + [item[1]]
                        hpq.update((item[0], pathFromState), costNext)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    "*** YOUR CODE HERE ***"
    # queueXY: ((x,y),[path]) #
    cola = HPQ(problem, heuristica)
    
    #Did we already win?  :o
    if problem.isGoalState(problem.getStartState()):
        return []
    
    pathFromStart = []
    visited = []
    state = (problem.getStartState(),[])

    cola.push(state, heuristic)
    
    while(True):
        #Exit condition: Fail D:
        if cola.isEmpty():
            return []

        position, pathFromStart = cola.pop()

        #State already seen?
        if position in visited:
            continue

        visited.append(position)

        #Exit condition: Goal! :D
        if problem.isGoalState(position):
            return pathFromStart

        successor = problem.getSuccessors(position)
        if successor:
            for item in successor:
                if item[0] not in visited:
                    pathFromState = pathFromStart + [item[1]]
                    state = (item[0], pathFromState)
                    cola.push(state, heuristic)


from util import PriorityQueue
class HPQ(PriorityQueue):
    def  __init__(self, problem, function):
        PriorityQueue.__init__(self)
        self.function = function
        self.problem = problem
    def push(self, element, heuristic):
        PriorityQueue.push(self, element, self.function(self.problem,element,heuristic))
def heuristica(problem, state, heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0], problem)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
