import random
from tqdm import trange
from board import Board
from utils_display import print_
from agent_greedy import GreedyAgent
from agent_human import HumanAgent
from agent_minimax import MinimaxAgent

def match(agents, rounds=1, verbose=True):
    """ simulate a match between two agents """
    assert rounds > 0
    assert len(agents) == 2
    assert not (agents[0].is_human() and agents[1].is_human())  # at most one human agent
    assert not verbose or (not agents[0].is_human() and not agents[1].is_human())  # if there is a human agent must be verbose

    if agents[1].is_human(): 
        agents.reverse()  # human is always bottom player

    print(f'\n{rounds}-round match: {agents[0].name()} (bottom player) vs. {agents[1].name()} (top player)\n')
    match_score = [0, 0]

    for round in trange(rounds, ncols=80, disable=rounds < 10 or verbose):
        # intial setup
        print_(f'round {round + 1}:', silent=not verbose)
        board = Board()
        turn = random.choice([0, 1])

        while not board.is_complete():
            if not board.actions():  # forfeit turn if no moves
                turn = 1 - turn
                board = board.flip()
                continue

            board.print_board(flip=turn, with_options=agents[turn].is_human(), silent=not verbose)

            action = agents[turn].move(board)
            board, keep_turn = board.successor(action)

            if not keep_turn:
                turn = 1 - turn
                board = board.flip(mutate=True)
        
        # output result
        board.print_board(flip=turn, silent=not verbose)
        if board.score() == 0:
            print_("it's a tie!", silent=not verbose)
        else:
            winner = turn if board.score() > 0 else 1 - turn
            match_score[winner] += 1
            print_(f'\n{agents[winner].name()} ({["bottom", "top"][winner]} player) wins the round!', silent=not verbose)
    
    # output match result
    if match_score[0] == match_score[1]:
        print(f"\nit's a tie! {match_score[0]} to {match_score[1]}")
    else:
        winner = 0 if match_score[0] > match_score[1] else 1
        print(f'\n{agents[winner].name()} ({["bottom", "top"][winner]} player) wins the match {max(match_score)} to {min(match_score)}!')

def solitaire():
    """ simulate an agent playing a solitaire version of mancala in which the agent gets to keep making moves until there are no marbles on its side """
    agent = MinimaxAgent()

    board = Board()
    board.print_board()

    while board.actions():
        action = agent.move(board)
        board, _ = board.successor(action)
        board.print_board()

def main():
    agents = [MinimaxAgent(horizon=3), GreedyAgent()]

    match(agents, verbose=False, rounds=1000)

if __name__ == "__main__":
    main()
