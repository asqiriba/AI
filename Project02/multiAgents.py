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
from util import manhattanDistance

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
        succesorPosition = successorGameState.getPacmanPosition()
        succesorFood = successorGameState.getFood()
        foodDistance = []
        ghostDistance = 0
        for x in range(0, succesorFood.width):
            for y in range(0, succesorFood.height):
                if succesorFood[x][y]:
                    foodDistance.append(util.manhattanDistance(succesorPosition, (x, y)))
        newGhostStates = successorGameState.getGhostStates()
        ghostPosition = successorGameState.getGhostPositions()
        ghostDistance = util.manhattanDistance(succesorPosition, ghostPosition[0])
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Declaring variables for later use.
        minFoodDistance = 999
        food = 0
        passedbyFood = 0
        ghosts = []
        newGhostState = len(newGhostStates)
        matrix = ((succesorFood.width - 3) + (succesorFood.height - 3))

        for d in foodDistance:
            if d < minFoodDistance and d != 0:
                minFoodDistance = d

        if minFoodDistance == 999:
            minFoodDistance = 0

        for x in range(0, succesorFood.width):
            for y in range(0, succesorFood.height):
                if succesorFood[x][y]:
                    food = food + 1
                
                check = currentGameState.hasFood(x, y)
                
                if check:
                    passedbyFood = passedbyFood + 1

        for g in newGhostStates:
            distance = manhattanDistance(succesorPosition, g.getPosition())
            if distance == 0:
                return -2
            
            ghostDistance = ghostDistance + distance
            ghosts.append(ghostDistance)

        food = abs(passedbyFood - food)
        ghostDistance = ghostDistance / newGhostState
        newGhostDistance = float(ghostDistance) / matrix
        
        if ghostDistance >= 5:
            newGhostDistance = 0

        for dist in ghosts:
            if dist > 1:
                continue
            else:
                newGhostDistance = -2

        new_food_dist = float(minFoodDistance) / matrix
        game_state = currentGameState.getPacmanPosition()
        final_value = float((1 - new_food_dist)) + float(food) + float(newGhostDistance)

        if succesorPosition != game_state:
            return float(final_value)
        else:
            return float(final_value) - 0.4

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #Ghosts.
        actions = gameState.getLegalActions(0)
        currentScore = -999
        returnAction = ''
        numberOfGhosts = gameState.getNumAgents() - 1
        
        def mini(gameState, depth, agentIndex):
            value = 999
            
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            actions = gameState.getLegalActions(agentIndex)
            
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == (gameState.getNumAgents() - 1):
                    value = min (value, maxi(successor, depth))
                    
                else:
                    value = min(value,mini(successor,depth,agentIndex+1))
                    
            return value
        
        def maxi(gameState, depth):
            value = -999
            currentDepth = depth + 1
            
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(0)
            
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                value = max (value, mini(successor, currentDepth, 1))
                
            return value
        
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            
            # Next level = min.
            score = mini(nextState, 0, 1)
            
            if score > currentScore:
                returnAction = action
                currentScore = score
                
        return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxi(gameState, depth, alpha, beta):
            currentDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)
            
            value = -999
            actions = gameState.getLegalActions(0)
            alphaNew = alpha
            
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                value = max (value, mini(successor, currentDepth, 1, alphaNew, beta))
                
                if value > beta:
                    return value
                
                alphaNew = max(alphaNew, value)
                
            return value
        
        #For Ghosts.
        def mini(gameState, depth, agentIndex, alpha, beta):
            value = 999
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            actions = gameState.getLegalActions(agentIndex)
            betaNew = beta
            
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == (gameState.getNumAgents() - 1):
                    value = min (value, maxi(successor, depth, alpha, betaNew))
                    
                    if value < alpha:
                        return value
                    betaNew = min(betaNew, value)
                else:
                    value = min(value, mini(successor, depth, agentIndex + 1, alpha, betaNew))
                    
                    if value < alpha:
                        return value
                    
                    betaNew = min(betaNew, value)
            
            return value

        # Acutal Alpha-Beta Pruning
        alpha = -999
        beta = 999
        currentScore = -999
        returnAction = ''
        actions = gameState.getLegalActions(0)
        
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = mini(nextState, 0, 1, alpha, beta)

            if score > currentScore:
                returnAction = action
                currentScore = score
   
            if score > beta:
                return returnAction
            
            alpha = max(alpha, score)
        
        return returnAction

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
        "*** YOUR CODE HERE ***"
        def maxi(gameState, depth):
            currentDepth = depth + 1
            
            if gameState.isWin() or gameState.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(gameState)
            
            value = -999
            actions = gameState.getLegalActions(0)
            
            for action in actions:
                successor= gameState.generateSuccessor(0, action)
                value = max (value, expectedLevel(successor, currentDepth, 1))
            
            return value
        
        
        def expectedLevel(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            actions = gameState.getLegalActions(agentIndex)
            totalValue = 0
            totalActions = len(actions)
            
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == (gameState.getNumAgents() - 1):
                    expectedvalue = maxi(successor, depth)
                else:
                    expectedvalue = expectedLevel(successor, depth, agentIndex + 1)
                
                totalValue = totalValue + expectedvalue
            
            if totalActions == 0:
                return  0
            
            return float(totalValue) / float(totalActions)
        
        
        actions = gameState.getLegalActions(0)
        currentScore = -999
        returnAction = ''
        
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = expectedLevel(nextState, 0, 1)
            
            if score > currentScore:
                returnAction = action
                currentScore = score
        
        return returnAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    scaredGhost = [ghostState.scaredTimer for ghostState in ghosts]
    
    foodList = food.asList()
    foodDistance = [0]
    
    for f in foodList:
        foodDistance.append(manhattanDistance(position, f))

    ghostLocation = []
    for ghost in ghosts:
        ghostLocation.append(ghost.getPosition())
    
    ghostDistance = [0]
    
    for l in ghostLocation:
        ghostDistance.append(manhattanDistance(position, l))

    totalPowerPellets = len(currentGameState.getCapsules())

    score = 0
    eatenFood = len(food.asList(False))           
    totalTimesScared = sum(scaredGhost)
    totalGhostDistances = sum(ghostDistance)
    foodDistances = 0
    
    if sum(foodDistance) > 0:
        foodDistances = 1.0 / sum(foodDistance)
        
    score += currentGameState.getScore()  + foodDistances + eatenFood

    if totalTimesScared > 0:    
        score +=   totalTimesScared + (-1 * totalPowerPellets) + (-1 * totalGhostDistances)
    else :
        score +=  totalGhostDistances + totalPowerPellets
    
    return score

# Abbreviation
better = betterEvaluationFunction
