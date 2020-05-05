import random
from board import Board
from agent_greedy import GreedyAgent
from agent_human import HumanAgent

def main():
    """ simulate a match between two agents """
    agents = [GreedyAgent(), HumanAgent()]

    assert not (agents[0].is_human() and agents[1].is_human())  # at most one human agent

    if agents[1].is_human(): 
        agents.reverse()  # human is always bottom player

    # intial setup
    print(f'\n{agents[0].name()} (bottom player) vs. {agents[1].name()} (top player)\n')
    board = Board()
    turn = random.choice([0, 1])

    while not board.is_complete():
        if not board.actions():  # forfeit turn if no moves
            turn = 1 - turn
            board = board.flip()
            continue

        board.print_board(flip=turn, with_options=agents[turn].is_human())

        action = agents[turn].move(board)
        board, keep_turn = board.successor(action)

        if not keep_turn:
            turn = 1 - turn
            board = board.flip()
    
    # output result
    board.print_board(flip=turn)
    if board.score() == 0:
        print("it's a tie!")
    else:
        winner = turn if board.score() > 0 else 1 - turn
        print(f'\n{agents[winner].name()} ({["bottom", "top"][winner]} player) wins!')

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
