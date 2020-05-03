import random
from agent import Agent

class GreedyAgent(Agent):
    """ choses the action which results in the highest score at the end of the action, regardless of who goes next """

    def move(self, board):
        options = []
        for action in board.actions():
            result, _ = board.successor(action)
            options.append((action, result.score()))
                
        best_score = max([score for _, score in options])
        best_actions = [action for action, score in options if score == best_score]

        return random.choice(best_actions)

