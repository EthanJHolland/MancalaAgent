import random
from agent import Agent
from utils_agent import find_optimal

class MinimaxAgent(Agent):
    def __init__(self, horizon=None):
        super().__init__()
        assert horizon is None or horizon > 0
        self.horizon = horizon

    def move(self, board):
        best_actions, _ = self.minimax(board, depth=0, is_min=False)
        return random.choice(best_actions)
    
    def minimax(self, board, depth, is_min):
        if depth == self.horizon or board.is_complete():
            return ([], self.evaluate(board))
        
        options = []
        for action in board.actions():
            next_board, keep_turn = board.successor(action)
            if keep_turn:
                _, value = self.minimax(next_board, depth + 1, is_min)
            else:
                _, value = self.minimax(next_board.flip(mutate=True), depth + 1, not is_min)
                value *= -1  # need to negate score value from opposite player's persepctive

            options.append((action, value))
        
        if not options:  # no valid moves - switch turn without incrementing depth
            return self.minimax(board.flip(mutate=True), depth, not is_min)

        return find_optimal(options, order=min if is_min else max)
    
    def evaluate(self, board):
        """ approximates the value of a board state to the player with the score """
        return board.score()

    def name(self):
        h_string = f' w/ horizon {self.horizon}' if self.horizon else ''
        return 'minimax agent' + h_string