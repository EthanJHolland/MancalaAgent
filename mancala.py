import random
from board import Board
from agent_greedy import GreedyAgent

def main():
    """ simulate a match between two agents """
    agents = [GreedyAgent(), GreedyAgent()]

    board = Board()
    board.print_board()
    turn = random.choice([0, 1])

    while not board.is_complete():
        if not board.actions():  # forfeit turn if no moves
            turn = 1 - turn
            board = board.flip()
            continue
        
        action = agents[turn].move(board)
        board, keep_turn = board.successor(action)
        board.print_board()

        if not keep_turn:
            turn = 1 - turn
            board = board.flip()
    
    if board.score() == 0:
        print("it's a tie!")
    elif board.score() > 0:
        print(f'player {turn + 1} wins!')
    else:
        print(f'player {(1 - turn) + 1} wins!')


def solitaire():
    """ simulate an agent playing a solitaire version of mancala in which the agent gets to keep making moves until there are no marbles on its side """
    agent = GreedyAgent()

    board = Board()
    board.print_board()

    while board.actions():
        action = agent.move(board)
        board, _ = board.successor(action)
        board.print_board()


if __name__ == "__main__":
    main()
