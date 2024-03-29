import copy
from utils_display import display_board

class Board:
    """ represents a mancala board
               opponent's side
    ===================================
    |    | 12| 11| 10| 9 | 8 | 7 |    |
    | 13 |---|---|---|---|---|---|  6 | <- player's goal
    |    | 0 | 1 | 2 | 3 | 4 | 5 |    |
    ===================================
                player's side

    [[0, 1, 2, 3, 4, 5, 6]
     [7, 8, 9, 10, 11, 12, 13]]
    """
    PLAYER = 0
    OPPONENT = 1

    def __init__(self, length=6, initial_marbles_per_cup=4, animate=False):
        self.length = length
        self.animate = animate
        
        self.board = [[initial_marbles_per_cup] * self.length + [0] for _ in range(2)]
    
    def __copy__(self):
        """ creates a new board with identical marble placement but which shares no references with this board """
        dup = Board(length=self.length, animate=self.animate)
        dup.board = copy.deepcopy(self.board)

        return dup
    
    def player_score(self):
        """ returns the number of marbles in the player's goal """
        return self.board[Board.PLAYER][self.length]
    
    def opponent_score(self):
        """ returns the number of marbles in the opponent's goal """
        return self.board[Board.OPPONENT][self.length]

    def score(self):
        """ returns the difference between the player's score and the opponent's score with positive values indicating the player is winning """
        return self.player_score() - self.opponent_score()

    def player_row(self):
        """ returns a list containing the # of marbles in each of the player's cups ordered from left to right from the persepctive of the player
            example:
                board:  ===================================     
                        |    | 12| 11| 10| 9 | 8 | 7 |    |
                        | 13 |---|---|---|---|---|---|  6 |
                        |    | 0 | 1 | 2 | 3 | 4 | 5 |    |
                        ===================================
                result: [0, 1, 2, 3, 4, 5]
        """
        return self.board[Board.PLAYER][:self.length]
    
    def opponent_row(self):
        """ returns a list containing the # of marbles in each of the opponent's cups ordered from left to right from the persepctive of the opponent
            example:
                board:  ===================================     
                        |    | 12| 11| 10| 9 | 8 | 7 |    |
                        | 13 |---|---|---|---|---|---|  6 |
                        |    | 0 | 1 | 2 | 3 | 4 | 5 |    |
                        ===================================
                result: [7, 8, 9, 10, 11, 12]
        """
        return self.board[Board.OPPONENT][:self.length]
    
    def is_complete(self):
        """ returns true iff all cups are empty (all marble's are in the goals) """
        return not (any(self.player_row()) or any(self.opponent_row()))

    def actions(self):
        """ gives a list of valid actions for the player under the board state """
        return [index for index, marbles in enumerate(self.player_row()) if marbles > 0]
    
    def opponent_actions(self):
        """ gives a list of valid actions for the opponent under the board state """
        return [index for index, marbles in enumerate(self.opponent_row()) if marbles > 0]

    def successor(self, action):
        """ returns a new board state with the result of the player taking the given action as well as a boolea which is true iff the player keeps their turn (landed in their goal) """
        assert action >= 0 and action < self.length and self.board[Board.PLAYER][action] > 0

        boardobj = copy.copy(self)

        def next(r, c):
            if r == Board.OPPONENT and c == boardobj.length - 1:  # skip opponents goal, next cup is start of own side of the board
                return (Board.PLAYER, 0)
           
            if c == boardobj.length:  # in own goal, next cup is on opponents side of board
                return (Board.OPPONENT, 0)
            
            return (r, c + 1)
        
        
        # pick up marbles
        marbles = boardobj.board[Board.PLAYER][action]
        boardobj.board[Board.PLAYER][action] = 0
        r, c = next(Board.PLAYER, action)
        
        while marbles:
            # place marble
            marbles -= 1
            boardobj.board[r][c] += 1

            if marbles == 0:
                if r == Board.PLAYER and c == self.length:  # ended in goal
                    return (boardobj, True)
                elif boardobj.board[r][c] == 1:  # ended in previously empty cup
                    return (boardobj, False)
                else:  # ended in non-empty cup so pick up marbles
                    marbles = boardobj.board[r][c]
                    boardobj.board[r][c] = 0
                
            r, c = next(r, c)

    def flip(self, mutate=False):
        """ gives the board from the perspective of the opponent, returning a new board object unless mutate is true """
        obj = self if mutate else copy.copy(self)
        obj.board.reverse()
        return obj
    
    def unique_string(self):
        """ returns a string such that two boards generate the same string iff they have the same board size and the same marble configuration (including goals) """
        return f"{','.join(map(str, self.player_row()))}|{','.join(map(str, self.opponent_row()))}|{self.player_score()}|{self.opponent_score()}"

    def print_board(self, flip=False, with_options=False, silent=False):
        """ if silent does nothing, otherwise prints the board, from a flipped perspective iff flip and also displaying options for the bottom player iff with_options """
        if not silent:
            if flip:
                display_board(self.opponent_row(), self.player_row(), self.opponent_score(), self.player_score(), self.animate, self.opponent_actions() if with_options else [])
            else:
                display_board(self.player_row(), self.opponent_row(), self.player_score(), self.opponent_score(), self.animate, self.actions() if with_options else [])
    