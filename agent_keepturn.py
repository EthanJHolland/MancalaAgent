import random
from agent import Agent
from utils_agent import find_optimal

class KeepTurnAgent(Agent):
    def __init__(self, with_caching=True):
        super().__init__()
        if with_caching:
            self.cache = {}
        self.with_caching = with_caching

    def move(self, board):
        if self.with_caching and board.unique_string() in self.cache:
            best_actions, _ = self.cache[board.unique_string()] 
        else:
            best_actions, _ = self.maxreachable(board)

        return random.choice(best_actions)
    
    def maxreachable(self, board):
        if self.with_caching and board.unique_string() in self.cache:
            return self.cache[board.unique_string()]

        options = []
        for action in board.actions():
            next_board, keep_turn = board.successor(action)
            if keep_turn:
                value = self.maxreachable(next_board)[1]
            else:
                value = board.score()
            
            options.append((action, value))
        
        if not options:  # no more marbles on player's side
            return ([], board.score())
        
        result = find_optimal(options, order=max)
        if self.with_caching:
            self.cache[board.unique_string()] = result
        return result
    
    def name(self):
        return 'keep turn agent'