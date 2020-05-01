import copy
from utils import display

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
                result: [10, 1, 2, 3, 4, 5]
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

    def successor(self, action):
        """ returns a new board state with the result of the player taking the given action """
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
                    return (boardobj, Board.PLAYER)
                elif boardobj.board[r][c] == 1:  # ended in previously empty cup
                    return (boardobj, Board.OPPONENT)
                else:  # ended in non-empty cup so pick up marbles
                    marbles = boardobj.board[r][c]
                    boardobj.board[r][c] = 0
                
            r, c = next(r, c)

    def flip(self):
        """ gives the board from the perspective of the opponent """
        flipped = copy.copy(self)
        flipped.board[Board.PLAYER] = self.board[Board.OPPONENT]
        flipped.board[Board.OPPONENT] = self.board[Board.PLAYER]

        return flipped

    def print_board(self):
        """ prints the board 
        ===================================
        |    | 12| 11| 10| 9 | 8 | 7 |    |
        | 13 |---|---|---|---|---|---|  6 |
        |    | 0 | 1 | 2 | 3 | 4 | 5 |    |
        ===================================
        """
        def place(num, num_spaces, justify_left=False):
            extra = num_spaces - len(str(num))

            if extra % 2 == 0:
                return ' ' * (extra // 2) + str(num) + ' ' * (extra // 2)
            else:
                return ' ' * (extra // 2 + (not justify_left)) + str(num) + ' ' * (extra // 2 + justify_left)
        
        def row_string(row):
            return VERT + ' ' * end_width + VERT + VERT.join([place(n, cup_width) for n in row]) + VERT + ' ' * end_width + VERT


        end_width = 4
        cup_width = 3
        border_len = 2 * (end_width + 1) + self.length * (cup_width + 1) + 1

        VERT = '|'
        HBORDER = '='
        HMID = '-'

        out = [
            HBORDER * border_len,
            row_string(reversed(self.opponent_row())),  # reverse opponents row to see from player's perspective
            VERT + place(self.opponent_score(), end_width, True) + (VERT + HMID * 3) * self.length + VERT + place(self.player_score(), end_width) + VERT,
            row_string(self.player_row()),
            HBORDER * border_len
        ]

        display(out, self.animate)
    