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
        "*** YOUR CODE HERE ***"

        
        score = 0.0
        currentFood = currentGameState.getFood()
        currentFood_PosList = currentFood.asList()
        min_distance_food = None
        min_distance_food_pos = None
        # food reward:
        for f_pos in currentFood_PosList:
          distance = manhattanDistance(f_pos, currentGameState.getPacmanPosition())
          if (min_distance_food is None or distance < min_distance_food):
            min_distance_food = distance
            min_distance_food_pos = f_pos
        # if newposition is closer to nearest food, give it more score
        score -= manhattanDistance(newPos, min_distance_food_pos)

        # ghost penalty:
        # Intuition: if pacman gets to close too ghost, give more penalty
        penalty = 0.
        for ghost in newGhostStates:
          # if it is normal scenario
          if ghost.scaredTimer == 0:
            # if too close too ghost:
            distance = manhattanDistance(ghost.getPosition(), newPos)
            if distance <= 3:
              penalty -= distance ** 2


      
        score += penalty
        return  score #default score
        #please change the return score as the score you want

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
        N = gameState.getNumAgents()
        def max_layer(gameState, agentIndex, depth):
          """
          Returns the (argmax_action, max_state_value) that can maximise state-action value
          """
          max_state_value = None
          argmax_action = None
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            # state value is min_layer's value
            _, state_value = min_layer(successor_gameState, agentIndex + 1, depth)

            if max_state_value is None:
              max_state_value = state_value
              argmax_action = action
            elif state_value > max_state_value:
              max_state_value = state_value
              argmax_action = action

          if max_state_value is None:
            # if it has no action to take
            return None, self.evaluationFunction(gameState)
          return argmax_action, max_state_value
        
        def min_layer(gameState, agentIndex, depth):
          """
          Return the (argmin_action, min_state_value) that can minimise state-action value
          """  
          min_state_value = None
          argmin_action = None
          
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            
            # if there is still ghost not been run
            if agentIndex + 1 < N:
              _, state_value = min_layer(successor_gameState, agentIndex=agentIndex+1, depth=depth)
            # if there is still depth remain to run
            elif depth > 1: 
              _, state_value = max_layer(successor_gameState, agentIndex=0, depth=depth-1) 
            # if it is the leaf node
            else:
              state_value = self.evaluationFunction(successor_gameState)
            # choose min
            if min_state_value is None:
              min_state_value = state_value
              argmin_action = action
            elif state_value < min_state_value:
              min_state_value = state_value
              argmin_action = action

          # if there is no action to take
          if min_state_value is None:
            return None, self.evaluationFunction(gameState)
          return argmin_action, min_state_value

        argmax_action, _ = max_layer(gameState, 0, self.depth)
        return argmax_action
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***" 
        N = gameState.getNumAgents()
        def max_layer(gameState, agentIndex, depth, alpha, beta):
          """
          Returns the (argmax_action, max_state_value) that can maximise state-action value
          """
          max_state_value = None
          argmax_action = None
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            # state value is min_layer's value
            _, state_value = min_layer(successor_gameState, agentIndex + 1, depth, alpha, beta)

            if max_state_value is None:
              max_state_value = state_value
              argmax_action = action
            elif state_value > max_state_value:
              max_state_value = state_value
              argmax_action = action

            # alpha beta pruning
            if beta is not None:
              if max_state_value > beta:
                return argmax_action, max_state_value
            if alpha is None:
              alpha = max_state_value
            else:
              alpha = max(max_state_value, alpha)

          if max_state_value is None:
            # if it has no action to take
            return None, self.evaluationFunction(gameState)
          return argmax_action, max_state_value

        def min_layer(gameState, agentIndex, depth, alpha, beta):
          """
          Return the (argmin_action, min_state_value) that can minimise state-action value
          """  
          min_state_value = None
          argmin_action = None
          
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            
            # if there is still ghost not been run
            if agentIndex + 1 < N:
              _, state_value = min_layer(successor_gameState, agentIndex=agentIndex+1, depth=depth, 
                alpha=alpha, beta=beta)
            # if there is still depth remain to run
            elif depth > 1: 
              _, state_value = max_layer(successor_gameState, agentIndex=0, depth=depth-1,
                alpha=alpha, beta=beta) 
            # if it is the leaf node
            else:
              state_value = self.evaluationFunction(successor_gameState)
            # choose min
            if min_state_value is None:
              min_state_value = state_value
              argmin_action = action
            elif state_value < min_state_value:
              min_state_value = state_value
              argmin_action = action

            # alpha beta pruning
            if alpha is not None:
              # if it is already smaller than alpha
              if min_state_value < alpha:
                return argmin_action, min_state_value
            if beta is None:
              beta = min_state_value
            else:
              beta = min(min_state_value, beta)

          # if there is no action to take
          if min_state_value is None:
            return None, self.evaluationFunction(gameState)
          return argmin_action, min_state_value

        argmax_action, _ = max_layer(gameState, 0, self.depth, None, None)
        return argmax_action



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
        N = gameState.getNumAgents()
        def max_layer(gameState, agentIndex, depth):
          """
          Returns the (argmax_action, max_state_value) that can maximise state-action value
          """
          max_state_value = None
          argmax_action = None
          
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            # min layer return expected value
            state_value = min_layer(successor_gameState, agentIndex + 1, depth)
          
            # store max state value's action
            if max_state_value is None:
              max_state_value = state_value
              argmax_action = action
            elif state_value > max_state_value:
              max_state_value = state_value
              argmax_action = action

          # if there is no action to take
          if max_state_value is None:
            # if it has no action to take
            return None, self.evaluationFunction(gameState)

          # return epxect state value
          return argmax_action, max_state_value
        
        def min_layer(gameState, agentIndex, depth):
          """
          Return the (argmin_action, min_state_value) that can minimise state-action value
          """  
          expect_state_value = 0
          action_len = len(gameState.getLegalActions(agentIndex))
          # Bellman-expectation 
          for action in gameState.getLegalActions(agentIndex):
            successor_gameState = gameState.generateSuccessor(agentIndex, action)
            
            # if there is still ghost not been run
            if agentIndex + 1 < N:
              state_value = min_layer(successor_gameState, agentIndex=agentIndex+1, depth=depth)
            # if there is still depth remain to run
            elif depth > 1: 
              _, state_value = max_layer(successor_gameState, agentIndex=0, depth=depth-1) 
            # if it is has depth over
            else:
              state_value = self.evaluationFunction(successor_gameState)
            
            expect_state_value += float(state_value) / float(action_len)

          # if there is no action to take
          if action_len == 0:
            return self.evaluationFunction(gameState)
          return expect_state_value
    
        argmax_action, _ = max_layer(gameState, 0, self.depth)
        return argmax_action

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

