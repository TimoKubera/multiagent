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


from re import X
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        Features of the evaluation function:
        1. Quantity of the food on the board
                - the fewer, the better
                - linear relationship
        2. Distance from pacman to the clostest food
                - the closer, the better
                - linear relationship
        3. Distance from pacman to the ghosts
                - the closer, the worse
                - relationship is -1/x, where x is the distance
        4. Game Score
                - the higher, the better
                - linear relationship
        """
        from util import manhattanDistance

        # 1. Quantity of the food on the board
        w2 = 1
        f2 = (lambda x: -x)
        quantity = 0
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    quantity += 1
        val2 = f2(quantity)

        # 2. Distance from pacman to the clostest food
        w1 = 1
        f1 = (lambda x: -x)
        min_dist = 99999

        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    manh_dist = manhattanDistance(newPos, (x, y))
                    if manh_dist < min_dist:
                        min_dist = manh_dist
        if quantity == 0: # if there is no food on the board, there is no distance to the closest food
            val1 = 0
        else:
            val1 = f1(min_dist)

        # 3. Distance from pacman to the ghosts
        w3 = 5
        f3 = (lambda x: -1/x)
        val3 = 0
        for ghost in newGhostStates:
            manh_dist = manhattanDistance(newPos, ghost.getPosition())
            if manh_dist > 0:
                val3 += f3(manh_dist)
            else:
                val3 = -99999

        # 4. Game Score
        w4 = 1
        val4 = successorGameState.getScore()

        return w1 * val1 + w2 * val2 + w3 * val3 + w4 * val4

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
        num_agents = gameState.getNumAgents()
        takeAction = ""

        def value(state, currDepth, agent=0):
            if state.isWin() or state.isLose() or currDepth == self.depth:
                return self.evaluationFunction(state)
            if agent == 0:
                return max_value(state, currDepth)
            else:
                return min_value(state, currDepth, agent)
            
        def max_value(state, currDepth, agent=0):
            nonlocal takeAction
            v = -9999
            next_agent = 1
            for action in state.getLegalActions(agent):
                new_v = value(state.generateSuccessor(agent, action), currDepth, next_agent)
                if new_v > v:
                    v = new_v
                    if currDepth == 0:
                        takeAction = action
            return v
        
        def min_value(state, currDepth, agent):
            v = 9999
            next_agent = (agent + 1) % num_agents
            if next_agent == 0:
                currDepth += 1
            for action in state.getLegalActions(agent):
                v = min(v, value(state.generateSuccessor(agent, action), currDepth, next_agent))
            return v

        currDepth = 0
        value(gameState, currDepth)
        return takeAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
