from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def move(self, board):
        """ choose a move to make from a given board state """
        pass

    @abstractmethod
    def name(self):
        """ display name for agent """
        pass

    def is_human(self):
        """ returns true iff agent is controlled manually by a human """
        return False