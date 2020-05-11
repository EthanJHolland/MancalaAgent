import random
from agent import Agent
from utils_agent import random_optimal

class GreedyAgent(Agent):
    def move(self, board):
        """ choses the action which results in the highest score at the end of the action, regardless of who goes next """
        options = []
        for action in board.actions():
            result, _ = board.successor(action)
            options.append((action, result.score()))

        return random_optimal(options, order=max)[0]

    def name(self):
        return 'greedy agent'
