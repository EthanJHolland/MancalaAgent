from agent import Agent
from display_utils import option_list_to_text

class HumanAgent(Agent):
    def move(self, board):
        choice = None
        options = list(map(str, board.actions()))
        option_str = option_list_to_text(options)

        while choice not in options:
            if choice:
                print(f'{choice} is not a valid move')
            choice = input(f'your move ({option_str}): ')
        
        return int(choice)
    
    def name(self):
        return 'human'

    def is_human(self):
        """ return True to indicate that agent is a human agent """
        return True
