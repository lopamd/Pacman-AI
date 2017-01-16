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
import sys

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
        
        #print "Current new position",newPos
        #print "Current Position:",currentGameState.getPacmanPosition()
        #print "Ghost states: ",successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
        
        foodlist = newFood.asList()
        min_manhattan_heuristic_food = sys.maxint
        for food in foodlist:
            manhattan_dist_food = util.manhattanDistance(newPos, food)
            if(min_manhattan_heuristic_food > manhattan_dist_food) and manhattan_dist_food != 0:
                min_manhattan_heuristic_food = manhattan_dist_food
            
        ghostlist = successorGameState.getGhostPositions()
        min_manhattan_heuristic_ghost = sys.maxint
        for ghost in ghostlist:
            manhattan_dist_ghost = util.manhattanDistance(newPos, ghost)
            if(min_manhattan_heuristic_ghost > manhattan_dist_ghost):
                min_manhattan_heuristic_ghost = manhattan_dist_ghost
                
        score = (min_manhattan_heuristic_ghost / min_manhattan_heuristic_food)+ max(newScaredTimes) + 5*successorGameState.getScore()
        return score

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
        "*** YOUR CODE HERE ***"
       
        def maxvalue(gameState,depth):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            max_v = (-float("inf"),None)
            actions = gameState.getLegalActions(0)
            for action in actions:
                successors = gameState.generateSuccessor(0,action)
                min_value_returned = minvalue(successors,depth+1)
                if(max_v[0] < min_value_returned[0]):
                    max_v = (min_value_returned[0],action)
            return max_v
    
        def minvalue(gameState, depth):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            min_v = (float("inf"),None)
            curr_agent_index = depth % gameState.getNumAgents()
            next_level_agent_index = (depth+1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(curr_agent_index)
            for action in actions:
                successors = gameState.generateSuccessor(curr_agent_index,action)
                if(next_level_agent_index == 0):
                    value_returned = maxvalue(successors,depth+1)
                else:
                    value_returned = minvalue(successors,depth+1)
                if(min_v[0] > value_returned[0]):
                    min_v = (value_returned[0],action)
            return min_v
        return maxvalue(gameState,0)[1]
     
 
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxvalue(gameState,depth,alpha,beta):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            max_v = (-float("inf"),None)
            actions = gameState.getLegalActions(0)
            for action in actions:
                successors = gameState.generateSuccessor(0,action)
                min_value_returned = minvalue(successors,depth+1,alpha,beta)
                if(min_value_returned[0] > max_v[0]):
                    max_v = (min_value_returned[0],action)
                '''
                alpha = max(max_v[0],alpha)
		        if(alpha > beta):
                    return max_v
		        '''
                if(max_v[0] > beta):
                    return max_v
                alpha = max(max_v[0],alpha)
            return max_v
    
        def minvalue(gameState, depth,alpha,beta):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            min_v = (float("inf"),None)
            curr_agent_index = depth % gameState.getNumAgents()
            next_level_agent_index = (depth+1) % gameState.getNumAgents()
            actions = gameState.getLegalActions(curr_agent_index)
            for action in actions:
                successors = gameState.generateSuccessor(curr_agent_index,action)
                if(next_level_agent_index == 0):
                    value_returned = maxvalue(successors,depth+1,alpha,beta)
                else:
                    value_returned = minvalue(successors,depth+1,alpha,beta)
                if(value_returned[0] < min_v[0]):
                    min_v = (value_returned[0],action)
                ''' 
		        if(beta < alpha):
                    return min_v
                beta = min(min_v[0],beta)
		        '''
                if(min_v[0] < alpha):
                    return min_v
                beta = min(min_v[0],beta)
            return min_v
        return maxvalue(gameState,0,-float("inf"),float("inf"))[1]

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
        def maxvalue(gameState,depth):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            max_v = (-float("inf"),None)
            actions = gameState.getLegalActions(0)
            for action in actions:
                successors = gameState.generateSuccessor(0,action)
                min_value_returned = expectvalue(successors,depth+1)
                if(max_v[0] < min_value_returned[0]):
                    max_v = (min_value_returned[0],action)
            return max_v
    
        def expectvalue(gameState, depth):
            if(depth == (self.depth * gameState.getNumAgents()) or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState),None)
            curr_agent_index = depth % gameState.getNumAgents()
            actions = gameState.getLegalActions(curr_agent_index)
            expecti_val = 0
            probability_val = 1.0/len(actions)
            next_level_agent_index = (depth+1) % gameState.getNumAgents()
            for action in actions:
                successors = gameState.generateSuccessor(curr_agent_index,action)
                if(next_level_agent_index == 0):
                    value_returned = maxvalue(successors,depth+1)
                else:
                    value_returned = expectvalue(successors,depth+1)
                expecti_val = expecti_val + (value_returned[0] * probability_val)
                expect = (expecti_val,action)
            return expect
        return maxvalue(gameState,0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: If ghosts are nearby for a successor state, pacman should avoid
      that sucessor but it should aggresively approach the food always. Thus, The evaluation
      function score should be inversely proportional to the minium food distance and directly
      proportion to minimum ghost distance. As seen in the last project, manhattan distance
      proved to be a good metric for measuring the distance between current state and goal state,
      that is choosen as the distance metric here.
 
      In addition to that, current game state score should be the highest factor while calculating
      the score as we are trying to eating all the food and maximize the score. That's why it has
      highest coefficient in the linear combination. It is also seen that average score increases
      upon increasing this coefficient.

      If a capsule is nearby or scared time is higher, the score should be higher because pacman
      can run and eat all the dots without worrying about the ghosts.

      I have also tried to use the minimum scared time as one of the parameter. Although, every
      pacman game was wining with this, average score was less than 1000. That's why it is not used.
       	
    """
    "*** YOUR CODE HERE ***"
        # Useful information you can extract from a GameState (pacman.py)
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
    #print "Current new position",newPos
    #print "Current Position:",currentGameState.getPacmanPosition()
    #print "Ghost states: ",successorGameState.getGhostPositions()
    "*** YOUR CODE HERE ***"
        
    foodlist = newFood.asList()
    min_manhattan_heuristic_food = sys.maxint
    for food in foodlist:
        manhattan_dist_food = util.manhattanDistance(newPos, food)
        if(min_manhattan_heuristic_food > manhattan_dist_food) and manhattan_dist_food != 0:
            min_manhattan_heuristic_food = manhattan_dist_food
            
    ghostlist = currentGameState.getGhostPositions()
    min_manhattan_heuristic_ghost = sys.maxint
    for ghost in ghostlist:
        manhattan_dist_ghost = util.manhattanDistance(newPos, ghost)
        if(min_manhattan_heuristic_ghost > manhattan_dist_ghost):
            min_manhattan_heuristic_ghost = manhattan_dist_ghost
    '''            
    min_manhattan_scaredTime = sys.maxint
    for ghost in ghostlist:
        manhattan_dist_scaredTime = util.manhattanDistance(newPos, ghost)
        if(min_manhattan_scaredTime > manhattan_dist_scaredTime):
            min_manhattan_scaredTime = manhattan_dist_scaredTime
            
    if(min_manhattan_scaredTime == 0):
         min_manhattan_scaredTime = -100          
    '''
    
    capsuleList = currentGameState.getCapsules()
    min_capsule_dist = sys.maxint
    for capsule in capsuleList:
        manhattan_dist_capsule = util.manhattanDistance(newPos, capsule)
        if(min_capsule_dist > manhattan_dist_capsule) and manhattan_dist_capsule != 0:
            min_capsule_dist = manhattan_dist_capsule
                
        if(min_manhattan_heuristic_ghost == 0):
            min_manhattan_heuristic_ghost = -500
        
    score = (min_manhattan_heuristic_ghost / min_manhattan_heuristic_food) +\
	    (2*max(newScaredTimes))  + 25 * currentGameState.getScore() + 1.0/min_capsule_dist
            
    return score    
    
# Abbreviation
better = betterEvaluationFunction

